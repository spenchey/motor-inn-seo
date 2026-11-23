# Brief: chevy-suvs-for-sale-carroll-iowa

- **Site:** www.motorinnofcarroll.com (Motor Inn Chevrolet of Carroll)
- **URL:** https://www.motorinnofcarroll.com/chevy-suvs-for-sale-carroll-iowa
- **Status:** NEW page (the Chevy site has model pages but no SUV shopping page).
- **Intent tier:** ready-now
- **H1:** Chevy SUVs for Sale in Carroll, Iowa
- **Primary query:** carroll iowa chevy suburban
- **AI mirror target (handoff only, not in the mirror file):** Chevy-host mirror (per-host catalog, spenchey/ai-markdown-proxy)

## Routing decision

Chevrolet site. These are new-Chevrolet model and body-style shopping queries.

Blazer queries go to their own page (chevy-blazer-for-sale-carroll-iowa) because together they are a 2,700-impression cluster. "carroll iowa chevy suburban" (1,518 impressions, position 25.3) is the largest row here.

## Source evidence (GSC, 12 months ending 2026-11-22)

Source: `ads/gsc-keywords-12mo.json`. Every row in it is labeled `sc-domain:motorinnautogroup.com`. The Chevrolet property is BLOCKED for the service account (`siteUnverifiedUser` in `pipeline/cache/gsc-ebe12c…json`, 2026-10-19). The Toyota property has its own data, which these rows don't include. A ✓ in the Ads-40 column means the query is also one of the 40 exact-match terms in `ads/gsc-ads-package-2026-11-22/keywords.csv`, and that file's landing page is shown.

| Query | Impressions | Clicks | Avg pos | Ads-40 | Current landing page (Ads-40 file) |
|---|---:|---:|---:|:-:|---|
| carroll iowa chevy suburban | 1518 | 0 | 25.3 |  |  |
| chevy suv near me | 903 | 0 | 3.2 |  |  |
| chevy traverse near me | 876 | 0 | 6.1 |  |  |
| chevy equinox near me | 776 | 1 | 7.8 |  |  |
| equinox lease near me | 613 | 0 | 2.7 |  |  |
| chevy suv for sale | 597 | 0 | 2.6 | ✓ | https://www.motorinnautogroup.com/Contactus/Carroll |
| chevrolet trax near me | 552 | 0 | 10.5 |  |  |
| tahoe deals near me | 501 | 0 | 8.5 |  |  |
| best chevy suv for families | 56 | 0 | 92.4 |  |  |
| chevy tahoe prices near me | 50 | 0 | 9.4 |  |  |
| tahoe for sale | 42 | 0 | 2.0 |  |  |
| chevrolet traverse for sale | 33 | 1 | 3.0 |  |  |
| chevy tahoe for sale | 32 | 0 | 1.8 |  |  |
| suburban for sale | 25 | 1 | 2.2 |  |  |
| chevy suburban for sale near me | 19 | 1 | 3.1 |  |  |

Cluster total: **6,593 impressions** across 15 queries.

## Question phrasing sources

Each H2 and FAQ question follows a real GSC query. Rows marked DERIVED are conversion or support questions with no direct GSC row (10+ impressions), answered from owner-verified facts.

| Question | Where | GSC query it follows | Impressions |
|---|---|---|---:|
| Which Chevy SUVs can I buy near me in Carroll? | H2 | chevy suv near me | 903 |
| Which Chevy SUV is best for families? | H2 | best chevy suv for families | 56 |
| Where can I find a Chevy Suburban in Carroll, Iowa? | H2 | carroll iowa chevy suburban | 1518 |
| How do I get Chevy SUV lease deals near me? | H2 | equinox lease near me | 613 |
| Can I buy a used Chevy SUV in Carroll? | H2 | DERIVED | |
| Where can I buy a Chevy SUV in Carroll, Iowa? | FAQ | chevy suv for sale | 597 |
| What is the best Chevy SUV for families? | FAQ | best chevy suv for families | 56 |
| Where can I find a Chevy Suburban in Carroll, Iowa? | FAQ | carroll iowa chevy suburban | 1518 |
| How do I find Chevy Equinox or Tahoe lease deals near Carroll? | FAQ | tahoe deals near me | 501 |

## Internal links (all verified in the 2026-11-05 sitemap snapshots in `brain/research/`)

| Anchor | URL | Note |
|---|---|---|
| new inventory search | https://www.motorinnofcarroll.com/searchnew.aspx | same site |
| Trax | https://www.motorinnofcarroll.com/2026-chevrolet-trax | same site |
| Trailblazer | https://www.motorinnofcarroll.com/2026-chevrolet-trailblazer | same site |
| Equinox | https://www.motorinnofcarroll.com/2026-chevrolet-equinox | same site |
| Blazer | https://www.motorinnofcarroll.com/2026-chevrolet-blazer | same site |
| Traverse | https://www.motorinnofcarroll.com/2026-chevrolet-traverse | same site |
| Tahoe | https://www.motorinnofcarroll.com/2026-chevrolet-tahoe | same site |
| Suburban | https://www.motorinnofcarroll.com/2026-chevrolet-suburban | same site |
| Equinox EV | https://www.motorinnofcarroll.com/2026-chevrolet-equinox-ev | same site |
| Blazer EV | https://www.motorinnofcarroll.com/2026-chevrolet-blazer-ev | same site |
| best Chevrolet SUVs for families | https://www.motorinnautogroup.com/best-chevrolet-suvs-for-families | cross-site (group) |
| Search Suburban inventory | https://www.motorinnofcarroll.com/searchnew.aspx?Model=Suburban | same site (filtered search) |
| used inventory search | https://www.motorinnofcarroll.com/searchused.aspx | same site |
| under $20K page | https://www.motorinnofcarroll.com/under-20k.html | same site |

## Cross-links to add after publish (target pages do not exist yet)

- Link to /chevy-blazer-for-sale-carroll-iowa from the Blazer bullet and to /chevy-dealer-carroll-iowa from the intro once both are live.

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
- Model-filtered search links use the DealerOn pattern searchnew.aspx?Model=<Model> (the group homepage uses the same pattern). Click-test each filter before handoff.
- The 'best chevy suv for families' row is at position 92 and the group site already has /best-chevrolet-suvs-for-families, so this page links there instead of competing with it.
