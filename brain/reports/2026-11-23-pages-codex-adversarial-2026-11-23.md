# Adversarial QA: 2026-11-23 page packages

- **Date:** 2026-11-23. Live status checks began 16:34:44 UTC / 10:34:44 America/Chicago.
- **Overall verdict: FAIL — 8 BLOCKING findings, 7 MINOR findings.**
- **Scope:** plan and original task; all 45 package files and 9 AI mirrors; all 7 generator sources; the four named house-rule/owner files; complete GSC export and five ads-package files; specified GSC cache, three sitemap snapshots, three contact captures, NAP-audit JSON and Buick/GMC removal request.
- **Methods:** read-only source inspection with line numbers, Python standard-library comparisons/arithmetic, existing validator with bytecode writing disabled, curl GETs. All 54 generated artifacts were read and matched to their generator output in memory. Complete FAQ questions and answers were independently compared across actual Markdown, schema and mirror files.
- **Network:** available. One deduplicated status GET per 89 scoped URLs; body checks for all 11 parameterized links plus targeted claim/redirect checks. Every status request exited 0 with no stderr. Each curl had a 20-second limit.
- **Boundaries:** this report is the only file written. No fixes, rebuilds, Git mutations, publishing, deployments, logins, form submissions or POSTs.
- **Limits:** no rendered-browser, form-submission or live-GSC-account test. No claim these drafts are installed. No total probe deadline; total session elapsed unmeasured. Checks stopped after scoped coverage and confirmation of the HD defect.

## Per-page × charter verdicts

C1 claim traceability; C2 FAQ parity/AEO; C3 shopper voice; C4 live links/filters; C5 metadata; C6 NAP/house facts; C7 evidence/routing; C8 schema validity.

| Package | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 |
|---|---|---|---|---|---|---|---|---|
| chevy-dealer-carroll-iowa | PASS | PASS | FAIL | MINOR¹ | PASS | PASS | MINOR | PASS |
| contactus-carroll | PASS | PASS | FAIL | PASS | PASS | PASS | FAIL | PASS |
| chevy-suvs-for-sale-carroll-iowa | FAIL | MINOR | FAIL | MINOR¹ | PASS | PASS | PASS | PASS |
| toyota-dealers-in-iowa | MINOR | PASS | FAIL | MINOR¹ | PASS | PASS | PASS | PASS |
| chevy-blazer-for-sale-carroll-iowa | FAIL | MINOR | FAIL | MINOR¹ | PASS | PASS | PASS | PASS |
| used-cars-carroll-iowa | FAIL | PASS | FAIL | MINOR | PASS | PASS | PASS | PASS |
| chevy-trucks-for-sale-carroll-iowa | FAIL | MINOR | FAIL | FAIL | PASS | PASS | FAIL | PASS |
| toyota-tacoma-tundra-for-sale-carroll-iowa | MINOR | PASS | FAIL | MINOR¹ | PASS | PASS | FAIL | PASS |
| toyota-sequoia-sienna-for-sale-carroll-iowa | MINOR | PASS | FAIL | MINOR¹ | PASS | PASS | PASS | PASS |

¹ The seven NEW-page canonical URLs in AI metadata return 404. They are declared unpublished targets, not contextual links to unpublished sibling pages. This expected draft state remains an open live-link condition before publication; it is not counted as a blocking defect or numbered finding. All 82 existing destinations returned final 200. The truck C4 failure is an incorrect filter despite HTTP 200.

C8 covers syntax, vocabulary, references and NAP consistency. Unsupported FAQ content is counted under C1, and contact-page identity under C7. Broader plan arithmetic limitations are R1-013.

## Charters recorded before probes

| # | Expected contract | Risk / entrypoint | Isolation / exit |
|---|---|---|---|
| 1 | Claims have an opened cited repo source | Content, FAQ, schema, AI against brief/facts.py sources | Read only; all distinct claims supported or reported |
| 2 | FAQ text identical; 3–6 pairs, 2–4 self-contained sentences | Actual file comparisons | In-memory parsing; all 9 packages |
| 3 | Question/answer-first structure, one next step, no production text | Complete content and mirrors | No edits; inspect all packages |
| 4 | Final 200 and functioning model filters | Deduplicated curl GETs | 20 seconds/request; no submissions |
| 5 | Title ≤60, description ≤155, OG fields and routed host | Actual meta.md | Compare all nine |
| 6 | Canonical phone/address; no banned identity/credit/test-drive wording | Shopper text and schema | Inspect all representations |
| 7 | Exact GSC rows/totals/phrasing; routing and NEW status correct | Export, ads CSV and sitemap snapshots | Compare independently in memory |
| 8 | JSON-LD parses; vocabulary/IDs valid; no review/rating markup | Actual schema files | Compare official vocabulary and copy |

The report-only QA skill's extra evidence files, telemetry and learning-store writes were omitted to honor the user's single-report write boundary.

## Findings

### R1-001 — BLOCKING — HD inventory link hides three matching listings

- **File:line:** content/page-packages/2026-11-23/chevy-trucks-for-sale-carroll-iowa/content.md:29; content/page-packages/2026-11-23/ai/chevy-trucks-for-sale-carroll-iowa.md:51; truck brief.md:68. Generator: content/page-packages/2026-11-23/_src/pages_chevy.py:328 and :359.
- **Expected:** “Search HD inventory” returns the store's Silverado 2500 HD listings.
- **Observed:** Model=Silverado%202500HD returns zero results. The live model name has a space before HD. Changing only that space returns three matching trucks.
- **Evidence / confirmation:** body GETs, replayed against the original and corrected URLs:
  ~~~text
  original: 200 .../searchnew.aspx?Model=Silverado%202500HD
  TotalNumberSearchResults":0,"Filters":{"Model":"Silverado 2500HD"}

  corrected: 200 .../searchnew.aspx?Model=Silverado%202500%20HD
  TotalNumberSearchResults":3,"Filters":{"Model":"Silverado 2500 HD"}
  2026 Chevrolet Silverado 2500 HD LT
  2026 Chevrolet Silverado 2500 HD LT
  2026 Chevrolet Silverado 2500 HD Custom
  ~~~
  Command: curl -sS -L --max-time 20 -w '\nFINAL %{http_code} %{url_effective}' URL; Python inspected returned HTML. The unfiltered inventory also lists those three models.
- **Suggested fix:** change the generator destinations to Model=Silverado%202500%20HD, regenerate, and repeat the result/body check. A 200-only check misses this defect.

### R1-002 — BLOCKING — Model lease terms are promised on a page where they were not found

- **File:line:** content/page-packages/2026-11-23/chevy-suvs-for-sale-carroll-iowa/content.md:50, faq.md:19, schema.json:111; content/page-packages/2026-11-23/chevy-blazer-for-sale-carroll-iowa/content.md:43, faq.md:15, schema.json:103; content/page-packages/2026-11-23/chevy-trucks-for-sale-carroll-iowa/content.md:51, faq.md:15, schema.json:103. AI copies: content/page-packages/2026-11-23/ai/chevy-suvs-for-sale-carroll-iowa.md:25, ai/chevy-blazer-for-sale-carroll-iowa.md:21 and ai/chevy-trucks-for-sale-carroll-iowa.md:21.
- **Expected:** the assertion that current model lease/finance offers “are posted” has a cited source containing those offers.
- **Observed:** cited sources establish identity, owner policies and sitemap URLs, not current model lease programs. The linked /chevroletspecialoffers returns 200, but its fetched main copy contains customer-category bonus programs rather than the promised model lease terms.
- **Evidence / confirmation:** opened the fact lists at SUV brief.md:80–87, Blazer brief.md:66–73 and truck brief.md:78–86 and their underlying sources. Two body GET reviews of https://www.motorinnofcarroll.com/chevroletspecialoffers found:
  ~~~text
  Chevrolet Military Program
  Chevrolet Educator Program
  Chevrolet First Responder Program
  Blazer: 0 occurrences in raw HTML
  Tahoe: 0 occurrences in raw HTML
  No model lease terms in extracted main copy; no iframe elements.
  ~~~
  Silverado/Equinox strings elsewhere in site markup do not establish offer terms in the main copy. Browser-injected offers were not tested. This is an unsupported affirmative promise, not a claim Chevrolet has no leases.
- **Suggested fix:** ask shoppers to contact the Carroll sales team about current options, or cite/link a verified source actually presenting the relevant offers. Update every FAQ representation together.

### R1-003 — BLOCKING — Test-drive requests become unconditional readiness promises

- **File:line:** content/page-packages/2026-11-23/chevy-blazer-for-sale-carroll-iowa/content.md:25; content/page-packages/2026-11-23/used-cars-carroll-iowa/content.md:38. Generator: content/page-packages/2026-11-23/_src/pages_chevy.py:249 and _src/pages_group.py:175.
- **Expected:** request a convenient time subject to vehicle availability and dealership confirmation.
- **Observed:** after a form request, “the team will have the Blazer or Blazer EV ready” / “will have the vehicle ready at a time that works for you.”
- **Evidence / confirmation:** content/ready-design-OWNER-NOTES.md:6–7 approves “at your convenience” and no hard time promise, not guaranteed readiness. A live GET of the group test-drive page says:
  ~~~text
  A request is not a confirmed appointment until the dealership responds
  ~~~
  The Blazer EV filtered response had TotalNumberSearchResults:0. That does not prove a future test drive impossible; it shows why unconditional readiness is unsupported.
- **Suggested fix:** say the team will confirm the vehicle and appointment after the request. Preserve the owner's license/insurance ban.

### R1-004 — BLOCKING — Brand service capability becomes knowledge of every individual used vehicle

- **File:line:** content/page-packages/2026-11-23/used-cars-carroll-iowa/content.md:26; generator content/page-packages/2026-11-23/_src/pages_group.py:166.
- **Expected:** claim documented Toyota/Chevrolet service capability.
- **Observed:** “If you're buying a used Toyota or Chevrolet, the service department already knows that vehicle.” This extends brand familiarity to an unqualified assertion about the individual vehicle.
- **Evidence / confirmation:** opened cited brain/BRIEF.md:14–15 and content/ready-design-OWNER-NOTES.md:8–9. They establish factory service/Chevrolet certification, not prior service, inspection or familiarity with every used unit. The used fact list at brief.md:80–87 contains no unit-history source.
- **Suggested fix:** describe the team's work on these brands. Remove the individual-vehicle assertion unless a unit-specific inspection/history source supports it.

### R1-005 — BLOCKING — Used/general targets are assigned to brand-site pages

- **File:line:** content/page-packages/2026-11-23/chevy-trucks-for-sale-carroll-iowa/brief.md:12, :25, :27 and :31; content/page-packages/2026-11-23/toyota-tacoma-tundra-for-sale-carroll-iowa/brief.md:12 and :26.
- **Expected:** CLAUDE-BRIEF-2026-11-23.md:16–18 routes used/general intent to the group site and new-brand intent to its brand site.
- **Observed:** the Chevy brief acknowledges “trucks for sale near me” is brandless but includes it because it is “tiny.” It counts used Silverado/Colorado targets too. The Toyota brief calls all its targets new-truck intent while counting “used toyota tacoma.”
- **Evidence / confirmation:** exact export matches:
  ~~~text
  trucks for sale near me           52 impressions, 11 clicks, position 7.9
  used chevy silverado for sale     35 impressions,  2 clicks, position 2.5
  used chevy colorado for sale      19 impressions,  1 click,  position 1.8
  used toyota tacoma                79 impressions,  1 click,  position 6.2
  Chevy cluster: 1692 - 52 - 35 - 19 = 1586
  Toyota truck cluster: 552 - 79 = 473
  ~~~
  Export query lines: ads/gsc-keywords-12mo.json:424, :1096, :2832 and :3042. Values are accurate; target assignment is the defect.
- **Suggested fix:** assign these targets to group used-truck content and recompute brand-page clusters. A contextual used-inventory cross-link can remain without counting that query as a new-brand target.

### R1-006 — BLOCKING — Contact handoff treats a redirect alias as a separate page

- **File:line:** content/page-packages/2026-11-23/contactus-carroll/brief.md:14–20; content.md:1; meta.md:3; schema.json:6–7 and :195; content/page-packages/2026-11-23/ai/contactus-carroll.md:5. Plan: docs/page-plans/page-plan-2026-11-23.md:31 and :64.
- **Expected:** placement, canonical and consolidation advice match the observed live destination.
- **Observed:** the brief treats /Contactus/Carroll and /contactus.aspx as different competing pages and recommends the former as owner. The former currently redirects to the latter; its own canonical is /contactus.aspx.
- **Evidence / confirmation:** required status GET and later body GET agreed:
  ~~~text
  input: https://www.motorinnautogroup.com/Contactus/Carroll
  final: 200 https://www.motorinnautogroup.com/contactus.aspx
  <link rel="canonical" href="https://www.motorinnautogroup.com/contactus.aspx" />
  <h1 class="header">Contact Us</h1>
  ~~~
  Historical GSC rows for two paths do not prove two currently editable pages.
- **Suggested fix:** revise the in-place handoff around the observed final page, then align canonical/og:url/WebPage/FAQ IDs and mirror metadata. If a different canonical is wanted, describe that as an explicit proposed routing change for owner/DealerOn review.

### R1-007 — BLOCKING — All AI mirrors contain visible production instructions

- **File:line:** content/page-packages/2026-11-23/ai/chevy-dealer-carroll-iowa.md:6–7; ai/contactus-carroll.md:6–7; ai/chevy-suvs-for-sale-carroll-iowa.md:6–7; ai/toyota-dealers-in-iowa.md:6–7; ai/chevy-blazer-for-sale-carroll-iowa.md:6–7; ai/used-cars-carroll-iowa.md:6–7; ai/chevy-trucks-for-sale-carroll-iowa.md:6–7; ai/toyota-tacoma-tundra-for-sale-carroll-iowa.md:6–7; ai/toyota-sequoia-sienna-for-sale-carroll-iowa.md:6–7. Generator: content/page-packages/2026-11-23/_src/build.py:237–239.
- **Expected:** shopper/entity information in the ingestion resource; deployment instructions in the handoff.
- **Observed:** ordinary visible list items say “Target AI host” and “Status: draft for review (not deployed).” Seven also expose “per-host catalog, spenchey/ai-markdown-proxy.”
- **Evidence / confirmation:** all nine actual mirrors match build_ai output. These lines are neither comments nor a fenced handoff; they are emitted into the same Markdown resource as the answers.
- **Suggested fix:** move target/status notes into the brief or an explicitly excluded handoff field before mirror release. The draft status is accurate; placing workflow text in the ingestion body is the defect. This finding does not claim current publication.

### R1-008 — BLOCKING — Eight pages have competing conversion actions

- **Expected:** brain/VOICE-DNA.md:20 and :33 require one obvious next step and no competing CTAs.
- **Observed / file:line evidence:** the primary action is followed by explicit requests for different conversion forms:

| File under content/page-packages/2026-11-23/ | Primary | Competing requests |
|---|---|---|
| contactus-carroll/content.md | :7 call/visit | :33 start trade value; :43 request test drive |
| used-cars-carroll-iowa/content.md | :7 search/call | :30 get trade value; :38 request test drive |
| chevy-dealer-carroll-iowa/content.md | :5 call | :23 ask for quote; :27 schedule service; :35 get pre-approved |
| chevy-blazer-for-sale-carroll-iowa/content.md | :5 search/call | :21 get pre-approved; :25 request test drive; :29 value trade |
| chevy-trucks-for-sale-carroll-iowa/content.md | :5 search/call | :33 get pre-approved; :37 value trade |
| toyota-dealers-in-iowa/content.md | :5 call | :31 schedule service; :35 value trade/get pre-approved |
| toyota-tacoma-tundra-for-sale-carroll-iowa/content.md | :5 search/call | :17 take both on a test drive; :25 value trade/get pre-approved |
| toyota-sequoia-sienna-for-sale-carroll-iowa/content.md | :5 search/call | :17 book test drives; :25 get pre-approved |

- **Evidence / confirmation:** complete line-numbered content reads. These are imperative requests to distinct conversion forms, beyond informational model navigation. Each bold primary CTA is repeated twice as intended.
- **Suggested fix:** choose one primary conversion and make supporting finance/trade/service information informational, or document an owner exception to the house rule. No copy was changed.

### R1-009 — MINOR — Qualitative vehicle descriptions lack a substantive cited source

- **File:line:** content/page-packages/2026-11-23/chevy-suvs-for-sale-carroll-iowa/content.md:12–18; chevy-blazer-for-sale-carroll-iowa/content.md:17; chevy-trucks-for-sale-carroll-iowa/content.md:20–23; toyota-tacoma-tundra-for-sale-carroll-iowa/content.md:17 and :35–39; toyota-sequoia-sienna-for-sale-carroll-iowa/content.md:17–21 and :39–43. Descriptions recur in their FAQ/schema and AI summaries.
- **Expected:** cited repo passages describe row counts, size class, relative dimensions, fuel/powertrain type and towing use.
- **Observed:** cited sitemap model/offer URLs establish page/name existence, not those descriptions. A URL containing i-FORCE-MAX does not itself establish “hybrid powertrain.”
- **Evidence / confirmation:** opened all three complete sitemap snapshots and relevant fact lists. Generator content/page-packages/2026-11-23/_src/pages_chevy.py:16 and _src/pages_toyota.py:13 explicitly leave OEM wording spot-checks open. No cited captured OEM description was supplied.
- **Suggested fix:** capture/cite relevant OEM passages in the repo and check all representations. MINOR as instructed for qualitative OEM descriptors; this is an evidence gap, not a finding the descriptors are factually wrong.

### R1-010 — MINOR — Toyota directory-completeness claim has no cited repo evidence

- **File:line:** content/page-packages/2026-11-23/toyota-dealers-in-iowa/content.md:9; generator content/page-packages/2026-11-23/_src/pages_toyota.py:41.
- **Expected:** a captured cited source supports the assertion that toyota.com's dealer search lists all Iowa dealers.
- **Observed:** Toyota brief.md:85–91, _src/pages_toyota.py:6–12 and facts.py comments provide identity, owner policies, sitemaps and landmark evidence, not locator evidence.
- **Evidence / confirmation:** opened every listed source. The generator review note at _src/pages_toyota.py:107 calls the statement generic; that does not establish completeness.
- **Suggested fix:** capture a primary locator source or remove the completeness assertion. No competitor is named and no closest/only claim was found; risk is low.

### R1-011 — MINOR — Three FAQ answers omit the dealership and city

- **File:line:** content/page-packages/2026-11-23/chevy-suvs-for-sale-carroll-iowa/faq.md:19; chevy-blazer-for-sale-carroll-iowa/faq.md:15; chevy-trucks-for-sale-carroll-iowa/faq.md:15. Corresponding content lines: :50, :43, :51; schema answer lines: :111, :103, :103; AI answer lines: :25, :21, :21.
- **Expected:** each answer names dealership and city independently of its heading/page.
- **Observed:** lease answers begin “Current Chevrolet … offers are posted…” and refer to a domain and “the sales team,” without “Motor Inn Chevrolet of Carroll in Carroll, Iowa.”
- **Evidence / confirmation:** full answer comparison found verbatim parity across all four representations, consistently reproducing the omission. Each answer has two sentences.
- **Suggested fix:** explicitly name the store and city while correcting R1-002. This is an AEO quotation/context defect.

### R1-012 — MINOR — Shared headings and some lead sentences fail the required structure

- **File:line:** “Frequently asked questions” is a non-question H2 in content/page-packages/2026-11-23/contactus-carroll/content.md:45; used-cars-carroll-iowa/content.md:40; chevy-dealer-carroll-iowa/content.md:41; chevy-suvs-for-sale-carroll-iowa/content.md:34; chevy-blazer-for-sale-carroll-iowa/content.md:31; chevy-trucks-for-sale-carroll-iowa/content.md:39; toyota-dealers-in-iowa/content.md:37; toyota-tacoma-tundra-for-sale-carroll-iowa/content.md:27; toyota-sequoia-sienna-for-sale-carroll-iowa/content.md:27.
- **Expected:** brain/VOICE-DNA.md:17–18 requires question H2s and a direct answer in the first sentence.
- **Observed:** the shared FAQ label is not a question. The SUV answer at content.md:9 begins “Here's the lineup…” and truck answer at content.md:18 begins “Match the truck to the job,” deferring specifics to later bullets.
- **Evidence / confirmation:** all nine complete content reads. build.py:132 hard-codes the label; validate.py:88 expressly exempts it. The supplied voice rule has no such exception.
- **Suggested fix:** use a shopper-question heading or document an allowed label exception, and replace generic lead sentences with concrete answers.

### R1-013 — MINOR — Plan-wide totals are misstated or cannot be reproduced

- **File:line:** docs/page-plans/page-plan-2026-11-23.md:23, :78, :80 and :83.
- **Expected:** totals correspond to defined export rows with an explicit threshold.
- **Observed / evidence:** independent sums of the complete ads/gsc-keywords-12mo.json:

| Plan statement | Recomputed evidence |
|---|---|
| Toyota model “for sale” is about 860 impressions “in total” (:23) | 552 + 311 = 863 counts only two planned packages, including a used-Tacoma row and a non-sale size question. Fourteen unambiguous Toyota-model “for sale” rows alone total 1,187, before RAV4 and further variants. |
| Non-franchise lease/service about 600 (:78) | Word-boundary Chrysler/Dodge/Ram/Jeep/Ford + lease/service: 432 across all 18 matching rows; 404 across 11 rows with ≥15 impressions. |
| Camaro/Corvette/Malibu/Impala “for sale” about 330 (:80) | All matching variants: 658; ≥10 impressions: 292; ≥15: 235. No membership/threshold reproduces the claimed number as written. |
| Carroll finance about 190 (:83) | All eight Carroll queries containing finance/financing/loan: 153; the three ≥15 rows: 37 + 81 + 21 = 139. |

- **Command/output excerpt:** Python loaded the complete JSON, filtered query strings with those predicates and summed impressions. The 1,187 lower bound is 239+52+150+32+136+30+132+97+48+94+32+92+25+28 for Tacoma/Tundra/Sequoia/Sienna/Camry/Highlander/4Runner/Corolla sale queries.
- **Confirmation / limits:** all nine exact package totals passed separately. Other broad research-gap estimates, including repairs and RAV4 research, lack exact membership and cannot be certified as precise clusters. The town gap 3,718/46 rows and approximately 1,300 non-franchise-used total were reproducible.
- **Suggested fix:** label 863 as the two-package total; correct finance/lease-service figures; supply membership and thresholds for broad gap estimates.

### R1-014 — MINOR — “Every month” recurrence is not demonstrated

- **File:line:** docs/page-plans/page-plan-2026-11-23.md:14; related argument in content/page-packages/2026-11-23/chevy-dealer-carroll-iowa/brief.md:16.
- **Expected:** monthly recurrence supported by monthly observations.
- **Observed:** the plan says LLC-name queries “recur every month on both properties.” The cited sources are one 12-month group aggregate and one 28-day group/Toyota cache.
- **Evidence / confirmation:** the complete cache request spans 2026-09-19 through 2026-10-16. Query rows give group 242/255/278 and Toyota 93/108/168 impressions, matching brief ranges. Property objects contain query_rows/page_rows for that single window, not a monthly series. All 10,636 annual export rows carry the group property.
- **Suggested fix:** say these queries also occur in the cached 28-day period. Keep “every month” only with a monthly series. The annual LLC total itself is correct: 2,268 + 2,138 + 2,041 = 6,447.

### R1-015 — MINOR — Used test-drive preselection could not be confirmed

- **File:line:** content/page-packages/2026-11-23/used-cars-carroll-iowa/content.md:38; content/page-packages/2026-11-23/ai/used-cars-carroll-iowa.md:52.
- **Expected:** if ?type=Used is intended to preselect used vehicles, the response demonstrates that selection.
- **Observed:** HTTP 200 retains ?type=Used, but the fetched page is a general new-or-used request page. No selected Used control was found; returned script says var vehicleType = '';.
- **Evidence / confirmation:** the initial filter body check and later targeted review found no positive Used preselection. The live description says “Choose a current new or used listing.”
- **Suggested fix:** confirm the selection in a rendered browser or use the general test-drive URL without implying preselection. MINOR/inconclusive for this hint; page reachability passes. JavaScript execution and form submission were not performed.

## Link-check ledger

Command used once per deduplicated scoped URL:
~~~sh
curl -sS -L -o /dev/null -w '%{http_code} %{url_effective}' --max-time 20 URL
~~~

All results below were observed directly. “Planned” identifies only the canonical target in a declared NEW draft's AI metadata. Seven such 404s must be resolved before mirror publication; they are not broken contextual links to sibling pages.

| URL | Final code | Final destination / note |
|---|---:|---|
| https://www.motorinnautogroup.com/ | 200 | Same URL |
| https://www.motorinnautogroup.com/Contactus/Carroll | 200 | https://www.motorinnautogroup.com/contactus.aspx |
| https://www.motorinnautogroup.com/best-chevrolet-suvs-for-families | 200 | Same URL |
| https://www.motorinnautogroup.com/blog/2027-toyota-tacoma-trd-pro-honeycomb-reservation-interest | 200 | Same URL |
| https://www.motorinnautogroup.com/blog/heavy-duty-vs-light-duty-trucks | 200 | Same URL |
| https://www.motorinnautogroup.com/carfax-1-owner.html | 200 | Same URL |
| https://www.motorinnautogroup.com/finance-locations.html | 200 | Same URL |
| https://www.motorinnautogroup.com/highlander-vs-grand-highlander | 200 | Same URL |
| https://www.motorinnautogroup.com/hours.aspx | 200 | Same URL |
| https://www.motorinnautogroup.com/searchnew.aspx | 200 | Same URL |
| https://www.motorinnautogroup.com/service-locations.html | 200 | Same URL |
| https://www.motorinnautogroup.com/testdrive.aspx | 200 | Same URL |
| https://www.motorinnautogroup.com/testdrive.aspx?type=Used | 200 | Same URL |
| https://www.motorinnautogroup.com/trade.aspx | 200 | Same URL |
| https://www.motorinnautogroup.com/under-15k.html | 200 | Same URL |
| https://www.motorinnautogroup.com/under-20000 | 200 | Same URL |
| https://www.motorinnautogroup.com/used-cars-carroll-iowa | 200 | Same URL |
| https://www.motorinnautogroup.com/used-inventory | 200 | Same URL |
| https://www.motorinnautogroup.com/used-trucks | 200 | Same URL |
| https://www.motorinnautogroup.com/where-to-service-toyota-carroll-iowa | 200 | Same URL |
| https://www.motorinnofcarroll.com/ | 200 | Same URL |
| https://www.motorinnofcarroll.com/2026-chevrolet-blazer | 200 | Same URL |
| https://www.motorinnofcarroll.com/2026-chevrolet-blazer-ev | 200 | Same URL |
| https://www.motorinnofcarroll.com/2026-chevrolet-colorado | 200 | Same URL |
| https://www.motorinnofcarroll.com/2026-chevrolet-equinox | 200 | Same URL |
| https://www.motorinnofcarroll.com/2026-chevrolet-equinox-ev | 200 | Same URL |
| https://www.motorinnofcarroll.com/2026-chevrolet-silverado-ev | 200 | Same URL |
| https://www.motorinnofcarroll.com/2026-chevrolet-silverado-hd | 200 | Same URL |
| https://www.motorinnofcarroll.com/2026-chevrolet-silverado-ld | 200 | Same URL |
| https://www.motorinnofcarroll.com/2026-chevrolet-suburban | 200 | Same URL |
| https://www.motorinnofcarroll.com/2026-chevrolet-tahoe | 200 | Same URL |
| https://www.motorinnofcarroll.com/2026-chevrolet-trailblazer | 200 | Same URL |
| https://www.motorinnofcarroll.com/2026-chevrolet-traverse | 200 | Same URL |
| https://www.motorinnofcarroll.com/2026-chevrolet-trax | 200 | Same URL |
| https://www.motorinnofcarroll.com/aboutus.aspx | 200 | Same URL |
| https://www.motorinnofcarroll.com/chevroletspecialoffers | 200 | Same URL |
| https://www.motorinnofcarroll.com/chevy-blazer-for-sale-carroll-iowa | 404 | Planned unpublished canonical target |
| https://www.motorinnofcarroll.com/chevy-dealer-carroll-iowa | 404 | Planned unpublished canonical target |
| https://www.motorinnofcarroll.com/chevy-suvs-for-sale-carroll-iowa | 404 | Planned unpublished canonical target |
| https://www.motorinnofcarroll.com/chevy-trucks-for-sale-carroll-iowa | 404 | Planned unpublished canonical target |
| https://www.motorinnofcarroll.com/collision-shop | 200 | Same URL |
| https://www.motorinnofcarroll.com/ev-protection-plan-chevrolet | 200 | Same URL |
| https://www.motorinnofcarroll.com/finance.aspx | 200 | Same URL |
| https://www.motorinnofcarroll.com/hours.aspx | 200 | Same URL |
| https://www.motorinnofcarroll.com/preapproved.aspx | 200 | Same URL |
| https://www.motorinnofcarroll.com/quote.aspx | 200 | Same URL |
| https://www.motorinnofcarroll.com/searchnew.aspx | 200 | Same URL |
| https://www.motorinnofcarroll.com/searchnew.aspx?Model=Blazer | 200 | Same URL |
| https://www.motorinnofcarroll.com/searchnew.aspx?Model=Blazer%20EV | 200 | Same URL |
| https://www.motorinnofcarroll.com/searchnew.aspx?Model=Colorado | 200 | Same URL |
| https://www.motorinnofcarroll.com/searchnew.aspx?Model=Silverado%201500 | 200 | Same URL |
| https://www.motorinnofcarroll.com/searchnew.aspx?Model=Silverado%202500HD | 200 | Same URL |
| https://www.motorinnofcarroll.com/searchnew.aspx?Model=Suburban | 200 | Same URL |
| https://www.motorinnofcarroll.com/searchused.aspx | 200 | Same URL |
| https://www.motorinnofcarroll.com/service | 200 | Same URL |
| https://www.motorinnofcarroll.com/silverado-1500-vs-ford-f-150 | 200 | Same URL |
| https://www.motorinnofcarroll.com/silverado-1500-vs-ram-1500 | 200 | Same URL |
| https://www.motorinnofcarroll.com/testdrive.aspx | 200 | Same URL |
| https://www.motorinnofcarroll.com/trade.aspx | 200 | Same URL |
| https://www.motorinnofcarroll.com/under-20k.html | 200 | Same URL |
| https://www.motorinnofcarroll.com/we-buy-cars.html | 200 | Same URL |
| https://www.motorinntoyotaofcarroll.com/ | 200 | Same URL |
| https://www.motorinntoyotaofcarroll.com/2026-toyota-grand-highlander.html | 200 | Same URL |
| https://www.motorinntoyotaofcarroll.com/2026-toyota-sequoia.html | 200 | Same URL |
| https://www.motorinntoyotaofcarroll.com/2026-toyota-tundra.html | 200 | Same URL |
| https://www.motorinntoyotaofcarroll.com/certified-pre-owned.html | 200 | Same URL |
| https://www.motorinntoyotaofcarroll.com/electrified | 200 | Same URL |
| https://www.motorinntoyotaofcarroll.com/hours.aspx | 200 | Same URL |
| https://www.motorinntoyotaofcarroll.com/manufacturer-incentives.aspx | 200 | Same URL |
| https://www.motorinntoyotaofcarroll.com/newspecials.html | 200 | Same URL |
| https://www.motorinntoyotaofcarroll.com/preapproved.aspx | 200 | Same URL |
| https://www.motorinntoyotaofcarroll.com/searchnew.aspx | 200 | Same URL |
| https://www.motorinntoyotaofcarroll.com/searchnew.aspx?Model=Sequoia | 200 | Same URL |
| https://www.motorinntoyotaofcarroll.com/searchnew.aspx?Model=Sienna | 200 | Same URL |
| https://www.motorinntoyotaofcarroll.com/searchnew.aspx?Model=Tacoma | 200 | Same URL |
| https://www.motorinntoyotaofcarroll.com/searchnew.aspx?Model=Tundra | 200 | Same URL |
| https://www.motorinntoyotaofcarroll.com/searchused.aspx | 200 | Same URL |
| https://www.motorinntoyotaofcarroll.com/service-center.html | 200 | Same URL |
| https://www.motorinntoyotaofcarroll.com/serviceappmt.aspx | 200 | Same URL |
| https://www.motorinntoyotaofcarroll.com/testdrive.aspx | 200 | Same URL |
| https://www.motorinntoyotaofcarroll.com/toyota-dealer-near-audubon-ia-50025-motor-inn-toyota-of-carroll/ | 200 | Same URL |
| https://www.motorinntoyotaofcarroll.com/toyota-dealer-near-denison-ia-51442-motor-inn-toyota-of-carroll/ | 200 | Same URL |
| https://www.motorinntoyotaofcarroll.com/toyota-dealer-near-jefferson-ia-50129-motor-inn-toyota-of-carroll/ | 200 | Same URL |
| https://www.motorinntoyotaofcarroll.com/toyota-dealers-in-iowa | 404 | Planned unpublished canonical target |
| https://www.motorinntoyotaofcarroll.com/toyota-sequoia-sienna-for-sale-carroll-iowa | 404 | Planned unpublished canonical target |
| https://www.motorinntoyotaofcarroll.com/toyota-sienna | 200 | Same URL |
| https://www.motorinntoyotaofcarroll.com/toyota-tacoma | 200 | Same URL |
| https://www.motorinntoyotaofcarroll.com/toyota-tacoma-tundra-for-sale-carroll-iowa | 404 | Planned unpublished canonical target |
| https://www.motorinntoyotaofcarroll.com/trade.aspx | 200 | Same URL |

### Inventory filter body checks

Returned SRP state was checked beyond HTTP status. Counts are temporary observations, not stock promises.

| Host | Requested model | Results | Outcome |
|---|---|---:|---|
| www.motorinnofcarroll.com | Blazer | 1 | Applied in returned Filters.Model state |
| www.motorinnofcarroll.com | Blazer EV | 0 | Applied in returned Filters.Model state |
| www.motorinnofcarroll.com | Colorado | 3 | Applied in returned Filters.Model state |
| www.motorinnofcarroll.com | Silverado 1500 | 1 | Applied in returned Filters.Model state |
| www.motorinnofcarroll.com | Silverado 2500HD | 0 | FAIL — wrong model name; R1-001 |
| www.motorinnofcarroll.com | Suburban | 0 | Applied in returned Filters.Model state |
| www.motorinntoyotaofcarroll.com | Sequoia | 1 | Applied in returned Filters.Model state |
| www.motorinntoyotaofcarroll.com | Sienna | 0 | Applied in returned Filters.Model state |
| www.motorinntoyotaofcarroll.com | Tacoma | 3 | Applied in returned Filters.Model state |
| www.motorinntoyotaofcarroll.com | Tundra | 3 | Applied in returned Filters.Model state |

The proposed corrected HD URL was also tested: https://www.motorinnofcarroll.com/searchnew.aspx?Model=Silverado%202500%20HD returned 200 and three listings.

Zero results for Blazer EV, Suburban and Sienna were retained as empty filtered searches, not treated as proof of broken URLs or vehicle availability. Their requested models appear in returned filter state; none redirected to an unfiltered page. Used-test-drive preselection remains R1-015.

## Verification details and things found clean

- **GSC tables:** all 108 target rows exactly match query, impressions, clicks and position to one decimal. Ads-40 membership/landing-page annotations match the CSV. All 80 phrasing-map entries were read: 54 non-DERIVED entries exist in the export; 26 are DERIVED. Actual brief phrasing-table impressions match.
- **Cluster arithmetic:** Chevy dealer 13,633; contact 7,379; Chevy SUVs 6,593; Toyota dealer 2,831; Blazer 2,731; used 2,569; Chevy trucks 1,692; Toyota trucks 552; Sequoia/Sienna 311. Sum 38,291. Accurate arithmetic does not cure the routing membership defects.
- **FAQ parity:** all 40 Q&As match verbatim among faq.md, content.md, FAQPage JSON and AI mirrors. Each package has 4 or 5 pairs; every answer has 2–4 sentences. The three missing store/city contexts are R1-011. No “click here.”
- **Actual title/description lengths:** Chevy dealer 52/148; contact 55/148; Chevy SUVs 57/154; Toyota dealer 51/151; Blazer 59/151; used 58/148; Chevy trucks 59/151; Toyota trucks 58/144; Sequoia/Sienna 59/142. All OG fields exist and canonical hosts match briefs. Contact destination semantics remain R1-006.
- **NAP/source checks:** every content and AI file prints (712) 792-5000; schema uses equivalent +1-712-792-5000. All dealer addresses match 1526 Le Clark Road, Carroll, IA 51401. Contact captures and brain/STATE.md:43–45 support identity/phone. The NAP-audit group-homepage excerpt supports store names and Highway 30. Owner notes support sales hours, walk-in appraisals, lender-network financing and Chevrolet certification.
- **Banned facts/terms:** no 522-2526, specified tracking number, 50501, Buick/GMC identity, Spirit Lake/Estherville/Lake City location claim, “bad credit,” or license/insurance test-drive wording in shopper copy/schema. Neighbor-town ZIPs inside existing link URLs are not Carroll address claims. No invented price/payment/APR/lease figure, years-in-business number, award, #1/only/closest claim or competitor factual comparison. Price numbers label existing inventory-search categories.
- **Voice scan:** no banned Voice-DNA terms; zero exclamation marks in every content.md. All package-specific section headings are questions. Structure, CTA and production-language defects are listed above.
- **Placement exception assessed:** both in-place Placement blockquotes explicitly label DealerOn instructions, precede the H1 and are visually separate from the body. They are unambiguous handoff notes under the user's exception, not counted as shopper copy or a defect. Omit them during implementation.
- **Sitemaps:** parsed all 264 group, 217 Chevy and 242 Toyota snapshot URLs. All seven NEW targets are absent. The used refresh URL exists. /Contactus/Carroll is absent, and its current redirect was checked directly.
- **Schema:** all nine files parse. All 10 used types and 26 non-keyword properties exist in the official [Schema.org vocabulary](https://schema.org/version/latest/schemaorg-current-https.jsonld). Dealer inheritance/properties and hours were reviewed against [AutoDealer](https://schema.org/AutoDealer) and [OpeningHoursSpecification](https://schema.org/OpeningHoursSpecification). NAP matches the copy; all @id-only references resolve within their graphs. No aggregateRating or review markup. These checks do not establish search-engine rich-result eligibility.
- **Native validator:** python3 -B content/page-packages/2026-11-23/_src/validate.py exited 0: “checked 9 packages … RESULT: PASS,” with 11 filtered-link warnings. The adversarial verdict remains FAIL because its checks do not cover the demonstrated source, intent and behavior defects.
- **Cleanup:** all Python/curl processes exited. No GUI app, browser tab, server, watcher, SSH session, tunnel or background service was opened. No extra fixtures, evidence files, caches, packages or tests were written. Only this report was created/updated. Fixes and a fresh adversarial pass remain necessary before owner review.
