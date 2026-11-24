# SEO draft queue (NOW / NEXT / HOLD / DROP)

Format per motorinn-seo-article-pipeline: family | verdict | evidence (source, date) | confidence | next move.
Cap: NOW holds at most two rows (this week's batch MOT-3708 is owner-directed and grouped as one NOW row of refreshes + one NOW row of cluster drafts).

| Topic family | Verdict | Evidence | Confidence | Next move |
|---|---|---|---|---|
| /used-inventory + /used-suvs copy refresh (Carroll buyer intent, links to top used VDPs) | NOW (batched) | pos 9.3, 16 clicks / 572 impr; 1,330 views, 171s; used_vdp conv 1,849; bounce 0.4% (GSC/GA4 week Nov 9-15 via findings/reports/digital-synthesis-2026-11-23.md) | high | This batch; page gate passed; awaiting owner approval |
| 'carroll iowa car dealerships' cluster expansion (plural-page refresh correcting live 712-522-2526 / 'since 1934' defects + new used-car-dealer page) | NOW (batched) | cluster 169+88+36 impr pos 12-26 (STATE.md); plural week figures 54 impr pos 20.9 (audit-2026-11-23); AI answers 'best used car dealer carroll iowa' cite 4 rivals, us 0/4 (ai-vis-2026-11-23); /car-dealership-carroll-iowa 2,337s avg proves format | high | This batch; fold into F-all-page-draft-unpublished-f6f160 / -7c7f82 package queue |
| Wave-2 six pages (Leg B, deliveries/site-packages/2026-11-15) | NOW (owner decision pending) | register rows F-all-page-draft-unpublished-f6f160 / -7c7f82; package built 2026-11-15 | high | Spencer approves/declines the 2026-11-15 package; our batch joins the same ask |
| Wave-1 city pages (8) + answer pages (3), content/drafts/city-pages (2026-10) | NEXT | drafted 2+ months, unpublished (register row -7c7f82); drafts predate brand kit v2.2 (say 'since 1934', include Buick/GMC wording) | medium | Rewrite-to-standard before any package re-send; the plural-page copy now live shows those defects shipped once - gate everything through page_gate.py + brand kit |
| 'car dealerships near me' | HOLD | pos 4.1, 49 impr already (STATE.md); near-me intent is GBP territory, not an article (pipeline rule) | high | Stays with gbp-velocity-cron; no page |
| /searchused.aspx, /service-area, leadless blog posts | DROP (TRAP) | STATE.md TRAPS rows: real traffic, zero leads | high | No investment |
| Single-town pages beyond Carroll (Lake City, Denison, etc.) | HOLD | town-by-service pages route through motorinn-local-pages and its quarterly plan; not this synthesis item | medium | Feed motorinn-local-pages Q1 review with GSC query pull for each town |
