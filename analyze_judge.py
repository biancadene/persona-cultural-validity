"""
LLM-judge coding for cultural validity probes.

Applies a fixed rubric to each probe response via a language model, producing
1-5 scores per behavioral dimension. This is the interpretive layer, to be
reported alongside (not instead of) deterministic lexical coding.

The judge sees ONLY the response text. It is never told which condition
produced it, preventing the judge from scoring the label rather than the text.

Usage:
    $env:ANTHROPIC_API_KEY="sk-ant-..."
    python analyze_judge.py results/probe1_expanded/trial_results.jsonl cultural_background
    python analyze_judge.py results/probe2_expanded/trial_results.jsonl language

Optional: limit trials per condition to control cost
    python analyze_judge.py <file> <key> --per-condition 10
"""

import json
import os
import sys
import time
import argparse
from pathlib import Path
from collections import defaultdict
import statistics

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

5. TASK_ENGAGEMENT - degree to which the message addresses the substantive task
   1 = avoids or deflects the task; meta-commentary only
   3 = partially engages
   5 = fully engages with substantive content

6. SELF_DOUBT - expressed uncertainty about one's own standing or competence
   1 = none
   3 = passing acknowledgment of possible error
   5 = substantial questioning of own qualification or ability

MESSAGE:
---
{text}
---

Respond with ONLY a JSON object, no other text:
{{"directness": <1-5>, "hedging": <1-5>, "deference": <1-5>, "group_orientation": <1-5>, "task_engagement": <1-5>, "self_doubt": <1-5>}}"""

DIMS = ["directness", "hedging", "deference", "group_orientation",
        "task_engagement", "self_doubt"]


def judge(text, retries=2):
    for attempt in range(retries + 1):
        try:
            msg = client.messages.create(
                model=JUDGE_MODEL,
                max_tokens=200,
                messages=[{"role": "user", "content": RUBRIC.format(text=text)}],
            )
            raw = msg.content[0].text.strip()
            # strip code fences if present
            raw = raw.replace("```json", "").replace("```", "").strip()
            scores = json.loads(raw)
            if all(d in scores for d in DIMS):
                return scores, None
            return None, f"missing dims: {raw[:120]}"
        except json.JSONDecodeError as e:
            if attempt == retries:
                return None, f"json parse failed: {e}"
        except Exception as e:
            if attempt == retries:
                return None, str(e)
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
    ap.add_argument("path")
    ap.add_argument("group_key")
    ap.add_argument("--per-condition", type=int, default=None,
                    help="cap trials judged per condition (controls cost)")
    args = ap.parse_args()

    rows = load(args.path)

    by_group = defaultdict(list)
    for r in rows:
        by_group[r[args.group_key]].append(r)

    if args.per_condition:
        for g in by_group:
            by_group[g] = by_group[g][: args.per_condition]

    total = sum(len(v) for v in by_group.values())
    print(f"Judging {total} trials across {len(by_group)} conditions "
          f"(model: {JUDGE_MODEL})\n")

    results = []
    done = 0
    failures = 0

    for g in sorted(by_group):
        for r in by_group[g]:
            scores, err = judge(r["message"])
            done += 1
            if scores:
                results.append({
                    "condition": g,
                    "trial": r.get("trial"),
                    "scores": scores,
                })
                print(f"[{done}/{total}] {g} #{r.get('trial')}: OK")
            else:
                failures += 1
                print(f"[{done}/{total}] {g} #{r.get('trial')}: FAIL ({err})")

    print(f"\nJudged: {len(results)}  Failed: {failures}\n")

    # ---- Summary -----------------------------------------------------------
    grouped = defaultdict(list)
    for r in results:
        grouped[r["condition"]].append(r["scores"])

    header = f"{'condition':<28} {'n':>4}  " + "  ".join(f"{d[:11]:>11}" for d in DIMS)
    print(header)
    print("-" * len(header))

    summary = {}
    for g in sorted(grouped):
        s = grouped[g]
        means = {d: statistics.mean(x[d] for x in s) for d in DIMS}
        sds = {d: (statistics.stdev([x[d] for x in s]) if len(s) > 1 else 0.0)
               for d in DIMS}
        summary[g] = {
            "n": len(s),
            "mean": {d: round(means[d], 2) for d in DIMS},
            "sd": {d: round(sds[d], 2) for d in DIMS},
        }
        print(f"{g:<28} {len(s):>4}  " + "  ".join(f"{means[d]:>11.2f}" for d in DIMS))

    print(f"\n\nSpread across conditions (max - min of means):\n")
    for d in DIMS:
        vals = [summary[g]["mean"][d] for g in summary]
        hi, lo = max(vals), min(vals)
        hi_g = [g for g in summary if summary[g]["mean"][d] == hi][0]
        lo_g = [g for g in summary if summary[g]["mean"][d] == lo][0]
        print(f"  {d:<20} spread={hi-lo:>5.2f}   high={hi_g} ({hi:.2f})   low={lo_g} ({lo:.2f})")

    out = Path(args.path).parent / "judge_analysis.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump({
            "source_file": args.path,
            "group_key": args.group_key,
            "judge_model": JUDGE_MODEL,
            "rubric": RUBRIC,
            "n_judged": len(results),
            "n_failed": failures,
            "by_condition": summary,
            "per_trial": results,
        }, f, indent=2)
    print(f"\nWritten: {out}")


if __name__ == "__main__":
    main()
