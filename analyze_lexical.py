"""
Lexical coding analysis for cultural validity probes.

Counts predefined linguistic markers in probe responses. Fully deterministic
and reproducible: no model judgment involved. Provides the objective backbone
for behavioral claims, to be compared against LLM-judge coding.

Marker categories are defined a priori from cross-cultural communication
research (directness, hedging, group orientation, deference, competence
signalling) and applied identically across all conditions.

Usage:
    python analyze_lexical.py results/probe1_expanded/trial_results.jsonl cultural_background
    python analyze_lexical.py results/probe2_expanded/trial_results.jsonl language
    python analyze_lexical.py results/probe3_expanded/trial_results.jsonl cultural_background
"""

import json
import re
import sys
from pathlib import Path
from collections import defaultdict
import statistics

# ---------------------------------------------------------------------------
# Marker definitions. Regex, case-insensitive, word-boundary anchored where
# sensible. Defined once and applied uniformly to every condition.
# ---------------------------------------------------------------------------

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
    "competence_hedge": [
        r"\bI don't actually have\b", r"\bI'm an AI\b", r"\bI am an AI\b",
        r"\bI can't (?:assess|evaluate|judge)\b", r"\bI should clarify\b",
        r"\bI don't have (?:a|any) (?:native|professional|real)\b",
        r"\bnot actually\b", r"\bI should be honest\b",
        r"\bI lack\b", r"\bI'm not (?:qualified|able)\b",
    ],
    "task_engagement": [
        r"\barchitecture\b", r"\bscalab", r"\blatency\b", r"\bthroughput\b",
        r"\bbottleneck\b", r"\bdatabase\b", r"\bAPI\b", r"\bservice\b",
        r"\bconsistency\b", r"\bpartition\b", r"\bcach", r"\bload\b",
        r"\bfailure mode\b", r"\bcoupling\b",
    ],
}

COMPILED = {
    cat: [re.compile(p, re.IGNORECASE) for p in pats]
    for cat, pats in MARKERS.items()
}


def score_text(text):
    """Return raw counts and per-100-word normalized rates for each category."""
    words = max(len(text.split()), 1)
    raw = {}
    norm = {}
    for cat, pats in COMPILED.items():
        n = sum(len(p.findall(text)) for p in pats)
        raw[cat] = n
        norm[cat] = round(n / words * 100, 3)
    return raw, norm, words


def load(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return [r for r in rows if r.get("status") == "success"]


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    path = sys.argv[1]
    group_key = sys.argv[2]

    rows = load(path)
    print(f"Loaded {len(rows)} successful trials from {path}")
    print(f"Grouping by: {group_key}\n")

    by_group = defaultdict(list)
    for r in rows:
        raw, norm, words = score_text(r["message"])
        r["_raw"] = raw
        r["_norm"] = norm
        r["_words"] = words
        by_group[r[group_key]].append(r)

    categories = list(MARKERS.keys())

    # ---- Per-group summary -------------------------------------------------
    header = f"{'condition':<28} {'n':>4} {'words':>7}  " + "  ".join(
        f"{c[:11]:>11}" for c in categories
    )
    print(header)
    print("-" * len(header))

    summary = {}
    for g in sorted(by_group):
        trials = by_group[g]
        mean_words = statistics.mean(t["_words"] for t in trials)
        means = {
            c: statistics.mean(t["_norm"][c] for t in trials) for c in categories
        }
        summary[g] = {
            "n": len(trials),
            "mean_words": round(mean_words, 1),
            "means_per_100w": {c: round(means[c], 3) for c in categories},
            "pct_trials_with_marker": {
                c: round(
                    100 * sum(1 for t in trials if t["_raw"][c] > 0) / len(trials), 1
                )
                for c in categories
            },
        }
        row = f"{g:<28} {len(trials):>4} {mean_words:>7.1f}  " + "  ".join(
            f"{means[c]:>11.2f}" for c in categories
        )
        print(row)

    # ---- Percent of trials containing each marker --------------------------
    print(f"\n\n% of trials containing at least one marker in category:\n")
    print(header)
    print("-" * len(header))
    for g in sorted(by_group):
        pcts = summary[g]["pct_trials_with_marker"]
        row = f"{g:<28} {summary[g]['n']:>4} {'':>7}  " + "  ".join(
            f"{pcts[c]:>10.1f}%" for c in categories
        )
        print(row)

    # ---- Spread across conditions -----------------------------------------
    print(f"\n\nSpread across conditions (max - min of per-100w means):\n")
    for c in categories:
        vals = [summary[g]["means_per_100w"][c] for g in summary]
        hi = max(vals); lo = min(vals)
        hi_g = [g for g in summary if summary[g]["means_per_100w"][c] == hi][0]
        lo_g = [g for g in summary if summary[g]["means_per_100w"][c] == lo][0]
        print(f"  {c:<20} spread={hi-lo:>6.2f}   high={hi_g} ({hi:.2f})   low={lo_g} ({lo:.2f})")

    # ---- Write JSON --------------------------------------------------------
    out = Path(path).parent / "lexical_analysis.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(
            {
                "source_file": str(path),
                "group_key": group_key,
                "n_trials": len(rows),
                "marker_definitions": MARKERS,
                "by_condition": summary,
            },
            f,
            indent=2,
        )
    print(f"\n\nWritten: {out}")


if __name__ == "__main__":
    main()
