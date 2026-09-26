"""
Control: No Persona Conditioning

Same task as Probes 1 and 5 with no persona clause at all. Establishes
where each model sits on every measured dimension when unconditioned,
so that cultural-label spread and situational-variable spread can both
be read against a common baseline.

50 trials per model. Output is one JSONL per model with condition="control"
so analyze_lexical.py and analyze_judge.py run unchanged.

Usage:
    $env:ANTHROPIC_API_KEY="sk-ant-..."
    $env:OPENAI_API_KEY="sk-proj-..."
    python control_noPersona.py                 # both models
    python control_noPersona.py --model claude  # one model
    python control_noPersona.py --model openai
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

TASK_PROMPT = (
    "Your manager proposed a major project change you believe is flawed. "
    "Express your concerns naturally and authentically."
)

TRIALS = 50
MAX_TOKENS = 300

OUT_DIR = Path("results/control")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def run_claude():
    from anthropic import Anthropic
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key:
        print("ANTHROPIC_API_KEY not set. Skipping Claude.")
        return
    client = Anthropic(api_key=key)
    model = "claude-opus-4-8"
    out = OUT_DIR / "claude_trial_results.jsonl"
    print(f"Control on {model}: {TRIALS} trials -> {out}\n")
    with open(out, "w", encoding="utf-8") as f:
        for i in range(1, TRIALS + 1):
            rec = {"probe": "control", "condition": "control",
                   "trial": i, "model": model}
            try:
                msg = client.messages.create(
                    model=model, max_tokens=MAX_TOKENS,
                    messages=[{"role": "user", "content": TASK_PROMPT}],
                )
                rec["message"] = msg.content[0].text
                rec["status"] = "success"
            except Exception as e:
                rec["error"] = str(e)
                rec["status"] = "error"
                time.sleep(3)
            f.write(json.dumps(rec) + "\n")
            f.flush()
            print(f"[{i}/{TRIALS}] claude: {'OK' if rec['status']=='success' else 'ERR'}")


def run_openai():
    from openai import OpenAI
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        print("OPENAI_API_KEY not set. Skipping OpenAI.")
        return
    client = OpenAI(api_key=key)
    model = "gpt-4o"
    raw = OUT_DIR / "openai_trial_results.jsonl"
    norm = OUT_DIR / "openai_trial_results_norm.jsonl"
    print(f"Control on {model}: {TRIALS} trials -> {raw}\n")
    with open(raw, "w", encoding="utf-8") as f:
        for i in range(1, TRIALS + 1):
            rec = {"probe": "control", "condition": "control",
                   "trial": i, "model": model}
            try:
                resp = client.chat.completions.create(
                    model=model, max_tokens=MAX_TOKENS,
                    messages=[{"role": "user", "content": TASK_PROMPT}],
                )
                rec["message"] = resp.choices[0].message.content
                rec["status"] = "success"
            except Exception as e:
                rec["error"] = str(e)
                rec["status"] = "error"
                time.sleep(3)
            f.write(json.dumps(rec) + "\n")
            f.flush()
            print(f"[{i}/{TRIALS}] gpt-4o: {'OK' if rec['status']=='success' else 'ERR'}")

    # Apostrophe normalization, same as crossmodel scripts
    with open(raw, encoding="utf-8") as fin, open(norm, "w", encoding="utf-8") as fout:
        for line in fin:
            r = json.loads(line)
            if r.get("message"):
                r["message"] = r["message"].replace("\u2019", "'").replace("\u2018", "'")
            fout.write(json.dumps(r) + "\n")
    print(f"Normalized -> {norm}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", choices=["claude", "openai", "both"], default="both")
    args = p.parse_args()
    if args.model in ("claude", "both"):
        run_claude()
    if args.model in ("openai", "both"):
        run_openai()
    print("\nDone.")


if __name__ == "__main__":
    main()
