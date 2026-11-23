# Brief: toyota-tacoma-tundra-for-sale-carroll-iowa

- **Site:** www.motorinntoyotaofcarroll.com (Motor Inn Toyota of Carroll)
- **URL:** https://www.motorinntoyotaofcarroll.com/toyota-tacoma-tundra-for-sale-carroll-iowa
- **Status:** NEW page. The Toyota site has model research pages (/toyota-tacoma, /2026-toyota-tundra.html) but no 'for sale' shopping page. An unpublished content/ready-design/toyota-tacoma-carroll-iowa.html draft exists without a set canonical; see the routing note.
- **Intent tier:** ready-now
- **H1:** Toyota Tacoma and Tundra for Sale in Carroll, Iowa
- **Primary query:** toyota tacoma for sale
- **AI mirror target (handoff only, not in the mirror file):** Toyota-host mirror (per-host catalog, spenchey/ai-markdown-proxy)

## Routing decision

Toyota site. These are new-Toyota truck shopping queries.

**Why one page for two models:** each model alone is thin (Tacoma about 290 impressions, Tundra about 180), and truck shoppers often compare the two. Splitting can wait until each model shows more volume in GSC.

**Used intent excluded:** "used toyota tacoma" (79 impressions) is used intent, which the routing rule sends to the group site, so it is not targeted here. The used section on this page is a support cross-link only.

**Conflict with an earlier draft:** content/ready-design/toyota-tacoma-carroll-iowa.html covers Tacoma-in-Carroll on the group site. Under the 2026-11-23 rule, new-Toyota model intent belongs on the Toyota site, so don't publish both.

## Source evidence (GSC, 12 months ending 2026-11-22)

Source: `ads/gsc-keywords-12mo.json`. Every row in it is labeled `sc-domain:motorinnautogroup.com`. The Chevrolet property is BLOCKED for the service account (`siteUnverifiedUser` in `pipeline/cache/gsc-ebe12c…json`, 2026-10-19). The Toyota property has its own data, which these rows don't include. A ✓ in the Ads-40 column means the query is also one of the 40 exact-match terms in `ads/gsc-ads-package-2026-11-22/keywords.csv`, and that file's landing page is shown.

| Query | Impressions | Clicks | Avg pos | Ads-40 | Current landing page (Ads-40 file) |
|---|---:|---:|---:|:-:|---|
| toyota tacoma for sale | 239 | 4 | 2.9 | ✓ | https://www.motorinnautogroup.com/Contactus/Carroll |
| toyota tundra for sale | 150 | 3 | 6.4 | ✓ | https://www.motorinnautogroup.com/Contactus/Carroll |
| toyota tacoma for sale near me | 52 | 1 | 2.2 |  |  |
| toyota tundra for sale trd pro | 32 | 0 | 10.0 |  |  |

Cluster total: **473 impressions** across 4 queries.

## Question phrasing sources

Each H2 and FAQ question follows a real GSC query. Rows marked DERIVED are conversion or support questions with no direct GSC row (10+ impressions), answered from owner-verified facts.

| Question | Where | GSC query it follows | Impressions |
|---|---|---|---:|
| Where can I find a Toyota Tacoma for sale near me? | H2 | toyota tacoma for sale near me | 52 |
| Is a Toyota Tundra for sale in Carroll? | H2 | toyota tundra for sale | 150 |
| Tacoma or Tundra: which Toyota truck fits? | H2 | DERIVED | |
| Can I buy a used Toyota Tacoma? | H2 | DERIVED | |
| Can I trade in and finance a Toyota truck in Carroll? | H2 | DERIVED | |
| Where can I find a Toyota Tacoma for sale near Carroll, Iowa? | FAQ | toyota tacoma for sale | 239 |
| Is a Toyota Tundra for sale in Carroll, Iowa? | FAQ | toyota tundra for sale trd pro | 32 |
| What is the difference between the Toyota Tacoma and Tundra? | FAQ | DERIVED | |

## Internal links (all verified in the 2026-11-05 sitemap snapshots in `brain/research/`)

| Anchor | URL | Note |
|---|---|---|
| new Tacoma inventory | https://www.motorinntoyotaofcarroll.com/searchnew.aspx?Model=Tacoma | same site (filtered search) |
| new Tundra inventory | https://www.motorinntoyotaofcarroll.com/searchnew.aspx?Model=Tundra | same site (filtered search) |
| Tacoma model page | https://www.motorinntoyotaofcarroll.com/toyota-tacoma | same site |
| 2027 Tacoma TRD Pro | https://www.motorinnautogroup.com/blog/2027-toyota-tacoma-trd-pro-honeycomb-reservation-interest | cross-site (group) |
| Tundra model page | https://www.motorinntoyotaofcarroll.com/2026-toyota-tundra.html | same site |
| test drive page | https://www.motorinntoyotaofcarroll.com/testdrive.aspx | same site |
| Toyota Certified Pre-Owned | https://www.motorinntoyotaofcarroll.com/certified-pre-owned.html | same site |
| used inventory search | https://www.motorinntoyotaofcarroll.com/searchused.aspx | same site |
| used trucks | https://www.motorinnautogroup.com/used-trucks | cross-site (group) |
| trade page | https://www.motorinntoyotaofcarroll.com/trade.aspx | same site |
| pre-approval page | https://www.motorinntoyotaofcarroll.com/preapproved.aspx | same site |
| specials page | https://www.motorinntoyotaofcarroll.com/newspecials.html | same site |

## Cross-links to add after publish (target pages do not exist yet)

- Link from /toyota-dealers-in-iowa ('What can I buy') once live, and from the /toyota-tacoma model page.

## Fact sources used in copy

- Address, store name: Toyota contact page (.firecrawl/motorinntoyotaofcarroll.com-contactus.aspx.md), 'Motor Inn Toyota Of Carroll, 1526 Le Clark Road, Carroll, IA 51401'.
- Phone (712) 792-5000: required on customer-facing Toyota copy (brief + brain/STATE.md ruling 2026-11-02). The 712-513-xxxx numbers on the Toyota contact page look like tracking numbers and are not printed. 522-2526 is never used.
- 'Just off West US Highway 30': group homepage snippet (.firecrawl/nap-audit/20261029/_ap_uest.json).
- Walk-in trade appraisal, lender-network financing, hours: content/ready-design-OWNER-NOTES.md (2026-10-23).
- Model, CPO, service and town pages: Toyota sitemap snapshot brain/research/live-https_www_motorinntoyotaofcarroll_com_sitemap_xml.html (2026-11-05).
- 'i-FORCE MAX': live offer URLs offerdetails-New-Carroll-Iowa-2026-Toyota-Tundra-i-FORCE-MAX-… in both sitemaps.
- 2027 Tacoma TRD Pro blog post: group sitemap snapshot.

## Review notes for Spencer

- Vehicle descriptions are kept qualitative (midsize vs full-size, SUV vs minivan) with no specs. 'i-FORCE MAX' (name only, no powertrain type claimed) comes from the live Tundra offer URL on both sites. Spot-check the wording against toyota.com before handoff.
- Model-filtered search links use the DealerOn pattern searchnew.aspx?Model=<Model>. Click-test each filter before handoff.
- The 2027 Tacoma TRD Pro blog link is described only as 'our post'. Its reservation content wasn't verified.
