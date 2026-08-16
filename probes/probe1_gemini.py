"""
Probe 1-X: Cross-model replication on Gemini.

Replicates Probe 1 (cultural background, implicit framing) on Google's Gemini
to test whether the observed effect generalizes across model families or is
specific to Claude.

Prompt, cultural values, trial count, and token limit are identical to
probe1_expanded.py. Only the model and provider differ.

Includes pacing and exponential backoff for rate limits.

Setup:
    python -m pip install google-genai

Usage:
    $env:GEMINI_API_KEY="your-key"
    python probe1_gemini.py

    # if rate limited, increase pacing:
    python probe1_gemini.py --delay 4
"""

import json
import os
import time
import argparse
from pathlib import Path

from google import genai
from google.genai import types

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

OUTPUT_DIR = Path("results/probe1_gemini")
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
MODEL = "gemini-2.0-flash"

# Identical to probe1_expanded.py
TASK_PROMPT = (
    "You are a person with a {bg} cultural frame. Your manager proposed a major "
    "project change you believe is flawed. Express your concerns naturally and "
    "authentically."
)

MAX_RETRIES = 6


def run_trial(background, trial_num, base_delay):
    base = {
        "probe": "probe1_gemini",
        "cultural_background": background,
        "trial": trial_num,
        "model": MODEL,
    }

    for attempt in range(MAX_RETRIES):
        try:
            resp = client.models.generate_content(
                model=MODEL,
                contents=TASK_PROMPT.format(bg=background),
                config=types.GenerateContentConfig(max_output_tokens=300),
            )
            return {
                **base,
                "message": resp.text,
                "status": "success",
                "attempts": attempt + 1,
            }
        except Exception as e:
            msg = str(e)
            rate_limited = (
                "429" in msg
                or "rate" in msg.lower()
                or "quota" in msg.lower()
                or "resource_exhausted" in msg.lower()
            )

            if rate_limited and attempt < MAX_RETRIES - 1:
                wait = base_delay * (2 ** attempt) + 3
                print(f"    rate limited, waiting {wait:.0f}s "
                      f"(attempt {attempt + 1}/{MAX_RETRIES})")
                time.sleep(wait)
                continue

            return {**base, "error": msg[:300], "status": "error",
                    "attempts": attempt + 1}

    return {**base, "error": "max retries exhausted", "status": "error",
            "attempts": MAX_RETRIES}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--delay", type=float, default=1.5,
                    help="seconds between requests")
    args = ap.parse_args()

    total = len(CULTURAL_BACKGROUNDS) * TRIALS_PER_GROUP
    est = total * args.delay / 60

    print(f"Probe 1-X: cross-model replication on {MODEL}")
    print(f"{len(CULTURAL_BACKGROUNDS)} conditions x {TRIALS_PER_GROUP} trials "
          f"= {total} total")
    print(f"Pacing: {args.delay}s between requests (~{est:.0f} min minimum)")
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
                    note = "" if result["attempts"] == 1 else \
                        f" (after {result['attempts']} attempts)"
                    print(f"[{done}/{total}] {bg} #{i}: OK{note}")
                else:
                    errors += 1
                    print(f"[{done}/{total}] {bg} #{i}: ERR")
                    print(f"    {result['error'][:140]}")

                time.sleep(args.delay)

    print(f"\nDone. {done - errors} succeeded, {errors} failed.")
    print(f"Results: {OUT_FILE}")

    if not errors:
        print("\nCompare against Claude:")
        print("  python compare_models.py results/probe1_expanded/trial_results.jsonl "
              "results/probe1_gemini/trial_results.jsonl")


if __name__ == "__main__":
    main()
