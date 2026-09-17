# 5. Page opportunity scoring

## Purpose
Rank local purchase/service pages by traffic potential multiplied by ease of execution, with an explicit 50501 shopper view.

## Inputs
Jobs 1–4; current inventory/category availability; existing page/canonical map; estimated DealerOn authoring and QA hours; GSC export when available. Use the README geography rules.

## Exact steps
1. Create one candidate row per canonical page and primary intent. Group overlapping synonyms; do not score duplicate city pages as independent demand.
2. Assign `core` for Carroll/Lake City/Denison/Audubon/Storm Lake/Sac City; assign `50501-Fort-Dodge` only for an explicit Fort Dodge/50501 query or separately verified local source. Add other expansion markets separately. A GSC country filter cannot isolate 50501 shoppers.
3. Compute traffic potential T from one documented source: 28-day non-brand impressions for the cluster on its owning property. Use T=1 for 1–49, 2 for 50–199, 3 for 200–499, 4 for 500–999, 5 for >=1,000. Zero observed impressions gets T=0 with coverage noted. Deduplicate page overlaps by query before estimating cluster demand; use query-only totals when available, not a sum of duplicated page rows.
4. If GSC is unavailable, use a dated, approved localized keyword-volume source with the same bins and mark `volume-proxy`. Do not equate volume with expected visits. If neither exists, T=null and numeric score=null. Create a provisional qualitative queue using buyer evidence, current stock/service relevance and implementation readiness; do not invent numeric traffic potential.
5. Estimate total hours including content, DealerOn coordination, link work, QA and required approvals. Ease E=5 for <=2h; 4 for >2–4h; 3 for >4–8h; 2 for >8–16h; 1 for >16h. The formula rewards lower effort: `base_score = T × E`, range 0–25. Do not multiply traffic by raw hours, which would reward expensive work.
6. Set relevance R=1 for verified supported inventory/service and matching geography, R=0.5 for a relevant category with unconfirmed availability, R=0 for unsupported offerings or a wrong entity. `priority_score = base_score × R`. A factual or routing blocker adds `HOLD` regardless of score.
7. Record evidence confidence: HIGH=current direct query evidence and verified offer; MEDIUM=dated localized volume proxy; LOW=qualitative only. Sort eligible rows by priority_score descending, confidence HIGH before MEDIUM, hours ascending, then canonical URL alphabetically. Keep null scores in a separate provisional list.
8. Publish separate core and 50501 views. Show five candidates per view if available, otherwise all available with missing-count explanation. Do not call 50501 Carroll. Feed only reviewed candidates to job 7.

## Worked arithmetic example (fictional, not measured)
A used-trucks page with 650 eligible impressions has T=4. Estimated 3 hours gives E=4. Verified offer/geography gives R=1. Score=16. A 12-hour candidate with the same traffic has E=2 and score=8. Missing GSC and volume data yields no numerical score.

## Output artifact path
`/Users/spencerheywood/motor-inn-seo/agents/runs/RUN_DATE/opportunity-scoring.csv`
Columns: `candidate_id,host,url,intent,market_segment,demand_source,source_window,eligible_demand,T,hours,E,R,base_score,priority_score,confidence,status,blocker,review_decision`.
Also `opportunity-scoring.md` with core/50501 tables and qualitative fallback.

## Verification checklist
- [ ] Formula reproducible; expensive work does not gain points.
- [ ] Null data not replaced with estimated traffic or zero.
- [ ] 50501 expansion view present and geographically accurate.
- [ ] Query/page duplication and stock relevance checked.
- [ ] Review required before a brief enters the production queue.
