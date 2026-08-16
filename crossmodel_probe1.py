"""
Cross-model replication of Probe 1 (poles only).

Tests whether the Individualist/Collectivist directness gap observed on
claude-opus-4-8 replicates on OpenAI and Gemini.

Usage:
    python crossmodel_probe1.py --check          # access check only, ~2 calls
    python crossmodel_probe1.py --provider gemini
    python crossmodel_probe1.py --provider openai
    python crossmodel_probe1.py --provider both

Output: results/crossmodel_probe1.jsonl  (append-only, resumable)
Run your existing lexical coding script over that file.
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Verbatim from probes/probe1_expanded.py line 42-46.
# Uses MatrAIx's actual phrase template: "with a {value} cultural frame"
# Variable renamed from {bg} to {value} to match this script; wording unchanged.
# ---------------------------------------------------------------------------

PROMPT_TEMPLATE = (
    "You are a person with a {value} cultural frame. Your manager proposed a major "
    "project change you believe is flawed. Express your concerns naturally and "
    "authentically."
)

MAX_TOKENS = 300

CONDITIONS = [
    "Individualist (Western)",
    "Collectivist (East Asian)",
]

TRIALS_PER_CONDITION = 25

# Model names. Gemini confirmed present in your models.list() output.
# OpenAI name is a guess -- --check will print your actual available models.
GEMINI_MODEL = "gemini-3.5-flash"
OPENAI_MODEL = "gpt-4o"

OUTFILE = Path("results/crossmodel_probe1.jsonl")

SLEEP_BETWEEN_CALLS = 1.5   # seconds, be polite to the quota
MAX_RETRIES = 4


# ---------------------------------------------------------------------------
# Provider adapters
# ---------------------------------------------------------------------------

def call_gemini(prompt):
    from google import genai
    from google.genai import types
    client = genai.Client()
    resp = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(max_output_tokens=MAX_TOKENS),
    )
    return resp.text


def call_openai(prompt):
    from openai import OpenAI
    client = OpenAI()
    resp = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=MAX_TOKENS,
    )
    return resp.choices[0].message.content


PROVIDERS = {
    "gemini": call_gemini,
    "openai": call_openai,
}

MODEL_NAMES = {
    "gemini": GEMINI_MODEL,
    "openai": OPENAI_MODEL,
}


# ---------------------------------------------------------------------------
# Access check
# ---------------------------------------------------------------------------

def check_access(provider):
    """One tiny call. Tells you immediately if you are capped or misconfigured."""
    print(f"\n--- checking {provider} ---")

    keyvar = "GOOGLE_API_KEY" if provider == "gemini" else "OPENAI_API_KEY"
    if not (os.environ.get(keyvar) or os.environ.get("GEMINI_API_KEY")):
        print(f"  NO KEY: {keyvar} not set in environment")
        return False

    if provider == "openai":
        try:
            from openai import OpenAI
            models = [m.id for m in OpenAI().models.list()]
            chat = sorted([m for m in models if m.startswith(("gpt", "o1", "o3", "o4"))])
            print(f"  available chat models: {chat[:25]}")
            if OPENAI_MODEL not in models:
                print(f"  WARNING: '{OPENAI_MODEL}' not in your list. Edit OPENAI_MODEL.")
        except Exception as e:
            print(f"  could not list models: {e}")

    try:
        out = PROVIDERS[provider]("Reply with the single word: ok")
        print(f"  OK -- {MODEL_NAMES[provider]} responded: {str(out).strip()[:60]}")
        return True
    except Exception as e:
        msg = str(e)
        print(f"  FAILED: {msg[:300]}")
        low = msg.lower()
        if "404" in msg or "not_found" in low or "not found" in low or "does not exist" in low:
            print("  -> Bad model name. Fix GEMINI_MODEL/OPENAI_MODEL at the top of this file.")
        elif "429" in msg or "quota" in low or "resource_exhausted" in low:
            print("  -> This is a quota/rate limit. Not a code problem. Try later.")
        elif "auth" in low or "api key" in low or "401" in low or "permission" in low:
            print("  -> Auth problem. Check your API key env var.")
        return False


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def load_done():
    """Resume support: skip trials already recorded."""
    done = set()
    if OUTFILE.exists():
        with open(OUTFILE, encoding="utf-8") as f:
            for line in f:
                try:
                    r = json.loads(line)
                    if r.get("response"):
                        done.add((r["provider"], r["condition"], r["trial"]))
                except json.JSONDecodeError:
                    continue
    return done


def run(provider):
    OUTFILE.parent.mkdir(parents=True, exist_ok=True)
    done = load_done()
    fn = PROVIDERS[provider]

    total = len(CONDITIONS) * TRIALS_PER_CONDITION
    completed = 0
    failures = 0

    for condition in CONDITIONS:
        prompt = PROMPT_TEMPLATE.format(value=condition)

        for trial in range(1, TRIALS_PER_CONDITION + 1):
            completed += 1
            key = (provider, condition, trial)
            if key in done:
                print(f"[{completed}/{total}] skip (already done) {condition} #{trial}")
                continue

            text, err = None, None
            for attempt in range(MAX_RETRIES):
                try:
                    text = fn(prompt)
                    break
                except Exception as e:
                    err = str(e)
                    low = err.lower()
                    if "404" in err or "not_found" in low or "not found" in low:
                        break
                    if "429" in err or "quota" in low or "resource_exhausted" in low:
                        wait = min(60, 5 * (2 ** attempt))
                        print(f"    rate limited, waiting {wait}s "
                              f"(attempt {attempt + 1}/{MAX_RETRIES})")
                        time.sleep(wait)
                    else:
                        break

            record = {
                "provider": provider,
                "model": MODEL_NAMES[provider],
                "probe": 1,
                "condition": condition,
                "trial": trial,
                "prompt": prompt,
                "response": text,
                "error": None if text else err,
                "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            }
            with open(OUTFILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")

            if text:
                print(f"[{completed}/{total}] {condition} #{trial} ok")
            else:
                failures += 1
                print(f"[{completed}/{total}] {condition} #{trial} FAILED: {str(err)[:120]}")
                if failures >= 5:
                    print("\n5 consecutive-ish failures. Stopping to save quota.")
                    print(f"Partial results saved to {OUTFILE}. Rerun later to resume.")
                    return

            time.sleep(SLEEP_BETWEEN_CALLS)

    print(f"\nDone: {provider}. Results in {OUTFILE}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true", help="access check only")
    p.add_argument("--provider", choices=["gemini", "openai", "both"], default="both")
    args = p.parse_args()

    targets = ["gemini", "openai"] if args.provider == "both" else [args.provider]

    ok = {t: check_access(t) for t in targets}

    if args.check:
        print("\nCheck complete. Rerun without --check to collect trials.")
        return

    live = [t for t in targets if ok[t]]
    if not live:
        print("\nNo provider available right now. Nothing run, no quota burned.")
        sys.exit(1)

    for t in live:
        print(f"\n=== running {t} ({MODEL_NAMES[t]}) ===")
        run(t)


if __name__ == "__main__":
    main()
