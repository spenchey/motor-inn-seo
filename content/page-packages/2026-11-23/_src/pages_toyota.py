"""Toyota-site pages (www.motorinntoyotaofcarroll.com)."""

G = "https://www.motorinnautogroup.com"
T = "https://www.motorinntoyotaofcarroll.com"

TOYOTA_SOURCES = [
    "Address, store name: Toyota contact page (.firecrawl/motorinntoyotaofcarroll.com-contactus.aspx.md), 'Motor Inn Toyota Of Carroll, 1526 Le Clark Road, Carroll, IA 51401'.",
    "Phone (712) 792-5000: required on customer-facing Toyota copy (brief + brain/STATE.md ruling 2026-11-02). The 712-513-xxxx numbers on the Toyota contact page look like tracking numbers and are not printed. 522-2526 is never used.",
    "'Just off West US Highway 30': group homepage snippet (.firecrawl/nap-audit/20261029/_ap_uest.json).",
    "Walk-in trade appraisal, lender-network financing, hours: content/ready-design-OWNER-NOTES.md (2026-10-23).",
    "Model, CPO, service and town pages: Toyota sitemap snapshot brain/research/live-https_www_motorinntoyotaofcarroll_com_sitemap_xml.html (2026-11-05).",
]
OEM_NOTE = "Vehicle descriptions are kept qualitative (midsize vs full-size, SUV vs minivan) with no specs. 'i-FORCE MAX' (name only, no powertrain type claimed) comes from the live Tundra offer URL on both sites. Spot-check the wording against toyota.com before handoff."
FILTER_NOTE = "Model-filtered search links use the DealerOn pattern searchnew.aspx?Model=<Model>. Click-test each filter before handoff."

PAGES = [
    {
        "slug": "toyota-dealers-in-iowa",
        "store": "toyota",
        "path": "/toyota-dealers-in-iowa",
        "status": "NEW page. The live Toyota site already has /toyota-dealer-carroll-iowa and /toyota-dealer-near-carroll-ia-51401-…/, which target Carroll-local intent. This page targets the statewide and 'near me' wording instead, and it links to the town pages rather than repeating them.",
        "tier": "ready-now",
        "queries": [
            "toyota dealers in iowa", "toyota dealerships in iowa", "iowa toyota dealers",
            "toyota dealership near me", "toyota dealer near me", "toyota service near me", "toyota iowa",
            "toyota dealers iowa", "toyota dealer iowa", "toyota dealership iowa", "toyota dealers near me",
            "toyota near me", "toyota dealerships iowa", "toyota dealership in iowa", "toyota dealerships near me",
            "toyota in iowa", "toyota dealer in iowa", "iowa toyota dealership", "toyota iowa dealers",
        ],
        "h1": "Toyota Dealer in West-Central Iowa: Motor Inn Toyota of Carroll",
        "title": "Toyota Dealer in Iowa | Motor Inn Toyota of Carroll",
        "meta": "Looking for a Toyota dealer in Iowa? Motor Inn Toyota of Carroll is at 1526 Le Clark Road, Carroll, off US 30. New, Certified, service. (712) 792-5000.",
        "og_title": "Toyota Dealer in West-Central Iowa | Motor Inn Toyota of Carroll",
        "og_desc": "New Toyotas, Toyota Certified Pre-Owned vehicles and Toyota service at 1526 Le Clark Road in Carroll, Iowa.",
        "cta": "Call Motor Inn Toyota of Carroll at (712) 792-5000.",
        "intro": f"""
Motor Inn Toyota of Carroll is a Toyota dealer in west-central Iowa, at 1526 Le Clark Road in Carroll, just off West US Highway 30. It sells new Toyotas and Certified Pre-Owned Toyotas, and it services Toyotas at that one address. Call (712) 792-5000.
""",
        "sections": [
            ("Where are Toyota dealers in Iowa?", f"""
Toyota dealers are spread across Iowa. In west-central Iowa, Motor Inn Toyota of Carroll sits on Le Clark Road in Carroll, just off US Highway 30. Shoppers from across the area come here for new Toyotas, Certified Pre-Owned vehicles and service.
"""),
            ("Is there a Toyota dealership near me?", f"""
If you live in or around Carroll, Motor Inn Toyota of Carroll is your local Toyota dealership. We also have pages for nearby towns:

- [Toyota dealer near Denison]({T}/toyota-dealer-near-denison-ia-51442-motor-inn-toyota-of-carroll/)
- [Toyota dealer near Audubon]({T}/toyota-dealer-near-audubon-ia-50025-motor-inn-toyota-of-carroll/)
- [Toyota dealer near Jefferson]({T}/toyota-dealer-near-jefferson-ia-50129-motor-inn-toyota-of-carroll/)

Call (712) 792-5000 before you drive over, and the team will confirm the vehicle you want is available.
"""),
            ("What can I buy at a Toyota dealer in Carroll, Iowa?", f"""
- [New Toyota inventory]({T}/searchnew.aspx): cars, trucks, SUVs and minivans
- [Toyota hybrids and electrified vehicles]({T}/electrified)
- [Toyota Certified Pre-Owned]({T}/certified-pre-owned.html)
- [Used inventory]({T}/searchused.aspx) of other brands too
- [Current Toyota offers]({T}/newspecials.html) and [manufacturer incentives]({T}/manufacturer-incentives.aspx)
"""),
            ("Where can I get Toyota service near me?", f"""
The [Toyota service center]({T}/service-center.html) at Motor Inn Toyota of Carroll is at the same Le Clark Road address. Service appointments can be made by phone at (712) 792-5000 or on the [service scheduling page]({T}/serviceappmt.aspx). For more, see [where to service a Toyota in Carroll]({G}/where-to-service-toyota-carroll-iowa).
"""),
            ("Can I trade in and finance at the Carroll Toyota dealer?", f"""
Yes. Trade appraisals are walk-in, with no appointment needed, and an online trade estimate is on the [trade page]({T}/trade.aspx). Motor Inn works with a network of lenders, and online pre-approval is on the [pre-approval page]({T}/preapproved.aspx).
"""),
        ],
        "faq": [
            ("Where is a Toyota dealer in west-central Iowa?",
             "Motor Inn Toyota of Carroll is a Toyota dealer at 1526 Le Clark Road in Carroll, Iowa, just off West US Highway 30. It sells new and Certified Pre-Owned Toyotas and services Toyota vehicles. The phone number is (712) 792-5000."),
            ("Is there a Toyota dealership in Carroll, Iowa?",
             "Yes. Motor Inn Toyota of Carroll is a Toyota dealership at 1526 Le Clark Road, Carroll, IA 51401. It shares that address with Motor Inn Chevrolet of Carroll, and both are part of Motor Inn Auto Group."),
            ("Where can I get Toyota service near Carroll, Iowa?",
             "Motor Inn Toyota of Carroll has a Toyota service center at 1526 Le Clark Road in Carroll, Iowa. Service can be scheduled online at motorinntoyotaofcarroll.com or by calling (712) 792-5000."),
            ("Does Motor Inn Toyota of Carroll sell Certified Pre-Owned Toyotas?",
             "Yes. Motor Inn Toyota of Carroll in Carroll, Iowa, sells Toyota Certified Pre-Owned vehicles as well as new Toyotas and used vehicles of other brands. Current certified inventory is listed on motorinntoyotaofcarroll.com."),
            ("Can I trade in my car at the Toyota dealer in Carroll without an appointment?",
             "Yes. Motor Inn Toyota of Carroll appraises trade-ins on a walk-in basis, so no appointment is needed. Shoppers can also start a trade value online at motorinntoyotaofcarroll.com before they visit."),
        ],
        "links": [
            ("Toyota dealer near Denison", f"{T}/toyota-dealer-near-denison-ia-51442-motor-inn-toyota-of-carroll/", "same site"),
            ("Toyota dealer near Audubon", f"{T}/toyota-dealer-near-audubon-ia-50025-motor-inn-toyota-of-carroll/", "same site"),
            ("Toyota dealer near Jefferson", f"{T}/toyota-dealer-near-jefferson-ia-50129-motor-inn-toyota-of-carroll/", "same site"),
            ("New Toyota inventory", f"{T}/searchnew.aspx", "same site"),
            ("Toyota hybrids and electrified vehicles", f"{T}/electrified", "same site"),
            ("Toyota Certified Pre-Owned", f"{T}/certified-pre-owned.html", "same site"),
            ("Used inventory", f"{T}/searchused.aspx", "same site"),
            ("Current Toyota offers", f"{T}/newspecials.html", "same site"),
            ("manufacturer incentives", f"{T}/manufacturer-incentives.aspx", "same site"),
            ("Toyota service center", f"{T}/service-center.html", "same site"),
            ("service scheduling page", f"{T}/serviceappmt.aspx", "same site"),
            ("where to service a Toyota in Carroll", f"{G}/where-to-service-toyota-carroll-iowa", "cross-site (group)"),
            ("trade page", f"{T}/trade.aspx", "same site"),
            ("pre-approval page", f"{T}/preapproved.aspx", "same site"),
        ],
        "post_links": [
            "Link this page from the Toyota homepage or /aboutus.aspx, and from motorinnautogroup.com/contactus.aspx.",
            "Link /toyota-tacoma-tundra-for-sale-carroll-iowa and /toyota-sequoia-sienna-for-sale-carroll-iowa from the 'What can I buy' list once they are live.",
        ],
        "sources": TOYOTA_SOURCES,
        "routing": """
Toyota site. The intent is to find a new Toyota dealer, so it routes to the Toyota store's site.

**Cannibalization guard:** the high-volume Carroll-Toyota queries ("toyota carroll iowa" 1,202, "carroll toyota" 864, "motor inn toyota of carroll" 683) already rank at positions 1.6 to 5.6 with 250-click rows, mostly through /Contactus/Carroll. They are left out on purpose. This page targets only the Iowa-wide and 'near me' wording, which sits at positions 3 to 7 with low CTR. The page names no competing dealers and makes no 'closest' or 'only' claim.
""",
        "notes": [
            "'Toyota dealerships in nebraska' (55 impressions) is out of market and not targeted.",
            "'where can i find toyota service centers in iowa with weekend hours?' (55 impressions) is NOT answered with weekend service hours, because the repo has no source for service hours. Service hours are left to the hours page.",
            "The page makes no statement about other dealers beyond 'Toyota dealers are spread across Iowa'. No competitor is named, and there is no closest/only claim.",
        ],
        "ai_summary": "Motor Inn Toyota of Carroll is a Toyota dealer in west-central Iowa at 1526 Le Clark Road, Carroll, Iowa 51401, just off West US Highway 30, phone (712) 792-5000. It sells new Toyotas and Toyota Certified Pre-Owned vehicles, runs a Toyota service center, appraises trade-ins without an appointment, and is part of Motor Inn Auto Group with Motor Inn Chevrolet of Carroll at the same address.",
    },
    {
        "slug": "toyota-tacoma-tundra-for-sale-carroll-iowa",
        "store": "toyota",
        "path": "/toyota-tacoma-tundra-for-sale-carroll-iowa",
        "status": "NEW page. The Toyota site has model research pages (/toyota-tacoma, /2026-toyota-tundra.html) but no 'for sale' shopping page. An unpublished content/ready-design/toyota-tacoma-carroll-iowa.html draft exists without a set canonical; see the routing note.",
        "tier": "ready-now",
        "queries": [
            "toyota tacoma for sale", "toyota tundra for sale",
            "toyota tacoma for sale near me", "toyota tundra for sale trd pro",
        ],
        "h1": "Toyota Tacoma and Tundra for Sale in Carroll, Iowa",
        "title": "Tacoma & Tundra for Sale in Carroll, IA | Motor Inn Toyota",
        "meta": "Shop the Toyota Tacoma and Tundra, new and used, at Motor Inn Toyota of Carroll, 1526 Le Clark Road, Carroll, Iowa. Test drives: (712) 792-5000.",
        "og_title": "Toyota Tacoma and Tundra for Sale in Carroll, Iowa",
        "og_desc": "New and used Toyota Tacoma and Tundra pickups at Motor Inn Toyota of Carroll.",
        "cta": "Search Toyota trucks or call (712) 792-5000.",
        "intro": f"""
Motor Inn Toyota of Carroll sells the Toyota Tacoma and Toyota Tundra at 1526 Le Clark Road in Carroll, Iowa. Search [new Tacoma inventory]({T}/searchnew.aspx?Model=Tacoma) and [new Tundra inventory]({T}/searchnew.aspx?Model=Tundra) to see what's on the lot today, or call (712) 792-5000.
""",
        "sections": [
            ("Where can I find a Toyota Tacoma for sale near me?", f"""
At Motor Inn Toyota of Carroll, just off West US Highway 30 in Carroll. [Search new Tacoma inventory]({T}/searchnew.aspx?Model=Tacoma) or read about the truck on the [Tacoma model page]({T}/toyota-tacoma). Watching for the next TRD Pro? See our post on the [2027 Tacoma TRD Pro]({G}/blog/2027-toyota-tacoma-trd-pro-honeycomb-reservation-interest).
"""),
            ("Is a Toyota Tundra for sale in Carroll?", f"""
Yes. Motor Inn Toyota of Carroll sells the new Toyota Tundra in Carroll, Iowa, and inventory changes, so [search new Tundra inventory]({T}/searchnew.aspx?Model=Tundra) for what's on the lot today and see the [Tundra model page]({T}/2026-toyota-tundra.html) for the lineup. If you want a specific trim, such as a TRD Pro, call (712) 792-5000 and ask the team to look for one.
"""),
            ("Tacoma or Tundra: which Toyota truck fits?", f"""
The Tacoma is Toyota's midsize pickup. It's a good fit if you want a truck that's easier to park in town and still handles weekend gear. The Tundra is Toyota's full-size pickup, with an available i-FORCE MAX powertrain, for bigger towing and hauling jobs. Driving both back to back is the quickest way to feel the difference; test drives can be arranged by phone or on the [test drive page]({T}/testdrive.aspx).
"""),
            ("Can I buy a used Toyota Tacoma?", f"""
Yes, when one is on the lot. Check [Toyota Certified Pre-Owned]({T}/certified-pre-owned.html) and the [used inventory search]({T}/searchused.aspx). For used trucks of every brand across Motor Inn Auto Group, see [used trucks]({G}/used-trucks).
"""),
            ("Can I trade in and finance a Toyota truck in Carroll?", f"""
Yes. Trade appraisals are walk-in, with no appointment needed, and an online estimate is on the [trade page]({T}/trade.aspx). Motor Inn works with a network of lenders; pre-approval is on the [pre-approval page]({T}/preapproved.aspx), and current Toyota specials are on the [specials page]({T}/newspecials.html).
"""),
        ],
        "faq": [
            ("Where can I find a Toyota Tacoma for sale near Carroll, Iowa?",
             "Motor Inn Toyota of Carroll sells the new Toyota Tacoma at 1526 Le Clark Road in Carroll, Iowa. Inventory changes, so the Tacoma search on motorinntoyotaofcarroll.com shows what is on the lot today. The phone number is (712) 792-5000."),
            ("Is a Toyota Tundra for sale in Carroll, Iowa?",
             "Motor Inn Toyota of Carroll sells the new Toyota Tundra, including the available i-FORCE MAX powertrain, at 1526 Le Clark Road in Carroll, Iowa. To find a specific trim such as a TRD Pro, call the sales team at (712) 792-5000."),
            ("What is the difference between the Toyota Tacoma and Tundra?",
             "The Toyota Tacoma is a midsize pickup, and the Toyota Tundra is a full-size pickup built for bigger towing and hauling jobs. Motor Inn Toyota of Carroll in Carroll, Iowa, sells both and can set up a back-to-back test drive."),
        ],
        "links": [
            ("new Tacoma inventory", f"{T}/searchnew.aspx?Model=Tacoma", "same site (filtered search)"),
            ("new Tundra inventory", f"{T}/searchnew.aspx?Model=Tundra", "same site (filtered search)"),
            ("Tacoma model page", f"{T}/toyota-tacoma", "same site"),
            ("2027 Tacoma TRD Pro", f"{G}/blog/2027-toyota-tacoma-trd-pro-honeycomb-reservation-interest", "cross-site (group)"),
            ("Tundra model page", f"{T}/2026-toyota-tundra.html", "same site"),
            ("test drive page", f"{T}/testdrive.aspx", "same site"),
            ("Toyota Certified Pre-Owned", f"{T}/certified-pre-owned.html", "same site"),
            ("used inventory search", f"{T}/searchused.aspx", "same site"),
            ("used trucks", f"{G}/used-trucks", "cross-site (group)"),
            ("trade page", f"{T}/trade.aspx", "same site"),
            ("pre-approval page", f"{T}/preapproved.aspx", "same site"),
            ("specials page", f"{T}/newspecials.html", "same site"),
        ],
        "post_links": ["Link from /toyota-dealers-in-iowa ('What can I buy') once live, and from the /toyota-tacoma model page."],
        "sources": TOYOTA_SOURCES + ["'i-FORCE MAX': live offer URLs offerdetails-New-Carroll-Iowa-2026-Toyota-Tundra-i-FORCE-MAX-… in both sitemaps.", "2027 Tacoma TRD Pro blog post: group sitemap snapshot."],
        "routing": """
Toyota site. These are new-Toyota truck shopping queries.

**Why one page for two models:** each model alone is thin (Tacoma about 290 impressions, Tundra about 180), and truck shoppers often compare the two. Splitting can wait until each model shows more volume in GSC.

**Used intent excluded:** "used toyota tacoma" (79 impressions) is used intent, which the routing rule sends to the group site, so it is not targeted here. The used section on this page is a support cross-link only.

**Conflict with an earlier draft:** content/ready-design/toyota-tacoma-carroll-iowa.html covers Tacoma-in-Carroll on the group site. Under the 2026-11-23 rule, new-Toyota model intent belongs on the Toyota site, so don't publish both.
""",
        "notes": [OEM_NOTE, FILTER_NOTE,
                  "The 2027 Tacoma TRD Pro blog link is described only as 'our post'. Its reservation content wasn't verified."],
        "ai_summary": "Motor Inn Toyota of Carroll, 1526 Le Clark Road, Carroll, Iowa 51401 (phone (712) 792-5000), sells the new Toyota Tacoma (midsize pickup) and Toyota Tundra (full-size pickup, available i-FORCE MAX powertrain), as well as used and Toyota Certified Pre-Owned trucks when they are in inventory.",
    },
    {
        "slug": "toyota-sequoia-sienna-for-sale-carroll-iowa",
        "store": "toyota",
        "path": "/toyota-sequoia-sienna-for-sale-carroll-iowa",
        "status": "NEW page. The Toyota site has model research pages (/2026-toyota-sequoia.html, /toyota-sienna) but no 'for sale' shopping page.",
        "tier": "ready-now",
        "queries": [
            "toyota sequoia for sale", "toyota sienna for sale", "toyota sequoia for sale near me",
            "what toyota is bigger than a highlander",
        ],
        "h1": "Toyota Sequoia and Sienna for Sale in Carroll, Iowa",
        "title": "Sequoia & Sienna for Sale in Carroll, IA | Motor Inn Toyota",
        "meta": "Shop the Toyota Sequoia SUV and Sienna minivan at Motor Inn Toyota of Carroll, 1526 Le Clark Road, Carroll, Iowa. Test drives: (712) 792-5000.",
        "og_title": "Toyota Sequoia and Sienna for Sale in Carroll, Iowa",
        "og_desc": "Two big Toyota family haulers, the Sequoia SUV and the Sienna minivan, at Motor Inn Toyota of Carroll.",
        "cta": "Search Sequoia and Sienna inventory or call (712) 792-5000.",
        "intro": f"""
Motor Inn Toyota of Carroll sells the Toyota Sequoia and the Toyota Sienna at 1526 Le Clark Road in Carroll, Iowa. Search [new Sequoia inventory]({T}/searchnew.aspx?Model=Sequoia) and [new Sienna inventory]({T}/searchnew.aspx?Model=Sienna) to see what's on the lot today, or call (712) 792-5000.
""",
        "sections": [
            ("Where can I find a Toyota Sequoia for sale near me?", f"""
At Motor Inn Toyota of Carroll, just off West US Highway 30 in Carroll. [Search new Sequoia inventory]({T}/searchnew.aspx?Model=Sequoia) and see the [Sequoia model page]({T}/2026-toyota-sequoia.html). If the trim you want isn't on the lot, ask the team about finding one.
"""),
            ("Is a Toyota Sienna for sale near Carroll?", f"""
Yes. Motor Inn Toyota of Carroll sells the new Toyota Sienna in Carroll, Iowa, and inventory changes, so [search new Sienna inventory]({T}/searchnew.aspx?Model=Sienna) and see the [Sienna model page]({T}/toyota-sienna). Call (712) 792-5000 to check a specific trim or color.
"""),
            ("Sequoia or Sienna: which fits your family?", f"""
Both carry a big family. The Sequoia is Toyota's full-size SUV, a good pick if you tow a camper or boat or want SUV ground clearance. The Sienna is Toyota's minivan, with sliding doors that make car seats and school pickup easier. Bring the car seats to a test drive of each; test drives can be arranged by phone or on the [test drive page]({T}/testdrive.aspx).
"""),
            ("What Toyota is bigger than a Highlander?", f"""
The Grand Highlander and the Sequoia are both bigger than the Highlander. The Grand Highlander is the next step up, and the Sequoia is Toyota's full-size SUV. Compare the first two in [Highlander vs. Grand Highlander]({G}/highlander-vs-grand-highlander), or see the [Grand Highlander model page]({T}/2026-toyota-grand-highlander.html).
"""),
            ("Can I buy a used Sequoia or Sienna in Carroll?", f"""
Yes, when one is on the lot. Check [Toyota Certified Pre-Owned]({T}/certified-pre-owned.html) and the [used inventory search]({T}/searchused.aspx). Trade appraisals are walk-in, with no appointment needed, and online pre-approval is on the [pre-approval page]({T}/preapproved.aspx).
"""),
        ],
        "faq": [
            ("Where can I find a Toyota Sequoia for sale near Carroll, Iowa?",
             "Motor Inn Toyota of Carroll sells the new Toyota Sequoia at 1526 Le Clark Road in Carroll, Iowa. Inventory changes, so the Sequoia search on motorinntoyotaofcarroll.com shows what is on the lot today. The phone number is (712) 792-5000."),
            ("Is a Toyota Sienna for sale in Carroll, Iowa?",
             "Motor Inn Toyota of Carroll sells the new Toyota Sienna minivan at 1526 Le Clark Road in Carroll, Iowa. To check a specific trim or color, call the sales team at (712) 792-5000."),
            ("Should I buy a Toyota Sequoia or a Toyota Sienna?",
             "The Toyota Sequoia is a full-size SUV suited to towing and rougher roads, and the Toyota Sienna is a minivan with sliding doors that make car seats and daily family trips easier. Motor Inn Toyota of Carroll in Carroll, Iowa, sells both and can set up test drives of each."),
            ("What Toyota is bigger than a Highlander?",
             "The Toyota Grand Highlander and the Toyota Sequoia are both larger than the Highlander. The Grand Highlander is the next size up, and the Sequoia is Toyota's full-size SUV. Motor Inn Toyota of Carroll in Carroll, Iowa, sells all three."),
        ],
        "links": [
            ("new Sequoia inventory", f"{T}/searchnew.aspx?Model=Sequoia", "same site (filtered search)"),
            ("new Sienna inventory", f"{T}/searchnew.aspx?Model=Sienna", "same site (filtered search)"),
            ("Sequoia model page", f"{T}/2026-toyota-sequoia.html", "same site"),
            ("Sienna model page", f"{T}/toyota-sienna", "same site"),
            ("test drive page", f"{T}/testdrive.aspx", "same site"),
            ("Highlander vs. Grand Highlander", f"{G}/highlander-vs-grand-highlander", "cross-site (group)"),
            ("Grand Highlander model page", f"{T}/2026-toyota-grand-highlander.html", "same site"),
            ("Toyota Certified Pre-Owned", f"{T}/certified-pre-owned.html", "same site"),
            ("used inventory search", f"{T}/searchused.aspx", "same site"),
            ("pre-approval page", f"{T}/preapproved.aspx", "same site"),
        ],
        "post_links": ["Link from /toyota-dealers-in-iowa ('What can I buy') once live, and from the /toyota-sienna and /2026-toyota-sequoia.html model pages."],
        "sources": TOYOTA_SOURCES + ["Highlander vs. Grand Highlander page: group sitemap snapshot (live)."],
        "routing": """
Toyota site. These are new-Toyota model shopping queries.

**Why one page for two models:** each model has about 130 to 170 impressions, too thin for its own page. Both are three-row family vehicles that buyers cross-shop. "what toyota is bigger than a highlander" (position 4.2) fits here as a size-up question.
""",
        "notes": [OEM_NOTE, FILTER_NOTE,
                  "'is the sequoia built on the tundra frame' (11 impressions) is NOT answered, because there's no repo source for platform facts. Add it if Spencer supplies an OEM source.",
                  "'2024 toyota sequoia sr5' (36 impressions) is a single-used-unit query and isn't targeted."],
        "ai_summary": "Motor Inn Toyota of Carroll, 1526 Le Clark Road, Carroll, Iowa 51401 (phone (712) 792-5000), sells the new Toyota Sequoia (full-size SUV) and Toyota Sienna (minivan), plus the Grand Highlander, which with the Sequoia is larger than the Highlander. Used and Toyota Certified Pre-Owned units are sold when in inventory.",
    },
]
