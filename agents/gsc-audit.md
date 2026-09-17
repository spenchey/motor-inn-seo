# 2. Search Console page/query audit

## Purpose
Measure the queries and pages driving local used-vehicle, Toyota and service demand on each DealerOn site.

## Inputs
Exact Search Console properties for all three hosts; authorized read-only credential loading; approved page map from crawl; previous run. Current task state: credentials unavailable.

## BLOCKED-IF-NO-CREDS
Do not report current GSC metrics until access is proven. Required unblock: the property owner completes the requested **service-account re-invite acceptance in the GSC UI** for each property. In Settings -> Users and permissions, confirm the exact service-account email and permission. Service accounts do not have a normal invitation inbox; the operational completion criterion is an owner-granted user visible in GSC plus successful authenticated reads. If a human invitation is pending, that human accepts it. Do not wait for a service account to click an email.

Historical memory identifies `ga4-reader@jeeves-485623.iam.gserviceaccount.com` as a prior Toyota reader, but its present identity/grant/credential validity is unverified. Confirm the current account with the owner; do not assume an old Toyota grant covers the other sites. Need: securely accessible authorized credentials, Search Console API enabled, read-only OAuth scope `https://www.googleapis.com/auth/webmasters.readonly`, and property access. Never place keys in reports.

For each property, require `sites.get` HTTP 200 with an appropriate permission and a minimal `searchanalytics.query` HTTP 200. An empty successful result proves authorization, not traffic. On missing credentials, 401, 403, or property mismatch, create `gsc-audit.md` with status BLOCKED, exact affected property, non-secret error, owner and next action. No substitute numbers from GA4 or the May audit. Other jobs may continue.

## Exact steps
1. Check credentials without printing secrets, then run the property-specific canaries above. Use the actual property IDs returned by the account. Domain properties and URL-prefix properties are different IDs.
2. Choose the last 28 complete finalized days, ending no later than three days before run date. Use the preceding 28 days as comparison. Record Search Console's Pacific date boundaries; request `dataState: final`, `type: web`, country `usa`.
3. Request dimensions `[page, query]` per property and period. Set `rowLimit: 25000`, `startRow: 0`; increment startRow by returned rows until fewer than 25,000 are returned. Retain raw responses locally. API top-row limits and anonymized queries mean this is not a complete census.
4. Make a separate page-only query for totals. Page/query sums may differ because of query privacy and aggregation; preserve the discrepancy. Never sum average positions or average CTR values without weighting.
5. Classify absolute URLs into used inventory (including `/used-inventory`, `/searchused.aspx`, `/used-cars`, `/used-trucks`, `/used-suvs`), new Toyota (`/new-toyota`, relevant `/searchnew.aspx` and model pages on Toyota/group hosts), and service (actual crawl-confirmed service, oil change, tires and scheduling pages). Route names are candidates until verified. Include Chevrolet service; do not mix new Chevrolet into Toyota results.
6. Preserve original URLs and add a normalized matching key. Remove tracking parameters only from that key, not evidence; preserve functional filter parameters. Record redirects and Google-selected canonicals separately.
7. For each page/query, compute clicks/impressions deltas, CTR = clicks/impressions, CTR change in percentage points, and position change. Return null for division by zero. Lower average position is better. Segment brand/non-brand, device when separately queried, and core/expansion city wording. GSC has no city/ZIP dimension; do not claim a 50501 audience from country data.
8. Flag queries with at least 50 impressions in 28 days and average position 4–20; sort by impressions descending, then clicks descending. Flag drops of at least 30% clicks only when prior clicks >=10. Label small samples and seasonality.
9. Feed candidates to job 5 and the raw page/query evidence to job 9. Make recommendations, not canonical/redirect changes.

## Output artifact path
`/Users/spencerheywood/motor-inn-seo/agents/runs/RUN_DATE/gsc-audit.md`
Also `gsc-page-query.csv`, `gsc-page-totals.csv`, and `gsc-raw/` when access exists.
CSV: `property,period,start_date,end_date,page,normalized_page,query,page_group,market_segment,clicks,impressions,ctr,position,retrieved_at,status`.

## Verification checklist
- [ ] Three properties have separate canary status and evidence.
- [ ] Required UI grant/re-invite completion documented, no secret values.
- [ ] Matching 28-day windows and finalized data used.
- [ ] Pagination and top-row/privacy limits disclosed.
- [ ] Page totals not equated with query-visible totals.
- [ ] Current BLOCKED state overrides stale connected audit.

References: [User permissions](https://support.google.com/webmasters/answer/7687615), [Search Analytics API](https://developers.google.com/webmaster-tools/v1/searchanalytics/query).
