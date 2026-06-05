# Content & Question-Bank Audit (Senior PM review) — June 2026

Scope: the 400-question bank (`questions.js` / `tools/build_questions.py`), the quiz engine behaviour, and the supporting content pages. Findings are evidence-based (measured from the data), prioritised, with recommended fixes and effort.

---

## 🔴 P0 — Critical (fix before any traffic / launch)

### 1. The correct answer is ALWAYS option A (100% of questions)
- **Evidence:** all 400 questions store `answer: 0`, and the quiz renders options in fixed order (`question.options.forEach(...)` in `script.js` — no shuffle). So in the quiz, flashcards and the SITXFSA005 Q&A page, the correct answer is **always the first option**.
- **Why it's critical:** a user can score 100% by always picking A. It makes the test look rigged/broken, destroys trust, undermines real study value, and is the kind of low-quality signal that hurts AdSense approval and dwell-time/SEO.
- **Fix (recommended): shuffle options at render time and remap the answer index.** In `QuizController.renderQuestion`, shuffle a copy of `question.options`, track where the correct one lands, and compare against that. This randomises every attempt with zero data changes. (Alternative: redistribute `answer` across 0–3 in the data — but render-time shuffle is better because it re-randomises each attempt and also fixes flashcards/Q&A consistency.)
- **Effort:** ~30 min in `script.js` (+ apply the same shuffle in flashcards and the static Q&A page, or note those show a fixed order).

---

## 🟠 P1 — High

### 2. Too few scenario questions (only ~10%)
- **Evidence:** ~41 / 400 (10%) are scenario/situational ("food left out 3 hours — what do you do?"); ~90% are definition/recall.
- **Why:** real RTO assessments and strong prep lean heavily on applied/scenario judgement. A recall-heavy bank trains memorisation, not understanding, and is weaker differentiation versus the doc-dump competitors.
- **Fix:** rewrite/extend toward ~35–45% scenario. Practically: convert ~80–100 existing recall items into scenarios and/or add ~60 new scenario questions (temperature, cross-contamination, allergens, high-risk are the richest for scenarios).
- **Effort:** medium (authoring) — phaseable.

### 3. No author / "last reviewed" / sourcing (E-E-A-T) on content
- **Evidence:** pages have no visible author, review date, or citations; food safety is YMYL (health-adjacent), where Google weights trust heavily.
- **Fix:** add an author/About identity, a "Last reviewed: <date>" line on content + topic + blog pages, and cite FSANZ / state authorities in explanations and guides.
- **Effort:** low–medium (template + a sources pass).

### 4. State pages share the identical generic bank
- **Evidence:** only 2/400 questions mention a state; all 8 state pages serve the same 400 questions.
- **Why:** state pages claim local relevance but the practice content is identical — borderline thin/duplicate intent, and a missed chance to make state pages genuinely distinct (NSW single-RTO rule, VIC DoFoodSafely, council registration, etc.).
- **Fix:** add a small set of state-specific questions (e.g. 5–8 per state) surfaced when arriving from a state page, or at least a state-specific "what's different here" quiz callout. Even 40–60 state-tagged questions would do it.
- **Effort:** medium.

---

## 🟡 P2 — Medium / polish

### 5. Topic weighting is flat vs real exam emphasis
- **Evidence:** 33–34 questions per topic, evenly. Temperature control and hygiene/cross-contamination dominate real assessments.
- **Fix:** rebalance slightly (e.g. temperature 45–50, allergens/cross-contamination/hygiene higher; legislation/pest lower), or weight selection in `pickQuestions`. Optional.

### 6. No difficulty tagging or stratified test selection
- **Evidence:** questions have no `difficulty` field; a 40-question run is a random draw from 400, so a single attempt may over-sample one topic and miss others.
- **Fix:** add a `difficulty` field (easy/medium/hard) and/or stratify the 40-question draw to guarantee topic coverage (e.g. proportional per topic). Improves perceived quality and study value.
- **Effort:** low–medium.

### 7. Explanations don't cite the rule's basis
- **Evidence:** explanations are clear (avg 133 chars) but rarely reference *why* (Food Standards Code / 2-hr-4-hr rule / Standard 3.2.2A).
- **Fix:** append a short reference tag to key explanations (it adds authority + E-E-A-T). Optional but valuable.

### 8. Minor: 1 near-duplicate question stem
- Low impact; review the one flagged pair for distinctness.

---

## ✅ What's already strong
- 400 **genuinely unique** questions (0 padding/"set N"), all with 4 options and a 2–4 sentence explanation (min 90 chars).
- No lazy "all/none of the above" options.
- Even topic coverage across all 12 syllabus areas.
- Rich supporting content: 12 topic pages (FAQ + LearningResource schema), 12 blog posts, 4 industry pages, 3 keyword pages, interactive tool, flashcards, glossary — all schema-rich, unique titles/descriptions, og:image, 0 broken links.

---

## Recommended order of work
1. **P0 #1 — shuffle answer options** (non-negotiable; ~30 min). Without this the whole test is invalid.
2. **P1 #3 — E-E-A-T** (author + last-reviewed + sources) — fast, helps trust + rankings.
3. **P1 #2 — raise scenario ratio** to ~40% (phased authoring).
4. **P1 #4 — state-specific questions.**
5. **P2 #5–7 — difficulty tags, stratified selection, weighting, citations.**

The single most important action is #1 — it is a correctness bug, not a nice-to-have.
