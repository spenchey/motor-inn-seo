# Wave 2 adversarial QA rerun 4

- Date: 2026-11-15
- Revision under test: `949f19b423be118839b4f88536886c3b1a428427`
- Mode: Full, report-only functional QA
- Scope: Six HTML delivery packages under `deliveries/site-packages/2026-11-15/motorinnautogroup/` and their matching `content/drafts/seo/*-REVIEW.md` packets
- Status: FAIL

**Overall verdict: FAIL.** Four packages pass all five checks. About Us passes shopper voice but retains claim-mapping gaps; maintenance retains visible source-verification/publication status. FAQ parity, internal links and metadata pass on all six packages. No package or review packet was changed.

The output filename follows the user's explicit rerun4 destination. The five checks and report structure follow rerun2. Current on-disk files, including any uncommitted changes, are the inputs. No prior PASS result is proof for this run.

## Charters

### 1. Claim traceability

- Contract/source: Every factual shopper-facing claim maps to the matching review packet's source map or is visibly `[NEEDS-VERIFY]`, per the user rubric.
- Risk: An unsupported statement could reach shoppers as fact.
- Entrypoint/inputs: Authored HTML, metadata, FAQ JSON-LD, and all six matching review packets.
- Isolation/probe: Read-only, line-numbered extraction and full packet reads using Python/BeautifulSoup; manual claim-to-source comparison. No source edits or fresh external-source research.
- Exit condition: Every claim accounted for, or an exact file:line finding.

### 2. FAQ parity

- Contract/source: FAQPage JSON-LD parses, contains exactly three questions per page, matches visible question wording, and matches answers in substance, per the user rubric.
- Risk: Search markup could contradict the visible answer.
- Entrypoint/inputs: Each HTML's JSON-LD and visible headings/answers.
- Isolation/probe: Local `json.loads`, entity counts, normalized heading comparison, and manual answer comparison.
- Exit condition: Six parseable blocks and all 18 question/answer pairs pass, or exact evidence of failure.

### 3. Shopper voice

- Contract/source: `brain/VOICE-DNA.md` and the user's zero-visible-workflow-language rule in `#content-main`.
- Risk: Editorial, approval, permission, page-lifecycle, or publication instructions could reach shoppers.
- Entrypoint/inputs: All visible authored text, including verification markers, FAQ answers, and footers.
- Isolation/probe: Static visible-text extraction, workflow/banned-phrase scans, and full manual reading. Explicit scrutiny of “not listed yet,” “will appear,” “yet to be,” permission, summarizing, and publication language. Comments/scripts/styles are not visible copy.
- Exit condition: Zero visible workflow leaks and no material voice violation, or exact file:line findings. A verification marker does not exempt workflow language.

### 4. Internal links

- Contract/source: Every `motorinnautogroup.com` HTTP(S) href in authored `#content-main` returns final HTTP 200 with `curl -L`, using rerun2's authored-content scope.
- Risk: A shopper could reach a broken destination.
- Entrypoint/inputs: Every extracted authored internal href occurrence, including repeated URLs.
- Isolation/probe: Separate read-only public GET requests per occurrence; `curl -L --fail-with-body --connect-timeout 10 --max-time 20`, final status/URL/redirect/exit-code receipts. No submissions or remote writes.
- Exit condition: Every occurrence returns final 200, or the containing page fails.

### 5. Metadata length

- Contract/source: Title 50-60 characters and description 120-158, inclusive, per the user rubric.
- Risk: Search snippets could truncate or underuse the allowed space.
- Entrypoint/inputs: Each HTML's title/description and delivery `metadata.json`.
- Isolation/probe: Local Unicode character counts and HTML/metadata consistency comparison.
- Exit condition: Both lengths pass for all six pages, or an exact file:line finding.

Only this report may be written in the repository. Evidence will be retained in this report and terminal receipts; no evidence sidecars, configuration/bookkeeping helpers, dependencies, product tests, or browser setup will be created.

## Per-page verdict

| Page | 1. Claims sourced or flagged | 2. FAQPage | 3. Shopper voice | 4. Internal hrefs | 5. Title / meta | Overall |
|---|---|---|---|---|---|---|
| `aboutus-augment-spirit-lake` | **FAIL** — contact number and categorical inventory-scope answer lack matching claim/source entries | **PASS** — parses; exactly 3; 3/3 question and substantive answer matches | **PASS** — prior approval/filter-testing/page-lifecycle instructions removed | **PASS** — 6/6 final 200 | **PASS** — 52 / 151 | **FAIL** |
| `heavy-duty-vs-light-duty-trucks` | **PASS** — Ford/Chevrolet map ratings, percentages, classes and configuration cautions | **PASS** — parses; exactly 3; 3/3 question and substantive answer matches | **PASS** — no material voice violation found | **PASS** — 4/4 final 200 | **PASS** — 52 / 136 | **PASS** |
| `highlander-vs-grand-highlander` | **PASS** — Toyota maps dimensions, seating, cargo and six computed deltas | **PASS** — parses; exactly 3; 3/3 question and substantive answer matches | **PASS** — prior production-footer defect remains fixed | **PASS** — 4/4 final 200 | **PASS** — 54 / 139 | **PASS** |
| `toyota-rav4-carroll-iowa` | **PASS** — Toyota maps model facts, upholstery and dated sales framing | **PASS** — parses; exactly 3; 3/3 question and substantive answer matches | **PASS** — no material voice violation found | **PASS** — 4/4 final 200 | **PASS** — 50 / 131 | **PASS** |
| `trim-levels-explained` | **PASS** — Toyota/KBB/FTC/Ford map definitions, upholstery and capability cautions | **PASS** — parses; exactly 3; 3/3 question and substantive answer matches | **PASS** — no material voice violation found | **PASS** — 4/4 final 200 | **PASS** — 55 / 139 | **PASS** |
| `used-car-maintenance-mileage` | **PASS** — Toyota/FTC/AAA map advice; the phone now has an explicit mapping | **PASS** — parses; exactly 3; 3/3 question and substantive answer matches | **FAIL** — visible source-verification/publication status at line 897 | **PASS** — 4/4 final 200 | **PASS** — 52 / 151 | **FAIL** |

Result: **4 PASS, 2 FAIL.** Across the 30 page/check combinations: **28 PASS, 2 FAIL**. One failed check fails the page and the package set.

## Contract outcomes

| Contract and source | Exact probe / evidence | Expected → observed | Outcome |
|---|---|---|---|
| Claim support, user rubric and six matching packets | Full packet reads, authored-block extraction, source-map comparisons and identical replay; W2-RERUN4-001 | Every factual claim mapped or visibly flagged → About Us retains mapping gaps; 5/6 pages pass | **FAIL** |
| FAQ parsing and visible parity, user rubric | Python JSON parsing, recursive FAQPage discovery, entity counts, normalized headings and manual answer review; 18-pair table below | Six parseable blocks, exactly 3 entities each; 18/18 matching visible question wordings and substantive answers → observed | **PASS** |
| Shopper voice, user rubric and `brain/VOICE-DNA.md:7-21,27-33` | Full visible-text reads, candidate phrase scan, manual review and unchanged replay; W2-RERUN4-002 | Zero visible workflow language → maintenance line 897 retains source-verification/publication status; 5/6 pages pass | **FAIL** |
| Internal links, rerun2 authored-content scope | 26 separate curl GETs; exact command and occurrence ledger below | Every occurrence final-200 → 26/26 HTTP 200, exit 0, empty stderr | **PASS** |
| Metadata length, user rubric | Unicode character counts and HTML-to-metadata comparison | Title 50-60 and meta 120-158 → all 12 lengths pass; all six metadata files agree | **PASS** |

No browser or visual score applies to this functional/static QA run.

## Findings

### W2-RERUN4-001: About Us retains factual claims without matching source-map entries

- Classification / severity: Claim-traceability defect; release-blocking under check 1.
- Expected: Every factual shopper-facing assertion maps in this page's own packet source map or is visibly marked `[NEEDS-VERIFY]`.
- Observed, phone: `712-792-5000` appears five times in visible authored copy at `index.html:887,888,891,903,914`. Its matching packet never contains that number. Packet lines 35-40 map the About Us structure/target and general inventory destination, without identifying or mapping the displayed contact-number claim. This is a mapping failure; the number's correctness is not disproved.
- Observed, inventory: The visible FAQ at `index.html:912` answers “No” to “Does the general inventory page show only Spirit Lake vehicles?” The same categorical answer is in JSON-LD at `:917`. Packet lines 35-40 map the inventory destination without a claim/source entry establishing the asserted geographic scope; packet `:53` still treats a permanent Spirit Lake-only filter as unverified. The factual “No” has no scope-evidence mapping or visible flag. A working destination alone does not establish that mapping.
- Evidence: `deliveries/site-packages/2026-11-15/motorinnautogroup/aboutus-augment-spirit-lake/index.html:887,888,891,903,912,914,917`; `content/drafts/seo/aboutus-augment-spirit-lake-REVIEW.md:35-56`.
- Confirmation: The exact static extraction was rerun unchanged at 2026-11-15T19:38:20.630303+00:00. The full page extraction and all 18 input hashes were identical. The packet contains zero instances of the phone number; the visible block contains five phone mentions and zero `[NEEDS-VERIFY]` markers. Input hashes are retained below.
- Regression detail: The previous all-location-coverage assertion and visible approval/filter-testing instructions are gone. Maintenance's separate packet now maps the phone at `used-car-maintenance-mileage-REVIEW.md:38`; that does not complete the matching About Us packet.
- Next action: Add explicit claim/source mappings for the contact number and inventory scope, or remove/qualify the unsupported assertion with the rubric's visible verification treatment. Report-only; no package or packet edited.

### W2-RERUN4-002: Maintenance still exposes source-verification and publication status

- Classification / severity: Shopper-voice defect; release-blocking under check 3.
- Expected: Visible `#content-main` answers shoppers or gives the required verification marker without exposing source-review or publication workflow.
- Observed: `index.html:897` says: “MotorHappy’s published guidance for high-mileage vehicles has not been verified.” It reports the writer's source-verification state and describes publication immediately below the MotorHappy question at `:896`. It is visible body copy.
- Evidence: `deliveries/site-packages/2026-11-15/motorinnautogroup/used-car-maintenance-mileage/index.html:896-897`; `content/drafts/seo/used-car-maintenance-mileage-REVIEW.md:44,50` explicitly records the still-open source task.
- Confirmation: The unchanged static replay reproduced the exact paragraph, source line and input hashes.
- Regression detail: The previous requests to obtain permission, locate an original publication or wait “Until a named original source is available” are gone. The remaining sentence still reports editorial source-review status. Shopper advice about confirming vehicle records at `:908-909` now passes voice.
- Next action: Keep source-verification status and research tasks in the packet; use direct shopper maintenance guidance in the visible answer. Report-only; no edit made.

## Claim-support specifics

HTML references below are under `deliveries/site-packages/2026-11-15/motorinnautogroup/<slug>/index.html`; packet references are `content/drafts/seo/<slug>-REVIEW.md`.

| Page | Claim families and HTML evidence | Matching packet source map | Result |
|---|---|---|---|
| `aboutus-augment-spirit-lake` | General inventory guidance at 883-884 maps; requests to confirm entity/location/service/transfer/inspection details at 887-908 do not invent those details. Five contact-number mentions and the inventory-scope answer retain the gaps in W2-RERUN4-001. | 35-40; unresolved Spirit Lake facts at 48-56 | **FAIL** |
| `heavy-duty-vs-light-duty-trucks` | 13,500/2,440/40,000/8,000 maxima at 890; 150/1500 versus HD naming at 893-894; 10%/15% hitch loads at 898; weight-rating definitions at 901-902; configuration/label guidance at 913-914. | 31-36: Ford F-150, Super Duty, tow guide, Chevrolet naming and qualified daily-use advice | **PASS** |
| `highlander-vs-grand-highlander` | Both 2026 models' length, wheelbase, third-row legroom and cargo at 887-892; six deltas recompute as 6.5, 3.9, 5.5, 4.6, 9.5 and 13.2; seating at 912; source footer at 923. | 34-36: Toyota dimensions and explicit delta map | **PASS** |
| `toyota-rav4-carroll-iowa` | Dated 2025 best-ever annual-sales framing at 882/913; electrified lineup and 226/236 hp at 886/894; 8.1-inch clearance and 1,750/3,500-lb configuration-specific tow ratings at 894; upholstery at 898-899/912. No guaranteed resale/scarcity assertion. | 29-32: Toyota overview, press release, brochure/interior specs and dated sales results | **PASS** |
| `trim-levels-explained` | Equipment/model/trim/package definitions at 882-888; configuration-dependent truck ratings at 891-892; Toyota material terminology at 895-896/917; equipment/model-year verification at 903-912. | 31-35: Toyota, Kelley Blue Book, FTC and Ford | **PASS** |
| `used-car-maintenance-mileage` | No fixed lifespan at 882-886/921; review-mileage headings at 892-894 are not service intervals; factory-schedule, inspection/history, warning-sign and corrosion advice at 889-905; phone at 908. No MotorHappy recommendations or universal Motor Inn inspection steps are asserted as verified facts. The source-status sentence is the separate voice failure. | 29-38: Toyota, FTC, AAA and explicit phone mapping; open MotorHappy/process questions at 50-53 | **PASS** |

All six authored blocks now contain **zero** literal visible `[NEEDS-VERIFY]` markers. About Us's nine and maintenance's four open items remain packet-side. Moving an unknown to a packet is acceptable only when the visible text stops asserting that unknown as fact; it does not satisfy the visible-flag alternative for an unsupported claim that remains.

The requested contract is claim-to-source mapping against supplied packets, not a new independent audit of every external source's factual truth.

## Shopper-voice specifics

- About Us `index.html:882-915`: no remaining visible editor, production, approval, permission, page-lifecycle or publication instruction. “not listed yet,” “will appear,” “yet to be,” “approved wording,” “provide and test,” and “No location-specific claim is made here” are absent from visible copy. **PASS.**
- Maintenance: the former permission/summarization and future-publication instructions are absent; source-status wording at `:897` remains. **FAIL.**
- Highlander `index.html:909` qualifies the recommendation by saying one model is not better for every family. That is shopper advice, not an editorial instruction. Its footer at `:923` is a source credit. **PASS.**
- Maintenance `index.html:905` says to inspect corrosion before “approving a major repair.” That refers to the shopper's repair decision; it is not the voice defect.
- Trucks, RAV4 and trim levels: all visible paragraphs, lists, tables, FAQs and footers reviewed. No banned marketing phrase, exclamation stack or material production-language leak found. All H2s are shopper questions.
- About Us `index.html:880` contains an HTML augmentation/approval comment. It is not visibly rendered and is excluded from the visible-copy contract. JSON-LD and packet-only workflow notes are likewise not visible shopper text.

## FAQPage specifics

All six JSON-LD blocks parse and each contains exactly three Question entities with answers. All 18 question wordings match a visible heading after case/whitespace normalization; all 18 answers match the visible content in substance.

As in rerun2, the matching heading can be an H1, H2 or FAQ H3. Visible body/table content supports schema summaries that expand a short FAQ reply. FAQ parity does not establish source support: About Us's inventory answer is identical in both surfaces and still fails mapping.

| Page | Schema question | Visible heading line | JSON-LD line | Substantive answer comparison |
|---|---|---:|---:|---|
| `aboutus-augment-spirit-lake` | Should you confirm a used vehicle's location before visiting? | 911 | 917 | PASS — Same availability/location advice; apostrophe typography only. |
| `aboutus-augment-spirit-lake` | Does the general inventory page show only Spirit Lake vehicles? | 912 | 917 | PASS — Identical answer; source-map failure is separate. |
| `aboutus-augment-spirit-lake` | Are transfers between locations guaranteed? | 913 | 917 | PASS — Identical conditional transfer caution. |
| `heavy-duty-vs-light-duty-trucks` | How does a light-duty full-size truck compare to a heavy-duty model for everyday use? | 884 | 924 | PASS — Same daily-use/capacity comparison; configuration qualifications at 886 and capacity comparison at 889-890. |
| `heavy-duty-vs-light-duty-trucks` | Why can payload run out before towing capacity? | 896 | 924 | PASS — Same passengers/cargo/accessories/hitch/tongue/pin payload explanation. |
| `heavy-duty-vs-light-duty-trucks` | Does a 2500 badge tell you the towing capacity? | 919 | 924 | PASS — Same configuration-dependent rating; factors visible at 914. |
| `highlander-vs-grand-highlander` | Is the Grand Highlander bigger than the Highlander? | 881 | 926 | PASS — Same 6.5-inch length and 3.9-inch wheelbase differences. |
| `highlander-vs-grand-highlander` | How much third-row legroom does the Grand Highlander add? | 921 | 926 | PASS — Same 33.5-inch legroom and 5.5-inch gain. |
| `highlander-vs-grand-highlander` | Does the Grand Highlander have more cargo room? | 922 | 926 | PASS — Same cargo advantage; schema's 20.6/97.5 values visible in table at 890/892. |
| `toyota-rav4-carroll-iowa` | What factors explain the Toyota RAV4's market dominance? | 884 | 916 | PASS — Same grades/drivetrains/cabin-space explanation. |
| `toyota-rav4-carroll-iowa` | Does every 2026 RAV4 have all-wheel drive? | 910 | 916 | PASS — Same eligible hybrid FWD/AWD and plug-in AWD distinction. |
| `toyota-rav4-carroll-iowa` | Does every RAV4 use SofTex seats? | 912 | 916 | PASS — Same fabric/SofTex/synthetic-suede distinction. |
| `trim-levels-explained` | What do car trim levels mean? | 883 | 922 | PASS — Same equipment-version definition; explicit definition also at 882. |
| `trim-levels-explained` | What does trim level mean on a truck? | 890 | 922 | PASS — Same equipment-version versus towing-rating distinction and configuration caveat. |
| `trim-levels-explained` | Is SofTex leather? | 917 | 922 | PASS — Same Toyota SofTex terminology. |
| `used-car-maintenance-mileage` | How many miles can a car last before it breaks down? | 881 | 926 | PASS — Same no-fixed-mileage answer and condition/history factors. |
| `used-car-maintenance-mileage` | Can maintenance guarantee a car will reach a certain mileage? | 921 | 926 | PASS — Identical no-lifespan-guarantee answer. |
| `used-car-maintenance-mileage` | Should you buy a used car without service records? | 922 | 926 | PASS — Same missing-records uncertainty and pricing/inspection advice. |

## Internal-link results

All **26/26 authored internal href occurrences** returned final HTTP 200, curl exit 0 and empty stderr. Every occurrence was fetched separately, including duplicates. Eight distinct destinations were tested. The requests ran 2026-11-15T19:37:27.062193+00:00 through 2026-11-15T19:37:28.941612+00:00, using up to four independent curl subprocesses at once.

Exact argument pattern, substituting each extracted URL without shell interpolation:

```bash
curl --silent --show-error --location --fail-with-body --connect-timeout 10 --max-time 20 --output /dev/null --write-out '%{json}' URL
```

Each Python subprocess had a 25-second timeout; curl's URL limit was 20 seconds. Status, effective URL, redirect count, exit code, stderr and per-request duration were observed in terminal receipts. Results are retained here.

| URL | Occurrences tested | Final status | Final URL / redirects per request |
|---|---:|---:|---|
| `https://www.motorinnautogroup.com/searchused.aspx` | 3 | 200 | `https://www.motorinnautogroup.com/used-inventory`; 1 redirect(s) |
| `https://www.motorinnautogroup.com/aboutus.aspx` | 1 | 200 | `https://www.motorinnautogroup.com/aboutus.aspx`; 0 redirect(s) |
| `https://www.motorinnautogroup.com/car-maintenance-by-mileage` | 4 | 200 | `https://www.motorinnautogroup.com/car-maintenance-by-mileage`; 0 redirect(s) |
| `https://www.motorinnautogroup.com/2022-toyota-rav4-carroll-ia` | 5 | 200 | `https://www.motorinnautogroup.com/2022-toyota-rav4-carroll-ia`; 0 redirect(s) |
| `https://www.motorinnautogroup.com/vehicle-trim-levels-explained` | 5 | 200 | `https://www.motorinnautogroup.com/vehicle-trim-levels-explained`; 0 redirect(s) |
| `https://www.motorinnautogroup.com/searchall.aspx` | 4 | 200 | `https://www.motorinnautogroup.com/searchall.aspx`; 0 redirect(s) |
| `https://www.motorinnautogroup.com/highlander-vs-grand-highlander` | 2 | 200 | `https://www.motorinnautogroup.com/highlander-vs-grand-highlander`; 0 redirect(s) |
| `https://www.motorinnautogroup.com/blog/heavy-duty-vs-light-duty-trucks` | 2 | 200 | `https://www.motorinnautogroup.com/blog/heavy-duty-vs-light-duty-trucks`; 0 redirect(s) |

Occurrence paths are relative to `deliveries/site-packages/2026-11-15/motorinnautogroup/`. Zero-redirect rows retain the requested effective URL. Every `/searchused.aspx` occurrence resolved to `https://www.motorinnautogroup.com/used-inventory`.

| Request | Page:line | Requested path on www.motorinnautogroup.com | Final HTTP | Redirects | Curl exit |
|---|---|---|---:|---:|---:|
| 001 | `aboutus-augment-spirit-lake/index.html:884` | `/searchused.aspx` | 200 | 1 | 0 |
| 002 | `aboutus-augment-spirit-lake/index.html:914` | `/aboutus.aspx` | 200 | 0 | 0 |
| 003 | `aboutus-augment-spirit-lake/index.html:914` | `/searchused.aspx` | 200 | 1 | 0 |
| 004 | `aboutus-augment-spirit-lake/index.html:915` | `/car-maintenance-by-mileage` | 200 | 0 | 0 |
| 005 | `aboutus-augment-spirit-lake/index.html:915` | `/2022-toyota-rav4-carroll-ia` | 200 | 0 | 0 |
| 006 | `aboutus-augment-spirit-lake/index.html:915` | `/vehicle-trim-levels-explained` | 200 | 0 | 0 |
| 007 | `heavy-duty-vs-light-duty-trucks/index.html:915` | `/searchall.aspx` | 200 | 0 | 0 |
| 008 | `heavy-duty-vs-light-duty-trucks/index.html:922` | `/vehicle-trim-levels-explained` | 200 | 0 | 0 |
| 009 | `heavy-duty-vs-light-duty-trucks/index.html:922` | `/car-maintenance-by-mileage` | 200 | 0 | 0 |
| 010 | `heavy-duty-vs-light-duty-trucks/index.html:922` | `/2022-toyota-rav4-carroll-ia` | 200 | 0 | 0 |
| 011 | `highlander-vs-grand-highlander/index.html:917` | `/searchall.aspx` | 200 | 0 | 0 |
| 012 | `highlander-vs-grand-highlander/index.html:924` | `/2022-toyota-rav4-carroll-ia` | 200 | 0 | 0 |
| 013 | `highlander-vs-grand-highlander/index.html:924` | `/vehicle-trim-levels-explained` | 200 | 0 | 0 |
| 014 | `highlander-vs-grand-highlander/index.html:924` | `/car-maintenance-by-mileage` | 200 | 0 | 0 |
| 015 | `toyota-rav4-carroll-iowa/index.html:907` | `/searchall.aspx` | 200 | 0 | 0 |
| 016 | `toyota-rav4-carroll-iowa/index.html:914` | `/highlander-vs-grand-highlander` | 200 | 0 | 0 |
| 017 | `toyota-rav4-carroll-iowa/index.html:914` | `/vehicle-trim-levels-explained` | 200 | 0 | 0 |
| 018 | `toyota-rav4-carroll-iowa/index.html:914` | `/car-maintenance-by-mileage` | 200 | 0 | 0 |
| 019 | `trim-levels-explained/index.html:908` | `/searchall.aspx` | 200 | 0 | 0 |
| 020 | `trim-levels-explained/index.html:920` | `/2022-toyota-rav4-carroll-ia` | 200 | 0 | 0 |
| 021 | `trim-levels-explained/index.html:920` | `/highlander-vs-grand-highlander` | 200 | 0 | 0 |
| 022 | `trim-levels-explained/index.html:920` | `/blog/heavy-duty-vs-light-duty-trucks` | 200 | 0 | 0 |
| 023 | `used-car-maintenance-mileage/index.html:917` | `/searchused.aspx` | 200 | 1 | 0 |
| 024 | `used-car-maintenance-mileage/index.html:924` | `/vehicle-trim-levels-explained` | 200 | 0 | 0 |
| 025 | `used-car-maintenance-mileage/index.html:924` | `/2022-toyota-rav4-carroll-ia` | 200 | 0 | 0 |
| 026 | `used-car-maintenance-mileage/index.html:924` | `/blog/heavy-duty-vs-light-duty-trucks` | 200 | 0 | 0 |

## Metadata specifics

Counts are Unicode characters in actual parsed HTML with inclusive limits. All titles/descriptions equal their corresponding delivery `metadata.json` values.

| Page | Title length | Meta length | Result / evidence |
|---|---:|---:|---|
| `aboutus-augment-spirit-lake` | 52 | 151 | PASS; HTML lines 6/14; `metadata.json` agrees |
| `heavy-duty-vs-light-duty-trucks` | 52 | 136 | PASS; HTML lines 6/14; `metadata.json` agrees |
| `highlander-vs-grand-highlander` | 54 | 139 | PASS; HTML lines 6/14; `metadata.json` agrees |
| `toyota-rav4-carroll-iowa` | 50 | 131 | PASS; HTML lines 6/14; `metadata.json` agrees |
| `trim-levels-explained` | 55 | 139 | PASS; HTML lines 6/14; `metadata.json` agrees |
| `used-car-maintenance-mileage` | 52 | 151 | PASS; HTML lines 6/14; `metadata.json` agrees |

## Evidence and timing

- Execution repository: local terminal, `/Users/spencerheywood/motor-inn-seo`.
- Tested branch/revision: `main`, `949f19b423be118839b4f88536886c3b1a428427`, commit “wave2 fix round4: flag brackets off-page to shopper guidance; phone + packet source mappings per codex rerun3.”
- Input state: all six HTML files, six packets and six metadata files matched HEAD byte-for-byte at first extraction and unchanged replay. No uncommitted package/packet fix was pending in these inputs.
- Native runtime/tools: Python 3.13.6, BeautifulSoup, Python JSON parser; curl 8.7.1 (x86_64-apple-darwin25.0) libcurl/8.7.1 (SecureTransport) LibreSSL/3.3.6 zlib/1.2.12 nghttp2/1.68.1.
- Initial static observation: 2026-11-15T19:36:32.483390+00:00. Identical replay: 2026-11-15T19:38:20.630303+00:00. Both processes exited 0; the full `pages` extraction and all 18 hashes matched.
- Probe budget: full static/functional mode without a total cap; 20-second curl and 25-second subprocess limits.
- Guarded command time: unmeasured; no gstack evidence/deadline wrapper was used because the one-report write boundary takes precedence over its extra artifacts/bookkeeping. Curl batch wall time was independently measured as 1.88 seconds.
- Total session elapsed: unmeasured; final report write, acknowledgement and cleanup/verification were not complete when this field was assembled.
- Stop reason: all five requested checks completed for all six packages; failures confirmed by unchanged replay.
- Evidence destination: this report and terminal receipts. No sidecars, downloaded pages or temporary scripts were written.

### Input SHA-256 manifest

HTML paths: `deliveries/site-packages/2026-11-15/motorinnautogroup/<slug>/index.html`. Packet paths: `content/drafts/seo/<slug>-REVIEW.md`.

| Page | HTML SHA-256 | Packet SHA-256 |
|---|---|---|
| `aboutus-augment-spirit-lake` | `9af121fb4f1b728e4f9d90168e37b0b747485eaef9226037097009764a10b2b8` | `053a634e8b508a374704b2cb462154fafae0308c913814e282abb6a9736a8fb6` |
| `heavy-duty-vs-light-duty-trucks` | `67c551eefebd8e649a04ae9afb358ed8df2cffefd7964b7d79a1b419cc594851` | `41a3dad8af68215972230c9c16296af5d591e9442608f44cde126b68682b4013` |
| `highlander-vs-grand-highlander` | `eb410ecc86edf4f41d0f973ba4296fcc2aea98a5186ee0d68ede528a50efed9c` | `92fe6b8f9c42e63f914ccbf9b5f33019abcfeda0bf18402bb27a47a0be3be307` |
| `toyota-rav4-carroll-iowa` | `741472daa2aa1b7a5d0c6d9cfccecc0bfdd37e0fc201fe7b3ea2fb289155f909` | `7b2b7a8b32ec5786da79917443c16542899b0f234880abb1987a53c6fcb4f91a` |
| `trim-levels-explained` | `2ff205e596e32cf2ce18346e467ec7d9df241a49c26eab6da28ca6668262a9ed` | `36b7197f70f6c6cae8f74a72b35dd7b353139e93f1e0cfebe3cc9d3f132727d4` |
| `used-car-maintenance-mileage` | `4c9c129bb8457c3990254b855e9bee869c7b6d0cf08cd1bc0d6b4423ebb9a4c7` | `aac4d4cc8f74c80c127e593c70cf9d8da4e9a4acf4835fa37ef5498bcc10b1f1` |

| Metadata file under package root | SHA-256 |
|---|---|
| `aboutus-augment-spirit-lake/metadata.json` | `9fea15aa4ed9cb3cd37b40a520defa14b3408b1c1c3e2531dfa04249722ace23` |
| `heavy-duty-vs-light-duty-trucks/metadata.json` | `63639acf8866852cdb910e8832bfb2c7ea5618357add8b4a4480b3010405f7a2` |
| `highlander-vs-grand-highlander/metadata.json` | `465f757487cabc8592fb9e581f71b8e11a029640b6a7b98e217e6b8d7e605cb9` |
| `toyota-rav4-carroll-iowa/metadata.json` | `74e5ac48c9d8c9d9b3124b7132b6c18d1e5531aa5f5107bb463eb47777d3f453` |
| `trim-levels-explained/metadata.json` | `e9cd07a725802ac54aa0c768184c87c7f436b49573b0bc757fd22c0ae2928ca5` |
| `used-car-maintenance-mileage/metadata.json` | `10daaa1e45edd58f9366474263fecb63902db52167d8e681235385101aba09a2` |

### Static extraction program actually executed

The following read-only command was run twice from the repository root. Its `pages` result, including hashes, authored blocks, parsed FAQ objects, packet lines, metadata and scan candidates, was identical on replay. The scan identifies candidates; verdicts also use manual semantic review.

```bash
python3 - <<'PY'
from pathlib import Path
from bs4 import BeautifulSoup, Comment
import hashlib,json,re,subprocess,datetime,platform
root=Path.cwd(); base=root/'deliveries/site-packages/2026-11-15/motorinnautogroup'
def sha(b): return hashlib.sha256(b).hexdigest()
def norm(s): return ' '.join(s.split()).casefold()
def walk(x):
 if isinstance(x,dict):
  if x.get('@type')=='FAQPage' or isinstance(x.get('@type'),list) and 'FAQPage' in x['@type']: yield x
  for v in x.values(): yield from walk(v)
 elif isinstance(x,list):
  for v in x: yield from walk(v)
result={'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':platform.python_version(),'head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'branch':subprocess.check_output(['git','branch','--show-current'],text=True).strip(),'status':subprocess.check_output(['git','status','--short'],text=True),'pages':[]}
for folder in sorted(base.iterdir()):
 if not folder.is_dir(): continue
 slug=folder.name; hp=folder/'index.html'; pp=root/'content/drafts/seo'/f'{slug}-REVIEW.md'; mp=folder/'metadata.json'
 raw=hp.read_bytes(); soup=BeautifulSoup(raw,'html.parser'); content=soup.select_one('#content-main'); assert content
 files={}
 for p in [hp,pp,mp]:
  b=p.read_bytes(); rel=str(p.relative_to(root)); hb=subprocess.check_output(['git','show','HEAD:'+rel]); files[rel]={'sha256':sha(b),'matches_HEAD':b==hb}
 title=soup.title.get_text(); md=soup.find('meta',attrs={'name':re.compile('^description$',re.I)})
 schemas=[]; errors=[]
 for s in soup.find_all('script',type='application/ld+json'):
  try:
   data=json.loads(s.string or s.get_text()); schemas.extend({'line':s.sourceline,'data':d} for d in walk(data))
  except Exception as e: errors.append({'line':s.sourceline,'error':str(e)})
 links=[{'line':a.sourceline,'href':a['href'],'text':a.get_text(' ',strip=True)} for a in content.find_all('a',href=True) if re.match(r'^https?://(?:www\.)?motorinnautogroup\.com(?:[/:?#]|$)',a['href'],re.I)]
 for tag in list(content.find_all(['script','style','template','noscript'])): tag.decompose()
 for c in content.find_all(string=lambda t:isinstance(t,Comment)): c.extract()
 for tag in list(content.find_all(attrs={'hidden':True})): tag.decompose()
 blocks=[{'line':t.sourceline,'tag':t.name,'text':t.get_text(' ',strip=True)} for t in content.find_all(['h1','h2','h3','h4','p','li','caption','th','td'])]
 full=content.get_text(' ',strip=True)
 headings=[{'line':t.sourceline,'text':t.get_text(' ',strip=True)} for t in content.find_all(['h1','h2','h3','h4'])]
 faq=[]
 for schema in schemas:
  for entity in schema['data'].get('mainEntity',[]):
   q=entity.get('name',''); matches=[h for h in headings if norm(h['text'])==norm(q)]; faq.append({'question':q,'schema_answer':entity.get('acceptedAnswer',{}).get('text'),'matches':matches})
 pattern=r'editor|production|approv|permission|publish|publication|summari[sz]|not listed yet|will appear|yet to be|not stated|on this page|listed above|available source|source is available|once.{0,60}confirm|before.{0,50}confirm|provide and test|no.{0,30}claim|draft|handoff|schema|unleash|elevate|seamless|journey|discover the difference|unparalleled|state.of.the.art|competitive|commitment to excellence'
 result['pages'].append({'slug':slug,'files':files,'title':{'text':title,'length':len(title),'line':soup.title.sourceline},'description':{'text':md['content'],'length':len(md['content']),'line':md.sourceline},'metadata':json.loads(mp.read_text()),'json_errors':errors,'faq_schemas':schemas,'faq':faq,'links':links,'visible_blocks':blocks,'visible_text':full,'voice_scan_hits':[b for b in blocks if re.search(pattern,b['text'],re.I)],'verification_marker_count':full.count('[NEEDS-VERIFY]'),'packet_lines':[f'{i}: {line}' for i,line in enumerate(pp.read_text().splitlines(),1)]})
print(json.dumps(result,ensure_ascii=False))
PY
```

## Discoveries and proposed permanent check

No product test or checker was created or changed.

| Discovery | Proposed case | Evidence | Disposition |
|---|---|---|---|
| Removing visible flags can leave an untraced fact, and moving some source notes off-page can leave a verification-status sentence visible. | Extend the existing preflight review to compare every phone/inventory-scope assertion with its own packet map and manually inspect source-status wording in visible content. | W2-RERUN4-001 and W2-RERUN4-002; unchanged replay. | Proposed only; no test, package or packet changed. |

Value: protects=per-page traceability and shopper voice; fails_when=displayed phone/inventory facts lack their own mapping or visible flag, or source-review status is visible; why_new=phone mapping was added only to maintenance and the remaining source-status sentence escaped the rewrite; seam=none; no_claim=phrase scanning cannot replace semantic review or prove external-source truth.

## Coverage limits, cleanup, and learning

- All five required checks completed. No required check was skipped, blocked, timed out or counted as passed without observation.
- Authored scope matches rerun2: `#content-main`, including FAQs, related guides and source footers. DealerOn template/navigation hrefs outside it were not part of this contract.
- External-source truth, deployment, live page replacement, visual rendering and search-engine eligibility were not audited. HTTP 200 establishes link status, not publication of these local packages.
- Each matching packet was reviewed separately. Packet-side verification lists do not exempt unsupported factual assertions left in visible copy.
- Prior reports supplied the charter/context; their PASS results were not reused as proof.
- The user's fixed report path and one-report boundary take precedence over skill defaults for evidence sidecars, telemetry/configuration helpers, learning stores and storage destinations. Those extra writes were not run.
- Pre-existing untracked `WAVE2-DIRECTIVE.md` and rerun/rerun2/rerun3 reports were left in place.
- Opened: short-lived Python, curl and shell commands. All completed, including the link worker pool and subprocesses. No GUI app, browser/tab, server, SSH connection, tunnel, watcher or persistent background service was opened. Nothing remains running for this job.
- Only this requested report was written. No package, packet, draft, product test, configuration, dependency, Git commit or deployment was changed.
- Learning retained here only: each page needs its own claim mapping, and shopper copy still fails when it reports the writer's source-verification state.

## Final verdict

**FAIL.** Four packages pass all five checks. About Us now passes shopper voice but fails claim traceability. Maintenance now passes the contact-number mapping check but fails shopper voice at `index.html:897`. All six packages pass FAQ parity, internal-link status and metadata length. The package set does not satisfy the required all-checks-pass rule.
