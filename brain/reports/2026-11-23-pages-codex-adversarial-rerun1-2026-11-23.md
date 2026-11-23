# Adversarial QA rerun 1: 2026-11-23 page packages

- **Date:** 2026-11-23. Read-only live status checks: 17:01:14–17:01:19 UTC (11:01:14–11:01:19 America/Chicago).
- **Overall verdict: FAIL. Two distinct BLOCKING issues remain:** competing test-drive requests (R1-008) and the new unsupported online-pricing policy (R2-001, also the regression of R1-002). **Four MINOR issues:** R1-009, R1-013, R1-014 and R2-002. Do not count R1-002/R2-001 twice.
- **Prior findings:** 10 CLOSED, 4 STILL-OPEN, 1 REGRESSED. **New findings:** R2-001 BLOCKING; R2-002 MINOR.
- **Scope:** the plan, original task, all 45 package files, all 9 AI mirrors, all 7 generator sources, named house rules/owner notes, full GSC export, all 5 ads-package files, specified GSC cache, all 3 sitemap snapshots, all 3 contact captures, NAP-audit JSON and Buick/GMC removal request.
- **Methods:** complete file reads and independent Python standard-library comparisons/arithmetic; actual FAQ answers compared across all four representations; all 54 generated artifacts compared with generator output in memory, without rebuilding. Native validator run with python3 -B. Graph discovery was attempted first; the indexed project has no nodes for these new source files, so direct reads were used.
- **Network:** available. Exactly one status GET per 87 deduplicated scoped URLs, with the requested curl flags and 20-second limit. All exited 0, stderr empty: 80 final 200s and 7 expected unpublished-target 404s. Separate body GETs checked all 10 model filters and targeted claim/redirect questions.
- **Authority/limits:** report-only; no rendered-browser, live-account GSC, form, login, POST, deployment or publication checks. No total probe deadline; individual curl limit 20 seconds, Python subprocess limit 25 seconds. Total session elapsed and aggregate guarded command time: unmeasured. Probes stopped after scoped checks and confirmation. No skill bookkeeping, telemetry, learning-store, screenshot or extra evidence files were written.
- **Input stability:** SHA-256 comparison of all 62 files in this batch directory found no changed, missing or added files during the audit. The packages remain drafts. Owner decisions were respected: approved trade/financing/hours/test-drive facts were not reopened; neither the frozen about page nor the separate heavy-duty page decision was challenged.

## Per-page × charter verdicts

C1 claims; C2 FAQ parity/AEO; C3 shopper voice/structure/actions; C4 live URLs/filters; C5 metadata; C6 NAP/owner rules; C7 evidence/routing/arithmetic; C8 schema syntax/vocabulary/references.

| Package | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 |
|---|---|---|---|---|---|---|---|---|
| chevy-dealer-carroll-iowa | PASS | PASS | MINOR | MINOR¹ | PASS | PASS | MINOR | PASS |
| contactus-carroll | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS |
| chevy-suvs-for-sale-carroll-iowa | FAIL | PASS | PASS | MINOR¹ | PASS | PASS | PASS | PASS |
| toyota-dealers-in-iowa | PASS | PASS | PASS | MINOR¹ | PASS | PASS | PASS | PASS |
| chevy-blazer-for-sale-carroll-iowa | FAIL | PASS | FAIL | MINOR¹ | PASS | PASS | PASS | PASS |
| used-cars-carroll-iowa | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | PASS |
| chevy-trucks-for-sale-carroll-iowa | FAIL | PASS | PASS | MINOR¹ | PASS | PASS | PASS | PASS |
| toyota-tacoma-tundra-for-sale-carroll-iowa | MINOR | PASS | PASS | MINOR¹ | PASS | PASS | PASS | PASS |
| toyota-sequoia-sienna-for-sale-carroll-iowa | MINOR | PASS | PASS | MINOR¹ | PASS | PASS | PASS | PASS |

¹ Only the declared NEW canonical URL printed in its AI mirror returns 404; all existing destinations and all model filters pass. This is the documented unpublished draft state, carried as MINOR rather than a new defect. Recheck after publication. No contextual sibling-page link points to one of those seven targets.

The plan-only finance arithmetic issue R1-013 is C7 MINOR at docs/page-plans/page-plan-2026-11-23.md:84; it is not assigned to an unrelated package. C1 FAIL on the three Chevrolet shopping pages includes R2-001; those pages also retain the MINOR OEM-source gap. C8 evaluates structural validity; false FAQ text is counted under C1.

## Prior-finding closure table

**Path key:** P = content/page-packages/2026-11-23/. Paths below are relative to the repository root. Each closure applies to the original finding; newly discovered adjacent cases are separately numbered.

| Prior ID | Current status | Current file:line evidence and expected → observed |
|---|---|---|
| R1-001 HD filter | **CLOSED** | P/chevy-trucks-for-sale-carroll-iowa/content.md:29 and P/ai/chevy-trucks-for-sale-carroll-iowa.md:45 use Model=Silverado%202500%20HD. Expected matching HD results → fresh body GET gives Filters.Model="Silverado 2500 HD", TotalNumberSearchResults=3, including LT and Custom trucks. |
| R1-002 offers posted | **REGRESSED — BLOCKING; same issue as R2-001** | The old specials-page promise is gone at P/chevy-suvs-for-sale-carroll-iowa/content.md:28, P/chevy-blazer-for-sale-carroll-iowa/content.md:21 and P/chevy-trucks-for-sale-carroll-iowa/content.md:33. However, the replacement FAQs at those files :50, :43 and :51 assert that the dealership does not post fixed numbers online. Expected sourced, neutral advice → an unsupported dealership-wide policy now propagates through all four representations. Detailed evidence and fix in R2-001. |
| R1-003 readiness promise | **CLOSED** | P/chevy-blazer-for-sale-carroll-iowa/content.md:25 and P/used-cars-carroll-iowa/content.md:38 now require team confirmation of vehicle/time. P/contactus-carroll/content.md:43 uses the same qualified approach. The unconditional readiness wording is absent from all shopper representations. |
| R1-004 individual used-vehicle knowledge | **CLOSED** | P/used-cars-carroll-iowa/content.md:26 now describes factory Toyota/Chevrolet service and the brand's service department. Expected brand capability → no assertion of prior knowledge of each individual vehicle. Source brain/BRIEF.md:14–15 supports factory service. |
| R1-005 used/general truck routing | **CLOSED** | P/chevy-trucks-for-sale-carroll-iowa/brief.md:13 excludes the 52/35/19-impression rows; :23–31 contains only the 9 retained targets, totaling 1,586 at :33. P/toyota-tacoma-tundra-for-sale-carroll-iowa/brief.md:17 excludes the 79-impression used Tacoma row; :27–30 contains 4 retained targets, totaling 473 at :32. P/_src/phrasing_map.py:65 and :83 mark used sections DERIVED. The corresponding used FAQs were removed. Supporting used links are allowed. |
| R1-006 redirect alias | **CLOSED** | P/contactus-carroll/brief.md:4–5 and :15–21, content.md:1, meta.md:3 and :8, schema.json:6–7 and :195, and P/ai/contactus-carroll.md:5 now target /contactus.aspx. Fresh alias GET ends at that page with a self-canonical. Other consolidation choices remain explicit owner decisions. |
| R1-007 AI production language | **CLOSED** | All nine AI files now go from the canonical line at :5 to the Q&A heading at :7; e.g. P/ai/contactus-carroll.md:5–7 and P/ai/chevy-blazer-for-sale-carroll-iowa.md:5–7. Actual complete-file checks found no target-host/status/deployment instructions. P/_src/build.py:233–240 emits no such fields; handoff targeting remains in brief.md:9. |
| R1-008 competing actions | **STILL-OPEN — BLOCKING** | Expected one obvious action, with supporting forms informational (brain/VOICE-DNA.md:20, :33). P/contactus-carroll/content.md:7 chooses call/visit, but :43 still says to use the test-drive page. P/used-cars-carroll-iowa/content.md:7 chooses inventory search/call, but :38 still directs use of the test-drive form. P/chevy-blazer-for-sale-carroll-iowa/content.md:5 chooses search/call, but :25 still says to use the test-drive page and :47 says "Request one online"; the latter also remains in faq.md:19, schema.json:111 and P/ai/chevy-blazer-for-sale-carroll-iowa.md:23. Quote/service/trade/pre-approval commands were otherwise converted to informational references. Toyota truck/family test-drive availability is now descriptive; the car-seat preparation advice is not treated as a booking CTA. **Fix:** make the three remaining form invitations informational in every representation, retaining the chosen primary action. |
| R1-009 OEM descriptors | **STILL-OPEN — MINOR; acceptable at this draft gate** | P/chevy-suvs-for-sale-carroll-iowa/content.md:9–18, P/chevy-blazer-for-sale-carroll-iowa/content.md:17, P/chevy-trucks-for-sale-carroll-iowa/content.md:18–23, P/toyota-tacoma-tundra-for-sale-carroll-iowa/content.md:17 and P/toyota-sequoia-sienna-for-sale-carroll-iowa/content.md:17–21 retain qualitative vehicle descriptions. Their fact lists point to sitemaps, not captured descriptive OEM passages. P/_src/pages_chevy.py:16 and P/_src/pages_toyota.py:13 still require an OEM check. "Hybrid" is removed from the i-FORCE MAX description. No plainly wrong descriptor was established; per this rerun's instructions, this remains MINOR and does not independently fail the draft gate. It is not source closure: capture/cite OEM passages before handoff, as plan :131 requires. |
| R1-010 Toyota locator completeness | **CLOSED** | P/toyota-dealers-in-iowa/content.md:9 no longer says toyota.com lists every dealer. P/_src/pages_toyota.py:41 and :107 confirm the removal. No directory-completeness, closest or only claim remains in the shopper representations. |
| R1-011 lease answer context | **CLOSED** | P/chevy-suvs-for-sale-carroll-iowa/faq.md:19, P/chevy-blazer-for-sale-carroll-iowa/faq.md:15 and P/chevy-trucks-for-sale-carroll-iowa/faq.md:15 now explicitly name Motor Inn Chevrolet of Carroll in Carroll, Iowa. All four representations match. Their new policy claim is R2-001, not a context failure. |
| R1-012 shared headings / SUV-truck leads | **CLOSED for the reported instances** | FAQ headings are questions in all nine content files: e.g. P/contactus-carroll/content.md:45, P/used-cars-carroll-iowa/content.md:40 and P/chevy-dealer-carroll-iowa/content.md:41. P/_src/build.py:132 generates the question. P/chevy-suvs-for-sale-carroll-iowa/content.md:9 now answers with the small-to-full-size lineup; P/chevy-trucks-for-sale-carroll-iowa/content.md:18 names the models and uses. Two different surviving generic leads are newly reported as R2-002. |
| R1-013 plan totals | **STILL-OPEN — MINOR** | docs/page-plans/page-plan-2026-11-23.md:23, :79–81 now reproduce 784 combined Toyota-package impressions, 595/17 non-franchise lease/service/repair, 629/13 other Toyota-model rows and 235/8 discontinued-Chevy sale rows. But :84 says Carroll finance is 214/11. Whole-word Carroll/Carrol + finance/loan gives **212/9**. The extra two rows are "car financing carrollton" and "car loan carrollton", one impression each (ads/gsc-keywords-12mo.json:17721 and :17868). A substring match reproduces 214/11 by admitting Carrollton. **Fix:** use whole-town matching and correct the displayed total/count. Other rough research estimates remain explicitly approximate. |
| R1-014 monthly recurrence | **STILL-OPEN — MINOR** | docs/page-plans/page-plan-2026-11-23.md:14 is corrected, but P/chevy-dealer-carroll-iowa/brief.md:17 still says "They do recur month to month"; P/_src/pages_chevy.py:120 reproduces it. The cache request has just the 2026-09-19 through 2026-10-16 window (pipeline/cache/gsc-ebe12c9ada14b64a0e7109947605c9fda56519dd29dc75342cd69bd0b4e74383.json:59515–59521). Expected monthly observations → one annual aggregate and one 28-day window. **Fix:** apply the plan's corrected wording to this brief's generator too. |
| R1-015 used preselection | **CLOSED** | P/used-cars-carroll-iowa/content.md:38, brief.md:74 and P/ai/used-cars-carroll-iowa.md:50 use the plain /testdrive.aspx URL. No ?type=Used remains in actual shopper artifacts. Its final status is 200. No used preselection is now promised. |

## NEW findings

### R2-001 — BLOCKING — Replacement lease FAQs invent a dealership-wide online-pricing policy

- **File:line:** P/chevy-suvs-for-sale-carroll-iowa/content.md:50, faq.md:19, schema.json:111 and P/ai/chevy-suvs-for-sale-carroll-iowa.md:23; P/chevy-blazer-for-sale-carroll-iowa/content.md:43, faq.md:15, schema.json:103 and P/ai/chevy-blazer-for-sale-carroll-iowa.md:19; P/chevy-trucks-for-sale-carroll-iowa/content.md:51, faq.md:15, schema.json:103 and P/ai/chevy-trucks-for-sale-carroll-iowa.md:19. Generator: P/_src/pages_chevy.py:183, :260 and :341.
- **Expected:** refer shoppers to the sales team for current terms, or describe only this draft's choice not to quote figures. A claim about what the dealership publishes elsewhere needs an opened cited source.
- **Observed:** every replacement answer says "the dealership does not post fixed numbers online." The body sections say only "we don't post numbers here," which is narrower. No owner note or fact source establishes the wider policy. SUV brief.md:82–87, Blazer brief.md:68–73 and truck brief.md:74–80 instead cite identity, owner service/trade/financing facts and sitemap URLs.
- **Evidence / command:** complete fact-source reads, four-way FAQ comparison and repeated read-only body GETs of the Chevrolet specials page:
  ~~~sh
  curl -sS -L --max-time 20 -w '\nFINAL %{http_code} %{url_effective}' https://www.motorinnofcarroll.com/newspecials.html
  ~~~
  Both the initial fetch and confirmation returned exit 0, empty stderr and final 200 at the same URL. HTMLParser extraction, excluding script/style/noscript text, found:
  ~~~text
  2026 Chevrolet Colorado LT ... Offer Expires 11/30/2026 ...
  4.9% APR for 75 Months
  FINAL 200 https://www.motorinnofcarroll.com/newspecials.html
  ~~~
- **Confirmation / limits:** this is an example of published numeric finance terms, not evidence of any particular Blazer/Equinox/Tahoe/Silverado lease. It contradicts the unqualified no-online-figures policy; it does not revive the previous unsupported promise about the category-program page. More narrowly interpreting "fixed" as "permanent" would still leave an uncited policy and ambiguous shopper copy.
- **Suggested fix:** replace the second sentence with a page-scoped statement, such as "Terms change, so this page does not quote a lease price." Keep the store/city and phone advice. Update the generator and all four FAQ representations together. Do not add live offer figures to these evergreen drafts.

### R2-002 — MINOR — Two remaining sections delay the answer behind navigation instructions

- **File:line:** P/chevy-dealer-carroll-iowa/content.md:15–20, specifically :17; P/used-cars-carroll-iowa/content.md:17–22, specifically :19. Generator: P/_src/pages_chevy.py:51 and P/_src/pages_group.py:160.
- **Expected:** brain/VOICE-DNA.md:18 requires the first sentence under each heading to answer directly, with evidence/navigation after it.
- **Observed:** under the question about which new Chevrolet models shoppers can buy, the first sentence says "Start with the ... inventory search, or open a model page"; the actual models follow in the bullets. Under the question about finding a used car under $20,000, the first sentence says "Start with the price searches"; it does not explain the available filter or qualify stock.
- **Evidence / command/output excerpt:** complete line-numbered file inspection, confirmed with a read-only Python line filter:
  ~~~text
  chevy-dealer-carroll-iowa/content.md:17: Start with the [new Chevrolet inventory search](...), or open a model page:
  used-cars-carroll-iowa/content.md:19: Start with the price searches. They update with the lot, so you see what's actually available today.
  ~~~
  Both actual files match their generator output. These are different instances from the SUV/truck leads closed under R1-012.
- **Suggested fix:** open the Chevrolet section by naming the model families. Open the used-price section by stating that Motor Inn has live under-$20,000 and under-$15,000 inventory filters and that availability varies. Retain the links afterward; do not promise units are in stock.

## Charters recorded before probes

These were written to this report before validation/network probes; wording is retained here.

| # | Expected | Risk / entrypoint | Isolation / exit |
|---|---|---|---|
| 1 | Each shopper claim has an opened cited source | All copy, FAQs, schema and AI against brief/facts sources | Read-only; all distinct claims supported or reported |
| 2 | FAQ parity, 3–6 answers, 2–4 self-contained sentences | Actual Markdown and JSON | In-memory independent comparisons across nine packages |
| 3 | Shopper voice, question/answer-first headings, one action | Full copy and AI; separate placement note | Read-only; all pages assessed |
| 4 | Final 200 and working model filters | Every deduplicated scoped URL | One status GET each, 20-second limit; extra body GETs for filters |
| 5 | Metadata limits, OG fields and routed canonical | Actual meta files and briefs | Compare nine packages |
| 6 | Correct phone/address and owner facts | All shopper representations | Scan and inspect all pages |
| 7 | Exact GSC data, totals, sources, routing and sitemap absence | Complete export, ads files, cache and snapshots | Independent arithmetic and membership checks |
| 8 | Valid schema vocabulary, IDs, identity, no rating/review | All nine JSON graphs | Parse and compare vocabulary/references |

## Link-check ledger

The status command was invoked once per deduplicated URL below, as separate curl subprocesses:

~~~sh
curl -sS -L -o /dev/null -w '%{http_code} %{url_effective}' --max-time 20 URL
~~~

All final URLs equaled the requested URL. Every request exited 0 with no stderr. The seven 404s are the planned NEW canonical targets, not contextual links to live destinations. Additional diagnostic URLs are listed separately after this scoped ledger.

| URL | Final code |
|---|---:|
| https://www.motorinnautogroup.com/ | 200 |
| https://www.motorinnautogroup.com/best-chevrolet-suvs-for-families | 200 |
| https://www.motorinnautogroup.com/blog/2027-toyota-tacoma-trd-pro-honeycomb-reservation-interest | 200 |
| https://www.motorinnautogroup.com/blog/heavy-duty-vs-light-duty-trucks | 200 |
| https://www.motorinnautogroup.com/carfax-1-owner.html | 200 |
| https://www.motorinnautogroup.com/contactus.aspx | 200 |
| https://www.motorinnautogroup.com/finance-locations.html | 200 |
| https://www.motorinnautogroup.com/highlander-vs-grand-highlander | 200 |
| https://www.motorinnautogroup.com/hours.aspx | 200 |
| https://www.motorinnautogroup.com/searchnew.aspx | 200 |
| https://www.motorinnautogroup.com/service-locations.html | 200 |
| https://www.motorinnautogroup.com/testdrive.aspx | 200 |
| https://www.motorinnautogroup.com/trade.aspx | 200 |
| https://www.motorinnautogroup.com/under-15k.html | 200 |
| https://www.motorinnautogroup.com/under-20000 | 200 |
| https://www.motorinnautogroup.com/used-cars-carroll-iowa | 200 |
| https://www.motorinnautogroup.com/used-inventory | 200 |
| https://www.motorinnautogroup.com/used-trucks | 200 |
| https://www.motorinnautogroup.com/where-to-service-toyota-carroll-iowa | 200 |
| https://www.motorinnofcarroll.com/ | 200 |
| https://www.motorinnofcarroll.com/2026-chevrolet-blazer | 200 |
| https://www.motorinnofcarroll.com/2026-chevrolet-blazer-ev | 200 |
| https://www.motorinnofcarroll.com/2026-chevrolet-colorado | 200 |
| https://www.motorinnofcarroll.com/2026-chevrolet-equinox | 200 |
| https://www.motorinnofcarroll.com/2026-chevrolet-equinox-ev | 200 |
| https://www.motorinnofcarroll.com/2026-chevrolet-silverado-ev | 200 |
| https://www.motorinnofcarroll.com/2026-chevrolet-silverado-hd | 200 |
| https://www.motorinnofcarroll.com/2026-chevrolet-silverado-ld | 200 |
| https://www.motorinnofcarroll.com/2026-chevrolet-suburban | 200 |
| https://www.motorinnofcarroll.com/2026-chevrolet-tahoe | 200 |
| https://www.motorinnofcarroll.com/2026-chevrolet-trailblazer | 200 |
| https://www.motorinnofcarroll.com/2026-chevrolet-traverse | 200 |
| https://www.motorinnofcarroll.com/2026-chevrolet-trax | 200 |
| https://www.motorinnofcarroll.com/aboutus.aspx | 200 |
| https://www.motorinnofcarroll.com/chevy-blazer-for-sale-carroll-iowa | 404 |
| https://www.motorinnofcarroll.com/chevy-dealer-carroll-iowa | 404 |
| https://www.motorinnofcarroll.com/chevy-suvs-for-sale-carroll-iowa | 404 |
| https://www.motorinnofcarroll.com/chevy-trucks-for-sale-carroll-iowa | 404 |
| https://www.motorinnofcarroll.com/collision-shop | 200 |
| https://www.motorinnofcarroll.com/ev-protection-plan-chevrolet | 200 |
| https://www.motorinnofcarroll.com/finance.aspx | 200 |
| https://www.motorinnofcarroll.com/hours.aspx | 200 |
| https://www.motorinnofcarroll.com/preapproved.aspx | 200 |
| https://www.motorinnofcarroll.com/quote.aspx | 200 |
| https://www.motorinnofcarroll.com/searchnew.aspx | 200 |
| https://www.motorinnofcarroll.com/searchnew.aspx?Model=Blazer | 200 |
| https://www.motorinnofcarroll.com/searchnew.aspx?Model=Blazer%20EV | 200 |
| https://www.motorinnofcarroll.com/searchnew.aspx?Model=Colorado | 200 |
| https://www.motorinnofcarroll.com/searchnew.aspx?Model=Silverado%201500 | 200 |
| https://www.motorinnofcarroll.com/searchnew.aspx?Model=Silverado%202500%20HD | 200 |
| https://www.motorinnofcarroll.com/searchnew.aspx?Model=Suburban | 200 |
| https://www.motorinnofcarroll.com/searchused.aspx | 200 |
| https://www.motorinnofcarroll.com/service | 200 |
| https://www.motorinnofcarroll.com/silverado-1500-vs-ford-f-150 | 200 |
| https://www.motorinnofcarroll.com/silverado-1500-vs-ram-1500 | 200 |
| https://www.motorinnofcarroll.com/testdrive.aspx | 200 |
| https://www.motorinnofcarroll.com/trade.aspx | 200 |
| https://www.motorinnofcarroll.com/under-20k.html | 200 |
| https://www.motorinnofcarroll.com/we-buy-cars.html | 200 |
| https://www.motorinntoyotaofcarroll.com/ | 200 |
| https://www.motorinntoyotaofcarroll.com/2026-toyota-grand-highlander.html | 200 |
| https://www.motorinntoyotaofcarroll.com/2026-toyota-sequoia.html | 200 |
| https://www.motorinntoyotaofcarroll.com/2026-toyota-tundra.html | 200 |
| https://www.motorinntoyotaofcarroll.com/certified-pre-owned.html | 200 |
| https://www.motorinntoyotaofcarroll.com/electrified | 200 |
| https://www.motorinntoyotaofcarroll.com/hours.aspx | 200 |
| https://www.motorinntoyotaofcarroll.com/manufacturer-incentives.aspx | 200 |
| https://www.motorinntoyotaofcarroll.com/newspecials.html | 200 |
| https://www.motorinntoyotaofcarroll.com/preapproved.aspx | 200 |
| https://www.motorinntoyotaofcarroll.com/searchnew.aspx | 200 |
| https://www.motorinntoyotaofcarroll.com/searchnew.aspx?Model=Sequoia | 200 |
| https://www.motorinntoyotaofcarroll.com/searchnew.aspx?Model=Sienna | 200 |
| https://www.motorinntoyotaofcarroll.com/searchnew.aspx?Model=Tacoma | 200 |
| https://www.motorinntoyotaofcarroll.com/searchnew.aspx?Model=Tundra | 200 |
| https://www.motorinntoyotaofcarroll.com/searchused.aspx | 200 |
| https://www.motorinntoyotaofcarroll.com/service-center.html | 200 |
| https://www.motorinntoyotaofcarroll.com/serviceappmt.aspx | 200 |
| https://www.motorinntoyotaofcarroll.com/testdrive.aspx | 200 |
| https://www.motorinntoyotaofcarroll.com/toyota-dealer-near-audubon-ia-50025-motor-inn-toyota-of-carroll/ | 200 |
| https://www.motorinntoyotaofcarroll.com/toyota-dealer-near-denison-ia-51442-motor-inn-toyota-of-carroll/ | 200 |
| https://www.motorinntoyotaofcarroll.com/toyota-dealer-near-jefferson-ia-50129-motor-inn-toyota-of-carroll/ | 200 |
| https://www.motorinntoyotaofcarroll.com/toyota-dealers-in-iowa | 404 |
| https://www.motorinntoyotaofcarroll.com/toyota-sequoia-sienna-for-sale-carroll-iowa | 404 |
| https://www.motorinntoyotaofcarroll.com/toyota-sienna | 200 |
| https://www.motorinntoyotaofcarroll.com/toyota-tacoma | 200 |
| https://www.motorinntoyotaofcarroll.com/toyota-tacoma-tundra-for-sale-carroll-iowa | 404 |
| https://www.motorinntoyotaofcarroll.com/trade.aspx | 200 |

### Model-filter body checks

Every requested Model value matched the returned Filters.Model state; no filter redirected to an unfiltered page. These temporary counts establish filter behavior, not future availability.

| Host | Model value | TotalNumberSearchResults | Result |
|---|---|---:|---|
| www.motorinnofcarroll.com | Blazer | 1 | PASS |
| www.motorinnofcarroll.com | Blazer EV | 0 | PASS — applied, empty |
| www.motorinnofcarroll.com | Colorado | 3 | PASS |
| www.motorinnofcarroll.com | Silverado 1500 | 1 | PASS |
| www.motorinnofcarroll.com | Silverado 2500 HD | 3 | PASS — R1-001 closed |
| www.motorinnofcarroll.com | Suburban | 0 | PASS — applied, empty |
| www.motorinntoyotaofcarroll.com | Sequoia | 1 | PASS |
| www.motorinntoyotaofcarroll.com | Sienna | 0 | PASS — applied, empty |
| www.motorinntoyotaofcarroll.com | Tacoma | 3 | PASS |
| www.motorinntoyotaofcarroll.com | Tundra | 3 | PASS |

Body method: curl -sS -L --max-time 20 -w '\nFINAL %{http_code} %{url_effective}' URL; Python inspected TotalNumberSearchResults, returned Filters.Model and the HD listing names. All ten body requests exited 0 with no stderr. The HD response contained three 2026 Silverado 2500 HD trucks (two LT and one Custom).

### Additional diagnostic GETs

These were not extra status checks of the 87 scoped URLs; they were body/claim/redirect investigations.

| URL | Final result | Observation / scope |
|---|---|---|
| https://www.motorinnautogroup.com/Contactus/Carroll | 200 → https://www.motorinnautogroup.com/contactus.aspx | Redirect destination and self-canonical match the repaired contact package |
| https://www.motorinnofcarroll.com/newspecials.html | 200 | Published price/finance figures; fetched again to confirm R2-001 |
| https://www.motorinnofcarroll.com/chevroletspecialoffers | 200 | Customer-category program page; no longer cited by the repaired FAQs |
| https://www.motorinnofcarroll.com/manufacturer-incentives.aspx | 404 | Diagnostic lookup only; this Chevrolet URL is not in the packages and is not a finding |
| https://www.motorinnautogroup.com/under-20000 | 200 | Body title supports the under-$20,000 category |
| https://www.motorinnautogroup.com/under-15k.html | 200 | Body title supports the under-$15,000 category |
| https://schema.org/version/latest/schemaorg-current-https.jsonld | Parsed successfully; curl exit 0 | Official vocabulary check described below |

## Verification evidence and coverage

### Independent checks against actual files

- **Generated-file consistency:** all 54 actual artifacts matched the seven sources' output in memory. No build entrypoint was executed and no generated artifact was rewritten. This check does not make the generator's claims authoritative; underlying cited sources were separately read.
- **GSC:** all **104 target rows** matched exact query, impressions, clicks and one-decimal position in the complete 10,636-row export. There were no duplicate query strings. All rows have the group property label; the plan's property-access caveat is supported by the cached Chevy BLOCKED-NO-ACCESS/siteUnverifiedUser object and the separate Toyota query rows.
- **Ads-40:** membership markers and landing-page annotations matched the complete CSV. The contact routing statement is arithmetically correct: 13 of its targets appear in Ads-40; 11 land on the historical contact alias and 2 on the homepage.
- **Phrasing:** all 78 map entries were read; all 50 non-DERIVED source queries exist in the export. All 87 actual brief phrasing-table rows matched their sources and impressions; 28 are marked DERIVED. The corrected plan's 28 support-question count matches current output.
- **Plan arithmetic:** the nine table totals match their packages. The two Toyota model packages total 473 + 311 = 784. The three LLC rows total 6,447/0 clicks. Town gaps reproduce 3,718/46 with the stated threshold/exclusions; non-franchise lease/service/repair 595/17; other Toyota models 629/13 (including the "rav 4" spelling); discontinued-Chevy sale queries 235/8. The finance exception is R1-013. Rough research figures were treated as expressly approximate, not exact cluster totals.
- **Historical cache:** Toyota positions 6.0 and 10.2, 1,919/329 irrelevant-name impressions, and group/Toyota LLC ranges 242–278 / 93–168 reproduce the cache. It contains one 28-day request window, not monthly recurrence evidence.
- **Routing/sitemaps:** the four removed used/general truck targets are absent from brand target tables. Group pages cover general/used intent; Toyota and Chevrolet new-model pages use their named brand hosts. All 723 sitemap entries were read (group 264, Chevrolet 217, Toyota 242); the seven NEW target URLs are absent. Supporting used-inventory cross-links do not turn them into used-target pages.

| Package | Target rows | Cluster impressions | FAQ pairs | Actual title / meta characters |
|---|---:|---:|---:|---|
| chevy-dealer-carroll-iowa | 17 | 13,633 | 5 | 52 / 148 |
| contactus-carroll | 17 | 7,379 | 5 | 55 / 148 |
| chevy-suvs-for-sale-carroll-iowa | 15 | 6,593 | 4 | 57 / 154 |
| toyota-dealers-in-iowa | 19 | 2,831 | 5 | 51 / 151 |
| chevy-blazer-for-sale-carroll-iowa | 6 | 2,731 | 4 | 59 / 151 |
| used-cars-carroll-iowa | 13 | 2,569 | 5 | 58 / 148 |
| chevy-trucks-for-sale-carroll-iowa | 9 | 1,586 | 3 | 59 / 151 |
| toyota-tacoma-tundra-for-sale-carroll-iowa | 4 | 473 | 3 | 58 / 144 |
| toyota-sequoia-sienna-for-sale-carroll-iowa | 4 | 311 | 4 | 59 / 142 |
| **Total** | **104** | **38,106** | **38** | All within 60 / 155 |

### Claims, identity, copy and schema

- Opened all three cited contact captures, the NAP homepage excerpt, brain/BRIEF.md, brain/VOICE-DNA.md, brain/STATE.md, owner notes and removal request. They establish street/city/ZIP, canonical phone, store names/shared address, Highway 30, franchise/factory-service identity, family ownership, Chevrolet certification, lender network, walk-in trade appraisal and approved sales hours. Model/offer sitemap URLs establish names/page existence; they do not close the qualitative-descriptor evidence gap.
- **All 38 Q&As match verbatim** across faq.md, content.md, schema.json and AI mirrors. Each package has 3–5 pairs and each answer has 2–4 sentences, names Motor Inn and Carroll, and contains no "click here." Headings, entity facts, AI summaries and schema were also read outside those shared answers.
- All actual titles/descriptions meet the requested limits; all OG title/description fields exist; canonical and og:url hosts follow the briefs. The repaired contact WebPage/FAQ IDs and AI canonical use /contactus.aspx.
- Canonical phone/address occur on every content page and AI mirror; schema uses equivalent +1-712-792-5000. No banned printed phone, Carroll ZIP error, Buick/GMC identity, prohibited location claim, "bad credit" or license/insurance test-drive requirement was found in shopper artifacts. Source/handoff notes mentioning excluded numbers or brands are not shopper copy.
- No invented price/payment/APR/lease figure, numerical vehicle spec, years-in-business figure, award, #1/only/closest claim, competitor factual comparison or specific current-stock promise was found. Inventory-category price labels are supported by the named category pages. No unsourced service-hours schedule is printed; the numerical schedule is explicitly sales hours.
- No Voice-DNA banned terms or exclamation marks were found in content pages. All content H2s are questions. The actionable CTA and answer-first exceptions are reported above.
- **Placement notes assessed:** P/contactus-carroll/content.md:1 and P/used-cars-carroll-iowa/content.md:1 explicitly label placement/in-place instructions before the H1, and tell the implementer what to retain. They are unambiguously separate handoff notes under this charter's exception. Omit that blockquote when transferring page copy; no finding was raised.
- **Schema:** all nine JSON files parse; all 10 used types and 25 non-keyword properties occur in the official [Schema.org vocabulary](https://schema.org/version/latest/schemaorg-current-https.jsonld). Graphs use appropriate dealer/address/brand/hours and FAQ question/answer structures; every @id-only reference resolves within its graph. Telephone/address/hours match the copy and owner facts. No aggregateRating or review markup. Reference checks included [AutoDealer](https://schema.org/AutoDealer), [OpeningHoursSpecification](https://schema.org/OpeningHoursSpecification) and [FAQPage](https://schema.org/FAQPage). This is not a rich-result eligibility claim.

### Native validator

~~~sh
python3 -B content/page-packages/2026-11-23/_src/validate.py
~~~

~~~text
checked 9 packages
[10 filtered-link warnings]
RESULT: PASS
~~~

Exit 0. Its ten warnings were independently resolved by the live body checks above. The validator's PASS does not cover the demonstrated policy, CTA, plan-membership, recurrence or generic-lead defects; the adversarial verdict therefore remains FAIL.

## Cleanup and boundaries

Only this requested report was created/updated. No package fixes, product tests, commits, rebuilds, installs, source caches or extra report copies were made. The 62 batch input files retained identical SHA-256 hashes. Report-only skill telemetry/checkpoint sidecars were omitted to honor the single-file boundary.

Opened only short-lived local shell/Python/curl checks; all completed and exited. No GUI app, browser tab, server, watcher, SSH connection, tunnel or background service was opened, so none remains to close. Existing shared software was not stopped.

## Things checked and found clean

- All 38 FAQ pairs have exact four-way parity, permitted lengths and dealership/city context.
- All 104 package GSC rows, nine cluster totals, metadata limits and routed hosts match.
- All 80 existing URL destinations and ten model filters work; the HD filter is corrected.
- Phone/address/owner rules, schema syntax/references and the seven NEW sitemap exclusions pass.
- AI workflow text and the original readiness, individual-vehicle-knowledge and locator-completeness claims are removed.
