#!/usr/bin/env python3
"""Check LinkedIn ad copy against the hard constraints.

Checks hook length (<=140 chars, where LinkedIn's "see more" cut lands), intro
length (<=600), headline length (<=70 recommended), on-image headline words
(<8), banned words, and banned openers.

Usage:
  python3 check_copy.py ads.json
  python3 check_copy.py --hook "Your ops team isn't slow." --intro "..." --headline "..."

ads.json is a list of objects. Every field except "id" is optional:
  [{"id": "cost-of-inaction/A", "hook": "...", "intro": "...",
    "headline": "...", "image_text": "...", "cta": "..."}]

Exit code is 1 if any ad has a failure, 0 otherwise.
"""
import argparse
import json
import re
import sys

HOOK_MAX = 140
INTRO_MAX = 600
HEADLINE_MAX = 70
IMAGE_WORDS_MAX = 7  # "under 8 words"

BANNED_WORDS = [
    "unlock", "leverage", "supercharge", "seamless",
    "game-changer", "game changer", "revolutionize", "effortless",
]
BANNED_OPENERS = [
    r"^\s*are you struggling",
    r"^\s*struggling with",
    r"^\s*tired of",
]


def banned_hits(text):
    hits = []
    lower = text.lower()
    for w in BANNED_WORDS:
        # stems catch unlocks/unlocking/leveraged/revolutionizes etc.
        stem = w[:-1] if w.endswith("e") else w
        if re.search(r"\b" + re.escape(stem), lower):
            hits.append(w)
    return sorted(set(hits))


def check_ad(ad):
    fails, notes = [], []
    hook = ad.get("hook", "")
    intro = ad.get("intro", "")
    headline = ad.get("headline", "")
    image_text = ad.get("image_text", "")

    if hook:
        n = len(hook)
        notes.append(f"hook {n}/{HOOK_MAX}")
        if n > HOOK_MAX:
            fails.append(f"hook is {n} chars; payoff must land within {HOOK_MAX}")
        for pat in BANNED_OPENERS:
            if re.search(pat, hook, re.I):
                fails.append("hook uses a banned opener")
                break
        if hook.strip().endswith("?"):
            notes.append("hook is a question: check it isn't engagement bait")
    if intro:
        n = len(intro)
        notes.append(f"intro {n}/{INTRO_MAX}")
        if n > INTRO_MAX:
            fails.append(f"intro is {n} chars; limit {INTRO_MAX}")
        if hook and not intro.strip().startswith(hook.strip()[:40]):
            notes.append("intro doesn't start with the hook text")
    if headline:
        n = len(headline)
        notes.append(f"headline {n}/{HEADLINE_MAX}")
        if n > HEADLINE_MAX:
            fails.append(f"headline is {n} chars; keep to about {HEADLINE_MAX} to avoid truncation")
    if image_text:
        w = len(image_text.split())
        notes.append(f"image text {w} words")
        if w > IMAGE_WORDS_MAX:
            fails.append(f"on-image text is {w} words; keep under 8")

    for field in ("hook", "intro", "headline", "image_text", "cta"):
        for hit in banned_hits(ad.get(field, "")):
            fails.append(f"banned word '{hit}' in {field}")
    return fails, notes


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("file", nargs="?", help="JSON file of ads (use - for stdin)")
    for f in ("hook", "intro", "headline", "image_text", "cta"):
        p.add_argument("--" + f.replace("_", "-"), dest=f)
    args = p.parse_args()

    if args.file:
        raw = sys.stdin.read() if args.file == "-" else open(args.file).read()
        ads = json.loads(raw)
        if isinstance(ads, dict):
            ads = [ads]
    else:
        single = {f: getattr(args, f) for f in ("hook", "intro", "headline", "image_text", "cta") if getattr(args, f)}
        if not single:
            p.error("provide a JSON file or at least one of --hook/--intro/--headline/--image-text/--cta")
        ads = [single]

    failed = 0
    for i, ad in enumerate(ads, 1):
        label = ad.get("id", f"ad {i}")
        fails, notes = check_ad(ad)
        status = "FAIL" if fails else "ok"
        print(f"[{status}] {label}: " + "; ".join(notes))
        for f in fails:
            print(f"    - {f}")
        failed += bool(fails)
    print(f"\n{len(ads) - failed}/{len(ads)} passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
