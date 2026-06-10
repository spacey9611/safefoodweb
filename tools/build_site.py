#!/usr/bin/env python3
"""Generate Food Safety Practice Test AU static site from White Card template."""

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WHITECARD = ROOT.parent / "whitecard"
DOMAIN = "https://food-safety-practice-test-au.com"
SITE_NAME = "Food Safety Practice AU"
BRAND_TITLE = "Food Safety Practice Test"
TAGLINE = "Free SITXFSA005 practice · 650 questions"
QUESTION_COUNT = 650
YEAR = "2026"

HOME_SCHEMA = """
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Organization",
      "name": "Food Safety Practice AU",
      "url": "https://food-safety-practice-test-au.com",
      "description": "Free Australian food safety practice tests and study resources for SITXFSA005 and SITXFSA006 certification preparation"
    }
    </script>
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "WebSite",
      "name": "Food Safety Practice Test Australia",
      "url": "https://food-safety-practice-test-au.com"
    }
    </script>
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Quiz",
      "name": "Food Safety Practice Test (SITXFSA005)",
      "about": { "@type": "Thing", "name": "Australian Food Safety Handler Training" },
      "isAccessibleForFree": true,
      "inLanguage": "en-AU"
    }
    </script>
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "What is food safety training in Australia?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Food safety training covers hygienic food handling under SITXFSA005 (food handlers) and SITXFSA006 (Food Safety Supervisors). It aligns with the Australia New Zealand Food Standards Code and state food Acts."
          }
        },
        {
          "@type": "Question",
          "name": "Food Safety Practice Test Format and Topics",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Each practice test randomly selects 40 questions from our bank of 650 exam-style questions. Topics include temperature control, cross contamination, allergens, cleaning, HACCP, and FSS duties."
          }
        },
        {
          "@type": "Question",
          "name": "Is food safety certification valid in every Australian state?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Yes. Nationally recognised units SITXFSA005 and SITXFSA006 are accepted across all states and territories. Each state has its own regulator (e.g. NSW Food Authority, Department of Health Victoria)."
          }
        },
        {
          "@type": "Question",
          "name": "Is this the official food safety test?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "This practice test is for educational purposes only. We are not affiliated with FSANZ or any government agency. For official certification, complete training through an accredited RTO."
          }
        }
      ]
    }
    </script>"""

GUIDE_SCHEMA = """
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "WebPage",
      "name": "Food Safety Study Guide 2026",
      "description": "Complete food safety study guide for Australian food handlers and Food Safety Supervisors. Temperature, hygiene, allergens, HACCP and more.",
      "url": "https://food-safety-practice-test-au.com/guide.html",
      "inLanguage": "en-AU",
      "isPartOf": { "@type": "WebSite", "name": "Food Safety Practice Test Australia", "url": "https://food-safety-practice-test-au.com" }
    }
    </script>
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "What is the temperature danger zone in Australia?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "The temperature danger zone is 5°C to 60°C. Potentially hazardous food should spend as little time as possible in this range because bacteria multiply rapidly. Hot food must be held at 60°C or above; cold storage is 5°C or below."
          }
        },
        {
          "@type": "Question",
          "name": "What is the difference between SITXFSA005 and SITXFSA006?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "SITXFSA005 covers food handler skills — personal hygiene, temperature control, and contamination prevention. SITXFSA006 is for Food Safety Supervisors who oversee the food safety program on site."
          }
        },
        {
          "@type": "Question",
          "name": "How often must a Food Safety Supervisor certificate be renewed?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Food Safety Supervisor (FSS) certificates must typically be renewed every 5 years in Australia. Requirements may vary slightly by state regulator."
          }
        }
      ]
    }
    </script>"""

STATES = {
    "nsw": {
        "name": "New South Wales",
        "abbr": "NSW",
        "regulator": "NSW Food Authority",
        "reg_url": "https://www.foodauthority.nsw.gov.au/",
        "fss": "Most hospitality businesses (Class 1 and 2) must appoint at least one Food Safety Supervisor (FSS) with a nationally recognised certificate.",
        "handler": "All food handlers must have skills and knowledge in food safety. NSW accepts online food handler training from approved providers.",
        "extra_faq": [
            ("Is Food Safety Supervisor training mandatory in NSW?", "Yes. Class 1 and 2 food businesses must have at least one FSS on the premises during all hours of operation."),
            ("How much does food safety training cost in NSW?", "Food handler courses typically cost $25–$60 online. FSS courses range from $85–$230 depending on the RTO."),
            ("How often must I renew my FSS certificate in NSW?", "Every 5 years. You must complete refresher training before your certificate expires."),
        ],
    },
    "vic": {
        "name": "Victoria",
        "abbr": "VIC",
        "regulator": "Department of Health Victoria",
        "reg_url": "https://www.health.vic.gov.au/food-safety",
        "fss": "Class 1 and 2 premises require a Food Safety Supervisor. Victoria also offers the free DoFoodSafely online learning program for food handlers.",
        "handler": "Food handlers should complete food safety training. The free DoFoodSafely program at dofoodsafely.health.vic.gov.au is widely used in Victoria.",
        "extra_faq": [
            ("What is DoFoodSafely in Victoria?", "A free online food safety learning program run by the Victorian Department of Health. It is not a formal certificate but helps food handlers meet training requirements."),
            ("Can I do FSS training online in Victoria?", "Yes. Many RTOs offer fully online FSS courses recognised in Victoria and nationally."),
            ("Who regulates food safety in Victoria?", "The Department of Health Victoria oversees food safety, with local councils conducting inspections."),
        ],
    },
    "qld": {
        "name": "Queensland",
        "abbr": "QLD",
        "regulator": "Queensland Health / Safe Food Production Queensland",
        "reg_url": "https://www.health.qld.gov.au/public-health/food-poisoning",
        "fss": "Licensed food businesses must have an Food Safety Supervisor with a current certificate on site during operation.",
        "handler": "All food handlers must have appropriate food safety skills and knowledge under the Food Act 2006 (Qld).",
        "extra_faq": [
            ("Is an FSS required for all Queensland food businesses?", "Licensed food businesses (most cafes, restaurants, and takeaways) must have at least one FSS on premises during operation."),
            ("How do I get a food handler certificate in QLD?", "Complete a recognised food safety course through an RTO or approved online provider. SITXFSA005 is the standard unit."),
            ("Does Queensland accept certificates from other states?", "Yes. Nationally recognised units SITXFSA005 and SITXFSA006 are accepted across Australia."),
        ],
    },
    "wa": {
        "name": "Western Australia",
        "abbr": "WA",
        "regulator": "WA Department of Health",
        "reg_url": "https://www.health.wa.gov.au/Articles/A_E/Food-safety",
        "fss": "Food businesses must have adequate food safety practices. Many venues appoint a Food Safety Supervisor as best practice and for compliance.",
        "handler": "Food handlers must demonstrate food safety knowledge. Training through recognised courses is strongly recommended.",
        "extra_faq": [
            ("Who inspects food businesses in WA?", "Local government environmental health officers inspect food premises on behalf of the WA Department of Health."),
            ("Is food safety training mandatory in WA?", "While not always legally mandated for every worker, food businesses must ensure staff have adequate food safety knowledge."),
            ("What unit code covers food handler training?", "SITXFSA005 — Use hygienic practices for food safety — is the national standard unit for food handlers."),
        ],
    },
    "sa": {
        "name": "South Australia",
        "abbr": "SA",
        "regulator": "SA Health",
        "reg_url": "https://www.sahealth.sa.gov.au/wps/wcm/connect/public+content/sa+health+internet/health+topics/food+safety",
        "fss": "Food businesses must comply with the Food Act 2001 (SA). Appointing a trained Food Safety Supervisor is required for most licensed premises.",
        "handler": "All staff handling food must have appropriate food safety skills and knowledge.",
        "extra_faq": [
            ("How often is an FSS certificate renewed in SA?", "Every 5 years, consistent with national requirements for Food Safety Supervisor qualifications."),
            ("Who enforces food safety in South Australia?", "SA Health sets standards; local councils inspect and enforce at the premises level."),
            ("Can I use online training for my SA food business?", "Yes. Nationally recognised online courses from approved RTOs are accepted in South Australia."),
        ],
    },
    "act": {
        "name": "Australian Capital Territory",
        "abbr": "ACT",
        "regulator": "ACT Health",
        "reg_url": "https://www.health.act.gov.au/food-safety",
        "fss": "Food businesses in the ACT must comply with the Food Act 2001. A Food Safety Supervisor is required for most licensed food businesses.",
        "handler": "Food handlers must have skills and knowledge appropriate to their work. Training courses are available online and in person.",
        "extra_faq": [
            ("Does the Dec 2023 Standard 3.2.2A apply in the ACT?", "Yes. The national food safety standard applies in the ACT, extending requirements to schools, childcare, and aged care settings."),
            ("Who inspects ACT food premises?", "ACT Health and Access Canberra conduct food safety inspections and enforcement."),
            ("Is food safety training recognised nationally from the ACT?", "Yes. Certificates for SITXFSA005/006 obtained in the ACT are valid across all Australian states."),
        ],
    },
    "nt": {
        "name": "Northern Territory",
        "abbr": "NT",
        "regulator": "NT Health",
        "reg_url": "https://health.nt.gov.au/professionals/environmental-health/food-safety",
        "fss": "Licensed food businesses in the NT should have a Food Safety Supervisor with current nationally recognised training.",
        "handler": "All food handlers must maintain hygienic practices and food safety knowledge appropriate to their role.",
        "extra_faq": [
            ("Who regulates food safety in the NT?", "NT Health Environmental Health branch, with local council involvement in inspections."),
            ("Are online food safety courses accepted in the NT?", "Yes, when delivered by a registered training organisation offering nationally recognised units."),
            ("What is the danger zone temperature?", "5°C to 60°C — food must not remain in this range for more than 4 hours (or 2 hours for high-risk foods)."),
        ],
    },
    "tas": {
        "name": "Tasmania",
        "abbr": "TAS",
        "regulator": "Department of Health Tasmania",
        "reg_url": "https://www.health.tas.gov.au/health-topics/food-safety",
        "fss": "Food businesses in Tasmania must comply with the Food Act 2003. Most licensed premises require a Food Safety Supervisor.",
        "handler": "Food handlers need appropriate skills and knowledge. SITXFSA005 training is the standard pathway.",
        "extra_faq": [
            ("How do I renew my FSS certificate in Tasmania?", "Complete refresher training through an RTO before your 5-year certificate expires."),
            ("Who inspects Tasmanian food businesses?", "Local council environmental health officers inspect food premises across Tasmania."),
            ("Does Tasmania follow the Australia New Zealand Food Standards Code?", "Yes. Tasmania adopts the national Food Standards Code alongside state food legislation."),
        ],
    },
}

TOPICS = [
    ("food-standards", "Food Standards Code & Legislation", "Australia New Zealand Food Standards Code",
     "The Food Standards Code sets national rules for food safety, labelling, and handling across Australia and New Zealand."),
    ("food-handler", "Food Handler Responsibilities", "SITXFSA005 hygienic practices",
     "Food handlers must follow hygienic practices, report illness, and handle food safely to prevent contamination and foodborne illness."),
    ("temperature", "Temperature & Danger Zone", "5°C to 60°C danger zone",
     "Keeping food out of the temperature danger zone (5°C–60°C) is critical. Hot food must stay above 60°C; cold food below 5°C."),
    ("cross-contamination", "Cross Contamination", "Preventing pathogen transfer",
     "Cross contamination occurs when bacteria spread from raw to ready-to-eat food, surfaces, or equipment. Separate, colour-code, and sanitise."),
    ("hygiene", "Personal Hygiene", "Hand washing and clean uniforms",
     "Personal hygiene — hand washing, clean clothing, covering cuts, and staying home when ill — is the first line of food safety defence."),
    ("cleaning", "Cleaning & Sanitising", "Two-step clean then sanitise",
     "Cleaning removes visible dirt; sanitising reduces bacteria to safe levels. Both steps are required on food contact surfaces."),
    ("allergens", "Allergen Management", "Top 10 allergens in Australia",
     "Australia's top allergens include peanuts, tree nuts, milk, eggs, wheat, soy, sesame, fish, crustacea, and lupin. Declare and separate them."),
    ("storage", "Food Storage & Labelling", "FIFO and date marking",
     "Store food correctly: raw below cooked, label with use-by dates, follow FIFO (First In, First Out), and keep fridges at 5°C or below."),
    ("pest-control", "Pest Control", "Keeping pests out of kitchens",
     "Pests carry disease. Seal entry points, store food off the floor, manage waste, and report sightings to your supervisor immediately."),
    ("haccp", "HACCP Basics", "Hazard Analysis Critical Control Points",
     "HACCP identifies hazards and sets critical control points (CCPs) like cooking temperature and cold storage to keep food safe."),
    ("fss-duties", "Food Safety Supervisor Duties", "SITXFSA006 supervisor role",
     "The FSS oversees food safety programs, trains staff, monitors CCPs, and ensures the business complies with the Food Standards Code."),
    ("high-risk", "High-Risk Foods & Vulnerable Groups", "Eggs, poultry, rice, and vulnerable diners",
     "High-risk foods include poultry, eggs, cooked rice, and dairy. Vulnerable groups — children, elderly, pregnant women — need extra care."),
]

# Question banks per topic (~34 each = 408)
QUESTION_BANK = {
    "food-standards": [
        ("What is the Australia New Zealand Food Standards Code?", ["A set of national food safety and labelling standards", "A state-only NSW regulation", "A restaurant menu guide", "An import tax document"], 0, "The Food Standards Code is adopted by all states and territories."),
        ("Which body develops food standards for Australia?", ["Food Standards Australia New Zealand (FSANZ)", "SafeWork Australia", "The ACCC", "Local councils only"], 0, "FSANZ develops standards; states enforce them."),
        ("What does Standard 3.2.2 cover?", ["Food safety practices and general requirements", "Organic farming rules", "Import tariffs", "Menu pricing"], 0, "Standard 3.2.2 sets core food safety requirements for businesses."),
        ("What did Standard 3.2.2A (Dec 2023) expand?", ["Food handler training to schools, childcare, aged care and charities", "Only restaurant licensing", "Export rules only", "Alcohol service"], 0, "The 2023 expansion broadened food handler requirements."),
        ("Who is responsible for enforcing the Food Standards Code locally?", ["Local councils and state health departments", "The Federal Police", "Food Standards Australia New Zealand directly", "Customers"], 0, "Enforcement is at state/local level."),
        ("What is a 'food business' under the Code?", ["Any business handling food for sale", "Only restaurants", "Only supermarkets", "Only food manufacturers"], 0, "Broad definition includes cafes, caterers, schools, etc."),
        ("Must food businesses comply with the Food Standards Code?", ["Yes, it is legally binding when adopted by states", "No, it is optional advice", "Only if they have more than 10 staff", "Only in NSW"], 0, "States adopt the Code through their food Acts."),
        ("What is the purpose of a food safety program?", ["To identify and control food safety hazards systematically", "To market the restaurant", "To calculate wages", "To design menus"], 0, "Food safety programs manage hazards proactively."),
        ("Which document must many food businesses maintain?", ["Records of food safety activities and training", "Staff social media policies", "Customer loyalty cards only", "Vehicle logbooks"], 0, "Records demonstrate compliance during inspections."),
        ("Can a food business operate without knowing the Code?", ["No — ignorance is not a defence under food law", "Yes, if the business is small", "Yes, for the first year only", "Only takeaway shops are exempt"], 0, "Businesses must ensure staff have adequate knowledge."),
    ],
    "food-handler": [
        ("What unit covers food handler training nationally?", ["SITXFSA005 — Use hygienic practices for food safety", "CPCCWHS1001", "HLTAID011", "BSBWOR301"], 0, "SITXFSA005 is the standard food handler unit."),
        ("When must a food handler wash hands?", ["Before handling food, after toilet, after touching raw food, after breaks", "Once per shift only", "Only when visibly dirty", "Never if wearing gloves"], 0, "Hand washing is required at multiple critical points."),
        ("Can a food handler work while vomiting?", ["No — they must report illness and not handle food", "Yes, if they wear gloves", "Yes, for short shifts only", "Only if they feel better after an hour"], 0, "Infectious illness can contaminate food."),
        ("What must food handlers do with cuts on hands?", ["Cover with a waterproof dressing and wear a glove", "Ignore small cuts", "Use a bandaid only when handling cash", "Stop work permanently"], 0, "Open wounds can introduce pathogens."),
        ("Who is considered a food handler?", ["Anyone who touches food or food contact surfaces", "Only the head chef", "Only staff with certificates", "Only full-time employees"], 0, "Includes kitchen hands, wait staff, and managers."),
        ("What should a food handler do if they see a food safety hazard?", ["Report it to the supervisor immediately", "Fix it alone without telling anyone", "Ignore it if busy", "Post about it online"], 0, "Reporting hazards prevents incidents."),
        ("Are food handlers responsible for their own hygiene?", ["Yes — personal hygiene is every handler's duty", "No — only the FSS is responsible", "No — only the owner", "Only on weekends"], 0, "Personal responsibility is a core principle."),
        ("What jewellery is generally not allowed when handling food?", ["Rings, watches, and dangling earrings on hands/arms", "A plain wedding band is often acceptable per policy", "Hair ties", "Name badges"], 0, "Jewellery can harbour bacteria and fall into food."),
        ("When should gloves be changed?", ["When torn, after raw food, after breaks, or between tasks", "Once per day", "Never — one pair all shift", "Only when they look dirty"], 0, "Gloves are not a substitute for hand washing."),
        ("What is the food handler's role in allergen management?", ["Follow procedures, avoid cross contact, and communicate with customers", "Ignore allergen requests", "Only the manager handles allergens", "Remove all allergen labels"], 0, "Every handler plays a part in allergen safety."),
    ],
    "temperature": [
        ("What is the temperature danger zone?", ["5°C to 60°C", "0°C to 100°C", "10°C to 50°C", "20°C to 80°C"], 0, "Bacteria multiply rapidly between 5°C and 60°C."),
        ("How long can potentially hazardous food stay in the danger zone?", ["No more than 4 hours total (2 hours for high-risk in many settings)", "8 hours", "Unlimited if covered", "24 hours"], 0, "Time in the danger zone must be minimised."),
        ("What is the minimum hot holding temperature?", ["60°C or above", "45°C", "50°C", "40°C"], 0, "Hot food must be kept at 60°C or hotter."),
        ("What is the maximum cold storage temperature for fridges?", ["5°C or below", "10°C", "8°C", "0°C exactly"], 0, "Cold food must be stored at 5°C or below."),
        ("What temperature should frozen food be stored at?", ["-15°C or colder", "0°C", "-5°C", "5°C"], 0, "Freezers should be -15°C or below."),
        ("Why must food be cooled quickly?", ["To pass through the danger zone fast and limit bacterial growth", "To save energy", "To improve taste only", "It does not matter"], 0, "Slow cooling keeps food in the danger zone too long."),
        ("What is the two-stage cooling guideline?", ["60°C to 21°C within 2 hours, then to 5°C within 4 more hours", "Cool overnight at room temperature", "Put hot food straight in the freezer", "Leave on bench until cold"], 0, "Rapid staged cooling reduces risk."),
        ("How should you check food temperatures?", ["Use a calibrated probe thermometer in the thickest part", "Touch with your hand", "Guess by steam", "Read the oven dial only"], 0, "Thermometers give accurate readings."),
        ("What should you do if hot food falls below 60°C?", ["Reheat to 75°C or discard within time limits", "Serve it anyway", "Add ice", "Mix with cold food"], 0, "Below 60°C, bacteria can grow."),
        ("Why is reheating important?", ["Must reach 75°C in the centre to kill pathogens", "Only for taste", "To reduce salt", "Reheating is never needed"], 0, "75°C centre temperature is the standard reheat target."),
    ],
    "cross-contamination": [
        ("What is cross contamination?", ["Transfer of harmful bacteria from one food/surface to another", "Mixing two sauces together", "Cooking two items at once", "Using the same oven"], 0, "Cross contamination spreads pathogens."),
        ("How do you prevent raw and cooked food contact?", ["Use separate boards, utensils, and storage areas", "Stack raw on top of cooked", "Rinse quickly between uses only", "Use the same knife if washed weekly"], 0, "Separation is essential."),
        ("What colour board is often used for raw meat?", ["Red (in colour-coded systems)", "Green", "Blue", "White only"], 0, "Colour coding helps prevent cross contamination."),
        ("What should you do after cutting raw chicken?", ["Wash and sanitise the board and knife before next use", "Wipe with a dry cloth", "Use for salad immediately", "Soak in water overnight only"], 0, "Sanitising kills remaining bacteria."),
        ("Can cloths spread contamination?", ["Yes — use separate cloths for raw and ready-to-eat areas", "No, cloths are always safe", "Only paper towels spread bacteria", "Cloths do not matter"], 0, "Damp cloths can harbour bacteria."),
        ("Why store raw food below cooked food in the fridge?", ["Raw juices dripping onto cooked food cause contamination", "Raw food is heavier", "Cooked food tastes better on top", "It saves space only"], 0, "Drip contamination is a common hazard."),
        ("What is indirect cross contamination?", ["Bacteria spread via hands, cloths, equipment, or surfaces", "Only direct food-to-food contact", "Contamination from customers only", "Only from pests"], 0, "Hands and surfaces are common vectors."),
        ("Should you wash raw chicken before cooking?", ["No — washing spreads bacteria around the kitchen", "Yes, always wash thoroughly", "Only wash in the sink with other items", "Wash with soap"], 0, "FSANZ and health authorities advise not to wash raw poultry."),
        ("How does cross contamination relate to allergens?", ["Allergen proteins can transfer via shared equipment", "Allergens cannot cross contaminate", "Only peanuts cross contaminate", "Cooking removes all allergen risk"], 0, "Even trace amounts can trigger reactions."),
        ("What is the best way to handle egg contamination risk?", ["Treat raw eggs as potentially hazardous; separate from ready-to-eat food", "Crack eggs on salad bowls", "Store eggs above ready-to-eat food", "Ignore cracked eggs"], 0, "Raw eggs may contain Salmonella."),
    ],
    "hygiene": [
        ("How long should hand washing take?", ["At least 20 seconds with soap and warm water", "5 seconds", "1 minute with cold water only", "Only use sanitiser, no water"], 0, "20 seconds minimum with proper technique."),
        ("When must hair be restrained in food prep?", ["Always — use hats, nets, or ties", "Only for long hair", "Never in cafes", "Only when health inspector visits"], 0, "Hair can fall into food."),
        ("What clothing is appropriate for food handling?", ["Clean uniform or apron, closed shoes", "Open sandals and street clothes", "Any clothing if gloves worn", "Swimwear in summer"], 0, "Clean dedicated clothing reduces contamination."),
        ("Should food handlers eat in prep areas?", ["No — eat and drink only in designated break areas", "Yes, if careful", "Only managers may eat in kitchen", "Yes, if food is covered"], 0, "Eating in prep areas introduces contamination."),
        ("What illnesses must be reported to your supervisor?", ["Vomiting, diarrhoea, fever, sore throat with fever, jaundice", "Only hospitalisation", "No illnesses need reporting", "Only COVID-19"], 0, "These symptoms may indicate infectious disease."),
        ("How should sneezing near food be handled?", ["Turn away, sneeze into elbow, wash hands before returning to food", "Sneeze into hands and continue", "Ignore it", "Wear perfume to mask it"], 0, "Respiratory droplets can contaminate food."),
        ("Are fingernails important for food hygiene?", ["Yes — short, clean, unpolished nails reduce pathogen harbouring", "No, nails do not matter", "Only chefs need short nails", "Long nails are fine with gloves"], 0, "Long or polished nails can hide bacteria."),
        ("What is double hand washing?", ["Wash, apply soap, wash again — used after toilet or raw food in some protocols", "Wash twice with water only", "Two people wash one pair of hands", "Not a real practice"], 0, "Some businesses require enhanced hand washing."),
        ("Why is smoking prohibited in food prep areas?", ["Smoke and ash contaminate food and surfaces", "Only for fire risk", "It is a preference", "Only illegal at night"], 0, "Smoking introduces contaminants."),
        ("What should you do before starting a food handling shift?", ["Wash hands, check uniform, report illness, review tasks", "Start immediately without preparation", "Only check social media", "Eat a meal at the bench"], 0, "Pre-shift hygiene sets the standard."),
    ],
    "cleaning": [
        ("What is the difference between cleaning and sanitising?", ["Cleaning removes dirt; sanitising reduces microbes to safe levels", "They are the same thing", "Sanitising removes dirt", "Cleaning kills all bacteria"], 0, "Both steps are required."),
        ("What must be cleaned and sanitised?", ["Food contact surfaces, equipment, and utensils", "Only floors", "Only once per month", "Only the dining room"], 0, "Anything touching food needs both steps."),
        ("What temperature should a commercial dishwasher reach?", ["At least 80°C for final rinse (or equivalent sanitising method)", "40°C", "60°C for rinse", "Room temperature"], 0, "Hot rinse sanitises in commercial dishwashers."),
        ("How often should food contact surfaces be sanitised?", ["Regularly — between tasks and at least daily", "Once per year", "Only when visibly dirty", "Never if gloves used"], 0, "Frequency depends on use but is ongoing."),
        ("What is a food-grade sanitiser?", ["A chemical approved for use on food contact surfaces at correct concentration", "Any household bleach undiluted", "Perfume spray", "Dish soap only"], 0, "Must be used at manufacturer-specified dilution."),
        ("Why clean before sanitising?", ["Sanitisers work poorly on surfaces with organic matter", "It saves sanitiser", "Order does not matter", "Cleaning replaces sanitising"], 0, "Dirt blocks sanitiser action."),
        ("What should you use to dry sanitised equipment?", ["Air dry or single-use paper — not dirty tea towels", "Reused wet cloths", "Leave wet in sink", "Shake only"], 0, "Cloths can recontaminate."),
        ("How do you clean a food spill on the floor?", ["Clean spill, then sanitise if near food areas; mark wet floor if needed", "Leave until end of shift", "Mop with same water all day without changing", "Cover with cardboard"], 0, "Spills are slip and contamination hazards."),
        ("What records might a business keep for cleaning?", ["Cleaning schedules and completed checklists", "Only customer complaints", "No records needed", "Staff birthdays"], 0, "Records prove systematic cleaning."),
        ("Can you use the same sanitiser for hands and surfaces?", ["No — use hand wash for hands, surface sanitiser for equipment", "Yes, always interchangeable", "Only sanitiser for both", "Bleach on hands is fine"], 0, "Different products for different purposes."),
    ],
    "allergens": [
        ("How many major food allergens must be declared in Australia?", ["10 — including peanuts, tree nuts, milk, eggs, wheat, soy, sesame, fish, crustacea, lupin", "5", "3", "15"], 0, "Australia has 10 declared allergens."),
        ("What is cross contact in allergen management?", ["Unintentional transfer of allergen proteins to allergen-free food", "Customer mixing foods on plate", "Cooking allergens longer", "Labelling errors only at factory"], 0, "Cross contact is a kitchen risk."),
        ("How should allergen ingredients be stored?", ["Clearly labelled and separated from other foods", "Mixed with similar items", "Unlabelled to save time", "Above all other stock"], 0, "Separation and labelling prevent mistakes."),
        ("What must staff do when a customer declares an allergy?", ["Follow business allergen procedure, check ingredients, communicate with kitchen", "Guess that small amounts are OK", "Serve anyway", "Recommend they eat elsewhere without checking"], 0, "Allergic reactions can be life-threatening."),
        ("Can cooking always destroy allergens?", ["No — most allergens are proteins that survive cooking", "Yes, all allergens destroyed above 100°C", "Only peanuts survive cooking", "Frying removes all allergens"], 0, "Heat does not reliably destroy allergenic proteins."),
        ("What is an allergen statement on a menu?", ["Information about which dishes contain declared allergens", "Marketing text only", "Optional in all states", "Only for export food"], 0, "Menus should help customers identify allergens."),
        ("Why use separate utensils for allergen-free meals?", ["To prevent cross contact from shared equipment", "For presentation only", "It is not necessary", "Only in hospitals"], 0, "Shared tools can carry allergen traces."),
        ("What is anaphylaxis?", ["A severe, potentially life-threatening allergic reaction", "A mild rash only", "Food intolerance without immune response", "A type of food poisoning"], 0, "Anaphylaxis requires immediate emergency action."),
        ("Should you remove an allergen from a plated dish if requested?", ["No — prepare fresh; removal may leave traces", "Yes, pick nuts off the top", "Scrape sauce off", "Rinse under tap"], 0, "Traces remain; fresh preparation is required."),
        ("What training helps with allergen management?", ["Food safety training covering allergen awareness and business procedures", "No training needed", "Only online reviews", "Only FSS needs allergen knowledge"], 0, "All handlers should understand allergen basics."),
    ],
    "storage": [
        ("What does FIFO mean?", ["First In, First Out — use oldest stock first", "Fast In, Fast Out", "First In, Forgot Out", "Food In, Freezer Out"], 0, "FIFO reduces waste and spoilage."),
        ("Where should raw meat be stored in a fridge?", ["On the lowest shelf in a sealed container", "On the top shelf", "Next to ready-to-eat salads", "At room temperature"], 0, "Lowest shelf prevents drip contamination."),
        ("What is a use-by date?", ["The date after which food may be unsafe to eat", "A quality suggestion only", "When the shop bought the food", "The cooking date"], 0, "Use-by dates are safety dates for perishable food."),
        ("How should dry goods be stored?", ["Off the floor, away from walls, in sealed containers", "On the floor in original boxes", "Next to cleaning chemicals unlabelled", "In direct sunlight"], 0, "Proper storage prevents pests and contamination."),
        ("What temperature should a display fridge maintain?", ["5°C or below for cold display", "10°C", "15°C", "0°C exactly always"], 0, "Display fridges must keep food cold."),
        ("Why label stored food containers?", ["Identify contents and use-by dates", "Decoration only", "Labels are optional", "Only for frozen food"], 0, "Labelling prevents mistakes and waste."),
        ("How should hot food be stored if not served immediately?", ["Hot hold above 60°C or cool rapidly for refrigeration", "Leave at room temperature", "Put straight in fridge while hot without covering", "Leave uncovered on bench"], 0, "Avoid extended time in the danger zone."),
        ("What should you do with swollen canned food?", ["Do not use — discard; may indicate botulism risk", "Open and smell", "Serve if smell OK", "Freeze it"], 0, "Swollen cans can mean dangerous contamination."),
        ("How should eggs be stored?", ["In refrigeration, in original carton if possible", "At room temperature always", "Near raw chicken uncovered", "In warm cupboard"], 0, "Refrigeration extends safety of eggs."),
        ("What is the best practice for thawing frozen food?", ["In fridge, microwave (if cooking immediately), or under cold running water", "On bench all day", "In hot water bath overnight", "Near oven"], 0, "Safe thawing keeps food out of danger zone."),
    ],
    "pest-control": [
        ("Why are pests a food safety hazard?", ["They carry disease and contaminate food and surfaces", "They only damage packaging", "They improve ventilation", "Only flies matter"], 0, "Rodents and insects spread pathogens."),
        ("What is a sign of rodent activity?", ["Droppings, gnaw marks, and grease trails", "Clean floors only", "Extra food stock", "Bright lights"], 0, "Early signs should trigger pest control."),
        ("How should doors help pest control?", ["Fit door seals and keep doors closed; use screens where needed", "Leave open for air", "Remove all seals", "Block exits"], 0, "Physical barriers exclude pests."),
        ("Where should waste be stored?", ["In lidded bins, emptied regularly, away from food prep", "Next to prep bench open", "On floor in kitchen", "Only outside never emptied"], 0, "Waste attracts pests."),
        ("What should you do if you see a cockroach in the kitchen?", ["Report it and follow pest management plan", "Ignore single insects", "Spray chemicals near open food", "Continue without telling anyone"], 0, "One pest often indicates more."),
        ("How does proper storage reduce pests?", ["Food off floor and sealed removes food sources", "Pests ignore sealed food", "Only matters for dry goods", "Open storage is fine"], 0, "Eliminating access and food deters pests."),
        ("Who is responsible for pest control in a food business?", ["The business owner/PCBU with contracted pest technicians as needed", "Only council", "Only customers", "Nobody"], 0, "Business must maintain pest-free premises."),
        ("Should pesticides be used near open food?", ["No — follow licensed pest controller guidance away from food", "Yes, any spray is fine", "Only organic pesticides on open food", "Daily spraying is standard"], 0, "Chemical contamination is a risk."),
        ("What role do fly screens play?", ["Prevent flying insects entering food areas", "Decoration only", "Block ventilation required", "Not used in commercial kitchens"], 0, "Screens are a standard exclusion measure."),
        ("How often should pest control be reviewed?", ["Regularly as part of food safety program and after any sightings", "Never after initial setup", "Only when closing business", "Every 10 years"], 0, "Ongoing monitoring is essential."),
    ],
    "haccp": [
        ("What does HACCP stand for?", ["Hazard Analysis and Critical Control Points", "Health And Cleaning Control Program", "Hot And Cold Cooking Process", "Handling All Customer Complaints Properly"], 0, "HACCP is the international food safety system."),
        ("What is a critical control point (CCP)?", ["A step where control is essential to prevent or eliminate a hazard", "Any kitchen task", "Only the delivery step", "Customer service point"], 0, "CCPs are monitored closely."),
        ("Give an example of a CCP in cooking.", ["Ensuring poultry reaches 75°C at centre", "Washing uniforms", "Ordering stock", "Setting tables"], 0, "Cooking temperature kills pathogens in poultry."),
        ("What is hazard analysis?", ["Identifying biological, chemical, and physical hazards in the process", "Counting customers", "Menu design", "Staff scheduling only"], 0, "First step in HACCP."),
        ("Why monitor CCPs?", ["To verify controls are working and food is safe", "For marketing", "Only for large factories", "Monitoring is optional"], 0, "Monitoring catches failures before food is served."),
        ("What should happen if a CCP limit is exceeded?", ["Corrective action — discard, re-cook, or fix process per plan", "Serve food anyway", "Hide the record", "Wait until next week"], 0, "Corrective actions protect customers."),
        ("Who developed HACCP originally?", ["NASA and Pillsbury for safe space food", "Australian cafes", "Fast food chains only", "Local councils"], 0, "HACCP has aerospace origins."),
        ("Is HACCP required for all food businesses?", ["Many businesses use HACCP-based food safety programs; requirements vary by business type", "Never required", "Only overseas", "Only for supermarkets"], 0, "Most licensed food businesses use HACCP principles."),
        ("What records does HACCP typically require?", ["Temperature logs, cleaning records, corrective actions", "Only profit records", "No records", "Customer emails only"], 0, "Documentation proves the system works."),
        ("What are the seven HACCP principles?", ["Hazard analysis, CCPs, limits, monitoring, corrective action, verification, documentation", "Three steps only", "Cook, serve, clean", "Buy, store, sell"], 0, "Seven principles form the HACCP framework."),
    ],
    "fss-duties": [
        ("What unit covers Food Safety Supervisor training?", ["SITXFSA006 — Participate in safe food handling practices", "SITXFSA005 only", "CPCCWHS1001", "RSA certification"], 0, "SITXFSA006 is the FSS unit."),
        ("How often must an FSS certificate be renewed?", ["Every 5 years", "Every year", "Never", "Every 10 years"], 0, "National standard is 5-year renewal."),
        ("What is the FSS required to do on site?", ["Supervise food handling, know food safety program, train and direct staff", "Only manage payroll", "Only order food", "Only serve customers"], 0, "FSS is the on-site food safety leader."),
        ("Must an FSS be on premises during all operating hours?", ["Required for many Class 1 and 2 businesses when operating", "Never required on site", "Only once per week", "Only during inspections"], 0, "Varies by state and business class."),
        ("Can one FSS cover multiple venues?", ["Generally one FSS per premises unless approved alternative arrangements", "One person for unlimited sites simultaneously", "FSS not needed per site", "Only franchises exempt"], 0, "Each premises typically needs coverage."),
        ("What should the FSS do during an inspection?", ["Cooperate, provide records, demonstrate compliance", "Refuse entry", "Hide records", "Only speak to owner"], 0, "Inspectors verify compliance with food law."),
        ("Who can become a Food Safety Supervisor?", ["Someone who completes SITXFSA006 from a registered training organisation", "Any staff member without training", "Only chefs with 10 years experience", "Only business owners"], 0, "Formal qualification is required."),
        ("What is the FSS role in training staff?", ["Ensure food handlers have skills and knowledge; deliver or organise training", "No training role", "Only train managers", "Training is optional"], 0, "FSS supports ongoing staff competency."),
        ("What happens if a business has no FSS when required?", ["Breaches food law; may face penalties or closure", "Nothing", "Small fine only once ever", "Automatic insurance claim"], 0, "Non-compliance has legal consequences."),
        ("Does the FSS replace the need for handler hygiene?", ["No — all handlers must still follow hygienic practices", "Yes, FSS does all food handling", "Only FSS touches food", "Handlers need no training if FSS present"], 0, "FSS supervises; everyone remains responsible."),
    ],
    "high-risk": [
        ("Which foods are considered potentially hazardous?", ["Foods that support bacterial growth — protein-rich, moist, neutral pH", "Only dry rice uncooked", "Canned food unopened", "Whole uncut vegetables only"], 0, "Potentially hazardous foods need temperature control."),
        ("Why is cooked rice a high-risk food?", ["Bacillus cereus spores can survive cooking and grow if rice is held warm", "It is dry", "It is always safe", "Only brown rice is risky"], 0, "Rice must be cooled and stored properly."),
        ("Why are vulnerable groups at higher risk?", ["Weaker immune systems — elderly, infants, pregnant women, ill people", "They eat more food", "They prefer raw food", "No difference in risk"], 0, "Extra care needed for vulnerable diners."),
        ("Which group was added to mandatory handler training in 2023?", ["Schools, childcare, aged care, and charities (Standard 3.2.2A)", "Only five-star hotels", "Only importers", "Only farmers markets"], 0, "Dec 2023 expansion broadened requirements."),
        ("Why is raw egg in mayonnaise risky?", ["Salmonella may be present in raw eggs", "Eggs are always safe raw", "Only if eggs are brown", "Free-range eliminates risk"], 0, "Use pasteurised egg for raw preparations."),
        ("What is listeria and why care in aged care catering?", ["Bacteria dangerous to elderly and pregnant — can grow in fridge on some foods", "Harmless mould", "Only in frozen food", "Only overseas problem"], 0, "Listeria risk drives strict cold chain rules."),
        ("How should high-risk food be transported?", ["In insulated containers maintaining safe temperatures", "In open trays in hot car", "At room temperature for hours", "Without covering"], 0, "Transport keeps food in safe temperature range."),
        ("Why is poultry considered high-risk?", ["Salmonella and Campylobacter common in raw poultry", "It is always low risk", "Only duck is risky", "Cooking does not help"], 0, "Must cook to 75°C centre temperature."),
        ("What is a foodborne illness outbreak?", ["Two or more people with same illness from same food/source", "One customer complaint", "Staff cold", "Spoiled milk smell only"], 0, "Outbreaks trigger investigation and reporting."),
        ("How should leftovers of high-risk food be handled?", ["Refrigerate within 2 hours, use within safe timeframe, reheat to 75°C", "Leave on bench overnight", "Keep at room temperature", "Never refrigerate"], 0, "Prompt cooling and limited storage time reduce risk."),
    ],
}


def load_unique_questions():
    """Load the authored, unique question bank (tools/questions_data.json) if present.
    This is the single source of truth and avoids the legacy (set N) padding."""
    data_file = ROOT / "tools" / "questions_data.json"
    if data_file.exists():
        return json.loads(data_file.read_text(encoding="utf-8"))
    return None


def expand_questions():
    """Legacy fallback: expand base questions to QUESTION_COUNT with variations.
    NOTE: prefer load_unique_questions(); this padding is retained only as a fallback."""
    out = []
    qid = 1
    per_topic = QUESTION_COUNT // len(TOPICS)
    for slug, _, _, _ in TOPICS:
        bank = QUESTION_BANK.get(slug, [])
        for i in range(per_topic):
            base = bank[i % len(bank)]
            q_text, opts, ans, expl = base
            if i >= len(bank):
                q_text = q_text.replace("?", f" (set {i // len(bank) + 1})?")
            out.append({
                "id": f"q{qid:03d}",
                "topic": slug,
                "question": q_text,
                "options": list(opts),
                "answer": ans,
                "explanation": expl + " (Ref: Food Standards Code / SITXFSA005–006.)",
            })
            qid += 1
    while len(out) < QUESTION_COUNT:
        src = out[len(out) % len(out)]
        out.append({**src, "id": f"q{len(out) + 1:03d}"})
    return out[:QUESTION_COUNT]


def header_html(active_nav=""):
    nav_items = [
        ("", "Practice Test"),
        ("guide.html", "Study Guide"),
        ("temperature-danger-zone-checker.html", "Danger Zone Tool"),
        ("tips.html", "Exam Tips"),
        ("find-a-course.html", "Find a Course"),
        ("blog/", "Blog"),
        ("flashcards.html", "Flashcards"),
        ("glossary.html", "Glossary"),
    ]
    nav = "\n".join(
        f'                <a href="/{href}" class="nav-link{" nav-link--active" if active_nav == label else ""}">{label}</a>'
        for href, label in nav_items
    )
    states = "\n".join(
        f'                <a href="/food-safety-{code}.html" class="state-link" title="Food Safety Practice Test {info["abbr"]}">{info["abbr"]}</a>'
        for code, info in STATES.items()
    )
    return f"""    <header class="site-header">
        <div class="container site-header__top">
            <a href="/" class="site-brand">
                <span class="site-brand__mark" aria-hidden="true">AU</span>
                <span class="site-brand__text">
                    <span class="site-brand__title">{BRAND_TITLE}</span>
                    <span class="site-brand__tagline">{TAGLINE}</span>
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
                <button type="button" class="font-resize-btn" id="font-decrease" aria-label="Decrease text size" title="Smaller text">A−</button>
                <button type="button" class="font-resize-btn" id="font-increase" aria-label="Increase text size" title="Larger text">A+</button>
            </div>
        </div>
    </header>"""


def footer_html():
    return f"""    <footer class="footer">
        <div class="container">
            <p>&copy; {YEAR} {SITE_NAME}</p>
            <nav class="footer-links">
                <a href="/about.html">About</a>
                <span class="separator">|</span>
                <a href="/terms.html">Terms of Use</a>
                <span class="separator">|</span>
                <a href="legal.html#privacy">Privacy Policy</a>
                <span class="separator">|</span>
                <a href="legal.html#legal">Legal Notice</a>
                <span class="separator">|</span>
                <a href="legal.html#contact">Contact Us</a>
            </nav>
            <p class="footer-disclaimer">We may earn a commission if you purchase through links on this site.</p>
            <p class="footer-disclaimer">Not affiliated with FSANZ, state health departments, or the Australian Government.</p>
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
    </div>"""


def head_consent():
    return """    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag("consent", "default", {
        "ad_storage": "denied",
        "ad_user_data": "denied",
        "ad_personalization": "denied",
        "analytics_storage": "denied",
        "wait_for_update": 500
      });
      dataLayer.push({ "event": "default_consent_set" });
    </script>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-N69BCEQGQ2"></script>
    <script>
      gtag('js', new Date());
      gtag('config', 'G-N69BCEQGQ2');
    </script>"""


def page_shell(title, description, canonical, body, extra_head="", active_nav="", scripts="""    <script src="faq-accordion.js" defer></script>
    <script src="site-ui.js" defer></script>"""):
    return f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
{head_consent()}
    <title>{title}</title>
    <meta name="description" content="{description}">
    <meta name="robots" content="index, follow">
    <meta name="author" content="{SITE_NAME}">
    <link rel="canonical" href="{canonical}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:image" content="{DOMAIN}/og-default.png">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="/style.css?v=7">
{extra_head}
</head>
<body>
{header_html(active_nav)}
{body}
{footer_html()}
{scripts}
</body>
</html>"""


def topic_grid_html(exclude_slug=None):
    items = []
    for i, (slug, label, _, _) in enumerate(TOPICS, 1):
        if slug == exclude_slug:
            continue
        items.append(
            f'                    <a href="topic-{slug}.html" class="topic-link-card"><span class="topic-link-card__nr" aria-hidden="true">{i}</span> {label}</a>'
        )
    return "\n".join(items)


def write_questions_js(questions):
    lines = [
        "// Food Safety Practice Test AU — Question Bank",
        f"// {len(questions)} questions aligned with SITXFSA005 / SITXFSA006 & Food Standards Code",
        "",
        "export const QUESTIONS = [",
    ]
    for q in questions:
        opts = json.dumps(q["options"], ensure_ascii=False)
        lines.append("    {")
        lines.append(f'        id: "{q["id"]}",')
        lines.append(f'        topic: "{q["topic"]}",')
        lines.append(f'        question: {json.dumps(q["question"], ensure_ascii=False)},')
        lines.append(f"        options: {opts},")
        lines.append(f'        answer: {q["answer"]},')
        lines.append(f'        explanation: {json.dumps(q["explanation"], ensure_ascii=False)},')
        lines.append("    },")
    lines.append("];")
    (ROOT / "questions.js").write_text("\n".join(lines) + "\n", encoding="utf-8")


def adapt_script_js():
    src = (WHITECARD / "script.js").read_text(encoding="utf-8")
    repl = [
        ("Australian White Card Practice Test", "Australian Food Safety Practice Test"),
        ("wc_progress_v1", "fs_progress_v1"),
        ("wc_gamify_v1", "fs_gamify_v1"),
        ("wc_dc_", "fs_dc_"),
        ("wc_font_size_v1", "fs_font_size_v1"),
        ("wc_bookmarks_v1", "fs_bookmarks_v1"),
        ("wc_cookie_accepted_v1", "fs_cookie_accepted_v1"),
        ("White Card", "Food Safety"),
        ("white-card-practice-test-au.com", "food-safety-practice-test-au.com"),
        ("white-card-", "food-safety-"),
        ("CPCCWHS1001", "SITXFSA005"),
        ("552", str(QUESTION_COUNT)),
        ("Site Trainee", "Kitchen Hand"),
        ("Apprentice", "Line Cook"),
        ("Tradesperson", "Chef"),
        ("Senior Tradie", "Head Chef"),
        ("Site Supervisor", "Food Safety Supervisor"),
        ("Safety Champion", "Food Safety Champion"),
        ("Book your accredited White Card course", "Book your accredited food safety course"),
        ("construction induction", "food safety certification"),
        ("SafeWork NSW", "NSW Food Authority"),
        ("WorkSafe Victoria", "Department of Health Victoria"),
        ("WorkSafe Queensland", "Queensland Health"),
        ("WorkSafe WA", "WA Department of Health"),
        ("SafeWork SA", "SA Health"),
        ("WorkSafe ACT", "ACT Health"),
        ("NT WorkSafe", "NT Health"),
        ("'nt': 'NT WorkSafe'", "'nt': 'NT Health'"),
        ("'tas': 'WorkSafe Tasmania'", "'tas': 'Department of Health Tasmania'"),
        ("Safe Work Australia", "Food Standards Australia New Zealand"),
    ]
    for old, new in repl:
        src = src.replace(old, new)
    # Replace TOPIC_LABELS block
    topic_labels = ",\n".join(
        f"    {{ slug: '{slug}', label: '{label}' }}" for slug, label, _, _ in TOPICS
    )
    src = re.sub(
        r"const TOPIC_LABELS = \[.*?\];",
        f"const TOPIC_LABELS = [\n{topic_labels}\n];",
        src,
        count=1,
        flags=re.DOTALL,
    )
    # Update pass messages for food safety (80% typical)
    src = src.replace(
        "The official Food Safety assessment requires 100%",
        "Most RTOs require around 80% to pass the official food safety assessment",
    )
    (ROOT / "script.js").write_text(src, encoding="utf-8")
    # Ensure all 8 states are present (whitecard template omits NT/TAS)
    patch = """const stateRegulators = {
    'nsw': 'NSW Food Authority',
    'vic': 'Department of Health Victoria',
    'qld': 'Queensland Health',
    'wa': 'WA Department of Health',
    'sa': 'SA Health',
    'act': 'ACT Health',
    'nt': 'NT Health',
    'tas': 'Department of Health Tasmania',
    'default': 'Food Standards Australia New Zealand'
};

// State Display Names
const stateNames = {
    'nsw': 'NSW',
    'vic': 'VIC',
    'qld': 'QLD',
    'wa': 'WA',
    'sa': 'SA',
    'act': 'ACT',
    'nt': 'NT',
    'tas': 'TAS',
    'default': 'Australia'
};"""
    src2 = (ROOT / "script.js").read_text(encoding="utf-8")
    src2 = re.sub(
        r"const stateRegulators = \{.*?\};\n\n// State Display Names\nconst stateNames = \{.*?\};",
        patch,
        src2,
        count=1,
        flags=re.DOTALL,
    )
    (ROOT / "script.js").write_text(src2, encoding="utf-8")


def adapt_style_css():
    css = (WHITECARD / "style.css").read_text(encoding="utf-8")
    css = css.replace("White Card Practice Test", "Food Safety Practice Test")
    css = css.replace("hi-vis construction, premium", "hospitality food safety, premium")
    css = css.replace("--hv:        #FFD400;", "--hv:        #00C853;")
    css = css.replace("--hv-deep:   #F2C200;", "--hv-deep:   #00A843;")
    css = css.replace("--hv-soft:   #FFF6CC;", "--hv-soft:   #E8F8EE;")
    (ROOT / "style.css").write_text(css, encoding="utf-8")


def write_index():
    topic_links = topic_grid_html()
    faq_items = """
                    <dt class="faq-question" tabindex="0" aria-expanded="false">
                        <span>What is food safety training in Australia?</span>
                        <span class="faq-toggle">+</span>
                    </dt>
                    <dd class="faq-answer" hidden>
                        Food safety training covers hygienic food handling under <strong>SITXFSA005</strong> (food handlers) and <strong>SITXFSA006</strong> (Food Safety Supervisors). It aligns with the Australia New Zealand Food Standards Code and state food Acts.
                    </dd>
                    <dt class="faq-question" tabindex="0" aria-expanded="false">
                        <span>Food Safety Practice Test Format and Topics</span>
                        <span class="faq-toggle">+</span>
                    </dt>
                    <dd class="faq-answer" hidden>
                        Each practice test randomly selects <strong>40 questions</strong> from our bank of <strong>400 exam-style questions</strong>. Topics include temperature control, cross contamination, allergens, cleaning, HACCP, and FSS duties.
                    </dd>
                    <dt class="faq-question" tabindex="0" aria-expanded="false">
                        <span>Is food safety certification valid in every Australian state?</span>
                        <span class="faq-toggle">+</span>
                    </dt>
                    <dd class="faq-answer" hidden>
                        Yes. Nationally recognised units SITXFSA005 and SITXFSA006 are accepted across all states and territories. Each state has its own regulator (e.g. NSW Food Authority, Department of Health Victoria).
                    </dd>
                    <dt class="faq-question" tabindex="0" aria-expanded="false">
                        <span>Is this the official food safety test?</span>
                        <span class="faq-toggle">+</span>
                    </dt>
                    <dd class="faq-answer" hidden>
                        This practice test is for educational purposes only. We are not affiliated with FSANZ or any government agency. For official certification, complete training through an accredited RTO.
                    </dd>"""
    body = f"""
    <section class="home-editorial-hero" aria-labelledby="home-hero-title">
        <div class="container home-editorial-hero__inner">
            <p class="home-editorial-hero__badge">SITXFSA005 · All Australian states</p>
            <h1 id="home-hero-title" class="home-editorial-hero__title">Pass Your Food Safety Test <br><span class="home-editorial-hero__accent">Free Practice Test: {QUESTION_COUNT} Questions</span></h1>
            <ul class="home-editorial-hero__list">
                <li><strong>{QUESTION_COUNT}+</strong> exam-style questions (40 per attempt)</li>
                <li><strong>Instant feedback</strong> with explanations for every answer</li>
                <li><strong>Aligned with Food Standards Code</strong> &amp; SITXFSA005/006</li>
            </ul>
            <p class="home-editorial-hero__meta">~25 minutes · No sign up · Unlimited retries</p>
        </div>
    </section>

    <main class="container">
        <div id="start-screen" class="screen active">
            <div class="intro-content intro-content--modes" id="practice-modes"></div>
        </div>
        <div id="quiz-screen" class="screen">
            <div class="progress-container">
                <div class="progress-bar"><div id="progress-fill" class="progress-fill"></div></div>
                <p class="progress-text">Question <span id="current-question">1</span> of <span id="total-questions">40</span></p>
            </div>
            <div class="question-container">
                <div id="question-text" class="question-text"></div>
                <div id="options-container" class="options-container"></div>
                <div id="explanation" class="explanation"></div>
                <button id="next-btn" class="btn btn-primary" style="display: none;">Next Question</button>
            </div>
        </div>
        <div id="result-screen" class="screen">
            <div class="result-content">
                <h2 id="result-title">Test Complete!</h2>
                <div id="score-display" class="score-display">
                    <div class="score-circle"><span id="score-percentage">0%</span></div>
                    <p id="score-text" class="score-text"></p>
                    <p id="pass-fail-message" class="pass-fail-message"></p>
                </div>
                <button id="restart-btn" class="btn btn-primary">Restart Test</button>
            </div>
        </div>
        <div id="affiliate-box" class="affiliate-box">
            <div class="affiliate-card">
                <p class="affiliate-eyebrow">Ready for the real thing?</p>
                <h3 class="affiliate-heading">Book your accredited food safety course</h3>
                <p class="affiliate-text">Practice gets you exam-ready, but your certificate must be issued by a registered training organisation. Compare providers in your state from $85.</p>
                <div class="affiliate-actions" style="display:flex;gap:10px;flex-wrap:wrap;">
                <a href="/" class="btn btn-primary">Start free practice test &rarr;</a>
                <a href="/find-a-course.html" class="btn btn-secondary affiliate-cta" rel="sponsored nofollow">Find an accredited course &rarr;</a></div>
                <p class="affiliate-disclosure">We may earn a commission from course providers, at no extra cost to you.</p>
            </div>
        </div>
    </main>

    <article id="seo-text" class="seo-text">
        <div class="container">
            <header><h2>Australian Food Safety Practice Test — Free Online Preparation for SITXFSA005</h2></header>
            <section aria-label="Flashcards">
                <div class="affiliate-card affiliate-card--promo">
                    <p class="affiliate-eyebrow">Free · interactive</p>
                    <h3 class="affiliate-heading">Food Safety Flashcards</h3>
                    <p class="affiliate-text">Flip through exam-style questions from all 12 syllabus areas. A quick way to revise temperature rules, allergens, HACCP, and FSS duties on your phone.</p>
                    <a href="/flashcards.html" class="btn btn-primary">Open flashcards &rarr;</a>
                </div>
            </section>
            <section aria-label="Study by topic">
                <h3>Study by Topic: All 12 Food Safety Areas</h3>
                <p>Drill any topic from the food safety syllabus. Each topic page explains key facts and links to a focused practice set:</p>
                <div class="topic-link-grid">
{topic_links}
                </div>
            </section>
            <section>
                <h3>Frequently Asked Questions About Food Safety</h3>
                <dl>
{faq_items}
                </dl>
            </section>
        </div>
    </article>

    <div class="ad-slot" data-ad-slot="home-incontent" role="complementary" aria-label="Advertisement">
        <span class="ad-slot__label">Advertisement</span>
    </div>"""
    html = page_shell(
        f"Free Food Safety Practice Test Australia {YEAR} | {QUESTION_COUNT} Questions",
        f"Free food safety practice test: {QUESTION_COUNT} exam-style SITXFSA005 questions with instant feedback. No sign-up — prepare for your food handler or FSS assessment.",
        f"{DOMAIN}/",
        body,
        extra_head=HOME_SCHEMA,
        active_nav="Practice Test",
        scripts="""    <script src="faq-accordion.js" defer></script>
    <script type="module" src="script.js"></script>""",
    )
    (ROOT / "index.html").write_text(html, encoding="utf-8")


def write_state_page(code, info):
    faq_schema = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in info["extra_faq"]]
    extra_head = f"""    <meta name="state" content="{code}">
    <script type="application/ld+json">
{json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_schema}, indent=2)}
    </script>"""
    faq_html = "\n".join(
        f"""                    <dt class="faq-question" tabindex="0" aria-expanded="false"><span>{q}</span><span class="faq-toggle">+</span></dt>
                    <dd class="faq-answer" hidden>{a}</dd>"""
        for q, a in info["extra_faq"]
    )
    body = f"""
    <section class="home-editorial-hero" aria-labelledby="state-hero-title">
        <div class="container home-editorial-hero__inner">
            <p class="home-editorial-hero__badge">{info["abbr"]} · {info["regulator"]}</p>
            <h1 id="state-hero-title" class="home-editorial-hero__title">Food Safety Practice Test <br><span class="home-editorial-hero__accent">{info["name"]} ({info["abbr"]})</span></h1>
            <ul class="home-editorial-hero__list">
                <li><strong>{QUESTION_COUNT}+</strong> exam-style questions (40 per attempt)</li>
                <li>Aligned with <strong>{info["regulator"]}</strong> requirements</li>
                <li>SITXFSA005 food handler &amp; SITXFSA006 FSS preparation</li>
            </ul>
        </div>
    </section>
    <main class="container">
        <div id="start-screen" class="screen active"><div class="intro-content intro-content--modes" id="practice-modes"></div></div>
        <div id="quiz-screen" class="screen">
            <div class="progress-container">
                <div class="progress-bar"><div id="progress-fill" class="progress-fill"></div></div>
                <p class="progress-text">Question <span id="current-question">1</span> of <span id="total-questions">40</span></p>
            </div>
            <div class="question-container">
                <div id="question-text" class="question-text"></div>
                <div id="options-container" class="options-container"></div>
                <div id="explanation" class="explanation"></div>
                <button id="next-btn" class="btn btn-primary" style="display: none;">Next Question</button>
            </div>
        </div>
        <div id="result-screen" class="screen">
            <div class="result-content">
                <h2 id="result-title">Test Complete!</h2>
                <div id="score-display" class="score-display">
                    <div class="score-circle"><span id="score-percentage">0%</span></div>
                    <p id="score-text" class="score-text"></p>
                    <p id="pass-fail-message" class="pass-fail-message"></p>
                </div>
                <button id="restart-btn" class="btn btn-primary">Restart Test</button>
            </div>
        </div>
    </main>
    <article class="seo-text">
        <div class="container">
            <h2>Food Safety Training in {info["name"]}</h2>
            <p>Food safety in {info["name"]} is regulated by <a href="{info["reg_url"]}" target="_blank" rel="noopener"><strong>{info["regulator"]}</strong></a>. {info["fss"]} {info["handler"]}</p>
            <h3>{info["abbr"]} Food Safety FAQ</h3>
            <dl>{faq_html}</dl>
            <p><a href="/find-a-course.html">Find an accredited food safety course in {info["abbr"]} &rarr;</a></p>
        </div>
    </article>"""
    html = page_shell(
        f"Free Food Safety Practice Test {info['abbr']} {YEAR} | SITXFSA005",
        f"Free food safety practice test for {info['name']} ({info['abbr']}). {QUESTION_COUNT} SITXFSA005 questions with instant feedback. No sign-up required.",
        f"{DOMAIN}/food-safety-{code}.html",
        body,
        extra_head=extra_head,
        active_nav="Practice Test",
        scripts="""    <script src="faq-accordion.js" defer></script>
    <script type="module" src="script.js"></script>""",
    )
    (ROOT / f"food-safety-{code}.html").write_text(html, encoding="utf-8")


def write_topic_page(slug, label, subtitle, intro):
    related = topic_grid_html(exclude_slug=slug)
    body = f"""
    <main class="container">
        <article class="content-page">
            <div class="content-hero">
                <h1>{label}</h1>
                <p class="content-hero-sub">{subtitle}</p>
                <a href="/?mode=topic&amp;topic={slug}" class="btn btn-primary">Practice this topic &rarr;</a>
            </div>
            <section class="guide-section">
                <h3>About this topic</h3>
                <p>{intro} This topic is part of SITXFSA005 (food handlers) and SITXFSA006 (Food Safety Supervisors) training across Australia.</p>
            </section>
            <section class="guide-section">
                <h3>Key facts to remember</h3>
                <p>Use our topic drill to test yourself on {label.lower()}. Read the study guide first, then practise until you score consistently above 80%.</p>
            </section>
            <section class="guide-section">
                <h3>Related topics</h3>
                <div class="topic-link-grid">
{related}
                </div>
            </section>
            <div class="content-cta">
                <h3>Ready to test yourself?</h3>
                <p>Our {QUESTION_COUNT}-question bank includes dedicated drills for every topic.</p>
                <a href="/?mode=topic&amp;topic={slug}" class="btn btn-primary">Start {label} drill</a>
                <a href="/" class="btn btn-secondary">Full practice test</a>
            </div>
        </article>
    </main>"""
    html = page_shell(
        f"{label} Practice Questions {YEAR}",
        f"Practise {label.lower()} questions for your food safety test. Free SITXFSA005/SITXFSA006 drill with instant feedback.",
        f"{DOMAIN}/topic-{slug}.html",
        body,
        active_nav="Study Guide",
    )
    (ROOT / f"topic-{slug}.html").write_text(html, encoding="utf-8")


def write_guide():
    body = f"""
    <main class="container">
        <article class="content-page guide-page">
            <h1>Food Safety Study Guide {YEAR}</h1>
            <p class="content-hero-sub">Everything you need for SITXFSA005 (food handler) and SITXFSA006 (Food Safety Supervisor)</p>
            <section class="guide-section">
                <h2>Core topics</h2>
                <div class="topic-link-grid">
{topic_grid_html()}
                </div>
            </section>
            <section class="guide-section">
                <h2>Quick reference</h2>
                <ul>
                    <li><strong>Temperature danger zone:</strong> 5°C to 60°C — minimise time food spends here</li>
                    <li><strong>Hot holding:</strong> 60°C or above</li>
                    <li><strong>Cold storage:</strong> 5°C or below</li>
                    <li><strong>Cook poultry/minced meat:</strong> 75°C at centre</li>
                    <li><strong>FSS renewal:</strong> every 5 years</li>
                    <li><strong>Top allergens (AU):</strong> peanut, tree nuts, milk, egg, wheat, soy, sesame, fish, crustacea, lupin</li>
                </ul>
            </section>
            <div class="content-cta">
                <a href="/" class="btn btn-primary">Start free practice test</a>
                <a href="/tips.html" class="btn btn-secondary">Exam tips</a>
            </div>
        </article>
    </main>"""
    (ROOT / "guide.html").write_text(
        page_shell(
            f"Food Safety Study Guide {YEAR} | SITXFSA005 & SITXFSA006",
            "Complete food safety study guide for Australian food handlers and Food Safety Supervisors. Temperature, hygiene, allergens, HACCP and more.",
            f"{DOMAIN}/guide.html",
            body,
            extra_head=GUIDE_SCHEMA,
            active_nav="Study Guide",
        ),
        encoding="utf-8",
    )


def write_tips():
    body = """
    <main class="container">
        <article class="content-page">
            <h1>Food Safety Exam Tips</h1>
            <section class="guide-section">
                <h2>Before the test</h2>
                <ul>
                    <li>Complete at least three full 40-question practice runs on this site</li>
                    <li>Drill weak topics using topic mode — especially temperature and cross contamination</li>
                    <li>Memorise the danger zone (5°C–60°C) and key temperatures (60°C hot hold, 5°C cold, 75°C cook)</li>
                    <li>Review the 10 declared allergens</li>
                </ul>
            </section>
            <section class="guide-section">
                <h2>During the assessment</h2>
                <ul>
                    <li>Read every question twice — many wrong answers come from misreading "NOT" or "EXCEPT"</li>
                    <li>Eliminate obviously wrong options first</li>
                    <li>When unsure, choose the answer that best protects public health</li>
                    <li>Most RTOs require about 80% to pass — aim higher in practice</li>
                </ul>
            </section>
            <div class="content-cta">
                <a href="/" class="btn btn-primary">Start practice test</a>
            </div>
        </article>
    </main>"""
    (ROOT / "tips.html").write_text(
        page_shell(
            f"How to Pass the Food Safety Test {YEAR} | Exam Tips",
            "Expert tips to pass your Australian food safety handler or FSS assessment. Study strategy, common mistakes, and what RTOs expect.",
            f"{DOMAIN}/tips.html",
            body,
            active_nav="Exam Tips",
        ),
        encoding="utf-8",
    )


def write_find_course():
    providers = [
        ("Australian Institute of Food Safety (AIFS)", "https://www.foodsafety.com.au/", "$199–$230"),
        ("Clear To Work", "https://www.cleartowork.com.au/", "$86–$125"),
        ("Allens Training", "https://www.allenstraining.com.au/", "$85–$110"),
        ("Club Training Australia", "https://clubtraining.com.au/", "$95–$120"),
    ]
    rows = "\n".join(
        f'<li><a href="{url}" target="_blank" rel="sponsored noopener">{name}</a> — typical price {price}</li>'
        for name, url, price in providers
    )
    body = f"""
    <main class="container">
        <article class="content-page">
            <h1>Find a Food Safety Course</h1>
            <p>Practice tests prepare you for the knowledge component, but official <strong>SITXFSA005</strong> (food handler) or <strong>SITXFSA006</strong> (Food Safety Supervisor) certificates must be issued by a registered training organisation (RTO).</p>
            <section class="guide-section">
                <h2>Popular accredited providers</h2>
                <ul>{rows}</ul>
            </section>
            <section class="guide-section">
                <h2>What to look for</h2>
                <ul>
                    <li>Nationally recognised unit codes (SITXFSA005 or SITXFSA006)</li>
                    <li>RTO listed on training.gov.au</li>
                    <li>Certificate valid in your state</li>
                    <li>FSS certificate renewed every 5 years</li>
                </ul>
            </section>
            <p class="footer-disclaimer">We may earn a commission if you purchase through links on this page.</p>
            <div class="content-cta"><a href="/" class="btn btn-primary">Back to free practice test</a></div>
        </article>
    </main>"""
    (ROOT / "find-a-course.html").write_text(
        page_shell(
            f"Find Food Safety Course Australia {YEAR} | SITXFSA005 & FSS",
            "Compare accredited food safety courses in Australia. SITXFSA005 food handler and SITXFSA006 FSS training from $85.",
            f"{DOMAIN}/find-a-course.html",
            body,
            active_nav="Find a Course",
        ),
        encoding="utf-8",
    )


def write_glossary():
    terms = [
        ("CCP", "Critical Control Point — a step where control is essential to food safety."),
        ("Cross contamination", "Transfer of harmful bacteria or allergens from one food/surface to another."),
        ("Danger zone", "5°C to 60°C — temperature range where bacteria multiply rapidly."),
        ("FSS", "Food Safety Supervisor — trained person responsible for on-site food safety."),
        ("FSANZ", "Food Standards Australia New Zealand — develops food standards."),
        ("HACCP", "Hazard Analysis Critical Control Points — systematic food safety management."),
        ("Potentially hazardous food", "Food that supports bacterial growth; needs temperature control."),
        ("SITXFSA005", "National unit: Use hygienic practices for food safety (food handler)."),
        ("SITXFSA006", "National unit: Participate in safe food handling practices (FSS)."),
        ("Sanitise", "Reduce microorganisms to safe levels after cleaning."),
    ]
    dl = "\n".join(f"<dt><strong>{t}</strong></dt><dd>{d}</dd>" for t, d in terms)
    body = f"""
    <main class="container">
        <article class="content-page">
            <h1>Food Safety Glossary</h1>
            <dl class="glossary-list">{dl}</dl>
            <div class="content-cta"><a href="/" class="btn btn-primary">Practice test</a></div>
        </article>
    </main>"""
    (ROOT / "glossary.html").write_text(
        page_shell(
            f"Food Safety Glossary {YEAR} | Key Terms A–Z",
            "Australian food safety glossary: danger zone, HACCP, FSS, SITXFSA005, cross contamination and more.",
            f"{DOMAIN}/glossary.html",
            body,
            active_nav="Glossary",
        ),
        encoding="utf-8",
    )


def write_flashcards():
    body = """
    <main class="container">
        <article class="content-page">
            <div class="feature-hero">
                <h1>Food Safety Flashcards</h1>
                <p>Flip through the full question bank at your own pace. Tap a card to reveal the answer and explanation, bookmark tricky ones, or have them read aloud.</p>
            </div>
            <div id="flashcards-app"></div>
        </article>
    </main>"""
    (ROOT / "flashcards.html").write_text(
        page_shell(
            f"Food Safety Flashcards {YEAR} | Free Study Cards",
            f"Free food safety flashcards covering all {QUESTION_COUNT} SITXFSA005 practice questions with answers and explanations. Read-aloud and bookmark options. No sign-up.",
            f"{DOMAIN}/flashcards.html",
            body,
            active_nav="Flashcards",
            scripts="""    <script src="faq-accordion.js" defer></script>
    <script src="site-ui.js" defer></script>
    <script type="module" src="script.js"></script>""",
        ),
        encoding="utf-8",
    )


def write_bookmarks():
    body = """
    <main class="container">
        <article class="content-page">
            <div class="feature-hero">
                <h1>Your Bookmarked Questions</h1>
                <p>Questions you saved during a practice test or on flashcards appear here for focused review. Bookmarks are stored privately in your browser.</p>
            </div>
            <div id="bookmarks-app"></div>
            <div class="content-cta" style="margin-top:24px;">
                <a href="/" class="btn btn-primary">Take a practice test</a>
                <a href="/flashcards.html" class="btn btn-secondary">Study flashcards</a>
            </div>
        </article>
    </main>"""
    (ROOT / "bookmarks.html").write_text(
        page_shell(
            "My Bookmarked Questions | Food Safety Practice Test",
            "Review food safety questions you bookmarked during practice, with answers and explanations. Saved privately in your browser.",
            f"{DOMAIN}/bookmarks.html",
            body,
            scripts="""    <script src="faq-accordion.js" defer></script>
    <script src="site-ui.js" defer></script>
    <script type="module" src="script.js"></script>""",
        ).replace('<meta name="robots" content="index, follow">', '<meta name="robots" content="noindex, follow">'),
        encoding="utf-8",
    )


def write_progress():
    body = """
    <main class="container">
        <article class="content-page">
            <div class="feature-hero">
                <h1>Your Progress</h1>
                <p>Your stats are saved privately in your browser. Keep practising until you consistently score 80%+ on full practice tests.</p>
            </div>
            <div id="progress-app"></div>
        </article>
    </main>"""
    (ROOT / "progress.html").write_text(
        page_shell(
            "My Progress | Food Safety Practice Test",
            "Track your food safety test preparation: XP, day streak, best and average scores, weak questions, and exam-readiness.",
            f"{DOMAIN}/progress.html",
            body,
            scripts="""    <script src="faq-accordion.js" defer></script>
    <script src="site-ui.js" defer></script>
    <script type="module" src="script.js"></script>""",
        ).replace('<meta name="robots" content="index, follow">', '<meta name="robots" content="noindex, follow">'),
        encoding="utf-8",
    )


def write_about_legal():
    about = """
    <main class="container"><article class="content-page">
    <h1>About Food Safety Practice AU</h1>
    <p>We provide free food safety practice tests for Australian food handlers and Food Safety Supervisors preparing for SITXFSA005 and SITXFSA006 assessments.</p>
    <p>We are not affiliated with FSANZ, state health departments, or any government body.</p>
    </article></main>"""
    (ROOT / "about.html").write_text(
        page_shell("About | Food Safety Practice AU", "About Food Safety Practice AU — free SITXFSA005 practice tests.", f"{DOMAIN}/about.html", about),
        encoding="utf-8",
    )
    legal = """
    <main class="container"><article class="content-page">
    <h1 id="legal">Legal Notice</h1>
    <p>Educational content only. Not official certification.</p>
    <h2 id="privacy">Privacy Policy</h2>
    <p>We use cookies for analytics and advertising with your consent. Progress may be stored locally in your browser.</p>
    <h2 id="contact">Contact</h2>
    <p>Email: contact@food-safety-practice-test-au.com</p>
    </article></main>"""
    (ROOT / "legal.html").write_text(
        page_shell("Legal & Privacy | Food Safety Practice AU", "Legal notice and privacy policy.", f"{DOMAIN}/legal.html", legal),
        encoding="utf-8",
    )
    terms = """
    <main class="container"><article class="content-page">
    <h1>Terms of Use</h1>
    <p>Use this site for personal study. Content is provided as-is without warranty. Practice tests do not replace accredited RTO training.</p>
    </article></main>"""
    (ROOT / "terms.html").write_text(
        page_shell("Terms of Use | Food Safety Practice AU", "Terms of use for Food Safety Practice AU.", f"{DOMAIN}/terms.html", terms),
        encoding="utf-8",
    )


def write_blog():
    """Blog posts are maintained via tools/build_blog_posts.py — do not overwrite here."""
    pass


def write_sitemap():
    # DEPRECATED: the sitemap is now generated from tools/SITEMAP_URLS.py via
    # tools/build_all_safe.py (single source of truth). This legacy version is
    # kept only for the full build_site.py flow; prefer build_all_safe.py.
    urls = [f"{DOMAIN}/"]
    for code in STATES:
        urls.append(f"{DOMAIN}/food-safety-{code}.html")
    for slug, _, _, _ in TOPICS:
        urls.append(f"{DOMAIN}/topic-{slug}.html")
    for page in ["guide.html", "tips.html", "find-a-course.html", "flashcards.html", "glossary.html", "about.html", "legal.html", "terms.html", "blog/", "temperature-danger-zone-checker.html"]:
        urls.append(f"{DOMAIN}/{page}")
    blog_slugs = [
        "how-to-pass-food-safety-test",
        "food-safety-supervisor-vs-food-handler",
        "is-food-safety-test-hard-australia",
        "temperature-danger-zone-australia-guide",
        "food-safety-certificate-cost-australia-by-state",
        "how-to-get-food-safety-certificate-online-australia",
        "food-safety-training-aged-care-childcare",
        "10-priority-allergens-australia-food-safety-exam",
        "food-safety-certificate-expire-renewal-australia",
        "haccp-basics-food-handlers-australia",
        "cross-contamination-food-safety-exam-tips",
        "food-safety-practice-test-before-real-exam",
    ]
    for slug in blog_slugs:
        urls.append(f"{DOMAIN}/blog/{slug}/")
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{u}</loc>")
        lines.append(f"    <lastmod>2026-06-05</lastmod>")
        lines.append("  </url>")
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_config():
    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n",
        encoding="utf-8",
    )
    redirects = "\n".join(
        f'    {{ "source": "/food-safety-{code}", "destination": "/food-safety-{code}.html", "permanent": true }},'
        for code in STATES
    )
    vercel = f"""{{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "cleanUrls": false,
  "trailingSlash": false,
  "redirects": [
    {{
      "source": "/:path*",
      "has": [{{ "type": "host", "value": "www.food-safety-practice-test-au.com" }}],
      "destination": "https://food-safety-practice-test-au.com/:path*",
      "permanent": true
    }},
{redirects}
    {{ "source": "/", "has": [{{ "type": "query", "key": "state", "value": "nsw" }}], "destination": "/food-safety-nsw.html", "permanent": true }},
    {{ "source": "/", "has": [{{ "type": "query", "key": "state", "value": "vic" }}], "destination": "/food-safety-vic.html", "permanent": true }},
    {{ "source": "/", "has": [{{ "type": "query", "key": "state", "value": "qld" }}], "destination": "/food-safety-qld.html", "permanent": true }},
    {{ "source": "/", "has": [{{ "type": "query", "key": "state", "value": "wa" }}], "destination": "/food-safety-wa.html", "permanent": true }},
    {{ "source": "/", "has": [{{ "type": "query", "key": "state", "value": "sa" }}], "destination": "/food-safety-sa.html", "permanent": true }},
    {{ "source": "/", "has": [{{ "type": "query", "key": "state", "value": "act" }}], "destination": "/food-safety-act.html", "permanent": true }},
    {{ "source": "/", "has": [{{ "type": "query", "key": "state", "value": "nt" }}], "destination": "/food-safety-nt.html", "permanent": true }},
    {{ "source": "/", "has": [{{ "type": "query", "key": "state", "value": "tas" }}], "destination": "/food-safety-tas.html", "permanent": true }}
  ]
}}"""
    (ROOT / "vercel.json").write_text(vercel, encoding="utf-8")


def main():
    print("Building Food Safety Practice Test AU...")
    shutil.copy(WHITECARD / "faq-accordion.js", ROOT / "faq-accordion.js")
    site_ui = (WHITECARD / "site-ui.js").read_text(encoding="utf-8").replace("wc_", "fs_")
    (ROOT / "site-ui.js").write_text(site_ui, encoding="utf-8")
    adapt_style_css()
    adapt_script_js()
    questions = load_unique_questions()
    if questions:
        print(f"  Loaded {len(questions)} authored unique questions (tools/questions_data.json)")
    else:
        questions = expand_questions()
        print(f"  WARNING: using legacy padded bank ({len(questions)} questions) — run tools/build_questions.py to author unique ones")
    write_questions_js(questions)
    write_index()
    for code, info in STATES.items():
        write_state_page(code, info)
    for slug, label, subtitle, intro in TOPICS:
        write_topic_page(slug, label, subtitle, intro)
    write_guide()
    write_tips()
    write_find_course()
    write_glossary()
    write_flashcards()
    write_bookmarks()
    write_progress()
    write_about_legal()
    write_blog()
    write_sitemap()
    write_config()
    print(f"Done. Site ready at {ROOT}")


if __name__ == "__main__":
    main()
