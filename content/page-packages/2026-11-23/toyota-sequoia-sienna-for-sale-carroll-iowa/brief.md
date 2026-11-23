# Brief: toyota-sequoia-sienna-for-sale-carroll-iowa

- **Site:** www.motorinntoyotaofcarroll.com (Motor Inn Toyota of Carroll)
- **URL:** https://www.motorinntoyotaofcarroll.com/toyota-sequoia-sienna-for-sale-carroll-iowa
- **Status:** NEW page. The Toyota site has model research pages (/2026-toyota-sequoia.html, /toyota-sienna) but no 'for sale' shopping page.
- **Intent tier:** ready-now
- **H1:** Toyota Sequoia and Sienna for Sale in Carroll, Iowa
- **Primary query:** toyota sequoia for sale
- **AI mirror target (handoff only, not in the mirror file):** Toyota-host mirror (per-host catalog, spenchey/ai-markdown-proxy)

## Routing decision

Toyota site. These are new-Toyota model shopping queries.

**Why one page for two models:** each model has about 130 to 170 impressions, too thin for its own page. Both are three-row family vehicles that buyers cross-shop. "what toyota is bigger than a highlander" (position 4.2) fits here as a size-up question.

## Source evidence (GSC, 12 months ending 2026-11-22)

Source: `ads/gsc-keywords-12mo.json`. Every row in it is labeled `sc-domain:motorinnautogroup.com`. The Chevrolet property is BLOCKED for the service account (`siteUnverifiedUser` in `pipeline/cache/gsc-ebe12c…json`, 2026-10-19). The Toyota property has its own data, which these rows don't include. A ✓ in the Ads-40 column means the query is also one of the 40 exact-match terms in `ads/gsc-ads-package-2026-11-22/keywords.csv`, and that file's landing page is shown.

| Query | Impressions | Clicks | Avg pos | Ads-40 | Current landing page (Ads-40 file) |
|---|---:|---:|---:|:-:|---|
| toyota sequoia for sale | 136 | 1 | 5.1 | ✓ | https://www.motorinnautogroup.com/Contactus/Carroll |
| toyota sienna for sale | 132 | 1 | 3.1 | ✓ | https://www.motorinnautogroup.com/Contactus/Carroll |
| toyota sequoia for sale near me | 30 | 0 | 8.1 |  |  |
| what toyota is bigger than a highlander | 13 | 0 | 4.2 |  |  |

Cluster total: **311 impressions** across 4 queries.

## Question phrasing sources

Each H2 and FAQ question follows a real GSC query. Rows marked DERIVED are conversion or support questions with no direct GSC row (10+ impressions), answered from owner-verified facts.

| Question | Where | GSC query it follows | Impressions |
|---|---|---|---:|
| Where can I find a Toyota Sequoia for sale near me? | H2 | toyota sequoia for sale near me | 30 |
| Is a Toyota Sienna for sale near Carroll? | H2 | toyota sienna for sale | 132 |
| Sequoia or Sienna: which fits your family? | H2 | DERIVED | |
| What Toyota is bigger than a Highlander? | H2 | what toyota is bigger than a highlander | 13 |
| Can I buy a used Sequoia or Sienna in Carroll? | H2 | DERIVED | |
| Where can I find a Toyota Sequoia for sale near Carroll, Iowa? | FAQ | toyota sequoia for sale | 136 |
| Is a Toyota Sienna for sale in Carroll, Iowa? | FAQ | toyota sienna for sale | 132 |
| Should I buy a Toyota Sequoia or a Toyota Sienna? | FAQ | DERIVED | |
| What Toyota is bigger than a Highlander? | FAQ | what toyota is bigger than a highlander | 13 |

## Internal links (all verified in the 2026-11-05 sitemap snapshots in `brain/research/`)

| Anchor | URL | Note |
|---|---|---|
| new Sequoia inventory | https://www.motorinntoyotaofcarroll.com/searchnew.aspx?Model=Sequoia | same site (filtered search) |
| new Sienna inventory | https://www.motorinntoyotaofcarroll.com/searchnew.aspx?Model=Sienna | same site (filtered search) |
| Sequoia model page | https://www.motorinntoyotaofcarroll.com/2026-toyota-sequoia.html | same site |
| Sienna model page | https://www.motorinntoyotaofcarroll.com/toyota-sienna | same site |
| test drive page | https://www.motorinntoyotaofcarroll.com/testdrive.aspx | same site |
| Highlander vs. Grand Highlander | https://www.motorinnautogroup.com/highlander-vs-grand-highlander | cross-site (group) |
| Grand Highlander model page | https://www.motorinntoyotaofcarroll.com/2026-toyota-grand-highlander.html | same site |
| Toyota Certified Pre-Owned | https://www.motorinntoyotaofcarroll.com/certified-pre-owned.html | same site |
| used inventory search | https://www.motorinntoyotaofcarroll.com/searchused.aspx | same site |
| pre-approval page | https://www.motorinntoyotaofcarroll.com/preapproved.aspx | same site |

## Cross-links to add after publish (target pages do not exist yet)

- Link from /toyota-dealers-in-iowa ('What can I buy') once live, and from the /toyota-sienna and /2026-toyota-sequoia.html model pages.

## Fact sources used in copy

- Address, store name: Toyota contact page (.firecrawl/motorinntoyotaofcarroll.com-contactus.aspx.md), 'Motor Inn Toyota Of Carroll, 1526 Le Clark Road, Carroll, IA 51401'.
- Phone (712) 792-5000: required on customer-facing Toyota copy (brief + brain/STATE.md ruling 2026-11-02). The 712-513-xxxx numbers on the Toyota contact page look like tracking numbers and are not printed. 522-2526 is never used.
- 'Just off West US Highway 30': group homepage snippet (.firecrawl/nap-audit/20261029/_ap_uest.json).
- Walk-in trade appraisal, lender-network financing, hours: content/ready-design-OWNER-NOTES.md (2026-10-23).
- Model, CPO, service and town pages: Toyota sitemap snapshot brain/research/live-https_www_motorinntoyotaofcarroll_com_sitemap_xml.html (2026-11-05).
- Highlander vs. Grand Highlander page: group sitemap snapshot (live).

## Review notes for Spencer

- Vehicle descriptions are kept qualitative (midsize vs full-size, SUV vs minivan) with no specs. 'i-FORCE MAX' (name only, no powertrain type claimed) comes from the live Tundra offer URL on both sites. Spot-check the wording against toyota.com before handoff.
- Model-filtered search links use the DealerOn pattern searchnew.aspx?Model=<Model>. Click-test each filter before handoff.
- 'is the sequoia built on the tundra frame' (11 impressions) is NOT answered, because there's no repo source for platform facts. Add it if Spencer supplies an OEM source.
- '2024 toyota sequoia sr5' (36 impressions) is a single-used-unit query and isn't targeted.
