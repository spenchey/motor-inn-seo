# Brief: chevy-dealer-carroll-iowa

- **Site:** www.motorinnofcarroll.com (Motor Inn Chevrolet of Carroll)
- **URL:** https://www.motorinnofcarroll.com/chevy-dealer-carroll-iowa
- **Status:** NEW page. The Chevy site has no dealer-location landing page; the sitemap snapshot shows none.
- **Intent tier:** ready-now
- **H1:** Chevy Dealer in Carroll, Iowa: Motor Inn Chevrolet of Carroll
- **Primary query:** motor inn of carroll l.l.c. near me
- **AI mirror target (handoff only, not in the mirror file):** Chevy-host mirror (per-host catalog, spenchey/ai-markdown-proxy)

## Routing decision

Chevrolet site (motorinnofcarroll.com). Every query here is Chevrolet-specific dealer or store-name intent, so Spencer's rule sends it to the Chevy store's site.

**This is the biggest clean gap in the export:** about 13,600 impressions at an average position near 24, with almost no clicks. It includes 6,400+ impressions on store-name queries such as "motor inn of carroll l.l.c. near me/chevy/chevrolet", where Google doesn't connect the store's name to a page. There's no existing URL to refresh: the Chevy sitemap has no dealer-location page.

**Caveat on the headline number:** the three "motor inn of carroll l.l.c." rows (6,447 impressions) have zero clicks in 12 months. They also appear in the cached 28-day window: the 28-day cache to 2026-10-16 shows 242 to 278 impressions each on the group property, plus 93 to 168 on the Toyota property, where the Toyota homepage ranks around 14 to 17. That fits a store-name search Google can't resolve, but automated lookups can't be ruled out. Without those rows, this cluster is still about 7,200 impressions at a position near 24, so it stays P1.

## Source evidence (GSC, 12 months ending 2026-11-22)

Source: `ads/gsc-keywords-12mo.json`. Every row in it is labeled `sc-domain:motorinnautogroup.com`. The Chevrolet property is BLOCKED for the service account (`siteUnverifiedUser` in `pipeline/cache/gsc-ebe12c…json`, 2026-10-19). The Toyota property has its own data, which these rows don't include. A ✓ in the Ads-40 column means the query is also one of the 40 exact-match terms in `ads/gsc-ads-package-2026-11-22/keywords.csv`, and that file's landing page is shown.

| Query | Impressions | Clicks | Avg pos | Ads-40 | Current landing page (Ads-40 file) |
|---|---:|---:|---:|:-:|---|
| motor inn of carroll l.l.c. near me | 2268 | 0 | 21.0 |  |  |
| motor inn of carroll l.l.c. chevy | 2138 | 0 | 23.7 |  |  |
| motor inn of carroll l.l.c. chevrolet | 2041 | 0 | 24.1 |  |  |
| chevy carroll iowa | 1573 | 16 | 25.3 |  |  |
| carroll iowa chevy dealers | 1513 | 0 | 26.3 | ✓ | https://www.motorinnautogroup.com/Contactus/Carroll |
| chevrolet carroll iowa | 1417 | 3 | 24.8 |  |  |
| chevy dealer in carroll | 1239 | 1 | 22.6 | ✓ | https://www.motorinnautogroup.com/Contactus/Carroll |
| chevrolet dealer carroll | 583 | 0 | 25.2 | ✓ | https://www.motorinnautogroup.com/Contactus/Carroll |
| chevy dealer carroll ia | 226 | 1 | 17.6 | ✓ | https://www.motorinnautogroup.com/Contactus/Carroll |
| chevy dealer carroll iowa | 168 | 47 | 4.0 | ✓ | https://www.motorinnautogroup.com/Contactus/Carroll |
| motor inn chevrolet of carroll | 143 | 31 | 1.2 |  |  |
| chevy dealer near me | 103 | 14 | 3.0 |  |  |
| carroll chevrolet | 63 | 5 | 2.9 |  |  |
| chevrolet dealer near me | 55 | 2 | 15.5 |  |  |
| chevy dealers near me | 50 | 2 | 8.9 |  |  |
| chevy dealership near me | 28 | 2 | 2.4 |  |  |
| chevy dealers in iowa | 25 | 2 | 20.2 |  |  |

Cluster total: **13,633 impressions** across 17 queries.

## Question phrasing sources

Each H2 and FAQ question follows a real GSC query. Rows marked DERIVED are conversion or support questions with no direct GSC row (10+ impressions), answered from owner-verified facts.

| Question | Where | GSC query it follows | Impressions |
|---|---|---|---:|
| Where is the Chevy dealer in Carroll, Iowa? | H2 | chevy dealer carroll iowa | 168 |
| Is Motor Inn of Carroll a Chevrolet dealer? | H2 | motor inn of carroll l.l.c. chevrolet | 2041 |
| Which new Chevrolet models can I shop in Carroll? | H2 | chevrolet carroll iowa | 1417 |
| Does the Chevy dealer in Carroll service Chevrolets? | H2 | DERIVED | |
| Can I trade in or sell my car at the Carroll Chevy dealer? | H2 | DERIVED | |
| Can I get Chevy financing in Carroll? | H2 | DERIVED | |
| Is there a Chevy dealer near me? | H2 | chevy dealer near me | 103 |
| Where is the Chevy dealer in Carroll, Iowa? | FAQ | chevy dealer carroll iowa | 168 |
| Is Motor Inn of Carroll a Chevrolet dealer? | FAQ | motor inn of carroll l.l.c. chevrolet | 2041 |
| Does the Chevy dealer in Carroll, Iowa, do Chevrolet service? | FAQ | DERIVED | |
| Can I trade in my car at the Carroll Chevy dealer without an appointment? | FAQ | DERIVED | |
| Is there a Chevy dealer and a Toyota dealer at the same place in Carroll? | FAQ | motor inn toyota and chevrolet of carroll | 114 |

## Internal links (all verified in the 2026-11-05 sitemap snapshots in `brain/research/`)

| Anchor | URL | Note |
|---|---|---|
| Get hours and directions | https://www.motorinnofcarroll.com/hours.aspx | same site |
| About Motor Inn of Carroll | https://www.motorinnofcarroll.com/aboutus.aspx | same site |
| new Chevrolet inventory search | https://www.motorinnofcarroll.com/searchnew.aspx | same site |
| Colorado | https://www.motorinnofcarroll.com/2026-chevrolet-colorado | same site |
| Silverado 1500 | https://www.motorinnofcarroll.com/2026-chevrolet-silverado-ld | same site |
| Silverado HD | https://www.motorinnofcarroll.com/2026-chevrolet-silverado-hd | same site |
| Silverado EV | https://www.motorinnofcarroll.com/2026-chevrolet-silverado-ev | same site |
| Trax | https://www.motorinnofcarroll.com/2026-chevrolet-trax | same site |
| Trailblazer | https://www.motorinnofcarroll.com/2026-chevrolet-trailblazer | same site |
| Equinox | https://www.motorinnofcarroll.com/2026-chevrolet-equinox | same site |
| Blazer | https://www.motorinnofcarroll.com/2026-chevrolet-blazer | same site |
| Traverse | https://www.motorinnofcarroll.com/2026-chevrolet-traverse | same site |
| Tahoe | https://www.motorinnofcarroll.com/2026-chevrolet-tahoe | same site |
| Suburban | https://www.motorinnofcarroll.com/2026-chevrolet-suburban | same site |
| Equinox EV | https://www.motorinnofcarroll.com/2026-chevrolet-equinox-ev | same site |
| Blazer EV | https://www.motorinnofcarroll.com/2026-chevrolet-blazer-ev | same site |
| quote page | https://www.motorinnofcarroll.com/quote.aspx | same site |
| service page | https://www.motorinnofcarroll.com/service | same site |
| collision shop | https://www.motorinnofcarroll.com/collision-shop | same site |
| trade page | https://www.motorinnofcarroll.com/trade.aspx | same site |
| We Buy Cars | https://www.motorinnofcarroll.com/we-buy-cars.html | same site |
| pre-approval page | https://www.motorinnofcarroll.com/preapproved.aspx | same site |
| financing page | https://www.motorinnofcarroll.com/finance.aspx | same site |

## Cross-links to add after publish (target pages do not exist yet)

- Add a link to this page from motorinnofcarroll.com/aboutus.aspx and the Chevy homepage, so it isn't orphaned.
- Link this page from the new chevy-suvs, chevy-blazer and chevy-trucks pages, and the reverse, once all four are live.
- Link from motorinnautogroup.com/contactus.aspx ('Chevy dealer in Carroll').

## Fact sources used in copy

- Years in business ('family-owned for more than 75 years'): Spencer decision 2026-11-23, matching owner notes '75+' (content/ready-design-OWNER-NOTES.md).
- Address: Chevy contact page (.firecrawl/motorinnofcarroll.com-contactus.aspx.md) lists 'Motor Inn of Carroll, 1526 Le Clark Rd, Carroll, IA 51401'.
- Phone (712) 792-5000: brain/STATE.md ruling 2026-11-02. The 877-775-6741 / 877-733-5984 numbers on the Chevy contact page look like call-tracking numbers and are not printed.
- 'Motor Inn Chevrolet of Carroll' name, 'just off West US Highway 30': group homepage snippet (.firecrawl/nap-audit/20261029/_ap_uest.json).
- Chevrolet certified service, walk-in trade appraisal, lender-network financing, hours: content/ready-design-OWNER-NOTES.md (2026-10-23).
- Model pages and service/finance/trade URLs: Chevy sitemap snapshot brain/research/live-https_www_motorinnofcarroll_com_sitemap_xml.html (2026-11-05).
- No Buick/GMC mentions: content/drafts/buick-gmc-removal-request.md (no longer a Buick or GMC dealer).
- Service-area towns: brain/VOICE-DNA.md and Toyota-site sitemap town pages (used here as places shoppers drive in from, not as store locations).

## Review notes for Spencer

- The store's legal name ('Motor Inn of Carroll L.L.C.') appears only in searcher queries, never in repo facts, so the copy uses 'Motor Inn of Carroll' and 'Motor Inn Chevrolet of Carroll', which both appear on the live sites.
- brain/STATE.md (2026-09-23) notes that the Chevy store has no distinct GBP listing surfaced by name. This page helps, but a Chevy GBP entity fix would help more.
- Spirit Lake, Estherville, Algona and Monona queries are dropped: Motor Inn is Carroll only, with no store there (Spencer, 2026-11-23).
- Vehicle descriptions are kept qualitative (two-row vs three-row, gas vs electric, light vs heavy duty) with no specs. Spot-check the wording against chevrolet.com before handoff.
