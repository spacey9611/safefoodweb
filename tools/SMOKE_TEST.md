# Smoke Test — Food Safety Practice Test AU

Run this checklist after **every** change phase, before considering the work done.
Open the site locally (e.g. `python3 -m http.server` from the project root) and check each item.

## Critical safety rules (read before editing)
- **NEVER run** `python3 tools/build_site.py` — it overwrites `index.html`, `guide.html` and manual edits.
- **Safe generators only:** `build_blog_posts.py`, `build_jobs.py`, `build_keyword_pages.py`, `build_topics_only.py` (once created).
- **Manual-only — edit in place, never regenerate:** `index.html`, `guide.html`, `temperature-danger-zone-checker.html`, `bookmarks.html`, `progress.html`.
- Do **one phase only** per session. Do **not** commit unless asked.
- Sitemap source of truth: `tools/SITEMAP_URLS.py` (50 indexable URLs; excludes bookmarks, progress, legacy standalone).

## Functional smoke checklist
1. **Homepage quiz** — load `/`, start the Full test, answer **2 questions**, confirm: option highlights correct/incorrect, explanation shows, Next advances, score updates.
2. **Exam mode** — start Exam mode, confirm the countdown timer appears (40:00) and the combo streak pill shows after 2 correct.
3. **Dark mode on guide** — open `/guide.html`, toggle the theme button (🌙/☀️), confirm colours switch and the choice persists on reload.
4. **Flashcards** — open `/flashcards.html`, flip a card, Next/Previous and Shuffle work.
5. **Danger-zone slider** — open `/temperature-danger-zone-checker.html`, drag the slider: <5°C = "Chilled safe", 5–60 = "Danger zone", >60 = "Hot safe"; 2h/4h calculator returns keep / use-now / discard.
6. **3 internal links** — click any 3 internal links (e.g. a topic page, a blog post, a state page) and confirm they resolve (no 404).

## SEO / integrity quick checks (automated)
Run the site audit (well-formed HTML, unique titles/descriptions, valid JSON-LD, no broken links):
- expected result: **0 issues**, **50 indexable URLs** present in `sitemap.xml` (after Phase 1+).
- confirm `tools/SITEMAP_URLS.py` `to_local()` resolves for every path.
- no indexable page under ~300 words except intentional tool/quiz UI shells.

## Per-phase extra checks
- **Phase 1:** `/food-safety-practice-test-au.html` 301s to `/`; 3 keyword pages in sitemap + linked from home.
- **Phase 2:** `og:image` present on homepage + one state page; blog titles ≤60 chars before the brand suffix.
- **Phase 5:** after `build_all_safe.py`, a diff of `index.html` and `guide.html` is **empty** (manual pages untouched).
- **Phase 6:** dark mode + font-resize both work on flashcards and guide (no double font-resize binding).
