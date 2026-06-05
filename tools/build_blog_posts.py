#!/usr/bin/env python3
"""Build long-form SEO blog posts into blog/<slug>/index.html and rebuild blog/index.html.
Run: python3 tools/build_blog_posts.py
"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
BLOG = ROOT / "blog"
DOMAIN = "https://food-safety-practice-test-au.com"
CSS_VER = "7"

NAV = [("../../","Practice Test"),("../../guide.html","Study Guide"),
       ("../../temperature-danger-zone-checker.html","Danger Zone Tool"),("../../tips.html","Exam Tips"),
       ("../../find-a-course.html","Find a Course"),("../../blog/","Blog"),
       ("../../flashcards.html","Flashcards"),("../../glossary.html","Glossary")]
STATES = [("nsw","NSW"),("vic","VIC"),("qld","QLD"),("wa","WA"),("sa","SA"),("act","ACT"),("nt","NT"),("tas","TAS")]

def header(active_blog=True):
    nav = "\n".join(
        f'                <a href="{h}" class="nav-link{" nav-link--active" if (t=="Blog" and active_blog) else ""}">{t}</a>' for h,t in NAV)
    states = "\n".join(
        f'                <a href="../../food-safety-{c}.html" class="state-link" title="Food Safety Practice Test {a}">{a}</a>' for c,a in STATES)
    return f'''    <header class="site-header">
        <div class="container site-header__top">
            <a href="../../" class="site-brand">
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

FOOTER = '''    <footer class="footer">
        <div class="container">
            <p>&copy; 2026 Food Safety Practice AU</p>
            <nav class="footer-links">
                <a href="../../about.html">About</a>
                <span class="separator">|</span>
                <a href="../../terms.html">Terms of Use</a>
                <span class="separator">|</span>
                <a href="../../legal.html#privacy">Privacy Policy</a>
                <span class="separator">|</span>
                <a href="../../legal.html#legal">Legal Notice</a>
                <span class="separator">|</span>
                <a href="../../legal.html#contact">Contact Us</a>
            </nav>
            <p class="footer-disclaimer">We may earn a commission if you purchase through links on this site.</p>
            <p class="footer-disclaimer">This article is general information and educational practice only. It is not official certification or legal advice. Your certificate must be issued by a Registered Training Organisation (RTO).</p>
        </div>
    </footer>

    <div id="cookie-banner" class="cookie-banner" role="dialog" aria-live="polite" aria-label="Cookie notice">
        <div class="cookie-banner__content">
            <p>This site uses cookies and similar technologies to improve your experience and support analytics and advertising. By continuing to use this site, you agree to our <a href="../../legal.html#privacy">Privacy Policy</a>.</p>
            <div class="cookie-banner__actions">
                <button id="cookie-accept" class="btn btn-primary cookie-btn">Accept</button>
            </div>
        </div>
    </div>
    <script src="../../faq-accordion.js" defer></script>
    <script src="../../cookie-consent.js" defer></script>
    <script src="../../site-ui.js" defer></script>'''

def faq_block(faqs):
    items = "\n                ".join(
        f'<dt class="faq-question" tabindex="0" aria-expanded="false"><span>{q}</span><span class="faq-toggle">+</span></dt>\n                <dd class="faq-answer" hidden>{a}</dd>'
        for q,a in faqs)
    return f'''            <h2>Frequently asked questions</h2>
            <dl>
                {items}
            </dl>'''

def schema_block(title, desc, slug, faqs):
    faq = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}
    art = {"@context":"https://schema.org","@type":"Article","headline":title,
           "description":desc,"author":{"@type":"Organization","name":"Food Safety Practice AU"},
           "publisher":{"@type":"Organization","name":"Food Safety Practice AU"},
           "datePublished":"2026-06-05","dateModified":"2026-06-05",
           "image":f"{DOMAIN}/og-default.png",
           "mainEntityOfPage":f"{DOMAIN}/blog/{slug}"}
    breadcrumb = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":f"{DOMAIN}/"},
        {"@type":"ListItem","position":2,"name":"Blog","item":f"{DOMAIN}/blog"},
        {"@type":"ListItem","position":3,"name":title,"item":f"{DOMAIN}/blog/{slug}"}]}
    return ('    <script type="application/ld+json">\n'+json.dumps(art,indent=2,ensure_ascii=True)+'\n    </script>\n'
            '    <script type="application/ld+json">\n'+json.dumps(faq,indent=2,ensure_ascii=True)+'\n    </script>\n'
            '    <script type="application/ld+json">\n'+json.dumps(breadcrumb,indent=2,ensure_ascii=True)+'\n    </script>')

CTA = '''            <div class="guide-cta">
                <h3>Practice for free</h3>
                <p>Test yourself with 650 exam-style questions across 12 topics. Instant feedback, no sign-up.</p>
                <a href="../../" class="btn btn-primary">Start the free practice test</a>
                <a href="../../temperature-danger-zone-checker.html" class="btn btn-secondary">Danger zone tool</a>
            </div>'''

POSTS = []

def post(slug, title, desc, h1, lead, body, faqs):
    POSTS.append(dict(slug=slug, title=title, desc=desc, h1=h1, lead=lead, body=body, faqs=faqs))

# ── POST: How to pass (expanded) ────────────────────────────────────────────
post(
 "how-to-pass-food-safety-test",
 "How to Pass the Food Safety Test in 2026",
 "Step-by-step study plan to pass the SITXFSA005 food safety test in Australia: key temperatures, topic checklist and the score to aim for.",
 "How to Pass the Food Safety Test in 2026",
 "Passing your food safety assessment is mostly about <strong>understanding a handful of core rules</strong> &mdash; especially temperature control &mdash; and practising until you can apply them in scenario questions. This step-by-step plan works whether you are new to hospitality or refreshing before an RTO assessment.",
 '''            <h2>Step 1: Know the numbers that appear on every test</h2>
            <p>Before anything else, memorise the temperatures and time rules that show up again and again. Do not just recite them &mdash; understand <em>why</em> each one exists (bacteria multiply fastest between 5&deg;C and 60&deg;C).</p>
            <table class="cook-table">
                <thead><tr><th>Rule</th><th>Target</th></tr></thead>
                <tbody>
                    <tr><td>Temperature danger zone</td><td class="temp-val">5&deg;C &ndash; 60&deg;C</td></tr>
                    <tr><td>Cold storage (fridge)</td><td class="temp-val">5&deg;C or below</td></tr>
                    <tr><td>Hot holding / display</td><td class="temp-val">60&deg;C or above</td></tr>
                    <tr><td>Cook poultry &amp; minced meat (centre)</td><td class="temp-val">75&deg;C</td></tr>
                    <tr><td>Reheat cooked food</td><td class="temp-val">70&deg;C+</td></tr>
                    <tr><td>FSS certificate renewal</td><td class="temp-val">every 5 years</td></tr>
                </tbody>
            </table>
            <p>Use our <a href="../../temperature-danger-zone-checker.html">danger zone checker</a> to practise applying these numbers to real scenarios, and read the full <a href="../temperature-danger-zone-australia-guide/">temperature danger zone guide</a> if any row is unclear.</p>
            <h2>Step 2: Work through all 12 syllabus topics</h2>
            <p>The assessment draws from the full food safety syllabus, not just temperature. Spend at least one short session on each area:</p>
            <ul>
                <li>Food Standards Code &amp; legislation</li>
                <li>Food handler responsibilities &amp; personal hygiene</li>
                <li>Temperature &amp; the danger zone</li>
                <li>Cross contamination &amp; cleaning/sanitising</li>
                <li>Allergen management (all 10 priority allergens)</li>
                <li>Storage, labelling, pest control, HACCP basics</li>
                <li>Food Safety Supervisor duties &amp; high-risk foods</li>
            </ul>
            <p>Our <a href="../../guide.html">study guide</a> links to focused pages for each topic. Pick your weakest two and drill them on the <a href="../../">free practice test</a> using topic mode. For deeper reading on the trickiest areas, see our guides on <a href="../cross-contamination-food-safety-exam-tips/">cross contamination</a>, <a href="../10-priority-allergens-australia-food-safety-exam/">10 priority allergens</a>, and <a href="../haccp-basics-food-handlers-australia/">HACCP basics</a>.</p>
            <h2>Step 3: Practise under exam conditions</h2>
            <p>Reading notes is not enough. You need to answer <strong>40 multiple-choice questions</strong> under time pressure, the way most RTO assessments work.</p>
            <ul>
                <li><strong>Week 1:</strong> Take a full 40-question practice test open-book. Note every wrong answer and read the explanation.</li>
                <li><strong>Week 2:</strong> Retake without notes. Use timed exam mode if your RTO assessment is timed.</li>
                <li><strong>Daily:</strong> Complete the daily challenge on the homepage and flip through <a href="../../flashcards.html">flashcards</a> on your phone during breaks.</li>
            </ul>
            <p>After each attempt, use review weak questions to retest only what you missed &mdash; much faster than starting from scratch every time.</p>
            <h2>Step 4: Fix your weak spots before booking the real test</h2>
            <p>Most people who struggle on the real assessment failed to fix the same two topics on practice tests: <strong>temperature/scenario questions</strong> and <strong>allergens</strong>. If you are below 80% on practice tests, do not book your RTO assessment yet. Drill <a href="../../topic-temperature.html">temperature</a> and <a href="../../topic-allergens.html">allergens</a> until your score holds. Also review <a href="../cross-contamination-food-safety-exam-tips/">cross contamination scenarios</a> &mdash; they often combine with temperature questions.</p>
            <p>Not sure how hard the real thing feels? Read <a href="../is-food-safety-test-hard-australia/">Is the food safety test hard?</a> for an honest breakdown of question types and pass expectations.</p>
            <h2>What score should you aim for?</h2>
            <p>Aim to score <strong>80% or higher on full practice tests at least twice in a row</strong> before your official assessment. That mirrors the pass mark most RTOs use and gives you a buffer for nerves on the day. Our practice test is educational only &mdash; your certificate must still come from an accredited RTO &mdash; but hitting 80%+ here is the best predictor that you are ready.</p>
            <h2>Step 5: Book your RTO assessment only when ready</h2>
            <p>Once you hit 80%+ twice, choose your unit (<a href="../food-safety-supervisor-vs-food-handler/">food handler vs FSS</a>), compare <a href="../food-safety-certificate-cost-australia-by-state/">costs by state</a>, and book through an accredited RTO. Until then, keep practising &mdash; retesting weak topics costs nothing and saves you a failed assessment fee.</p>
            <p>More detail on study technique: <a href="../../tips.html">exam tips</a> &middot; <a href="../food-safety-practice-test-before-real-exam/">why practice tests matter</a></p>''',
 [("How long should I study before the food safety test?","Most people need 3&ndash;10 hours of focused study depending on experience. Spread it over several days rather than one cram session."),
  ("Can I pass using only free practice tests?","Free practice tests prepare you for the knowledge component, but your official certificate must be issued by a Registered Training Organisation (RTO) after their assessment."),
  ("What topics are tested most often?","Temperature control, cross contamination, personal hygiene, and allergens appear most frequently. HACCP and FSS duties are also common on supervisor-level assessments."),
  ("Should I use timed practice before the real exam?","Yes, if your RTO uses a time limit. Our timed exam mode mirrors a 40-minute full test and builds the pace and calm you need on the day.")],
)

# ── POST: FSS vs food handler (expanded) ────────────────────────────────────
post(
 "food-safety-supervisor-vs-food-handler",
 "Food Safety Supervisor vs Food Handler",
 "SITXFSA005 vs SITXFSA006 explained: who needs which certificate in Australia, Standard 3.2.2A changes, and how to prepare with free practice.",
 "Food Safety Supervisor vs Food Handler: What's the Difference?",
 "If you are starting in food work &mdash; or your manager has asked you to get &ldquo;the food safety cert&rdquo; &mdash; you may see two unit codes: <strong>SITXFSA005</strong> and <strong>SITXFSA006</strong>. They are related but not the same. This guide explains the difference, who needs which one, and how the December 2023 training expansion affects schools, childcare, aged care, and charities.",
 '''            <h2>SITXFSA005: food handler</h2>
            <p><strong>SITXFSA005 &mdash; Use hygienic practices for food safety</strong> is the core unit for food handlers. It covers what most people think of as &ldquo;food safety training&rdquo;:</p>
            <ul>
                <li>Personal hygiene and reporting illness</li>
                <li>Temperature control and the danger zone (5&deg;C&ndash;60&deg;C)</li>
                <li>Preventing cross contamination</li>
                <li>Cleaning and sanitising</li>
                <li>Basic allergen awareness</li>
                <li>Safe receiving, storage, and disposal of food</li>
            </ul>
            <p>Anyone who handles unpackaged food in a commercial kitchen, café, catering operation, or similar setting typically needs this level of skills and knowledge. Many employers expect a certificate showing you have completed SITXFSA005 (or equivalent training) before you start handling food.</p>
            <h2>SITXFSA006: Food Safety Supervisor</h2>
            <p><strong>SITXFSA006 &mdash; Participate in safe food handling practices</strong> builds on the food handler unit. A <strong>Food Safety Supervisor (FSS)</strong> is the person responsible for overseeing food safety on site &mdash; monitoring procedures, training staff, keeping records, and acting when something goes wrong.</p>
            <p>FSS training usually includes SITXFSA005 content plus supervisor-level topics such as:</p>
            <ul>
                <li>Implementing and monitoring the food safety program</li>
                <li>HACCP principles and critical control points</li>
                <li>Responding to incidents and non-conformances</li>
                <li>Coordinating cleaning, pest control, and supplier issues</li>
            </ul>
            <p>Most RTOs deliver SITXFSA005 and SITXFSA006 together for people training as an FSS. You cannot skip the handler knowledge &mdash; the supervisor role assumes you already understand it.</p>
            <h2>Who must have a Food Safety Supervisor on site?</h2>
            <p>Under the Food Standards Code, most <strong>Class 1 and Class 2 food businesses</strong> &mdash; cafés, restaurants, takeaway shops, caterers, and many other premises that handle potentially hazardous food &mdash; must appoint at least one FSS. That person must hold a current certificate and, in most cases, be on the premises or readily available during operation.</p>
            <p>Exact requirements can vary slightly by state regulator. For state-specific context see our pages for <a href="../../food-safety-nsw.html">NSW</a>, <a href="../../food-safety-vic.html">VIC</a>, and <a href="../../food-safety-qld.html">QLD</a>, or read <a href="../food-safety-certificate-cost-australia-by-state/">certificate costs by state</a>.</p>
            <h2>December 2023: Standard 3.2.2A expansion</h2>
            <p>From December 2023, <strong>Standard 3.2.2A</strong> extended food handler training requirements to more sectors, including <strong>schools, childcare, aged care, and charities</strong> that serve food. Even if you are not in a traditional restaurant, you may now need documented food handler training where you did not before.</p>
            <p>Read the full breakdown: <a href="../food-safety-training-aged-care-childcare-2023/">Food safety training for aged care, childcare &amp; schools</a>.</p>
            <h2>Which one do you need?</h2>
            <table class="cook-table">
                <thead><tr><th>Your situation</th><th>Usually need</th></tr></thead>
                <tbody>
                    <tr><td>Kitchen hand, barista, line cook (not supervising)</td><td>SITXFSA005 food handler</td></tr>
                    <tr><td>Head chef, duty manager, person in charge of food safety</td><td>SITXFSA006 FSS (+ 005)</td></tr>
                    <tr><td>Childcare / aged care food service worker</td><td>Food handler training (3.2.2A)</td></tr>
                    <tr><td>Volunteer serving food at a charity event</td><td>Check 3.2.2A &mdash; training may be required</td></tr>
                </tbody>
            </table>
            <p>When in doubt, ask your employer or check with your state food regulator. Both qualifications are nationally recognised once issued by an accredited RTO.</p>
            <h2>How to prepare before you enrol</h2>
            <p>Whether you need 005 or 006, the knowledge tested overlaps heavily with what we cover on this site. Use the <a href="../../">free 40-question practice test</a>, drill <a href="../../topic-fss-duties.html">FSS duties</a> if you are going for supervisor, and follow our <a href="../how-to-pass-food-safety-test/">step-by-step pass guide</a> before your RTO assessment. See also <a href="../how-to-get-food-safety-certificate-online-australia/">how to get a certificate online</a> and <a href="../food-safety-certificate-expire-renewal-australia/">renewal rules</a> if you are recertifying.</p>''',
 [("Can one person be both food handler and Food Safety Supervisor?","Yes. The FSS is usually a senior staff member who also handles food. They hold SITXFSA006 (which includes handler-level knowledge) and oversee others who may hold SITXFSA005 or equivalent training."),
  ("Is SITXFSA005 enough to be a Food Safety Supervisor?","No. An FSS must hold SITXFSA006 (or the previous equivalent units in some states). SITXFSA005 alone qualifies you as a trained food handler, not as the nominated supervisor."),
  ("Does a food handler certificate expire?","SITXFSA005 certificates do not have a fixed national expiry like FSS, but employers may require refresher training. FSS certificates must be renewed every 5 years."),
  ("Are the units accepted in every Australian state?","Yes. SITXFSA005 and SITXFSA006 are nationally recognised. Some states (notably NSW) have additional FSS registration steps, but the core units are the same.")],
)

# ── POST 1 ──────────────────────────────────────────────────────────────────
post(
 "is-food-safety-test-hard-australia",
 "Is the Food Safety Test Hard? (Australia 2026)",
 "Honest guide to how hard the SITXFSA005 food safety test is in Australia: question types, pass rates, and how to prepare with free practice.",
 "Is the Food Safety Test Hard? What to Expect in Australia (2026)",
 "If you have just been told you need a food safety certificate for work, it is normal to wonder how hard the test really is. The honest answer: for most people it is <strong>not difficult &mdash; as long as you understand the core rules rather than just memorising them</strong>. This guide explains exactly what the test covers, the question types you will see, why some people fail, and how long you should spend preparing.",
 '''            <h2>What the food safety test actually tests</h2>
            <p>The first thing to understand is that the food safety assessment is <strong>not a cooking test</strong>. It does not check whether you can julienne a carrot or plate a dish. It assesses your knowledge under the nationally recognised unit <strong>SITXFSA005 &mdash; Use hygienic practices for food safety</strong> (and SITXFSA006 if you are training as a Food Safety Supervisor).</p>
            <p>In plain terms, it checks that you understand how to keep food safe: temperature control, personal hygiene, cleaning and sanitising, preventing cross-contamination, allergen awareness, and reporting illness. These are practical, common-sense topics &mdash; but they come with specific numbers and rules you need to know.</p>
            <h2>Typical question types</h2>
            <p>Most assessments use <strong>multiple-choice questions</strong>, often with some true/false or short scenario questions. Expect a mix of:</p>
            <ul>
                <li><strong>Temperature numbers</strong> &mdash; the danger zone (5&deg;C&ndash;60&deg;C), cooking temperatures (75&deg;C for poultry and mince), cold storage (5&deg;C or below) and hot holding (60&deg;C or above).</li>
                <li><strong>Cross-contamination</strong> &mdash; separating raw and ready-to-eat food, colour-coded boards, and when to wash hands or change gloves.</li>
                <li><strong>Allergens</strong> &mdash; recognising the priority allergens and how to avoid cross-contact.</li>
                <li><strong>Scenario questions</strong> &mdash; for example, &ldquo;food has been left out for three hours, what do you do?&rdquo; These test whether you can apply the rules, not just recite them.</li>
            </ul>
            <p>You can see exactly these formats on our <a href="../../">free practice test</a> and drill the trickiest area on the <a href="../../topic-temperature.html">temperature and danger zone</a> page.</p>
            <h2>Why people fail (and how to avoid it)</h2>
            <p>The most common reason people struggle is <strong>memorising numbers without understanding them</strong>. If you simply try to remember &ldquo;5 to 60&rdquo; without understanding <em>why</em> that range is dangerous (bacteria multiply fastest there), the scenario questions will catch you out. When you understand the reasoning, the answers become obvious even when the question is worded in an unfamiliar way.</p>
            <p>The second reason is rushing. Read each question fully &mdash; watch for words like <em>not</em>, <em>except</em> and <em>always</em>, which change the answer entirely.</p>
            <h2>How long does study take?</h2>
            <p>It depends on your experience:</p>
            <ul>
                <li><strong>Experienced hospitality workers:</strong> often just 3&ndash;4 hours of focused revision.</li>
                <li><strong>Newcomers to food work:</strong> around 6&ndash;10 hours, spread over a few sessions, is plenty.</li>
            </ul>
            <p>Short, regular study beats one long cram session. Follow our step-by-step <a href="../how-to-pass-food-safety-test/">how to pass guide</a>, or see quick <a href="../../tips.html">exam tips</a>. Heavy topics to drill include <a href="../haccp-basics-food-handlers-australia/">HACCP basics</a>, <a href="../10-priority-allergens-australia-food-safety-exam/">allergens</a>, and <a href="../cross-contamination-food-safety-exam-tips/">cross contamination</a>.</p>
            <h2>RTO assessment vs our free practice test</h2>
            <p>It is important to be clear about the difference. The <strong>official assessment</strong> is delivered by a Registered Training Organisation (RTO) and leads to a nationally recognised certificate. Our site is a <strong>free practice and revision tool</strong> &mdash; it helps you prepare and shows you where you are weak, but it does not issue a certificate. Think of practice tests as your rehearsal and the RTO as opening night.</p>
            <h2>What score should I aim for on practice tests?</h2>
            <p>Aim to <strong>consistently score 80% or higher</strong> on full practice tests before you sit the real assessment. Most RTOs require around 80% to pass, so hitting that mark reliably (not just once) is a strong sign you are ready. If you are sitting at 60&ndash;70%, focus on your weakest topics &mdash; usually temperature control and allergens &mdash; and retest until the score sticks.</p>''',
 [("Is the food safety test timed?","Some RTO assessments are timed and some are not &mdash; it varies by provider. Practising under a self-imposed time limit (our exam mode adds a timer) builds the speed and calm you need either way."),
  ("Can I retake the food safety test if I fail?","Yes. RTOs generally allow you to review the material and re-attempt the assessment. Our free practice test can be taken unlimited times to build your score first."),
  ("Is the food safety test the same in every state?","The knowledge (SITXFSA005/006) is nationally recognised and consistent, but some states add requirements &mdash; for example, NSW has its own Food Safety Supervisor scheme. The core test content is the same."),
  ("Do I need the food safety test for hospitality?","Most hospitality roles that involve handling unpackaged food require food safety skills and knowledge, and many businesses must appoint a certified Food Safety Supervisor under Standard 3.2.2A. Check the requirement for your specific role and state.")],
)

# ── POST 2 ──────────────────────────────────────────────────────────────────
post(
 "temperature-danger-zone-australia-guide",
 "Temperature Danger Zone Australia: Complete Guide",
 "Everything you need to know about the 5°C–60°C danger zone in Australia: hot hold, cold storage, 2-hour/4-hour rule, and exam tips.",
 "Temperature Danger Zone Australia: Complete Guide (5°C to 60°C)",
 "Temperature control is the single most important &mdash; and most tested &mdash; topic in Australian food safety. Get the <strong>danger zone (5&deg;C to 60&deg;C)</strong> right and you will prevent most cases of foodborne illness and answer a large share of your exam questions correctly. This is the complete guide.",
 '''            <h2>Why the danger zone exists</h2>
            <p>Between <strong>5&deg;C and 60&deg;C</strong>, the bacteria that cause food poisoning multiply rapidly &mdash; some can double in number every 20 minutes. The goal of almost every temperature rule is the same: keep potentially hazardous food <strong>out of this range</strong>, either colder than 5&deg;C or hotter than 60&deg;C. Want to test any temperature instantly? Use our <a href="../../temperature-danger-zone-checker.html">interactive danger-zone checker</a>.</p>
            <h2>The key temperatures at a glance</h2>
            <table class="cook-table">
                <thead><tr><th>Step</th><th>Target</th></tr></thead>
                <tbody>
                    <tr><td>Cold storage (fridge)</td><td class="temp-val">5&deg;C or below</td></tr>
                    <tr><td>Frozen storage (freezer)</td><td class="temp-val">about &minus;18&deg;C</td></tr>
                    <tr><td>Hot holding / display</td><td class="temp-val">60&deg;C or above</td></tr>
                    <tr><td>Cook poultry &amp; minced meat</td><td class="temp-val">75&deg;C centre</td></tr>
                    <tr><td>Reheating cooked food</td><td class="temp-val">at least 70&deg;C</td></tr>
                    <tr><td>Cooling: 60&deg;C &rarr; 21&deg;C</td><td class="temp-val">within 2 hours</td></tr>
                    <tr><td>Cooling: 21&deg;C &rarr; 5&deg;C</td><td class="temp-val">within 4 more hours</td></tr>
                </tbody>
            </table>
            <h2>Hot holding: 60&deg;C and above</h2>
            <p>Food on display or being held for service &mdash; bain-maries, heat lamps, hot boxes &mdash; must stay at <strong>60&deg;C or hotter</strong>. At that temperature bacteria stop multiplying. If hot-held food drops below 60&deg;C, you must reheat it to 75&deg;C or discard it within the time limits.</p>
            <h2>Cold storage: 5&deg;C and below</h2>
            <p>Fridges must keep potentially hazardous food at <strong>5&deg;C or below</strong>. Check the temperature daily, do not overload the fridge (cold air must circulate), and never put large hot pots straight inside &mdash; they warm everything around them.</p>
            <h2>Cooking and reheating temperatures</h2>
            <p>Cook <strong>poultry and minced meat to 75&deg;C</strong> in the centre, because mincing spreads surface bacteria all the way through. Reheat cooked food rapidly to <strong>at least 70&deg;C</strong> before hot-holding. Always measure with a clean, calibrated probe thermometer in the thickest part &mdash; colour and time are unreliable.</p>
            <h2>The 2-hour / 4-hour rule, explained simply</h2>
            <p>This rule covers ready-to-eat potentially hazardous food that has been in the danger zone. Add up the <strong>total</strong> time, then:</p>
            <ul>
                <li><strong>Under 2 hours:</strong> safe &mdash; refrigerate it for later, or use it now.</li>
                <li><strong>2 to 4 hours:</strong> use it immediately &mdash; do not put it back in the fridge.</li>
                <li><strong>Over 4 hours:</strong> throw it out.</li>
            </ul>
            <h2>Common exam trick questions</h2>
            <p>Examiners love the danger zone because it is easy to test with scenarios. A classic: <em>&ldquo;Food has been left out for 3 hours &mdash; what do you do?&rdquo;</em> The answer is <strong>use it immediately</strong> (it is in the 2&ndash;4 hour window) &mdash; not refrigerate it for tomorrow. Another: <em>&ldquo;A bain-marie reads 52&deg;C&rdquo;</em> &mdash; that is in the danger zone, so reheat to 75&deg;C and fix the unit. Practise these on our <a href="../../topic-temperature.html">temperature topic drill</a> and revise quickly with <a href="../../flashcards.html">flashcards</a>.</p>
            <h2>Fridge vs freezer</h2>
            <p>Keep them straight: the <strong>fridge</strong> holds chilled food at 5&deg;C or below; the <strong>freezer</strong> holds frozen food at around &minus;18&deg;C. Freezing pauses bacteria but does not kill them, so food that has fully thawed and warmed should not be refrozen.</p>
            <h2>Thawing safely</h2>
            <p>How you thaw matters as much as how you cook. The safe methods are: <strong>in the fridge</strong> (best), <strong>as part of the cooking process</strong>, or <strong>in the microwave if you cook immediately after</strong>. The unsafe method &mdash; and a favourite exam wrong-answer &mdash; is leaving food on the bench at room temperature, where the outside sits in the danger zone for hours while the centre is still frozen.</p>
            <h2>Receiving and transport temperatures</h2>
            <p>Temperature control starts at the back door. Cold deliveries should arrive at <strong>5&deg;C or below</strong> and hot food at <strong>60&deg;C or above</strong>; if not, assess and consider rejecting them. The same applies to transport &mdash; catering and deliveries must keep cold food cold and hot food hot using insulated or refrigerated containers, with a check on arrival.</p>
            <h2>Calibrating your thermometer</h2>
            <p>Your monitoring is only as good as your probe. Check it in an <strong>ice slurry (should read 0&deg;C)</strong> and in <strong>boiling water (about 100&deg;C at sea level)</strong>. If it's out, it needs adjusting or replacing &mdash; an inaccurate thermometer can convince you unsafe food is safe. Clean and sanitise the probe before and between uses to avoid cross-contamination.</p>
            <h2>Put the numbers to the test</h2>
            <p>The fastest way to lock these temperatures in is to use them. Slide through scenarios on the <a href="../../temperature-danger-zone-checker.html">danger-zone checker</a>, then prove it on the <a href="../../">free practice test</a>. Temperature questions often appear alongside <a href="../cross-contamination-food-safety-exam-tips/">cross contamination</a> and <a href="../10-priority-allergens-australia-food-safety-exam/">allergen</a> scenarios &mdash; read those guides too. If you're studying for a specific state, start from your <a href="../../food-safety-nsw.html">state page</a> or follow our <a href="../how-to-pass-food-safety-test/">how to pass guide</a>.</p>''',
 [("What is the temperature danger zone?","The temperature danger zone is 5&deg;C to 60&deg;C. Bacteria multiply rapidly in this range, so potentially hazardous food must be kept below 5&deg;C or above 60&deg;C."),
  ("How long can food stay out of the fridge?","Use the 2-hour/4-hour rule: under 2 hours total in the danger zone you can refrigerate or use it; 2 to 4 hours, use it immediately; over 4 hours, throw it out."),
  ("What temperature should hot food be held at?","Hot food on display or being held for service must be kept at 60&deg;C or above to stop bacteria multiplying."),
  ("What temperature should I reheat food to?","Reheat cooked food rapidly to at least 70&deg;C (many businesses target 75&deg;C) before hot-holding it at 60&deg;C or above.")],
)

# ── POST 3 ──────────────────────────────────────────────────────────────────
post(
 "food-safety-certificate-cost-australia-by-state",
 "Food Safety Certificate Cost by State (2026)",
 "Typical food safety certificate prices in NSW, VIC, QLD and all states: food handler vs FSS, online vs classroom. Informational guide only.",
 "Food Safety Certificate Cost in Australia by State (2026 Guide)",
 "How much does a food safety certificate cost in Australia? It depends on the unit you need, your state, and whether you study online or in a classroom. This is an <strong>informational guide</strong> to typical 2026 price ranges &mdash; we do not sell courses, so the figures below are general indications only. Always compare accredited RTOs in your state for current prices.",
 '''            <h2>What you are paying for</h2>
            <p>There are two nationally recognised units, and they cost different amounts:</p>
            <ul>
                <li><strong>SITXFSA005 (Food Handler)</strong> &mdash; the basic hygienic-practices unit. This is the cheaper option.</li>
                <li><strong>SITXFSA006 (Food Safety Supervisor)</strong> &mdash; usually bundled with 005 and priced higher because it covers supervising food safety.</li>
            </ul>
            <p>Not sure which one you need? Read <a href="../food-safety-supervisor-vs-food-handler/">Food Safety Supervisor vs Food Handler</a> first.</p>
            <h2>Typical price ranges (2026, indicative)</h2>
            <p>Prices vary widely between RTOs. As a rough guide, food handler (SITXFSA005) courses online are often in the <strong>$25&ndash;$60</strong> range, while Food Safety Supervisor (SITXFSA005 + SITXFSA006) courses typically run <strong>$85&ndash;$230</strong>. Classroom delivery costs more than online. Some states add a certificate or scheme fee.</p>
            <table class="cook-table">
                <thead><tr><th>State / Territory</th><th>Food Handler (005)</th><th>FSS (005+006)</th></tr></thead>
                <tbody>
                    <tr><td><a href="../../food-safety-nsw.html">NSW</a> (own FSS scheme)</td><td class="temp-val">~$25&ndash;$60</td><td class="temp-val">~$120&ndash;$230</td></tr>
                    <tr><td><a href="../../food-safety-vic.html">VIC</a> (free DoFoodSafely for handlers)</td><td class="temp-val">free&ndash;$60</td><td class="temp-val">~$85&ndash;$200</td></tr>
                    <tr><td><a href="../../food-safety-qld.html">QLD</a></td><td class="temp-val">~$25&ndash;$60</td><td class="temp-val">~$90&ndash;$200</td></tr>
                    <tr><td><a href="../../food-safety-wa.html">WA</a></td><td class="temp-val">~$25&ndash;$60</td><td class="temp-val">~$90&ndash;$200</td></tr>
                    <tr><td><a href="../../food-safety-sa.html">SA</a></td><td class="temp-val">~$25&ndash;$60</td><td class="temp-val">~$90&ndash;$200</td></tr>
                    <tr><td><a href="../../food-safety-act.html">ACT</a></td><td class="temp-val">~$25&ndash;$60</td><td class="temp-val">~$90&ndash;$200</td></tr>
                    <tr><td><a href="../../food-safety-nt.html">NT</a></td><td class="temp-val">~$25&ndash;$60</td><td class="temp-val">~$90&ndash;$200</td></tr>
                    <tr><td><a href="../../food-safety-tas.html">TAS</a></td><td class="temp-val">~$25&ndash;$60</td><td class="temp-val">~$90&ndash;$200</td></tr>
                </tbody>
            </table>
            <p><em>Indicative only &mdash; confirm current pricing with accredited RTOs in your state.</em></p>
            <h2>What affects the price</h2>
            <ul>
                <li><strong>Online vs classroom:</strong> online self-paced is cheapest; face-to-face costs more for the trainer's time.</li>
                <li><strong>Express certificates:</strong> same-day marking or rushed issuing often adds a fee.</li>
                <li><strong>State scheme fees:</strong> NSW, for example, has its own Food Safety Supervisor certificate scheme that can add to the cost.</li>
                <li><strong>Bundles:</strong> doing 005 and 006 together is usually cheaper than separately.</li>
            </ul>
            <h2>How to keep the cost down (legitimately)</h2>
            <p>Only buy the unit you actually need &mdash; many handlers do not need the full FSS qualification. In Victoria, the free <strong>DoFoodSafely</strong> program builds handler knowledge at no cost (though it is not a nationally recognised certificate). And prepare with free practice first so you pass the assessment the first time and do not pay for re-sits. Our <a href="../../">free practice test</a> and <a href="../../guide.html">study guide</a> cost nothing.</p>
            <p>We do not recommend specific paid providers. When you are ready, <strong>compare accredited RTOs in your state</strong> on training.gov.au or your state regulator's site.</p>
            <h2>Online vs classroom: the cost trade-off</h2>
            <p>Online self-paced courses are almost always the cheapest because there is no trainer time to pay for, and you can finish in a few hours. Classroom delivery costs more but suits people who want face-to-face support or prefer a structured session. Both lead to the same nationally recognised unit, so for most people online is the value choice. For the full process, see <a href="../how-to-get-food-safety-certificate-online-australia/">how to get a food safety certificate online</a>.</p>
            <h2>Hidden costs to watch for</h2>
            <ul>
                <li><strong>Express/same-day issuing</strong> fees on top of the course price.</li>
                <li><strong>State scheme or certificate fees</strong> (for example, NSW's Food Safety Supervisor scheme).</li>
                <li><strong>Re-sit fees</strong> if you fail &mdash; which is exactly why preparing with free practice first pays off.</li>
                <li><strong>Buying the wrong unit</strong> &mdash; paying for the full FSS when you only needed the food handler unit.</li>
            </ul>
            <h2>Is the cheapest option always best?</h2>
            <p>Cheapest is fine <em>if</em> the provider is a genuine accredited RTO &mdash; always verify on training.gov.au. Be cautious of anything that looks too cheap and isn't a registered provider, because a certificate that isn't nationally recognised is money wasted. Value comes from a recognised certificate you pass first time, not the lowest sticker price.</p>''',
 [("What is the cheapest way to get food safety certified?","Choose online self-paced delivery and only the unit you need (food handler vs FSS). In Victoria the free DoFoodSafely program covers handler knowledge. Preparing with free practice first helps you pass first time and avoid re-sit fees."),
  ("Is an online food safety certificate valid in all states?","A certificate for the nationally recognised units (SITXFSA005/006) from an accredited RTO is recognised across Australia, though NSW runs its own Food Safety Supervisor scheme with extra requirements."),
  ("Why does the FSS course cost more than food handler?","The Food Safety Supervisor qualification includes an extra unit (SITXFSA006) covering supervising food safety, so it involves more training and assessment than the food handler unit alone."),
  ("Does a food safety certificate expire?","Food Safety Supervisor certificates generally need renewal every 5 years. Employers or states may also expect food handlers to refresh their training periodically.")],
)

# ── POST 4 ──────────────────────────────────────────────────────────────────
post(
 "how-to-get-food-safety-certificate-online-australia",
 "Get a Food Safety Certificate Online (AU)",
 "Step-by-step guide to getting your food safety certificate online in Australia: SITXFSA005, RTO requirements, and how to prepare with free practice.",
 "How to Get a Food Safety Certificate Online in Australia",
 "Getting a food safety certificate online in Australia is straightforward once you know the steps. You complete a nationally recognised unit through an accredited training provider, pass the assessment, and receive your certificate &mdash; often within a day. Here is the full process, plus how to prepare so you pass first time.",
 '''            <h2>Step 1: Confirm which unit you need</h2>
            <p>There are two options. <strong>SITXFSA005</strong> (Use hygienic practices for food safety) is for food handlers. <strong>SITXFSA006</strong> (Participate in safe food handling practices) is the additional unit for Food Safety Supervisors, usually done together with 005. If you are unsure, read <a href="../food-safety-supervisor-vs-food-handler/">Food Safety Supervisor vs Food Handler</a> &mdash; choosing the right unit saves you money and time.</p>
            <h2>Step 2: Find an accredited RTO</h2>
            <p>Your certificate is only valid if it comes from a <strong>Registered Training Organisation (RTO)</strong>. You can verify any provider on the national register at <strong>training.gov.au</strong>, or check your state regulator's approved-provider list. In NSW, the Food Safety Supervisor course must be done through an RTO approved by the NSW Food Authority.</p>
            <h2>Step 3: Complete the online training and assessment</h2>
            <p>Online courses are usually <strong>self-paced</strong>: you work through the learning material, then complete the assessment (typically multiple choice, sometimes with short scenario questions). Many can be finished in a few hours. Because there is no trainer beside you, going in well-prepared matters &mdash; which is where free practice helps.</p>
            <h2>Step 4: Receive your certificate</h2>
            <p>Once you pass, the RTO issues a <strong>Statement of Attainment</strong> for the unit(s). Keep a digital and printed copy &mdash; employers will ask to see it, and Food Safety Supervisor certificates need renewal every 5 years.</p>
            <h2>Online vs classroom: pros and cons</h2>
            <table class="cook-table">
                <thead><tr><th>Online</th><th>Classroom</th></tr></thead>
                <tbody>
                    <tr><td>Cheaper, self-paced, fast</td><td>Hands-on, trainer support</td></tr>
                    <tr><td>Study anywhere, anytime</td><td>Fixed times and location</td></tr>
                    <tr><td>Best for confident self-learners</td><td>Best if you prefer guidance</td></tr>
                </tbody>
            </table>
            <p>Both lead to the same nationally recognised unit. Online suits most people; classroom suits those who want face-to-face support or have limited English/literacy and prefer a trainer.</p>
            <h2>Nationally recognised = works across states</h2>
            <p>The units SITXFSA005 and SITXFSA006 are <strong>nationally recognised</strong>, so a certificate earned online in one state is accepted in others &mdash; with the note that NSW has its own Food Safety Supervisor scheme. Check your <a href="../../food-safety-nsw.html">state page</a> for local details.</p>
            <h2>Prepare first with free practice</h2>
            <p>Online assessments give you fewer chances to ask questions, so walk in confident. Use our <a href="../../">free 650-question practice test</a> and <a href="../../guide.html">study guide</a> to revise temperature control, allergens, hygiene and cross-contamination before you start. Aim for 80%+ on practice before you sit the real thing.</p>
            <h2>What to check before you pay for an online course</h2>
            <ul>
                <li><strong>Is it a real RTO?</strong> Verify the provider on training.gov.au &mdash; a certificate that isn't nationally recognised is worthless.</li>
                <li><strong>Does it cover the right unit?</strong> SITXFSA005 for handlers, SITXFSA005 + SITXFSA006 for supervisors.</li>
                <li><strong>State requirements:</strong> in NSW the Food Safety Supervisor course must be done through an NSW Food Authority-approved RTO.</li>
                <li><strong>What's included:</strong> check whether the price covers the assessment and certificate issuing, and any express fees.</li>
            </ul>
            <h2>What online assessments usually ask</h2>
            <p>Expect multiple-choice questions on the same core areas every time: the temperature danger zone and the 2-hour/4-hour rule, cooking and reheating temperatures, hand washing and personal hygiene, cross-contamination, allergens, and cleaning vs sanitising. If you can answer our <a href="../../topic-temperature.html">temperature</a> and <a href="../../topic-allergens.html">allergen</a> drills comfortably, the online assessment will feel familiar.</p>''',
 [("How long does an online food safety certificate take?","Many online SITXFSA005 courses can be completed in a few hours, since they are self-paced. The full Food Safety Supervisor (005+006) takes a little longer."),
  ("Is an online food safety certificate accepted by employers?","Yes &mdash; as long as it is issued by an accredited RTO for the nationally recognised units, employers across Australia accept it. Always use a provider listed on training.gov.au."),
  ("Can I work before getting my certificate?","This depends on your employer and state rules. Some businesses require the certificate before your first shift; others allow supervised work while you complete it. Check with your employer."),
  ("What is an RTO?","A Registered Training Organisation is an accredited provider authorised to deliver nationally recognised training and issue certificates. Only an RTO can certify you for SITXFSA005/006.")],
)

# ── POST 5 ──────────────────────────────────────────────────────────────────
post(
 "food-safety-training-aged-care-childcare-2023",
 "Food Safety Training: Aged Care, Childcare & Schools",
 "Who needs food handler training under Standard 3.2.2A: aged care, childcare, schools and charities. December 2023 changes explained simply.",
 "Food Safety Training for Aged Care, Childcare & Schools: Standard 3.2.2A Explained",
 "In December 2023, Australia's food safety rules changed in an important way. <strong>Standard 3.2.2A</strong> expanded food-handler training and Food Safety Supervisor requirements to more sectors &mdash; including aged care, childcare, schools and charities. If you work in one of these settings, here is what it means for you in plain English.",
 '''            <h2>What is Standard 3.2.2A?</h2>
            <p>Standard 3.2.2A is part of the Australia New Zealand Food Standards Code. It introduced <strong>Food Safety Management Tools</strong> &mdash; a set of requirements designed to reduce foodborne illness. The headline changes were stronger expectations around <strong>food handler training</strong> and the appointment of a certified <strong>Food Safety Supervisor (FSS)</strong> in many businesses.</p>
            <h2>Which sectors were added?</h2>
            <p>The change is especially significant for settings that serve <strong>vulnerable people</strong>, where the consequences of unsafe food are most serious. These include:</p>
            <ul>
                <li><strong>Aged care</strong> &mdash; residents are highly vulnerable to illnesses like listeriosis. See our <a href="../../food-safety-aged-care.html">aged care food safety</a> page.</li>
                <li><strong>Childcare and early learning</strong> &mdash; young children are vulnerable and allergies are common. See <a href="../../food-safety-childcare.html">childcare food safety</a>.</li>
                <li><strong>Schools and canteens</strong> &mdash; see <a href="../../food-safety-school-canteen.html">school canteen food safety</a>.</li>
                <li><strong>Charities and community groups</strong> serving food to the public.</li>
            </ul>
            <h2>What training is required?</h2>
            <p>Food handlers in affected businesses must have food safety <strong>skills and knowledge</strong> appropriate to their work &mdash; commonly demonstrated through the nationally recognised unit <strong>SITXFSA005</strong> or an equivalent recognised program. The focus is on the practical basics: temperature control, hygiene, cleaning, cross-contamination and allergen management. Revise these on our <a href="../../topic-food-handler.html">food handler responsibilities</a> page.</p>
            <h2>Who needs a Food Safety Supervisor?</h2>
            <p>Many Category 1 and 2 businesses must appoint a certified FSS who is reasonably available during food operations. The FSS oversees food safety, guides staff and acts when something is unsafe. Learn the role on our <a href="../../topic-fss-duties.html">FSS duties</a> page and read <a href="../food-safety-supervisor-vs-food-handler/">Food Safety Supervisor vs Food Handler</a> if you are unsure which qualification you need. The FSS holds SITXFSA005 and SITXFSA006, renewed every 5 years.</p>
            <h2>Why this matters for your exam prep</h2>
            <p>If you work in aged care, childcare or a school, expect your assessment to lean on <strong>high-risk foods and vulnerable groups</strong> &mdash; why Listeria matters, why honey is unsafe for infants, and why allergen control is critical. Brush up specifically on <a href="../../topic-high-risk.html">high-risk foods and vulnerable groups</a> before you sit the test.</p>
            <h2>Practical advice for workers in these sectors</h2>
            <ul>
                <li>Confirm with your employer whether you need SITXFSA005, the full FSS qualification, or an equivalent program.</li>
                <li>Follow your workplace's documented food safety program &mdash; it is tailored to your setting.</li>
                <li>Prepare with our <a href="../../">free practice test</a>, focusing on temperature, allergens and high-risk foods.</li>
            </ul>
            <h2>What &ldquo;skills and knowledge&rdquo; actually means</h2>
            <p>The Code doesn't always demand a specific certificate for every handler &mdash; it requires that handlers have food safety <strong>skills and knowledge appropriate to their role</strong>. In practice, that is demonstrated through recognised training (like SITXFSA005), structured in-house instruction, or supervision by someone competent. In vulnerable settings, businesses lean towards formal recognised training because the stakes are higher.</p>
            <h2>Records, supervision and culture</h2>
            <p>Standard 3.2.2A is about more than a certificate on the wall. Affected businesses are expected to keep evidence that controls are working &mdash; think temperature logs, cleaning schedules and training records &mdash; and to have a Food Safety Supervisor who is reasonably available to guide staff. For workers, that means you'll be expected to actually <em>do</em> the monitoring and recording, not just know the theory. Brush up on the supervisor side via <a href="../../topic-fss-duties.html">FSS duties</a>.</p>
            <h2>Why these sectors were targeted</h2>
            <p>Children, the elderly, pregnant women and immunocompromised people can become seriously ill from foodborne pathogens that a healthy adult might shrug off &mdash; <em>Listeria</em> is the classic example, dangerous in pregnancy and aged care. Extending training requirements to these settings is a direct response to that elevated risk, which is why your assessment will emphasise <a href="../../topic-high-risk.html">high-risk foods and vulnerable groups</a>. Prepare with our <a href="../how-to-pass-food-safety-test/">how to pass guide</a> and <a href="../10-priority-allergens-australia-food-safety-exam/">allergen cheat sheet</a>.</p>''',
 [("Do childcare workers need food safety training?","If they handle, prepare or serve food, childcare workers need appropriate food safety skills and knowledge. Under Standard 3.2.2A many services must also appoint a certified Food Safety Supervisor."),
  ("Do volunteers at charities need food safety training?","Volunteers who handle food must follow safe food handling practices. Whether formal certification is required depends on the activity and what is served; many community groups provide food safety induction and appoint a supervisor."),
  ("Is a Food Safety Supervisor required in aged care kitchens?","Yes &mdash; aged care is a setting serving vulnerable people, so under Standard 3.2.2A most aged care food businesses must appoint a certified Food Safety Supervisor."),
  ("When did Standard 3.2.2A take effect?","The requirements began applying from December 2023, expanding food handler training and Food Safety Supervisor obligations to more sectors, including those serving vulnerable people.")],
)

# ── POST 6 ──────────────────────────────────────────────────────────────────
post(
 "10-priority-allergens-australia-food-safety-exam",
 "10 Priority Allergens Australia: Exam Cheat Sheet",
 "All 10 declarable allergens in Australia: names, hidden sources, and common exam questions for SITXFSA005 food safety tests.",
 "10 Priority Allergens Australia: Exam Cheat Sheet for Food Handlers",
 "Allergen questions catch out more food safety students than almost any topic except temperature. The good news: once you know the <strong>10 priority allergens</strong> and where they hide, the questions become easy marks. Here is your complete cheat sheet for the SITXFSA005 exam &mdash; and for keeping customers safe.",
 '''            <h2>The 10 priority allergens</h2>
            <p>Under Australian law, these allergens must be declared. Memorise the list, then learn the hidden sources &mdash; that is where exams (and real kitchens) trip people up. Drill them on our <a href="../../topic-allergens.html">allergen management</a> page.</p>
            <table class="cook-table">
                <thead><tr><th>Allergen</th><th>Watch out for (hidden sources)</th></tr></thead>
                <tbody>
                    <tr><td class="temp-val">Peanut</td><td>satay sauce, some baked goods, shared fryer oil</td></tr>
                    <tr><td class="temp-val">Tree nuts</td><td>pesto, praline, nut meals, garnishes</td></tr>
                    <tr><td class="temp-val">Milk</td><td>butter, cream, cheese, milk solids, some breads</td></tr>
                    <tr><td class="temp-val">Egg</td><td>mayonnaise, fresh pasta, glazes, some sauces</td></tr>
                    <tr><td class="temp-val">Wheat / gluten</td><td>soy sauce, batters, crumbs, thickeners, gravies</td></tr>
                    <tr><td class="temp-val">Soy</td><td>soy sauce, tofu, many processed/packaged foods</td></tr>
                    <tr><td class="temp-val">Sesame</td><td>tahini, hummus, seeded breads, some oils</td></tr>
                    <tr><td class="temp-val">Fish</td><td>fish sauce, Worcestershire sauce, stocks</td></tr>
                    <tr><td class="temp-val">Crustacea</td><td>prawns, crab, lobster; shared oil and utensils</td></tr>
                    <tr><td class="temp-val">Lupin</td><td>some flours and baked goods (often forgotten!)</td></tr>
                </tbody>
            </table>
            <h2>Cross-contamination (cross-contact) risk</h2>
            <p>Even a trace can trigger a severe reaction, so allergens spread through <strong>shared equipment, surfaces, hands, gloves and oil</strong>. Cooking does <em>not</em> destroy allergens. To serve an allergic customer safely, use clean or dedicated equipment, fresh ingredients and a clean surface &mdash; removing a visible allergen is not enough.</p>
            <h2>Labelling basics</h2>
            <p>On packaged food, the priority allergens must be <strong>declared clearly in plain English</strong>, both in the ingredient list and a summary statement. In food service, you must be able to give customers accurate allergen information on request &mdash; if you cannot confirm a dish is safe, say so.</p>
            <h2>Common exam mistakes</h2>
            <ul>
                <li><strong>Confusing intolerance with allergy:</strong> an allergy is an immune response that can be life-threatening (anaphylaxis); an intolerance (e.g. lactose) is uncomfortable but not usually dangerous. Exams test this distinction.</li>
                <li><strong>Forgetting lupin:</strong> it is the allergen most people leave off the list of 10. Don't.</li>
                <li><strong>Thinking cooking removes allergens:</strong> it does not.</li>
                <li><strong>Assuming &ldquo;may contain traces&rdquo; is just marketing:</strong> treat it as a real risk.</li>
            </ul>
            <h2>Study tips for allergen questions</h2>
            <p>Learn the list with a memory aid, then focus on hidden sources and the allergy-vs-intolerance distinction. Quick repetition works well here &mdash; use our <a href="../../flashcards.html">flashcards</a> and check unfamiliar terms in the <a href="../../glossary.html">glossary</a>. Then test yourself on the <a href="../../">full practice test</a> and read <a href="../cross-contamination-food-safety-exam-tips/">cross contamination exam tips</a> for allergen cross-contact scenarios.</p>
            <h2>How to handle an allergy request, step by step</h2>
            <p>Exams increasingly use real-service scenarios, and this is the safe routine to know:</p>
            <ol>
                <li><strong>Listen and take it seriously</strong> &mdash; never treat an allergy as a preference.</li>
                <li><strong>Check accurately</strong> &mdash; confirm ingredients <em>and</em> preparation (including sauces, oils and garnishes). If you can't confirm it is safe, say so honestly.</li>
                <li><strong>Prevent cross-contact</strong> &mdash; use clean or dedicated equipment, fresh ingredients and a clean surface; change gloves and wash hands.</li>
                <li><strong>Communicate clearly</strong> &mdash; tell the kitchen, and tell the customer what you can and can't guarantee.</li>
            </ol>
            <h2>Allergy vs intolerance: why it matters</h2>
            <p>An <strong>allergy</strong> is an immune reaction that can escalate to anaphylaxis &mdash; potentially fatal &mdash; from even a trace. An <strong>intolerance</strong> (such as lactose intolerance) causes discomfort but is not usually life-threatening. The controls differ: an intolerant customer may tolerate a small amount, whereas for an allergic customer there is no safe trace. Confusing these is a classic exam error and a real-world danger, so keep them distinct.</p>
            <h2>Vulnerable settings need extra care</h2>
            <p>In <a href="../../food-safety-childcare.html">childcare</a> and <a href="../../food-safety-aged-care.html">aged care</a>, allergen control is even more critical because the people served may be unable to check food themselves and may react severely. Follow each person's documented allergy plan to the letter.</p>''',
 [("What is anaphylaxis?","Anaphylaxis is a severe, rapid and potentially life-threatening allergic reaction. It can affect breathing and circulation within minutes and needs immediate adrenaline (an EpiPen) and an ambulance."),
  ("Must all allergens be listed on menus?","Food businesses must be able to provide accurate allergen information when asked. Packaged foods must declare priority allergens on the label; food service must communicate them reliably to customers."),
  ("Is gluten an allergen in Australia?","Wheat is a priority allergen and gluten must be declared. Gluten is also critical for people with coeliac disease, who must avoid even traces."),
  ("What about sulphites?","Added sulphites above a certain level must be declared on labels in Australia. They are a recognised sensitivity, though the 10 priority allergens are the core list tested in food safety training.")],
)

# ── POST 7 ──────────────────────────────────────────────────────────────────
post(
 "food-safety-certificate-expire-renewal-australia",
 "Does a Food Safety Certificate Expire? Renewal Rules",
 "How long food safety certificates last in Australia: FSS 5-year renewal, food handler rules, and what to do when your certificate expires.",
 "Does a Food Safety Certificate Expire? Renewal Rules in Australia",
 "A common question once you are certified: does it last forever? The short answer is <strong>Food Safety Supervisor certificates expire and need renewing every 5 years</strong>, while food handler training has no fixed national expiry but may need refreshing. Here is how it works and what to do when your certificate lapses.",
 '''            <h2>Food Safety Supervisor (SITXFSA006): renew every 5 years</h2>
            <p>A Food Safety Supervisor certificate is generally valid for <strong>5 years</strong> from the date of issue. Before it expires, the FSS must complete <strong>refresher training</strong> to recertify. Businesses that are required to have an FSS need to make sure their supervisor's certificate stays current &mdash; or appoint another certified FSS. Learn the role on our <a href="../../topic-fss-duties.html">FSS duties</a> page.</p>
            <h2>Food handler (SITXFSA005): no fixed national expiry</h2>
            <p>The food handler unit does not carry a fixed national expiry date the way the FSS certificate does. However, <strong>employers and some state requirements may expect periodic refresher training</strong> to keep your knowledge current, especially as rules and best practice evolve. Treat it as &ldquo;keep it fresh&rdquo; rather than &ldquo;once and forget&rdquo;.</p>
            <h2>Expired FSS vs never certified</h2>
            <p>There is an important difference. Someone whose FSS certificate has <strong>expired</strong> was trained but is now out of date &mdash; they recertify with refresher training. Someone who was <strong>never certified</strong> must complete the full qualification. Either way, if your business legally needs an FSS, you cannot rely on an expired certificate to meet that requirement.</p>
            <h2>What happens if your certificate expires while you are working?</h2>
            <p>If you are the nominated Food Safety Supervisor and your certificate lapses, the business may no longer meet its legal obligation to have a current certified FSS. In practice you should <strong>recertify before the expiry date</strong>, or the business should appoint another certified FSS to cover the gap. Don't leave it to the last minute &mdash; book refresher training ahead of time.</p>
            <h2>How to prepare for your renewal assessment</h2>
            <p>Renewal still involves an assessment, so treat it like the first time: revise the core topics &mdash; temperature control, the 2-hour/4-hour rule, allergens, cleaning and cross-contamination. Our <a href="../../">free practice test</a> and <a href="../../guide.html">study guide</a> are an easy way to knock the rust off before you recertify. Drill <a href="../10-priority-allergens-australia-food-safety-exam/">allergens</a> and <a href="../cross-contamination-food-safety-exam-tips/">cross contamination</a> if those were weak last time. If you are weighing up which qualification you need, see <a href="../food-safety-supervisor-vs-food-handler/">Food Safety Supervisor vs Food Handler</a>.</p>
            <h2>State differences</h2>
            <p>The 5-year FSS renewal cycle applies broadly, but states administer schemes differently &mdash; NSW, for example, runs its own Food Safety Supervisor certificate scheme. Check your <a href="../../food-safety-nsw.html">state page</a> for local detail.</p>
            <h2>How to never let your certificate lapse</h2>
            <ul>
                <li><strong>Diarise the expiry</strong> &mdash; set a reminder 2&ndash;3 months before the 5-year mark.</li>
                <li><strong>Book refresher training early</strong> &mdash; don't wait until the final week.</li>
                <li><strong>Keep digital and printed copies</strong> of your Statement of Attainment.</li>
                <li><strong>If you're the nominated FSS</strong>, make sure the business has cover if you're away or leave.</li>
            </ul>
            <h2>Food handler refresher: when employers ask again</h2>
            <p>Even without a national expiry date, many employers re-check food handler training every few years or when roles change. If you have not handled food for a while, a quick refresh on <a href="../temperature-danger-zone-australia-guide/">temperature rules</a> and a run through our <a href="../food-safety-practice-test-before-real-exam/">practice test guide</a> before returning to work is sensible &mdash; and often expected.</p>
            <h2>What employers check</h2>
            <p>Employers typically ask to see your certificate when you start and may re-check it periodically. For roles that legally require a Food Safety Supervisor, a current (not expired) certificate is part of the business meeting its obligations &mdash; so keeping yours valid protects your employability as well as the business.</p>''',
 [("How often do I renew my Food Safety Supervisor certificate?","Food Safety Supervisor certificates generally need renewing every 5 years through refresher training before the expiry date."),
  ("Can I keep working with an expired FSS certificate?","If your role requires a current Food Safety Supervisor certificate, an expired one does not meet the requirement. You should recertify before expiry, or the business should appoint another certified FSS."),
  ("Is renewal the same as the first certificate?","Renewal involves refresher training and assessment rather than starting from scratch, but you still demonstrate current knowledge. Revising beforehand makes it straightforward."),
  ("Do certificate expiry rules differ by state?","The 5-year FSS renewal applies broadly, but some states run their own schemes (for example NSW), so check your state's specific requirements.")],
)

# ── POST 8 ──────────────────────────────────────────────────────────────────
post(
 "haccp-basics-food-handlers-australia",
 "HACCP Basics for Food Handlers: Exam Guide",
 "Simple HACCP guide for Australian food handlers: CCPs, hazard types, monitoring, and common SITXFSA005 exam questions explained.",
 "HACCP Basics for Food Handlers: What You Need for the Exam",
 "&ldquo;HACCP&rdquo; sounds technical, but for the SITXFSA005 exam you only need the basics &mdash; not a food-science degree. This guide explains HACCP in plain English: what it stands for, the seven principles, what a Critical Control Point is, and what food handlers actually need to do. Drill it further on our <a href=\"../../topic-haccp.html\">HACCP topic</a> page.",
 '''            <h2>What does HACCP stand for?</h2>
            <p><strong>HACCP = Hazard Analysis and Critical Control Points</strong>. It is a systematic, <em>preventive</em> approach to food safety: instead of testing the finished food and hoping for the best, you identify where things could go wrong and control those points as you go.</p>
            <h2>The 7 principles in plain English</h2>
            <ol>
                <li><strong>Analyse hazards</strong> &mdash; work out what could make food unsafe.</li>
                <li><strong>Identify Critical Control Points (CCPs)</strong> &mdash; the steps where control is essential.</li>
                <li><strong>Set critical limits</strong> &mdash; the measurable line, e.g. cook to 75&deg;C.</li>
                <li><strong>Monitor</strong> &mdash; check the CCP stays within its limit (e.g. probe the temperature).</li>
                <li><strong>Corrective action</strong> &mdash; decide in advance what to do if a limit is missed (reheat or discard).</li>
                <li><strong>Verify</strong> &mdash; confirm the whole system is working (e.g. review records, calibrate thermometers).</li>
                <li><strong>Keep records</strong> &mdash; write it down to prove control and spot trends.</li>
            </ol>
            <h2>The three hazard types</h2>
            <ul>
                <li><strong>Biological</strong> &mdash; bacteria, viruses, mould (e.g. Salmonella).</li>
                <li><strong>Chemical</strong> &mdash; cleaning agents, allergens, natural toxins.</li>
                <li><strong>Physical</strong> &mdash; glass, metal, hair, plastic.</li>
            </ul>
            <h2>Critical Control Points with food examples</h2>
            <p>A CCP is a step where, if you lose control, food becomes unsafe &mdash; and there is no later step to fix it. Classic CCPs:</p>
            <ul>
                <li><strong>Cooking</strong> &mdash; reaching 75&deg;C kills pathogens (critical limit: 75&deg;C centre).</li>
                <li><strong>Cooling</strong> &mdash; the two-stage rule limits time in the danger zone.</li>
                <li><strong>Reheating</strong> &mdash; reaching at least 70&deg;C before hot-holding.</li>
            </ul>
            <h2>Hazard vs risk vs control</h2>
            <p>Exams sometimes test these words. A <strong>hazard</strong> is something that can cause harm (e.g. Salmonella in raw chicken). The <strong>risk</strong> is how likely and how serious that harm is. A <strong>control</strong> is what you do to prevent it (cook to 75&deg;C). Keep them straight and the questions are easy.</p>
            <h2>What food handlers do vs the FSS</h2>
            <p>You do not need to <em>write</em> a HACCP plan as a food handler &mdash; that is more the role of the business and the Food Safety Supervisor. Your job is to <strong>follow the controls and do the monitoring</strong>: check temperatures, cool food properly, clean and sanitise, and report when something is wrong. See <a href="../../topic-fss-duties.html">FSS duties</a> for the supervisor side and <a href="../../topic-cleaning.html">cleaning &amp; sanitising</a> for a key prerequisite.</p>
            <h2>Three real-world kitchen examples</h2>
            <ul>
                <li><strong>Roast chicken:</strong> cooking is the CCP; probe to 75&deg;C; if it reads 68&deg;C, keep cooking (corrective action).</li>
                <li><strong>Bulk bolognese:</strong> cooling is the CCP; divide into shallow trays and hit 21&deg;C in 2 hours, 5&deg;C in 4 more.</li>
                <li><strong>Leftover curry:</strong> reheating is the CCP; reach 70&deg;C+ before service, or discard if outside time limits.</li>
            </ul>
            <h2>Prerequisite programs: the foundation under HACCP</h2>
            <p>HACCP doesn't work on its own &mdash; it sits on top of everyday good practices called <strong>prerequisite programs</strong>. These include cleaning and sanitising, pest control, personal hygiene, staff training, and proper storage. If the basics aren't in place, the critical controls can't be relied on. That's why exams pair HACCP with topics like <a href="../../topic-cleaning.html">cleaning &amp; sanitising</a> and <a href="../../topic-hygiene.html">personal hygiene</a>.</p>
            <h2>Monitoring and records in a small kitchen</h2>
            <p>You don't need fancy systems. In a small cafe, monitoring a CCP might be as simple as <strong>probing the chicken and writing the temperature on a chart</strong>, checking the fridge each morning, or logging cooling times. The point of the record is twofold: it proves control if an inspector asks, and it helps you spot a pattern (like a fridge slowly creeping up) before it becomes a problem.</p>
            <h2>Why HACCP is &ldquo;preventive&rdquo;</h2>
            <p>The big idea to take into the exam: HACCP <strong>stops problems before they happen</strong> rather than testing the finished food and hoping. Designing controls into cooking, cooling and reheating &mdash; and checking them &mdash; is far more reliable than discovering a problem after the food is served. For a full study plan that includes HACCP, see <a href="../how-to-pass-food-safety-test/">how to pass the food safety test</a> and <a href="../cross-contamination-food-safety-exam-tips/">cross contamination tips</a>.</p>''',
 [("Do food handlers need full HACCP training?","No. Food handlers need to understand the basics and follow the controls and monitoring. Writing and managing the HACCP-based food safety plan is more the role of the business and the Food Safety Supervisor."),
  ("What is a Critical Control Point (CCP)?","A CCP is a step where control is essential to keep food safe and there is no later step to fix a problem &mdash; for example cooking, cooling or reheating, each with a measurable critical limit."),
  ("What is the difference between HACCP and a food safety plan?","HACCP is the method (principles for identifying and controlling hazards). A food safety plan/program is the documented system a specific business builds using those principles."),
  ("What are the three types of food safety hazard?","Biological (bacteria, viruses), chemical (cleaning agents, allergens, toxins) and physical (glass, metal, hair).")],
)

# ── POST 9 ──────────────────────────────────────────────────────────────────
post(
 "cross-contamination-food-safety-exam-tips",
 "Cross Contamination Exam Tips for Food Handlers",
 "Cross contamination explained for Australian food safety exams: direct, indirect, equipment, allergens, and common multiple-choice traps.",
 "Cross Contamination: Exam Tips Every Food Handler Must Know",
 "Cross contamination is one of the most heavily tested topics in food safety &mdash; and one of the easiest to lose marks on because of cleverly worded scenario questions. This guide breaks down every angle examiners use, then gives you five &ldquo;exam trap&rdquo; questions with explanations. Drill it live on our <a href=\"../../topic-cross-contamination.html\">cross contamination</a> page.",
 '''            <h2>What cross contamination actually means</h2>
            <p>Cross contamination is the transfer of <strong>harmful bacteria or allergens</strong> from one food, surface, person or piece of equipment to another. It is the reason raw chicken and a fresh salad must never share an unwashed board or knife.</p>
            <h2>Direct vs indirect</h2>
            <ul>
                <li><strong>Direct:</strong> raw food touches ready-to-eat food &mdash; e.g. raw chicken stored above and dripping onto a salad.</li>
                <li><strong>Indirect:</strong> bacteria travel via a go-between &mdash; hands, a knife, a board, a cloth or gloves. This is the more common (and more tested) type.</li>
            </ul>
            <h2>Raw vs ready-to-eat</h2>
            <p>Ready-to-eat food gets <strong>no further cooking step</strong> to kill bacteria, so it must be protected absolutely from raw-food contact. In the fridge, store ready-to-eat food <strong>above</strong> raw meat, with raw poultry and mince at the bottom.</p>
            <h2>Colour coding</h2>
            <p>Many kitchens use colour-coded boards and utensils to keep tasks separate &mdash; a common system: <strong>red</strong> for raw meat, <strong>yellow</strong> for raw poultry, <strong>blue</strong> for raw fish, <strong>green</strong> for fruit and veg, <strong>white</strong> for dairy/bakery. You don't always need to memorise every colour, but understand the principle: separation prevents transfer.</p>
            <h2>Hand washing vs gloves</h2>
            <p>A favourite exam point: <strong>gloves are not a substitute for hand washing</strong>. Gloves spread bacteria just like bare hands if you wear the same pair across tasks. Wash hands before gloving and change gloves (washing again) between raw and ready-to-eat work.</p>
            <h2>Allergen cross-contact vs bacterial cross-contamination</h2>
            <p>These are related but different. <strong>Bacterial</strong> cross-contamination spreads pathogens (often killed by cooking). <strong>Allergen</strong> cross-contact spreads allergen proteins &mdash; which cooking does <em>not</em> destroy. A trace of peanut transferred by a shared utensil can harm an allergic customer even after cooking. Read our full <a href="../10-priority-allergens-australia-food-safety-exam/">10 priority allergens guide</a> for the exam cheat sheet.</p>
            <h2>Clean vs sanitise</h2>
            <p>Cleaning removes visible dirt; sanitising reduces bacteria to safe levels. You must <strong>clean first, then sanitise</strong> &mdash; sanitiser doesn't work on a dirty surface. See <a href="../../topic-cleaning.html">cleaning &amp; sanitising</a> for the full method.</p>
            <h2>Exam trap section: 5 tricky scenarios</h2>
            <p><strong>1.</strong> <em>You finish cutting raw chicken and need the board for salad. What do you do?</em><br>Answer: wash, rinse and sanitise the board (or use a different clean board). Wiping with a cloth is not enough.</p>
            <p><strong>2.</strong> <em>A handler wears gloves all shift to &ldquo;stay clean&rdquo;. Safe?</em><br>Answer: no &mdash; unchanged gloves spread bacteria between tasks. Change them and wash hands between tasks.</p>
            <p><strong>3.</strong> <em>Raw beef is stored above a cooked ham. Problem?</em><br>Answer: yes &mdash; raw juices can drip onto the ready-to-eat ham. Store ready-to-eat above raw.</p>
            <p><strong>4.</strong> <em>Chips are fried in the same oil as crumbed (wheat) fish. Are the chips gluten-free?</em><br>Answer: no &mdash; shared oil carries the wheat allergen. Not safe for a gluten-avoiding customer.</p>
            <p><strong>5.</strong> <em>A cloth used on the raw-meat bench is then used to wipe the salad bench. Issue?</em><br>Answer: yes &mdash; the cloth transfers bacteria. Use separate, frequently sanitised or single-use cloths.</p>
            <p>Lock these in with our <a href="../../topic-hygiene.html">personal hygiene</a> drill and the <a href="../../">full practice test</a>. For a structured study plan, see <a href="../how-to-pass-food-safety-test/">how to pass the food safety test</a>.</p>''',
 [("Are gloves enough to prevent cross contamination?","No. Gloves spread bacteria just like bare hands if reused across tasks. Wash hands before putting gloves on and change gloves between raw and ready-to-eat tasks."),
  ("Can you use the same board for raw chicken and salad?","Not without cleaning and sanitising it first (or switching to a clean board). Wiping with a cloth does not remove the bacteria left by raw chicken."),
  ("What is cross-contact?","Cross-contact is the allergen version of cross contamination &mdash; allergen traces transferring via shared equipment, surfaces, hands or oil. Cooking does not remove allergens."),
  ("What is the difference between clean and sanitise?","Cleaning removes visible dirt and grease; sanitising reduces remaining bacteria to a safe level. You must clean before sanitising for the sanitiser to work.")],
)

# ── POST 10 ─────────────────────────────────────────────────────────────────
post(
 "food-safety-practice-test-before-real-exam",
 "Food Safety Practice Test Before the Real Exam",
 "Benefits of free food safety practice tests before your SITXFSA005 assessment: weak topics, timing, confidence, and how to use 650 questions effectively.",
 "Why You Should Take a Food Safety Practice Test Before Your Real Exam",
 "You wouldn't sit a driving test without practising &mdash; the food safety assessment is no different. A few free practice runs before your real RTO assessment is the single highest-return thing you can do. Here is why it works, backed by how learning actually sticks, and how to use practice tests effectively.",
 '''            <h2>1. It shows you your weak topics</h2>
            <p>Most people <em>think</em> they know the material until a question proves otherwise. Practice tests surface your real gaps &mdash; usually <strong>temperature control, allergens and HACCP</strong>. Instead of revising everything evenly, you can pour your time into the 2&ndash;3 topics that are actually costing you marks. Start with the <a href="../../topic-temperature.html">temperature</a> and <a href="../../topic-allergens.html">allergen</a> drills if you're unsure.</p>
            <h2>2. It builds speed for timed assessments</h2>
            <p>Some RTO assessments are timed. Practising under time pressure trains you to read carefully <em>and</em> move at a steady pace, so the clock never rattles you. Our exam mode adds a countdown so you can rehearse exactly that feeling before it counts.</p>
            <h2>3. It reduces test anxiety</h2>
            <p>A huge amount of exam stress is simply <strong>fear of the unknown</strong>. Once you have seen the question style, answered hundreds of them and watched your score climb, the real assessment feels familiar instead of frightening. Familiarity is calm.</p>
            <h2>The study science: why testing beats re-reading</h2>
            <p>Decades of research point to the same finding: <strong>actively recalling</strong> information (testing yourself) builds far stronger memory than passively re-reading notes. Every practice question forces recall, and the instant explanation corrects mistakes while they're fresh &mdash; a loop that locks knowledge in fast.</p>
            <h2>How to use practice tests effectively</h2>
            <ul>
                <li><strong>Full test</strong> &mdash; simulate the real thing with a 40-question run. Use this to benchmark your readiness.</li>
                <li><strong>Topic drill</strong> &mdash; hammer a weak area (e.g. <a href="../../topic-temperature.html">temperature</a>) until it's automatic.</li>
                <li><strong>Flashcards</strong> &mdash; quick, repeated recall on the go. Great for allergens and key numbers. Open <a href="../../flashcards.html">flashcards</a>.</li>
                <li><strong>Daily challenge</strong> &mdash; one question a day keeps the knowledge warm between study sessions.</li>
            </ul>
            <p>For a structured plan, follow our <a href="../../tips.html">exam tips</a>.</p>
            <h2>What our free practice test offers</h2>
            <p>Our tool gives you <strong>650 exam-style questions across 12 topics</strong>, with <strong>instant feedback and explanations</strong> for every answer, and <strong>no sign-up</strong>. You can take it unlimited times, drill individual topics, switch to a timed exam mode, and track your best score &mdash; all free. Studying for a specific state? Start from your <a href="../../food-safety-nsw.html">state page</a>.</p>
            <h2>A simple 5-day study plan</h2>
            <p>You don't need weeks. This plan gets most people exam-ready in under an hour a day:</p>
            <ul>
                <li><strong>Day 1 &mdash; Benchmark.</strong> Take a full 40-question test. Note your score and which topics you missed.</li>
                <li><strong>Day 2 &mdash; Temperature.</strong> Drill the <a href="../../topic-temperature.html">danger zone</a> and the 2-hour/4-hour rule until it's automatic.</li>
                <li><strong>Day 3 &mdash; Allergens &amp; hygiene.</strong> Drill <a href="../../topic-allergens.html">allergens</a> and personal hygiene; use flashcards on the go.</li>
                <li><strong>Day 4 &mdash; HACCP &amp; cross-contamination.</strong> Focus on CCPs and clean-vs-sanitise.</li>
                <li><strong>Day 5 &mdash; Mock exam.</strong> Do a timed full test. If you score 80%+, book your assessment.</li>
            </ul>
            <h2>Turn mistakes into marks</h2>
            <p>The real value isn't the score &mdash; it's the <strong>review</strong>. Every question you get wrong is a free lesson if you read the explanation and understand <em>why</em>. Re-test the same weak topic a day later (spaced repetition) and it sticks. That loop &mdash; attempt, review, re-test &mdash; is what moves people from 65% to a confident 85%.</p>
            <h2>The honest bit</h2>
            <p>Practice tests prepare you brilliantly, but they are <strong>educational only</strong> &mdash; they do not issue a certificate. Your official, nationally recognised certificate must come from a Registered Training Organisation. Think of practice as the training, and the RTO assessment as the official result. Follow our <a href="../how-to-pass-food-safety-test/">step-by-step pass guide</a> or read <a href="../is-food-safety-test-hard-australia/">is the test hard?</a> before you book. <a href="../../">Start your free practice test</a> now.</p>''',
 [("How many practice tests should I take?","Take full practice tests until you consistently score 80% or higher &mdash; usually two to four runs &mdash; while drilling weak topics in between. Consistency matters more than a single good score."),
  ("What score means I'm ready?","Reliably scoring 80%+ on full practice tests is a strong signal you're ready, since most RTOs require around 80% to pass. Aim to hit it more than once."),
  ("Is free practice enough to pass?","Free practice is excellent preparation and covers the knowledge you need, but the official certificate must come from an accredited RTO. Use practice to get exam-ready, then certify with an RTO."),
  ("What's the difference between this site and the RTO exam?","This site is a free practice and revision tool. The RTO assessment is the official, accredited test that leads to a nationally recognised certificate. We help you prepare; the RTO certifies you.")],
)

# ── EMIT ─────────────────────────────────────────────────────────────────────
def render(p):
    return f'''<!DOCTYPE html>
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
    <title>{p["title"]} | Food Safety AU</title>
    <meta name="description" content="{p["desc"]}">
    <meta name="robots" content="index, follow">
    <meta name="author" content="Food Safety Practice AU">
    <link rel="canonical" href="https://food-safety-practice-test-au.com/blog/{p["slug"]}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://food-safety-practice-test-au.com/blog/{p["slug"]}">
    <meta property="og:title" content="{p["title"]}">
    <meta property="og:description" content="{p["desc"]}">
    <meta property="og:image" content="{DOMAIN}/og-default.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:image" content="{DOMAIN}/og-default.png">
    <link rel="icon" type="image/x-icon" href="../../favicon.ico">
    <link rel="stylesheet" href="../../style.css?v={CSS_VER}">
{schema_block(p["title"], p["desc"], p["slug"], p["faqs"])}
</head>
<body>
{header()}

    <main class="container">
        <article class="blog-article">
            <p class="blog-breadcrumb"><a href="../../">Home</a> &rsaquo; <a href="../">Blog</a></p>
            <h1>{p["h1"]}</h1>
            <p class="blog-lead">{p["lead"]}</p>
            <div class="ad-slot" data-ad-slot="blog-top" role="complementary" aria-label="Advertisement"><span class="ad-slot__label">Advertisement</span></div>
{p["body"]}
{faq_block(p["faqs"])}
{CTA}
        </article>
    </main>
{FOOTER}
</body>
</html>
'''

def build_index():
    cards = [(p["slug"], p["title"], p["desc"]) for p in POSTS]
    items = "".join(
        f'<a href="{href}" class="blog-card"><h2>{t}</h2><p>{d}</p></a>' for href, t, d in cards)
    collection_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Food Safety Blog",
        "url": "https://food-safety-practice-test-au.com/blog",
        "inLanguage": "en-AU",
        "mainEntity": {
            "@type": "ItemList",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1,
                 "url": f"https://food-safety-practice-test-au.com/blog/{href}",
                 "name": t}
                for i, (href, t, d) in enumerate(cards)
            ],
        },
    }, indent=2, ensure_ascii=True)
    nav = "\n".join(
        f'                <a href="/{href.lstrip("/")}" class="nav-link{" nav-link--active" if t == "Blog" else ""}">{t}</a>'
        for href, t in [("", "Practice Test"), ("guide.html", "Study Guide"),
                        ("temperature-danger-zone-checker.html", "Danger Zone Tool"),
                        ("tips.html", "Exam Tips"), ("find-a-course.html", "Find a Course"),
                        ("blog/", "Blog"), ("flashcards.html", "Flashcards"), ("glossary.html", "Glossary")])
    states = "\n".join(
        f'                <a href="/food-safety-{c}.html" class="state-link" title="Food Safety Practice Test {a}">{a}</a>'
        for c, a in STATES)
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
    <title>Food Safety Blog 2026 | Tips &amp; Study Guides</title>
    <meta name="description" content="Food safety study tips, FSS vs food handler guides, and Australian certification advice.">
    <meta name="robots" content="index, follow">
    <meta name="author" content="Food Safety Practice AU">
    <link rel="canonical" href="https://food-safety-practice-test-au.com/blog">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://food-safety-practice-test-au.com/blog">
    <meta property="og:title" content="Food Safety Blog 2026 | Tips &amp; Study Guides">
    <meta property="og:description" content="Food safety study tips, FSS vs food handler guides, and Australian certification advice.">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="stylesheet" href="/style.css?v={CSS_VER}">
    <meta property="og:image" content="https://food-safety-practice-test-au.com/og-default.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:image" content="https://food-safety-practice-test-au.com/og-default.png">
    <script type="application/ld+json">
{collection_schema}
    </script>
</head>
<body>
    <header class="site-header">
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
    </header>

    <main class="container">
        <header class="blog-index-header"><h1>Food Safety Blog</h1></header>
        <div class="blog-list">{items}</div>
        <div class="content-cta" style="margin-top:24px;">
            <h3>Ready to test yourself?</h3>
            <p>Try 650 free exam-style questions with instant feedback. No sign-up required.</p>
            <a href="/" class="btn btn-primary">Start the free practice test</a>
        </div>
    </main>
    <footer class="footer">
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
            <p class="footer-disclaimer">Not affiliated with FSANZ, state health departments, or the Australian Government.</p>
        </div>
    </footer>

    <div id="cookie-banner" class="cookie-banner" role="dialog" aria-live="polite" aria-label="Cookie notice">
        <div class="cookie-banner__content">
            <p>This site uses cookies and similar technologies to improve your experience and support analytics and advertising. By continuing to use this site, you agree to our <a href="/legal.html#privacy">Privacy Policy</a>.</p>
            <div class="cookie-banner__actions">
                <button id="cookie-accept" class="btn btn-primary cookie-btn">Accept</button>
            </div>
        </div>
    </div>
    <script src="/faq-accordion.js" defer></script>
    <script src="/cookie-consent.js" defer></script>
    <script src="/site-ui.js" defer></script>
</body>
</html>
'''
    (BLOG / "index.html").write_text(html, encoding="utf-8")

if __name__ == "__main__":
    for p in POSTS:
        d = BLOG / p["slug"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(render(p), encoding="utf-8")
        words = len(__import__("re").sub("<[^>]+>"," ", p["body"]).split())
        print(f"wrote blog/{p['slug']}/ | ~{words} body words | {len(p['faqs'])} FAQs")
    build_index()
    print(f"rebuilt blog/index.html with {len(POSTS)} cards")
    print("DONE", len(POSTS), "posts")
