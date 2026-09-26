"""
Probe 5 (Condition A): Situational Variables Replace Cultural Labels

Same task as Probe 1 (manager proposes flawed change; express concerns).
Cultural background label is removed entirely. In its place, three
Brown & Levinson (1987) situational variables are specified directly:

    power_distance   : low | high
    social_distance  : close | distant
    imposition_size  : small | large

2 x 2 x 2 = 8 conditions, mirroring the 8 cultural_background values in
Probe 1. 25 trials each, n=200. Same model, temperature, max_tokens.

Tests the paper's stated next experiment (v7, Limitations): whether
situational variables predict the behaviors measured (directness,
deference, hedging, permission-seeking) without a cultural label present.

Usage:
    $env:ANTHROPIC_API_KEY="sk-ant-..."
    python probes/probe5_situational.py
"""

import json
import os
import time
from itertools import product
from pathlib import Path
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

OUTPUT_DIR = Path("results/probe5_situational")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUTPUT_DIR / "trial_results.jsonl"

# Brown & Levinson situational variables, each binary
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

TRIALS_PER_GROUP = 25
MODEL = "claude-opus-4-8"

# Task text is identical to Probe 1. Only the persona clause changes:
# cultural frame is replaced by three situational descriptors.
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


def run_trial(cond, trial_num):
    label = condition_label(cond)
    try:
        msg = client.messages.create(
            model=MODEL,
            max_tokens=300,
            messages=[{"role": "user", "content": build_prompt(cond)}],
        )
        return {
            "probe": "probe5_situational",
            "condition": label,
            "power_distance": cond["power_distance"],
            "social_distance": cond["social_distance"],
            "imposition_size": cond["imposition_size"],
            "trial": trial_num,
            "message": msg.content[0].text,
            "model": MODEL,
            "status": "success",
        }
    except Exception as e:
        return {
            "probe": "probe5_situational",
            "condition": label,
            "power_distance": cond["power_distance"],
            "social_distance": cond["social_distance"],
            "imposition_size": cond["imposition_size"],
            "trial": trial_num,
            "error": str(e),
            "model": MODEL,
            "status": "error",
        }


def main():
    total = len(CONDITIONS) * TRIALS_PER_GROUP
    print(f"Probe 5 situational: {len(CONDITIONS)} conditions x "
          f"{TRIALS_PER_GROUP} trials = {total} total\n")

    done = 0
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        for cond in CONDITIONS:
            label = condition_label(cond)
            for i in range(1, TRIALS_PER_GROUP + 1):
                result = run_trial(cond, i)
                f.write(json.dumps(result) + "\n")
                f.flush()
                done += 1
                status = "OK" if result["status"] == "success" else "ERR"
                print(f"[{done}/{total}] {label} #{i}: {status}")
                if result["status"] == "error":
                    time.sleep(3)

    print(f"\nDone. Results written to {OUT_FILE}")


if __name__ == "__main__":
    main()
