"""Shared, sourced facts for the 2026-11-23 page packages.

Every value here is traceable to a repo file. Do not add facts without a source line.
"""

ADDRESS = {
    "street": "1526 Le Clark Road",
    "city": "Carroll",
    "region": "IA",
    "zip": "51401",
}
# src: .firecrawl/motorinnautogroup.com-contact-us.md; .firecrawl/motorinntoyotaofcarroll.com-contactus.aspx.md;
#      .firecrawl/motorinnofcarroll.com-contactus.aspx.md (all three stores list 1526 Le Clark Rd, Carroll, IA 51401)
ADDRESS_LINE = "1526 Le Clark Road, Carroll, IA 51401"

PHONE = "(712) 792-5000"
PHONE_E164 = "+1-712-792-5000"
# src: brain/STATE.md "CUSTOMER-FACING RULING (Spencer 2026-11-02): 792-5000 is THE customer number";
#      GBP listing 'Motor Inn Toyota and Chevrolet of Carroll' +1712-792-5000; group contact page Sales 712-792-5000.
# The 877-/712-513- numbers on the brand-site contact pages are tracking numbers and are NOT printed.

LANDMARK = "just off West US Highway 30"
# src: group homepage snippet in .firecrawl/nap-audit/20261029/_ap_uest.json
#      ("Located just off of W US Hwy 30 in Carroll, Iowa")

# Owner-verified 2026-10-23 (content/ready-design-OWNER-NOTES.md):
HOURS_TEXT = "Monday through Wednesday 8:00 a.m. to 5:30 p.m., Thursday 8:00 a.m. to 7:00 p.m., Friday 8:00 a.m. to 5:30 p.m., Saturday 8:00 a.m. to 3:00 p.m., closed Sunday"
HOURS_SCHEMA = [
    {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Friday"], "opens": "08:00", "closes": "17:30"},
    {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Thursday"], "opens": "08:00", "closes": "19:00"},
    {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday"], "opens": "08:00", "closes": "15:00"},
]

# Owner-verified 2026-10-23 (content/ready-design-OWNER-NOTES.md):
#  - trade appraisal is walk-in, no appointment needed
#  - financing = lender network; never say "bad credit"
#  - test drive: no license/insurance talk; "at your convenience", no time promise
#  - Chevrolet certified service
# Voice DNA (brain/VOICE-DNA.md): family-owned; serves Denison, Audubon, Storm Lake, Sac City.
YEARS = "more than 75 years"
# src: Spencer decision 2026-11-23 ("75 years"), matching the owner-verified "75+ years" in
#      content/ready-design-OWNER-NOTES.md (2026-10-23). Supersedes the homepage's "over 85 years" and the
#      2026-10 pages' "since 1934" (flagged in the plan for DealerOn to align).

AREA_TOWNS = "Denison, Audubon, Jefferson, Storm Lake and Sac City"
# src: brain/VOICE-DNA.md (Denison, Audubon, Storm Lake, Sac City); Toyota-site sitemap has
#      toyota-dealer-near-jefferson-ia-50129 / -audubon-ia-50025 / -denison-ia-51442 pages.

STORES = {
    "group": {
        "name": "Motor Inn Auto Group",
        "url": "https://www.motorinnautogroup.com/",
        "host": "www.motorinnautogroup.com",
        "brands": ["Toyota", "Chevrolet"],
        "service_url": "https://www.motorinnautogroup.com/service-locations.html",
        "ai_host": "ai.motorinnautogroup.com (group mirror)",
    },
    "toyota": {
        "name": "Motor Inn Toyota of Carroll",
        "url": "https://www.motorinntoyotaofcarroll.com/",
        "host": "www.motorinntoyotaofcarroll.com",
        "brands": ["Toyota"],
        "service_url": "https://www.motorinntoyotaofcarroll.com/serviceappmt.aspx",
        "ai_host": "Toyota-host mirror (per-host catalog, spenchey/ai-markdown-proxy)",
    },
    "chevy": {
        "name": "Motor Inn Chevrolet of Carroll",
        "alt": "Motor Inn of Carroll",
        "url": "https://www.motorinnofcarroll.com/",
        "host": "www.motorinnofcarroll.com",
        "brands": ["Chevrolet"],
        "service_url": "https://www.motorinnofcarroll.com/service",
        "ai_host": "Chevy-host mirror (per-host catalog, spenchey/ai-markdown-proxy)",
    },
}
# src names: group homepage snippet ("Motor Inn Toyota of Carroll", "Motor Inn Chevrolet of Carroll");
#            Chevy contact page ("Motor Inn of Carroll").
