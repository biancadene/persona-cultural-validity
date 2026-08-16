"""
Probe 1-X: Cross-model replication (rate-limit tolerant).

Replicates Probe 1 on GPT-4o. Identical prompt, values, trial count, and
token limit to probe1_expanded.py; only the model and provider differ.

New OpenAI accounts have low per-minute rate limits. This version paces
requests and retries on 429 with exponential backoff, so a full run completes
without manual restarts.

Usage:
    $env:OPENAI_API_KEY="sk-proj-..."
    python probe1_gpt4o.py

    # if still rate limited, increase the pause:
    python probe1_gpt4o.py --delay 4
"""

import json
import os
import time
import argparse
from pathlib import Path
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

OUTPUT_DIR = Path("results/probe1_gpt4o")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUTPUT_DIR / "trial_results.jsonl"

CULTURAL_BACKGROUNDS = [
    "Individualist (Western)",
    "Collectivist (East Asian)",
    "South Asian",
    "Latin",
    "African",
    "Middle Eastern",
    "Indigenous",
    "Mixed / diaspora",
]

TRIALS_PER_GROUP = 25
MODEL = "gpt-4o"

TASK_PROMPT = (
    "You are a person with a {bg} cultural frame. Your manager proposed a major "
    "project change you believe is flawed. Express your concerns naturally and "
    "authentically."
)

MAX_RETRIES = 6


def run_trial(background, trial_num, base_delay):
    """Call the API, retrying with exponential backoff on rate limits."""
    base = {
        "probe": "probe1_gpt4o",
        "cultural_background": background,
        "trial": trial_num,
        "model": MODEL,
    }

    for attempt in range(MAX_RETRIES):
        try:
            resp = client.chat.completions.create(
                model=MODEL,
                max_tokens=300,
                messages=[
                    {"role": "user", "content": TASK_PROMPT.format(bg=background)}
                ],
            )
            return {
                **base,
                "message": resp.choices[0].message.content,
                "status": "success",
                "attempts": attempt + 1,
            }
        except Exception as e:
            msg = str(e)
            is_rate_limit = "429" in msg or "rate limit" in msg.lower()

            if is_rate_limit and attempt < MAX_RETRIES - 1:
                # exponential backoff: 5, 10, 20, 40, 80 seconds
                wait = base_delay * (2 ** attempt) + 3
                print(f"    rate limited, waiting {wait}s "
                      f"(attempt {attempt + 1}/{MAX_RETRIES})")
                time.sleep(wait)
                continue

            return {**base, "error": msg[:300], "status": "error",
                    "attempts": attempt + 1}

    return {**base, "error": "max retries exhausted", "status": "error",
            "attempts": MAX_RETRIES}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--delay", type=float, default=2.0,
                    help="seconds between requests (raise if rate limited)")
    args = ap.parse_args()

    total = len(CULTURAL_BACKGROUNDS) * TRIALS_PER_GROUP
    est_min = total * args.delay / 60

    print(f"Probe 1-X: cross-model replication on {MODEL}")
    print(f"{len(CULTURAL_BACKGROUNDS)} conditions x {TRIALS_PER_GROUP} trials "
          f"= {total} total")
    print(f"Pacing: {args.delay}s between requests (~{est_min:.0f} min minimum)")
    print("Prompt and design identical to probe1_expanded.py (Claude Opus 4.8)\n")

    done = 0
    errors = 0

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        for bg in CULTURAL_BACKGROUNDS:
            for i in range(1, TRIALS_PER_GROUP + 1):
                result = run_trial(bg, i, args.delay)
                f.write(json.dumps(result) + "\n")
                f.flush()
                done += 1

                if result["status"] == "success":
                    retry_note = "" if result["attempts"] == 1 else \
                        f" (after {result['attempts']} attempts)"
                    print(f"[{done}/{total}] {bg} #{i}: OK{retry_note}")
                else:
                    errors += 1
                    print(f"[{done}/{total}] {bg} #{i}: ERR")
                    print(f"    {result['error'][:140]}")

                time.sleep(args.delay)

    print(f"\nDone. {done - errors} succeeded, {errors} failed.")
    print(f"Results: {OUT_FILE}")

    if errors:
        print(f"\n{errors} trials failed. Re-run with a larger --delay if these")
        print("were rate limits, or check your OpenAI usage dashboard.")
    else:
        print("\nCompare against Claude:")
        print("  python compare_models.py")


if __name__ == "__main__":
    main()
