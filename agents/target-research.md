# 11. Target research file builder (Holmberg step 2)

## Purpose
For each chosen target page/query, assemble the evidence file the writer needs, so drafts
cite reality instead of inventing.

## Inputs
killer_pages.py output; approved target list; DataForSEO creds
(~/.config/motorinn/dataforseo.env, $2/day cap).

## Exact steps
1. mkdir -p brain/research/<slug>/ ; copy brain/research/RESEARCH-TEMPLATE.md -> research.md
2. SERP: POST /v3/serp/google/organic/live/regular (location 2840, language en) for the
   primary query. Fill the top-10 table. Cost ~$0.002.
3. AI citations: POST /v3/serp/google/ai_mode/live/advanced -> ai_overview.references;
   plus /v3/dataforseo_labs/google/domain_mention/live if enabled. Record who gets cited.
4. GA4xGSC: run brain/killer_pages.py, paste this page's row (imps/clicks/pos/keyEvents).
5. Gap pass: Firecrawl-scrape top-3 competitor pages (free first; fallback API ~10 credits),
   list covering/missing/better vs our page. Cite URL per line; write 'missing' if unknown.
6. Unique material: pull from BRIEF.md + DMS-feed facts only. Anything unverifiable ->
   NEEDS-VERIFY flag.
7. Output outline: H2 = exact query phrasings from GSC/DFS; one CTA.
8. Commit brain/research/<slug>/. Draft generation (runbook 12) reads this file ONLY.

## Rules
Max 2 new research files per week (spread cost). Never cite a page you didn't fetch.
