"""
Cross-model replication of Probe 5 (situational variables) on GPT-4o.

Same 8 Brown & Levinson conditions and task prompt as probes/probe5_situational.py.
Tests whether the situational-variable effect transfers across model families,
given that the Probe 1 cultural-label effect did not (v7, section 4.5).

Resumable: re-running skips trials already present in the output file.
Writes raw JSONL, then a copy with typographic apostrophes normalized
(GPT-4o emits U+2019 in roughly a third of responses; Claude emits none).

Usage:
    $env:OPENAI_API_KEY="sk-..."
    python crossmodel_probe5.py --check       # verify provider access, no quota spent
    python crossmodel_probe5.py               # run all 200 trials
    python analyze_lexical.py results/crossmodel_probe5_openai_norm.jsonl condition
"""

import argparse
import json
import os
import sys
import time
from itertools import product
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("openai package not installed. Run: pip install openai")
    sys.exit(1)

RAW_FILE = Path("results/crossmodel_probe5.jsonl")
NORM_FILE = Path("results/crossmodel_probe5_openai_norm.jsonl")
RAW_FILE.parent.mkdir(parents=True, exist_ok=True)

MODEL = "gpt-4o"
TRIALS_PER_GROUP = 25
MAX_TOKENS = 300

# Identical to probes/probe5_situational.py
POWER_DISTANCE = {
    "low": "you and your manager treat each other as near-equals",
    "high": "your manager holds considerable authority over you",
}
SOCIAL_DISTANCE = {
    "close": "you and your manager know each other well",
    "distant": "you and your manager have a formal, arm's-length relationship",
}
IMPOSITION_SIZE = {
    "small": "raising this concern is a minor matter",
    "large": "raising this concern carries significant weight and risk",
}

CONDITIONS = [
    {"power_distance": p, "social_distance": s, "imposition_size": i}
    for p, s, i in product(POWER_DISTANCE, SOCIAL_DISTANCE, IMPOSITION_SIZE)
]

TASK_PROMPT = (
    "You are a person in a workplace where {power}, {social}, and {imposition}. "
    "Your manager proposed a major project change you believe is flawed. "
    "Express your concerns naturally and authentically."
)


def condition_label(cond):
    return f"P{cond['power_distance']}_S{cond['social_distance']}_I{cond['imposition_size']}"


def build_prompt(cond):
    return TASK_PROMPT.format(
        power=POWER_DISTANCE[cond["power_distance"]],
        social=SOCIAL_DISTANCE[cond["social_distance"]],
        imposition=IMPOSITION_SIZE[cond["imposition_size"]],
    )


def load_completed():
    """Return set of (condition_label, trial) already written, for resume."""
    done = set()
    if RAW_FILE.exists():
        with open(RAW_FILE, encoding="utf-8") as f:
            for line in f:
                try:
                    rec = json.loads(line)
                    if rec.get("status") == "success":
                        done.add((rec["condition"], rec["trial"]))
                except json.JSONDecodeError:
                    continue
    return done


def check_access(client):
    try:
        client.chat.completions.create(
            model=MODEL,
            max_tokens=5,
            messages=[{"role": "user", "content": "ping"}],
        )
        print(f"OK: {MODEL} reachable.")
        return True
    except Exception as e:
        print(f"FAIL: {e}")
        return False


def run_trial(client, cond, trial_num):
    label = condition_label(cond)
    base = {
        "probe": "crossmodel_probe5",
        "provider": "openai",
        "condition": label,
        "power_distance": cond["power_distance"],
        "social_distance": cond["social_distance"],
        "imposition_size": cond["imposition_size"],
        "trial": trial_num,
        "model": MODEL,
    }
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            messages=[{"role": "user", "content": build_prompt(cond)}],
        )
        base["message"] = resp.choices[0].message.content
        base["status"] = "success"
    except Exception as e:
        base["error"] = str(e)
        base["status"] = "error"
    return base


def normalize_apostrophes():
    """Write a copy of the raw file with U+2019 and U+2018 replaced by ASCII."""
    n = 0
    with open(RAW_FILE, encoding="utf-8") as fin, \
         open(NORM_FILE, "w", encoding="utf-8") as fout:
        for line in fin:
            rec = json.loads(line)
            if "message" in rec and rec["message"]:
                rec["message"] = (
                    rec["message"]
                    .replace("\u2019", "'")
                    .replace("\u2018", "'")
                )
            fout.write(json.dumps(rec) + "\n")
            n += 1
    print(f"Normalized {n} records -> {NORM_FILE}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true",
                        help="verify API access only, spend no quota")
    args = parser.parse_args()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY not set.")
        sys.exit(1)
    client = OpenAI(api_key=api_key)

    if args.check:
        sys.exit(0 if check_access(client) else 1)

    completed = load_completed()
    total = len(CONDITIONS) * TRIALS_PER_GROUP
    print(f"Cross-model Probe 5 on {MODEL}: {len(CONDITIONS)} conditions x "
          f"{TRIALS_PER_GROUP} trials = {total} total")
    if completed:
        print(f"Resuming: {len(completed)} already done.\n")
    else:
        print()

    done = len(completed)
    with open(RAW_FILE, "a", encoding="utf-8") as f:
        for cond in CONDITIONS:
            label = condition_label(cond)
            for i in range(1, TRIALS_PER_GROUP + 1):
                if (label, i) in completed:
                    continue
                result = run_trial(client, cond, i)
                f.write(json.dumps(result) + "\n")
                f.flush()
                done += 1
                status = "OK" if result["status"] == "success" else "ERR"
                print(f"[{done}/{total}] {label} #{i}: {status}")
                if result["status"] == "error":
                    time.sleep(3)

    print(f"\nRaw results: {RAW_FILE}")
    normalize_apostrophes()


if __name__ == "__main__":
    main()
