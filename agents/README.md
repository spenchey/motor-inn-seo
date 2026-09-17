# Motor Inn dealership SEO agent pack

Prepared 2026-09-16. These are manual runbooks, not installed agents or scheduled jobs.

## Purpose
Turn measured local search demand into reviewable DealerOn content and citation fixes.

## Inputs and boundaries
- Root: `/Users/spencerheywood/motor-inn-seo/`. All outputs stay under this root.
- Sites: `https://www.motorinnautogroup.com/` (group/used), `https://www.motorinntoyotaofcarroll.com/` (Toyota), `https://www.motorinnofcarroll.com/` (Chevrolet). These are proposed intent owners; confirm current canonical URLs before assigning a page.
- Core geography: Carroll, Iowa, and the requested approximately 50-mile market: Lake City, Denison, Audubon, Storm Lake, Sac City. Verify distances before making drive-time or radius claims.
- `50501` is Fort Dodge, not Carroll (`51401`). Score it as a separate expansion cohort. Okoboji is also an expansion-market test; never label it part of the Carroll 50-mile core.
- Do not touch `ai.*` markdown proxies. Do not publish, submit profile changes, send email/messages, buy domains, or run paid APIs. Output drafts for Spencer's review only.
- No credentials, customer names, phone numbers, email addresses, VINs, loan details, or raw CRM messages in SEO artifacts. Summarize questions without identifying a person.
- Unknown values are `null` or `UNKNOWN`; blocked data is never zero. Keep source dates and status with every metric. Do not turn historical traffic into current evidence.

## Context reconciliation
The requested `audits/audit-latest.md` was read. It resolves to a May 25, 2026 report containing `GSC skipped: no` and `GSC: connected`, contrary to the task's expected skipped state. Treat it as historical only. The current instruction says GSC credentials are unavailable, so jobs 2 and 9 start BLOCKED-IF-NO-CREDS.

The requested `/Users/spencerheywood/.hermes/profiles/jeeves/workspace/llms.txt` does not exist on this host. No substitute draft was found in this SEO repository. Do not invent its contents or modify a proxy.

No saved buyer-question list or staged package matching `MOTORINN-SEO-STAGING-4a2aaec73b56bb4638eef49a5d6a9b4d` was found in this repository. The pack supplies a clearly labeled 20-question seed list and references the package as an unresolved input.

## Exact steps: weekly flow
1. Set `RUN_DATE` to the local America/Chicago date in `YYYY-MM-DD`. Create `agents/runs/RUN_DATE/` when executing a job. Never overwrite older run evidence.
2. Run **2 / gsc-audit.md**, **3 / ai-mentions.md**, then **5 / opportunity-scoring.md**. Jobs 1, 4, 6, 8, 9 and 10 supply supporting evidence when available. Keep unavailable inputs visible in the scorecard.
3. Write `weekly-review.md` with the top five candidates, input freshness, confidence, blockers, and approve/hold/reject fields. Spencer reviews it. The job runner does not approve its own proposal.
4. Feed reviewed candidates to **7 / content-brief.md**. Each brief names an exact host, canonical candidate, evidence, and the staged DealerOn package where applicable.
5. Keep all briefs in drafts. This task does not authorize a DealerOn handoff or publication.
6. On the first working day of each month, perform the monthly crawl below. Recheck affected pages after an independently authorized deployment.

## Monthly crawl procedure
1. Fetch robots.txt and sitemap.xml on each of the three DealerOn hosts. Record status, retrieval time, sitemap children, and canonical host. Never include the AI proxy hosts.
2. Crawl sitemap URLs and their internal HTML links at one request per second per host, concurrency one, maximum 2,000 URLs per host. Exclude search facets and query-parameter combinations from recursive expansion. On 403/429, stop that host and record BLOCKED; do not evade controls.
3. Record status, redirect chain, indexability, canonical, title, description, H1, depth and incoming internal links. Distinguish inventory SRPs, vehicle detail pages and permanent content pages.
4. Flag broken links, redirect chains, orphan pages, duplicate titles, conflicting canonicals, noindexed money pages and expired vehicle links. Sample service and model pages at mobile width.
5. Run job 9 only if GSC data passes job 2; crawl similarity alone is not proof of cannibalization. Produce recommendations only, with DealerOn routing/canonical changes held for review.

## Output artifact path
`/Users/spencerheywood/motor-inn-seo/agents/runs/RUN_DATE/weekly-review.md`
Monthly: same directory, `monthly-crawl.csv` and `monthly-crawl.md`.
Every report header: `job`, `run_date`, `status` (COMPLETE / PARTIAL / BLOCKED), `source_window`, `retrieved_at`, `properties_checked`, `inputs`, `blockers`, `next_owner`. COMPLETE means the described job ran; creation of this pack is not a completed SEO audit.

## Job index
| Job | Runbook | Main output |
|---|---|---|
| 1 | [Keyword research](keyword-research.md) | keyword-research.csv + buyer-questions.csv |
| 2 | [GSC audit](gsc-audit.md) | gsc-audit.md + gsc-page-query.csv |
| 3 | [AI mentions](ai-mentions.md) | ai-mentions.csv + ai-mentions.md |
| 4 | [Citation gaps](citation-gaps.md) | citation-gaps.csv |
| 5 | [Opportunity scoring](opportunity-scoring.md) | opportunity-scoring.csv |
| 6 | [Topical map](topical-map.md) | topical-map.csv |
| 7 | [Content brief](content-brief.md) | content/drafts/seo-briefs/RUN_DATE/PAGE-SLUG.md |
| 8 | [Internal links](internal-links.md) | internal-links.csv |
| 9 | [Cannibalization](cannibalization.md) | cannibalization.csv + cannibalization.md |
| 10 | [Local citations](local-citations.md) | local-citations.csv |

## Verification checklist
- [ ] All three sites considered separately; no proxy mutation.
- [ ] Current evidence separated from the May audit and historical memory.
- [ ] Weekly sequence 2/3/5 -> review -> 7 recorded, even when blocked.
- [ ] CRM information de-identified; no customer communication.
- [ ] No paid request, publication, DNS change or outreach performed.
- [ ] Monthly crawl includes timestamps and explicit limits.

Geography reference: [Iowa state directory, Fort Dodge 50501](https://publications.iowa.gov/130/1/stateofiowametrodirectory03s.pdf). Carroll address: [Motor Inn](https://www.motorinnautogroup.com/).
