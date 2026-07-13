## GEO/SEO Toolkit Findings — https://motorinn-website.vercel.app — 2026-07-13 (weekly)

_Deterministic analyzer battery (MOT-2431): vendored claude-seo + geo-seo-claude (tools/PROVENANCE.md). Synthesis is templated from analyzer scores — no LLM in this path. Checklists: tools/skills-sh/marketingskills-seo-audit/SKILL.md, tools/skills-sh/opc-seo-geo/SKILL.md._

### P1 — fix now

- none

### P2 — this month

- [crawlers.json#sitemaps] robots.txt Sitemap points at `www.motorinnautogroup.com` while the audited site is `motorinn-website.vercel.app` — crawlers on this host are handed another domain's sitemap. Verify this is intended pre-cutover, and that it flips at cutover.
- [llmstxt.json#issues] llms.txt exists but has 1 validation issue(s): No page links found (use '- [Page Title](url): Description')
- [citability.json#average_citability_score] Citability 33.7/100 — AI engines are unlikely to quote this page; restructure toward self-contained 130-170 word answer passages (tools/skills-sh/opc-seo-geo/SKILL.md).

### P3 / info

- [crawlers.json#ai_crawler_status] All tracked AI crawlers allowed (GPTBot, ClaudeBot, PerplexityBot, CCBot, ...).
- [technical.json#canonical] Canonical points at `staging.motorinnautogroup.com` (audited host `motorinn-website.vercel.app`) — expected on staging pre-cutover; MUST flip at cutover.
- [technical.json#meta_tags.robots] noindex present — expected on the staging host; MUST be removed at cutover.
- [onpage.json#images] 6/12 image(s) missing alt text.
- [drift.json#summary] No SEO element drift vs last baseline.
- [citability.json#all_blocks] Low-citability block (score 25): "New Toyotas & Chevrolets, plus a wide used inventory of every make — o..."
- [citability.json#all_blocks] Low-citability block (score 30): "1526 Le Clark Road, Carroll, IA 51401 Sales: Mon–Fri 8:00 AM – 5:30 PM..."
- [citability.json#all_blocks] Low-citability block (score 46): "Yes. Our one-stop financial services center works with 20+ lenders to..."
- ...plus 1 more (see analyzer JSON).

### Analyzer scores

| Analyzer | Metric | Value |
|---|---|---:|
| onpage | homepage word count | 961 |
| onpage | JSON-LD blocks on homepage | 3 |
| drift | critical changes vs baseline | 0 |
| drift | warning changes vs baseline | 0 |
| citability | content blocks analyzed | 3 |
| citability | average citability score (0-100) | 33.7 |
| content-quality | overall quality (0-100) | 91 |
| sitemap | URLs discovered via sitemap | 50 |

Machine output: `audits/toolkit/2026-07-13/` (JSON per analyzer + summary.json).
