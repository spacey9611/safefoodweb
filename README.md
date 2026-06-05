# Food Safety Practice Test AU

Free Australian food safety practice test site — cloned from the [White Card Practice Test](https://white-card-practice-test-au.com/) model for **food-safety-practice-test-au.com**.

## What's included

- **400-question** practice bank (SITXFSA005 / SITXFSA006 aligned)
- Interactive quiz: full test (40 Q), quick quiz (5 Q), topic drills, weak-area review
- **8 state pages** (NSW, VIC, QLD, WA, SA, ACT, NT, TAS)
- **12 topic pages** (temperature, allergens, HACCP, FSS duties, etc.)
- Study guide, exam tips, find-a-course (affiliate), glossary, flashcards landing
- Blog (2 starter posts)
- SEO: sitemap, schema, FAQ accordions

## Local preview

```bash
cd /Users/anxhelikulajanku/Desktop/Adsense/foodpractice
python3 -m http.server 8080
```

Open http://localhost:8080

## Regenerate site content

After editing `tools/build_site.py` (questions, state copy, topics):

```bash
python3 tools/build_site.py
```

## Deploy (Vercel)

1. Register **food-safety-practice-test-au.com**
2. Import this folder to Vercel (static site, no build command)
3. Point DNS to Vercel
4. Add your GA4 / GTM / AdSense IDs to `index.html` when ready
5. Submit `sitemap.xml` in Google Search Console

## Monetisation (from market analysis)

- **AdSense** — education/training CPC $2–4 in AU
- **Affiliates** — AIFS, ClearToWork, Allens Training, Club Training (15–25% commission)
