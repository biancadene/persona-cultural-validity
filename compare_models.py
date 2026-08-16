"""
Cross-model comparison for Probe 1.

Loads Claude and GPT-4o results from the identical probe and reports marker
prevalence side by side, so the key question is directly readable: does the
cultural-label effect generalize across model families?

Marker definitions are identical to analyze_lexical.py.

Usage:
    python compare_models.py
    python compare_models.py results/probe1_expanded/trial_results.jsonl results/probe1_gpt4o/trial_results.jsonl
"""

import json
import re
import sys
from pathlib import Path
from collections import defaultdict

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
}

COMPILED = {c: [re.compile(p, re.I) for p in pats] for c, pats in MARKERS.items()}
CATS = list(MARKERS.keys())

IND = "Individualist (Western)"
COL = "Collectivist (East Asian)"


def has(text, cat):
    return any(p.search(text) for p in COMPILED[cat])


def load(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return [r for r in rows if r.get("status") == "success"]


def table(rows):
    by_bg = defaultdict(list)
    for r in rows:
        by_bg[r["cultural_background"]].append(r)
    return {
        bg: {c: 100 * sum(1 for t in ts if has(t["message"], c)) / len(ts)
             for c in CATS}
        for bg, ts in by_bg.items()
    }, {bg: len(ts) for bg, ts in by_bg.items()}


def main():
    if len(sys.argv) >= 3:
        p_claude, p_gpt = sys.argv[1], sys.argv[2]
    else:
        p_claude = "results/probe1_expanded/trial_results.jsonl"
        p_gpt = "results/probe1_gpt4o/trial_results.jsonl"

    claude_rows = load(p_claude)
    gpt_rows = load(p_gpt)

    t_claude, n_claude = table(claude_rows)
    t_gpt, n_gpt = table(gpt_rows)

    model_claude = claude_rows[0].get("model", "claude")
    model_gpt = gpt_rows[0].get("model", "gpt")

    print(f"{model_claude}: {len(claude_rows)} trials")
    print(f"{model_gpt}: {len(gpt_rows)} trials\n")

    # ---- Side by side per marker ------------------------------------------
    for cat in CATS:
        print(f"\n{'='*74}")
        print(f"{cat.upper()}  (% of trials containing marker)")
        print(f"{'='*74}")
        print(f"{'cultural background':<28}{model_claude:>18}{model_gpt:>18}{'diff':>10}")
        print("-" * 74)
        bgs = sorted(set(t_claude) | set(t_gpt))
        for bg in bgs:
            c = t_claude.get(bg, {}).get(cat)
            g = t_gpt.get(bg, {}).get(cat)
            if c is None or g is None:
                continue
            print(f"{bg:<28}{c:>17.0f}%{g:>17.0f}%{g-c:>+9.0f}")

    # ---- Headline comparison ----------------------------------------------
    print(f"\n\n{'='*74}")
    print("HEADLINE: Individualist vs Collectivist gap, by model")
    print(f"{'='*74}")
    print(f"{'marker':<24}{model_claude:>18}{model_gpt:>18}{'diff':>12}")
    print("-" * 74)

    for cat in CATS:
        gc = gg = None
        if IND in t_claude and COL in t_claude:
            gc = abs(t_claude[IND][cat] - t_claude[COL][cat])
        if IND in t_gpt and COL in t_gpt:
            gg = abs(t_gpt[IND][cat] - t_gpt[COL][cat])
        if gc is not None and gg is not None:
            print(f"{cat:<24}{gc:>15.0f}pt{gg:>15.0f}pt{gg-gc:>+9.0f}pt")

    print(f"""

{'='*74}
READING THIS RESULT
{'='*74}

If GPT-4o shows gaps of similar magnitude and direction, the cultural-label
effect generalizes across model families. That substantially strengthens the
claim that stereotyping originates in model priors rather than in any one
model's training.

If GPT-4o shows markedly smaller gaps, the effect is Claude-specific. That is
also a real finding, and arguably more actionable for practitioners choosing
a model for persona simulation.

If GPT-4o shows LARGER gaps, the Claude results understate the general
problem.

Note that marker definitions were developed against Claude output. If GPT-4o
phrases directness or hedging differently, lexical coding may undercount it.
Check raw responses before concluding a null.
""")

    out = Path("results") / "cross_model_comparison.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump({
            "claude_file": p_claude,
            "gpt_file": p_gpt,
            "claude_model": model_claude,
            "gpt_model": model_gpt,
            "n_claude": len(claude_rows),
            "n_gpt": len(gpt_rows),
            "claude_table": {bg: {c: round(v, 1) for c, v in d.items()}
                             for bg, d in t_claude.items()},
            "gpt_table": {bg: {c: round(v, 1) for c, v in d.items()}
                          for bg, d in t_gpt.items()},
        }, f, indent=2)
    print(f"Written: {out}")


if __name__ == "__main__":
    main()
