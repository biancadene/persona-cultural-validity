"""
Probe 4: Isolating framing salience.

Probes 1 and 3 differed in both task and framing, confounding the framing
interpretation. This probe holds the task constant and varies ONLY whether
the reflection cue directs attention to cultural background.

Both conditions receive a reflection sentence of comparable length and
structure, so the comparison is not confounded by prompt length or by the
presence of a reflection instruction per se.

  Condition A (neutral cue):  reflect on general workplace habit
  Condition B (cultural cue): reflect on cultural background

If polarization drops under B but not A, the effect is attributable to
cultural salience specifically rather than to reflection in general.

8 cultural values x 2 conditions x 25 trials = 400 trials.

Usage:
    $env:ANTHROPIC_API_KEY="sk-ant-..."
    python probe4_framing.py
"""

import json
import os
import time
from pathlib import Path
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

OUTPUT_DIR = Path("results/probe4_framing")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUTPUT_DIR / "trial_results.jsonl"

# Exact schema values, persona/schema/dimensions.json index 24
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

TRIALS_PER_CELL = 25
MODEL = "claude-opus-4-8"

# Identical task in both conditions. Identical persona conditioning.
# The ONLY difference is the object of the reflection cue.
#
# Cue lengths are closely matched:
#   neutral:  "Consider how you typically handle disagreement at work."   (9 words)
#   cultural: "Consider how your cultural background shapes the way you
#              handle disagreement."                                      (11 words)

PROMPTS = {
    "neutral_cue": (
        "You are a person with a {bg} cultural frame. "
        "Consider how you typically handle disagreement at work. "
        "Your manager proposed a major project change you believe is flawed. "
        "Express your concerns naturally and authentically."
    ),
    "cultural_cue": (
        "You are a person with a {bg} cultural frame. "
        "Consider how your cultural background shapes the way you handle disagreement. "
        "Your manager proposed a major project change you believe is flawed. "
        "Express your concerns naturally and authentically."
    ),
}


def run_trial(background, condition, trial_num):
    base = {
        "probe": "probe4_framing",
        "cultural_background": background,
        "framing_condition": condition,
        "trial": trial_num,
        "model": MODEL,
    }
    try:
        msg = client.messages.create(
            model=MODEL,
            max_tokens=300,
            messages=[{
                "role": "user",
                "content": PROMPTS[condition].format(bg=background),
            }],
        )
        return {**base, "message": msg.content[0].text, "status": "success"}
    except Exception as e:
        return {**base, "error": str(e), "status": "error"}


def main():
    conditions = list(PROMPTS.keys())
    total = len(CULTURAL_BACKGROUNDS) * len(conditions) * TRIALS_PER_CELL

    print(f"Probe 4: framing isolation")
    print(f"{len(CULTURAL_BACKGROUNDS)} cultural values x {len(conditions)} conditions "
          f"x {TRIALS_PER_CELL} trials = {total} total")
    print("Task held constant; only the reflection cue varies.\n")

    done = 0
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        for condition in conditions:
            for bg in CULTURAL_BACKGROUNDS:
                for i in range(1, TRIALS_PER_CELL + 1):
                    result = run_trial(bg, condition, i)
                    f.write(json.dumps(result) + "\n")
                    f.flush()
                    done += 1
                    status = "OK" if result["status"] == "success" else "ERR"
                    print(f"[{done}/{total}] {condition} | {bg} #{i}: {status}")
                    if result["status"] == "error":
                        time.sleep(3)

    print(f"\nDone. Results written to {OUT_FILE}")
    print("\nAnalyze each condition separately, then compare:")
    print("  python analyze_probe4.py")


if __name__ == "__main__":
    main()
