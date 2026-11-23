"""Group-site pages (www.motorinnautogroup.com)."""

G = "https://www.motorinnautogroup.com"
T = "https://www.motorinntoyotaofcarroll.com"
C = "https://www.motorinnofcarroll.com"

COMMON_SOURCES = [
    "Address, phone: group contact page (.firecrawl/motorinnautogroup.com-contact-us.md); phone ruling brain/STATE.md 2026-11-02.",
    "Hours, walk-in trade appraisal, lender-network financing, test-drive framing, Chevrolet certified: content/ready-design-OWNER-NOTES.md (owner answers 2026-10-23).",
    "'Just off West US Highway 30', store names: group homepage snippet in .firecrawl/nap-audit/20261029/_ap_uest.json.",
    "'Factory service', 'franchised': brain/BRIEF.md.",
]

PAGES = [
    {
        "slug": "contactus-carroll",
        "store": "group",
        "path": "/contactus.aspx",
        "status": "IN-PLACE content block for the existing live contact page /contactus.aspx. /Contactus/Carroll, the URL in the GSC data, now 301-redirects there (live check 2026-11-23), and /contactus.aspx is its own canonical. Not a new URL. The folder slug 'contactus-carroll' is kept for continuity.",
        "placement": "Add the sections and FAQ below as one content block BELOW the existing contact form on /contactus.aspx. Keep the page's current title, meta and H1 in cycle 1. The H1 line below is the proposed cycle-2 heading. Until then, render it as styled text, not a second H1.",
        "ship_plan": [
            "Cycle 1: the content block only (sections + FAQ + visit block), placed below the form, plus the FAQPage/AutoDealer JSON-LD. Leave the title, meta and H1 unchanged.",
            "Cycle 2 (after 2-4 weeks of GSC readings): switch the title and meta to the meta.md versions, then promote the H1.",
            "Separately, as a DealerOn case: canonical or 301 decision for /car-dealerships-carroll-iowa and /car-dealerships-in-carroll-iowa.html (Spencer's call).",
        ],
        "tier": "ready-now",
        "queries": [
            "car dealerships carroll iowa", "carroll iowa car dealerships", "carroll dealerships",
            "car dealerships in carroll iowa", "carroll iowa dealerships", "carroll ia dealerships",
            "carroll iowa auto dealers", "car dealerships carroll", "carroll car dealerships",
            "carroll ia car dealerships", "car dealers carroll iowa", "carroll car dealership",
            "carroll iowa car dealers", "car dealership carroll iowa", "car dealers in carroll iowa",
            "dealerships in carroll iowa", "carroll auto sales",
        ],
        "h1": "Car Dealerships in Carroll, Iowa: Motor Inn Auto Group",
        "title": "Car Dealerships in Carroll, Iowa | Motor Inn Auto Group",
        "meta": "Toyota and Chevrolet at one Carroll, Iowa address: 1526 Le Clark Road. New and used vehicles, trade-ins, financing and service. Call (712) 792-5000.",
        "og_title": "Car Dealerships in Carroll, Iowa | Motor Inn Auto Group",
        "og_desc": "Toyota and Chevrolet at one Carroll address. New and used vehicles, walk-in trade appraisals, financing and factory service.",
        "cta": "Call (712) 792-5000 or stop by 1526 Le Clark Road, Carroll.",
        "intro": """
Motor Inn Auto Group is a car dealership at 1526 Le Clark Road in Carroll, Iowa, just off West US Highway 30. Two franchised stores share that one address: Motor Inn Toyota of Carroll and Motor Inn Chevrolet of Carroll. You can shop new Toyotas and Chevrolets, look at used cars of any brand, trade in, set up financing and book service in one stop.
""",
        "sections": [
            ("Which car dealerships are in Carroll, Iowa?", f"""
Motor Inn Auto Group is the Toyota and Chevrolet dealership group on Le Clark Road in Carroll. It is family-owned and runs two franchised stores under one roof, so you don't have to drive across town to compare brands.

If you're comparing Carroll car dealerships, start with three questions. Do they carry the brand you want? Can they take your trade and handle financing in the same visit? Can they service the vehicle after you buy it? At Motor Inn the answer to all three is yes.
"""),
            ("What can I buy at a Carroll car dealership?", f"""
At Motor Inn you can buy a new Toyota, a new Chevrolet, or a used car, truck or SUV of any brand.

- [Search new Toyota and Chevrolet inventory]({G}/searchnew.aspx)
- [Search used inventory]({G}/used-inventory)
- [Used vehicles under $20,000]({G}/under-20000)

Inventory changes, so the live search is the best way to see what's on the lot today.
"""),
            ("Is there a Chevy dealer and a Toyota dealer in Carroll, Iowa?", f"""
Yes. Motor Inn Toyota of Carroll and Motor Inn Chevrolet of Carroll both operate at 1526 Le Clark Road. You can compare a Toyota and a Chevrolet side by side on the same visit.

Each store has its own website: [Motor Inn Toyota of Carroll]({T}/) and [Motor Inn Chevrolet of Carroll]({C}/).
"""),
            ("Can I trade in and finance at the same dealership?", f"""
Yes. Trade appraisals are walk-in, so you don't need an appointment. An online trade estimate is also on the [trade page]({G}/trade.aspx).

For financing, Motor Inn works with a network of lenders on new and used vehicles. Bring the payment range you have in mind, and the team will go through your options with you. Details are on the [financing page]({G}/finance-locations.html).
"""),
            ("Can I get my car serviced at a Carroll dealership?", f"""
Yes. Motor Inn offers factory service for Toyota and Chevrolet vehicles in Carroll, and the Chevrolet service department is Chevrolet certified. Both service departments are listed on the [service page]({G}/service-locations.html).
"""),
            ("How do I schedule a test drive in Carroll?", f"""
Call (712) 792-5000 with the vehicle you want to drive, and the team will confirm the vehicle and a time with you. Test-drive details are also on the [test drive page]({G}/testdrive.aspx).
"""),
        ],
        "faq": [
            ("Which car dealerships are in Carroll, Iowa?",
             "Motor Inn Auto Group is a car dealership at 1526 Le Clark Road in Carroll, Iowa. It runs two franchised stores at that address, Motor Inn Toyota of Carroll and Motor Inn Chevrolet of Carroll. Shoppers can compare new Toyota and Chevrolet vehicles and used cars of any brand in one visit. The phone number is (712) 792-5000."),
            ("Where is the car dealership in Carroll, IA?",
             "Motor Inn Auto Group is at 1526 Le Clark Road, Carroll, IA 51401, just off West US Highway 30. Sales hours are Monday through Wednesday 8:00 a.m. to 5:30 p.m., Thursday 8:00 a.m. to 7:00 p.m., Friday 8:00 a.m. to 5:30 p.m. and Saturday 8:00 a.m. to 3:00 p.m. The dealership is closed on Sunday."),
            ("Is there a Chevy dealer and a Toyota dealer in Carroll, Iowa?",
             "Yes. Motor Inn Toyota of Carroll and Motor Inn Chevrolet of Carroll both operate at 1526 Le Clark Road in Carroll, Iowa. Shoppers can compare a new Toyota and a new Chevrolet on the same visit. Both stores can be reached at (712) 792-5000."),
            ("Can I trade in my car at a Carroll dealership without an appointment?",
             "Yes. Motor Inn Auto Group in Carroll, Iowa, appraises trade-ins on a walk-in basis, so no appointment is needed. Shoppers can also start a trade value online on the dealership's trade page before they visit."),
            ("Can I get car financing at a dealership in Carroll, Iowa?",
             "Yes. Motor Inn Auto Group in Carroll works with a network of lenders to set up financing on new and used vehicles. Shoppers can bring a payment range, and the team will go through the options with them. Call (712) 792-5000 to start."),
        ],
        "links": [
            ("Search new Toyota and Chevrolet inventory", f"{G}/searchnew.aspx", "same site"),
            ("Search used inventory", f"{G}/used-inventory", "same site"),
            ("Used vehicles under $20,000", f"{G}/under-20000", "same site"),
            ("Motor Inn Toyota of Carroll", f"{T}/", "cross-site (Toyota store)"),
            ("Motor Inn Chevrolet of Carroll", f"{C}/", "cross-site (Chevy store)"),
            ("trade page", f"{G}/trade.aspx", "same site"),
            ("financing page", f"{G}/finance-locations.html", "same site"),
            ("service page", f"{G}/service-locations.html", "same site"),
            ("test drive page", f"{G}/testdrive.aspx", "same site"),
            ("hours page", f"{G}/hours.aspx", "same site (visit block)"),
        ],
        "post_links": [
            "Link 'Chevy dealer in Carroll' -> motorinnofcarroll.com/chevy-dealer-carroll-iowa once it is live.",
            "Link 'Toyota dealer in Iowa' -> motorinntoyotaofcarroll.com/toyota-dealers-in-iowa once it is live.",
        ],
        "sources": COMMON_SOURCES,
        "routing": """
Group site. "Car dealerships Carroll Iowa" is cross-brand, general-dealership intent, which Spencer's 2026-11-23 rule sends to motorinnautogroup.com.

**URL choice: in-place on the contact page, not a new page.** GSC sends this cluster to /Contactus/Carroll (11 of the 13 cluster rows that are also in the Ads-40 file land there, and the other 2 land on the group homepage; 203 clicks at position 10.3 on 'carroll iowa car dealerships'; the brain/reports/gsc-cannibalization-2026-11-03.md split shows /Contactus/Carroll winning). **That URL now 301-redirects to /contactus.aspx**, and /contactus.aspx declares itself canonical (curl check 2026-11-23). The editable page is /contactus.aspx, and the GSC credit consolidates there. Other URLs chasing this intent:
1. /contactus.aspx (live; receives the ranking contact traffic). **Recommended owner.**
2. /car-dealerships-carroll-iowa (live; its 2026-10 approved refresh prints the banned 522-2526 number).
3. /car-dealerships-in-carroll-iowa.html (live; duplicate).
4. content/ready-design/contactus-money-page.html (unpublished draft for the same /contactus.aspx page, same H1).

Spencer to decide: (a) whether 2 and 3 get a canonical or 301 to /contactus.aspx; (b) which copy ships on /contactus.aspx, this package or the ready-design draft. Recommended: this package, because it carries the 12-month evidence and current house rules. Don't ship both.
""",
        "notes": [
            "This content block goes BELOW the existing contact form. Keep the form as the first thing on the page: it is the #1 lead page (brain/STATE.md, 7,166 key events in 28 days).",
            "/Contactus/Carroll 301s to /contactus.aspx (checked 2026-11-23). Internal links and GBP should point at /contactus.aspx directly, with no UTM variants (see brain/reports/gsc-cannibalization-2026-11-03.md).",
            "Years in business were left out on purpose: the homepage says 'over 85 years', the owner notes say '75+', and the 2026-10 pages say 'since 1934'. Pick one and it can go in the first section.",
            "Hours are owner-verified sales hours. Service hours are left to the hours page.",
        ],
        "ai_summary": "Motor Inn Auto Group is a family-owned car dealership at 1526 Le Clark Road, Carroll, Iowa 51401, phone (712) 792-5000. Two franchised stores share the address: Motor Inn Toyota of Carroll and Motor Inn Chevrolet of Carroll. It sells new Toyota and Chevrolet vehicles and used vehicles of any brand, offers walk-in trade appraisals, arranges financing through a lender network, and provides factory service.",
    },
    {
        "slug": "used-cars-carroll-iowa",
        "store": "group",
        "path": "/used-cars-carroll-iowa",
        "status": "IN-PLACE refresh of the existing live URL /used-cars-carroll-iowa. Not a new URL.",
        "placement": "Replace the body copy of the live /used-cars-carroll-iowa page in cycle 1. Keep the live title, meta and H1 until cycle 2.",
        "ship_plan": [
            "Cycle 1: body copy + FAQ + JSON-LD. Leave the title, meta and H1 unchanged.",
            "Cycle 2: title, meta and H1 from meta.md and content.md.",
        ],
        "tier": "ready-now",
        "queries": [
            "used cars carroll ia", "used cars carroll iowa", "cars for sale carroll iowa",
            "used car carroll ia", "used cars for sale carroll ia", "used car dealers carroll ia",
            "used car dealerships carroll ia", "used car dealers carroll", "used cars carroll",
            "used car dealerships carroll", "used cars for sale carroll", "used car carroll",
            "used car dealerships near me",
        ],
        "h1": "Used Cars for Sale in Carroll, Iowa",
        "title": "Used Cars for Sale in Carroll, Iowa | Motor Inn Auto Group",
        "meta": "Used cars, trucks and SUVs of every brand at Motor Inn Auto Group, 1526 Le Clark Road, Carroll, Iowa. Walk-in trade appraisals. Call (712) 792-5000.",
        "og_title": "Used Cars for Sale in Carroll, Iowa",
        "og_desc": "Used cars, trucks and SUVs of every brand at Motor Inn Auto Group in Carroll. Trade in, finance and test drive in one visit.",
        "cta": "Search used inventory or call (712) 792-5000.",
        "intro": f"""
Motor Inn Auto Group sells used cars, trucks and SUVs of every brand at 1526 Le Clark Road in Carroll, Iowa. You can trade in your current vehicle, set up financing and take a test drive in the same visit. The [used inventory search]({G}/used-inventory) shows what's on the lot right now.
""",
        "sections": [
            ("Where can I find used cars for sale in Carroll, Iowa?", f"""
Motor Inn Auto Group's used lot is at 1526 Le Clark Road in Carroll, just off West US Highway 30. The used inventory covers more than Toyota and Chevrolet: you'll find other brands too, depending on what has come in on trade.

- [Search all used inventory]({G}/used-inventory)
- [CARFAX 1-Owner vehicles]({G}/carfax-1-owner.html)
- [Certified Pre-Owned Toyotas]({T}/certified-pre-owned.html) at Motor Inn Toyota of Carroll
"""),
            ("Can I find a used car under $20,000 in Carroll?", f"""
Motor Inn Auto Group has live used-inventory filters for vehicles under $20,000 and under $15,000. What's available changes as cars sell and trades come in, so check the filters for today's options:

- [Used vehicles under $20,000]({G}/under-20000)
- [Used vehicles under $15,000]({G}/under-15k.html)
"""),
            ("Which used car dealers in Carroll, IA also service what they sell?", f"""
Motor Inn is a franchised Toyota and Chevrolet dealership, so the same dealership that sells the used car also has factory service for Toyota and Chevrolet on site. After you buy, a used Toyota or Chevrolet can be serviced at the brand's own service department. Both are listed on the [service page]({G}/service-locations.html).
"""),
            ("Can I trade in my car toward a used car?", f"""
Yes. Trade appraisals are walk-in, with no appointment needed. An online trade estimate is also on the [trade page]({G}/trade.aspx).
"""),
            ("Can I get financing on a used car in Carroll?", f"""
Yes. Motor Inn works with a network of lenders on used vehicles as well as new ones. Tell the team your payment range, and they'll walk you through the options. Details are on the [financing page]({G}/finance-locations.html).
"""),
            ("Can I test drive a used car before I buy?", f"""
Yes. Call (712) 792-5000 with the vehicle you're looking at, and the team will confirm the vehicle and a time with you. Test-drive details are also on the [test drive page]({G}/testdrive.aspx).
"""),
        ],
        "faq": [
            ("Where can I find used cars for sale in Carroll, Iowa?",
             "Motor Inn Auto Group sells used cars, trucks and SUVs at 1526 Le Clark Road in Carroll, Iowa, just off West US Highway 30. The used inventory includes more brands than Toyota and Chevrolet, depending on trade-ins. The live used inventory search on motorinnautogroup.com shows what is on the lot today."),
            ("Does a Carroll used car dealer take trade-ins without an appointment?",
             "Yes. Motor Inn Auto Group in Carroll, Iowa, appraises trade-ins on a walk-in basis, so no appointment is needed. Shoppers can also start a trade value online before they visit."),
            ("Can I get financing on a used car in Carroll, Iowa?",
             "Yes. Motor Inn Auto Group in Carroll works with a network of lenders to finance used vehicles as well as new ones. Shoppers can bring a payment range, and the team will go through the options with them."),
            ("How do I find a used car under $20,000 in Carroll?",
             "Motor Inn Auto Group in Carroll, Iowa, has price-filtered used searches for vehicles under $20,000 and under $15,000 on motorinnautogroup.com. Those searches update as inventory changes. To check a specific vehicle, call (712) 792-5000."),
            ("Are there used car dealerships in Carroll, IA?",
             "Yes. Motor Inn Auto Group sells used cars, trucks and SUVs of every brand at 1526 Le Clark Road in Carroll, Iowa. Because it is also a franchised Toyota and Chevrolet dealership, factory service for both brands is on site. The phone number is (712) 792-5000."),
        ],
        "links": [
            ("used inventory search", f"{G}/used-inventory", "same site"),
            ("CARFAX 1-Owner vehicles", f"{G}/carfax-1-owner.html", "same site"),
            ("Certified Pre-Owned Toyotas", f"{T}/certified-pre-owned.html", "cross-site (Toyota store)"),
            ("Used vehicles under $20,000", f"{G}/under-20000", "same site"),
            ("Used vehicles under $15,000", f"{G}/under-15k.html", "same site"),
            ("service page", f"{G}/service-locations.html", "same site"),
            ("trade page", f"{G}/trade.aspx", "same site"),
            ("financing page", f"{G}/finance-locations.html", "same site"),
            ("test drive page", f"{G}/testdrive.aspx", "same site"),
            ("hours page", f"{G}/hours.aspx", "same site (visit block)"),
        ],
        "post_links": [
            "Sibling: link to /best-place-to-buy-used-car-carroll-iowa (live) from the 'Which used car dealers in Carroll, IA also service what they sell?' section if Spencer wants a second used-car entry point.",
        ],
        "sources": COMMON_SOURCES + [
            "Price-filter pages /under-20000 and /under-15k.html, /carfax-1-owner.html: group sitemap snapshot brain/research/live-https_www_motorinnautogroup_com_sitemap_xml.html.",
            "Toyota CPO page: Toyota sitemap snapshot.",
        ],
        "routing": """
Group site. Used inventory is multi-brand, so Spencer's rule sends it to motorinnautogroup.com. "Cars for sale carroll iowa" (425 impressions, position 23.9) is folded in because the searcher hasn't named a brand or new vs used, and the used lot is the broadest match.

**URL choice: refresh the live /used-cars-carroll-iowa** instead of adding a new slug. The group site already has /used-cars, /used-inventory, /used-cars-carroll-iowa and /best-place-to-buy-used-car-carroll-iowa, and another used-cars URL would split the signal further.
""",
        "notes": [
            "The 2026-10 approved refresh of this slug (content/page-packages/2026-10/designed/) is not this copy. If it was published, check it for the banned 522-2526 number: the sibling 2026-10 designed pages print it.",
            "The cluster is about 2,600 impressions at positions 14 to 26, which suggests the live page isn't being picked for these queries. After publish, check in GSC which URL Google chooses.",
            "No competitors are named or described. The franchised-dealer section only states facts about Motor Inn.",
        ],
        "ai_summary": "Motor Inn Auto Group, 1526 Le Clark Road, Carroll, Iowa 51401 (phone (712) 792-5000), sells used cars, trucks and SUVs of every brand alongside new Toyota and Chevrolet vehicles. Trade-in appraisals are walk-in with no appointment, financing is arranged through a lender network, and factory Toyota and Chevrolet service is on site.",
    },
]
