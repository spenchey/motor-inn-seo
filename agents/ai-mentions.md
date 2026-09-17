# 3. Weekly AI mentions and citations

## Purpose
Measure whether buyer-facing AI answers mention the Carroll business and identify the exact sources supporting those answers.

## Inputs
Stable 20-question list below or the versioned saved list from job 1; browser access to ChatGPT, Perplexity and Google Search AI Overviews; previous week's evidence. No actual saved set was found locally at build time. The following `seed-v1` set is generated for this pack, not extracted from lead notes and not yet tested.

## CREDS-NEEDED
DataForSEO account reportedly created 2026-08-17; credentials are NOT available on disk per the task. Need the account's API login/password through the approved secret store, enabled endpoints, location/language support, sufficient balance and explicit spending authorization. A website login or signup date does not prove API access. Do not search for or print passwords. Do not assume one endpoint reproduces all three consumer products. Until these are supplied, use accessible manual interfaces; if an interface requires unavailable login/access, mark its observations BLOCKED. No API installation or paid call is part of this task.

## Saved seed-v1 questions
| ID | Exact question | Segment |
|---|---|---|
| Q01 | What is the best used car dealer in Carroll Iowa? | core |
| Q02 | Where can I find used trucks for sale in Carroll IA? | core |
| Q03 | Where can I buy a used SUV in Carroll Iowa? | core |
| Q04 | Which Toyota dealer serves Carroll IA? | core |
| Q05 | Which Chevy dealer serves Carroll IA? | core |
| Q06 | Where can I get Toyota service near Lake City IA? | core |
| Q07 | Where can I get an oil change in Carroll IA? | core |
| Q08 | Who offers Chevy service in Carroll Iowa? | core |
| Q09 | Where can I find a used Silverado near Denison IA? | core |
| Q10 | Where can I buy a Toyota RAV4 near Audubon IA? | core |
| Q11 | Where can I find a Toyota Tundra near Carroll IA? | core |
| Q12 | Where can I buy a Chevy Equinox near Sac City IA? | core |
| Q13 | Which used car dealers near Storm Lake IA take trade-ins? | core |
| Q14 | Where can I sell my car near Carroll IA without buying another? | core |
| Q15 | How can I apply for auto financing at a Carroll IA dealership? | core |
| Q16 | Where can I compare used trucks and used SUVs near Lake City IA? | core |
| Q17 | Where can I get tires for my Toyota near Carroll IA? | core |
| Q18 | Which Carroll IA dealerships have customer reviews I can read? | core |
| Q19 | Which Toyota dealer is near Okoboji Iowa? | expansion: Okoboji |
| Q20 | Where can shoppers in Fort Dodge IA 50501 buy a used truck? | expansion: 50501 |

## Exact steps
1. Freeze question text and IDs before starting. Use the same device, English language, US country, Carroll location context where supported, and account/search mode each week. Record actual location behavior; do not claim a simulated location is verified.
2. Run each question once on each of three surfaces: 60 planned observations. Use a fresh conversation per question with no leading Motor Inn instruction. Record timestamp, surface, displayed model/version if available, logged-in state, search mode and question-set version.
3. For Google, search the exact question. If no AI Overview appears, mark `NO_OVERVIEW`; normal search results are not AI citations. For ChatGPT/Perplexity, record whether web search is enabled. Do not silently switch products or infer results from a different search engine.
4. Save answer text or screenshot and cited source URLs to `ai-evidence/`. If a login wall, error or rate limit occurs, record BLOCKED/ERROR. Never treat failure as a missing brand mention.
5. Classify `mentioned` yes/no only for completed answers. Match Motor Inn Auto Group, Motor Inn Toyota of Carroll, Motor Inn of Carroll and Motor Inn Chevrolet of Carroll only when the answer identifies Carroll or links to the correct entity. Other Motor Inn locations and hotels are ambiguous, not matches.
6. Record recommendation position if the answer uses an ordered list, otherwise null. Record dealership-site citation independently from brand mention. Expand citation links and retain original + final URLs, page titles, source domains, competitors and any incorrect factual claim.
7. Calculate mention rate = completed answers mentioning the correct business / completed answers. Report per surface and core/expansion segment. Report NO_OVERVIEW, blocked, error and coverage counts separately out of 20 each. Never put unavailable answers in the absence denominator.
8. Compare only matched question/surface/mode observations week over week. Do not claim causation from a one-week change. Feed cited sources to job 4 and observed gaps to job 5.

## Output artifact path
`/Users/spencerheywood/motor-inn-seo/agents/runs/RUN_DATE/ai-mentions.csv`
Columns: `question_id,question_set,surface,model,search_mode,locale,observed_at,status,mentioned,entity,rank,cites_dealer_site,cited_urls,competitors,evidence_path,notes`.
Also `ai-mentions.md` for coverage/rates and `ai-evidence/` for source records. CSV cells containing lists use JSON arrays.

## Verification checklist
- [ ] Exactly 20 stable questions and 60 planned surface observations.
- [ ] Generated seed origins disclosed; no invented historical saved list.
- [ ] Answer evidence supports every mention and citation classification.
- [ ] No Overview and blocked access separated from no mention.
- [ ] Entity identity and expansion geography checked.
- [ ] DataForSEO credentials and spend remain explicit blockers.
