"""
Probe 6b (Grounding, low-stakes profile): Cultural Label Plus Situational Variables

Companion to Probe 6. Same design, opposite corner of the situational space.

Probe 6 paired each cultural label with the most face-threatening profile
(Phigh_Sdistant_Ilarge) and found the label was not neutralized. This probe
pairs each label with the least face-threatening profile (Plow_Sclose_Ismall).

If the label still dominates here, situational context does not neutralize
cultural labels regardless of stakes. If the label's effect shrinks, the
Probe 6 result is specific to high-stakes configurations.

8 conditions x 25 trials = 200. Same model, temperature, max_tokens.

Usage:
    $env:ANTHROPIC_API_KEY="sk-ant-..."
    python probes/probe6b_grounding_lowstakes.py
    python analyze_lexical.py results/probe6b_grounding_lowstakes/trial_results.jsonl cultural_background
    python analyze_judge.py results/probe6b_grounding_lowstakes/trial_results.jsonl cultural_background --per-condition 10
"""

import json
import os
import time
from pathlib import Path
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

OUTPUT_DIR = Path("results/probe6b_grounding_lowstakes")
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

# Fixed situational profile: Probe 5 condition Plow_Sclose_Ismall
SITUATION = (
    "you and your manager treat each other as near-equals, "
    "you and your manager know each other well, "
    "and raising this concern is a minor matter"
)

TRIALS_PER_GROUP = 25
MODEL = "claude-opus-4-8"

TASK_PROMPT = (
    "You are a person with a {bg} cultural frame, in a workplace where {situation}. "
    "Your manager proposed a major project change you believe is flawed. "
    "Express your concerns naturally and authentically."
)


def run_trial(background, trial_num):
    try:
        msg = client.messages.create(
            model=MODEL,
            max_tokens=300,
            messages=[{"role": "user",
                       "content": TASK_PROMPT.format(bg=background, situation=SITUATION)}],
        )
        return {
            "probe": "probe6b_grounding_lowstakes",
            "cultural_background": background,
            "situation": "Plow_Sclose_Ismall",
            "trial": trial_num,
            "message": msg.content[0].text,
            "model": MODEL,
            "status": "success",
        }
    except Exception as e:
        return {
            "probe": "probe6b_grounding_lowstakes",
            "cultural_background": background,
            "situation": "Plow_Sclose_Ismall",
            "trial": trial_num,
            "error": str(e),
            "model": MODEL,
            "status": "error",
        }


def main():
    total = len(CULTURAL_BACKGROUNDS) * TRIALS_PER_GROUP
    print(f"Probe 6b grounding (low stakes): {len(CULTURAL_BACKGROUNDS)} labels x "
          f"{TRIALS_PER_GROUP} trials = {total} total")
    print(f"Fixed situation: Plow_Sclose_Ismall\n")

    done = 0
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
                    time.sleep(3)

    print(f"\nDone. Results written to {OUT_FILE}")


if __name__ == "__main__":
    main()
