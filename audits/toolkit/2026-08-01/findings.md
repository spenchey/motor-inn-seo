## GEO/SEO Toolkit Findings — https://motorinn-website.vercel.app — 2026-08-01 (monthly)

_Deterministic analyzer battery (MOT-2431): vendored claude-seo + geo-seo-claude (tools/PROVENANCE.md). Synthesis is templated from analyzer scores — no LLM in this path. Checklists: tools/skills-sh/marketingskills-seo-audit/SKILL.md, tools/skills-sh/opc-seo-geo/SKILL.md._

### P1 — fix now

- none

### P2 — this month

- [crawlers.json#sitemaps] robots.txt Sitemap points at `www.motorinnautogroup.com` while the audited site is `motorinn-website.vercel.app` — crawlers on this host are handed another domain's sitemap. Verify this is intended pre-cutover, and that it flips at cutover.
- [llmstxt.json#issues] llms.txt exists but has 1 validation issue(s): No page links found (use '- [Page Title](url): Description')
- [citability.json#average_citability_score] Citability 35.0/100 — AI engines are unlikely to quote this page; restructure toward self-contained 130-170 word answer passages (tools/skills-sh/opc-seo-geo/SKILL.md).

### P3 / info

- [crawlers.json#ai_crawler_status] All tracked AI crawlers allowed (GPTBot, ClaudeBot, PerplexityBot, CCBot, ...).
- [technical.json#canonical] Canonical points at `staging.motorinnautogroup.com` (audited host `motorinn-website.vercel.app`) — expected on staging pre-cutover; MUST flip at cutover.
- [technical.json#meta_tags.robots] noindex present — expected on the staging host; MUST be removed at cutover.
- [drift.json#summary] No SEO element drift vs last baseline.
- [citability.json#all_blocks] Low-citability block (score 25): "New Toyotas & Chevrolets, plus a wide used inventory of every make — o..."
- [citability.json#all_blocks] Low-citability block (score 30): "1526 Le Clark Road, Carroll, IA 51401 Sales:Mon–Fri 8:00 AM – 5:30 PM..."
- [citability.json#all_blocks] Low-citability block (score 50): "Yes. Our one-stop financial services center works with 20+ lenders to..."
- [brand.json#platforms] No confirmed brand-presence signal on: linkedin, reddit, wikipedia, youtube — these correlate strongest with AI citations (YouTube 0.737); manual check URLs are in brand.json.

### Analyzer scores

| Analyzer | Metric | Value |
|---|---|---:|
| onpage | homepage word count | 1230 |
| onpage | JSON-LD blocks on homepage | 3 |
| drift | critical changes vs baseline | 0 |
| drift | warning changes vs baseline | 0 |
| citability | content blocks analyzed | 3 |
| citability | average citability score (0-100) | 35.0 |
| content-quality | overall quality (0-100) | 90 |
| sitemap | URLs discovered via sitemap | 50 |

Machine output: `audits/toolkit/2026-08-01/` (JSON per analyzer + summary.json).
