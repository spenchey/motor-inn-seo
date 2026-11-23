# Brief: chevy-trucks-for-sale-carroll-iowa

- **Site:** www.motorinnofcarroll.com (Motor Inn Chevrolet of Carroll)
- **URL:** https://www.motorinnofcarroll.com/chevy-trucks-for-sale-carroll-iowa
- **Status:** NEW page on the Chevy site. Supersedes the routing of the unpublished content/ready-design/chevy-trucks-carroll-iowa.html draft, which canonicalizes to the group site. That draft was retired 2026-11-23.
- **Intent tier:** ready-now
- **H1:** Chevy Trucks for Sale in Carroll, Iowa
- **Primary query:** chevrolet truck for sale
- **AI mirror target (handoff only, not in the mirror file):** Chevy-host mirror (per-host catalog, spenchey/ai-markdown-proxy)

## Routing decision

Chevrolet site. These are new-Chevrolet truck shopping queries. Brandless and used truck queries ("trucks for sale near me" 52, "used chevy silverado for sale" 35, "used chevy colorado for sale" 19) are NOT targeted here. Under the routing rule they belong to the group site's existing /used-trucks page. The used section on this page is a support cross-link only.

**Conflict with an earlier draft:** content/ready-design/chevy-trucks-carroll-iowa.html targets the same intent with a group-site canonical. Under the 2026-11-23 routing rule, brand-specific intent goes to the brand site. That draft was retired on 2026-11-23 (moved to content/ready-design/_retired/2026-11-23/). Its built copy is still in deliveries/site-packages/2026-11-05/motorinnautogroup/chevy-trucks-carroll-iowa/, so remove it from that batch before the batch goes to DealerOn.

## Source evidence (GSC, 12 months ending 2026-11-22)

Source: `ads/gsc-keywords-12mo.json`. Every row in it is labeled `sc-domain:motorinnautogroup.com`. The Chevrolet property is BLOCKED for the service account (`siteUnverifiedUser` in `pipeline/cache/gsc-ebe12c…json`, 2026-10-19). The Toyota property has its own data, which these rows don't include. A ✓ in the Ads-40 column means the query is also one of the 40 exact-match terms in `ads/gsc-ads-package-2026-11-22/keywords.csv`, and that file's landing page is shown.

| Query | Impressions | Clicks | Avg pos | Ads-40 | Current landing page (Ads-40 file) |
|---|---:|---:|---:|:-:|---|
| chevrolet truck for sale | 638 | 0 | 4.4 | ✓ | https://www.motorinnautogroup.com/Contactus/Carroll |
| chevy truck for sale near me | 407 | 0 | 9.7 | ✓ | https://www.motorinnautogroup.com/Contactus/Carroll |
| silverado lease deals near me | 386 | 0 | 5.4 |  |  |
| chevy colorado for sale near me | 42 | 2 | 3.0 |  |  |
| chevy 2500 for sale | 34 | 1 | 5.8 |  |  |
| chevy colorado for sale | 28 | 2 | 4.9 |  |  |
| chevrolet 2500 for sale | 20 | 0 | 8.4 |  |  |
| silverado zr2 for sale | 16 | 0 | 11.2 |  |  |
| chevy trucks | 15 | 0 | 4.5 |  |  |

Cluster total: **1,586 impressions** across 9 queries.

## Question phrasing sources

Each H2 and FAQ question follows a real GSC query. Rows marked DERIVED are conversion or support questions with no direct GSC row (10+ impressions), answered from owner-verified facts.

| Question | Where | GSC query it follows | Impressions |
|---|---|---|---:|
| Where can I find a Chevy truck for sale near me? | H2 | chevy truck for sale near me | 407 |
| Which Chevy truck should I buy? | H2 | chevy trucks | 15 |
| Is a Chevy 2500 for sale in Carroll? | H2 | chevy 2500 for sale | 34 |
| How do I get Silverado lease deals near me? | H2 | silverado lease deals near me | 386 |
| Can I buy a used Chevy Silverado or Colorado in Carroll? | H2 | DERIVED | |
| Where can I find a Chevy truck for sale near Carroll, Iowa? | FAQ | chevrolet truck for sale | 638 |
| Is a Chevy 2500 for sale in Carroll, Iowa? | FAQ | chevrolet 2500 for sale | 20 |
| How do I get Silverado lease deals near me? | FAQ | silverado lease deals near me | 386 |

## Internal links (all verified in the 2026-11-05 sitemap snapshots in `brain/research/`)

| Anchor | URL | Note |
|---|---|---|
| Search new Chevy inventory | https://www.motorinnofcarroll.com/searchnew.aspx | same site |
| New Silverado 1500 | https://www.motorinnofcarroll.com/searchnew.aspx?Model=Silverado%201500 | same site (filtered search) |
| New Colorado | https://www.motorinnofcarroll.com/searchnew.aspx?Model=Colorado | same site (filtered search) |
| Used trucks and other used vehicles | https://www.motorinnofcarroll.com/searchused.aspx | same site |
| Colorado | https://www.motorinnofcarroll.com/2026-chevrolet-colorado | same site |
| Silverado 1500 | https://www.motorinnofcarroll.com/2026-chevrolet-silverado-ld | same site |
| Silverado HD | https://www.motorinnofcarroll.com/2026-chevrolet-silverado-hd | same site |
| Silverado EV | https://www.motorinnofcarroll.com/2026-chevrolet-silverado-ev | same site |
| heavy-duty vs. light-duty trucks | https://www.motorinnautogroup.com/blog/heavy-duty-vs-light-duty-trucks | cross-site (group) |
| Silverado 1500 vs. Ford F-150 | https://www.motorinnofcarroll.com/silverado-1500-vs-ford-f-150 | same site |
| Silverado 1500 vs. Ram 1500 | https://www.motorinnofcarroll.com/silverado-1500-vs-ram-1500 | same site |
| Search HD inventory | https://www.motorinnofcarroll.com/searchnew.aspx?Model=Silverado%202500%20HD | same site (filtered search) |
| pre-approval page | https://www.motorinnofcarroll.com/preapproved.aspx | same site |
| used trucks page | https://www.motorinnautogroup.com/used-trucks | cross-site (group) |
| trade page | https://www.motorinnofcarroll.com/trade.aspx | same site |

## Cross-links to add after publish (target pages do not exist yet)

- Link from /chevy-dealer-carroll-iowa (Trucks bullet) once live.

## Fact sources used in copy

- Years in business ('family-owned for more than 75 years'): Spencer decision 2026-11-23, matching owner notes '75+' (content/ready-design-OWNER-NOTES.md).
- Address: Chevy contact page (.firecrawl/motorinnofcarroll.com-contactus.aspx.md) lists 'Motor Inn of Carroll, 1526 Le Clark Rd, Carroll, IA 51401'.
- Phone (712) 792-5000: brain/STATE.md ruling 2026-11-02. The 877-775-6741 / 877-733-5984 numbers on the Chevy contact page look like call-tracking numbers and are not printed.
- 'Motor Inn Chevrolet of Carroll' name, 'just off West US Highway 30': group homepage snippet (.firecrawl/nap-audit/20261029/_ap_uest.json).
- Chevrolet certified service, walk-in trade appraisal, lender-network financing, hours: content/ready-design-OWNER-NOTES.md (2026-10-23).
- Model pages and service/finance/trade URLs: Chevy sitemap snapshot brain/research/live-https_www_motorinnofcarroll_com_sitemap_xml.html (2026-11-05).
- No Buick/GMC mentions: content/drafts/buick-gmc-removal-request.md (no longer a Buick or GMC dealer).
- Group blog /blog/heavy-duty-vs-light-duty-trucks and /used-trucks: group sitemap snapshot.

## Review notes for Spencer

- No lease, payment, price or APR figures appear anywhere. Lease and deal queries are answered by sending the shopper to the sales team by phone. The /chevroletspecialoffers page is NOT cited, because the Codex check (2026-11-23) found it lists customer-category programs (military, educator, first responder), not model lease terms.
- Vehicle descriptions are kept qualitative (two-row vs three-row, gas vs electric, light vs heavy duty) with no specs. Spot-check the wording against chevrolet.com before handoff.
- Model-filtered search links use the DealerOn pattern searchnew.aspx?Model=<Model> (the group homepage uses the same pattern). Click-test each filter before handoff. The HD filter uses the live model name 'Silverado 2500 HD' (with a space), which Codex confirmed returns results on 2026-11-23.
- 'ZR2' is used only as an example of a trim the shopper can ask about. No claim is made about stock.
