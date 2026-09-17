# 9. Query/page cannibalization review

## Purpose
Identify competing landing pages, including `/used-inventory` versus `/searchused.aspx`, without confusing useful multiple results with harmful overlap.

## Inputs
Job 2 page/query exports for both 28-day windows, weekly query/page slices, current crawl canonicals/redirects, topical intent map, all three property IDs.

## BLOCKED-IF-NO-CREDS
Use the same credential and **service-account re-invite acceptance in the GSC UI** procedure as gsc-audit.md. Require property-specific authenticated read canaries. Current task state is BLOCKED. A crawl-only duplicate-content observation may be recorded as a hypothesis, but no query-overlap finding or quantified loss can be asserted without GSC data. Name missing property/export and next owner.

## Exact steps
1. Validate finalized matching windows and source properties. Preserve raw URL and normalized key. Remove tracking parameters only from keys; retain inventory filters and distinctions among SRP, model content and VDP intent.
2. For each query/property/window, find distinct pages. Retain pairs when each page has >=20 query impressions and >=20% of that query's summed page-row impressions. This denominator is an overlap diagnostic, not unique search volume. Include cross-property pairs separately with that same limitation.
3. Inspect `/used-inventory` vs `/searchused.aspx`, `/used-cars` aliases, Toyota pages on group vs Toyota hosts, and service pages across franchises. Compare title, intent, canonical, redirect behavior and actual destination.
4. Across four weekly slices, flag cases where the highest-click URL changes at least twice; break ties by impressions then URL. Inspect clicks, CTR and position per URL. Do not infer causality or lost clicks from overlap alone; low-volume cases remain inconclusive.
5. Classify each pair: useful distinct intent; canonical alias; potential competing same-intent pages; intentional brand separation; or insufficient data. Record source rows and the reason.
6. Recommend clarify intent, strengthen internal links, merge content, or request DealerOn canonical/redirect review. Never auto-redirect inventory search endpoints; confirm filtering, paid landing-page usage, GBP links and saved URLs first.
7. Identify the proposed owner URL using user intent, current canonical evidence, conversions where readable and link history. If evidence conflicts, HOLD and state the missing decision.
8. After a separately approved implementation, compare equivalent periods and preserve seasonality/stock caveats. This pack authorizes recommendations only.

## Output artifact path
`/Users/spencerheywood/motor-inn-seo/agents/runs/RUN_DATE/cannibalization.csv` and `cannibalization.md`.
CSV: `query,property_a,url_a,property_b,url_b,window,impressions_a,impressions_b,clicks_a,clicks_b,share_a,share_b,weekly_winner_changes,intent_match,canonical_evidence,classification,recommendation,confidence,blocker`.

## Verification checklist
- [ ] BLOCKED status emitted when GSC is unavailable.
- [ ] Requested used-inventory/searchused pair explicitly considered.
- [ ] Raw and normalized URLs retained; functional filters preserved.
- [ ] Overlap distinguished from demonstrated harm.
- [ ] Redirects/canonicals remain unexecuted proposals.
