# 4. AI citation gaps

## Purpose
Find third-party profile weaknesses on sources actually cited in buyer answers.

## Inputs
Job 3 observations and citation evidence; correct dealership names, addresses and contact details from the owning DealerOn host; platform profile URLs; previous gap list.

## Exact steps
1. If job 3 has no completed observations, output BLOCKED-AI-EVIDENCE. You may create a candidate profile inventory, but do not label it an AI citation finding.
2. Expand each cited URL and classify its source as DealerRater, CarGurus, Cars.com, Yelp, dealership site, Google, Facebook, local publication or other. Keep URL-level evidence and distinguish Motor Inn profiles from cited competitor profiles.
3. Count distinct question/surface observations citing each source; deduplicate repeated citations within one answer. Preserve platform and date. A citation is not a backlink.
4. For each relevant source, locate the Carroll profile and verify city, street address, website and dealership entity. Preserve separate Toyota/Chevrolet profiles where appropriate; do not merge unrelated rooftops.
5. Classify `verified-present`, `weak`, `missing-confirmed`, `not-found-in-search` or `unverified-access-blocked`. Missing-confirmed requires a reliable platform lookup or account-owner confirmation; lack of a search result is insufficient.
6. Mark weak only with a reason: incorrect NAP/website, duplicate record, broken profile, incomplete category/hours, stale supported details, or a documented review-recency/count gap versus same-platform local competitors. No invented minimum score. Log native platform rating/count with timestamp; do not mix time windows or syndicated counts.
7. Rank corrections by distinct citations descending, then identity errors first, then core-market relevance. Create a proposed correction with evidence, owner and approval status. For dealer-site gaps, name the precise factual content missing from the relevant existing page.
8. Send third-party actions to job 10 and on-site content candidates to job 5. Do not submit edits or contact platforms.

## Output artifact path
`/Users/spencerheywood/motor-inn-seo/agents/runs/RUN_DATE/citation-gaps.csv`
Columns: `source_domain,cited_url,question_ids,surfaces,citation_count,entity,profile_url,status,weakness,evidence_path,verified_at,proposed_fix,owner,approval_required`.
Also `citation-gaps.md` for the top five findings and inaccessible profiles.

## Verification checklist
- [ ] DealerRater, CarGurus, Cars.com, Yelp and dealer-site buckets included even when counts are unknown.
- [ ] Each observed citation traces to job 3 evidence.
- [ ] Missing and unverified profiles not conflated.
- [ ] Correct Carroll entity and current NAP checked.
- [ ] All actions remain proposed.
