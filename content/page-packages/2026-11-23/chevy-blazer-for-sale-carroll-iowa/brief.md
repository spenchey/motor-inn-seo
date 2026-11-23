# Brief: chevy-blazer-for-sale-carroll-iowa

- **Site:** www.motorinnofcarroll.com (Motor Inn Chevrolet of Carroll)
- **URL:** https://www.motorinnofcarroll.com/chevy-blazer-for-sale-carroll-iowa
- **Status:** NEW page (the Chevy site has year-model pages /2026-chevrolet-blazer and /2026-chevrolet-blazer-ev but no shopping or 'for sale' page).
- **Intent tier:** ready-now
- **H1:** Chevy Blazer for Sale Near Carroll, Iowa
- **Primary query:** chevy blazer for sale near me
- **AI mirror target (handoff only, not in the mirror file):** Chevy-host mirror (per-host catalog, spenchey/ai-markdown-proxy)

## Routing decision

Chevrolet site. These are new-Chevrolet single-model shopping queries.

This model gets its own page because it is the largest single-model cluster in the export (about 2,700 impressions). "chevy blazer for sale near me" already shows at position 2.0 with zero clicks, which suggests the current landing page (/Contactus/Carroll on the group site) doesn't match what Blazer shoppers want.

## Source evidence (GSC, 12 months ending 2026-11-22)

Source: `ads/gsc-keywords-12mo.json`. Every row in it is labeled `sc-domain:motorinnautogroup.com`. The Chevrolet property is BLOCKED for the service account (`siteUnverifiedUser` in `pipeline/cache/gsc-ebe12c…json`, 2026-10-19). The Toyota property has its own data, which these rows don't include. A ✓ in the Ads-40 column means the query is also one of the 40 exact-match terms in `ads/gsc-ads-package-2026-11-22/keywords.csv`, and that file's landing page is shown.

| Query | Impressions | Clicks | Avg pos | Ads-40 | Current landing page (Ads-40 file) |
|---|---:|---:|---:|:-:|---|
| chevy blazer for sale near me | 1013 | 0 | 2.0 | ✓ | https://www.motorinnautogroup.com/Contactus/Carroll |
| chevy blazer ev near me | 690 | 0 | 6.4 |  |  |
| blazer suv for sale | 626 | 0 | 8.1 |  |  |
| chevy blazer lease prices near me | 356 | 0 | 12.2 | ✓ | https://www.motorinnautogroup.com/Contactus/Carroll |
| chevy blazers for sale near me | 24 | 1 | 1.3 |  |  |
| chevy blazer for sale | 22 | 0 | 2.4 | ✓ | https://www.motorinnautogroup.com/Contactus/Carroll |

Cluster total: **2,731 impressions** across 6 queries.

## Question phrasing sources

Each H2 and FAQ question follows a real GSC query. Rows marked DERIVED are conversion or support questions with no direct GSC row (10+ impressions), answered from owner-verified facts.

| Question | Where | GSC query it follows | Impressions |
|---|---|---|---:|
| Where can I find a Chevy Blazer for sale near me? | H2 | chevy blazer for sale near me | 1013 |
| What's the difference between the Blazer and the Blazer EV? | H2 | chevy blazer ev near me | 690 |
| How do I get Chevy Blazer lease prices near me? | H2 | chevy blazer lease prices near me | 356 |
| Can I test drive a Blazer in Carroll? | H2 | DERIVED | |
| Can I trade in my car toward a Blazer? | H2 | DERIVED | |
| Where can I find a Chevy Blazer for sale near Carroll, Iowa? | FAQ | chevy blazers for sale near me | 24 |
| What is the difference between the Chevy Blazer and the Blazer EV? | FAQ | chevy blazer ev near me | 690 |
| How do I get Chevy Blazer lease prices near me? | FAQ | chevy blazer lease prices near me | 356 |
| Can I test drive a Chevy Blazer in Carroll, Iowa? | FAQ | DERIVED | |

## Internal links (all verified in the 2026-11-05 sitemap snapshots in `brain/research/`)

| Anchor | URL | Note |
|---|---|---|
| Search Blazer inventory | https://www.motorinnofcarroll.com/searchnew.aspx?Model=Blazer | same site (filtered search) |
| New Blazer EV inventory | https://www.motorinnofcarroll.com/searchnew.aspx?Model=Blazer%20EV | same site (filtered search) |
| Used inventory | https://www.motorinnofcarroll.com/searchused.aspx | same site |
| Blazer | https://www.motorinnofcarroll.com/2026-chevrolet-blazer | same site |
| Blazer EV | https://www.motorinnofcarroll.com/2026-chevrolet-blazer-ev | same site |
| EV protection plan | https://www.motorinnofcarroll.com/ev-protection-plan-chevrolet | same site |
| pre-approval page | https://www.motorinnofcarroll.com/preapproved.aspx | same site |
| test drive page | https://www.motorinnofcarroll.com/testdrive.aspx | same site |
| trade page | https://www.motorinnofcarroll.com/trade.aspx | same site |

## Cross-links to add after publish (target pages do not exist yet)

- Link from /chevy-suvs-for-sale-carroll-iowa (Blazer bullet) and /chevy-dealer-carroll-iowa once live.

## Fact sources used in copy

- Address: Chevy contact page (.firecrawl/motorinnofcarroll.com-contactus.aspx.md) lists 'Motor Inn of Carroll, 1526 Le Clark Rd, Carroll, IA 51401'.
- Phone (712) 792-5000: brain/STATE.md ruling 2026-11-02. The 877-775-6741 / 877-733-5984 numbers on the Chevy contact page look like call-tracking numbers and are not printed.
- 'Motor Inn Chevrolet of Carroll' name, 'just off West US Highway 30': group homepage snippet (.firecrawl/nap-audit/20261029/_ap_uest.json).
- Chevrolet certified service, walk-in trade appraisal, lender-network financing, hours: content/ready-design-OWNER-NOTES.md (2026-10-23).
- Model pages and service/finance/trade URLs: Chevy sitemap snapshot brain/research/live-https_www_motorinnofcarroll_com_sitemap_xml.html (2026-11-05).
- No Buick/GMC mentions: content/drafts/buick-gmc-removal-request.md (no longer a Buick or GMC dealer).

## Review notes for Spencer

- No lease, payment, price or APR figures appear anywhere. Lease and deal queries are answered by sending the shopper to the sales team by phone. The /chevroletspecialoffers page is NOT cited, because the Codex check (2026-11-23) found it lists customer-category programs (military, educator, first responder), not model lease terms.
- Vehicle descriptions are kept qualitative (two-row vs three-row, gas vs electric, light vs heavy duty) with no specs. Spot-check the wording against chevrolet.com before handoff.
- Model-filtered search links use the DealerOn pattern searchnew.aspx?Model=<Model> (the group homepage uses the same pattern). Click-test each filter before handoff. The Blazer EV filter value ('Blazer EV') is the most likely to need a fix.
