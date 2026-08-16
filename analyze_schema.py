"""
Schema and dependency graph analysis for the MatrAIx persona system.

Reproduces the results reported in the paper, sections 3.5 and 3.6:
  - permitted values for cultural_background and its render template
  - outgoing edge counts for five identity dimensions
  - documented vs. undocumented edge counts
  - edges from identity dimensions to competence dimensions
  - maximum conditional probability spread across identity values

Requires a local clone of the MatrAIx repository.

Usage:
    python analyze_schema.py /path/to/MatrAIx-Persona-8B
    python analyze_schema.py ~/MatrAIx-Persona-8B --json results/schema_analysis.json

The dependency graph is large (~25 MB) and is loaded fully into memory.

If the graph structure differs from what this script expects, run with
--inspect to print the observed structure instead of analyzing it.
"""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

SCHEMA_REL = Path("persona/schema/dimensions.json")
GRAPH_REL = Path("persona/synthesis/graph/full_dag.json")

IDENTITY_DIMS = [
    "cultural_background",
    "primary_language",
    "english_proficiency",
    "multilingualism",
    "demo_ethnicity_broad",
]

# Fields that constitute documentation. An edge carrying none of these is
# counted as undocumented (bare: edge_id, source, target, edge_weight, cpd).
DOC_FIELDS = [
    "rationale",
    "relation",
    "relation_type",
    "evidence_level",
    "strength",
    "confidence",
    "direction_semantics",
    "basis",
    "relationship_basis",
]

# Competence-bearing dimensions. Prefixes plus explicit names.
COMPETENCE_PREFIXES = ("skill_", "fam_", "prog_", "tool_")
COMPETENCE_NAMES = {
    "highest_education",
    "tech_savviness",
    "institution_tier",
    "academic_field",
    "seniority",
    "research_output",
}


def is_competence(target):
    return target.startswith(COMPETENCE_PREFIXES) or target in COMPETENCE_NAMES


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def load_json(path):
    if not path.exists():
        sys.exit(f"Not found: {path}\nCheck the MatrAIx clone path.")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def extract_edges(graph):
    """The edge list may sit at the top level or under a container key."""
    if isinstance(graph, list):
        return graph
    for key in ("edges", "directed_edges", "dag", "links"):
        if key in graph and isinstance(graph[key], list):
            return graph[key]
    for key, val in graph.items():
        if isinstance(val, list) and val and isinstance(val[0], dict):
            if "source" in val[0] and "target" in val[0]:
                return val
    sys.exit(
        "Could not locate the edge list in the graph file.\n"
        f"Top-level keys: {list(graph)[:20]}\n"
        "Rerun with --inspect."
    )


def extract_dimensions(schema):
    """Return {dimension_name: dimension_record}."""
    if isinstance(schema, dict):
        for key in ("dimensions", "schema"):
            if key in schema:
                schema = schema[key]
                break
    if isinstance(schema, dict):
        return schema
    if isinstance(schema, list):
        out = {}
        for i, d in enumerate(schema):
            if not isinstance(d, dict):
                continue
            name = d.get("name") or d.get("id") or d.get("key")
            if name:
                rec = dict(d)
                rec.setdefault("index", i)
                out[name] = rec
        return out
    sys.exit("Could not parse the schema file. Rerun with --inspect.")


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def cpt_max_spread(cpd):
    """
    Maximum probability difference between any two identity values.

    MatrAIx stores conditionals as a pairwise_conditional_matrix:

        {"type": "pairwise_conditional_matrix",
         "source_values": [...],           # rows
         "target_values": [...],           # columns
         "P_target_given_source": [[...]]} # row-major

    For each target outcome (column) we take the range across source values
    (rows), and return the largest such range. That is the most a single
    identity value can shift any one outcome probability.

    Also accepts a plain {identity_value: {outcome: p}} mapping as a fallback.
    Returns (spread, n_rows) or (None, 0) if unreadable.
    """
    if not isinstance(cpd, dict) or not cpd:
        return None, 0

    matrix = cpd.get("P_target_given_source")
    if isinstance(matrix, list) and matrix and isinstance(matrix[0], list):
        rows = [r for r in matrix if all(isinstance(x, (int, float)) for x in r)]
        if len(rows) < 2:
            return None, 0
        width = min(len(r) for r in rows)
        if width == 0:
            return None, 0
        spread = 0.0
        for j in range(width):
            col = [r[j] for r in rows]
            spread = max(spread, max(col) - min(col))
        return spread, len(rows)

    # Fallback: nested mapping form.
    rows = []
    for v in cpd.values():
        if isinstance(v, dict) and all(
            isinstance(x, (int, float)) for x in v.values()
        ):
            rows.append(v)
    if len(rows) < 2:
        return None, 0
    outcomes = set()
    for r in rows:
        outcomes |= set(r)
    spread = 0.0
    for o in outcomes:
        vals = [r[o] for r in rows if o in r]
        if len(vals) >= 2:
            spread = max(spread, max(vals) - min(vals))
    return spread, len(rows)


def identical_rows(cpd):
    """Count source values whose full outcome distribution is numerically identical."""
    matrix = cpd.get("P_target_given_source") if isinstance(cpd, dict) else None
    if not (isinstance(matrix, list) and matrix and isinstance(matrix[0], list)):
        return None
    counts = defaultdict(int)
    for r in matrix:
        counts[tuple(r)] += 1
    return max(counts.values()) if counts else None


def analyze(root, inspect=False):
    schema_raw = load_json(root / SCHEMA_REL)
    graph_raw = load_json(root / GRAPH_REL)

    if inspect:
        print("SCHEMA type:", type(schema_raw).__name__)
        if isinstance(schema_raw, dict):
            print("  keys:", list(schema_raw)[:20])
        print("GRAPH type:", type(graph_raw).__name__)
        if isinstance(graph_raw, dict):
            print("  keys:", list(graph_raw)[:20])
        edges = extract_edges(graph_raw)
        print(f"  edges: {len(edges)}")
        print("  sample edge:")
        print(json.dumps(edges[0], indent=4)[:1500])
        return None

    dims = extract_dimensions(schema_raw)
    edges = extract_edges(graph_raw)

    report = {"total_edges": len(edges), "dimensions": {}}
    print(f"Graph contains {len(edges)} directed edges.\n")

    # --- Schema: cultural_background -------------------------------------
    cb = dims.get("cultural_background")
    if cb:
        vals = cb.get("values") or cb.get("permitted_values") or cb.get("options")
        template = None
        for k in ("phrase_template", "template", "render", "phrase",
                  "render_template", "prompt_phrase", "phrasing"):
            if cb.get(k):
                template = cb[k]
                break
        print("cultural_background")
        print(f"  index:       {cb.get('index')}")
        print(f"  category:    {cb.get('category')}")
        print(f"  description: {cb.get('description')}")
        if template:
            print(f"  template:    {template}")
        else:
            print(f"  template:    not found under known keys")
            print(f"  record keys: {sorted(cb)}")
        print(f"  values ({len(vals) if vals else 0}):")
        for v in vals or []:
            print(f"    {v}")
        print()
        report["cultural_background_schema"] = {
            "index": cb.get("index"),
            "category": cb.get("category"),
            "description": cb.get("description"),
            "template": template,
            "record_keys": sorted(cb),
            "values": vals,
        }

    # --- Edges per identity dimension ------------------------------------
    by_source = defaultdict(list)
    for e in edges:
        by_source[e.get("source")].append(e)

    header = f"{'dimension':<24} {'edges':>7} {'documented':>11} {'to competence':>14}"
    print(header)
    print("-" * len(header))

    for dim in IDENTITY_DIMS:
        out = by_source.get(dim, [])
        documented = [e for e in out if any(f in e for f in DOC_FIELDS)]
        competence = [e for e in out if is_competence(str(e.get("target", "")))]

        print(f"{dim:<24} {len(out):>7} {len(documented):>11} {len(competence):>14}")

        spreads, spreads_bare = [], []
        for e in out:
            s, nrows = cpt_max_spread(e.get("cpd"))
            if s is None:
                continue
            rec = (s, str(e.get("target")), nrows)
            spreads.append(rec)
            if not any(f in e for f in DOC_FIELDS):
                spreads_bare.append(rec)

        over_002 = [t for s, t, _ in spreads_bare if s > 0.02]

        report["dimensions"][dim] = {
            "total_edges": len(out),
            "documented_edges": len(documented),
            "undocumented_edges": len(out) - len(documented),
            "edges_to_competence": len(competence),
            "documented_targets": sorted(str(e.get("target")) for e in documented),
            "max_cpt_spread_all": round(max(s for s, _, _ in spreads), 6) if spreads else None,
            "max_cpt_spread_undocumented": (
                round(max(s for s, _, _ in spreads_bare), 6) if spreads_bare else None
            ),
            "max_spread_target_undocumented": max(spreads_bare)[1] if spreads_bare else None,
            "cpt_tables_read": len(spreads),
            "cpt_tables_read_undocumented": len(spreads_bare),
            "undocumented_edges_over_0.02": over_002,
        }

    # --- Conditional probability spread detail ---------------------------
    print("\nConditional probability spread across identity values:")
    print("(section 3.6 reports the undocumented figure)")
    for dim in IDENTITY_DIMS:
        r = report["dimensions"][dim]
        if r["max_cpt_spread_all"] is None:
            print(f"  {dim:<24} no readable conditional tables")
            continue
        print(f"  {dim:<24} all edges:    max spread {r['max_cpt_spread_all']:.4f} "
              f"({r['cpt_tables_read']} tables)")
        if r["max_cpt_spread_undocumented"] is not None:
            print(f"  {'':<24} undocumented: max spread "
                  f"{r['max_cpt_spread_undocumented']:.4f} "
                  f"(target: {r['max_spread_target_undocumented']}, "
                  f"{r['cpt_tables_read_undocumented']} tables)")
            over = r["undocumented_edges_over_0.02"]
            print(f"  {'':<24} undocumented edges exceeding 0.02: {len(over)}"
                  + (f" ({', '.join(over[:5])})" if over else ""))

    # --- Identical distributions across identity values -------------------
    cb_out = by_source.get("cultural_background", [])
    identical = []
    for e in cb_out:
        n = identical_rows(e.get("cpd") or {})
        if n and n > 1:
            identical.append((n, str(e.get("target"))))
    if identical:
        identical.sort(reverse=True)
        print("\nEdges where multiple cultural values produce numerically "
              "identical distributions:")
        for n, t in identical[:10]:
            print(f"  {t:<32} {n} of 8 values identical")
        report["identical_distribution_edges"] = [
            {"target": t, "identical_values": n} for n, t in identical
        ]

    # --- Undocumented edge targets ---------------------------------------
    cb_edges = by_source.get("cultural_background", [])
    bare = [e for e in cb_edges if not any(f in e for f in DOC_FIELDS)]
    if bare:
        targets = sorted(str(e.get("target")) for e in bare)
        print(f"\ncultural_background: {len(bare)} undocumented edges.")
        print("  first 15 targets:", ", ".join(targets[:15]))
        report["cultural_background_bare_targets"] = targets

    # --- Identity-to-competence check ------------------------------------
    total_comp = sum(report["dimensions"][d]["edges_to_competence"] for d in IDENTITY_DIMS)
    print(
        f"\nIdentity-to-competence edges across all five dimensions: {total_comp}"
    )

    return report


def main():
    p = argparse.ArgumentParser()
    p.add_argument("matraix_root", help="path to a local MatrAIx clone")
    p.add_argument("--json", help="write full results to this path")
    p.add_argument("--inspect", action="store_true",
                   help="print observed file structure instead of analyzing")
    args = p.parse_args()

    root = Path(args.matraix_root).expanduser()
    report = analyze(root, inspect=args.inspect)

    if report and args.json:
        out = Path(args.json)
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        print(f"\nWritten: {out}")


if __name__ == "__main__":
    main()
