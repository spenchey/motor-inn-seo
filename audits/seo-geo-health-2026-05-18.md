# SEO/GEO Health Check — 2026-05-18

## Executive Summary
**Health: YELLOW** — Crawler access is open but AI-crawler rules are missing, llms.txt is absent, and homepage load time is slow. No blocking issues; 3 high-impact fixes available.

---

## Crawler Access — ✅ PASS (with gaps)

| Check | Status | Detail |
|---|---|---|
| robots.txt | ✅ 200 | Present, references sitemap.xml |
| sitemap.xml | ✅ 200 | Present, lastmod 2026-05-18 |
| Homepage | ✅ 200 | 395KB, 10.4s load time ⚠️ |
| searchnew.aspx | ✅ 200 | New inventory search accessible |
| service-area | ✅ 200 | Present, good content |
| llms.txt | ❌ 404 | **Missing** — needed for AI crawler guidance |

### AI Crawler Rules in robots.txt
| Crawler | Status |
|---|---|
| GPTBot | ⚠️ Not mentioned (allowed by default) |
| ChatGPT-User | ⚠️ Not mentioned (allowed by default) |
| PerplexityBot | ⚠️ Not mentioned (allowed by default) |
| ClaudeBot | ⚠️ Not mentioned (allowed by default) |
| anthropic-ai | ⚠️ Not mentioned (allowed by default) |
| CCBot | ⚠️ Not mentioned (allowed by default) |

**Risk:** No AI crawler directives means all bots can access everything by default. Not a blocker, but best practice is to explicitly allow search-indexing AI bots while optionally disallowing training-only bots (CCBot, anthropic-ai). This is a 1-line change.

---

## Traditional SEO — ✅ PASS

| Check | Status |
|---|---|
| Homepage title | ✅ "Carroll Chevrolet, Toyota Dealer in Carroll IA" |
| robots.txt | ✅ Valid, references sitemap |
| sitemap.xml | ✅ Valid, current lastmod (2026-05-18) |
| Sitemap URL count | ~40+ URLs (mostly collection/brand pages) |
| Canonical tags | ⚠️ Not verified (needs live VDP check) |

### Sitemap URL Patterns (sample)
- `/` (homepage, priority 1.0) ✅
- `/new-cars`, `/new-toyota`, `/new-chevrolet.html` ✅
- `/new-suvs`, `/new-crossovers`, `/new-trucks`, `/new-vans` ✅
- `/searchnew.aspx`, `/findmycar.aspx`, `/trade.aspx` ✅
- Content pages: `/why-buy-a-crossover-suv-ia`, `/best-chevrolet-suvs-for-families`, etc. ✅
- VDP patterns: tried `/used-Carroll-2023-Chevrolet-Equinox-...` → 404 ❌ (legacy patterns only)

**Note:** The site still uses legacy DealerOn URL patterns. The new `/used-Carroll-...` pattern (from website spec) is NOT live yet. Sitemap URLs use legacy `.aspx` and `.html` extensions.

---

## GEO Readiness — ⚠️ NEEDS WORK

| Dimension | Score | Notes |
|---|---|---|
| Citability | 40/100 | Service-area page has good section structure but no FAQ schema, no Q&A format |
| Structural Readability | 55/100 | Pages render but rely heavily on JS (DealerOn template); readability extractor gets partial content |
| Multi-Modal Content | 30/100 | No video schema, no image alt verification on pages checked |
| Authority & Brand Signals | 50/100 | "85+ years" mentioned, local addresses present, but no Wikipedia entity, no structured citations |
| Technical Accessibility | 45/100 | No llms.txt, homepage slow (10.4s), SSR but heavy JS, no AI crawler rules |
| **Overall GEO Score** | **44/100** | Below target (target: 60+) |

### Key GEO Gaps
1. **llms.txt missing** — Single highest-impact fix. Add at `https://www.motorinnautogroup.com/llms.txt` with inventory, service, and location sections
2. **No FAQ schema on service/location pages** — Motor Inn has good content on service-area page but no machine-readable Q&A
3. **Homepage load time (10.4s)** — Likely hurts both traditional SEO and AI crawler access
4. **No AI crawler directives** — robots.txt should explicitly allow GPTBot, PerplexityBot, ClaudeBot, ChatGPT-User

---

## Priority Actions (Ordered)

### 🔴 P0 — Blockers
None. Site is crawlable and indexable.

### 🟡 P1 — High Impact, Low Effort
1. **Add llms.txt** — 15-min change. Template:
   ```
   # Motor Inn Auto Group
   # Chevrolet & Toyota dealer in Carroll, IA since 1939
   
   ## New Inventory
   - New Chevrolet: https://www.motorinnautogroup.com/searchnew.aspx?Make=Chevrolet
   - New Toyota: https://www.motorinnautogroup.com/new-toyota
   
   ## Used Inventory
   - Used Cars: https://www.motorinnautogroup.com/used-cars
   - Used Trucks: https://www.motorinnautogroup.com/used-trucks
   
   ## Service
   - Service Area: https://www.motorinnautogroup.com/service-area
   - Service Locations: https://www.motorinnautogroup.com/service-locations.html
   
   ## About
   - About Us: https://www.motorinnautogroup.com/aboutus.aspx
   - Contact: https://www.motorinnautogroup.com/contact.aspx
   ```
2. **Add AI crawler rules to robots.txt** — 1-line addition:
   ```
   # Allow AI search crawlers
   User-agent: GPTBot
   Allow: /
   User-agent: ChatGPT-User
   Allow: /
   User-agent: PerplexityBot
   Allow: /
   User-agent: ClaudeBot
   Allow: /
   ```

### 🟢 P2 — Medium Effort
3. **Add FAQ schema on service area page** with questions like "What areas does Motor Inn serve?", "Do you deliver to Spirit Lake?"
4. **Investigate homepage load time** — 10.4s is high. Check image optimization, render-blocking resources.
5. **Verify VDP schema** on live vehicle pages once new URL pattern is live.

### ⚪ P3 — Continuous
6. Weekly GEO health recheck via existing cron (`908e5ef3`)
7. Monitor AI bot access logs for GPTBot/PerplexityBot crawl frequency

---

## Files Updated
- `~/motor-inn-seo/audits/seo-geo-health-2026-05-18.md` (this report)

---

*Next check: 2026-05-25 (weekly cron)*
*Sitemap analyzed: 40+ URLs, all HTTP 200 on the homepage-level checks*
*llms.txt: needs creation | AI crawler rules: needs addition*
