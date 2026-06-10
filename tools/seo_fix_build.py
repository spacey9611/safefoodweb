#!/usr/bin/env python3
"""One-shot SEO bulk fixes: nav links, title trims, sitemap regen."""
import pathlib, re, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent

TITLE_FIXES = {
    "index.html": (
        "<title>Free Food Safety Practice Test Australia 2026 | 650 Questions</title>",
        "<title>Free Food Safety Practice Test &amp; Quiz AU 2026</title>",
    ),
    "blog/10-priority-allergens-australia-food-safety-exam/index.html": (
        "<title>10 Priority Allergens Australia: Exam Cheat Sheet | Food Safety AU</title>",
        "<title>10 Priority Allergens: Exam Cheat Sheet | AU</title>",
    ),
    "blog/cross-contamination-food-safety-exam-tips/index.html": (
        "<title>Cross Contamination Exam Tips for Food Handlers | Food Safety AU</title>",
        "<title>Cross Contamination Exam Tips | AU</title>",
    ),
    "blog/food-safety-certificate-cost-australia-by-state/index.html": (
        "<title>Food Safety Certificate Cost by State (2026) | Food Safety AU</title>",
        "<title>Food Safety Certificate Cost by State | AU</title>",
    ),
    "blog/food-safety-certificate-expire-renewal-australia/index.html": (
        "<title>Does a Food Safety Certificate Expire? Renewal Rules in Australia | Food Safety AU</title>",
        "<title>Food Safety Certificate Expiry &amp; Renewal | AU</title>",
    ),
    "blog/food-safety-practice-test-before-real-exam/index.html": (
        "<title>Food Safety Practice Test Before the Real Exam | Food Safety AU</title>",
        "<title>Practice Test Before Your Real Exam | AU</title>",
    ),
    "blog/food-safety-training-aged-care-childcare/index.html": (
        "<title>Food Safety Training: Aged Care, Childcare & Schools | Food Safety AU</title>",
        "<title>Food Safety for Aged Care &amp; Childcare | AU</title>",
    ),
    "blog/is-food-safety-test-hard-australia/index.html": (
        "<title>Is the Food Safety Test Hard? (Australia 2026) | Food Safety AU</title>",
        "<title>Is the Food Safety Test Hard? | AU</title>",
    ),
    "blog/temperature-danger-zone-australia-guide/index.html": (
        "<title>Temperature Danger Zone Australia: Complete Guide (5°C to 60°C) | Food Safety AU</title>",
        "<title>Temperature Danger Zone Guide Australia | AU</title>",
    ),
}

OG_FIXES = {
    "index.html": (
        'content="Free Food Safety Practice Test Australia 2026 | 650 Questions"',
        'content="Free Food Safety Practice Test &amp; Quiz AU 2026"',
    ),
    "tips.html": (
        'content="How to Pass the Food Safety Test 2026 | Exam Tips"',
        'content="Food Safety Exam Tips 2026 | Study Smart &amp; Pass"',
    ),
}


def main():
    n_nav = n_title = 0
    for path in ROOT.rglob("*.html"):
        rel = str(path.relative_to(ROOT))
        text = path.read_text(encoding="utf-8")
        orig = text
        text = text.replace('href="/blog/"', 'href="/blog"')
        if orig != text:
            n_nav += 1
        if rel in TITLE_FIXES:
            old, new = TITLE_FIXES[rel]
            text = text.replace(old, new)
        if rel in OG_FIXES:
            old, new = OG_FIXES[rel]
            text = text.replace(old, new)
        if text != orig:
            path.write_text(text, encoding="utf-8")
            if rel in TITLE_FIXES or rel in OG_FIXES:
                n_title += 1
    print(f"nav /blog fix: {n_nav} files touched")
    print(f"title/og fixes: {len(TITLE_FIXES) + len(OG_FIXES)} patterns")


if __name__ == "__main__":
    main()
