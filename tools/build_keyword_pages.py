#!/usr/bin/env python3
"""Build high-intent keyword landing pages (FSS test, food handler test, SITXFSA005 Q&A).
Run: python3 tools/build_keyword_pages.py
"""
import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from cookie_snippets import COOKIE_HEAD, GA4_TAG, CONSENT_HEAD, cookie_banner_html

CSS_VER = "13"
DOMAIN = "https://food-safety-practice-test-au.com"

NAV = [("/","Practice Test"),("/guide.html","Study Guide"),("/temperature-danger-zone-checker.html","Danger Zone Tool"),
       ("/tips.html","Exam Tips"),("/find-a-course.html","Find a Course"),("/blog","Blog"),
       ("/flashcards.html","Flashcards"),("/glossary.html","Glossary")]
STATES = [("nsw","NSW"),("vic","VIC"),("qld","QLD"),("wa","WA"),("sa","SA"),("act","ACT"),("nt","NT"),("tas","TAS")]

def header():
    nav = "\n".join(f'                <a href="{h}" class="nav-link">{t}</a>' for h,t in NAV)
    states = "\n".join(f'                <a href="/food-safety-{c}.html" class="state-link" title="Food Safety Practice Test {a}">{a}</a>' for c,a in STATES)
    return f'''    <header class="site-header">
        <div class="container site-header__top">
            <a href="/" class="site-brand">
                <span class="site-brand__mark" aria-hidden="true">AU</span>
                <span class="site-brand__text">
                    <span class="site-brand__title">Food Safety Practice Test</span>
                    <span class="site-brand__tagline">Free SITXFSA005 practice &middot; 650 questions</span>
                </span>
            </a>
            <button type="button" class="nav-toggle" aria-label="Toggle navigation menu" aria-expanded="false" aria-controls="site-nav-drawer">Menu</button>
            <div class="site-header__drawer" id="site-nav-drawer">
                <div class="site-header__drawer-inner">
                    <nav class="secondary-nav" aria-label="Site navigation">
{nav}
                    </nav>
                </div>
            </div>
        </div>
        <div class="container site-header__states-wrap">
            <nav class="state-selector" aria-label="State selection">
{states}
            </nav>
            <div class="site-header__tools font-resize-toolbar" aria-label="Text size controls" role="group">
                <span class="font-resize-toolbar__label">Text size</span>
                <button type="button" class="font-resize-btn" id="font-decrease" aria-label="Decrease text size" title="Smaller text">A&minus;</button>
                <button type="button" class="font-resize-btn" id="font-increase" aria-label="Increase text size" title="Larger text">A+</button>
            </div>
        </div>
    </header>'''

FOOTER_HTML = '''    <footer class="footer">
        <div class="container">
            <p>&copy; 2026 Food Safety Practice AU</p>
            <nav class="footer-links">
                <a href="/about.html">About</a>
                <span class="separator">|</span>
                <a href="/terms.html">Terms of Use</a>
                <span class="separator">|</span>
                <a href="/legal.html#privacy">Privacy Policy</a>
                <span class="separator">|</span>
                <a href="/legal.html#legal">Legal Notice</a>
                <span class="separator">|</span>
                <a href="/legal.html#contact">Contact Us</a>
            </nav>
            <p class="footer-disclaimer">We may earn a commission if you purchase through links on this site.</p>
            <p class="footer-disclaimer">This page is free practice and educational content only. Your certificate must be issued by a Registered Training Organisation (RTO).</p>
        </div>
    </footer>'''

CROSS = '''            <section class="guide-section">
                <h2>More free practice</h2>
                <div class="topic-link-grid">
                    <a href="/food-handler-practice-test.html" class="topic-link-card">Food Handler Practice Test</a>
                    <a href="/food-safety-supervisor-practice-test.html" class="topic-link-card">Food Safety Supervisor (FSS) Test</a>
                    <a href="/sitxfsa005-questions-and-answers.html" class="topic-link-card">SITXFSA005 Questions &amp; Answers</a>
                    <a href="/guide.html" class="topic-link-card">Study Guide</a>
                    <a href="/temperature-danger-zone-checker.html" class="topic-link-card">Danger Zone Tool</a>
                    <a href="/flashcards.html" class="topic-link-card">Flashcards</a>
                    <a href="/dofoodsafely-vs-free-practice-test.html" class="topic-link-card">DoFoodSafely vs Free Practice Test</a>
                </div>
            </section>'''

PAGES = [
 {
  "slug":"food-safety-supervisor-practice-test.html",
  "title":"Food Safety Supervisor Practice Test (FSS) 2026 | Free",
  "desc":"Free Food Safety Supervisor (FSS) practice test for Australia. Practise SITXFSA005 & SITXFSA006 questions with instant feedback before your RTO assessment.",
  "ogt":"Food Safety Supervisor (FSS) Practice Test | Australia",
  "accent":"Food Safety Supervisor (FSS) Practice Test",
  "meta":"SITXFSA005 + SITXFSA006 · free · instant feedback · no sign-up",
  "intro":[
    "Preparing to become a <strong>Food Safety Supervisor (FSS)</strong>? This free practice test helps you get ready for the units that matter: <strong>SITXFSA005</strong> (use hygienic practices for food safety) and <strong>SITXFSA006</strong> (participate in safe food handling practices). Practise unlimited questions with instant feedback, then sit your official assessment with confidence.",
    "An FSS does more than handle food &mdash; they <em>supervise</em> food safety: guiding staff, monitoring temperatures and critical controls, and acting when something is unsafe. That means the assessment expects a deeper grasp of HACCP, supervisor duties, high-risk foods and the law, not just the basics.",
  ],
  "facts":[("Units","SITXFSA005 + SITXFSA006"),("Role","Supervises food safety"),("Cert validity","5 years (renew)"),("Best for","FSS / kitchen supervisors"),("Questions","650 free, 40 per run"),("Cost","Free practice")],
  "sections":[
    ("What the FSS test covers","<p>Beyond the food-handler basics, expect more on <a href=\"/topic-fss-duties.html\">Food Safety Supervisor duties</a>, <a href=\"/topic-haccp.html\">HACCP</a> and critical control points, <a href=\"/topic-high-risk.html\">high-risk foods and vulnerable groups</a>, and food law (Standard 3.2.2A). Temperature control and the 2-hour/4-hour rule remain core.</p>"),
    ("FSS vs food handler &mdash; what's the difference?","<p>A <strong>food handler</strong> (SITXFSA005) follows safe practices. A <strong>Food Safety Supervisor</strong> (SITXFSA005 + SITXFSA006) oversees them and is legally nominated for the business. Read the full breakdown in <a href=\"/blog/food-safety-supervisor-vs-food-handler/\">Food Safety Supervisor vs Food Handler</a>, or take the <a href=\"/food-handler-practice-test.html\">food handler practice test</a> if that's the unit you need.</p>"),
    ("How to prepare","<p>Drill the supervisor-heavy topics first, aim for <strong>80%+</strong> consistently, then sit your RTO assessment. NSW runs its own approved-RTO scheme &mdash; check your <a href=\"/food-safety-nsw.html\">state page</a>. Your official certificate must come from a Registered Training Organisation.</p>"),
  ],
  "faqs":[
    ("Is this an official Food Safety Supervisor certificate?","No. This is free practice and revision only. Your official FSS certificate must be issued by a Registered Training Organisation (RTO) that assesses SITXFSA005 and SITXFSA006."),
    ("What units does a Food Safety Supervisor need?","Most Food Safety Supervisors complete SITXFSA005 (use hygienic practices) and SITXFSA006 (participate in safe food handling practices)."),
    ("How is the FSS test different from the food handler test?","The FSS assessment expects more depth on supervising food safety &mdash; HACCP, supervisor duties, high-risk foods and food law &mdash; on top of the food-handler basics."),
    ("How long is an FSS certificate valid?","Generally 5 years, after which you must complete refresher training to recertify."),
    ("Do I need an approved RTO in NSW?","Yes. In NSW, FSS training must be completed through an RTO approved by the NSW Food Authority, and from 1 September 2025 both units must be done with the same approved RTO."),
  ],
  "related":[("/topic-fss-duties.html","FSS Duties"),("/topic-haccp.html","HACCP Basics"),("/topic-high-risk.html","High-Risk Foods"),("/topic-temperature.html","Temperature & Danger Zone")],
  "samples":False,
 },
 {
  "slug":"food-handler-practice-test.html",
  "title":"Food Handler Practice Test 2026 (SITXFSA005) | Free",
  "desc":"Free food handler practice test for Australia. 650 SITXFSA005 questions with instant feedback and explanations. No sign-up. Get job-ready for your first shift.",
  "ogt":"Food Handler Practice Test (SITXFSA005) | Australia",
  "accent":"Food Handler Practice Test",
  "meta":"SITXFSA005 · 650 questions · instant feedback · no sign-up",
  "intro":[
    "Starting a job that involves food? This free <strong>food handler practice test</strong> prepares you for <strong>SITXFSA005 &mdash; Use hygienic practices for food safety</strong>, the nationally recognised unit for food handlers across Australia. Answer real exam-style questions, get instant explanations, and walk into your assessment ready.",
    "A food handler is anyone who works with food or food-contact surfaces &mdash; kitchen hands, wait staff, baristas, deli and takeaway staff. You don't need cooking skill to pass; you need to understand hygiene, temperature control, cross-contamination and allergens.",
  ],
  "facts":[("Unit","SITXFSA005"),("For","All food handlers"),("Questions","650 free, 40 per run"),("Format","Multiple choice"),("Feedback","Instant + explanations"),("Cost","Free, no sign-up")],
  "sections":[
    ("What's on the food handler test","<p>The core topics are <a href=\"/topic-temperature.html\">temperature &amp; the danger zone</a>, <a href=\"/topic-hygiene.html\">personal hygiene</a>, <a href=\"/topic-cross-contamination.html\">cross-contamination</a>, <a href=\"/topic-allergens.html\">allergens</a>, <a href=\"/topic-cleaning.html\">cleaning &amp; sanitising</a> and <a href=\"/topic-storage.html\">food storage</a>. Drill any one of them or take a full 40-question run.</p>"),
    ("Need the supervisor version?","<p>If your role is a nominated Food Safety Supervisor, you'll also need SITXFSA006 &mdash; use the <a href=\"/food-safety-supervisor-practice-test.html\">Food Safety Supervisor (FSS) practice test</a> instead. Unsure which you need? See <a href=\"/blog/food-safety-supervisor-vs-food-handler/\">Food Safety Supervisor vs Food Handler</a>.</p>"),
    ("How to get certified","<p>Practise here until you score <strong>80%+</strong>, then complete SITXFSA005 with an accredited RTO to get your nationally recognised certificate. <a href=\"/find-a-course.html\" rel=\"sponsored nofollow\">Compare accredited courses &rarr;</a></p>"),
  ],
  "faqs":[
    ("Is this a real food handler certificate?","No &mdash; it's free practice and revision only. Your nationally recognised certificate must be issued by a Registered Training Organisation (RTO) that assesses SITXFSA005."),
    ("What unit is the food handler test?","SITXFSA005 &mdash; Use hygienic practices for food safety &mdash; is the national unit for food handlers in Australia."),
    ("Do I need a food handler certificate to work?","Most roles handling unpackaged food require food safety skills and knowledge, and many businesses must appoint a certified Food Safety Supervisor. Check your role and state."),
    ("How many questions are on the food handler test?","Our free practice draws 40 questions per run from a bank of 650, across all 12 food safety topics, with instant explanations."),
    ("Is the food handler test hard?","For most people, no &mdash; if you understand the danger zone and core hygiene rules. See our guide: is the food safety test hard?"),
  ],
  "related":[("/topic-temperature.html","Temperature & Danger Zone"),("/topic-hygiene.html","Personal Hygiene"),("/topic-allergens.html","Allergens"),("/topic-cross-contamination.html","Cross Contamination")],
  "samples":False,
 },
 {
  "slug":"sitxfsa005-questions-and-answers.html",
  "title":"SITXFSA005 Questions and Answers 2026 | Free Practice",
  "desc":"Free SITXFSA005 questions and answers with explanations. Sample food safety exam questions plus a full 650-question practice test. No sign-up required.",
  "ogt":"SITXFSA005 Questions and Answers | Free Practice",
  "accent":"SITXFSA005 Questions &amp; Answers",
  "meta":"Sample questions with answers + explanations · free practice test",
  "intro":[
    "Looking for <strong>SITXFSA005 questions and answers</strong> to study from? Below are sample exam-style questions with the correct answer and a plain-English explanation for each &mdash; original, accurate and free. When you're ready, take the full <a href=\"/\">650-question practice test</a> for instant feedback.",
    "SITXFSA005 (Use hygienic practices for food safety) is the nationally recognised unit for food handlers in Australia. Reading answers is a good start, but actively testing yourself is what makes the knowledge stick.",
  ],
  "facts":[("Unit","SITXFSA005"),("Below","10 sample Q&A"),("Full bank","650 questions"),("Answers","With explanations"),("Format","Multiple choice"),("Cost","Free, no sign-up")],
  "sections":[
    ("How to use this page","<p>Try to answer each question before reading the answer. Note any you get wrong, then drill that topic &mdash; for example <a href=\"/topic-temperature.html\">temperature</a> or <a href=\"/topic-allergens.html\">allergens</a> &mdash; and finish with a full <a href=\"/\">practice test</a>. Aim for 80%+ before your RTO assessment.</p>"),
  ],
  "faqs":[
    ("Are these the real SITXFSA005 exam questions?","No. These are original, exam-style practice questions written to match the SITXFSA005 knowledge areas. Actual RTO assessment questions vary by provider."),
    ("Can I pass SITXFSA005 just by reading answers?","Reading helps, but active testing works far better. Use the sample answers to learn, then take the full practice test to confirm you're ready."),
    ("Where do I get the official SITXFSA005 certificate?","Only a Registered Training Organisation (RTO) can assess and issue the nationally recognised SITXFSA005 certificate."),
    ("How many practice questions are there?","This page shows 10 worked examples; the full free practice test has 650 unique questions across 12 topics."),
  ],
  "related":[("/food-handler-practice-test.html","Food Handler Practice Test"),("/topic-temperature.html","Temperature & Danger Zone"),("/topic-allergens.html","Allergens"),("/guide.html","Study Guide")],
  "samples":True,
 },
 {
  "slug":"dofoodsafely-vs-free-practice-test.html",
  "title":"DoFoodSafely vs Free Practice Test 2026 | VIC & All States",
  "desc":"DoFoodSafely is VIC-only with 30 questions. Compare DoFoodSafely to our free all-states food safety practice test with 650 SITXFSA005 questions.",
  "ogt":"DoFoodSafely vs Free Food Safety Practice Test",
  "accent":"DoFoodSafely vs Free Practice Test",
  "meta":"VIC DoFoodSafely compared · 650 questions · all 8 states",
  "breadcrumb":"DoFoodSafely Comparison",
  "intro":[
    "Searching for <strong>DoFoodSafely</strong> or the Victorian government food handler quiz? <strong>DoFoodSafely</strong> (health.vic.gov.au) is a free Victorian training tool with about <strong>30 questions</strong> and a certificate for Victoria. It is a solid starting point if you work only in VIC &mdash; but it does not cover other states and offers limited repeat practice.",
    "This site gives you a <strong>free interactive practice test for all Australian states</strong>: <strong>650 SITXFSA005 exam-style questions</strong>, 12 topic drills, instant explanations, flashcards, and a danger-zone calculator. Use DoFoodSafely for the official VIC certificate path; use us to <em>prepare deeply</em> before any RTO or employer assessment.",
  ],
  "facts":[("DoFoodSafely","~30 Q, VIC only"),("This site","650 Q, all states"),("DoFoodSafely cert","VIC food handler"),("Our test","Practice only"),("Best combo","Both if in VIC"),("Cost","Both free")],
  "sections":[
    ("DoFoodSafely: what it is","<p><strong>DoFoodSafely</strong> is run by the Victorian Department of Health. It teaches basic food safety and issues a certificate recognised for Victorian food handlers. It is <strong>not available for NSW, QLD, WA, SA, ACT, NT or TAS</strong> &mdash; those states use accredited RTO courses instead. See our <a href=\"/food-safety-vic.html\">Food Safety Practice Test VIC</a> page for state-specific rules.</p>"),
    ("Where our free practice test wins","<ul><li><strong>650 questions</strong> vs ~30 &mdash; far more repeat practice before your real assessment</li><li><strong>All 8 states</strong> &mdash; not limited to Victoria</li><li><strong>12 topic drills</strong>, timed exam mode, weak-area review, flashcards</li><li><strong>SITXFSA005 + FSS topics</strong> including HACCP and supervisor duties</li><li><strong>Interactive tools</strong> like the <a href=\"/temperature-danger-zone-checker.html\">temperature danger zone checker</a></li></ul>"),
    ("Which should you use?","<p><strong>In Victoria:</strong> DoFoodSafely if you need the free VIC certificate pathway, <em>plus</em> our practice test to drill until you score 80%+ before any RTO assessment. <strong>Outside VIC:</strong> skip DoFoodSafely (it does not apply) and use our <a href=\"/\">free practice test</a>, <a href=\"/food-handler-practice-test.html\">food handler test</a>, or <a href=\"/find-a-course.html\">find an accredited course</a> in your state.</p>"),
  ],
  "faqs":[
    ("Is DoFoodSafely the same as SITXFSA005?","DoFoodSafely covers similar food safety knowledge for Victorian food handlers but is a Victorian program. SITXFSA005 is the nationally recognised unit issued by RTOs across Australia."),
    ("Can I use DoFoodSafely if I work in NSW or QLD?","DoFoodSafely is designed for Victoria. Other states require training through accredited RTOs. Use our all-states practice test to prepare regardless of where you work."),
    ("Is this site affiliated with DoFoodSafely?","No. We are an independent free practice resource, not affiliated with the Victorian Department of Health or DoFoodSafely."),
    ("Does your practice test replace DoFoodSafely?","No. Our site is practice and revision only. DoFoodSafely can issue a VIC certificate; our test helps you pass assessments with confidence."),
    ("How many questions does DoFoodSafely have?","DoFoodSafely has approximately 30 questions. Our free bank has 650 unique questions with 40 per practice run."),
  ],
  "related":[("/food-safety-vic.html","Food Safety VIC"),("/food-handler-practice-test.html","Food Handler Test"),("/sitxfsa005-questions-and-answers.html","SITXFSA005 Q&amp;A"),("/guide.html","Study Guide")],
  "samples":False,
 },
]

# 10 original worked examples for the SITXFSA005 Q&A page
SAMPLES = [
 ("What is the temperature danger zone in Australia?","5&deg;C to 60&deg;C","Bacteria multiply fastest between 5&deg;C and 60&deg;C, so potentially hazardous food must be kept below 5&deg;C or above 60&deg;C."),
 ("What core temperature should poultry and minced meat reach?","75&deg;C in the centre","Mincing spreads surface bacteria throughout the meat, so it must be cooked through to 75&deg;C, checked with a clean probe thermometer."),
 ("Under the 2-hour/4-hour rule, what do you do with food in the danger zone for 3 hours?","Use it immediately","Between 2 and 4 hours total, the food must be used now &mdash; it cannot be returned to the fridge. Over 4 hours, discard it."),
 ("What is the minimum hot-holding temperature for food on display?","60&deg;C or above","At 60&deg;C and above, bacteria stop multiplying, so hot-held food stays safe during service."),
 ("How long should you wash your hands?","At least 20 seconds with soap and warm water","Scrub all surfaces &mdash; palms, backs, between fingers, thumbs and nails &mdash; then rinse and dry with a clean single-use towel."),
 ("Do disposable gloves remove the need to wash your hands?","No","Gloves spread bacteria like bare hands if reused; wash hands before gloving and change gloves between tasks."),
 ("What colour cutting board is commonly used for raw poultry?","Yellow","A typical system: yellow = raw poultry, red = raw meat, blue = raw fish, green = fruit/veg, white = dairy/bakery."),
 ("How many priority allergens must be declared in Australia?","10","Peanuts, tree nuts, milk, eggs, sesame, soy, wheat/gluten, fish, crustacea and lupin. Cooking does not remove allergens."),
 ("A food handler has vomiting and diarrhoea. What should they do?","Not handle food and report it","They must stay away from food handling and typically be symptom-free for 48 hours before returning."),
 ("What is the difference between cleaning and sanitising?","Cleaning removes dirt; sanitising reduces bacteria","You must clean first, then sanitise &mdash; sanitiser does not work properly on a dirty surface."),
]

def build(p):
    intro = "\n            ".join(f"<p>{x}</p>" for x in p["intro"])
    facts = "\n                ".join(f'<div class="state-fact"><div class="state-fact__label">{l}</div><div class="state-fact__val">{v}</div></div>' for l,v in p["facts"])
    secs = "\n            ".join(f'<section class="guide-section"><h2>{h}</h2>{b}</section>' for h,b in p["sections"])
    samples = ""
    if p.get("samples"):
        items = "\n                ".join(
            f'<div class="review-item"><p class="rq"><strong>Q{i+1}.</strong> {q}</p><p class="ra"><strong>Answer:</strong> {a}</p><p class="re">{e}</p></div>'
            for i,(q,a,e) in enumerate(SAMPLES))
        samples = f'<section class="guide-section"><h2>10 SITXFSA005 sample questions &amp; answers</h2>\n                {items}\n            </section>'
    related = "\n                ".join(f'<a href="{h}" class="topic-link-card">{t}</a>' for h,t in p["related"])
    faqs = "\n                ".join(f'<dt class="faq-question" tabindex="0" aria-expanded="false"><span>{q}</span><span class="faq-toggle">+</span></dt>\n                <dd class="faq-answer" hidden>{a}</dd>' for q,a in p["faqs"])
    faq_schema = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in p["faqs"]]}
    crumb_name = p.get("breadcrumb") or p["accent"].replace("&amp;", "&")
    breadcrumb = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":f"{DOMAIN}/"},
        {"@type":"ListItem","position":2,"name":crumb_name,"item":f"{DOMAIN}/{p['slug']}"}]}
    html = f'''<!DOCTYPE html>
<html lang="en-AU">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
{CONSENT_HEAD}
{GA4_TAG}
{COOKIE_HEAD}
    <title>{p["title"]}</title>
    <meta name="description" content="{p["desc"]}">
    <meta name="robots" content="index, follow">
    <meta name="author" content="Food Safety Practice AU">
    <link rel="canonical" href="{DOMAIN}/{p["slug"]}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{DOMAIN}/{p["slug"]}">
    <meta property="og:title" content="{p["ogt"]}">
    <meta property="og:description" content="{p["desc"]}">
    <meta property="og:image" content="{DOMAIN}/og-default.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:image" content="{DOMAIN}/og-default.png">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="stylesheet" href="/style.css?v={CSS_VER}">
    <script type="application/ld+json">
{json.dumps(faq_schema, indent=2, ensure_ascii=True)}
    </script>
    <script type="application/ld+json">
{json.dumps(breadcrumb, indent=2, ensure_ascii=True)}
    </script>
</head>
<body>
{header()}

    <section class="home-editorial-hero" aria-labelledby="kw-hero-title">
        <div class="container home-editorial-hero__inner">
            <p class="home-editorial-hero__badge">Free &middot; no sign-up</p>
            <h1 id="kw-hero-title" class="home-editorial-hero__title">{p["accent"]}</h1>
            <p class="home-editorial-hero__meta">{p["meta"]}</p>
        </div>
    </section>

    <main class="container">
        <article class="content-page">
            {intro}
            <div class="content-cta">
                <h3>Start practising now</h3>
                <p>650 exam-style questions with instant explanations. No sign-up required.</p>
                <a href="/" class="btn btn-primary">Start the free practice test</a>
                <a href="/flashcards.html" class="btn btn-secondary">Flashcards</a>
            </div>
            <div class="ad-slot" data-ad-slot="kw-incontent" role="complementary" aria-label="Advertisement"><span class="ad-slot__label">Advertisement</span></div>
            {secs}
            {samples}
            <section class="guide-section">
                <h2>Related practice topics</h2>
                <div class="topic-link-grid">
                {related}
                </div>
            </section>
{CROSS}
            <section class="guide-section">
                <h2>Frequently asked questions</h2>
                <dl>
                {faqs}
                </dl>
            </section>
            <div class="affiliate-card" style="margin-top:18px;">
                <p class="affiliate-eyebrow">Ready for the real thing?</p>
                <h3 class="affiliate-heading">Book your accredited food safety course</h3>
                <p class="affiliate-text">Practice gets you exam-ready, but your certificate must be issued by a registered training organisation. Compare providers in your state from $85.</p>
                <a href="/find-a-course.html" class="btn btn-secondary affiliate-cta" rel="sponsored nofollow">Find an accredited course &rarr;</a>
                <p class="affiliate-disclosure">We may earn a commission from course providers, at no extra cost to you.</p>
            </div>
        <p class="byline" data-byline style="color:var(--muted);font-size:.85rem;border-top:1px solid var(--line);margin-top:22px;padding-top:14px;">Written and reviewed by the Food Safety Practice AU editorial team. Last reviewed June 2026. Based on the <a href="https://www.foodstandards.gov.au/" target="_blank" rel="noopener">Food Standards Code (FSANZ)</a> and Australian state/territory food authorities. General guidance only &mdash; not official certification.</p>
        </article>
    </main>
{FOOTER_HTML}
{cookie_banner_html()}
    <script src="faq-accordion.js" defer></script>
    <script src="cookie-consent.js" defer></script>
    <script src="site-ui.js" defer></script>
    <script src="/ads.js" defer></script>
</body>
</html>
'''
    (ROOT / p["slug"]).write_text(html, encoding="utf-8")
    return p["slug"]

if __name__ == "__main__":
    for p in PAGES:
        print("wrote", build(p))
    print("DONE", len(PAGES), "keyword pages")
