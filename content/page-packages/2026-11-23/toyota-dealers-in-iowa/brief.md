# Brief: toyota-dealers-in-iowa

- **Site:** www.motorinntoyotaofcarroll.com (Motor Inn Toyota of Carroll)
- **URL:** https://www.motorinntoyotaofcarroll.com/toyota-dealers-in-iowa
- **Status:** NEW page. The live Toyota site already has /toyota-dealer-carroll-iowa and /toyota-dealer-near-carroll-ia-51401-…/, which target Carroll-local intent. This page targets the statewide and 'near me' wording instead, and it links to the town pages rather than repeating them.
- **Intent tier:** ready-now
- **H1:** Toyota Dealer in West-Central Iowa: Motor Inn Toyota of Carroll
- **Primary query:** toyota dealers in iowa
- **AI mirror target (handoff only, not in the mirror file):** Toyota-host mirror (per-host catalog, spenchey/ai-markdown-proxy)

## Routing decision

Toyota site. The intent is to find a new Toyota dealer, so it routes to the Toyota store's site.

**Cannibalization guard:** the high-volume Carroll-Toyota queries ("toyota carroll iowa" 1,202, "carroll toyota" 864, "motor inn toyota of carroll" 683) already rank at positions 1.6 to 5.6 with 250-click rows, mostly through /Contactus/Carroll. They are left out on purpose. This page targets only the Iowa-wide and 'near me' wording, which sits at positions 3 to 7 with low CTR. The page names no competing dealers and makes no 'closest' or 'only' claim.

## Source evidence (GSC, 12 months ending 2026-11-22)

Source: `ads/gsc-keywords-12mo.json`. Every row in it is labeled `sc-domain:motorinnautogroup.com`. The Chevrolet property is BLOCKED for the service account (`siteUnverifiedUser` in `pipeline/cache/gsc-ebe12c…json`, 2026-10-19). The Toyota property has its own data, which these rows don't include. A ✓ in the Ads-40 column means the query is also one of the 40 exact-match terms in `ads/gsc-ads-package-2026-11-22/keywords.csv`, and that file's landing page is shown.

| Query | Impressions | Clicks | Avg pos | Ads-40 | Current landing page (Ads-40 file) |
|---|---:|---:|---:|:-:|---|
| toyota dealers in iowa | 500 | 51 | 4.5 | ✓ | https://www.motorinnautogroup.com/Contactus/Carroll |
| toyota dealerships in iowa | 410 | 47 | 4.1 | ✓ | https://www.motorinnautogroup.com/Contactus/Carroll |
| iowa toyota dealers | 288 | 36 | 3.7 | ✓ | https://www.motorinnautogroup.com/Contactus/Carroll |
| toyota dealership near me | 235 | 17 | 3.4 | ✓ | https://www.motorinnautogroup.com/Contactus/Carroll |
| toyota dealer near me | 195 | 15 | 3.8 | ✓ | https://www.motorinntoyotaofcarroll.com/ |
| toyota service near me | 165 | 0 | 3.8 |  |  |
| toyota iowa | 152 | 13 | 4.6 |  |  |
| toyota dealers iowa | 137 | 25 | 4.3 |  |  |
| toyota dealer iowa | 104 | 15 | 4.9 |  |  |
| toyota dealership iowa | 98 | 4 | 4.6 |  |  |
| toyota dealers near me | 86 | 9 | 2.8 |  |  |
| toyota near me | 82 | 3 | 6.3 |  |  |
| toyota dealerships iowa | 80 | 8 | 6.9 |  |  |
| toyota dealership in iowa | 67 | 13 | 4.3 |  |  |
| toyota dealerships near me | 53 | 4 | 3.6 |  |  |
| toyota in iowa | 49 | 4 | 6.1 |  |  |
| toyota dealer in iowa | 46 | 6 | 4.7 |  |  |
| iowa toyota dealership | 43 | 4 | 5.4 |  |  |
| toyota iowa dealers | 41 | 3 | 3.9 |  |  |

Cluster total: **2,831 impressions** across 19 queries.

## Question phrasing sources

Each H2 and FAQ question follows a real GSC query. Rows marked DERIVED are conversion or support questions with no direct GSC row (10+ impressions), answered from owner-verified facts.

| Question | Where | GSC query it follows | Impressions |
|---|---|---|---:|
| Where are Toyota dealers in Iowa? | H2 | toyota dealers in iowa | 500 |
| Is there a Toyota dealership near me? | H2 | toyota dealership near me | 235 |
| What can I buy at a Toyota dealer in Carroll, Iowa? | H2 | toyota dealer carroll iowa | 106 |
| Where can I get Toyota service near me? | H2 | toyota service near me | 165 |
| Can I trade in and finance at the Carroll Toyota dealer? | H2 | DERIVED | |
| Where is a Toyota dealer in west-central Iowa? | FAQ | toyota dealer in iowa | 46 |
| Is there a Toyota dealership in Carroll, Iowa? | FAQ | toyota dealership carroll iowa | 168 |
| Where can I get Toyota service near Carroll, Iowa? | FAQ | toyota service | 188 |
| Does Motor Inn Toyota of Carroll sell Certified Pre-Owned Toyotas? | FAQ | toyota used cars near me | 44 |
| Can I trade in my car at the Toyota dealer in Carroll without an appointment? | FAQ | DERIVED | |

## Internal links (all verified in the 2026-11-05 sitemap snapshots in `brain/research/`)

| Anchor | URL | Note |
|---|---|---|
| Toyota dealer near Denison | https://www.motorinntoyotaofcarroll.com/toyota-dealer-near-denison-ia-51442-motor-inn-toyota-of-carroll/ | same site |
| Toyota dealer near Audubon | https://www.motorinntoyotaofcarroll.com/toyota-dealer-near-audubon-ia-50025-motor-inn-toyota-of-carroll/ | same site |
| Toyota dealer near Jefferson | https://www.motorinntoyotaofcarroll.com/toyota-dealer-near-jefferson-ia-50129-motor-inn-toyota-of-carroll/ | same site |
| New Toyota inventory | https://www.motorinntoyotaofcarroll.com/searchnew.aspx | same site |
| Toyota hybrids and electrified vehicles | https://www.motorinntoyotaofcarroll.com/electrified | same site |
| Toyota Certified Pre-Owned | https://www.motorinntoyotaofcarroll.com/certified-pre-owned.html | same site |
| Used inventory | https://www.motorinntoyotaofcarroll.com/searchused.aspx | same site |
| Current Toyota offers | https://www.motorinntoyotaofcarroll.com/newspecials.html | same site |
| manufacturer incentives | https://www.motorinntoyotaofcarroll.com/manufacturer-incentives.aspx | same site |
| Toyota service center | https://www.motorinntoyotaofcarroll.com/service-center.html | same site |
| service scheduling page | https://www.motorinntoyotaofcarroll.com/serviceappmt.aspx | same site |
| where to service a Toyota in Carroll | https://www.motorinnautogroup.com/where-to-service-toyota-carroll-iowa | cross-site (group) |
| trade page | https://www.motorinntoyotaofcarroll.com/trade.aspx | same site |
| pre-approval page | https://www.motorinntoyotaofcarroll.com/preapproved.aspx | same site |

## Cross-links to add after publish (target pages do not exist yet)

- Link this page from the Toyota homepage or /aboutus.aspx, and from motorinnautogroup.com/contactus.aspx.
- Link /toyota-tacoma-tundra-for-sale-carroll-iowa and /toyota-sequoia-sienna-for-sale-carroll-iowa from the 'What can I buy' list once they are live.

## Fact sources used in copy

- Years in business ('family-owned for more than 75 years'): Spencer decision 2026-11-23, matching owner notes '75+' (content/ready-design-OWNER-NOTES.md).
- Address, store name: Toyota contact page (.firecrawl/motorinntoyotaofcarroll.com-contactus.aspx.md), 'Motor Inn Toyota Of Carroll, 1526 Le Clark Road, Carroll, IA 51401'.
- Phone (712) 792-5000: required on customer-facing Toyota copy (brief + brain/STATE.md ruling 2026-11-02). The 712-513-xxxx numbers on the Toyota contact page look like tracking numbers and are not printed. 522-2526 is never used.
- 'Just off West US Highway 30': group homepage snippet (.firecrawl/nap-audit/20261029/_ap_uest.json).
- Walk-in trade appraisal, lender-network financing, hours: content/ready-design-OWNER-NOTES.md (2026-10-23).
- Model, CPO, service and town pages: Toyota sitemap snapshot brain/research/live-https_www_motorinntoyotaofcarroll_com_sitemap_xml.html (2026-11-05).

## Review notes for Spencer

- 'Toyota dealerships in nebraska' (55 impressions) is out of market and not targeted.
- 'where can i find toyota service centers in iowa with weekend hours?' (55 impressions) is NOT answered with weekend service hours, because the repo has no source for service hours. Service hours are left to the hours page.
- The page makes no statement about other dealers beyond 'Toyota dealers are spread across Iowa'. No competitor is named, and there is no closest/only claim.
