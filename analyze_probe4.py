"""
Analysis for Probe 4 (framing isolation).

Computes marker prevalence separately for each framing condition, then
reports the change in polarization between conditions.

Primary comparison: the Individualist vs Collectivist gap, which showed the
largest effect in Probes 1 and 3. Also reports overall spread across all
eight cultural values, as a less cherry-picked measure.

Usage:
    python analyze_probe4.py
    python analyze_probe4.py results/probe4_framing/trial_results.jsonl
"""

import json
import re
import sys
import statistics
from pathlib import Path
from collections import defaultdict

# Marker definitions kept identical to analyze_lexical.py so results are
# directly comparable across probes.
MARKERS = {
    "hedging": [
        r"\bperhaps\b", r"\bmaybe\b", r"\bmight\b", r"\bI wonder\b",
        r"\bI think\b", r"\bpossibly\b", r"\bsomewhat\b", r"\ba bit\b",
        r"\bkind of\b", r"\bsort of\b", r"\bcould be\b", r"\bI'm not sure\b",
        r"\bit seems\b", r"\bI believe\b", r"\bpotentially\b",
    ],
    "directness": [
        r"\bI disagree\b", r"\bthis won't work\b", r"\bthis will not work\b",
        r"\bI'm concerned\b", r"\bthe problem is\b", r"\bhere's (?:what|why|the)\b",
        r"\bI want to be (?:straight|direct|clear|upfront)\b",
        r"\bto be (?:blunt|honest|direct|clear)\b", r"\bI don't think\b",
        r"\bwe should\b", r"\bmy concern is\b", r"\bflag\b",
    ],
    "permission_seeking": [
        r"\bwould it be (?:alright|okay|helpful|possible)\b",
        r"\bmay I\b", r"\bcould I\b", r"\bif I may\b",
        r"\bwould you mind\b", r"\bis it okay if\b",
        r"\bcan I (?:ask|raise|share|offer)\b", r"\bif that's alright\b",
    ],
    "group_reference": [
        r"\bthe team\b", r"\bour team\b", r"\bcolleagues\b", r"\btogether\b",
        r"\bconsensus\b", r"\bthe group\b", r"\beveryone\b",
        r"\bothers (?:have|might|may)\b", r"\bas a team\b", r"\bwe've\b",
    ],
    "deference": [
        r"\bI (?:respect|appreciate) your\b", r"\byour experience\b",
        r"\byour expertise\b", r"\byou may have\b",
        r"\byou (?:probably|likely) (?:know|have|considered)\b",
        r"\bI could be (?:wrong|missing)\b", r"\bI may be missing\b",
        r"\byou've thought\b", r"\bdefer\b",
    ],
    "meta_commentary": [
        r"\bcaricature\b", r"\bstereotyp", r"\bgeneraliz", r"\boversimplif",
        r"\bvary widely\b", r"\bnot a monolith\b", r"\bI should be honest\b",
        r"\bflatten", r"\breduce (?:this|it) to\b", r"\bindividuals? (?:differ|vary)\b",
    ],
}

COMPILED = {c: [re.compile(p, re.I) for p in pats] for c, pats in MARKERS.items()}
CATS = list(MARKERS.keys())
FOCUS = ["directness", "permission_seeking", "group_reference"]


def has_marker(text, cat):
    return any(p.search(text) for p in COMPILED[cat])


def load(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return [r for r in rows if r.get("status") == "success"]


def pct_table(trials_by_bg):
    """Return {background: {category: pct_of_trials_with_marker}}"""
    out = {}
    for bg, trials in trials_by_bg.items():
        out[bg] = {
            c: 100 * sum(1 for t in trials if has_marker(t["message"], c)) / len(trials)
            for c in CATS
        }
    return out


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "results/probe4_framing/trial_results.jsonl"
    rows = load(path)
    print(f"Loaded {len(rows)} successful trials\n")

    by_cond = defaultdict(lambda: defaultdict(list))
    for r in rows:
        by_cond[r["framing_condition"]][r["cultural_background"]].append(r)

    tables = {cond: pct_table(bgs) for cond, bgs in by_cond.items()}

    # ---- Per-condition tables ---------------------------------------------
    for cond in sorted(tables):
        print(f"\n{'='*78}")
        print(f"CONDITION: {cond}")
        print(f"{'='*78}")
        hdr = f"{'cultural background':<28}" + "".join(f"{c[:13]:>15}" for c in CATS)
        print(hdr)
        print("-" * len(hdr))
        for bg in sorted(tables[cond]):
            n = len(by_cond[cond][bg])
            row = f"{bg:<28}" + "".join(f"{tables[cond][bg][c]:>14.0f}%" for c in CATS)
            print(row)

    # ---- Primary comparison: Individualist vs Collectivist gap ------------
    IND = "Individualist (Western)"
    COL = "Collectivist (East Asian)"

    print(f"\n\n{'='*78}")
    print("PRIMARY COMPARISON: Individualist vs Collectivist gap, by condition")
    print(f"{'='*78}")
    print(f"{'marker':<22}{'neutral cue':>16}{'cultural cue':>16}{'change':>14}")
    print("-" * 68)

    for c in FOCUS:
        gaps = {}
        for cond in tables:
            if IND in tables[cond] and COL in tables[cond]:
                gaps[cond] = abs(tables[cond][IND][c] - tables[cond][COL][c])
        if len(gaps) == 2:
            neu = gaps.get("neutral_cue", float("nan"))
            cul = gaps.get("cultural_cue", float("nan"))
            delta = cul - neu
            pct = (delta / neu * 100) if neu else 0
            print(f"{c:<22}{neu:>14.0f}pt{cul:>14.0f}pt{delta:>+9.0f}pt ({pct:+.0f}%)")

    # ---- Secondary: overall spread across all 8 values --------------------
    print(f"\n\n{'='*78}")
    print("SECONDARY: spread across all 8 cultural values (max - min)")
    print(f"{'='*78}")
    print(f"{'marker':<22}{'neutral cue':>16}{'cultural cue':>16}{'change':>14}")
    print("-" * 68)

    for c in CATS:
        spreads = {}
        for cond in tables:
            vals = [tables[cond][bg][c] for bg in tables[cond]]
            spreads[cond] = max(vals) - min(vals)
        if len(spreads) == 2:
            neu = spreads.get("neutral_cue", 0)
            cul = spreads.get("cultural_cue", 0)
            delta = cul - neu
            pct = (delta / neu * 100) if neu else 0
            print(f"{c:<22}{neu:>14.0f}pt{cul:>14.0f}pt{delta:>+9.0f}pt ({pct:+.0f}%)")

    # ---- Interpretation aid ----------------------------------------------
    print(f"\n\n{'='*78}")
    print("READING THIS RESULT")
    print(f"{'='*78}")
    print("""
If gaps SHRINK under the cultural cue but the task is identical and both
conditions received a reflection sentence, that supports the claim that
cultural salience specifically reduces stereotyped output.

If gaps are UNCHANGED, the Probe 1 vs Probe 3 difference was likely driven
by the task difference, not by framing. Report accordingly.

If gaps GROW, making culture salient amplifies rather than dampens the
effect - which would contradict the Probe 3 result and needs reporting.

Note also the meta_commentary column: Probe 3 showed qualitative evidence of
the model explicitly declining to caricature. If that marker rises under the
cultural cue, it supports a reasoning-based mechanism.
""")

    out = Path(path).parent / "framing_analysis.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump({
            "source_file": str(path),
            "n_trials": len(rows),
            "marker_definitions": MARKERS,
            "by_condition": {
                cond: {bg: {c: round(v, 1) for c, v in cats.items()}
                       for bg, cats in tbl.items()}
                for cond, tbl in tables.items()
            },
        }, f, indent=2)
    print(f"Written: {out}")


if __name__ == "__main__":
    main()
