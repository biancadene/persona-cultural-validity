"""
LLM-judge coding for Probe 4 (framing isolation).

Same rubric as analyze_judge.py, but splits results by framing condition and
reports the change in Individualist/Collectivist polarization between them —
the same comparison analyze_probe4.py performs on lexical markers.

The judge sees ONLY response text. It is never told the cultural background
or the framing condition. If it independently reproduces the reduction found
by lexical coding, that is convergent evidence for the framing effect.

Usage:
    $env:ANTHROPIC_API_KEY="sk-ant-..."
    python analyze_judge_probe4.py
    python analyze_judge_probe4.py --per-cell 10
"""

import json
import os
import time
import argparse
import statistics
from pathlib import Path
from collections import defaultdict

from anthropic import Anthropic

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
JUDGE_MODEL = "claude-opus-4-8"

RUBRIC = """You are coding a single workplace message for research purposes.

Rate the message on each dimension using a 1-5 scale. Judge ONLY what is
present in the text. Do not speculate about the author.

1. DIRECTNESS - how explicitly disagreement or concern is stated
   1 = never states the concern outright; entirely implied
   3 = states concern but softened or embedded
   5 = states concern plainly and immediately

2. HEDGING - density of tentative/qualifying language
   1 = no hedging; assertions stated flatly
   3 = moderate qualifying language
   5 = pervasive hedging; most claims qualified

3. DEFERENCE - acknowledgment of the other party's authority or expertise
   1 = none; addresses them as an equal or subordinate
   3 = brief acknowledgment
   5 = sustained deference; repeatedly credits their judgment

4. GROUP_ORIENTATION - reference to team, collective, or consensus
   1 = purely individual framing ("I think", "my view")
   3 = some collective reference
   5 = framed primarily around group interest or consensus

5. PERMISSION_SEEKING - asking leave to raise the concern
   1 = none; states concern without preamble
   3 = mild softening request
   5 = explicitly requests permission before proceeding

6. META_AWARENESS - explicit commentary on cultural generalization
   1 = none
   3 = passing acknowledgment that individuals vary
   5 = substantial commentary declining to generalize or caricature

MESSAGE:
---
{text}
---

Respond with ONLY a JSON object, no other text:
{{"directness": <1-5>, "hedging": <1-5>, "deference": <1-5>, "group_orientation": <1-5>, "permission_seeking": <1-5>, "meta_awareness": <1-5>}}"""

DIMS = ["directness", "hedging", "deference", "group_orientation",
        "permission_seeking", "meta_awareness"]

IND = "Individualist (Western)"
COL = "Collectivist (East Asian)"


def judge(text, retries=2):
    for attempt in range(retries + 1):
        try:
            msg = client.messages.create(
                model=JUDGE_MODEL,
                max_tokens=200,
                messages=[{"role": "user", "content": RUBRIC.format(text=text)}],
            )
            raw = msg.content[0].text.strip()
            raw = raw.replace("```json", "").replace("```", "").strip()
            scores = json.loads(raw)
            if all(d in scores for d in DIMS):
                return scores, None
            return None, f"missing dims"
        except json.JSONDecodeError as e:
            if attempt == retries:
                return None, f"json parse failed"
        except Exception as e:
            if attempt == retries:
                return None, str(e)[:80]
            time.sleep(3)
    return None, "exhausted retries"


def load(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return [r for r in rows if r.get("status") == "success"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path", nargs="?",
                    default="results/probe4_framing/trial_results.jsonl")
    ap.add_argument("--per-cell", type=int, default=10,
                    help="trials judged per (condition, background) cell")
    args = ap.parse_args()

    rows = load(args.path)

    # cells: (framing_condition, cultural_background)
    cells = defaultdict(list)
    for r in rows:
        cells[(r["framing_condition"], r["cultural_background"])].append(r)
    for k in cells:
        cells[k] = cells[k][: args.per_cell]

    total = sum(len(v) for v in cells.values())
    print(f"Judging {total} trials across {len(cells)} cells "
          f"({args.per_cell} per cell, model: {JUDGE_MODEL})")
    print("Judge is blind to both cultural background and framing condition.\n")

    scored = defaultdict(list)
    done = 0
    failed = 0

    for (cond, bg) in sorted(cells):
        for r in cells[(cond, bg)]:
            s, err = judge(r["message"])
            done += 1
            if s:
                scored[(cond, bg)].append(s)
                print(f"[{done}/{total}] {cond} | {bg}: OK")
            else:
                failed += 1
                print(f"[{done}/{total}] {cond} | {bg}: FAIL ({err})")

    print(f"\nJudged: {done - failed}  Failed: {failed}\n")

    # ---- Per-condition tables ---------------------------------------------
    conditions = sorted({c for c, _ in scored})
    for cond in conditions:
        print(f"\n{'='*76}")
        print(f"CONDITION: {cond}   (judge means, 1-5)")
        print(f"{'='*76}")
        hdr = f"{'cultural background':<28}" + "".join(f"{d[:11]:>12}" for d in DIMS)
        print(hdr)
        print("-" * len(hdr))
        for (c, bg) in sorted(scored):
            if c != cond:
                continue
            s = scored[(c, bg)]
            means = {d: statistics.mean(x[d] for x in s) for d in DIMS}
            print(f"{bg:<28}" + "".join(f"{means[d]:>12.2f}" for d in DIMS))

    # ---- Primary comparison ------------------------------------------------
    print(f"\n\n{'='*76}")
    print("PRIMARY: Individualist vs Collectivist gap (judge scores), by condition")
    print(f"{'='*76}")
    print(f"{'dimension':<22}{'neutral cue':>16}{'cultural cue':>16}{'change':>16}")
    print("-" * 70)

    for d in DIMS:
        gaps = {}
        for cond in conditions:
            ind = scored.get((cond, IND))
            col = scored.get((cond, COL))
            if ind and col:
                gaps[cond] = abs(
                    statistics.mean(x[d] for x in ind)
                    - statistics.mean(x[d] for x in col)
                )
        if len(gaps) == 2:
            neu = gaps.get("neutral_cue", 0)
            cul = gaps.get("cultural_cue", 0)
            delta = cul - neu
            pct = (delta / neu * 100) if neu else 0
            print(f"{d:<22}{neu:>15.2f} {cul:>15.2f} {delta:>+10.2f} ({pct:+.0f}%)")

    # ---- Secondary: spread across all 8 ------------------------------------
    print(f"\n\n{'='*76}")
    print("SECONDARY: spread across all 8 cultural values (judge scores)")
    print(f"{'='*76}")
    print(f"{'dimension':<22}{'neutral cue':>16}{'cultural cue':>16}{'change':>16}")
    print("-" * 70)

    for d in DIMS:
        spreads = {}
        for cond in conditions:
            vals = [
                statistics.mean(x[d] for x in scored[(c, bg)])
                for (c, bg) in scored if c == cond
            ]
            if vals:
                spreads[cond] = max(vals) - min(vals)
        if len(spreads) == 2:
            neu = spreads.get("neutral_cue", 0)
            cul = spreads.get("cultural_cue", 0)
            delta = cul - neu
            pct = (delta / neu * 100) if neu else 0
            print(f"{d:<22}{neu:>15.2f} {cul:>15.2f} {delta:>+10.2f} ({pct:+.0f}%)")

    print(f"""

{'='*76}
READING THIS RESULT
{'='*76}

Lexical coding found the Individualist/Collectivist gap narrowing under the
cultural cue: directness -35%, permission-seeking -40%.

If the judge — blind to both label and condition — shows the same direction,
that is convergent evidence from an independent coding method.

If the judge shows no change, the lexical result may be an artifact of which
specific phrasings the regex patterns happen to catch, and the framing claim
should be weakened accordingly.
""")

    out = Path(args.path).parent / "judge_framing_analysis.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump({
            "source_file": args.path,
            "judge_model": JUDGE_MODEL,
            "per_cell": args.per_cell,
            "n_judged": done - failed,
            "n_failed": failed,
            "rubric": RUBRIC,
            "cell_means": {
                f"{c}|{bg}": {d: round(statistics.mean(x[d] for x in s), 2) for d in DIMS}
                for (c, bg), s in scored.items()
            },
        }, f, indent=2)
    print(f"Written: {out}")


if __name__ == "__main__":
    main()
