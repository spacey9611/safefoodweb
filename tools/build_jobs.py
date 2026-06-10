#!/usr/bin/env python3
"""Build industry / job-type SEO pages (aged care, childcare, school canteen, retail).
Run: python3 tools/build_jobs.py
"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent

NAV = [
    ("/", "Practice Test", False),
    ("/guide.html", "Study Guide", False),
    ("/temperature-danger-zone-checker.html", "Danger Zone Tool", False),
    ("/tips.html", "Exam Tips", False),
    ("/find-a-course.html", "Find a Course", False),
    ("/blog", "Blog", False),
    ("/flashcards.html", "Flashcards", False),
    ("/glossary.html", "Glossary", False),
]
STATES = [("nsw","NSW"),("vic","VIC"),("qld","QLD"),("wa","WA"),("sa","SA"),("act","ACT"),("nt","NT"),("tas","TAS")]

def header():
    nav = "\n".join(
        f'                <a href="{h}" class="nav-link">{t}</a>' for h,t,_ in NAV)
    states = "\n".join(
        f'                <a href="/food-safety-{c}.html" class="state-link" title="Food Safety Practice Test {a}">{a}</a>' for c,a in STATES)
    return f'''    <header class="site-header">
        <div class="container site-header__top">
            <a href="/" class="site-brand">
                <span class="site-brand__mark" aria-hidden="true">AU</span>
                <span class="site-brand__text">
                    <span class="site-brand__title">Food Safety Practice Test</span>
                    <span class="site-brand__tagline">Free SITXFSA005 practice · 650 questions</span>
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

FOOTER = '''    <footer class="footer">
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
            <p class="footer-disclaimer">Not affiliated with FSANZ, state health departments, or the Australian Government. General guidance only.</p>
        </div>
    </footer>

    <div id="cookie-banner-backdrop" class="cookie-banner-backdrop" aria-hidden="true"></div>
    <div id="cookie-banner" class="cookie-banner" role="dialog" aria-modal="true" aria-labelledby="cookie-banner-title" aria-live="polite">
        <div class="cookie-banner__content">
            <div class="cookie-banner__copy">
                <p id="cookie-banner-title"><strong>Accept cookies to continue</strong></p>
                <p class="cookie-banner__sub">We use cookies to keep the site running and to understand how people use our free practice tests. Tap accept to start studying. <a href="/legal.html#privacy">Privacy Policy</a></p>
            </div>
            <div class="cookie-banner__actions">
                <button type="button" id="cookie-accept" class="btn btn-primary cookie-btn cookie-btn--accept">Accept &amp; continue</button>
                <button type="button" id="cookie-deny" class="cookie-banner__reject">Essential cookies only</button>
            </div>
        </div>
    </div>
    <script src="faq-accordion.js" defer></script>
    <script src="cookie-consent.js" defer></script>
    <script src="site-ui.js" defer></script>'''

PAGES = [
 {
  "slug":"food-safety-aged-care.html",
  "title":"Food Safety Training for Aged Care 2026 | Australia",
  "desc":"Food safety for aged care in Australia: who needs SITXFSA005/006, the Listeria risk for residents, and free practice questions.",
  "ogt":"Food Safety Training for Aged Care | Australia 2026",
  "accent":"Aged Care",
  "meta":"Why aged-care kitchens are high-risk · Standard 3.2.2A · Free practice",
  "intro":[
    "Aged-care kitchens serve some of the most vulnerable people in the community. Older residents often have weaker immune systems and underlying health conditions, so a case of foodborne illness that would give a healthy adult a mild upset can be serious — even fatal — for an aged-care resident. That is why food safety in aged care is held to a high standard.",
    "Since December 2023, Standard 3.2.2A has extended Food Safety Supervisor and food-handler training requirements to settings that serve vulnerable people, including residential aged care. Most aged-care food businesses must have a certified Food Safety Supervisor and ensure everyone handling food has the right skills and knowledge.",
    "The nationally recognised units are SITXFSA005 (Use hygienic practices for food safety) for food handlers and SITXFSA006 (Participate in safe food handling practices) for supervisors. This page explains what's required and lets you practise free before you sit the real assessment.",
  ],
  "facts":[("Setting","Residential & home aged care"),("Risk level","High — vulnerable residents"),("Key pathogen","Listeria monocytogenes"),("FSS required?","Yes — under Standard 3.2.2A"),("Units","SITXFSA005 / SITXFSA006"),("Cert validity","5 years (FSS)")],
  "sections":[
    ("Why aged care is high-risk","<p>The biggest concern is <strong>Listeria monocytogenes</strong>, which can grow even at fridge temperatures and causes severe illness in the elderly. High-risk foods such as soft cheeses, pâté, cold deli meats, pre-cut fruit, raw seafood and unpasteurised dairy are often restricted or avoided in aged-care menus. Many residents also need <strong>texture-modified meals</strong> (minced or pureed), which involve extra handling steps where contamination and temperature abuse can creep in.</p>"),
    ("Who must be trained","<p>Anyone who handles food — kitchen staff, catering assistants, and care workers who plate or serve meals — needs food safety skills and knowledge. The facility must also appoint a certified <strong>Food Safety Supervisor</strong> who is reasonably available during food operations to guide staff, monitor temperatures and act when something is unsafe. Read our guide to <a href=\"/blog/food-safety-training-aged-care-childcare/\">Standard 3.2.2A for aged care, childcare &amp; schools</a>.</p>"),
    ("Key controls in an aged-care kitchen","<p>Strict temperature control (cold &le;5&deg;C, hot &ge;60&deg;C), the 2-hour/4-hour rule, thorough cooking to 75&deg;C, rapid cooling, and careful allergen and texture-modified meal handling. Cleaning and sanitising, dating of prepared foods and good personal hygiene round out the daily controls. Use our <a href=\"/temperature-danger-zone-checker.html\">danger-zone checker</a> to revise the temperatures.</p>"),
    ("How to get certified","<p>Your official certificate must be issued by a Registered Training Organisation (RTO). Practice tests like this one build confidence, but only an accredited RTO can assess and certify you. <a href=\"/find-a-course.html\" rel=\"sponsored nofollow\">Compare accredited courses &rarr;</a></p>"),
  ],
  "faqs":[
    ("Do aged-care food handlers need a certificate?","They must have food safety skills and knowledge, and under Standard 3.2.2A most aged-care facilities must appoint a certified Food Safety Supervisor. Completing SITXFSA005 (and SITXFSA006 for supervisors) through an RTO is the standard pathway."),
    ("Why is Listeria such a concern in aged care?","Listeria can grow at refrigeration temperatures and causes severe illness in elderly and immunocompromised people. High-risk ready-to-eat foods are therefore controlled tightly or avoided in aged-care menus."),
    ("Are soft cheeses and deli meats allowed in aged care?","Many facilities restrict or avoid higher-risk ready-to-eat foods like soft cheese, pâté and cold deli meats because of the Listeria risk to residents. Always follow your facility's food safety program."),
    ("Does Standard 3.2.2A apply to aged care?","Yes. The December 2023 changes extended Food Safety Supervisor and handler-training requirements to settings serving vulnerable people, including aged care."),
    ("Is this practice test enough to work in an aged-care kitchen?","It's excellent preparation, but your official certificate must come from an accredited RTO, and your employer will have its own food safety program and induction you must follow."),
  ],
  "related":[("/topic-high-risk.html","High-Risk Foods & Vulnerable Groups"),("/topic-temperature.html","Temperature & Danger Zone"),("/topic-cleaning.html","Cleaning & Sanitising"),("/topic-fss-duties.html","Food Safety Supervisor Duties")],
 },
 {
  "slug":"food-safety-childcare.html",
  "title":"Food Safety for Childcare & Early Learning 2026 | Australia",
  "desc":"Food safety for childcare in Australia: allergen and anaphylaxis control, who needs SITXFSA005, plus free practice questions.",
  "ogt":"Food Safety for Childcare & Early Learning | Australia 2026",
  "accent":"Childcare & Early Learning",
  "meta":"Allergens & anaphylaxis · vulnerable children · Standard 3.2.2A",
  "intro":[
    "Young children are highly vulnerable to foodborne illness and to severe allergic reactions, so food safety in childcare and early learning services is critical. Cooks, educators and anyone who prepares or serves food to children needs solid food safety knowledge.",
    "Standard 3.2.2A (from December 2023) extended food-handler training and Food Safety Supervisor requirements to settings that serve vulnerable people, which includes childcare and long day care. Services typically must appoint a certified Food Safety Supervisor and ensure food handlers are trained.",
    "Food safety also intersects with the National Quality Framework expectations around children's health and safety. This page covers what's required and gives you free, exam-style practice before you certify.",
  ],
  "facts":[("Setting","Childcare / long day care / OSHC"),("Risk level","High — young children"),("Top concern","Allergens & anaphylaxis"),("FSS required?","Yes — under Standard 3.2.2A"),("Core unit","SITXFSA005"),("Also relevant","NQF health & safety"),],
  "sections":[
    ("Why childcare is high-risk","<p>Children have developing immune systems and can suffer severe illness from pathogens like <strong>Salmonella</strong> and <strong>E. coli</strong>. Food allergies are also common in young children, and reactions can be life-threatening (<strong>anaphylaxis</strong>). Preventing allergen cross-contact and getting allergen information right is just as important as temperature control.</p>"),
    ("Allergen management is essential","<p>Australia recognises 10 priority allergens (peanuts, tree nuts, milk, eggs, sesame, soy, wheat/gluten, fish, crustacea and lupin). In childcare, even traces matter: use clean or dedicated equipment, prevent cross-contact, follow each child's documented allergy plan, and never guess. Revise with our <a href=\"/topic-allergens.html\">allergen practice questions</a>.</p>"),
    ("Other key controls","<p>Temperature control (cold &le;5&deg;C, hot &ge;60&deg;C), cooking to 75&deg;C, the 2-hour/4-hour rule, avoiding choking hazards and higher-risk foods (e.g. honey for infants under 12 months), strong personal hygiene and thorough cleaning. A certified Food Safety Supervisor oversees these practices.</p>"),
    ("How to get certified","<p>Educators and cooks gain the nationally recognised SITXFSA005 unit (and SITXFSA006 for supervisors) through an RTO. This free practice test prepares you; the certificate itself comes from an accredited provider. <a href=\"/find-a-course.html\" rel=\"sponsored nofollow\">Compare courses &rarr;</a></p>"),
  ],
  "faqs":[
    ("Do childcare educators need food safety training?","If they handle, prepare or serve food, they need appropriate food safety skills and knowledge. Under Standard 3.2.2A most services must also appoint a certified Food Safety Supervisor."),
    ("Why is allergen management so important in childcare?","Young children commonly have food allergies that can cause anaphylaxis — a life-threatening reaction. Even trace amounts can be dangerous, so cross-contact prevention and accurate allergy plans are essential."),
    ("Is honey safe for children in care?","Honey should not be given to infants under 12 months because it can contain Clostridium botulinum spores that cause infant botulism."),
    ("Does Standard 3.2.2A apply to childcare?","Yes. The 2023 changes extended food-handler training and Food Safety Supervisor requirements to childcare and other settings serving vulnerable people."),
    ("Will this practice test certify me to work in childcare?","No — it's preparation only. Your official SITXFSA005/006 certificate must be issued by a Registered Training Organisation, and your service will have its own policies and induction."),
  ],
  "related":[("/topic-allergens.html","Allergen Management"),("/topic-high-risk.html","High-Risk Foods & Vulnerable Groups"),("/topic-hygiene.html","Personal Hygiene"),("/topic-temperature.html","Temperature & Danger Zone")],
 },
 {
  "slug":"food-safety-school-canteen.html",
  "title":"School Canteen Food Safety 2026 | Australia",
  "desc":"School canteen food safety in Australia for staff and volunteers: temperature, allergens, training, plus free practice questions.",
  "ogt":"School Canteen Food Safety | Australia 2026",
  "accent":"School Canteens",
  "meta":"Staff & volunteers · allergens · safe handling · free practice",
  "intro":[
    "School canteens are often run by a mix of paid staff and volunteers, serving food to children throughout the day. Because children are a vulnerable group and canteens handle large volumes at peak times, good food safety practices are essential to prevent illness.",
    "Standard 3.2.2A extended food-handler training and Food Safety Supervisor requirements to settings that serve children, which can include school canteens depending on what they prepare and serve. Many canteens appoint a certified Food Safety Supervisor and ensure regular helpers understand safe food handling.",
    "Whether you're a canteen manager, paid assistant or parent volunteer, this page explains the essentials and gives you free practice questions to build confidence.",
  ],
  "facts":[("Setting","School canteens / tuckshops"),("Workforce","Staff + volunteers"),("Diners","Children (vulnerable)"),("FSS","Often required under 3.2.2A"),("Core unit","SITXFSA005"),("Peak risk","Volume + time in danger zone")],
  "sections":[
    ("Why canteens need strong food safety","<p>Canteens prepare and hold food for busy lunch periods, which creates time and temperature pressure. Pre-made sandwiches, hot food and dairy items can spend too long in the <strong>danger zone (5&ndash;60&deg;C)</strong> if not managed. Children are also a vulnerable group, so the consequences of a mistake are higher.</p>"),
    ("Volunteers count as food handlers","<p>Parent and community volunteers who handle food must follow the same safe practices as paid staff: hand washing, avoiding cross-contamination, keeping cold food cold and hot food hot, and reporting illness. A short induction and food safety knowledge protect both children and the canteen.</p>"),
    ("Allergens and healthy canteen rules","<p>Allergen management is vital — declare and separate the 10 priority allergens and follow each student's allergy plan. Many states also run healthy canteen guidelines, but those sit alongside, not instead of, food safety. Revise with our <a href=\"/topic-allergens.html\">allergen</a> and <a href=\"/topic-temperature.html\">temperature</a> drills.</p>"),
    ("How to get certified","<p>Canteen staff (and often the supervisor) complete SITXFSA005 / SITXFSA006 through an RTO. Use this free test to prepare, then certify with an accredited provider. <a href=\"/find-a-course.html\" rel=\"sponsored nofollow\">Compare courses &rarr;</a></p>"),
  ],
  "faqs":[
    ("Do school canteen volunteers need food safety training?","Volunteers who handle food must follow safe food handling practices and should receive food safety knowledge or induction. Whether formal certification is required depends on the canteen and Standard 3.2.2A; many appoint a certified Food Safety Supervisor."),
    ("What are the biggest risks in a school canteen?","Time and temperature abuse during busy lunch periods, cross-contamination, and allergen mistakes. Keeping cold food at or below 5°C, hot food at or above 60°C and managing allergens are the key controls."),
    ("Does Standard 3.2.2A apply to school canteens?","It extended requirements to settings serving children. Whether a specific canteen needs an FSS depends on what it prepares and serves — check with your school and state requirements."),
    ("Are healthy canteen guidelines the same as food safety?","No. Healthy canteen guidelines are about nutrition; food safety is about preventing illness. Canteens must meet both."),
    ("Will this test certify canteen volunteers?","It's free preparation only. A nationally recognised certificate must come from an RTO, and your canteen will have its own procedures to follow."),
  ],
  "related":[("/topic-temperature.html","Temperature & Danger Zone"),("/topic-allergens.html","Allergen Management"),("/topic-cross-contamination.html","Cross Contamination"),("/topic-hygiene.html","Personal Hygiene")],
 },
 {
  "slug":"food-safety-retail.html",
  "title":"Retail Food Handler Food Safety 2026 | Australia",
  "desc":"Retail food handler food safety in Australia: deli, bakery, supermarket, takeaway. SITXFSA005 basics plus free practice questions.",
  "ogt":"Retail Food Handler Food Safety | Australia 2026",
  "accent":"Retail & Takeaway",
  "meta":"Deli · bakery · supermarket · takeaway · free practice",
  "intro":[
    "Retail food work — supermarket delis, bakeries, sandwich bars, takeaway shops and cafes — involves handling ready-to-eat and potentially hazardous food for the public. Staff turnover is high and new hires often need to be job-ready quickly, which makes solid food safety knowledge important from day one.",
    "Food handlers in retail must have food safety skills and knowledge appropriate to their role, gained through the nationally recognised unit SITXFSA005. Many retail food businesses must also appoint a certified Food Safety Supervisor under Standard 3.2.2A.",
    "This page covers what retail food handlers need to know and gives you free, exam-style practice so you can walk into your assessment — and your first shift — confident.",
  ],
  "facts":[("Setting","Deli, bakery, takeaway, cafe"),("Workforce","High turnover, many new hires"),("Core unit","SITXFSA005"),("FSS required?","Often — under Standard 3.2.2A"),("Key controls","Temperature, date marking, hygiene"),("Cert validity","5 years (FSS)")],
  "sections":[
    ("What retail food handlers must know","<p>The essentials: keep cold food at or below <strong>5&deg;C</strong> and hot food at or above <strong>60&deg;C</strong>, apply the <strong>2-hour/4-hour rule</strong>, prevent cross-contamination between raw and ready-to-eat food, follow <strong>date marking</strong> and stock rotation (FIFO), and maintain strong personal hygiene including hand washing.</p>"),
    ("Deli and hot-food counters","<p>Sliced meats, salads and hot chickens are higher-risk ready-to-eat foods. Slicers and display units must be cleaned and sanitised, cold and hot displays must hold safe temperatures, and use-by dates must be respected. Listeria control matters wherever ready-to-eat food is handled.</p>"),
    ("Date marking and packaging","<p>Retail relies on accurate <strong>use-by</strong> (safety) and <strong>best-before</strong> (quality) dates, correct labelling including allergen declarations, and removing out-of-date stock from sale. Knowing the difference is commonly tested — see our <a href=\"/topic-storage.html\">storage &amp; labelling</a> drill.</p>"),
    ("How to get certified","<p>Complete SITXFSA005 (and SITXFSA006 for supervisors) through an RTO. This free practice test gets you ready fast; the certificate comes from an accredited provider. <a href=\"/find-a-course.html\" rel=\"sponsored nofollow\">Compare courses &rarr;</a></p>"),
  ],
  "faqs":[
    ("Do supermarket and takeaway staff need a food handler certificate?","They must have food safety skills and knowledge for their role, and SITXFSA005 is the standard unit. Many retail food businesses must also have a certified Food Safety Supervisor under Standard 3.2.2A."),
    ("What's the difference between use-by and best-before?","Use-by is a safety date — food must not be sold or eaten after it. Best-before is about quality; food may still be sold after it if safe. Retail staff are often tested on this."),
    ("How quickly can I get job-ready for retail food work?","The SITXFSA005 unit is often completed in a few hours online through an RTO. Practising here first means you're confident before the assessment and your first shift."),
    ("Why is Listeria relevant in a deli?","Listeria can grow in ready-to-eat foods like sliced meats and salads even under refrigeration, so deli hygiene, cleaning of slicers and date control are important."),
    ("Does this practice test give me a certificate?","No — it's free preparation only. Your nationally recognised certificate must be issued by a Registered Training Organisation."),
  ],
  "related":[("/topic-storage.html","Food Storage & Labelling"),("/topic-temperature.html","Temperature & Danger Zone"),("/topic-cross-contamination.html","Cross Contamination"),("/topic-food-handler.html","Food Handler Responsibilities")],
 },
]

OTHER_INDUSTRIES = [
 ("food-safety-aged-care.html","Aged Care"),
 ("food-safety-childcare.html","Childcare & Early Learning"),
 ("food-safety-school-canteen.html","School Canteens"),
 ("food-safety-retail.html","Retail & Takeaway"),
]

def build_page(p):
    intro = "\n            ".join(f"<p>{x}</p>" for x in p["intro"])
    facts = "\n                ".join(
        f'<div class="state-fact"><div class="state-fact__label">{l}</div><div class="state-fact__val">{v}</div></div>'
        for l,v in p["facts"])
    secs = "\n            ".join(
        f'<section class="guide-section"><h2>{h}</h2>{b}</section>' for h,b in p["sections"])
    faqs = "\n                ".join(
        f'<dt class="faq-question" tabindex="0" aria-expanded="false"><span>{q}</span><span class="faq-toggle">+</span></dt>\n                <dd class="faq-answer" hidden>{a}</dd>'
        for q,a in p["faqs"])
    related = "\n                ".join(
        f'<a href="{h}" class="topic-link-card">{t}</a>' for h,t in p["related"])
    others = "\n                ".join(
        f'<a href="/{h}" class="topic-link-card">{t}</a>' for h,t in OTHER_INDUSTRIES if h != p["slug"])
    schema = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in p["faqs"]]}
    schema_js = json.dumps(schema, indent=2, ensure_ascii=True)
    html = f'''<!DOCTYPE html>
<html lang="en-AU">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag("consent", "default", {{
        "ad_storage": "denied",
        "ad_user_data": "denied",
        "ad_personalization": "denied",
        "analytics_storage": "denied",
        "wait_for_update": 500
      }});
      dataLayer.push({{ "event": "default_consent_set" }});
    </script>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-N69BCEQGQ2"></script>
    <script>
      gtag('js', new Date());
      gtag('config', 'G-N69BCEQGQ2');
    </script>
    <script>
      try {{
        if (localStorage.getItem("fs_cookie_accepted_v1") === "true") {{
          document.documentElement.classList.add("cookies-accepted");
        }}
      }} catch (e) {{}}
    </script>
    <title>{p["title"]}</title>
    <meta name="description" content="{p["desc"]}">
    <meta name="robots" content="index, follow">
    <meta name="author" content="Food Safety Practice AU">
    <link rel="canonical" href="https://food-safety-practice-test-au.com/{p["slug"]}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://food-safety-practice-test-au.com/{p["slug"]}">
    <meta property="og:title" content="{p["ogt"]}">
    <meta property="og:description" content="{p["desc"]}">
    <meta property="og:image" content="https://food-safety-practice-test-au.com/og-default.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:image" content="https://food-safety-practice-test-au.com/og-default.png">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="stylesheet" href="/style.css?v=7">
    <script type="application/ld+json">
{schema_js}
    </script>
</head>
<body>
{header()}

    <section class="home-editorial-hero" aria-labelledby="job-hero-title">
        <div class="container home-editorial-hero__inner">
            <p class="home-editorial-hero__badge">Food safety by industry</p>
            <h1 id="job-hero-title" class="home-editorial-hero__title">Food Safety Training <br><span class="home-editorial-hero__accent">{p["accent"]}</span></h1>
            <p class="home-editorial-hero__meta">{p["meta"]}</p>
        </div>
    </section>

    <main class="container">
        <article class="content-page">
            {intro}
            <h2>{p["accent"]} requirements at a glance</h2>
            <div class="state-facts">
                {facts}
            </div>
            <div class="ad-slot" data-ad-slot="job-incontent" role="complementary" aria-label="Advertisement"><span class="ad-slot__label">Advertisement</span></div>
            {secs}
            <div class="content-cta">
                <h3>Practise free now</h3>
                <p>650 exam-style questions with instant explanations. No sign-up required.</p>
                <a href="/" class="btn btn-primary">Start the free practice test</a>
                <a href="/temperature-danger-zone-checker.html" class="btn btn-secondary">Danger zone tool</a>
            </div>
            <section class="guide-section">
                <h2>Related practice topics</h2>
                <div class="topic-link-grid">
                {related}
                </div>
            </section>
            <section class="guide-section">
                <h2>Food safety by industry</h2>
                <div class="topic-link-grid">
                {others}
                </div>
            </section>
            <section class="guide-section">
                <h2>{p["accent"]} Food Safety FAQ</h2>
                <dl>
                {faqs}
                </dl>
            </section>
            <div class="affiliate-card" style="margin-top:18px;">
                <p class="affiliate-eyebrow">Ready for the real thing?</p>
                <h3 class="affiliate-heading">Book your accredited food safety course</h3>
                <p class="affiliate-text">Practice gets you exam-ready, but your certificate must be issued by a registered training organisation. Compare providers in your state from $85.</p>
                <div class="affiliate-actions" style="display:flex;gap:10px;flex-wrap:wrap;">
                <a href="/" class="btn btn-primary">Start free practice test &rarr;</a>
                <a href="/find-a-course.html" class="btn btn-secondary affiliate-cta" rel="sponsored nofollow">Find an accredited course &rarr;</a></div>
                <p class="affiliate-disclosure">We may earn a commission from course providers, at no extra cost to you.</p>
            </div>
        </article>
    </main>
{FOOTER}
</body>
</html>
'''
    (ROOT / p["slug"]).write_text(html, encoding="utf-8")
    return p["slug"]

if __name__ == "__main__":
    for p in PAGES:
        print("wrote", build_page(p), "| FAQs:", len(p["faqs"]), "| sections:", len(p["sections"]))
    print("DONE", len(PAGES), "industry pages")
