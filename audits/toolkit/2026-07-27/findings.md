## GEO/SEO Toolkit Findings — https://motorinn-website.vercel.app — 2026-07-27 (weekly)

_Deterministic analyzer battery (MOT-2431): vendored claude-seo + geo-seo-claude (tools/PROVENANCE.md). Synthesis is templated from analyzer scores — no LLM in this path. Checklists: tools/skills-sh/marketingskills-seo-audit/SKILL.md, tools/skills-sh/opc-seo-geo/SKILL.md._

### P1 — fix now

- none

### P2 — this month

- [crawlers.json#sitemaps] robots.txt Sitemap points at `www.motorinnautogroup.com` while the audited site is `motorinn-website.vercel.app` — crawlers on this host are handed another domain's sitemap. Verify this is intended pre-cutover, and that it flips at cutover.
- [llmstxt.json#issues] llms.txt exists but has 1 validation issue(s): No page links found (use '- [Page Title](url): Description')

### P3 / info

- [crawlers.json#ai_crawler_status] All tracked AI crawlers allowed (GPTBot, ClaudeBot, PerplexityBot, CCBot, ...).
- [technical.json#canonical] Canonical points at `staging.motorinnautogroup.com` (audited host `motorinn-website.vercel.app`) — expected on staging pre-cutover; MUST flip at cutover.
- [technical.json#meta_tags.robots] noindex present — expected on the staging host; MUST be removed at cutover.
- [drift.json#summary] No SEO element drift vs last baseline.

### Analyzer scores

| Analyzer | Metric | Value |
|---|---|---:|
| onpage | homepage word count | 1232 |
| onpage | JSON-LD blocks on homepage | 3 |
| drift | critical changes vs baseline | 0 |
| drift | warning changes vs baseline | 0 |

Machine output: `audits/toolkit/2026-07-27/` (JSON per analyzer + summary.json).
