# Adversarial QA rerun 2: 2026-11-23 page packages

- **Date:** 2026-11-23. Scoped live status GETs: **17:17:47–17:17:52 UTC** (11:17:47–11:17:52 America/Chicago).
- **Overall verdict: PASS. No BLOCKING findings.** Three MINOR issues remain: the accepted pre-handoff OEM sourcing check **R1-009**, plus fresh findings **R3-001** and **R3-002**.
- **Prior findings:** **16 CLOSED, 1 STILL-OPEN (MINOR), 0 REGRESSED**, covering every R1-001 through R1-015 and R2-001 through R2-002.
- **Scope:** the plan and original task brief; all 45 package files, nine AI mirrors and seven generator sources; brain/BRIEF.md, brain/VOICE-DNA.md, brain/STATE.md, owner notes and the house gate in brain/LOG.md:269–272; complete GSC export, all five ads-package files, specified GSC cache, three sitemap snapshots, contact captures, NAP-audit JSON and Buick/GMC removal request. The manifest was also read.
- **Methods:** complete artifact reads, line-numbered source inspection, independent Python 3.13.6 comparisons/arithmetic, native validator with bytecode writing disabled, read-only curl GETs and official Schema.org references. All **54 actual generated artifacts** matched their generator output in memory; the build entrypoint was never executed. Graph discovery found the indexed project but no entries for these new sources, so direct reads were used. The complete actual Markdown/JSON was independently parsed, including FAQ answer text.
- **Network:** available. Exactly one requested status GET per **87 deduplicated scoped URLs**: **80 final 200s, seven expected unpublished-canonical 404s**. All exited 0 with empty stderr. Separate body GETs checked all ten model filters, the contact alias, Chevrolet specials, both group price categories and three hours pages. No model filter failed or remained indeterminate.
- **Authority/limits:** report-only; only this report was written. No rebuild, source fix, test creation, Git mutation, login, form submission, POST, deployment or publication. No rendered-browser or live-account GSC verification. Individual curl timeout 20 seconds; subprocess timeout 25 seconds; no total probe deadline. Total session elapsed and aggregate guarded command time: **unmeasured**. Scoped probes stopped after coverage and confirmation.
- **Input stability:** all **62 batch input files** retained identical SHA-256 hashes, with no additions or removals. Owner decisions were respected, including the frozen about page and separate heavy-duty page. This PASS is the requested **draft-package QA gate**, not source closure for R1-009, publication approval or proof of deployment.

## Per-page × charter verdicts

C1 claims; C2 FAQ parity/AEO; C3 shopper voice/structure/actions; C4 live links/filters; C5 metadata; C6 NAP/owner rules; C7 evidence/routing/arithmetic; C8 schema validity.

| Package | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 |
|---|---|---|---|---|---|---|---|---|
| chevy-dealer-carroll-iowa | PASS | PASS | PASS | MINOR¹ | PASS | PASS | PASS | PASS |
| contactus-carroll | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| chevy-suvs-for-sale-carroll-iowa | MINOR² | PASS | PASS | MINOR¹ | PASS | PASS | PASS | PASS |
| toyota-dealers-in-iowa | PASS | PASS | PASS | MINOR¹ | PASS | PASS | PASS | PASS |
| chevy-blazer-for-sale-carroll-iowa | MINOR² | PASS | PASS | MINOR¹ | PASS | PASS | PASS | PASS |
| used-cars-carroll-iowa | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| chevy-trucks-for-sale-carroll-iowa | MINOR² | PASS | PASS | MINOR¹ | PASS | PASS | PASS | PASS |
| toyota-tacoma-tundra-for-sale-carroll-iowa | MINOR² | PASS | MINOR³ | MINOR¹ | PASS | PASS | PASS | PASS |
| toyota-sequoia-sienna-for-sale-carroll-iowa | MINOR² | PASS | MINOR³ | MINOR¹ | PASS | PASS | PASS | PASS |

¹ Only the declared NEW canonical printed in the AI mirror returns 404. Existing contextual destinations all return 200. This is the documented unpublished state in plan:154, retained as MINOR rather than a new broken-link finding; resolve/recheck before publication.

² R1-009 qualitative OEM descriptor source gap, acceptable as MINOR at this draft gate. No plainly wrong description was established. This does not certify the descriptions against an uncaptured OEM source.

³ R3-001 answer-first polish. The **plan-only C7 MINOR R3-002** is not assigned to otherwise accurate package evidence tables. C8 covers structure/vocabulary/references; claim sourcing is counted under C1.

## Prior-finding closure table

**Path key:** P = content/page-packages/2026-11-23/. All file:line references are current and relative to the repository root. CLOSED applies to the reported defect; fresh, different instances are separately numbered.

| Prior finding | Status | Current file:line evidence; expected → observed |
|---|---|---|
| **R1-001 — HD filter** | **CLOSED** | P/chevy-trucks-for-sale-carroll-iowa/content.md:29, brief.md:65 and P/ai/chevy-trucks-for-sale-carroll-iowa.md:45 use Model=Silverado%202500%20HD. Expected matching HD inventory → fresh body GET returns Filters.Model="Silverado 2500 HD", TotalNumberSearchResults=3, final 200. |
| **R1-002 — offers posted on unsupported page** | **CLOSED** | P/chevy-suvs-for-sale-carroll-iowa/content.md:50, P/chevy-blazer-for-sale-carroll-iowa/content.md:43 and P/chevy-trucks-for-sale-carroll-iowa/content.md:51 now send shoppers to the named store by phone and say **"this page does not quote a lease price."** Expected sourced advice without a site-wide publishing assertion → original specials-page promise and replacement policy are absent; all four representations agree. R2-001 is also closed below. |
| **R1-003 — guaranteed test-drive readiness** | **CLOSED** | P/contactus-carroll/content.md:43, P/used-cars-carroll-iowa/content.md:38 and P/chevy-blazer-for-sale-carroll-iowa/content.md:25 require team confirmation of the vehicle and a time. Expected qualified scheduling → no unconditional "will have it ready" promise in shopper artifacts. Owner test-drive framing remains respected. |
| **R1-004 — prior knowledge of individual used vehicles** | **CLOSED** | P/used-cars-carroll-iowa/content.md:26 describes Toyota/Chevrolet factory service and the brand's own service department. Expected documented brand capability → no claim that staff already know every individual used vehicle. brain/BRIEF.md:14–15 supports factory service. |
| **R1-005 — used/general truck target routing** | **CLOSED** | P/chevy-trucks-for-sale-carroll-iowa/brief.md:13 explicitly excludes the 52/35/19-impression brandless/used rows; :23–31 contains nine retained targets totaling **1,586** at :33. P/toyota-tacoma-tundra-for-sale-carroll-iowa/brief.md:17 excludes used Tacoma's 79; :27–30 contains four retained targets totaling **473** at :32. P/_src/phrasing_map.py:65 and :83 mark supporting used sections DERIVED. Expected group routing for used/general targets → these are no longer brand-page targets; informational used cross-links remain. |
| **R1-006 — contact redirect alias as editable page** | **CLOSED** | P/contactus-carroll/brief.md:4–5 and :15–21, content.md:1, meta.md:3 and :8, schema.json:6–7 and :195, and P/ai/contactus-carroll.md:5 use **/contactus.aspx**. Fresh alias body GET ends there at 200 and returns its self-canonical. Expected coherent live destination/handoff → aligned; owner consolidation decisions are still explicitly pending. |
| **R1-007 — AI production/workflow text** | **CLOSED** | All nine actual AI files have canonical metadata at :5 followed by the Q&A heading at :7, e.g. P/ai/contactus-carroll.md:5–7 and P/ai/chevy-blazer-for-sale-carroll-iowa.md:5–7. P/_src/build.py:233–240 emits no target-host/status instructions. Expected shopper/entity text → workflow fields remain in briefs/manifest, with none in AI bodies. |
| **R1-008 — competing conversion requests** | **CLOSED** | P/contactus-carroll/content.md:43 and P/used-cars-carroll-iowa/content.md:38 now lead with **Call (712) 792-5000** and make test-drive links informational. P/chevy-blazer-for-sale-carroll-iowa/content.md:25 does the same; its FAQ at content.md:47, faq.md:19, schema.json:111 and P/ai/chevy-blazer-for-sale-carroll-iowa.md:23 also uses the phone and confirmation. Expected one primary action with informational support → remaining form invitations removed. Full-batch review found no surviving competing form command. Previously accepted descriptive online-service/test-drive availability is not reopened. |
| **R1-009 — qualitative OEM descriptor sourcing** | **STILL-OPEN — MINOR; acceptable at this gate** | P/chevy-suvs-for-sale-carroll-iowa/content.md:9–18, P/chevy-blazer-for-sale-carroll-iowa/content.md:17, P/chevy-trucks-for-sale-carroll-iowa/content.md:18–23, P/toyota-tacoma-tundra-for-sale-carroll-iowa/content.md:17 and P/toyota-sequoia-sienna-for-sale-carroll-iowa/content.md:17 and :21 retain qualitative size/row/powertrain/use descriptions. Opened fact lists/sitemaps establish model names and page existence, not descriptive OEM passages. P/_src/pages_chevy.py:16 and P/_src/pages_toyota.py:13 still require an OEM check; plan:131 and :145 deliberately retain it. Expected source closure → still pending. Per the supplied severity rule, no plainly wrong description was established and this remains non-blocking draft risk. **Capture/cite OEM passages before handoff.** |
| **R1-010 — Toyota locator completeness** | **CLOSED** | P/toyota-dealers-in-iowa/content.md:9 now identifies Carroll's dealer without claiming that toyota.com lists every dealer. P/_src/pages_toyota.py:41 and :107 agree. Expected no unsupported completeness/closest/only claim → none remains. |
| **R1-011 — lease answers omit store/city** | **CLOSED** | P/chevy-suvs-for-sale-carroll-iowa/faq.md:19, P/chevy-blazer-for-sale-carroll-iowa/faq.md:15 and P/chevy-trucks-for-sale-carroll-iowa/faq.md:15 explicitly name **Motor Inn Chevrolet of Carroll in Carroll, Iowa**. Expected quotable local context → present verbatim in FAQ/content/schema/AI. |
| **R1-012 — FAQ label and SUV/truck generic leads** | **CLOSED for reported instances** | Every content H2 is now a question; examples P/chevy-dealer-carroll-iowa/content.md:41, P/used-cars-carroll-iowa/content.md:40 and both Toyota model content.md:27. P/_src/build.py:132 generates the new FAQ question. P/chevy-suvs-for-sale-carroll-iowa/content.md:9 identifies the lineup; P/chevy-trucks-for-sale-carroll-iowa/content.md:18 gives model/use choices. Expected direct question-led structure → reported instances corrected. Different surviving Toyota leads are R3-001. |
| **R1-013 — plan arithmetic** | **CLOSED** | docs/page-plans/page-plan-2026-11-23.md:23 correctly states **473 + 311 = 784**; :79–81 reproduce **595/17, 629/13 and 235/8**; :84 now gives **212 across nine** whole-town Carroll/Carrol finance/loan rows, excluding Carrollton. Fresh full-export sums agree. The 629 includes both "rav4" and "rav 4" spellings. Expected reproducible membership/totals → corrected. Explicitly rough research estimates remain labeled rough. The separate nonnumeric FAQ coverage assertion is R3-002, not recurrence of this arithmetic defect. |
| **R1-014 — monthly recurrence** | **CLOSED** | P/chevy-dealer-carroll-iowa/brief.md:17 and P/_src/pages_chevy.py:120 now say **"They also appear in the cached 28-day window"**, matching plan:14. The opened pipeline/cache/gsc-ebe12c9ada14b64a0e7109947605c9fda56519dd29dc75342cd69bd0b4e74383.json request is 2026-09-19 through 2026-10-16. Expected only observed-window recurrence → no month-to-month claim remains. Its group 242/255/278 and Toyota 93/108/168 rows reproduce the brief's ranges. |
| **R1-015 — used test-drive preselection** | **CLOSED** | P/used-cars-carroll-iowa/content.md:38 uses plain **/testdrive.aspx**, returning 200. Its AI/brief links also use the plain destination. Expected no unverified Used preselection → no ?type=Used in shopper artifacts. |
| **R2-001 — invented no-online-pricing policy** | **CLOSED** | Same three repaired answers: SUV content.md:50 / faq.md:19 / schema.json:111 / P/ai/chevy-suvs-for-sale-carroll-iowa.md:23; Blazer :43 / :15 / :103 / AI :19; trucks :51 / :15 / :103 / AI :19. P/_src/pages_chevy.py:183, :260 and :341 say **"this page does not quote a lease price."** Expected page-scoped editorial choice → no dealership-wide no-online-figures claim. Fresh Chevrolet specials GET still contains numeric APR terms, without contradicting the repaired wording. |
| **R2-002 — Chevrolet/used sections delay answers** | **CLOSED for reported instances** | P/chevy-dealer-carroll-iowa/content.md:17 now names Colorado/Silverado, SUVs and EVs before navigation; P/used-cars-carroll-iowa/content.md:19 now states the two live price-filter categories and qualifies changing availability. P/_src/pages_chevy.py:51 and P/_src/pages_group.py:160 match. Expected direct answers → both reported leads fixed. R3-001 concerns different Toyota sections. |

## NEW findings

New IDs use **R3-xxx**, following the explicit report-format instruction and avoiding reuse of rerun 1's R2 identifiers.

### R3-001 — MINOR — Two Toyota shopping sections still start with navigation instead of an answer

- **File:line:** P/toyota-tacoma-tundra-for-sale-carroll-iowa/content.md:11–13 and P/toyota-sequoia-sienna-for-sale-carroll-iowa/content.md:11–13, specifically **:13 in both**. Generator: P/_src/pages_toyota.py:135 and :208.
- **Expected:** brain/VOICE-DNA.md:18 and :31 require the first sentence under a heading to answer directly. For "Is a Toyota Tundra/Sienna for sale…?", identify that Motor Inn Toyota of Carroll sells the model, qualify changing availability, then provide the search link.
- **Observed:** both first sentences direct the shopper to a search and model page. They do not answer the sale/dealer question in a self-contained sentence. Their later FAQs provide a direct dealer/model answer, so this is body-copy structure polish, not a false availability claim.
- **Evidence / command:** read-only line inspection, confirmed again after the complete-file audit:
  ~~~sh
  nl -ba content/page-packages/2026-11-23/toyota-tacoma-tundra-for-sale-carroll-iowa/content.md
  nl -ba content/page-packages/2026-11-23/toyota-sequoia-sienna-for-sale-carroll-iowa/content.md
  ~~~
  Exact opening text before the respective second links:
  ~~~text
  Tundra :13: [Search new Tundra inventory](https://www.motorinntoyotaofcarroll.com/searchnew.aspx?Model=Tundra) for what's on the lot today, and see the
  Sienna :13: [Search new Sienna inventory](https://www.motorinntoyotaofcarroll.com/searchnew.aspx?Model=Sienna) and see the
  ~~~
  Both actual files match the generator. Model-filter GETs separately confirm applied filters: Tundra 3 results, Sienna 0; these temporary counts must not become evergreen availability promises.
- **Suggested fix:** lead with "Motor Inn Toyota of Carroll sells the Toyota Tundra [or Sienna] in Carroll, Iowa; inventory changes." Keep navigation and trim/availability checks after that. Update the generator and regenerate in a separate authorized fix pass.
- **Confirmation:** two read-only inspections agreed; batch hashes remained unchanged. This is distinct from the specific R1-012 and R2-002 instances now closed.

### R3-002 — MINOR — Plan claims financing FAQ coverage that several packages do not have

- **File:line:** docs/page-plans/page-plan-2026-11-23.md:**84**. Counterexamples: P/toyota-tacoma-tundra-for-sale-carroll-iowa/faq.md:5–15 and P/toyota-sequoia-sienna-for-sale-carroll-iowa/faq.md:5–19 are their complete Q&A sets; neither answers financing. P/chevy-dealer-carroll-iowa/faq.md:5–23 and P/toyota-dealers-in-iowa/faq.md:5–23 also have no financing answer.
- **Expected:** plan coverage statements describe the delivered packages accurately. Body coverage and FAQ coverage should be distinguished.
- **Observed:** the finance gap row says **"every package answers financing in a FAQ."** The Toyota truck FAQ has only Tacoma availability, Tundra availability and the truck comparison; the Sequoia/Sienna FAQ has only model availability, family choice and size comparison. Their body copy does contain financing/pre-approval information. The financing total **212/9 is correct**; this finding concerns the coverage claim.
- **Evidence / command:** actual FAQ parsing in the full audit, then confirmation with a read-only complete-answer search:
  ~~~python
  for p in build.PAGES:
      answers = " ".join(answer for question, answer in p["faq"])
      if not re.search(r"financ", answers, re.I):
          print(p["slug"])
  ~~~
  Output (all 54 artifacts had already matched their generator output):
  ~~~text
  chevy-dealer-carroll-iowa
  chevy-blazer-for-sale-carroll-iowa
  toyota-dealers-in-iowa
  toyota-tacoma-tundra-for-sale-carroll-iowa
  toyota-sequoia-sienna-for-sale-carroll-iowa
  ~~~
  The Blazer FAQ discusses leases; that does not change the four clear counterexamples. Exact body evidence: Toyota truck content.md:25 and Sequoia/Sienna content.md:25 mention financing/pre-approval.
- **Suggested fix:** change the plan to say packages provide financing information in their body copy and/or FAQs. Adding FAQs is unnecessary to correct this sentence. The adjacent trade-in statement at plan:85 is supported and does not need changing.
- **Confirmation:** complete current FAQ sets and generator definitions agree. This is a plan-only documentation mismatch; no false shopper claim or required FAQ-count failure was found.

## Charters recorded before probes

The initial report recorded these contracts before validation/network probes. The single-file boundary superseded the QA skill's normal sidecars, bookkeeping and telemetry.

| Charter | Contract/source | Read-only method / exit condition |
|---|---|---|
| C1 Claims | Open sources named by briefs/facts comments | Inspect content, FAQ, schema, AI summaries/entity facts; all distinct claims supported or reported |
| C2 FAQ | Verbatim parity; 3–6 pairs; 2–4 self-contained sentences | Parse actual files independently and compare all four representations |
| C3 Voice | Question H2s, answer-first, one primary action, ban list, separable placement notes | Full shopper-copy and generator-intent review |
| C4 Links | Final 200; actual model-filter application | One status curl per unique scoped URL; extra filter-body GETs |
| C5 Metadata | Title ≤60; description ≤155; OG; routed canonical | Parse all nine actual meta files against briefs |
| C6 NAP | Correct phone/address/brands and owner facts | Scan and compare every shopper representation against opened authorities |
| C7 Evidence/routing | Exact GSC rows, totals, phrasing and NEW status | Full export/ads/cache arithmetic, intent membership and sitemap checks |
| C8 Schema | JSON/vocabulary/NAP/references, no reviews/ratings | Parse all nine graphs; official vocabulary and domain/range review |

## Link-check ledger

One invocation per deduplicated scoped URL:
~~~sh
curl -sS -L -o /dev/null -w '%{http_code} %{url_effective}' --max-time 20 URL
~~~

All 87 requests exited 0 with empty stderr; all final URLs equaled their input URL. The seven 404s are only declared NEW canonicals in AI metadata, with no contextual sibling-page link targeting an unpublished page.

| URL | Final code | Final destination / note |
|---|---:|---|
| https://www.motorinnautogroup.com/ | 200 | Same URL |
| https://www.motorinnautogroup.com/best-chevrolet-suvs-for-families | 200 | Same URL |
| https://www.motorinnautogroup.com/blog/2027-toyota-tacoma-trd-pro-honeycomb-reservation-interest | 200 | Same URL |
| https://www.motorinnautogroup.com/blog/heavy-duty-vs-light-duty-trucks | 200 | Same URL |
| https://www.motorinnautogroup.com/carfax-1-owner.html | 200 | Same URL |
| https://www.motorinnautogroup.com/contactus.aspx | 200 | Same URL |
| https://www.motorinnautogroup.com/finance-locations.html | 200 | Same URL |
| https://www.motorinnautogroup.com/highlander-vs-grand-highlander | 200 | Same URL |
| https://www.motorinnautogroup.com/hours.aspx | 200 | Same URL |
| https://www.motorinnautogroup.com/searchnew.aspx | 200 | Same URL |
| https://www.motorinnautogroup.com/service-locations.html | 200 | Same URL |
| https://www.motorinnautogroup.com/testdrive.aspx | 200 | Same URL |
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
| https://www.motorinnofcarroll.com/chevy-blazer-for-sale-carroll-iowa | 404 | Planned NEW canonical; not published |
| https://www.motorinnofcarroll.com/chevy-dealer-carroll-iowa | 404 | Planned NEW canonical; not published |
| https://www.motorinnofcarroll.com/chevy-suvs-for-sale-carroll-iowa | 404 | Planned NEW canonical; not published |
| https://www.motorinnofcarroll.com/chevy-trucks-for-sale-carroll-iowa | 404 | Planned NEW canonical; not published |
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
| https://www.motorinnofcarroll.com/searchnew.aspx?Model=Silverado%202500%20HD | 200 | Same URL |
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
| https://www.motorinntoyotaofcarroll.com/toyota-dealers-in-iowa | 404 | Planned NEW canonical; not published |
| https://www.motorinntoyotaofcarroll.com/toyota-sequoia-sienna-for-sale-carroll-iowa | 404 | Planned NEW canonical; not published |
| https://www.motorinntoyotaofcarroll.com/toyota-sienna | 200 | Same URL |
| https://www.motorinntoyotaofcarroll.com/toyota-tacoma | 200 | Same URL |
| https://www.motorinntoyotaofcarroll.com/toyota-tacoma-tundra-for-sale-carroll-iowa | 404 | Planned NEW canonical; not published |
| https://www.motorinntoyotaofcarroll.com/trade.aspx | 200 | Same URL |

### Model-filter body checks

Command: curl -sS -L --max-time 20 -w '\nFINAL %{http_code} %{url_effective}' URL. Returned HTML was inspected for **TotalNumberSearchResults** and **Filters.Model**. All ten exited 0, empty stderr, final 200 at the requested filtered URL; every returned model matched the requested value.

| Host | Requested/returned Model | Results at check | Verdict |
|---|---|---:|---|
| www.motorinnofcarroll.com | Blazer | 1 | PASS |
| www.motorinnofcarroll.com | Blazer EV | 0 | PASS — filter applied; empty |
| www.motorinnofcarroll.com | Colorado | 3 | PASS |
| www.motorinnofcarroll.com | Silverado 1500 | 1 | PASS |
| www.motorinnofcarroll.com | Silverado 2500 HD | 3 | PASS — corrected HD filter |
| www.motorinnofcarroll.com | Suburban | 0 | PASS — filter applied; empty |
| www.motorinntoyotaofcarroll.com | Sequoia | 1 | PASS |
| www.motorinntoyotaofcarroll.com | Sienna | 0 | PASS — filter applied; empty |
| www.motorinntoyotaofcarroll.com | Tacoma | 3 | PASS |
| www.motorinntoyotaofcarroll.com | Tundra | 3 | PASS |

Example observed HTML:
~~~text
"TotalNumberSearchResults":3,"Filters":{"Model":"Silverado 2500 HD"}
"TotalNumberSearchResults":0,"Filters":{"Model":"Sienna"}
~~~

Empty results alone are not filter failures or proof of permanent unavailability.

### Additional body/source GETs

These are diagnostic body reads, separate from the once-per-URL status ledger.

| URL | Result | Evidence / purpose |
|---|---|---|
| https://www.motorinnautogroup.com/Contactus/Carroll | 200 → https://www.motorinnautogroup.com/contactus.aspx | Self-canonical at destination; R1-006 |
| https://www.motorinnofcarroll.com/newspecials.html | 200, same URL | Still shows numeric APR terms, including 4.9% APR; repaired FAQs no longer assert otherwise |
| https://www.motorinnautogroup.com/under-20000 | 200, same URL | Title identifies used vehicles under $20,000 in Carroll |
| https://www.motorinnautogroup.com/under-15k.html | 200, same URL | Title "Vehicles Under 15k" supports the category label |
| https://www.motorinnautogroup.com/hours.aspx | curl exit 0; body inspected | Service-hours tab construction present; no service schedule copied into drafts |
| https://www.motorinnofcarroll.com/hours.aspx | curl exit 0; body inspected | ServiceHours tab present |
| https://www.motorinntoyotaofcarroll.com/hours.aspx | curl exit 0; body inspected | ServiceHours tab present |
| https://schema.org/version/latest/schemaorg-current-https.jsonld | curl exit 0; JSON parsed | 3,256 vocabulary records; no unknown used type/property |

## Verification evidence

### Exact data and artifact checks

Independent current-file comparisons returned:
~~~text
errors: []
artifacts compared against generator in memory: 54
export rows: 10636; duplicate query strings: 0
exact target rows: 104
FAQ pairs with four-way verbatim parity: 38
brief phrasing occurrences: 59 sourced, 28 DERIVED
phrasing map: 78 unique questions; 50 sourced, 28 DERIVED
all non-DERIVED source queries exist: True
~~~

All target query/impression/click/one-decimal position values match the export; all Ads-40 flags and landing-page annotations match keywords.csv. The generated-file comparison read every actual artifact; it did not treat the generator as proof of claims.

| Package | GSC rows | Impressions | FAQs | Title / meta chars |
|---|---:|---:|---:|---:|
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

Exact plan gap sums reproduce 3,718/46 town rows; approximately 1,300 non-franchise used rows (1,298/37 at ≥15); 595/17 non-franchise lease/service/repair; 629/13 other Toyota model rows including "rav 4"; 235/8 discontinued-Chevy sale rows; and 212/9 Carroll/Carrol finance/loan rows. Whole-word trade/appraisal intent yields no Carroll rows ≥15; the "ram c/v tradesman" model-name row is not trade-in intent. Rough research-only estimates were reviewed as explicitly approximate, not certified as precise clusters.

All 10,636 export rows carry the group property label. The opened cache confirms Chevy BLOCKED-NO-ACCESS/siteUnverifiedUser, Toyota's separate rows and the single 2026-09-19–10-16 window. No fresh account-access status is inferred from that historical cache. The contact routing note's Ads-40 landing distribution reproduces 11 contact-alias rows and two homepage rows.

Parsed **264 group, 217 Chevrolet and 242 Toyota** snapshot URLs. All seven NEW canonicals are absent; both in-place destinations are present. Supporting used cross-links do not reassign brand-page targets.

### Claims, copy, identity and schema

- Opened the cited contacts, NAP homepage excerpt, house rules, owner notes and removal request. They support the shared address, canonical phone, names, Highway 30, franchise/factory service, family ownership, Chevrolet certification, walk-in appraisal, lender network and approved sales hours. Facts.py comments supply shared source pointers. Model/offer sitemap URLs establish existence/names; they leave R1-009 open.
- All **38 Q&As** match verbatim among FAQ, content, schema and AI; each package has 3–5 pairs and each answer has 2–4 sentences, names Motor Inn and Carroll, and contains no "click here."
- All actual metadata lengths pass; OG title/description are present, and canonical/og:url hosts follow the brief routing. No new typo or host conflict was found.
- Every content page and AI mirror prints **(712) 792-5000** and the correct Carroll address; schema uses equivalent **+1-712-792-5000**. No banned printed phone, tracking number, 50501 address, Buick/GMC identity, prohibited store-location claim, "bad credit" or license/insurance test-drive requirement appears in shopper artifacts. Excluded terms in evidence/handoff notes are not counted as shopper copy.
- No invented transaction figure, numerical vehicle specification, stock guarantee, years-in-business figure, award, #1/only/closest assertion or competitor factual comparison was found. Existing inventory price-category labels are supported. The numerical hours are labeled **sales hours**; drafts defer service hours to the hours pages.
- All content H2s are questions; no Voice-DNA ban term and zero exclamation marks in content. The chosen primary action appears early and again at the end; finance, trade, service and test-drive forms are informational references. R3-001 records the remaining answer-first polish.
- **Placement exception:** P/contactus-carroll/content.md:1 and P/used-cars-carroll-iowa/content.md:1 explicitly label in-place handoff instructions before the H1. They identify the target page and what the implementer should keep. They are unambiguously separable from page copy under the supplied exception; no finding is raised. Transfer the body without the placement blockquote. AI mirrors contain no such workflow block.
- **Schema:** all nine files parse; all **10 types and 25 non-keyword properties** exist in the official [Schema.org vocabulary](https://schema.org/version/latest/schemaorg-current-https.jsonld). Dealer/address/brand/hours and FAQ question/answer structures were reviewed against [AutoDealer](https://schema.org/AutoDealer), [OpeningHoursSpecification](https://schema.org/OpeningHoursSpecification) and [FAQPage](https://schema.org/FAQPage). Telephone/address/hours match the copy and owner facts; all @id-only references resolve inside their graphs. No aggregateRating or review markup. This does not assert search-engine rich-result eligibility.

### Native validator

~~~sh
python3 -B content/page-packages/2026-11-23/_src/validate.py
~~~

~~~text
checked 9 packages
[10 filtered-link warnings]
RESULT: PASS
~~~

Exit 0. The ten filter warnings were independently resolved by the body checks above. Its PASS is corroborating evidence; the independent audit found the two MINOR issues its checks do not cover.

## Cleanup and boundaries

Only this report was created/updated. No package, source, test, cache, manifest, prior report or other file was written. Extra skill evidence/telemetry/learning artifacts were omitted to honor the user's single-file instruction. Batch SHA-256 comparison: **62 unchanged, zero changed/added/removed**.

Opened only short-lived local shell/Python/curl processes, which all completed and exited. **No GUI app, browser tab, server, watcher, SSH session, tunnel or background service was opened; none remains to close.** Existing shared software was left running. No fixes or publication were performed.

## Things checked and found clean

- All prior BLOCKING defects are closed; no new BLOCKING defect was demonstrated.
- All 38 FAQ pairs, 104 GSC rows, nine totals, metadata limits and canonical hosts pass.
- All 80 existing URL destinations and ten model filters work, including Silverado HD.
- Canonical NAP, owner facts, schema syntax/references and seven NEW sitemap exclusions pass.
- AI workflow text, unconditional readiness, individual-vehicle familiarity and unsupported publishing-policy claims are removed.
