# Brief: used-cars-carroll-iowa

- **Site:** www.motorinnautogroup.com (Motor Inn Auto Group)
- **URL:** https://www.motorinnautogroup.com/used-cars-carroll-iowa
- **Status:** IN-PLACE refresh of the existing live URL /used-cars-carroll-iowa. Not a new URL.
- **Intent tier:** ready-now
- **H1:** Used Cars for Sale in Carroll, Iowa
- **Primary query:** used cars carroll ia
- **AI mirror target (handoff only, not in the mirror file):** ai.motorinnautogroup.com (group mirror)

## Routing decision

Group site. Used inventory is multi-brand, so Spencer's rule sends it to motorinnautogroup.com. "Cars for sale carroll iowa" (425 impressions, position 23.9) is folded in because the searcher hasn't named a brand or new vs used, and the used lot is the broadest match.

**URL choice: refresh the live /used-cars-carroll-iowa** instead of adding a new slug. The group site already has /used-cars, /used-inventory, /used-cars-carroll-iowa and /best-place-to-buy-used-car-carroll-iowa, and another used-cars URL would split the signal further.

## Source evidence (GSC, 12 months ending 2026-11-22)

Source: `ads/gsc-keywords-12mo.json`. Every row in it is labeled `sc-domain:motorinnautogroup.com`. The Chevrolet property is BLOCKED for the service account (`siteUnverifiedUser` in `pipeline/cache/gsc-ebe12c…json`, 2026-10-19). The Toyota property has its own data, which these rows don't include. A ✓ in the Ads-40 column means the query is also one of the 40 exact-match terms in `ads/gsc-ads-package-2026-11-22/keywords.csv`, and that file's landing page is shown.

| Query | Impressions | Clicks | Avg pos | Ads-40 | Current landing page (Ads-40 file) |
|---|---:|---:|---:|:-:|---|
| used cars carroll ia | 781 | 1 | 14.5 |  |  |
| used cars carroll iowa | 667 | 23 | 15.9 |  |  |
| cars for sale carroll iowa | 425 | 18 | 23.9 | ✓ | https://www.motorinnautogroup.com/Contactus/Carroll |
| used car carroll ia | 96 | 0 | 25.7 |  |  |
| used cars for sale carroll ia | 91 | 0 | 23.2 |  |  |
| used car dealers carroll ia | 89 | 0 | 20.2 |  |  |
| used car dealerships carroll ia | 86 | 1 | 23.2 |  |  |
| used car dealers carroll | 62 | 0 | 23.5 |  |  |
| used cars carroll | 55 | 0 | 21.0 |  |  |
| used car dealerships carroll | 52 | 0 | 22.9 |  |  |
| used cars for sale carroll | 50 | 0 | 21.0 |  |  |
| used car carroll | 45 | 0 | 20.4 |  |  |
| used car dealerships near me | 70 | 8 | 12.8 |  |  |

Cluster total: **2,569 impressions** across 13 queries.

## Ship plan (house rule: one change per page per cycle, brain/BRIEF.md)

1. Cycle 1: body copy + FAQ + JSON-LD. Leave the title, meta and H1 unchanged.
2. Cycle 2: title, meta and H1 from meta.md and content.md.

## Question phrasing sources

Each H2 and FAQ question follows a real GSC query. Rows marked DERIVED are conversion or support questions with no direct GSC row (10+ impressions), answered from owner-verified facts.

| Question | Where | GSC query it follows | Impressions |
|---|---|---|---:|
| Where can I find used cars for sale in Carroll, Iowa? | H2 | used cars for sale carroll ia | 91 |
| Can I find a used car under $20,000 in Carroll? | H2 | DERIVED | |
| Which used car dealers in Carroll, IA also service what they sell? | H2 | used car dealers carroll ia | 89 |
| Can I trade in my car toward a used car? | H2 | DERIVED | |
| Can I get financing on a used car in Carroll? | H2 | DERIVED | |
| Can I test drive a used car before I buy? | H2 | test drive used car | 29 |
| Where can I find used cars for sale in Carroll, Iowa? | FAQ | used cars for sale carroll ia | 91 |
| Does a Carroll used car dealer take trade-ins without an appointment? | FAQ | DERIVED | |
| Can I get financing on a used car in Carroll, Iowa? | FAQ | DERIVED | |
| How do I find a used car under $20,000 in Carroll? | FAQ | DERIVED | |
| Are there used car dealerships in Carroll, IA? | FAQ | used car dealerships carroll ia | 86 |

## Internal links (all verified in the 2026-11-05 sitemap snapshots in `brain/research/`)

| Anchor | URL | Note |
|---|---|---|
| used inventory search | https://www.motorinnautogroup.com/used-inventory | same site |
| CARFAX 1-Owner vehicles | https://www.motorinnautogroup.com/carfax-1-owner.html | same site |
| Certified Pre-Owned Toyotas | https://www.motorinntoyotaofcarroll.com/certified-pre-owned.html | cross-site (Toyota store) |
| Used vehicles under $20,000 | https://www.motorinnautogroup.com/under-20000 | same site |
| Used vehicles under $15,000 | https://www.motorinnautogroup.com/under-15k.html | same site |
| service page | https://www.motorinnautogroup.com/service-locations.html | same site |
| trade page | https://www.motorinnautogroup.com/trade.aspx | same site |
| financing page | https://www.motorinnautogroup.com/finance-locations.html | same site |
| test drive page | https://www.motorinnautogroup.com/testdrive.aspx | same site |
| hours page | https://www.motorinnautogroup.com/hours.aspx | same site (visit block) |

## Cross-links to add after publish (target pages do not exist yet)

- Sibling: link to /best-place-to-buy-used-car-carroll-iowa (live) from the 'Which used car dealers in Carroll, IA also service what they sell?' section if Spencer wants a second used-car entry point.

## Fact sources used in copy

- Address, phone: group contact page (.firecrawl/motorinnautogroup.com-contact-us.md); phone ruling brain/STATE.md 2026-11-02.
- Hours, walk-in trade appraisal, lender-network financing, test-drive framing, Chevrolet certified: content/ready-design-OWNER-NOTES.md (owner answers 2026-10-23).
- 'Just off West US Highway 30', store names: group homepage snippet in .firecrawl/nap-audit/20261029/_ap_uest.json.
- 'Factory service', 'franchised': brain/BRIEF.md.
- Price-filter pages /under-20000 and /under-15k.html, /carfax-1-owner.html: group sitemap snapshot brain/research/live-https_www_motorinnautogroup_com_sitemap_xml.html.
- Toyota CPO page: Toyota sitemap snapshot.

## Review notes for Spencer

- The 2026-10 approved refresh of this slug (content/page-packages/2026-10/designed/) is not this copy. If it was published, check it for the banned 522-2526 number: the sibling 2026-10 designed pages print it.
- The cluster is about 2,600 impressions at positions 14 to 26, which suggests the live page isn't being picked for these queries. After publish, check in GSC which URL Google chooses.
- No competitors are named or described. The franchised-dealer section only states facts about Motor Inn.
