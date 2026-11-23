# Brief: contactus-carroll

- **Site:** www.motorinnautogroup.com (Motor Inn Auto Group)
- **URL:** https://www.motorinnautogroup.com/contactus.aspx
- **Status:** IN-PLACE content block for the existing live contact page /contactus.aspx. /Contactus/Carroll, the URL in the GSC data, now 301-redirects there (live check 2026-11-23), and /contactus.aspx is its own canonical. Not a new URL. The folder slug 'contactus-carroll' is kept for continuity.
- **Intent tier:** ready-now
- **H1:** Car Dealerships in Carroll, Iowa: Motor Inn Auto Group
- **Primary query:** car dealerships carroll iowa
- **AI mirror target (handoff only, not in the mirror file):** ai.motorinnautogroup.com (group mirror)

## Routing decision

Group site. "Car dealerships Carroll Iowa" is cross-brand, general-dealership intent, which Spencer's 2026-11-23 rule sends to motorinnautogroup.com.

**URL choice: in-place on the contact page, not a new page.** GSC sends this cluster to /Contactus/Carroll (11 of the 13 cluster rows that are also in the Ads-40 file land there, and the other 2 land on the group homepage; 203 clicks at position 10.3 on 'carroll iowa car dealerships'; the brain/reports/gsc-cannibalization-2026-11-03.md split shows /Contactus/Carroll winning). **That URL now 301-redirects to /contactus.aspx**, and /contactus.aspx declares itself canonical (curl check 2026-11-23). The editable page is /contactus.aspx, and the GSC credit consolidates there. Other URLs chasing this intent:
1. /contactus.aspx (live; receives the ranking contact traffic). **Recommended owner.**
2. /car-dealerships-carroll-iowa (live; its 2026-10 approved refresh prints the banned 522-2526 number).
3. /car-dealerships-in-carroll-iowa.html (live; duplicate).
4. content/ready-design/contactus-money-page.html (unpublished draft for the same page; retired 2026-11-23).

**Decided (2026-11-23, Spencer delegated the call):**
- (a) **301** both /car-dealerships-carroll-iowa and /car-dealerships-in-carroll-iowa.html to /contactus.aspx. A canonical tag is only a hint, and Google tends to ignore it between pages that aren't near-duplicates. A content page and a contact page aren't, so a canonical would likely leave the duplicates competing. A 301 consolidates them for certain and also retires the 2026-10 copy that prints the banned 522-2526.
- (b) This package ships on /contactus.aspx. The ready-design contactus draft is retired (moved to content/ready-design/_retired/2026-11-23/).

## Source evidence (GSC, 12 months ending 2026-11-22)

Source: `ads/gsc-keywords-12mo.json`. Every row in it is labeled `sc-domain:motorinnautogroup.com`. The Chevrolet property is BLOCKED for the service account (`siteUnverifiedUser` in `pipeline/cache/gsc-ebe12c…json`, 2026-10-19). The Toyota property has its own data, which these rows don't include. A ✓ in the Ads-40 column means the query is also one of the 40 exact-match terms in `ads/gsc-ads-package-2026-11-22/keywords.csv`, and that file's landing page is shown.

| Query | Impressions | Clicks | Avg pos | Ads-40 | Current landing page (Ads-40 file) |
|---|---:|---:|---:|:-:|---|
| car dealerships carroll iowa | 1831 | 105 | 23.6 | ✓ | https://www.motorinnautogroup.com/Contactus/Carroll |
| carroll iowa car dealerships | 1016 | 203 | 10.3 | ✓ | https://www.motorinnautogroup.com/Contactus/Carroll |
| carroll dealerships | 595 | 31 | 27.4 | ✓ | https://www.motorinnautogroup.com/Contactus/Carroll |
| car dealerships in carroll iowa | 462 | 34 | 20.3 |  |  |
| carroll iowa dealerships | 442 | 48 | 17.1 | ✓ | https://www.motorinnautogroup.com/Contactus/Carroll |
| carroll ia dealerships | 426 | 26 | 20.8 | ✓ | https://www.motorinnautogroup.com/Contactus/Carroll |
| carroll iowa auto dealers | 405 | 12 | 21.0 | ✓ | https://www.motorinnautogroup.com/ |
| car dealerships carroll | 382 | 2 | 36.7 | ✓ | https://www.motorinnautogroup.com/ |
| carroll car dealerships | 331 | 17 | 23.8 | ✓ | https://www.motorinnautogroup.com/Contactus/Carroll |
| carroll ia car dealerships | 329 | 42 | 16.0 | ✓ | https://www.motorinnautogroup.com/Contactus/Carroll |
| car dealers carroll iowa | 323 | 28 | 15.7 | ✓ | https://www.motorinnautogroup.com/Contactus/Carroll |
| carroll car dealership | 257 | 64 | 5.4 | ✓ | https://www.motorinnautogroup.com/Contactus/Carroll |
| carroll iowa car dealers | 213 | 17 | 15.9 | ✓ | https://www.motorinnautogroup.com/Contactus/Carroll |
| car dealership carroll iowa | 163 | 40 | 11.5 | ✓ | https://www.motorinnautogroup.com/Contactus/Carroll |
| car dealers in carroll iowa | 131 | 22 | 6.9 |  |  |
| dealerships in carroll iowa | 44 | 6 | 6.7 |  |  |
| carroll auto sales | 29 | 7 | 4.3 |  |  |

Cluster total: **7,379 impressions** across 17 queries.

## Ship plan (house rule: one change per page per cycle, brain/BRIEF.md)

1. Cycle 1: the content block only (sections + FAQ + visit block), placed below the form, plus the FAQPage/AutoDealer JSON-LD. Leave the title, meta and H1 unchanged.
2. Cycle 2 (after 2-4 weeks of GSC readings): switch the title and meta to the meta.md versions, then promote the H1.
3. Separately, as its own DealerOn request, AFTER the cycle-1 block is live on /contactus.aspx: 301 /car-dealerships-carroll-iowa and /car-dealerships-in-carroll-iowa.html to /contactus.aspx (decided 2026-11-23). Then update any internal links pointing at those two URLs.

## Question phrasing sources

Each H2 and FAQ question follows a real GSC query. Rows marked DERIVED are conversion or support questions with no direct GSC row (10+ impressions), answered from owner-verified facts.

| Question | Where | GSC query it follows | Impressions |
|---|---|---|---:|
| Which car dealerships are in Carroll, Iowa? | H2 | car dealerships carroll iowa | 1831 |
| What can I buy at a Carroll car dealership? | H2 | carroll car dealership | 257 |
| Is there a Chevy dealer and a Toyota dealer in Carroll, Iowa? | H2 | carroll iowa chevy dealers | 1513 |
| Can I trade in and finance at the same dealership? | H2 | DERIVED | |
| Can I get my car serviced at a Carroll dealership? | H2 | DERIVED | |
| How do I schedule a test drive in Carroll? | H2 | schedule a test drive | 267 |
| Which car dealerships are in Carroll, Iowa? | FAQ | car dealerships carroll iowa | 1831 |
| Where is the car dealership in Carroll, IA? | FAQ | car dealership carroll iowa | 163 |
| Is there a Chevy dealer and a Toyota dealer in Carroll, Iowa? | FAQ | carroll iowa chevy dealers | 1513 |
| Can I trade in my car at a Carroll dealership without an appointment? | FAQ | DERIVED | |
| Can I get car financing at a dealership in Carroll, Iowa? | FAQ | auto finance carroll ia | 81 |

## Internal links (all verified in the 2026-11-05 sitemap snapshots in `brain/research/`)

| Anchor | URL | Note |
|---|---|---|
| Search new Toyota and Chevrolet inventory | https://www.motorinnautogroup.com/searchnew.aspx | same site |
| Search used inventory | https://www.motorinnautogroup.com/used-inventory | same site |
| Used vehicles under $20,000 | https://www.motorinnautogroup.com/under-20000 | same site |
| Motor Inn Toyota of Carroll | https://www.motorinntoyotaofcarroll.com/ | cross-site (Toyota store) |
| Motor Inn Chevrolet of Carroll | https://www.motorinnofcarroll.com/ | cross-site (Chevy store) |
| trade page | https://www.motorinnautogroup.com/trade.aspx | same site |
| financing page | https://www.motorinnautogroup.com/finance-locations.html | same site |
| service page | https://www.motorinnautogroup.com/service-locations.html | same site |
| test drive page | https://www.motorinnautogroup.com/testdrive.aspx | same site |
| hours page | https://www.motorinnautogroup.com/hours.aspx | same site (visit block) |

## Cross-links to add after publish (target pages do not exist yet)

- Link 'Chevy dealer in Carroll' -> motorinnofcarroll.com/chevy-dealer-carroll-iowa once it is live.
- Link 'Toyota dealer in Iowa' -> motorinntoyotaofcarroll.com/toyota-dealers-in-iowa once it is live.

## Fact sources used in copy

- Years in business ('family-owned for more than 75 years'): Spencer decision 2026-11-23, matching owner notes '75+' (content/ready-design-OWNER-NOTES.md).
- Address, phone: group contact page (.firecrawl/motorinnautogroup.com-contact-us.md); phone ruling brain/STATE.md 2026-11-02.
- Hours, walk-in trade appraisal, lender-network financing, test-drive framing, Chevrolet certified: content/ready-design-OWNER-NOTES.md (owner answers 2026-10-23).
- 'Just off West US Highway 30', store names: group homepage snippet in .firecrawl/nap-audit/20261029/_ap_uest.json.
- 'Factory service', 'franchised': brain/BRIEF.md.

## Review notes for Spencer

- This content block goes BELOW the existing contact form. Keep the form as the first thing on the page: it is the #1 lead page (brain/STATE.md, 7,166 key events in 28 days).
- /Contactus/Carroll 301s to /contactus.aspx (checked 2026-11-23). Internal links and GBP should point at /contactus.aspx directly, with no UTM variants (see brain/reports/gsc-cannibalization-2026-11-03.md).
- Years in business: 'family-owned for more than 75 years' per Spencer's 2026-11-23 decision (owner notes: 75+). The live homepage still says 'over 85 years'; ask DealerOn to align it as a separate one-issue request.
- Hours are owner-verified sales hours. Service hours are left to the hours page.
