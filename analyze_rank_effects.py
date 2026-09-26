"""
Rank agreement and main effects: situational vs cultural conditioning.

Two analyses, no new API calls:

1. Cross-model rank agreement. For each judged dimension, ranks the 8
   conditions by mean score on Claude and on GPT-4o, then computes Spearman
   rho. Run separately for Probe 1 (8 cultural labels) and Probe 5 (8
   situational profiles). The v7 paper found rho at or near zero under
   cultural labels; this reports whether situational profiles do better.

2. Factorial main effects for Probe 5. The 8 situational conditions are a
   2x2x2 design. For each dimension and each model, reports the mean
   difference between high and low levels of power distance, social
   distance, and imposition size. This turns "situational variables work"
   into "which variable moves which dimension, on which model."

Spearman is computed by hand; no scipy dependency.

Usage:
    python analyze_rank_effects.py \
        results/probe1_expanded/judge_analysis.json \
        results/crossmodel_probe1_judge.json \
        results/probe5_situational/judge_analysis.json \
        results/crossmodel_probe5_judge.json
"""

import json
import sys
from itertools import product
from pathlib import Path

DIMS = ["directness", "hedging", "deference",
        "group_orientation", "task_engagement", "self_doubt"]


def load_means(path):
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    return {cond: v["mean"] for cond, v in d["by_condition"].items()}


def rank(values):
    """Average ranks for ties, 1 = smallest."""
    idx = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(idx):
        j = i
        while j + 1 < len(idx) and values[idx[j + 1]] == values[idx[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[idx[k]] = avg
        i = j + 1
    return ranks


def spearman(x, y):
    n = len(x)
    rx, ry = rank(x), rank(y)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    dx = sum((a - mx) ** 2 for a in rx) ** 0.5
    dy = sum((b - my) ** 2 for b in ry) ** 0.5
    return num / (dx * dy) if dx and dy else 0.0


def rank_agreement(name, claude, gpt):
    conds = sorted(set(claude) & set(gpt))
    print(f"\n{'=' * 66}")
    print(f"CROSS-MODEL RANK AGREEMENT: {name}  ({len(conds)} conditions)")
    print(f"{'=' * 66}")
    print(f"{'dimension':<20}{'Spearman rho':>14}")
    print("-" * 34)
    out = {}
    for dim in DIMS:
        x = [claude[c][dim] for c in conds]
        y = [gpt[c][dim] for c in conds]
        rho = spearman(x, y)
        out[dim] = round(rho, 3)
        print(f"{dim:<20}{rho:>+14.3f}")
    return out


def main_effects(name, means):
    """means: {condition_label: {dim: score}} for the 8 Probe 5 conditions."""
    levels = {
        "power_distance":  ("Phigh", "Plow"),
        "social_distance": ("Sdistant", "Sclose"),
        "imposition_size": ("Ilarge", "Ismall"),
    }
    print(f"\n{'=' * 66}")
    print(f"MAIN EFFECTS (high minus low): {name}")
    print(f"{'=' * 66}")
    print(f"{'dimension':<20}{'power':>12}{'social dist':>14}{'imposition':>14}")
    print("-" * 60)
    out = {}
    for dim in DIMS:
        row = {}
        for var, (hi, lo) in levels.items():
            hi_vals = [m[dim] for c, m in means.items() if hi in c]
            lo_vals = [m[dim] for c, m in means.items() if lo in c]
            if hi_vals and lo_vals:
                row[var] = round(sum(hi_vals) / len(hi_vals)
                                 - sum(lo_vals) / len(lo_vals), 2)
            else:
                row[var] = None
        out[dim] = row
        p = row["power_distance"]
        s = row["social_distance"]
        i = row["imposition_size"]
        fmt = lambda v: f"{v:>+.2f}" if v is not None else "n/a"
        print(f"{dim:<20}{fmt(p):>12}{fmt(s):>14}{fmt(i):>14}")
    return out


def main():
    if len(sys.argv) != 5:
        print(__doc__)
        sys.exit(1)
    p1_claude, p1_gpt, p5_claude, p5_gpt = sys.argv[1:5]

    c1, g1 = load_means(p1_claude), load_means(p1_gpt)
    c5, g5 = load_means(p5_claude), load_means(p5_gpt)

    results = {}
    results["rank_agreement_cultural"] = rank_agreement(
        "Probe 1, cultural labels", c1, g1)
    results["rank_agreement_situational"] = rank_agreement(
        "Probe 5, situational profiles", c5, g5)
    results["main_effects_claude"] = main_effects("Probe 5, Claude", c5)
    results["main_effects_gpt4o"] = main_effects("Probe 5, GPT-4o", g5)

    print(f"""

{'=' * 66}
READING THIS RESULT
{'=' * 66}

Rank agreement. Spearman rho near zero means the two models order the
conditions differently: the conditioning label does not name a shared
construct. Rho meaningfully positive means the models agree on which
conditions produce more of a behavior, even if magnitudes differ. With
n=8 conditions, rho above ~0.6 is worth reporting; below that, treat
as no detectable agreement.

Main effects. Each cell is the mean score across the four conditions
where that variable is high, minus the mean across the four where it
is low. Positive deference under power_distance means high-power
conditions were more deferential. Brown & Levinson predicts: power and
social distance increase deference and hedging, decrease directness;
imposition size does the same but more weakly.
""")

    out = Path("results") / "rank_effects_analysis.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"Written: {out}")


if __name__ == "__main__":
    main()
