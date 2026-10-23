# seo.party gap review — 2026-10-23 (evidence-checked, read-only)

## A) Claim audit
1. AI-visibility audit — PARTIALLY WRONG. Covered: runbook exists (agents/ai-mentions.md:1,
   20 questions, 60 observations); DFS AI-Mode check is wired (agents/weekly-report.md:10) and
   already ran live 2026-09-23 at $0.004 (brain/STATE.md:33). Claim's "only gap = prioritized
   fixes" is too narrow: the runbook has never produced agents/runs output (dir absent), so the
   real gap is execution + a weekly actionable fix loop, not just formatting.
2. Keyword-research parity via DFS — WRONG. agents/keyword-research.md:23 explicitly says
   volume stays null and no paid API calls "in this task", despite creds now existing
   (~/.config/motorinn/dataforseo.env). Pipeline uses DFS keywords_data
   (pipeline/BUILD-REPORT.md) but runbook isn't updated. Not parity.
3. Weekly report markdown vs HTML — PARTIALLY WRONG. agents/weekly-report.md:15 defines a
   <=25-line markdown digest, but no report has ever been written to brain/reports/ (dir empty).
   HTML artifact claim is cosmetic; missing execution is material.
4. Keyword-gap tool — WRONG. tools/skills-sh/opc-seo-geo/scripts/competitor_gap.py:3 already
   implements it via DFS domain_intersection/live. True gap is runbook wiring only.
5. seo-project-setup — TRUE. brain/ (BRIEF, STATE, LOG, SEO-PANEL, VOICE-DNA,
   competitor-read) plus 10 agent runbooks exceeds a setup checklist.

## B) True gaps ranked by Carroll-51401 leads impact
1. Keyword-gap integration into weekly flow (runbook + cron hook) — finds buyer queries
   competitors rank for that we don't (e.g. Choice Auto lead per brain/STATE.md:78).
2. AI-mentions execution + one-fix-per-cycle output — runbook exists, zero runs.
3. Report artifact automation — low lead impact, ops hygiene only.

## C) Top-gap implementation sketch (use existing DFS creds + brain/)
1. New agent task: agents/keyword-gap.md. Inputs: ~/.config/motorinn/dataforseo.env; target
   domains motorinnautogroup.com + two store domains; competitor set from
   brain/competitor-read-2026-09-23.md (choiceauto.biz, wittrockmotor.com, proautosales.net,
   billionauto.com). Reuse tools/skills-sh/opc-seo-geo/scripts/competitor_gap.py pattern:
   POST /v3/dataforseo_labs/google/domain_intersection/live with `intersections=false`,
   `location_code` = Carroll 51401 (or 2840 + county filter), `language_code=en`.
2. Dedupe/whitelist: keep only buyer-intent rows (used, service, financing, test-drive,
   model/CMP); require Carroll/51401 or <=50-mi geography. Map each surviving keyword to an
   existing target page via brain/STATE.md baselines or mark NEW_PAGE candidate.
3. Output: agents/runs/RUN_DATE/keyword-gap.csv (keyword,volume,difficulty,competitor,
   comp_position,our_position,owner_host,target_url,verdict,evidence_path) and pass top rows
   into agents/opportunity-scoring.md flow. Update brain/STATE.md target queue entries;
   $0.05/call cap and $2/day guard from brain/BRIEF.md house rules apply.
