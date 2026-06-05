#!/usr/bin/env python3
"""SINGLE SOURCE OF TRUTH for indexable URLs (Food Safety Practice Test AU).

Used by sitemap generation and link/QA checks. Keep this list authoritative:
when you add or remove an indexable page, update it HERE only.

NOTE (repo state, Phase 0): the project folder is NOT a git repository, so there
is no version control snapshot of index.html / guide.html / style.css / script.js.
Recommend `git init` before further phases so manual-page edits are recoverable.

EXCLUDED from the sitemap on purpose:
  - bookmarks.html   (user tool, noindex — personalised, no SEO value)
  - progress.html    (user tool, noindex — personalised, no SEO value)
  - food-safety-practice-test-au.html  (legacy standalone; Phase 1 redirects it -> /)
"""

DOMAIN = "https://food-safety-practice-test-au.com"

# ── Core ──────────────────────────────────────────────────────────────────
HOME = ["/"]

# ── Programmatic clusters ─────────────────────────────────────────────────
STATES = [
    "/food-safety-nsw.html",
    "/food-safety-vic.html",
    "/food-safety-qld.html",
    "/food-safety-wa.html",
    "/food-safety-sa.html",
    "/food-safety-act.html",
    "/food-safety-nt.html",
    "/food-safety-tas.html",
]

TOPICS = [
    "/topic-food-standards.html",
    "/topic-food-handler.html",
    "/topic-temperature.html",
    "/topic-cross-contamination.html",
    "/topic-hygiene.html",
    "/topic-cleaning.html",
    "/topic-allergens.html",
    "/topic-storage.html",
    "/topic-pest-control.html",
    "/topic-haccp.html",
    "/topic-fss-duties.html",
    "/topic-high-risk.html",
]

JOBS = [
    "/food-safety-aged-care.html",
    "/food-safety-childcare.html",
    "/food-safety-school-canteen.html",
    "/food-safety-retail.html",
]

KEYWORD_PAGES = [
    "/food-handler-practice-test.html",
    "/food-safety-supervisor-practice-test.html",
    "/sitxfsa005-questions-and-answers.html",
]

# ── Tools / guides / utility (indexable) ──────────────────────────────────
RESOURCES = [
    "/guide.html",
    "/tips.html",
    "/flashcards.html",
    "/glossary.html",
    "/find-a-course.html",
    "/temperature-danger-zone-checker.html",
    "/about.html",
    "/legal.html",
    "/terms.html",
    "/blog",
]

# ── Blog posts (12) ───────────────────────────────────────────────────────
BLOG_SLUGS = [
    "how-to-pass-food-safety-test",
    "food-safety-supervisor-vs-food-handler",
    "is-food-safety-test-hard-australia",
    "temperature-danger-zone-australia-guide",
    "food-safety-certificate-cost-australia-by-state",
    "how-to-get-food-safety-certificate-online-australia",
    "food-safety-training-aged-care-childcare-2023",
    "10-priority-allergens-australia-food-safety-exam",
    "food-safety-certificate-expire-renewal-australia",
    "haccp-basics-food-handlers-australia",
    "cross-contamination-food-safety-exam-tips",
    "food-safety-practice-test-before-real-exam",
]
BLOG = [f"/blog/{slug}" for slug in BLOG_SLUGS]

# ── Excluded (do NOT add to sitemap) ──────────────────────────────────────
EXCLUDED = [
    "/bookmarks.html",
    "/progress.html",
    "/food-safety-practice-test-au.html",
]

# ── Combined, ordered list of indexable paths ─────────────────────────────
PATHS = HOME + KEYWORD_PAGES + STATES + TOPICS + JOBS + RESOURCES + BLOG


def urls():
    """Return absolute URLs for every indexable path."""
    return [DOMAIN + p for p in PATHS]


def to_local(path):
    """Map a sitemap path to its local file (for QA/existence checks)."""
    if path == "/":
        return "index.html"
    if path == "/blog":
        return "blog/index.html"
    if path.startswith("/blog/"):
        slug = path.removeprefix("/blog/").strip("/")
        if slug:
            return f"blog/{slug}/index.html"
    if path.endswith("/"):
        return path.strip("/") + "/index.html"
    return path.lstrip("/")


if __name__ == "__main__":
    print(f"Indexable URLs: {len(PATHS)} | Excluded: {len(EXCLUDED)}")
    for p in PATHS:
        print(" ", DOMAIN + p)
