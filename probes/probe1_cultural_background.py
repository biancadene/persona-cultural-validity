"""
Probe 1: Cultural Background and Communication Directness

Tests whether cultural_background persona conditioning produces systematic
differences in communication directness, hedging language, and group
orientation when a persona is asked to disagree with a manager.

Usage:
    export ANTHROPIC_API_KEY="sk-ant-..."
    python probe1_cultural_background.py
"""

import json
import os
from pathlib import Path
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

OUTPUT_DIR = Path("results/probe1_cultural_background")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CULTURAL_BACKGROUNDS = [
    "Individualist (Western)",
    "Collectivist (East Asian)",
]

TRIALS_PER_GROUP = 10

TASK_PROMPT = (
    "You are {bg}. Your manager proposed a major project change you believe "
    "is flawed. Express your concerns naturally and authentically."
)


def run_trial(background: str, trial_num: int) -> dict:
    try:
        msg = client.messages.create(
            model="claude-opus-4-8",
            max_tokens=200,
            messages=[
                {"role": "user", "content": TASK_PROMPT.format(bg=background)}
            ],
        )
        return {
            "bg": background,
            "trial": trial_num,
            "message": msg.content[0].text,
            "status": "success",
        }
    except Exception as e:
        return {
            "bg": background,
            "trial": trial_num,
            "error": str(e),
            "status": "error",
        }


def main():
    results = []
    for bg in CULTURAL_BACKGROUNDS:
        for i in range(TRIALS_PER_GROUP):
            print(f"{bg} [{i + 1}/{TRIALS_PER_GROUP}]...", end=" ", flush=True)
            result = run_trial(bg, i + 1)
            results.append(result)
            print(result["status"].upper())

    out_file = OUTPUT_DIR / "trial_results.jsonl"
    with open(out_file, "w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")

    print(f"\nDone. Results written to {out_file}")


if __name__ == "__main__":
    main()
