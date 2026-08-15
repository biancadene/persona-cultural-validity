"""
Probe 1 (expanded): Cultural Background and Communication Directness

Tests all 8 cultural_background values from the MatrAIx schema, enabling
comparison between orientation-fused values (Individualist/Collectivist)
and orientation-free values (South Asian, Latin, African, Middle Eastern).

Values match persona/schema/dimensions.json index 24 exactly.

Usage:
    $env:ANTHROPIC_API_KEY="sk-ant-..."
    python probe1_expanded.py
"""

import json
import os
import time
from pathlib import Path
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

OUTPUT_DIR = Path("results/probe1_expanded")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUTPUT_DIR / "trial_results.jsonl"

# Exact schema values from persona/schema/dimensions.json, dimension index 24
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
MODEL = "claude-opus-4-8"

# Uses MatrAIx's actual phrase template: "with a {value} cultural frame"
TASK_PROMPT = (
    "You are a person with a {bg} cultural frame. Your manager proposed a major "
    "project change you believe is flawed. Express your concerns naturally and "
    "authentically."
)


def run_trial(background, trial_num):
    try:
        msg = client.messages.create(
            model=MODEL,
            max_tokens=300,
            messages=[{"role": "user", "content": TASK_PROMPT.format(bg=background)}],
        )
        return {
            "probe": "probe1_expanded",
            "cultural_background": background,
            "trial": trial_num,
            "message": msg.content[0].text,
            "model": MODEL,
            "status": "success",
        }
    except Exception as e:
        return {
            "probe": "probe1_expanded",
            "cultural_background": background,
            "trial": trial_num,
            "error": str(e),
            "model": MODEL,
            "status": "error",
        }


def main():
    total = len(CULTURAL_BACKGROUNDS) * TRIALS_PER_GROUP
    print(f"Probe 1 expanded: {len(CULTURAL_BACKGROUNDS)} conditions x "
          f"{TRIALS_PER_GROUP} trials = {total} total\n")

    done = 0
    # Append incrementally so a crash doesn't lose completed trials
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        for bg in CULTURAL_BACKGROUNDS:
            for i in range(1, TRIALS_PER_GROUP + 1):
                result = run_trial(bg, i)
                f.write(json.dumps(result) + "\n")
                f.flush()
                done += 1
                status = "OK" if result["status"] == "success" else "ERR"
                print(f"[{done}/{total}] {bg} #{i}: {status}")
                if result["status"] == "error":
                    # brief pause on error in case it's rate limiting
                    time.sleep(3)

    print(f"\nDone. Results written to {OUT_FILE}")


if __name__ == "__main__":
    main()
