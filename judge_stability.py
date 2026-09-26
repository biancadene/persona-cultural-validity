"""
Judge stability: run analyze_judge.py's rubric N times on a file, save each
run to its own JSON, and write an averaged by_condition summary.

The Claude judge at default temperature produces different scores on rerun.
A single run gives one rho; three runs give a mean and a range. This script
does the runs and the averaging. The averaged file has the same shape as a
single judge_analysis.json, so analyze_rank_effects.py accepts it directly.

Usage:
    $env:ANTHROPIC_API_KEY="sk-ant-..."
    python judge_stability.py <trial_results.jsonl> <group_key> --runs 3 --per-condition 10 --out results/<name>_judge_avg.json

Each individual run is saved as <out>_run1.json, <out>_run2.json, etc.
The averaged file is saved at <out>.
"""

import argparse
import json
import os
import statistics
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

DIMS = ["directness", "hedging", "deference", "group_orientation",
        "task_engagement", "self_doubt"]


def run_judge_once(path, group_key, per_condition, out_path):
    """Invoke analyze_judge.py, then move its default output to out_path."""
    cmd = [sys.executable, "analyze_judge.py", path, group_key]
    if per_condition:
        cmd += ["--per-condition", str(per_condition)]
    subprocess.run(cmd, check=True)
    default_out = Path(path).parent / "judge_analysis.json"
    default_out.replace(out_path)
    with open(out_path, encoding="utf-8") as f:
        return json.load(f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("group_key")
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--per-condition", type=int, default=10)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    stem = out.with_suffix("")

    runs = []
    for i in range(1, args.runs + 1):
        run_out = Path(f"{stem}_run{i}.json")
        print(f"\n{'=' * 60}\nRUN {i}/{args.runs} -> {run_out}\n{'=' * 60}")
        runs.append(run_judge_once(args.path, args.group_key,
                                   args.per_condition, run_out))

    # Average by_condition means across runs
    conds = sorted(runs[0]["by_condition"].keys())
    averaged = {}
    for c in conds:
        means = {}
        ranges = {}
        for d in DIMS:
            vals = [r["by_condition"][c]["mean"][d] for r in runs]
            means[d] = round(statistics.mean(vals), 2)
            ranges[d] = round(max(vals) - min(vals), 2)
        averaged[c] = {
            "n": runs[0]["by_condition"][c]["n"],
            "runs": args.runs,
            "mean": means,
            "range_across_runs": ranges,
        }

    print(f"\n\n{'=' * 60}\nAVERAGED ACROSS {args.runs} RUNS\n{'=' * 60}")
    header = f"{'condition':<28} " + "  ".join(f"{d[:11]:>11}" for d in DIMS)
    print(header)
    print("-" * len(header))
    for c in conds:
        print(f"{c:<28} " + "  ".join(f"{averaged[c]['mean'][d]:>11.2f}" for d in DIMS))

    print(f"\nMax range across runs, per dimension:")
    for d in DIMS:
        mx = max(averaged[c]["range_across_runs"][d] for c in conds)
        print(f"  {d:<20} {mx:.2f}")

    with open(out, "w", encoding="utf-8") as f:
        json.dump({
            "source_file": args.path,
            "group_key": args.group_key,
            "judge_model": runs[0]["judge_model"],
            "runs": args.runs,
            "per_condition": args.per_condition,
            "by_condition": averaged,
        }, f, indent=2)
    print(f"\nWritten: {out}")


if __name__ == "__main__":
    main()
