# Wave 2 adversarial QA rerun 3

- Date: 2026-11-15
- Revision under test: `80c05871dfebd0ba672fdb42deae958111f86242` (`main`)
- Working-tree inputs: current on-disk files; all tested package and packet files match HEAD. The latest voice fixes are already committed in HEAD, titled “wave2 fix round3.”
- Mode: Full, report-only functional QA
- Scope: Six named HTML delivery packages and their six matching `*-REVIEW.md` packets
- Status: FAIL

**Overall verdict: FAIL.** Four packages pass all five checks. `aboutus-augment-spirit-lake` and `used-car-maintenance-mileage` still contain visible editor, approval, or source-publication workflow language and have claim-mapping gaps. All six packages pass FAQ parity, internal links, and metadata length. No package or review packet was changed.

The charter and authored-content scope follow [rerun 2](wave2-codex-adversarial-rerun2-2026-11-15.md). Verdicts below come from fresh reads, parsing, semantic review, and live curl requests; prior PASS results were not carried forward as proof.

## Charters

### 1. Claim traceability

- Contract: Every factual shopper-facing claim is mapped to a source in the matching review packet or visibly marked `[NEEDS-VERIFY]`.
- Risk: Unsupported claims could be published as fact.
- Entrypoint: Authored HTML body copy, FAQ structured data, and matching packet source map.
- Isolation: Read-only current-revision inputs; no content edits.
- Probe: Full reads of the six packets and line-numbered authored text, followed by claim-to-source comparison. Particular attention to factual assertions introduced by the latest rewrite.
- Exit condition: Every claim is accounted for, or the page fails with exact evidence.

### 2. FAQ parity

- Contract: `FAQPage` JSON-LD parses, contains exactly three questions, and all three visibly rendered questions match its wording with substantively matching answers.
- Risk: Search markup could contradict or overstate the visible page.
- Entrypoint: Each HTML package's JSON-LD and visible headings/answers.
- Isolation: Local Python JSON parser and BeautifulSoup; no browser or publication.
- Probe: Parse JSON-LD, locate FAQPage objects, count entities, compare normalized visible question wording, and manually compare answers.
- Exit condition: Parse and all 3/3 question-and-answer pairs pass, or the page fails.

### 3. Shopper voice

- Contract: Visible `#content-main` copy follows `brain/VOICE-DNA.md` and contains zero editor, production, approval, permission, page-lifecycle, or publication language.
- Risk: Internal workflow instructions could reach shoppers.
- Entrypoint: All visible authored text, including FAQ answers, source footers, and visible verification markers.
- Isolation: Static extraction excluding comments, scripts, styles, templates, and noscript blocks; no rewriting.
- Probe: Banned-word and workflow-phrase scans plus manual review of every section. Explicitly inspect “not listed yet,” “will appear,” “yet to be,” permission, summarization, publication, and source-availability wording.
- Exit condition: Zero visible workflow-language leaks and no material voice violation, or the page fails. A verification marker does not exempt editor instructions inside it.

### 4. Internal links

- Contract: Every `motorinnautogroup.com` HTTP(S) href in authored `#content-main` content returns final HTTP 200 with `curl -L`.
- Risk: Shoppers could reach broken destinations.
- Entrypoint: All 26 extracted authored internal href occurrences, including repeated URLs.
- Isolation: Read-only public GET requests; no form submissions or site changes.
- Probe: A separate curl request for every occurrence, following redirects, with a 20-second URL limit.
- Exit condition: Every occurrence returns final 200, or the containing page fails.

### 5. Metadata length

- Contract: Title is 50-60 characters and meta description is 120-158 characters, inclusive.
- Risk: Search snippets may truncate or underuse available space.
- Entrypoint: Each HTML `<title>` and `<meta name="description">`; corresponding delivery `metadata.json` checked for consistency.
- Isolation: Local parsing and Unicode character counts.
- Exit condition: Both lengths fall in range, or the page fails.

## Per-page verdict

| Page | 1. Claims sourced or flagged | 2. FAQPage | 3. Shopper voice | 4. Internal hrefs | 5. Title / meta | Overall |
|---|---|---|---|---|---|---|
| `aboutus-augment-spirit-lake` | **FAIL** — categorical inventory-filter and all-location coverage assertions are not established by its source map; nine flags remain | **PASS** — parses; 3/3 wording and substantive answer matches | **FAIL** — visible “approved wording,” filter-testing instructions, and “No location-specific claim is made here” | **PASS** — 6/6 final 200 | **PASS** — 52 / 151 | **FAIL** |
| `heavy-duty-vs-light-duty-trucks` | **PASS** — Ford/Chevrolet source map accounts for ratings, percentages, classifications, and configuration cautions | **PASS** — parses; 3/3 wording and substantive answer matches | **PASS** — no material voice violation found | **PASS** — 4/4 final 200 | **PASS** — 52 / 136 | **PASS** |
| `highlander-vs-grand-highlander` | **PASS** — Toyota map covers dimensions, seating, cargo, and six computed deltas | **PASS** — parses; 3/3 wording and substantive answer matches | **PASS** — prior footer defect remains fixed | **PASS** — 4/4 final 200 | **PASS** — 54 / 139 | **PASS** |
| `toyota-rav4-carroll-iowa` | **PASS** — Toyota map covers model facts, upholstery, and dated sales framing | **PASS** — parses; 3/3 wording and substantive answer matches | **PASS** — no material voice violation found | **PASS** — 4/4 final 200 | **PASS** — 50 / 131 | **PASS** |
| `trim-levels-explained` | **PASS** — Toyota/KBB/FTC/Ford map covers definitions, upholstery, equipment confirmation, and capability cautions | **PASS** — parses; 3/3 wording and substantive answer matches | **PASS** — no material voice violation found | **PASS** — 4/4 final 200 | **PASS** — 55 / 139 | **PASS** |
| `used-car-maintenance-mileage` | **FAIL** — new shopper-facing phone number has no mapping in its matching packet; four process/source flags remain | **PASS** — parses; 3/3 wording and substantive answer matches | **FAIL** — source-publication instruction and “Until a named original source is available” remain visible | **PASS** — 4/4 final 200 | **PASS** — 52 / 151 | **FAIL** |

Result: **4 PASS, 2 FAIL.** Across the 30 page/check combinations: **26 PASS, 4 FAIL**. One failed check fails the page and the package set.

## Contract outcomes

| Contract and source | Exact probe / evidence | Expected → observed | Outcome |
|---|---|---|---|
| Claim support, user rubric and six review packets | Full six-packet reads; extraction program below; exact source-map comparisons in W2-RERUN3-003 and -004 | Every factual claim mapped or flagged → two packages have unmapped factual assertions | **FAIL** |
| FAQPage parsing and visible parity, user rubric | Python `json.loads`; entity counts; heading normalization; manual comparison of all answers; 18-pair table below | Six parseable FAQPage blocks, exactly three entities each, 18/18 question matches and 18/18 substantive answer matches → observed | **PASS** |
| Shopper voice, user rubric and `brain/VOICE-DNA.md:7-21,27-33` | Visible-text extraction, workflow/banned-word scan, full manual review, and identical replays of both failing packages | Zero visible editor/approval/publication workflow language → two pages retain it | **FAIL** |
| Internal link health, prior report's authored-content scope | 26 separate curl GETs; command and occurrence-level receipts below | Every authored internal href returns final HTTP 200 → 26/26 returned 200 with exit code 0 | **PASS** |
| Title/meta length, user rubric | Unicode character counts; HTML-to-`metadata.json` comparison | Title 50-60 and meta 120-158 → 6/6 titles and 6/6 descriptions pass; all six metadata files agree | **PASS** |

No browser or visual score applies to this functional/static QA run.

## Findings

### W2-RERUN3-001: About Us still exposes approval and editorial instructions

- Classification / severity: Content defect; release-blocking under the zero-workflow-language rule.
- Expected: Visible text answers shoppers or marks a missing fact without instructing an editor to approve wording, test a filter, or describe the page's claims.
- Observed: `index.html:888` visibly says “provide the approved wording”; `:896` says “provide and test the permanent Spirit Lake used-inventory filter”; `:908` asks what “reconditioning language is approved”; `:912` says “No location-specific claim is made here” and refers to waiting until a filter is verified. These are visible paragraphs inside `#content-main`, not comments or packet-only notes.
- Evidence: `deliveries/site-packages/2026-11-15/motorinnautogroup/aboutus-augment-spirit-lake/index.html:888,896,908,912`. HTML SHA-256: `107426b0e69afad2224aed35cec1ce20bd83ec7ea820f9b1567e306340339168`.
- Confirmation: The same extraction command was rerun on this page and its packet. The complete structured extraction was identical, including line text and input hashes.
- Regression detail: The earlier “not stated on this page yet,” “not listed yet,” and “will appear above” failures have been removed. The unchanged FAQ/editor instructions still fail the contract.
- Next action: Keep approval and testing instructions in the review packet. Express the remaining unknowns as factual verification flags and direct shopper guidance. Report-only; no edit made.

### W2-RERUN3-002: Maintenance still exposes source-research and publication workflow

- Classification / severity: Content defect; release-blocking under the zero-workflow-language rule.
- Expected: Visible text gives the maintenance answer or flags an unknown without asking a reader to locate a source's publication or wait for editorial research.
- Observed: `index.html:897` renders “[NEEDS-VERIFY: confirm the MotorHappy source and where it is published.] Until a named original source is available, follow the vehicle maker’s maintenance schedule, keep complete service records, and get new problems diagnosed early.” The marker contains a source-publication research instruction; the following unbracketed sentence still conditions the answer on an original source becoming available.
- Evidence: `deliveries/site-packages/2026-11-15/motorinnautogroup/used-car-maintenance-mileage/index.html:897`. HTML SHA-256: `31a423c1d672218ca16ed832efc4ed19708388534f7b0631b786ba6c3d05939c`.
- Confirmation: The same extraction command was rerun on this page and its packet. The complete structured extraction was identical, including line text and input hashes.
- Regression detail: “obtain permission,” “before summarizing,” and “has not published its list ... yet” are gone. This finding concerns the remaining source-publication instruction and source-availability wording, not the removed phrases.
- Next action: Keep source acquisition/publication questions in the packet and retain a shopper-facing verification flag and maintenance fallback without a source-research instruction. Report-only; no edit made.
- False-positive exclusion: “approving a major repair” at `:905` concerns the shopper's repair decision and was not counted as editorial approval language.

### W2-RERUN3-003: About Us inventory assertions exceed the supplied source mapping

- Classification / severity: Claim-traceability defect; release-blocking under check 1.
- Expected: A categorical statement about the absence of a location filter or coverage of every location has a matching source mapping, or is itself visibly marked as unverified.
- Observed: `index.html:895` states “There is no Spirit Lake-only inventory view; the general used-inventory search covers every Motor Inn Auto Group location.” The all-location assertion is repeated outside the verification brackets at `:896`. The packet's source map only identifies the production About Us structure/URL and general inventory destination; it does not map evidence for filter nonexistence or exhaustive location coverage. Its own open item 6 still asks for the permanent Spirit Lake-only filter and proof that it persists.
- Evidence: `deliveries/site-packages/2026-11-15/motorinnautogroup/aboutus-augment-spirit-lake/index.html:895-896`; `content/drafts/seo/aboutus-augment-spirit-lake-REVIEW.md:35-40,51`.
- Exact packet contrast: `REVIEW.md:38` maps “General used-inventory destination”; `:51` leaves “Permanent Spirit Lake-only used-inventory filter and proof that the filter persists” open. Neither establishes the categorical assertions.
- Confirmation: Identical replay of the HTML and complete packet; nine visible verification markers were recounted. The adjacent instruction to “provide and test” a filter does not mark the unbracketed absence/coverage assertions as unknown.
- Limit: This is a missing mapping, not a finding that the inventory assertions are false. A final HTTP 200 establishes reachability, not complete store coverage or absence of another filter.
- Next action: Map verified filter/coverage evidence in the packet or qualify and visibly flag those particular assertions. Report-only; no edit made.

### W2-RERUN3-004: Maintenance's new phone number lacks a matching packet source

- Classification / severity: Claim-traceability defect; release-blocking under check 1.
- Expected: A shopper-facing dealership contact number is mapped to its source in this page's matching packet or visibly flagged.
- Observed: The latest rewrite adds `712-792-5000` at `index.html:908`. The complete maintenance packet contains no occurrence of the number, and its source map covers Toyota maintenance guidance, FTC inspection/history guidance, and AAA warning-sign/corrosion guidance, with no dealership-contact source. Its four open flags concern MotorHappy and inspection processes, not the phone number.
- Evidence: `deliveries/site-packages/2026-11-15/motorinnautogroup/used-car-maintenance-mileage/index.html:908`; `content/drafts/seo/used-car-maintenance-mileage-REVIEW.md:27-37,44-51`. `git diff HEAD^ HEAD -- <maintenance-package>/index.html` confirms the number was introduced by the round-3 rewrite.
- Confirmation: Identical replay of the complete page/packet extraction; a separate full-packet phone-pattern check returned zero occurrences.
- Limit: This is a missing source-map entry, not a claim that the phone number is incorrect. A number elsewhere in the site template or another page's packet does not supply this matching packet's required mapping.
- Next action: Add the dealership contact source and number mapping to this packet, or visibly flag the number. Report-only; no edit made.

## Claim-support specifics

Package paths below are under `deliveries/site-packages/2026-11-15/motorinnautogroup/`; packets are under `content/drafts/seo/`.

- About Us: Existing About Us/inventory destinations map to `aboutus-augment-spirit-lake-REVIEW.md:35-40`. Nine entity, address, phone, hours, filter, transfer, department, and inspection unknowns remain visibly flagged at `index.html:883-908`. The unflagged categorical inventory assertions at `:895-896` remain a gap. **FAIL**, finding -003.
- Heavy-duty trucks: `heavy-duty-vs-light-duty-trucks-REVIEW.md:29-36` maps 13,500-lb/2,440-lb F-150 figures, 40,000-lb/8,000-lb Super Duty figures, 10%/15% load figures, class naming, and configuration cautions. These correspond to `index.html:885-914`. No public prices, awards, or stock guarantees were introduced. **PASS**.
- Highlander: `highlander-vs-grand-highlander-REVIEW.md:32-36` maps both models' 2026 dimensions, cargo, seating, and all six differences at `index.html:882-913`. Recomputing the displayed values gives 6.5 in., 3.9 in., 5.5 in., 4.6 cu. ft., 9.5 cu. ft., and 13.2 cu. ft. **PASS**.
- RAV4: `toyota-rav4-carroll-iowa-REVIEW.md:27-32` maps 226/236 hp, 8.1-in. clearance, 1,750/3,500-lb towing, drivetrain/upholstery details, and the dated 2025 sales framing at `index.html:882-913`. **PASS**.
- Trim levels: `trim-levels-explained-REVIEW.md:29-36` maps Toyota upholstery, KBB definitions, FTC equipment confirmation, and Ford configuration cautions to `index.html:882-919`. **PASS**.
- Maintenance: `used-car-maintenance-mileage-REVIEW.md:27-37` maps schedule/inspection/corrosion guidance. Mileage milestones are expressly review points, not universal replacement intervals. Four source/process unknowns remain flagged at `index.html:897,909`. The new phone number at `:908` has no matching packet source. **FAIL**, finding -004.

The contract is claim mapping against the supplied packets, not a fresh independent audit of every external source's factual truth. Known source mapping does not mean that a flagged business detail is approved.

## FAQPage specifics

All six JSON-LD sets parsed without errors. Each page contains one FAQPage with exactly three Question entities and accepted answers. All 18 schema questions match visible headings after the same case/whitespace normalization used in rerun 2. All 18 answers match in substance after manual comparison with the visible answer and relevant on-page details.

As in rerun 2, a matching visible question may be the H1, an H2, or an H3. A schema answer can summarize the visible response. For example, Highlander's cargo figures also appear in its visible comparison table. FAQ parity does not excuse the About Us FAQ's voice defect.

| Page | Schema question | Matching visible heading | Wording / answer substance |
|---|---|---|---|
| `aboutus-augment-spirit-lake` | 1. Should you confirm a used vehicle's location before visiting? | `index.html:911` | PASS / PASS |
| `aboutus-augment-spirit-lake` | 2. Does the general inventory page show only Spirit Lake vehicles? | `index.html:912` | PASS / PASS |
| `aboutus-augment-spirit-lake` | 3. Are transfers between locations guaranteed? | `index.html:913` | PASS / PASS |
| `heavy-duty-vs-light-duty-trucks` | 1. How does a light-duty full-size truck compare to a heavy-duty model for everyday use? | `index.html:884` | PASS / PASS |
| `heavy-duty-vs-light-duty-trucks` | 2. Why can payload run out before towing capacity? | `index.html:896` | PASS / PASS |
| `heavy-duty-vs-light-duty-trucks` | 3. Does a 2500 badge tell you the towing capacity? | `index.html:919` | PASS / PASS |
| `highlander-vs-grand-highlander` | 1. Is the Grand Highlander bigger than the Highlander? | `index.html:881` | PASS / PASS |
| `highlander-vs-grand-highlander` | 2. How much third-row legroom does the Grand Highlander add? | `index.html:921` | PASS / PASS |
| `highlander-vs-grand-highlander` | 3. Does the Grand Highlander have more cargo room? | `index.html:922` | PASS / PASS |
| `toyota-rav4-carroll-iowa` | 1. What factors explain the Toyota RAV4's market dominance? | `index.html:884` | PASS / PASS |
| `toyota-rav4-carroll-iowa` | 2. Does every 2026 RAV4 have all-wheel drive? | `index.html:910` | PASS / PASS |
| `toyota-rav4-carroll-iowa` | 3. Does every RAV4 use SofTex seats? | `index.html:912` | PASS / PASS |
| `trim-levels-explained` | 1. What do car trim levels mean? | `index.html:883` | PASS / PASS |
| `trim-levels-explained` | 2. What does trim level mean on a truck? | `index.html:890` | PASS / PASS |
| `trim-levels-explained` | 3. Is SofTex leather? | `index.html:917` | PASS / PASS |
| `used-car-maintenance-mileage` | 1. How many miles can a car last before it breaks down? | `index.html:881` | PASS / PASS |
| `used-car-maintenance-mileage` | 2. Can maintenance guarantee a car will reach a certain mileage? | `index.html:921` | PASS / PASS |
| `used-car-maintenance-mileage` | 3. Should you buy a used car without service records? | `index.html:922` | PASS / PASS |

## Internal-link results

All 26 authored internal href occurrences were requested separately. Each curl exited 0 and returned final HTTP 200. Eight distinct URLs were tested; repeated occurrences were not skipped.

Exact command shape, executed once per occurrence with its extracted URL:

```sh
curl -L --fail-with-body --max-time 20 --connect-timeout 10 --silent --show-error --output /dev/null --write-out '%{http_code}|%{url_effective}|%{num_redirects}|%{time_total}\n' 'EXTRACTED_URL'
```

The URL placeholder above is expanded from each row; output fields are final status, final URL, redirects, and curl total seconds. Curl stderr was not suppressed; no errors were reported.

| URL | Occurrences tested | Final status | Final URL / redirects |
|---|---:|---:|---|
| `https://www.motorinnautogroup.com/searchused.aspx` | 3 | 200 | `https://www.motorinnautogroup.com/used-inventory`; 1 redirect(s) |
| `https://www.motorinnautogroup.com/aboutus.aspx` | 1 | 200 | same URL; 0 redirect(s) |
| `https://www.motorinnautogroup.com/car-maintenance-by-mileage` | 4 | 200 | same URL; 0 redirect(s) |
| `https://www.motorinnautogroup.com/2022-toyota-rav4-carroll-ia` | 5 | 200 | same URL; 0 redirect(s) |
| `https://www.motorinnautogroup.com/vehicle-trim-levels-explained` | 5 | 200 | same URL; 0 redirect(s) |
| `https://www.motorinnautogroup.com/searchall.aspx` | 4 | 200 | same URL; 0 redirect(s) |
| `https://www.motorinnautogroup.com/highlander-vs-grand-highlander` | 2 | 200 | same URL; 0 redirect(s) |
| `https://www.motorinnautogroup.com/blog/heavy-duty-vs-light-duty-trucks` | 2 | 200 | same URL; 0 redirect(s) |

Occurrence-level receipts; input paths are relative to the package root named above. Each `searchused.aspx` request resolved to `https://www.motorinnautogroup.com/used-inventory`; all other final URLs equal the requested URL.

| Request | Authored href evidence | Requested path | Exit | Final HTTP | Redirects | Curl seconds |
|---|---|---|---:|---:|---:|---:|
| 01 | `aboutus-augment-spirit-lake/index.html:884` | `/searchused.aspx` | 0 | 200 | 1 | 0.491708 |
| 02 | `aboutus-augment-spirit-lake/index.html:914` | `/aboutus.aspx` | 0 | 200 | 0 | 0.245790 |
| 03 | `aboutus-augment-spirit-lake/index.html:914` | `/searchused.aspx` | 0 | 200 | 1 | 0.320889 |
| 04 | `aboutus-augment-spirit-lake/index.html:915` | `/car-maintenance-by-mileage` | 0 | 200 | 0 | 0.234301 |
| 05 | `aboutus-augment-spirit-lake/index.html:915` | `/2022-toyota-rav4-carroll-ia` | 0 | 200 | 0 | 0.230077 |
| 06 | `aboutus-augment-spirit-lake/index.html:915` | `/vehicle-trim-levels-explained` | 0 | 200 | 0 | 0.248400 |
| 07 | `heavy-duty-vs-light-duty-trucks/index.html:915` | `/searchall.aspx` | 0 | 200 | 0 | 0.260836 |
| 08 | `heavy-duty-vs-light-duty-trucks/index.html:922` | `/vehicle-trim-levels-explained` | 0 | 200 | 0 | 0.249407 |
| 09 | `heavy-duty-vs-light-duty-trucks/index.html:922` | `/car-maintenance-by-mileage` | 0 | 200 | 0 | 0.240491 |
| 10 | `heavy-duty-vs-light-duty-trucks/index.html:922` | `/2022-toyota-rav4-carroll-ia` | 0 | 200 | 0 | 0.250184 |
| 11 | `highlander-vs-grand-highlander/index.html:917` | `/searchall.aspx` | 0 | 200 | 0 | 0.274717 |
| 12 | `highlander-vs-grand-highlander/index.html:924` | `/2022-toyota-rav4-carroll-ia` | 0 | 200 | 0 | 0.232774 |
| 13 | `highlander-vs-grand-highlander/index.html:924` | `/vehicle-trim-levels-explained` | 0 | 200 | 0 | 0.235184 |
| 14 | `highlander-vs-grand-highlander/index.html:924` | `/car-maintenance-by-mileage` | 0 | 200 | 0 | 0.248040 |
| 15 | `toyota-rav4-carroll-iowa/index.html:907` | `/searchall.aspx` | 0 | 200 | 0 | 0.269370 |
| 16 | `toyota-rav4-carroll-iowa/index.html:914` | `/highlander-vs-grand-highlander` | 0 | 200 | 0 | 0.243153 |
| 17 | `toyota-rav4-carroll-iowa/index.html:914` | `/vehicle-trim-levels-explained` | 0 | 200 | 0 | 0.237903 |
| 18 | `toyota-rav4-carroll-iowa/index.html:914` | `/car-maintenance-by-mileage` | 0 | 200 | 0 | 0.277195 |
| 19 | `trim-levels-explained/index.html:908` | `/searchall.aspx` | 0 | 200 | 0 | 0.250644 |
| 20 | `trim-levels-explained/index.html:920` | `/2022-toyota-rav4-carroll-ia` | 0 | 200 | 0 | 0.250284 |
| 21 | `trim-levels-explained/index.html:920` | `/highlander-vs-grand-highlander` | 0 | 200 | 0 | 0.250343 |
| 22 | `trim-levels-explained/index.html:920` | `/blog/heavy-duty-vs-light-duty-trucks` | 0 | 200 | 0 | 0.251619 |
| 23 | `used-car-maintenance-mileage/index.html:917` | `/searchused.aspx` | 0 | 200 | 1 | 0.315647 |
| 24 | `used-car-maintenance-mileage/index.html:924` | `/vehicle-trim-levels-explained` | 0 | 200 | 0 | 0.242318 |
| 25 | `used-car-maintenance-mileage/index.html:924` | `/2022-toyota-rav4-carroll-ia` | 0 | 200 | 0 | 0.255592 |
| 26 | `used-car-maintenance-mileage/index.html:924` | `/blog/heavy-duty-vs-light-duty-trucks` | 0 | 200 | 0 | 0.248531 |

## Metadata specifics

Counts are Unicode characters in parsed HTML values. HTML and delivery `metadata.json` title/description values agree for all six packages.

| Page | Title length | Meta length | HTML evidence | Result |
|---|---:|---:|---|---|
| `aboutus-augment-spirit-lake` | 52 | 151 | `index.html:6` / `:14` | PASS |
| `heavy-duty-vs-light-duty-trucks` | 52 | 136 | `index.html:6` / `:14` | PASS |
| `highlander-vs-grand-highlander` | 54 | 139 | `index.html:6` / `:14` | PASS |
| `toyota-rav4-carroll-iowa` | 50 | 131 | `index.html:6` / `:14` | PASS |
| `trim-levels-explained` | 55 | 139 | `index.html:6` / `:14` | PASS |
| `used-car-maintenance-mileage` | 52 | 151 | `index.html:6` / `:14` | PASS |

## Evidence and timing

- Evidence location: this report's exact excerpts, per-pair/per-request tables, input hashes, and reproduction command below. No external evidence bundle was created.
- Runtime/native tools: Python 3.13.6, BeautifulSoup 4.12.3, Python JSON/hash libraries, Git, and curl.
- Input ownership: read-only existing packages and packets at the stated HEAD. The six delivery metadata files were also read for consistency.
- Stability: all 18 package HTML, delivery metadata, and review-packet hashes were unchanged between extraction and final input verification. `git diff --exit-code HEAD --` returned 0 before the report write.
- Confirmation: the exact extraction command below was rerun for both failing pages. Complete structured output matched each initial extraction.
- Probe budget: full functional mode without a total time limit or aggregate command guard. Local parsers read the finite supplied input files; curl had a 20-second URL limit and 10-second connection limit.
- Guarded command time: not measured with the optional gstack evidence guard; no guard-duration claim is made.
- Measured curl interval: sum of the 26 individual `time_total` values is **6.855397 seconds**. This excludes parsing, packet review, report writing, and cleanup.
- Total session elapsed: unmeasured; final report write, acknowledgement, and verification were not complete when assembled.
- Stop reason: all five requested checks completed for all six packages.
- Storage limitation: Glyph preflight exited 11 with `Glyph preflight failed: missing SMB password — No keychain password for glyphshare@spark-fa5a and GLYPH_SMB_PASSWORD is unset`. No reconnect, credential change, or write to Glyph followed. The user's explicitly requested report is the sole output and contains the audit evidence.
- Tooling adaptation: no gstack state/telemetry, checkpoint sidecars, scratch scripts, or learning-store files were written. The fixed report-only boundary and unavailable Glyph storage take precedence over optional artifact bookkeeping.

### Input fingerprints

HTML paths are `<package-root>/<page>/index.html`; packet paths are `content/drafts/seo/<page>-REVIEW.md`.

| Page | HTML SHA-256 | Review packet SHA-256 |
|---|---|---|
| `aboutus-augment-spirit-lake` | `107426b0e69afad2224aed35cec1ce20bd83ec7ea820f9b1567e306340339168` | `c0965809eb515f6f553d00f7552ee38bea29606c8695c76ae4c400d6b27c1095` |
| `heavy-duty-vs-light-duty-trucks` | `67c551eefebd8e649a04ae9afb358ed8df2cffefd7964b7d79a1b419cc594851` | `41a3dad8af68215972230c9c16296af5d591e9442608f44cde126b68682b4013` |
| `highlander-vs-grand-highlander` | `eb410ecc86edf4f41d0f973ba4296fcc2aea98a5186ee0d68ede528a50efed9c` | `92fe6b8f9c42e63f914ccbf9b5f33019abcfeda0bf18402bb27a47a0be3be307` |
| `toyota-rav4-carroll-iowa` | `741472daa2aa1b7a5d0c6d9cfccecc0bfdd37e0fc201fe7b3ea2fb289155f909` | `7b2b7a8b32ec5786da79917443c16542899b0f234880abb1987a53c6fcb4f91a` |
| `trim-levels-explained` | `2ff205e596e32cf2ce18346e467ec7d9df241a49c26eab6da28ca6668262a9ed` | `36b7197f70f6c6cae8f74a72b35dd7b353139e93f1e0cfebe3cc9d3f132727d4` |
| `used-car-maintenance-mileage` | `31a423c1d672218ca16ed832efc4ed19708388534f7b0631b786ba6c3d05939c` | `0b48175cc13c5e72f84498b39f496e345b772eda78a9bbd346011fb597a5cdaa` |

### Reproduction of the static extraction

The following exact read-only program was executed with each of the six slugs; it was then executed again with `aboutus-augment-spirit-lake` and `used-car-maintenance-mileage`. Run from the repository root and substitute the page slug for `PAGE_SLUG`. It outputs input hashes, metadata, parsed FAQ pairs, visible line text, internal hrefs, and the complete matching packet. The substantive claim and voice verdicts require the manual review documented above.

```sh
python3 - 'PAGE_SLUG' <<'PY'
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import hashlib,json,re,subprocess,sys
root=Path.cwd(); slug=sys.argv[1]
p=root/'deliveries/site-packages/2026-11-15/motorinnautogroup'/slug/'index.html'
packet=root/'content/drafts/seo'/f'{slug}-REVIEW.md'; meta=p.parent/'metadata.json'
html=p.read_text(); soup=BeautifulSoup(html,'html.parser'); mains=soup.select('#content-main'); main=mains[0]
title=soup.title.get_text(); desc=soup.select_one('meta[name="description"]')['content']
faq=[]; json_errors=[]
def walk(x):
 if isinstance(x,dict):
  if x.get('@type')=='FAQPage': faq.append(x)
  for v in x.values(): walk(v)
 elif isinstance(x,list):
  for v in x: walk(v)
for s in soup.select('script[type="application/ld+json"]'):
 try: walk(json.loads(s.string or s.get_text()))
 except Exception as e: json_errors.append(str(e))
headings=main.find_all(['h1','h2','h3','h4'])
norm=lambda t: re.sub(r'\s+',' ',t).strip().casefold()
faq_pairs=[]
for block in faq:
 for q in block.get('mainEntity',[]):
  matches=[h for h in headings if norm(h.get_text(' ',strip=True))==norm(q['name'])]
  h=matches[0] if matches else None; ans=[]
  if h:
   for el in h.next_siblings:
    if getattr(el,'name',None) in ['h1','h2','h3','h4']: break
    if getattr(el,'name',None): ans.append(el.get_text(' ',strip=True))
  faq_pairs.append({'question':q['name'],'question_match':bool(matches),'visible_line':h.sourceline if h else None,'schema_answer':q['acceptedAnswer']['text'],'visible_answer':' '.join(ans)})
links=[{'line':a.sourceline,'href':a['href']} for a in main.find_all('a',href=True) if (urlparse(a['href']).hostname or '').lower() in ['motorinnautogroup.com','www.motorinnautogroup.com']]
for el in main.select('script,style,template,noscript'): el.decompose()
result={'slug':slug,'sha256':{str(f.relative_to(root)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [p,packet,meta]},'main_count':len(mains),'title':{'line':soup.title.sourceline,'text':title,'length':len(title)},'description':{'line':soup.select_one('meta[name="description"]').sourceline,'text':desc,'length':len(desc)},'metadata_matches':json.loads(meta.read_text())['title']==title and json.loads(meta.read_text())['meta']==desc,'json_errors':json_errors,'faq_blocks':len(faq),'faq_counts':[len(x.get('mainEntity',[])) for x in faq],'faq_pairs':faq_pairs,'visible_lines':[f'{x.sourceline}: {x.get_text(" ",strip=True)}' for x in main.find_all(['h1','h2','h3','p','li','tr','figcaption']) if not x.find_parent(['script','style','template','noscript'])],'internal_hrefs':links,'review_packet':[f'{i}: {line}' for i,line in enumerate(packet.read_text().splitlines(),1)]}
print(json.dumps(result,ensure_ascii=False))
PY
```

The separate workflow/banned-word scan found no Voice DNA banned phrases, zero exclamation marks, and question-form H2s on every page. Its material workflow hits were the About Us paragraphs at 888, 896, 908, and 912 and the maintenance paragraph at 897. Every authored section was also read manually; phrase matching alone did not determine PASS.

## Discoveries and proposed permanent check

No product test was created in this report-only run.

| Discovery | Proposed case | Evidence | Disposition |
|---|---|---|---|
| Preserving a verification marker can still preserve visible approval, testing, or source-publication instructions; removing one banned phrase does not clear the whole section. | Extend the existing visible-text audit's phrase cases and manually review each visible marker and FAQ answer. | Findings -001 and -002; identical extraction replays | Proposed only |
| A voice rewrite can introduce new factual contact or inventory assertions without updating the corresponding source map. | Re-run the full claim-map review after wording changes, including new phone numbers, categorical negatives, and universal inventory-coverage terms. | Findings -003 and -004; HEAD diff and packet reads | Proposed only |

No new automated test is proposed beyond extending the existing audit and manual review; no test files were written.

## Coverage limits, cleanup, and learning

- All 30 requested page/check combinations were assessed. No requested contract remains unrun.
- External source truth was not independently re-researched; relevance/mapping was checked against the complete supplied packets. The phone finding does not say the number is wrong, and the inventory finding does not say those assertions are false.
- Internal-link scope is exactly the authored `#content-main` scope used in rerun 2. Inherited DealerOn navigation/footer links outside that block were not tested.
- Visibility was assessed from static authored markup. HTML comments and JSON-LD text were excluded from shopper voice; ordinary visible paragraphs, source footers, and verification markers were included. No browser-rendered visual or JavaScript behavior claim is made.
- Metadata limits apply to delivered HTML values. Packet metadata headings were read as packet context; agreement with older packet title wording was not an added sixth contract.
- The pre-existing untracked `WAVE2-DIRECTIVE.md` and two prior untracked rerun reports were not edited.
- Only this requested report was written. No packages, packets, drafts, tests, configurations, dependencies, Git history, external sites, or approval states were changed.
- Opened: short-lived shell, Python, Git, and curl commands. Closed: all commands completed; no persistent job was started. No browser tab, GUI app, server, tunnel, watcher, or service was opened, so none required closing.
- Durable learning retained here only: verification markers do not waive shopper voice, and every rewrite needs a fresh source-map comparison for new factual assertions.

## Final verdict

**FAIL.** Four of the six packages pass all five checks. Both `aboutus-augment-spirit-lake` and `used-car-maintenance-mileage` fail shopper voice and claim traceability. All six pass FAQ parity, all 26 authored internal href occurrences return final 200, and all six title/description pairs meet the required lengths. The required all-six/all-five PASS condition is not met.
