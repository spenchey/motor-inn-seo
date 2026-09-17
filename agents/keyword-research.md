# 1. Dealership keyword research

## Purpose
Find shopping and service questions that can produce useful Carroll-area DealerOn pages.

## Inputs
Six fixed seeds: `used trucks for sale Carroll IA`, `used cars Carroll IA`, `Toyota dealer Carroll IA`, `Chevy dealer Carroll IA`, `Toyota service near Lake City IA`, `oil change Carroll IA`.
Use the three sites, geography and output conventions in README.md; available GSC export; current inventory categories; existing drafts; a de-identified 90-day DealerSocket inquiry export and service-advisor question log.

## Source availability and where to get buyer questions
At build time, no DealerSocket notes or advisor logs were found in this SEO repository. `/Users/spencerheywood/clawd/data/lead-response/leads.db` was opened read-only with immutable mode; `leads` and `followups` both had zero rows. This is not evidence that the CRM has no leads.

For real questions, ask the CRM administrator to export inbound inquiry text and sales work notes from DealerSocket for the Carroll rooftop, with date and sales/service topic. Ask the service manager for advisor intake questions/customer concerns from repair-order or appointment logs, with date and service category. Strip identifiers before placing an export in `agents/inputs/` under this root. Do not export financial applications or credentials.

Historical memory points to `s3://motorinn-dealervault-raw/raw/dealersocket/historical/extract_date=2026-07-31/` (MessageTrack/WLInbox/work notes) and a Glyph archive. These are unverified, potentially stale pointers, not current reads. Have the data owner provide a de-identified extract; do not mount Glyph or start ingestion in this task. Service history is not necessarily advisor wording.

## Exact steps
1. Read README.md and log available inputs, dates and missing sources. If CRM/advisor data is missing, record `BUYER-NOTES-NEEDED`, identify its owner, and proceed with seed research only.
2. For readable authorized exports, inspect column names first. Extract question-bearing inbound notes; remove names, contacts, VINs, exact personal financial facts and staff signatures. Paraphrase into anonymous intent questions. Store only topic, paraphrased question, month and source type.
3. Normalize case and whitespace; group semantically equivalent questions. Count independent inquiries per group, not repeated follow-up messages. Record sample coverage and exclude test leads. Do not fabricate counts.
4. Expand each fixed seed by model, body style, transaction and the six named core cities. Examples: used Silverado in Carroll; RAV4 near Denison; tires near Audubon; trade-in near Sac City. Keep Fort Dodge/50501 and Okoboji in separate expansion segments.
5. Inspect a fresh search result for each seed and at most two meaningful variants per seed. Record exact query, date, location, result type, competing URL and visible People Also Ask questions. Do not label generated questions as observed buyer questions.
6. Merge GSC query evidence if job 2 is available. Otherwise leave clicks, impressions and position null. Leave keyword volume null until an approved source provides dated, geographically scoped data. No paid API calls in this task.
7. Assign one intent cluster and proposed owning host per keyword. Prefer existing `/used-inventory`, `/used-trucks`, `/used-suvs`, Toyota and service pages over duplicate location pages. Confirm actual URLs with the crawl.
8. Choose 20 stable monitoring questions for job 3; retain IDs across weeks. The seed set in job 3 is provisional until real notes are available. Feed candidate pages to jobs 5 and 6.

## Output artifact path
`/Users/spencerheywood/motor-inn-seo/agents/runs/RUN_DATE/keyword-research.csv`
Columns: `keyword,question_id,intent,model,body_style,city,market_segment,source_type,source_reference,source_date,observed_inquiry_count,volume,volume_geo,clicks,impressions,position,owner_host,target_url,confidence,blocker`.
Also `buyer-questions.csv` with `question_id,question,origin,topic,market_segment,source_month,frequency,status`, and `keyword-research.md` for coverage/blockers.

## Verification checklist
- [ ] All six exact seeds present.
- [ ] Carroll, Lake City, Denison, Audubon, Storm Lake, Sac City considered.
- [ ] Real notes distinguished from generated seeds and search questions.
- [ ] No customer identifiers or unredacted messages saved.
- [ ] Unknown volume remains null; duplicate page ideas consolidated.
- [ ] Missing notes have specific retrieval sources and owners.
