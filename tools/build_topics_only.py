#!/usr/bin/env python3
"""Build the 12 topic-*.html pages ONLY (deep content + FAQ schema).
SAFE: never touches index.html, guide.html or other manual pages.
Run: python3 tools/build_topics_only.py
"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
DOMAIN = "https://food-safety-practice-test-au.com"

NAV = [("/","Practice Test"),("/guide.html","Study Guide"),("/temperature-danger-zone-checker.html","Danger Zone Tool"),
       ("/tips.html","Exam Tips"),("/find-a-course.html","Find a Course"),("/blog/","Blog"),
       ("/flashcards.html","Flashcards"),("/glossary.html","Glossary")]
STATES = [("nsw","NSW"),("vic","VIC"),("qld","QLD"),("wa","WA"),("sa","SA"),("act","ACT"),("nt","NT"),("tas","TAS")]

# slug -> label (for the topic grid + ordering)
LABELS = [
 ("food-standards","Food Standards Code & Legislation"),
 ("food-handler","Food Handler Responsibilities"),
 ("temperature","Temperature & Danger Zone"),
 ("cross-contamination","Cross Contamination"),
 ("hygiene","Personal Hygiene"),
 ("cleaning","Cleaning & Sanitising"),
 ("allergens","Allergen Management"),
 ("storage","Food Storage & Labelling"),
 ("pest-control","Pest Control"),
 ("haccp","HACCP Basics"),
 ("fss-duties","Food Safety Supervisor Duties"),
 ("high-risk","High-Risk Foods & Vulnerable Groups"),
]

def header():
    nav="\n".join(f'                <a href="{h}" class="nav-link">{t}</a>' for h,t in NAV)
    states="\n".join(f'                <a href="/food-safety-{c}.html" class="state-link" title="Food Safety Practice Test {a}">{a}</a>' for c,a in STATES)
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

FOOTER='''    <footer class="footer">
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
            <p class="footer-disclaimer">Free practice and educational content only. Your certificate must be issued by a Registered Training Organisation (RTO).</p>
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
    <script src="/site-ui.js" defer></script>'''

# Per-topic deep content. Each: meta, intro[], sections[(h2,html)], traps[], faqs[(q,a)], blog(optional)
TOPICS = {}
def T(slug, meta, intro, sections, traps, faqs, blog=None):
    TOPICS[slug]=dict(meta=meta,intro=intro,sections=sections,traps=traps,faqs=faqs,blog=blog)

T("food-standards",
  "Food Standards Code & legislation practice questions for your Australian food safety test: FSANZ, Standard 3.2.2 and 3.2.2A explained.",
  ["Food law underpins every other topic on your assessment. In Australia, food safety is governed by the <strong>Australia New Zealand Food Standards Code</strong>, developed by <strong>FSANZ</strong> and enforced by state authorities and local councils.",
   "You don't need to memorise legal sections, but you should understand who sets the rules, who enforces them, and what businesses must do."],
  [("What the Code requires","<p><strong>Standard 3.2.2</strong> sets core food safety practices (receipt, storage, processing, display, transport, disposal) and food-handler health and hygiene. <strong>Standard 3.2.2A</strong> (from December 2023) added Food Safety Management Tools — requiring many businesses to appoint a certified Food Safety Supervisor and ensure handlers are trained.</p>"),
   ("Who enforces it","<p>FSANZ writes the standards; <strong>state/territory authorities and local council Environmental Health Officers</strong> inspect premises, issue improvement notices and can prosecute. The business proprietor holds ultimate legal responsibility for selling safe, suitable food.</p>")],
  ["'Use-by' is a safety date (illegal to sell after); 'best-before' is quality (can still sell if safe).",
   "There is no small-business exemption — the Code applies regardless of size.",
   "FSANZ does not inspect cafes; councils do."],
  [("Who develops Australia's food standards?","Food Standards Australia New Zealand (FSANZ) develops the Code; states and local councils enforce it."),
   ("What did Standard 3.2.2A change?","From December 2023 it required many businesses to appoint a certified Food Safety Supervisor and ensure food handlers are trained, including settings serving vulnerable people."),
   ("Is the Food Standards Code law?","Yes — it is adopted into law by each state and territory and is legally binding on food businesses.")],
  None)

T("food-handler",
  "Food handler responsibilities practice questions (SITXFSA005): hygiene, illness reporting, gloves and safe handling for your Australian food safety test.",
  ["A <strong>food handler</strong> is anyone who works with food or food-contact surfaces — kitchen hands, wait staff, baristas and managers. The national unit is <strong>SITXFSA005</strong>.",
   "Your duty is simple to state and vital to follow: do not contaminate food, and report anything that could make food unsafe."],
  [("Core responsibilities","<p>Wash hands at the right moments, keep yourself and your clothing clean, cover cuts with a brightly coloured waterproof dressing, and <strong>report illness</strong> — anyone with vomiting or diarrhoea must not handle food and should stay away until 48 hours symptom-free.</p>"),
   ("Gloves and utensils","<p>Gloves are not a substitute for hand washing; wash hands before gloving and change gloves between tasks. Avoid bare-hand contact with ready-to-eat food — use tongs, utensils or clean single-use gloves.</p>")],
  ["Gloves worn all shift spread bacteria like bare hands — change them between tasks.",
   "Feeling better is not enough after gastro — the rule is 48 hours symptom-free.",
   "A used tasting spoon must never go back into the food."],
  [("What unit covers food handler training?","SITXFSA005 — Use hygienic practices for food safety — is the national unit for food handlers."),
   ("When must a food handler wash their hands?","Before handling food, after the toilet, after handling raw food, after breaks, and after touching the face, hair or rubbish."),
   ("Can a food handler work while sick?","No. Anyone with vomiting or diarrhoea must not handle food and should be symptom-free for 48 hours before returning.")],
  ("/food-handler-practice-test.html","Food Handler Practice Test"))

T("temperature",
  "Temperature & danger zone practice questions for your Australian food safety test: 5°C–60°C, cooking temps, cooling and the 2-hour/4-hour rule.",
  ["Temperature control is the most-tested topic on the exam and the biggest cause of foodborne illness. The <strong>danger zone is 5&deg;C to 60&deg;C</strong>, where bacteria multiply fastest.",
   "Keep potentially hazardous food below 5&deg;C or above 60&deg;C, and minimise time in between."],
  [("The key numbers","<p>Cold storage <strong>&le;5&deg;C</strong>; hot holding <strong>&ge;60&deg;C</strong>; cook poultry and minced meat to <strong>75&deg;C</strong>; reheat to at least <strong>70&deg;C</strong>; freezer about <strong>&minus;18&deg;C</strong>. Use a clean, calibrated probe thermometer in the thickest part. Try the <a href=\"/temperature-danger-zone-checker.html\">danger-zone checker</a>.</p>"),
   ("The 2-hour/4-hour rule","<p>Total time in the danger zone: under 2 hours — refrigerate or use; 2–4 hours — use immediately; over 4 hours — throw it out. Cool hot food 60&deg;C&rarr;21&deg;C within 2 hours, then 21&deg;C&rarr;5&deg;C within 4 more.</p>")],
  ["Food out for 3 hours = use immediately, NOT refrigerate for tomorrow.",
   "Minced meat must be cooked through to 75°C even for a 'rare' burger.",
   "A bain-marie at 52°C is in the danger zone — reheat to 75°C and fix it."],
  [("What is the temperature danger zone?","5°C to 60°C — bacteria multiply fastest here, so keep food below 5°C or above 60°C."),
   ("What temperature should poultry be cooked to?","75°C in the centre, checked with a clean probe thermometer."),
   ("What is the 2-hour/4-hour rule?","Under 2 hours in the danger zone: refrigerate or use. 2–4 hours: use now. Over 4 hours: discard.")],
  ("/blog/temperature-danger-zone-australia-guide/","Temperature Danger Zone: Complete Guide"))

T("cross-contamination",
  "Cross contamination practice questions for your Australian food safety test: raw vs ready-to-eat, colour-coded boards, gloves and allergens.",
  ["<strong>Cross contamination</strong> is the transfer of harmful bacteria or allergens from one food, surface, person or piece of equipment to another. It is why raw chicken and salad must never share an unwashed board.",
   "Separation plus cleaning and sanitising between tasks is the core defence."],
  [("Direct vs indirect","<p><strong>Direct:</strong> raw food touches ready-to-eat food (e.g. raw meat dripping onto a salad). <strong>Indirect:</strong> bacteria travel via hands, knives, boards or cloths. Store ready-to-eat food above raw, with raw poultry and mince at the bottom.</p>"),
   ("Bacterial vs allergen","<p>Bacterial cross-contamination spreads pathogens (often killed by cooking); <strong>allergen cross-contact</strong> spreads allergen proteins, which cooking does <em>not</em> destroy. Use clean or dedicated equipment for allergic customers.</p>")],
  ["Gloves are not enough — reused gloves spread bacteria; change them.",
   "Wiping a board with a cloth is not cleaning — wash and sanitise it.",
   "Shared fryer oil carries the wheat allergen to 'plain' chips."],
  [("What is cross-contamination?","The transfer of harmful bacteria or allergens from one food, surface, person or piece of equipment to another."),
   ("Can I use the same board for raw chicken and salad?","Only after washing and sanitising it (or using a separate clean board). Wiping is not enough."),
   ("What is cross-contact?","The allergen version of cross-contamination — allergen traces transferring via shared equipment, hands or oil. Cooking does not remove allergens.")],
  ("/blog/cross-contamination-food-safety-exam-tips/","Cross Contamination: Exam Tips"))

T("hygiene",
  "Personal hygiene practice questions for your Australian food safety test: hand washing, illness, cuts, jewellery and clean uniforms.",
  ["Personal hygiene stops handlers contaminating food with bacteria from their bodies and clothing. The single most effective action is <strong>thorough, frequent hand washing</strong>.",
   "Wash for at least 20 seconds with soap and warm water, then dry with a clean single-use towel."],
  [("Hands and health","<p>Wash hands before handling food, after the toilet, after raw food, after breaks and after touching your face or hair. Cover cuts with a brightly coloured waterproof dressing and a glove. Report illness and stay off food handling until 48 hours symptom-free.</p>"),
   ("Clothing and grooming","<p>Wear clean clothing, tie back or cover hair, keep nails short and unpolished, and limit jewellery to a plain band. No eating, smoking or vaping in food areas.</p>")],
  ["Hand sanitiser does not replace washing after the toilet.",
   "A reused damp towel re-contaminates clean hands.",
   "Only a plain band ring is generally acceptable — no stones or watches."],
  [("How long should you wash your hands?","At least 20 seconds with soap and warm running water, then dry with a clean single-use towel."),
   ("What should a food handler do with a cut?","Cover it with a brightly coloured waterproof dressing and wear a glove over the top."),
   ("Is hand sanitiser enough after the toilet?","No — hands must be washed with soap and water; sanitiser is only an extra step.")],
  None)

T("cleaning",
  "Cleaning & sanitising practice questions for your Australian food safety test: clean vs sanitise, contact time, chemical safety and schedules.",
  ["Cleaning and sanitising are two different steps. <strong>Cleaning</strong> removes visible dirt and grease; <strong>sanitising</strong> reduces bacteria to a safe level. You must clean first, then sanitise.",
   "Food-contact surfaces need both, on a documented schedule."],
  [("The correct method","<p>Pre-clean, wash with hot water and detergent, rinse, apply sanitiser for its <strong>contact time</strong>, then air dry. Sanitiser does not work on a dirty surface, and wiping it off too soon makes it ineffective.</p>"),
   ("Chemical safety","<p>Store chemicals below and away from food, clearly labelled — never in unlabelled drink bottles. Follow the manufacturer's dilution; stronger is not better and can leave harmful residue.</p>")],
  ["A surface that looks clean can still carry bacteria — sanitising is still required.",
   "Detergent cleans but does not sanitise.",
   "Sanitiser needs contact time — don't wipe it straight off."],
  [("What is the difference between cleaning and sanitising?","Cleaning removes dirt and grease; sanitising reduces bacteria to a safe level. Clean first, then sanitise."),
   ("Why clean before sanitising?","Dirt and grease stop sanitiser working, so the surface must be cleaned first."),
   ("How should cleaning chemicals be stored?","Below and away from food, clearly labelled in suitable containers — never in unlabelled drink bottles.")],
  None)

T("allergens",
  "Allergen management practice questions for your Australian food safety test: the 10 priority allergens, cross-contact and labelling.",
  ["Allergen questions trip up many students. Australia recognises <strong>10 priority allergens</strong>: peanuts, tree nuts, milk, eggs, sesame, soy, wheat/gluten, fish, crustacea and lupin.",
   "For an allergic customer even a trace can be life-threatening, so cross-contact control and accurate information are essential."],
  [("Preventing cross-contact","<p>Use clean or dedicated equipment, fresh ingredients and a clean surface; change gloves and wash hands. Cooking does <strong>not</strong> destroy allergens, and shared fryer oil carries them between foods.</p>"),
   ("Information and labelling","<p>Packaged food must declare priority allergens in plain English. In food service you must give accurate allergen information on request — if you can't confirm a dish is safe, say so. Revise with the <a href=\"/blog/10-priority-allergens-australia-food-safety-exam/\">allergen cheat sheet</a>.</p>")],
  ["Allergy (immune, can be fatal) is not the same as intolerance (uncomfortable).",
   "Lupin is the allergen most people forget — it's one of the 10.",
   "Cooking does not remove allergens; 'may contain traces' is a real risk."],
  [("How many priority allergens are there in Australia?","Ten: peanuts, tree nuts, milk, eggs, sesame, soy, wheat/gluten, fish, crustacea and lupin."),
   ("Does cooking remove allergens?","No. Allergenic proteins survive cooking, so cross-contact must be prevented."),
   ("What is anaphylaxis?","A severe, rapid allergic reaction that can be life-threatening and needs immediate adrenaline and an ambulance.")],
  ("/blog/10-priority-allergens-australia-food-safety-exam/","10 Priority Allergens: Exam Cheat Sheet"))

T("storage",
  "Food storage & labelling practice questions for your Australian food safety test: FIFO, fridge order, use-by vs best-before and date marking.",
  ["Correct storage keeps food safe and prevents waste. The key ideas are <strong>temperature control, separation, and stock rotation (FIFO)</strong>.",
   "Label prepared food with a name and date so it is used within safe limits."],
  [("Fridge order and FIFO","<p>Store ready-to-eat food above raw, with raw poultry and mince at the bottom so juices can't drip down. Use <strong>First In, First Out</strong> — older stock to the front. Keep fridges &le;5&deg;C and don't overload them.</p>"),
   ("Dates and packaging","<p><strong>Use-by</strong> is a safety date (don't sell or eat after it); <strong>best-before</strong> is quality. Transfer opened cans to covered food-grade containers, label and refrigerate. Discard swollen or damaged cans.</p>")],
  ["Use-by = safety (must discard); best-before = quality (may still be fine).",
   "Raw meat goes BELOW ready-to-eat food, never above.",
   "A swollen can can mean dangerous spoilage — never use it."],
  [("What does FIFO mean?","First In, First Out — use older stock before newer stock to reduce waste and avoid expired food."),
   ("What is the difference between use-by and best-before?","Use-by is a safety date (don't sell after it); best-before is about quality."),
   ("Where should raw meat be stored in the fridge?","Below ready-to-eat food, with raw poultry and mince at the bottom.")],
  None)

T("pest-control",
  "Pest control practice questions for your Australian food safety test: signs of pests, proofing, waste management and safe treatment.",
  ["Pests carry disease and contaminate food and surfaces, so controlling them is a food safety priority. Effective control layers <strong>prevention, monitoring and professional treatment</strong>.",
   "Every staff member should recognise and report the signs of pests."],
  [("Keeping pests out","<p>Seal gaps, screen windows, use self-closing doors, store food in sealed containers off the floor, and manage waste with covered, regularly emptied bins. Remove cardboard promptly — it harbours cockroaches.</p>"),
   ("Detecting and treating","<p>Signs include droppings, gnaw marks and a musty smell. Report them immediately and protect food. Pesticide treatment should be done by a licensed professional — never spray household pesticide over food.</p>")],
  ["A single daytime cockroach often signals a hidden infestation — act on it.",
   "Never spray pesticide over or near food — use a licensed controller.",
   "Cardboard boxes are prime cockroach harbourage — break them down and remove."],
  [("What are common signs of pests?","Droppings, gnaw marks, grease marks along walls, and a musty smell."),
   ("Who should carry out pesticide treatment?","A licensed pest control professional, to avoid contaminating food with chemicals."),
   ("How do you keep pests out of a kitchen?","Seal entry points, screen openings, store food sealed and off the floor, and manage waste well.")],
  None)

T("haccp",
  "HACCP basics practice questions for your Australian food safety test: hazards, Critical Control Points, monitoring and corrective action.",
  ["<strong>HACCP</strong> (Hazard Analysis and Critical Control Points) is a preventive system: identify hazards and control them at the points that matter, rather than testing the finished food.",
   "Food handlers don't write the plan, but they follow the controls and do the monitoring."],
  [("Hazards and CCPs","<p>The three hazard types are <strong>biological, chemical and physical</strong>. A <strong>Critical Control Point</strong> is a step where control is essential — cooking (75&deg;C), cooling (two-stage) and reheating (70&deg;C+). Each CCP has a measurable critical limit.</p>"),
   ("Monitor, correct, record","<p>Monitor each CCP (e.g. probe the temperature), take predetermined <strong>corrective action</strong> if a limit is missed (reheat or discard), and keep records to prove control and spot trends.</p>")],
  ["A CCP has a measurable critical limit (e.g. 75°C) — vague targets fail.",
   "Some toxins survive reheating — prevention beats relying on a kill step.",
   "Food handlers follow and monitor controls; the FSS/business owns the plan."],
  [("What does HACCP stand for?","Hazard Analysis and Critical Control Points — a preventive approach to food safety."),
   ("What is a Critical Control Point?","A step where control is essential to keep food safe and there's no later step to fix a problem, e.g. cooking or cooling."),
   ("What are the three hazard types?","Biological (bacteria, viruses), chemical (cleaning agents, allergens, toxins) and physical (glass, metal, hair).")],
  ("/blog/haccp-basics-food-handlers-australia/","HACCP Basics for the Exam"))

T("fss-duties",
  "Food Safety Supervisor duties practice questions for your Australian food safety test: SITXFSA006, supervision, records and 3.2.2A.",
  ["A <strong>Food Safety Supervisor (FSS)</strong> oversees food safety on site. The role adds <strong>SITXFSA006</strong> to the food-handler unit and is legally nominated under Standard 3.2.2A.",
   "The FSS guides staff, monitors controls and acts when something is unsafe."],
  [("What the FSS does","<p>Supervises safe practices, ensures handlers are trained, monitors temperatures and records, leads corrective action, and is reasonably available during food operations. The certificate is valid for 5 years.</p>"),
   ("Responsibility and the law","<p>Appointing an FSS does <strong>not</strong> remove the proprietor's overall legal responsibility. In NSW, FSS training must be done through an NSW Food Authority-approved RTO. Compare the roles in <a href=\"/blog/food-safety-supervisor-vs-food-handler/\">FSS vs food handler</a>, or take the <a href=\"/food-safety-supervisor-practice-test.html\">FSS practice test</a>.</p>")],
  ["An FSS certificate expires after 5 years — it must be renewed.",
   "The owner keeps ultimate legal responsibility, not just the FSS.",
   "NSW requires an approved RTO for FSS training."],
  [("What units does a Food Safety Supervisor need?","SITXFSA005 and SITXFSA006 — the food handler unit plus supervising safe food handling."),
   ("How long is an FSS certificate valid?","Generally 5 years, after which refresher training is required."),
   ("Does an FSS remove the owner's responsibility?","No — the proprietor retains overall legal responsibility for selling safe food.")],
  ("/blog/food-safety-supervisor-vs-food-handler/","Food Safety Supervisor vs Food Handler"))

T("high-risk",
  "High-risk foods & vulnerable groups practice questions for your Australian food safety test: PHF, Listeria, and protecting at-risk diners.",
  ["<strong>Potentially hazardous (high-risk) foods</strong> need temperature control to stay safe — meat, poultry, dairy, eggs, seafood, cooked rice and prepared salads.",
   "Vulnerable groups — young children, the elderly, pregnant women and the immunocompromised — suffer more severe illness, so extra care applies."],
  [("Why these foods are risky","<p>They support rapid bacterial growth. <strong>Listeria</strong> is a special concern because it grows even at fridge temperatures and is dangerous in pregnancy and aged care. Cooked rice can grow toxin-forming <strong>Bacillus cereus</strong> if left warm.</p>"),
   ("Protecting vulnerable diners","<p>Settings like <a href=\"/food-safety-aged-care.html\">aged care</a> and <a href=\"/food-safety-childcare.html\">childcare</a> often avoid raw egg, soft cheeses, deli meats and undercooked foods, and apply stricter temperature and time control.</p>")],
  ["Listeria grows at fridge temperatures — soft cheese and deli meats are risky for vulnerable people.",
   "Honey is unsafe for infants under 12 months (botulism risk).",
   "Reheating may not destroy pre-formed toxins — control temperature from the start."],
  [("What are potentially hazardous foods?","Foods that need temperature control to stay safe — meat, dairy, eggs, seafood, cooked rice and prepared salads."),
   ("Why is Listeria a concern for vulnerable groups?","It can grow at fridge temperatures and causes severe illness in the elderly, pregnant women and the immunocompromised."),
   ("Is honey safe for babies?","No — honey should not be given to infants under 12 months due to the risk of infant botulism.")],
  None)

def topic_grid(exclude=None):
    cards=[]
    for i,(slug,label) in enumerate(LABELS,1):
        if slug==exclude: continue
        cards.append(f'<a href="/topic-{slug}.html" class="topic-link-card"><span class="topic-link-card__nr" aria-hidden="true">{i}</span> {label}</a>')
    return "\n                    ".join(cards)

LABEL_MAP=dict(LABELS)

TIPS = {
 "food-standards":"Focus on who does what — FSANZ writes the Code, state authorities and councils enforce it — and the use-by versus best-before distinction.",
 "food-handler":"Drill the hand-washing moments and the 48-hour illness exclusion rule, which appear in almost every assessment.",
 "temperature":"Lock in the numbers (5, 60, 75, 70 and −18°C) and the 2-hour/4-hour decisions before anything else — this topic carries the most marks.",
 "cross-contamination":"Practise the raw-to-ready-to-eat scenarios and remember gloves are not a substitute for hand washing.",
 "hygiene":"Memorise the 20-second hand wash, the cut-covering rule and the illness exclusion — these are guaranteed marks.",
 "cleaning":"Nail the clean-then-sanitise order and the idea of sanitiser contact time, which catch many people out.",
 "allergens":"Memorise the 10 priority allergens (don't forget lupin) and the difference between an allergy and an intolerance.",
 "storage":"Get FIFO, the top-to-bottom fridge order and use-by versus best-before solid — they recur constantly.",
 "pest-control":"Learn the signs of pests and the rule that licensed professionals carry out pesticide treatment.",
 "haccp":"Understand Critical Control Points and critical limits using real examples like cooking to 75°C.",
 "fss-duties":"Know the 5-year renewal, the two units (005 + 006), and that the owner keeps ultimate legal responsibility.",
 "high-risk":"Connect high-risk foods to vulnerable groups and remember Listeria grows even at fridge temperatures.",
}

def build(slug):
    d=TOPICS[slug]; label=LABEL_MAP[slug]
    faq_list = d["faqs"] + [(f"How can I revise {label.lower()} quickly?",
        f"Use topic-drill mode for {label.lower()} and read the explanation on every question you miss, then re-test. Flashcards and a full 40-question practice test help the knowledge stick before your assessment.")]
    extra_section = (f'<section class="guide-section"><h2>How to revise {label.lower()} for the exam</h2>'
        f'<p>{TIPS[slug]} The questions are usually scenario-based, so practise applying the rule rather than just reciting it. '
        f'Work through the {label} drill below until you can answer without hesitating, review anything you get wrong, then sit a full timed test to confirm you are exam-ready.</p></section>')
    intro="\n            ".join(f"<p>{x}</p>" for x in d["intro"])
    secs="\n            ".join(f'<section class="guide-section"><h2>{h}</h2>{b}</section>' for h,b in d["sections"])
    secs = secs + "\n            " + extra_section
    traps="".join(f"<li>{t}</li>" for t in d["traps"])
    faqs="\n                ".join(f'<dt class="faq-question" tabindex="0" aria-expanded="false"><span>{q}</span><span class="faq-toggle">+</span></dt>\n                <dd class="faq-answer" hidden>{a}</dd>' for q,a in faq_list)
    blog_html=""
    if d["blog"]:
        blog_html=f'<p class="see-also">See also: <a href="{d["blog"][0]}">{d["blog"][1]}</a>.</p>\n            '
    faq_schema={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq_list]}
    lr_schema={"@context":"https://schema.org","@type":"LearningResource","name":f"{label} — Food Safety Practice","learningResourceType":"Practice questions","educationalLevel":"SITXFSA005 / SITXFSA006","inLanguage":"en-AU","isAccessibleForFree":True,"url":f"{DOMAIN}/topic-{slug}.html"}
    html=f'''<!DOCTYPE html>
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
    <title>{label} Practice Questions {{}}</title>
    <meta name="description" content="{d['meta']}">
    <meta name="robots" content="index, follow">
    <meta name="author" content="Food Safety Practice AU">
    <link rel="canonical" href="{DOMAIN}/topic-{slug}.html">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{DOMAIN}/topic-{slug}.html">
    <meta property="og:title" content="{label} Practice Questions">
    <meta property="og:description" content="{d['meta']}">
    <meta property="og:image" content="{DOMAIN}/og-default.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:image" content="{DOMAIN}/og-default.png">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="stylesheet" href="/style.css?v=7">
    <script type="application/ld+json">
{json.dumps(faq_schema, indent=2, ensure_ascii=True)}
    </script>
    <script type="application/ld+json">
{json.dumps(lr_schema, indent=2, ensure_ascii=True)}
    </script>
</head>
<body>
{header()}

    <main class="container">
        <article class="content-page">
            <h1>{label}</h1>
            {intro}
            <div class="ad-slot" data-ad-slot="topic-incontent" role="complementary" aria-label="Advertisement"><span class="ad-slot__label">Advertisement</span></div>
            {secs}
            <section class="guide-section">
                <h2>Common exam traps</h2>
                <ul>{traps}</ul>
            </section>
            <section class="guide-section">
                <h2>{label} FAQ</h2>
                <dl>
                {faqs}
                </dl>
            </section>
            {blog_html}<div class="content-cta">
                <h3>Ready to test yourself?</h3>
                <p>Drill {label.lower()} questions, or take a full 40-question practice test. Instant feedback, no sign-up.</p>
                <a href="/?mode=topic&amp;topic={slug}" class="btn btn-primary">Start {label} drill</a>
                <a href="/" class="btn btn-secondary">Full practice test</a>
            </div>
            <section class="guide-section">
                <h2>Study all 12 topics</h2>
                <div class="topic-link-grid">
                    {topic_grid(exclude=slug)}
                </div>
            </section>
        </article>
    </main>
{FOOTER}
</body>
</html>
'''
    # inject the year into the title placeholder (kept literal-safe)
    html = html.replace(f"<title>{label} Practice Questions {{}}</title>", f"<title>{label} Practice Questions 2026</title>")
    (ROOT / f"topic-{slug}.html").write_text(html, encoding="utf-8")
    return slug

if __name__ == "__main__":
    built=[build(s) for s in TOPICS]
    print("built topics:", built)
    print("TOTAL:", len(built), "(expected 12 once all defined)")
