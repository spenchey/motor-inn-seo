"""Chevrolet-site pages (www.motorinnofcarroll.com)."""

G = "https://www.motorinnautogroup.com"
C = "https://www.motorinnofcarroll.com"

CHEVY_SOURCES = [
    "Address: Chevy contact page (.firecrawl/motorinnofcarroll.com-contactus.aspx.md) lists 'Motor Inn of Carroll, 1526 Le Clark Rd, Carroll, IA 51401'.",
    "Phone (712) 792-5000: brain/STATE.md ruling 2026-11-02. The 877-775-6741 / 877-733-5984 numbers on the Chevy contact page look like call-tracking numbers and are not printed.",
    "'Motor Inn Chevrolet of Carroll' name, 'just off West US Highway 30': group homepage snippet (.firecrawl/nap-audit/20261029/_ap_uest.json).",
    "Chevrolet certified service, walk-in trade appraisal, lender-network financing, hours: content/ready-design-OWNER-NOTES.md (2026-10-23).",
    "Model pages and service/finance/trade URLs: Chevy sitemap snapshot brain/research/live-https_www_motorinnofcarroll_com_sitemap_xml.html (2026-11-05).",
    "No Buick/GMC mentions: content/drafts/buick-gmc-removal-request.md (no longer a Buick or GMC dealer).",
]

LEASE_NOTE = "No lease, payment, price or APR figures appear anywhere. Lease and deal queries are answered by sending the shopper to the sales team by phone. The /chevroletspecialoffers page is NOT cited, because the Codex check (2026-11-23) found it lists customer-category programs (military, educator, first responder), not model lease terms."
OEM_NOTE = "Vehicle descriptions are kept qualitative (two-row vs three-row, gas vs electric, light vs heavy duty) with no specs. Spot-check the wording against chevrolet.com before handoff."
FILTER_NOTE = "Model-filtered search links use the DealerOn pattern searchnew.aspx?Model=<Model> (the group homepage uses the same pattern). Click-test each filter before handoff."

PAGES = [
    {
        "slug": "chevy-dealer-carroll-iowa",
        "store": "chevy",
        "path": "/chevy-dealer-carroll-iowa",
        "status": "NEW page. The Chevy site has no dealer-location landing page; the sitemap snapshot shows none.",
        "tier": "ready-now",
        "queries": [
            "motor inn of carroll l.l.c. near me", "motor inn of carroll l.l.c. chevy",
            "motor inn of carroll l.l.c. chevrolet", "chevy carroll iowa", "carroll iowa chevy dealers",
            "chevrolet carroll iowa", "chevy dealer in carroll", "chevrolet dealer carroll",
            "chevy dealer carroll ia", "chevy dealer carroll iowa", "motor inn chevrolet of carroll",
            "chevy dealer near me", "carroll chevrolet", "chevrolet dealer near me", "chevy dealers near me",
            "chevy dealership near me", "chevy dealers in iowa",
        ],
        "h1": "Chevy Dealer in Carroll, Iowa: Motor Inn Chevrolet of Carroll",
        "title": "Chevy Dealer in Carroll, Iowa | Motor Inn of Carroll",
        "meta": "Motor Inn Chevrolet of Carroll, Chevy dealer at 1526 Le Clark Road, Carroll, Iowa. New Chevy trucks and SUVs, used cars and service. (712) 792-5000.",
        "og_title": "Chevy Dealer in Carroll, Iowa | Motor Inn Chevrolet of Carroll",
        "og_desc": "New Chevrolet trucks and SUVs, used vehicles, walk-in trade appraisals and Chevrolet certified service at 1526 Le Clark Road, Carroll.",
        "cta": "Call Motor Inn Chevrolet of Carroll at (712) 792-5000.",
        "intro": f"""
Motor Inn Chevrolet of Carroll is a Chevrolet dealer at 1526 Le Clark Road in Carroll, Iowa, just off West US Highway 30. You'll also see the store listed as Motor Inn of Carroll. It sells new Chevrolet trucks and SUVs, sells used vehicles, and runs a Chevrolet certified service department, all at that one address.
""",
        "sections": [
            ("Where is the Chevy dealer in Carroll, Iowa?", f"""
Motor Inn Chevrolet of Carroll is at 1526 Le Clark Road, Carroll, IA 51401. The store shares its address with Motor Inn Toyota of Carroll, so you can compare a Chevy and a Toyota on the same visit. [Get hours and directions]({C}/hours.aspx).
"""),
            ("Is Motor Inn of Carroll a Chevrolet dealer?", f"""
Yes. Motor Inn of Carroll is the Chevrolet store of Motor Inn Auto Group, a family-owned dealership group in Carroll. The store also goes by Motor Inn Chevrolet of Carroll, and both names refer to the same dealership at 1526 Le Clark Road. [About Motor Inn of Carroll]({C}/aboutus.aspx).
"""),
            ("Which new Chevrolet models can I shop in Carroll?", f"""
In Carroll you can shop the current Chevrolet lineup: Colorado and Silverado trucks, SUVs from the Trax to the Suburban, and the Equinox EV and Blazer EV. The [new Chevrolet inventory search]({C}/searchnew.aspx) shows what's on the lot, and each model has its own page:

- **Trucks:** [Colorado]({C}/2026-chevrolet-colorado), [Silverado 1500]({C}/2026-chevrolet-silverado-ld), [Silverado HD]({C}/2026-chevrolet-silverado-hd), [Silverado EV]({C}/2026-chevrolet-silverado-ev)
- **SUVs:** [Trax]({C}/2026-chevrolet-trax), [Trailblazer]({C}/2026-chevrolet-trailblazer), [Equinox]({C}/2026-chevrolet-equinox), [Blazer]({C}/2026-chevrolet-blazer), [Traverse]({C}/2026-chevrolet-traverse), [Tahoe]({C}/2026-chevrolet-tahoe), [Suburban]({C}/2026-chevrolet-suburban)
- **Electric:** [Equinox EV]({C}/2026-chevrolet-equinox-ev), [Blazer EV]({C}/2026-chevrolet-blazer-ev)

Not sure which one fits? Call (712) 792-5000 and tell the team how you'll use it. Written quotes are available on the [quote page]({C}/quote.aspx).
"""),
            ("Does the Chevy dealer in Carroll service Chevrolets?", f"""
Yes. The service department at Motor Inn Chevrolet of Carroll is Chevrolet certified. Service details and online scheduling are on the [service page]({C}/service), and the store also has a [collision shop]({C}/collision-shop).
"""),
            ("Can I trade in or sell my car at the Carroll Chevy dealer?", f"""
Yes. Trade appraisals are walk-in, with no appointment needed. An online trade estimate is on the [trade page]({C}/trade.aspx), and selling without buying is covered on the [We Buy Cars]({C}/we-buy-cars.html) page.
"""),
            ("Can I get Chevy financing in Carroll?", f"""
Yes. Motor Inn works with a network of lenders on new and used vehicles. Details are on the [financing page]({C}/finance.aspx), and online pre-approval is on the [pre-approval page]({C}/preapproved.aspx).
"""),
            ("Is there a Chevy dealer near me?", f"""
If you live in or around Carroll, including drivers coming from {"Denison, Audubon, Jefferson, Storm Lake and Sac City"}, Motor Inn Chevrolet of Carroll is on Le Clark Road just off US Highway 30. Call (712) 792-5000 before you drive over, and the team will confirm the vehicle you want is available.
"""),
        ],
        "faq": [
            ("Where is the Chevy dealer in Carroll, Iowa?",
             "Motor Inn Chevrolet of Carroll is at 1526 Le Clark Road, Carroll, IA 51401, just off West US Highway 30. It sells new Chevrolet trucks and SUVs and used vehicles, and it has a Chevrolet certified service department. The phone number is (712) 792-5000."),
            ("Is Motor Inn of Carroll a Chevrolet dealer?",
             "Yes. Motor Inn of Carroll, also called Motor Inn Chevrolet of Carroll, is the Chevrolet dealership of Motor Inn Auto Group in Carroll, Iowa. It is located at 1526 Le Clark Road and shares that address with Motor Inn Toyota of Carroll."),
            ("Does the Chevy dealer in Carroll, Iowa, do Chevrolet service?",
             "Yes. Motor Inn Chevrolet of Carroll has a Chevrolet certified service department at 1526 Le Clark Road in Carroll, Iowa. Service can be scheduled online at motorinnofcarroll.com or by calling (712) 792-5000."),
            ("Can I trade in my car at the Carroll Chevy dealer without an appointment?",
             "Yes. Motor Inn Chevrolet of Carroll appraises trade-ins on a walk-in basis, so no appointment is needed. Shoppers can also start a trade value online at motorinnofcarroll.com before they visit."),
            ("Is there a Chevy dealer and a Toyota dealer at the same place in Carroll?",
             "Yes. Motor Inn Chevrolet of Carroll and Motor Inn Toyota of Carroll share one address at 1526 Le Clark Road in Carroll, Iowa. Shoppers can compare new Chevrolet and Toyota vehicles in the same visit."),
        ],
        "links": [
            ("Get hours and directions", f"{C}/hours.aspx", "same site"),
            ("About Motor Inn of Carroll", f"{C}/aboutus.aspx", "same site"),
            ("new Chevrolet inventory search", f"{C}/searchnew.aspx", "same site"),
            ("Colorado", f"{C}/2026-chevrolet-colorado", "same site"),
            ("Silverado 1500", f"{C}/2026-chevrolet-silverado-ld", "same site"),
            ("Silverado HD", f"{C}/2026-chevrolet-silverado-hd", "same site"),
            ("Silverado EV", f"{C}/2026-chevrolet-silverado-ev", "same site"),
            ("Trax", f"{C}/2026-chevrolet-trax", "same site"),
            ("Trailblazer", f"{C}/2026-chevrolet-trailblazer", "same site"),
            ("Equinox", f"{C}/2026-chevrolet-equinox", "same site"),
            ("Blazer", f"{C}/2026-chevrolet-blazer", "same site"),
            ("Traverse", f"{C}/2026-chevrolet-traverse", "same site"),
            ("Tahoe", f"{C}/2026-chevrolet-tahoe", "same site"),
            ("Suburban", f"{C}/2026-chevrolet-suburban", "same site"),
            ("Equinox EV", f"{C}/2026-chevrolet-equinox-ev", "same site"),
            ("Blazer EV", f"{C}/2026-chevrolet-blazer-ev", "same site"),
            ("quote page", f"{C}/quote.aspx", "same site"),
            ("service page", f"{C}/service", "same site"),
            ("collision shop", f"{C}/collision-shop", "same site"),
            ("trade page", f"{C}/trade.aspx", "same site"),
            ("We Buy Cars", f"{C}/we-buy-cars.html", "same site"),
            ("pre-approval page", f"{C}/preapproved.aspx", "same site"),
            ("financing page", f"{C}/finance.aspx", "same site"),
        ],
        "post_links": [
            "Add a link to this page from motorinnofcarroll.com/aboutus.aspx and the Chevy homepage, so it isn't orphaned.",
            "Link this page from the new chevy-suvs, chevy-blazer and chevy-trucks pages, and the reverse, once all four are live.",
            "Link from motorinnautogroup.com/contactus.aspx ('Chevy dealer in Carroll').",
        ],
        "sources": CHEVY_SOURCES + ["Service-area towns: brain/VOICE-DNA.md and Toyota-site sitemap town pages (used here as places shoppers drive in from, not as store locations)."],
        "routing": """
Chevrolet site (motorinnofcarroll.com). Every query here is Chevrolet-specific dealer or store-name intent, so Spencer's rule sends it to the Chevy store's site.

**This is the biggest clean gap in the export:** about 13,600 impressions at an average position near 24, with almost no clicks. It includes 6,400+ impressions on store-name queries such as "motor inn of carroll l.l.c. near me/chevy/chevrolet", where Google doesn't connect the store's name to a page. There's no existing URL to refresh: the Chevy sitemap has no dealer-location page.

**Caveat on the headline number:** the three "motor inn of carroll l.l.c." rows (6,447 impressions) have zero clicks in 12 months. They also appear in the cached 28-day window: the 28-day cache to 2026-10-16 shows 242 to 278 impressions each on the group property, plus 93 to 168 on the Toyota property, where the Toyota homepage ranks around 14 to 17. That fits a store-name search Google can't resolve, but automated lookups can't be ruled out. Without those rows, this cluster is still about 7,200 impressions at a position near 24, so it stays P1.
""",
        "notes": [
            "The store's legal name ('Motor Inn of Carroll L.L.C.') appears only in searcher queries, never in repo facts, so the copy uses 'Motor Inn of Carroll' and 'Motor Inn Chevrolet of Carroll', which both appear on the live sites.",
            "brain/STATE.md (2026-09-23) notes that the Chevy store has no distinct GBP listing surfaced by name. This page helps, but a Chevy GBP entity fix would help more.",
            "Spirit Lake, Estherville, Algona and Monona Chevy queries are left out on purpose (see the plan's gaps section).",
            OEM_NOTE,
        ],
        "ai_summary": "Motor Inn Chevrolet of Carroll (also known as Motor Inn of Carroll) is a Chevrolet dealer at 1526 Le Clark Road, Carroll, Iowa 51401, phone (712) 792-5000. It is part of Motor Inn Auto Group and shares its address with Motor Inn Toyota of Carroll. It sells new Chevrolet trucks, SUVs and EVs and used vehicles, appraises trade-ins without an appointment, arranges financing through a lender network, and has a Chevrolet certified service department.",
    },
    {
        "slug": "chevy-suvs-for-sale-carroll-iowa",
        "store": "chevy",
        "path": "/chevy-suvs-for-sale-carroll-iowa",
        "status": "NEW page (the Chevy site has model pages but no SUV shopping page).",
        "tier": "ready-now",
        "queries": [
            "carroll iowa chevy suburban", "chevy suv near me", "chevy traverse near me", "chevy equinox near me",
            "equinox lease near me", "chevy suv for sale", "chevrolet trax near me", "tahoe deals near me",
            "best chevy suv for families", "chevy tahoe prices near me", "tahoe for sale", "chevrolet traverse for sale",
            "chevy tahoe for sale", "suburban for sale", "chevy suburban for sale near me",
        ],
        "h1": "Chevy SUVs for Sale in Carroll, Iowa",
        "title": "Chevy SUVs for Sale in Carroll, IA | Motor Inn of Carroll",
        "meta": "Shop Chevy SUVs in Carroll, Iowa: Trax, Trailblazer, Equinox, Blazer, Traverse, Tahoe, Suburban and EVs at Motor Inn Chevrolet of Carroll. (712) 792-5000.",
        "og_title": "Chevy SUVs for Sale in Carroll, Iowa",
        "og_desc": "Every Chevrolet SUV, from Trax to Suburban, at Motor Inn Chevrolet of Carroll, 1526 Le Clark Road.",
        "cta": "Search new Chevy SUVs or call (712) 792-5000.",
        "intro": f"""
Motor Inn Chevrolet of Carroll sells the full Chevrolet SUV lineup at 1526 Le Clark Road in Carroll, Iowa: Trax, Trailblazer, Equinox, Blazer, Traverse, Tahoe and Suburban, plus the electric Equinox EV and Blazer EV. The [new inventory search]({C}/searchnew.aspx) shows which SUVs are on the lot today.
""",
        "sections": [
            ("Which Chevy SUVs can I buy near me in Carroll?", f"""
Motor Inn Chevrolet of Carroll sells Chevy SUVs from the small Trax up to the full-size Suburban, including two electric models. From smallest to largest:

- **Small SUVs:** [Trax]({C}/2026-chevrolet-trax), [Trailblazer]({C}/2026-chevrolet-trailblazer)
- **Two-row SUVs:** [Equinox]({C}/2026-chevrolet-equinox), [Blazer]({C}/2026-chevrolet-blazer)
- **Three-row SUVs:** [Traverse]({C}/2026-chevrolet-traverse), [Tahoe]({C}/2026-chevrolet-tahoe), [Suburban]({C}/2026-chevrolet-suburban)
- **Electric SUVs:** [Equinox EV]({C}/2026-chevrolet-equinox-ev), [Blazer EV]({C}/2026-chevrolet-blazer-ev)
"""),
            ("Which Chevy SUV is best for families?", f"""
If you need a third row, look at the Traverse, Tahoe and Suburban. Tahoe and Suburban are Chevy's full-size SUVs, and the Suburban is the longer of the two. If two rows are enough, compare the Equinox and Blazer.

Our group site has a longer guide: [best Chevrolet SUVs for families]({G}/best-chevrolet-suvs-for-families).
"""),
            ("Where can I find a Chevy Suburban in Carroll, Iowa?", f"""
At Motor Inn Chevrolet of Carroll, 1526 Le Clark Road. [Search Suburban inventory]({C}/searchnew.aspx?Model=Suburban) or [see the Suburban model page]({C}/2026-chevrolet-suburban). If the one you want isn't on the lot, ask the team about finding or ordering one.
"""),
            ("How do I get Chevy SUV lease deals near me?", f"""
Lease and finance terms on the Equinox, Tahoe and other Chevy SUVs come from factory programs that change, so we don't post numbers here. Call (712) 792-5000, and the sales team will give you today's options.
"""),
            ("Can I buy a used Chevy SUV in Carroll?", f"""
Yes, when one is on the lot. The [used inventory search]({C}/searchused.aspx) covers used Chevy SUVs and other brands, and the [under $20K page]({C}/under-20k.html) filters by price. Trade appraisals are walk-in, with no appointment needed.
"""),
        ],
        "faq": [
            ("Where can I buy a Chevy SUV in Carroll, Iowa?",
             "Motor Inn Chevrolet of Carroll sells new Chevrolet SUVs at 1526 Le Clark Road in Carroll, Iowa. The lineup includes the Trax, Trailblazer, Equinox, Blazer, Traverse, Tahoe and Suburban, plus the electric Equinox EV and Blazer EV. Call (712) 792-5000 to check what's on the lot."),
            ("What is the best Chevy SUV for families?",
             "For families that need a third row, the Chevrolet options are the Traverse, Tahoe and Suburban. The Tahoe and Suburban are Chevrolet's full-size SUVs, and the Suburban is the longer of the two. Motor Inn Chevrolet of Carroll in Carroll, Iowa, sells all three and can set up test drives."),
            ("Where can I find a Chevy Suburban in Carroll, Iowa?",
             "Motor Inn Chevrolet of Carroll sells the new Chevrolet Suburban at 1526 Le Clark Road in Carroll, Iowa. Inventory changes, so check the new-vehicle search at motorinnofcarroll.com or call (712) 792-5000 to confirm availability."),
            ("How do I find Chevy Equinox or Tahoe lease deals near Carroll?",
             "Motor Inn Chevrolet of Carroll in Carroll, Iowa, gives current Equinox and Tahoe lease and finance options by phone at (712) 792-5000. Lease terms come from factory programs that change, so this page does not quote a lease price."),
        ],
        "links": [
            ("new inventory search", f"{C}/searchnew.aspx", "same site"),
            ("Trax", f"{C}/2026-chevrolet-trax", "same site"),
            ("Trailblazer", f"{C}/2026-chevrolet-trailblazer", "same site"),
            ("Equinox", f"{C}/2026-chevrolet-equinox", "same site"),
            ("Blazer", f"{C}/2026-chevrolet-blazer", "same site"),
            ("Traverse", f"{C}/2026-chevrolet-traverse", "same site"),
            ("Tahoe", f"{C}/2026-chevrolet-tahoe", "same site"),
            ("Suburban", f"{C}/2026-chevrolet-suburban", "same site"),
            ("Equinox EV", f"{C}/2026-chevrolet-equinox-ev", "same site"),
            ("Blazer EV", f"{C}/2026-chevrolet-blazer-ev", "same site"),
            ("best Chevrolet SUVs for families", f"{G}/best-chevrolet-suvs-for-families", "cross-site (group)"),
            ("Search Suburban inventory", f"{C}/searchnew.aspx?Model=Suburban", "same site (filtered search)"),
            ("used inventory search", f"{C}/searchused.aspx", "same site"),
            ("under $20K page", f"{C}/under-20k.html", "same site"),
        ],
        "post_links": [
            "Link to /chevy-blazer-for-sale-carroll-iowa from the Blazer bullet and to /chevy-dealer-carroll-iowa from the intro once both are live.",
        ],
        "sources": CHEVY_SOURCES,
        "routing": """
Chevrolet site. These are new-Chevrolet model and body-style shopping queries.

Blazer queries go to their own page (chevy-blazer-for-sale-carroll-iowa) because together they are a 2,700-impression cluster. "carroll iowa chevy suburban" (1,518 impressions, position 25.3) is the largest row here.
""",
        "notes": [LEASE_NOTE, OEM_NOTE, FILTER_NOTE,
                  "The 'best chevy suv for families' row is at position 92 and the group site already has /best-chevrolet-suvs-for-families, so this page links there instead of competing with it."],
        "ai_summary": "Motor Inn Chevrolet of Carroll, 1526 Le Clark Road, Carroll, Iowa 51401 (phone (712) 792-5000), sells the full Chevrolet SUV lineup: Trax, Trailblazer, Equinox, Blazer, Traverse, Tahoe, Suburban, Equinox EV and Blazer EV. The three-row models are Traverse, Tahoe and Suburban. Current lease and finance options are given by phone.",
    },
    {
        "slug": "chevy-blazer-for-sale-carroll-iowa",
        "store": "chevy",
        "path": "/chevy-blazer-for-sale-carroll-iowa",
        "status": "NEW page (the Chevy site has year-model pages /2026-chevrolet-blazer and /2026-chevrolet-blazer-ev but no shopping or 'for sale' page).",
        "tier": "ready-now",
        "queries": [
            "chevy blazer for sale near me", "chevy blazer ev near me", "blazer suv for sale",
            "chevy blazer lease prices near me", "chevy blazers for sale near me", "chevy blazer for sale",
        ],
        "h1": "Chevy Blazer for Sale Near Carroll, Iowa",
        "title": "Chevy Blazer for Sale in Carroll, IA | Motor Inn of Carroll",
        "meta": "Find a Chevy Blazer or Blazer EV for sale at Motor Inn Chevrolet of Carroll, 1526 Le Clark Road, Carroll, Iowa. Test drives and offers: (712) 792-5000.",
        "og_title": "Chevy Blazer and Blazer EV for Sale Near Carroll, Iowa",
        "og_desc": "Shop the Chevrolet Blazer and the all-electric Blazer EV at Motor Inn Chevrolet of Carroll.",
        "cta": "Search Blazer inventory or call (712) 792-5000.",
        "intro": f"""
Motor Inn Chevrolet of Carroll sells the Chevrolet Blazer and the all-electric Blazer EV at 1526 Le Clark Road in Carroll, Iowa. [Search Blazer inventory]({C}/searchnew.aspx?Model=Blazer) to see what's on the lot, or call (712) 792-5000 to set up a test drive.
""",
        "sections": [
            ("Where can I find a Chevy Blazer for sale near me?", f"""
At Motor Inn Chevrolet of Carroll, just off West US Highway 30 in Carroll. Inventory changes, so check the live searches:

- [New Blazer inventory]({C}/searchnew.aspx?Model=Blazer)
- [New Blazer EV inventory]({C}/searchnew.aspx?Model=Blazer%20EV)
- [Used inventory]({C}/searchused.aspx), which sometimes includes a used Blazer
"""),
            ("What's the difference between the Blazer and the Blazer EV?", f"""
The Blazer runs on gas. The Blazer EV is all-electric. Both are two-row Chevrolet SUVs. Compare them on the model pages: [Blazer]({C}/2026-chevrolet-blazer) and [Blazer EV]({C}/2026-chevrolet-blazer-ev). EV owners can read about the [EV protection plan]({C}/ev-protection-plan-chevrolet).
"""),
            ("How do I get Chevy Blazer lease prices near me?", f"""
Lease and finance terms on the Blazer and Blazer EV come from factory programs that change, so we don't post numbers here. Call (712) 792-5000, and the sales team will give you today's options. Online pre-approval is on the [pre-approval page]({C}/preapproved.aspx).
"""),
            ("Can I test drive a Blazer in Carroll?", f"""
Yes. Call (712) 792-5000, and the team will confirm which Blazer or Blazer EV is available and set a time with you. Test-drive details are also on the [test drive page]({C}/testdrive.aspx).
"""),
            ("Can I trade in my car toward a Blazer?", f"""
Yes. Trade appraisals are walk-in, with no appointment needed. An online trade estimate is on the [trade page]({C}/trade.aspx).
"""),
        ],
        "faq": [
            ("Where can I find a Chevy Blazer for sale near Carroll, Iowa?",
             "Motor Inn Chevrolet of Carroll sells the new Chevrolet Blazer and Blazer EV at 1526 Le Clark Road in Carroll, Iowa. Inventory changes, so the Blazer search on motorinnofcarroll.com shows what is on the lot today. The phone number is (712) 792-5000."),
            ("What is the difference between the Chevy Blazer and the Blazer EV?",
             "The Chevrolet Blazer is a gas-powered two-row SUV, and the Blazer EV is an all-electric two-row SUV. Motor Inn Chevrolet of Carroll in Carroll, Iowa, sells both and can set up a test drive of either one."),
            ("How do I get Chevy Blazer lease prices near me?",
             "Motor Inn Chevrolet of Carroll in Carroll, Iowa, gives current Blazer and Blazer EV lease options by phone at (712) 792-5000. Lease prices come from factory programs that change, so this page does not quote a lease price."),
            ("Can I test drive a Chevy Blazer in Carroll, Iowa?",
             "Yes. Motor Inn Chevrolet of Carroll schedules Blazer and Blazer EV test drives at 1526 Le Clark Road in Carroll, Iowa. Call (712) 792-5000, and the team will confirm which Blazer is available and set a time."),
        ],
        "links": [
            ("Search Blazer inventory", f"{C}/searchnew.aspx?Model=Blazer", "same site (filtered search)"),
            ("New Blazer EV inventory", f"{C}/searchnew.aspx?Model=Blazer%20EV", "same site (filtered search)"),
            ("Used inventory", f"{C}/searchused.aspx", "same site"),
            ("Blazer", f"{C}/2026-chevrolet-blazer", "same site"),
            ("Blazer EV", f"{C}/2026-chevrolet-blazer-ev", "same site"),
            ("EV protection plan", f"{C}/ev-protection-plan-chevrolet", "same site"),
            ("pre-approval page", f"{C}/preapproved.aspx", "same site"),
            ("test drive page", f"{C}/testdrive.aspx", "same site"),
            ("trade page", f"{C}/trade.aspx", "same site"),
        ],
        "post_links": ["Link from /chevy-suvs-for-sale-carroll-iowa (Blazer bullet) and /chevy-dealer-carroll-iowa once live."],
        "sources": CHEVY_SOURCES,
        "routing": """
Chevrolet site. These are new-Chevrolet single-model shopping queries.

This model gets its own page because it is the largest single-model cluster in the export (about 2,700 impressions). "chevy blazer for sale near me" already shows at position 2.0 with zero clicks, which suggests the current landing page (/Contactus/Carroll on the group site) doesn't match what Blazer shoppers want.
""",
        "notes": [LEASE_NOTE, OEM_NOTE, FILTER_NOTE + " The Blazer EV filter value ('Blazer EV') is the most likely to need a fix."],
        "ai_summary": "Motor Inn Chevrolet of Carroll, 1526 Le Clark Road, Carroll, Iowa 51401 (phone (712) 792-5000), sells the gas-powered Chevrolet Blazer and the all-electric Blazer EV. Current lease options are given by phone, and test drives can be requested online or by phone.",
    },
    {
        "slug": "chevy-trucks-for-sale-carroll-iowa",
        "store": "chevy",
        "path": "/chevy-trucks-for-sale-carroll-iowa",
        "status": "NEW page on the Chevy site. Supersedes the routing of the unpublished content/ready-design/chevy-trucks-carroll-iowa.html draft, which canonicalizes to the group site.",
        "tier": "ready-now",
        "queries": [
            "chevrolet truck for sale", "chevy truck for sale near me", "silverado lease deals near me",
            "chevy colorado for sale near me",
            "chevy 2500 for sale", "chevy colorado for sale", "chevrolet 2500 for sale",
            "silverado zr2 for sale", "chevy trucks",
        ],
        "h1": "Chevy Trucks for Sale in Carroll, Iowa",
        "title": "Chevy Trucks for Sale in Carroll, IA | Motor Inn of Carroll",
        "meta": "Chevy trucks for sale in Carroll, Iowa: Colorado, Silverado 1500, Silverado HD and Silverado EV at Motor Inn Chevrolet of Carroll. Call (712) 792-5000.",
        "og_title": "Chevy Trucks for Sale in Carroll, Iowa",
        "og_desc": "Colorado, Silverado 1500, Silverado HD and Silverado EV, new and used, at Motor Inn Chevrolet of Carroll.",
        "cta": "Search Chevy trucks or call (712) 792-5000.",
        "intro": f"""
Motor Inn Chevrolet of Carroll sells new Chevrolet trucks at 1526 Le Clark Road in Carroll, Iowa: the Colorado, Silverado 1500, Silverado HD and Silverado EV. Used trucks are on the same lot. [Search new Chevy inventory]({C}/searchnew.aspx) to see what's available today.
""",
        "sections": [
            ("Where can I find a Chevy truck for sale near me?", f"""
At Motor Inn Chevrolet of Carroll, just off West US Highway 30. Use the live searches:

- [New Silverado 1500]({C}/searchnew.aspx?Model=Silverado%201500)
- [New Colorado]({C}/searchnew.aspx?Model=Colorado)
- [All new Chevrolet inventory]({C}/searchnew.aspx)
- [Used trucks and other used vehicles]({C}/searchused.aspx)
"""),
            ("Which Chevy truck should I buy?", f"""
Pick the Colorado for a midsize truck, the Silverado 1500 for full-size everyday work, the Silverado HD for heavy towing, or the Silverado EV if you want electric:

- **[Colorado]({C}/2026-chevrolet-colorado):** Chevy's midsize pickup, easier to park and handle around town.
- **[Silverado 1500]({C}/2026-chevrolet-silverado-ld):** the full-size light-duty pickup for everyday hauling and towing.
- **[Silverado HD]({C}/2026-chevrolet-silverado-hd):** the 2500HD and 3500HD heavy-duty pickups for the heaviest towing and farm work.
- **[Silverado EV]({C}/2026-chevrolet-silverado-ev):** the all-electric full-size pickup.

Not sure whether you need heavy duty? Read [heavy-duty vs. light-duty trucks]({G}/blog/heavy-duty-vs-light-duty-trucks). Comparing brands? See [Silverado 1500 vs. Ford F-150]({C}/silverado-1500-vs-ford-f-150) and [Silverado 1500 vs. Ram 1500]({C}/silverado-1500-vs-ram-1500).
"""),
            ("Is a Chevy 2500 for sale in Carroll?", f"""
The Silverado 2500HD is part of the [Silverado HD lineup]({C}/2026-chevrolet-silverado-hd). [Search HD inventory]({C}/searchnew.aspx?Model=Silverado%202500%20HD), or call (712) 792-5000 and ask about a specific configuration or trim, such as a ZR2 or a particular bed and cab.
"""),
            ("How do I get Silverado lease deals near me?", f"""
Lease and finance terms on the Silverado come from factory programs that change, so we don't post numbers here. Call (712) 792-5000, and the sales team will give you today's options. Online pre-approval is on the [pre-approval page]({C}/preapproved.aspx).
"""),
            ("Can I buy a used Chevy Silverado or Colorado in Carroll?", f"""
Yes, when one is on the lot. The [used inventory search]({C}/searchused.aspx) and the group's [used trucks page]({G}/used-trucks) show what's available. Trade appraisals are walk-in, with no appointment needed, and an online estimate is on the [trade page]({C}/trade.aspx).
"""),
        ],
        "faq": [
            ("Where can I find a Chevy truck for sale near Carroll, Iowa?",
             "Motor Inn Chevrolet of Carroll sells new Chevrolet Colorado, Silverado 1500, Silverado HD and Silverado EV pickups at 1526 Le Clark Road in Carroll, Iowa. Used trucks are sold on the same lot. Call (712) 792-5000 or check the live inventory search at motorinnofcarroll.com."),
            ("Is a Chevy 2500 for sale in Carroll, Iowa?",
             "Motor Inn Chevrolet of Carroll sells the Chevrolet Silverado 2500HD, part of Chevrolet's Silverado HD heavy-duty pickup line, at 1526 Le Clark Road in Carroll, Iowa. Inventory changes, so call (712) 792-5000 to ask about a specific cab, bed or trim."),
            ("How do I get Silverado lease deals near me?",
             "Motor Inn Chevrolet of Carroll in Carroll, Iowa, gives current Silverado lease and finance options by phone at (712) 792-5000. Lease terms come from factory programs that change, so this page does not quote a lease price."),
        ],
        "links": [
            ("Search new Chevy inventory", f"{C}/searchnew.aspx", "same site"),
            ("New Silverado 1500", f"{C}/searchnew.aspx?Model=Silverado%201500", "same site (filtered search)"),
            ("New Colorado", f"{C}/searchnew.aspx?Model=Colorado", "same site (filtered search)"),
            ("Used trucks and other used vehicles", f"{C}/searchused.aspx", "same site"),
            ("Colorado", f"{C}/2026-chevrolet-colorado", "same site"),
            ("Silverado 1500", f"{C}/2026-chevrolet-silverado-ld", "same site"),
            ("Silverado HD", f"{C}/2026-chevrolet-silverado-hd", "same site"),
            ("Silverado EV", f"{C}/2026-chevrolet-silverado-ev", "same site"),
            ("heavy-duty vs. light-duty trucks", f"{G}/blog/heavy-duty-vs-light-duty-trucks", "cross-site (group)"),
            ("Silverado 1500 vs. Ford F-150", f"{C}/silverado-1500-vs-ford-f-150", "same site"),
            ("Silverado 1500 vs. Ram 1500", f"{C}/silverado-1500-vs-ram-1500", "same site"),
            ("Search HD inventory", f"{C}/searchnew.aspx?Model=Silverado%202500%20HD", "same site (filtered search)"),
            ("pre-approval page", f"{C}/preapproved.aspx", "same site"),
            ("used trucks page", f"{G}/used-trucks", "cross-site (group)"),
            ("trade page", f"{C}/trade.aspx", "same site"),
        ],
        "post_links": ["Link from /chevy-dealer-carroll-iowa (Trucks bullet) once live."],
        "sources": CHEVY_SOURCES + ["Group blog /blog/heavy-duty-vs-light-duty-trucks and /used-trucks: group sitemap snapshot."],
        "routing": """
Chevrolet site. These are new-Chevrolet truck shopping queries. Brandless and used truck queries ("trucks for sale near me" 52, "used chevy silverado for sale" 35, "used chevy colorado for sale" 19) are NOT targeted here. Under the routing rule they belong to the group site's existing /used-trucks page. The used section on this page is a support cross-link only.

**Conflict with an earlier draft:** content/ready-design/chevy-trucks-carroll-iowa.html targets the same intent with a group-site canonical. Under the 2026-11-23 routing rule, brand-specific intent goes to the brand site. Recommendation: don't publish the group-site draft too, or the two pages will compete for the same queries.
""",
        "notes": [LEASE_NOTE, OEM_NOTE, FILTER_NOTE + " The HD filter uses the live model name 'Silverado 2500 HD' (with a space), which Codex confirmed returns results on 2026-11-23.",
                  "'ZR2' is used only as an example of a trim the shopper can ask about. No claim is made about stock."],
        "ai_summary": "Motor Inn Chevrolet of Carroll, 1526 Le Clark Road, Carroll, Iowa 51401 (phone (712) 792-5000), sells new Chevrolet Colorado, Silverado 1500, Silverado HD (2500HD and 3500HD) and Silverado EV pickups, plus used trucks. Current Silverado lease and finance options are given by phone.",
    },
]
