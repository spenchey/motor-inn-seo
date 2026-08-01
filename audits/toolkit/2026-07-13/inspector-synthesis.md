### Inspector Synthesis — 2026-07-13 (weekly staging)

All 6 analyzers OK; no failures [summary.json#analyzers]. The site is **still staging** (`motorinn-website.vercel.app`), which is expected pre-cutover. No new P1 blockers found in this run.

| Domain | State | Evidence |
|---|---|---|
| Crawlability | All AI crawlers allowed (GPTBot, ClaudeBot, PerplexityBot, Google-Extended, etc.) [crawlers.json#ai_crawler_status] | No change vs baseline |
| Robots/indexation | `robots=noindex,nofollow` — expected on staging; MUST flip before cutover [technical.json#meta_tags.robots] = pending cutover action |
| Canonicals | `canonical=https://staging.motorinnautogroup.com` — cross-host canonical from .vercel.app is normal pre-cutover [technical.json#canonical]; at cutover, all URLs on motorinnautogroup.com MUST self-canonicalize (see MOT-2437) |
| Sitemap pointer | robots.txt lists `www.motorinnautogroup.com/sitemap.xml` while the host is motorinn-website.vercel.app [crawlers.json#sitemaps] — verify this points to the live domain at cutover |
| lllms.txt | Present but **format_invalid** — 0 links; needs `- [Title](url)` entries per RFC [llmstxt.json#issues] |
| Image alt texts (**NEW**) | 6/12 vehicle images from DealerOn have **empty alt=""** (VIN-based URLs only): VINs `1GNEVGKW9PJ178289, 3GNAXWEX9JS508056, 3GNAXKEG4RL116830, 4T1F31AK0PU050516, 1FTPX125X5FB10521, 3GNAXUEG1PL229238` [onpage.json#images] — structural-data impact: no alt text propagates to Vehicle JSON-LD Offer |
| Citability | Average 33.7/100 (two F-blocks, one D-block) — zero uniqueness/signals across all blocks [citability.json#average_citability_score; citability.json#all_blocks] |
| Content quality | Overall 91/100 but flagged "repetitive" (score 63) [content-quality.json#flags] |
| Drift | 1 INFO trigger only — content_hash_changed (expected between deploys) [drift.json#triggered_findings]; zero critical/warning triggers [drift.json#summary] |
| Schema blocks | 3 preserved on homepage (AutoDealer + LocalBusiness); not removed vs baseline [drift.json#schema_removed] |

**Change-vs-previous-run**: This run matches MOT-2442's "post-fix" state — self-canonicals and cross-host refs are stable, H1 unchanged, schema present. The **only new finding** is 6 empty alt texts on DealerOn vehicle photos (previously unseen in toolkit data), which may stem from blank VDP spec fields.

---
