# Wave 2 adversarial QA rerun 5

- Date: 2026-11-15
- Revision under test: `d0c0e5b0f8f188dd4867a28ae3c641f1ad3f8aa5`
- Branch: `main`
- Mode: Full, report-only functional QA
- Scope: Six named HTML delivery packages and their six matching `*-REVIEW.md` packets
- Status: PASS
- Authority: Current user request; requested output filename is rerun 5.
- Methods: Python 3 / BeautifulSoup / JSON parsing; one read-only public `curl -L` GET per authored internal href occurrence, with 8-second connection and 20-second total URL limits. Static commands completed inline; no detached parser or polling process was used.
- Isolation: Read current on-disk package/packet contents; no package, packet, test, configuration, Git, browser, service, or credential changes. The sole permitted repository write is this report. Evidence will be embedded in this report; no sidecar report or repository bookkeeping is created.
- Storage preflight: Local Glyph helper exited 11: `Glyph preflight failed: missing SMB password — No keychain password for glyphshare@spark-fa5a and GLYPH_SMB_PASSWORD is unset`. No Glyph-dependent work or credential change will be performed. The fixed report destination remains available.

**Overall verdict: PASS.** All six packages pass all five checks. Current source maps cover the About Us phone and inventory-scope claims, and the maintenance answer now uses direct shopper guidance. No package or review packet was changed.

## Charters

### 1. Claim traceability

- Contract: Every factual shopper-facing claim is mapped to a source in the matching review packet or visibly marked `[NEEDS-VERIFY]`.
- Risk: Unsupported claims could be published as fact.
- Entrypoint: HTML body copy, structured data, and matching review packet source map.
- Isolation: Static reads at the exact tested revision; no content edits.
- Exit condition: Every claim is accounted for, or the page fails with exact evidence.

### 2. FAQ parity

- Contract: `FAQPage` JSON-LD parses, contains exactly three questions, and all three visibly rendered questions match its wording with substantively matching answers.
- Risk: Search markup could contradict or overstate the visible page.
- Entrypoint: Each HTML package's JSON-LD and visible FAQ section.
- Isolation: Local parser only; no browser or publication.
- Exit condition: Parse and all 3/3 question-and-answer pairs pass, or the page fails with exact evidence.

### 3. Shopper voice

- Contract: Visible copy follows `brain/VOICE-DNA.md` and contains zero editor, production, approval, schema, or handoff language.
- Risk: Internal workflow language could reach shoppers and weaken trust.
- Entrypoint: Visible text extracted from each HTML file, with focused review of all prior production-language failures.
- Isolation: Static read and text extraction; no rewriting.
- Exit condition: Zero visible production-language leaks and no material voice violation, or the page fails with exact evidence.

### 4. Internal links

- Contract: Every `motorinnautogroup.com` HTTP(S) `href` in the six HTML files returns HTTP 200 after redirects using `curl -L`.
- Risk: Shoppers could land on broken internal destinations.
- Entrypoint: All internal href occurrences extracted from the exact HTML inputs.
- Isolation: Read-only public GET/HEAD-equivalent requests; no form submissions or site changes.
- Exit condition: Every extracted occurrence is tested and returns final status 200, or the containing page fails.

### 5. Metadata length

- Contract: Title is 50-60 characters and meta description is 120-158 characters, inclusive.
- Risk: Search snippets may truncate or underuse available space.
- Entrypoint: `<title>` and `<meta name="description">` in each HTML file.
- Isolation: Local parsing only.
- Exit condition: Both lengths fall in range, or the page fails.

## Per-page verdict

| Page | 1. Claims sourced or flagged | 2. FAQPage | 3. Shopper voice | 4. Internal hrefs | 5. Title / meta | Overall |
|---|---|---|---|---|---|---|
| `aboutus-augment-spirit-lake` | **PASS** — phone and inventory-scope claims explicitly mapped; unknown Spirit Lake details are shopper confirmation requests | **PASS** — parses; exactly 3 questions; 3/3 visible wordings and substantive answers match | **PASS** — no visible production, permission, publication or page-lifecycle language | **PASS** — 6/6 final 200 | **PASS** — 52 / 151 | **PASS** |
| `heavy-duty-vs-light-duty-trucks` | **PASS** — Ford/Chevrolet map weight ratings, load percentages, class names and configuration cautions | **PASS** — parses; exactly 3 questions; 3/3 visible wordings and substantive answers match | **PASS** — no material shopper-voice violation | **PASS** — 4/4 final 200 | **PASS** — 52 / 136 | **PASS** |
| `highlander-vs-grand-highlander` | **PASS** — Toyota maps both 2026 models, dimensions, seating, cargo and all six computed deltas | **PASS** — parses; exactly 3 questions; 3/3 visible wordings and substantive answers match | **PASS** — previous approval-footer defect remains absent | **PASS** — 4/4 final 200 | **PASS** — 54 / 139 | **PASS** |
| `toyota-rav4-carroll-iowa` | **PASS** — Toyota maps model facts, upholstery and dated annual-sales framing | **PASS** — parses; exactly 3 questions; 3/3 visible wordings and substantive answers match | **PASS** — no material shopper-voice violation | **PASS** — 4/4 final 200 | **PASS** — 50 / 131 | **PASS** |
| `trim-levels-explained` | **PASS** — Toyota/KBB/FTC/Ford map trim definitions, materials, equipment and capability cautions | **PASS** — parses; exactly 3 questions; 3/3 visible wordings and substantive answers match | **PASS** — no material shopper-voice violation | **PASS** — 4/4 final 200 | **PASS** — 55 / 139 | **PASS** |
| `used-car-maintenance-mileage` | **PASS** — Toyota/FTC/AAA map the advice; phone explicitly mapped; no MotorHappy recommendation is attributed as fact | **PASS** — parses; exactly 3 questions; 3/3 visible wordings and substantive answers match | **PASS** — MotorHappy answer is direct maintenance guidance; no source-review or publication status | **PASS** — 4/4 final 200 | **PASS** — 52 / 151 | **PASS** |

Result: **6 PASS, 0 FAIL.** Across the 30 page/check combinations: **30 PASS, 0 FAIL**. Every package passes all five requested checks.

## Contract outcomes

| Contract and source | Exact probe / evidence | Expected → observed | Outcome |
|---|---|---|---|
| Claim support, user rubric and six matching review packets | Full packet reads with line numbers; full authored-block, metadata and schema extraction; claim-family comparison below; identical static replay | Every factual shopper-facing claim mapped or visibly flagged → all six pages meet the mapping contract | **PASS** |
| FAQPage parsing and visible parity, user rubric | Python JSON parsing, recursive FAQPage discovery, entity/type checks, normalized visible headings and manual answer comparison; 18-pair table below | Six parseable FAQPage blocks, exactly 3 Question/Answer entities each, 18/18 matching wordings and substantive answers → observed | **PASS** |
| Shopper voice, `brain/VOICE-DNA.md` and user zero-workflow-language rule | Entire visible `#content-main` read; broad workflow/lifecycle/marketing phrase scan and manual classification; unchanged scan replay | Zero visible editor/production/approval/permission/page-lifecycle/publication language → zero material leaks across six pages | **PASS** |
| Internal-link health, rerun2 authored-content scope | 26 independent read-only `curl --location` GETs; exact command template and occurrence ledger below | Every authored internal href occurrence final-200 → 26/26 final HTTP 200, curl exit 0 | **PASS** |
| Metadata length, user rubric | Python Unicode character counts of HTML title/description; extra read-only comparison to six package metadata files | Title 50-60, description 120-158 inclusive → all 12 lengths pass; metadata files match HTML | **PASS** |

No browser or visual score applies to this functional/static QA run.

## Findings

**No current failing findings.** The following closure findings document the corrected failure areas with current file:line evidence; they are not new defects.

### W2-RERUN5-001: About Us claim-map gaps are closed

- Classification / severity: Verified correction; no current blocking defect.
- Expected: Every factual shopper-facing claim maps in this page's own source map or is visibly marked `[NEEDS-VERIFY]`.
- Observed: The contact number `712-792-5000` at `index.html:887,888,891,903,914` is now explicitly mapped to the live About Us source in `aboutus-augment-spirit-lake-REVIEW.md:41`. The “No” answer to whether general inventory contains only Spirit Lake vehicles at `index.html:912`, repeated in schema at `:917`, is now explicitly mapped to the live used-inventory page's Carroll scope at packet `:42`.
- Evidence: `deliveries/site-packages/2026-11-15/motorinnautogroup/aboutus-augment-spirit-lake/index.html:887-917`; `content/drafts/seo/aboutus-augment-spirit-lake-REVIEW.md:35-42`.
- Confirmation: The current page and packet were extracted and hashed twice; both reads were identical. These were the two source-map gaps recorded in rerun4; each now has a claim-specific entry in the matching packet.
- Voice/unknown handling: Entity roles, Spirit Lake address/phone/hours, filtering, transfers, services and inspection details at HTML `:887-908` are shopper requests to confirm the exact situation. They do not assert an unverified ownership relationship, specific Spirit Lake contact details, a location-only filter, transfer guarantee or universal inspection process. Nine operational unknowns remain in packet `:50-58`.
- Disposition: **PASS** for traceability and voice. No package or packet edited by this run.

### W2-RERUN5-002: Maintenance source-review language is replaced by shopper guidance

- Classification / severity: Verified correction; no current blocking defect.
- Expected: Visible copy answers the shopper without source-research, permission, approval, publication or page-lifecycle instructions.
- Observed: Below the MotorHappy question at `index.html:896`, paragraph `:897` now reads: “Follow the vehicle maker’s maintenance schedule, keep complete service records, and get new problems diagnosed early. Weigh any MotorHappy-specific recommendation against the maker’s schedule for your exact vehicle.” It gives direct advice and does not claim to quote or summarize a verified MotorHappy source.
- Evidence: `deliveries/site-packages/2026-11-15/motorinnautogroup/used-car-maintenance-mileage/index.html:896-909`; generic schedule/inspection/warning-sign sources at `content/drafts/seo/used-car-maintenance-mileage-REVIEW.md:29-36`; contact-number source at `:38`; unresolved MotorHappy and dealer-process questions at `:50-53`.
- Confirmation: The complete visible-content extraction and the dedicated voice scan were repeated unchanged; paragraph, source lines and hashes matched. The previous “published guidance ... has not been verified” sentence is absent. Permission, summarization, “not listed yet,” “will appear,” “yet to be,” and source-availability/publication-status language are absent from the visible block.
- Dealer process handling: `index.html:908-909` asks the shopper for documentation on the specific vehicle. It does not promise every used vehicle receives a particular checklist or named reconditioning process.
- Disposition: **PASS** for voice and traceability. No package or packet edited by this run.

## Claim-support specifics

HTML references below mean `deliveries/site-packages/2026-11-15/motorinnautogroup/<slug>/index.html`; packet references mean `content/drafts/seo/<slug>-REVIEW.md`.

| Page | Claim families and HTML evidence | Matching packet source map | Result |
|---|---|---|---|
| `aboutus-augment-spirit-lake` | General inventory at 883-884; five phone mentions at 887/888/891/903/914; general-inventory scope at 912 and schema 917. Other Spirit Lake details are requests to confirm, not affirmative local facts. | 37-42: About Us, used-inventory destination, explicit phone and geographic-scope entries; open questions at 50-58 | **PASS** |
| `heavy-duty-vs-light-duty-trucks` | 13,500/2,440/40,000/8,000-lb maximums at 890; 150/1500 versus HD classes at 893-894; 10%/15% hitch loads at 898; rating definitions at 901-902; exact-configuration/label advice at 886/913-914. Daily-use recommendations are qualified by the exact truck and load. | 31-36: Ford F-150, Super Duty, towing guide, Chevrolet class names and qualified daily-use/nickname wording | **PASS** |
| `highlander-vs-grand-highlander` | 2026 model dimensions/cargo at 887-892; six deltas recompute as 6.5, 3.9, 5.5, 4.6, 9.5 and 13.2; seating up to eight at 912; schema/FAQ summaries supported by the same body/table. | 34-36: Toyota model-dimension sources and explicit computed-delta map | **PASS** |
| `toyota-rav4-carroll-iowa` | Dated 2025 best-ever annual-sales framing at 882/913; electrified lineup and 226/236 hp at 886/894; 8.1-inch clearance and 1,750/3,500-lb grade-specific tow ratings at 894; upholstery at 898-899/912. No guaranteed resale, scarcity or current-stock promise. | 29-32: Toyota overview, product release, brochure/interior specifications and dated sales results | **PASS** |
| `trim-levels-explained` | Model/trim/package definitions at 882-888; truck ratings depend on configuration at 891-892; Toyota material terminology at 895-896/917; equipment/model-year checks at 903-912. | 31-35: Toyota, Kelley Blue Book, FTC and Ford | **PASS** |
| `used-car-maintenance-mileage` | No fixed lifespan at 882-886/921; mileage headings at 892-894 are review points, not universal service intervals; factory schedule, inspection/history, warning signs and corrosion at 889-905; general maintenance guidance at 897; phone at 908. No sourced MotorHappy recommendation or universal dealer-process claim is asserted. | 29-38: Toyota, FTC, AAA and explicit phone mapping; open MotorHappy/process questions at 50-53 | **PASS** |

All six visible authored blocks contain **zero literal `[NEEDS-VERIFY]` markers**. About Us's nine and maintenance's four unresolved items remain packet-side. This passes because the visible text no longer asserts those unresolved details as facts; moving an unsupported factual claim into a packet alone would not meet the visible-flag alternative.

The contract is claim-to-source mapping against the supplied packets, including visible source credits and factual schema summaries. It is not an independent re-research of every external source's truth. Packet-only editorial notes and stale historical flag counts are not shopper-visible claims.

## Shopper-voice specifics

- About Us `index.html:882-915`: full body and footer reviewed. No “not listed yet,” “will appear,” “yet to be,” approval/filter-testing instruction, publication-status note, or future-placement wording remains. “Confirm ... before you drive” addresses the shopper's visit and specific vehicle. **PASS.**
- Maintenance `index.html:881-924`: full body, lists, FAQ and footer reviewed. MotorHappy `:897` is direct maintenance advice, and inspection wording `:908-909` is a vehicle-specific request for records. No source-permission, summarization, verification-state or publication-state note remains visible. **PASS.**
- Trucks `index.html:912` asks how the shopper verifies an exact truck's rating. RAV4 `:903` tells shoppers to verify the exact year and configuration before towing. These are purchase/use advice, not editorial source-review instructions.
- Maintenance `index.html:905` says “before buying or approving a major repair.” The approval concerns the shopper's repair decision, not approval of this page or copy.
- Highlander `index.html:909` qualifies which size suits a family; its source credit at `:923` is permitted factual attribution. Trim `:917` refers to the cited Toyota specification source. Neither describes a content-production or publication workflow.
- All six pages have zero matches to the VOICE-DNA marketing ban list, zero exclamation marks and shopper-question H2 headings. Every visible paragraph, list, table, FAQ and source/related-guide footer was manually read; the result does not rely only on keyword absence.
- About Us's HTML augmentation/approval comment at `index.html:880` is not rendered text. Hidden comments, scripts, JSON-LD and packet-only workflow notes are excluded from the visible `#content-main` voice test.

## FAQPage specifics

All six JSON-LD blocks parse. Each contains exactly three `Question` entities with nonempty `Answer` text. All 18 questions have matching visible heading wording after case/whitespace normalization; all 18 answers match in substance.

As in rerun2, the visible match may be an H1, H2 or FAQ H3. A schema answer may summarize corresponding body/table facts; it need not repeat only a short FAQ paragraph. No unverified MotorHappy recommendation is present in the maintenance schema.

| Page | Schema question | Visible heading line | JSON-LD line | Substantive answer comparison |
|---|---|---:|---:|---|
| `aboutus-augment-spirit-lake` | Should you confirm a used vehicle's location before visiting? | 911 | 917 | PASS — Same exact-vehicle availability and physical-location advice; apostrophe typography differs. |
| `aboutus-augment-spirit-lake` | Does the general inventory page show only Spirit Lake vehicles? | 912 | 917 | PASS — Identical general-inventory answer and request to confirm each vehicle's location. |
| `aboutus-augment-spirit-lake` | Are transfers between locations guaranteed? | 913 | 917 | PASS — Identical conditional transfer caution; no guarantee. |
| `heavy-duty-vs-light-duty-trucks` | How does a light-duty full-size truck compare to a heavy-duty model for everyday use? | 884 | 924 | PASS — Same daily-use versus capacity comparison; exact parking/ride configurations qualified at 886 and capability at 889-890. |
| `heavy-duty-vs-light-duty-trucks` | Why can payload run out before towing capacity? | 896 | 924 | PASS — Same occupants, cargo, accessories, hitch hardware and tongue/pin load explanation at 897-898. |
| `heavy-duty-vs-light-duty-trucks` | Does a 2500 badge tell you the towing capacity? | 919 | 924 | PASS — Same configuration-dependent rating; listed factors also visible at 914. |
| `highlander-vs-grand-highlander` | Is the Grand Highlander bigger than the Highlander? | 881 | 926 | PASS — Same 6.5-inch length and 3.9-inch wheelbase gains. |
| `highlander-vs-grand-highlander` | How much third-row legroom does the Grand Highlander add? | 921 | 926 | PASS — Same 33.5-inch legroom and 5.5-inch gain. |
| `highlander-vs-grand-highlander` | Does the Grand Highlander have more cargo room? | 922 | 926 | PASS — Same cargo advantage; schema's 20.6/97.5 values visible in table at 890/892. |
| `toyota-rav4-carroll-iowa` | What factors explain the Toyota RAV4's market dominance? | 884 | 916 | PASS — Same grades, drivetrain choices and passenger/cargo-space explanation at 885-886. |
| `toyota-rav4-carroll-iowa` | Does every 2026 RAV4 have all-wheel drive? | 910 | 916 | PASS — Same eligible hybrid FWD/AWD and plug-in AWD distinction. |
| `toyota-rav4-carroll-iowa` | Does every RAV4 use SofTex seats? | 912 | 916 | PASS — Same fabric/SofTex/synthetic-suede distinction. |
| `trim-levels-explained` | What do car trim levels mean? | 883 | 922 | PASS — Same equipment-version definition; full definition also visible at 882. |
| `trim-levels-explained` | What does trim level mean on a truck? | 890 | 922 | PASS — Same equipment-version versus towing-rating distinction and configuration caveat. |
| `trim-levels-explained` | Is SofTex leather? | 917 | 922 | PASS — Same Toyota material terminology; no leather assertion. |
| `used-car-maintenance-mileage` | How many miles can a car last before it breaks down? | 881 | 926 | PASS — Same no-fixed-mileage answer and maintenance/history/condition factors. |
| `used-car-maintenance-mileage` | Can maintenance guarantee a car will reach a certain mileage? | 921 | 926 | PASS — Identical no-guaranteed-lifespan answer. |
| `used-car-maintenance-mileage` | Should you buy a used car without service records? | 922 | 926 | PASS — Same uncertainty from missing records and instruction to price/inspect accordingly. |

## Internal-link results

The authored `#content-main` blocks contain **26** `motorinnautogroup.com` href occurrences covering **8** unique URLs. Every occurrence was fetched separately; no duplicate was passed from a cached result. All returned final HTTP 200 and curl exit 0. The raw captured output consisted of the status JSON below with no error text.

Exact command template, with `URL` replaced by each ledger href:

```sh
curl --location --silent --show-error --fail-with-body --connect-timeout 8 --max-time 20 --output /dev/null --write-out '{"http_code":%{http_code},"url_effective":"%{url_effective}","redirects":%{num_redirects},"time_total":%{time_total}}' 'URL'
```

`--location` is `curl -L`. No retry flag, credentials, form submission or external write was used.

| URL | Occurrences tested | Final status | Final URL / redirects |
|---|---:|---:|---|
| `https://www.motorinnautogroup.com/searchused.aspx` | 3 | 200 | `https://www.motorinnautogroup.com/used-inventory`; 1 redirect |
| `https://www.motorinnautogroup.com/aboutus.aspx` | 1 | 200 | same URL; 0 redirects |
| `https://www.motorinnautogroup.com/car-maintenance-by-mileage` | 4 | 200 | same URL; 0 redirects |
| `https://www.motorinnautogroup.com/2022-toyota-rav4-carroll-ia` | 5 | 200 | same URL; 0 redirects |
| `https://www.motorinnautogroup.com/vehicle-trim-levels-explained` | 5 | 200 | same URL; 0 redirects |
| `https://www.motorinnautogroup.com/searchall.aspx` | 4 | 200 | same URL; 0 redirects |
| `https://www.motorinnautogroup.com/highlander-vs-grand-highlander` | 2 | 200 | same URL; 0 redirects |
| `https://www.motorinnautogroup.com/blog/heavy-duty-vs-light-duty-trucks` | 2 | 200 | same URL; 0 redirects |

Occurrence ledger; all package paths are beneath `deliveries/site-packages/2026-11-15/motorinnautogroup/`. Final URLs are exactly those in the summary table: three `searchused.aspx` requests redirect once to `/used-inventory`; all other requests retain their requested URL.

| Probe | Package `index.html:line` | Requested href | Final status | Redirects | curl exit | Transfer seconds |
|---|---|---|---:|---:|---:|---:|
| L01 | `aboutus-augment-spirit-lake/index.html:884` | `https://www.motorinnautogroup.com/searchused.aspx` | 200 | 1 | 0 | 0.341335 |
| L02 | `aboutus-augment-spirit-lake/index.html:914` | `https://www.motorinnautogroup.com/aboutus.aspx` | 200 | 0 | 0 | 0.229607 |
| L03 | `aboutus-augment-spirit-lake/index.html:914` | `https://www.motorinnautogroup.com/searchused.aspx` | 200 | 1 | 0 | 0.305538 |
| L04 | `aboutus-augment-spirit-lake/index.html:915` | `https://www.motorinnautogroup.com/car-maintenance-by-mileage` | 200 | 0 | 0 | 0.220280 |
| L05 | `aboutus-augment-spirit-lake/index.html:915` | `https://www.motorinnautogroup.com/2022-toyota-rav4-carroll-ia` | 200 | 0 | 0 | 0.255686 |
| L06 | `aboutus-augment-spirit-lake/index.html:915` | `https://www.motorinnautogroup.com/vehicle-trim-levels-explained` | 200 | 0 | 0 | 0.260360 |
| L07 | `heavy-duty-vs-light-duty-trucks/index.html:915` | `https://www.motorinnautogroup.com/searchall.aspx` | 200 | 0 | 0 | 0.245499 |
| L08 | `heavy-duty-vs-light-duty-trucks/index.html:922` | `https://www.motorinnautogroup.com/vehicle-trim-levels-explained` | 200 | 0 | 0 | 0.246612 |
| L09 | `heavy-duty-vs-light-duty-trucks/index.html:922` | `https://www.motorinnautogroup.com/car-maintenance-by-mileage` | 200 | 0 | 0 | 0.241580 |
| L10 | `heavy-duty-vs-light-duty-trucks/index.html:922` | `https://www.motorinnautogroup.com/2022-toyota-rav4-carroll-ia` | 200 | 0 | 0 | 0.251370 |
| L11 | `highlander-vs-grand-highlander/index.html:917` | `https://www.motorinnautogroup.com/searchall.aspx` | 200 | 0 | 0 | 0.277745 |
| L12 | `highlander-vs-grand-highlander/index.html:924` | `https://www.motorinnautogroup.com/2022-toyota-rav4-carroll-ia` | 200 | 0 | 0 | 0.252685 |
| L13 | `highlander-vs-grand-highlander/index.html:924` | `https://www.motorinnautogroup.com/vehicle-trim-levels-explained` | 200 | 0 | 0 | 0.251844 |
| L14 | `highlander-vs-grand-highlander/index.html:924` | `https://www.motorinnautogroup.com/car-maintenance-by-mileage` | 200 | 0 | 0 | 0.241529 |
| L15 | `toyota-rav4-carroll-iowa/index.html:907` | `https://www.motorinnautogroup.com/searchall.aspx` | 200 | 0 | 0 | 0.265489 |
| L16 | `toyota-rav4-carroll-iowa/index.html:914` | `https://www.motorinnautogroup.com/highlander-vs-grand-highlander` | 200 | 0 | 0 | 0.247530 |
| L17 | `toyota-rav4-carroll-iowa/index.html:914` | `https://www.motorinnautogroup.com/vehicle-trim-levels-explained` | 200 | 0 | 0 | 0.239331 |
| L18 | `toyota-rav4-carroll-iowa/index.html:914` | `https://www.motorinnautogroup.com/car-maintenance-by-mileage` | 200 | 0 | 0 | 0.240409 |
| L19 | `trim-levels-explained/index.html:908` | `https://www.motorinnautogroup.com/searchall.aspx` | 200 | 0 | 0 | 0.274964 |
| L20 | `trim-levels-explained/index.html:920` | `https://www.motorinnautogroup.com/2022-toyota-rav4-carroll-ia` | 200 | 0 | 0 | 0.248260 |
| L21 | `trim-levels-explained/index.html:920` | `https://www.motorinnautogroup.com/highlander-vs-grand-highlander` | 200 | 0 | 0 | 0.228329 |
| L22 | `trim-levels-explained/index.html:920` | `https://www.motorinnautogroup.com/blog/heavy-duty-vs-light-duty-trucks` | 200 | 0 | 0 | 0.255730 |
| L23 | `used-car-maintenance-mileage/index.html:917` | `https://www.motorinnautogroup.com/searchused.aspx` | 200 | 1 | 0 | 0.298413 |
| L24 | `used-car-maintenance-mileage/index.html:924` | `https://www.motorinnautogroup.com/vehicle-trim-levels-explained` | 200 | 0 | 0 | 0.249670 |
| L25 | `used-car-maintenance-mileage/index.html:924` | `https://www.motorinnautogroup.com/2022-toyota-rav4-carroll-ia` | 200 | 0 | 0 | 0.240211 |
| L26 | `used-car-maintenance-mileage/index.html:924` | `https://www.motorinnautogroup.com/blog/heavy-duty-vs-light-duty-trucks` | 200 | 0 | 0 | 0.271833 |

## Metadata specifics

Character counts use Python `len()` on parsed Unicode title text and the description attribute, including spaces and punctuation. The exact inputs are at `index.html:6` and `:14` for every package. All six `metadata.json` title/meta values also match their HTML counterparts.

| Page | Title length | Meta length | Result |
|---|---:|---:|---|
| `aboutus-augment-spirit-lake` | 52 | 151 | PASS |
| `heavy-duty-vs-light-duty-trucks` | 52 | 136 | PASS |
| `highlander-vs-grand-highlander` | 54 | 139 | PASS |
| `toyota-rav4-carroll-iowa` | 50 | 131 | PASS |
| `trim-levels-explained` | 55 | 139 | PASS |
| `used-car-maintenance-mileage` | 52 | 151 | PASS |

## Evidence and timing

- Native runtime: Python 3.13.6, installed BeautifulSoup with `html.parser`, Python JSON parser and curl 8.7.1 (x86_64-apple-darwin25.0) libcurl/8.7.1 (SecureTransport) LibreSSL/3.3.6 zlib/1.2.12 nghttp2/1.68.1.
- Fixture ownership: Existing packages, packets and metadata were read only. The only newly created repository artifact is this requested report.
- Baseline receipt: `2026-11-15T19:48:26.471987+00:00`; first static extraction: `2026-11-15T19:48:26.604486+00:00`.
- Static replay receipt: `2026-11-15T19:50:25.180812+00:00`; page content, schema/FAQ, metadata, link extraction and all twelve HTML/packet hashes were identical to the initial extraction.
- Dedicated voice-scan replay: byte-identical result, including the three shopper-advice candidate hits classified above.
- Final validation receipt: `2026-11-15T19:50:25.525941+00:00`.
- Probe budget: No total deadline; static commands were finite and completed normally, curl had an 8-second connect and 20-second total limit per occurrence.
- Guarded command time: No aggregate guard was used; not measured. The ledger records curl's own `time_total` per transfer.
- Total session elapsed: Unmeasured; later report writing and verification are outside the probe receipts.
- Stop reason: All five scoped contracts completed for all six packages; no required QA probe remains blocked or not run.
- Revision: `d0c0e5b0f8f188dd4867a28ae3c641f1ad3f8aa5`, branch `main`; no tracked working-tree changes were present. The files on disk, including the committed round-5 fixes, are the consumed inputs.
- Repository-preservation proof: SHA-256 over sorted `(relative path, file SHA-256)` pairs from `git ls-files -co --exclude-standard -z`, excluding only this report. Baseline and final receipts both contain **1904** files and the same digest `9ea818be19eb4841662aa0490af9b0e9e6e6afd7353da532a9cd1b20d1ecff63`. This covers tracked and nonignored untracked files, not ignored caches or Git internals.
- Retained evidence: File:line observations, hash manifest, FAQ ledger, curl command/results and scan details are embedded here and supported by terminal receipts. The caller's single-report write boundary overrides sidecar evidence/checkpoint, second-copy, bookkeeping and learning-store defaults. No evidence sidecar was created or claimed.
- Storage limitation: The local Glyph preflight exited 11 because its saved SMB password is unavailable. No Glyph evidence bundle was written, no credential was changed and no storage-dependent job proceeded. This does not remove any of the five required content/link checks; their evidence is in this report.

### Input hash manifest

| Package | `index.html` SHA-256 | Matching `*-REVIEW.md` SHA-256 | `metadata.json` SHA-256 |
|---|---|---|---|
| `aboutus-augment-spirit-lake` | `9af121fb4f1b728e4f9d90168e37b0b747485eaef9226037097009764a10b2b8` | `c69fc7bded1f00fc75262c5d6276a60699a5fa9a68ebeef388d10fc23f73c3f1` | `9fea15aa4ed9cb3cd37b40a520defa14b3408b1c1c3e2531dfa04249722ace23` |
| `heavy-duty-vs-light-duty-trucks` | `67c551eefebd8e649a04ae9afb358ed8df2cffefd7964b7d79a1b419cc594851` | `41a3dad8af68215972230c9c16296af5d591e9442608f44cde126b68682b4013` | `63639acf8866852cdb910e8832bfb2c7ea5618357add8b4a4480b3010405f7a2` |
| `highlander-vs-grand-highlander` | `eb410ecc86edf4f41d0f973ba4296fcc2aea98a5186ee0d68ede528a50efed9c` | `92fe6b8f9c42e63f914ccbf9b5f33019abcfeda0bf18402bb27a47a0be3be307` | `465f757487cabc8592fb9e581f71b8e11a029640b6a7b98e217e6b8d7e605cb9` |
| `toyota-rav4-carroll-iowa` | `741472daa2aa1b7a5d0c6d9cfccecc0bfdd37e0fc201fe7b3ea2fb289155f909` | `7b2b7a8b32ec5786da79917443c16542899b0f234880abb1987a53c6fcb4f91a` | `74e5ac48c9d8c9d9b3124b7132b6c18d1e5531aa5f5107bb463eb47777d3f453` |
| `trim-levels-explained` | `2ff205e596e32cf2ce18346e467ec7d9df241a49c26eab6da28ca6668262a9ed` | `36b7197f70f6c6cae8f74a72b35dd7b353139e93f1e0cfebe3cc9d3f132727d4` | `e9cd07a725802ac54aa0c768184c87c7f436b49573b0bc757fd22c0ae2928ca5` |
| `used-car-maintenance-mileage` | `9e9fd5161a326fbe61ce63622d4cab832474202b313169884c6606eb7a5b4b16` | `aac4d4cc8f74c80c127e593c70cf9d8da4e9a4acf4835fa37ef5498bcc10b1f1` | `10daaa1e45edd58f9366474263fecb63902db52167d8e681235385101aba09a2` |

### Dedicated visible-text scan

The broad scan treated hits as candidates for manual review. The exact retained patterns were:

```text
workflow_terms: \b(?:editor\w*|production|approv\w*|permission|summari[sz]\w*|publish\w*|publication|schema|handoff|draft|unverified|verified|verify|source[- ]review)\b
page_lifecycle: \b(?:not listed yet|will appear|yet to be|this page|on this page|above|not stated|not published|not been verified|source is available|original publication|approved wording|provide and test|no location-specific claim|until .*source)\b
marketing_bans: \b(?:unleash|elevate|seamless|journey|discover the difference|unparalleled|state-of-the-art|competitive|commitment to excellence)\b|and more!
```

Observed page-lifecycle and marketing-ban hits: **0 across all six pages**. Broad workflow candidates: trucks `:912` (“verify” rating), RAV4 `:903` (“verify” year/configuration), and maintenance `:905` (“approving” a repair). All three are shopper actions, as documented above. About Us and maintenance `:897` contain no workflow candidate. Matching words were not silently ignored.

## Discoveries and proposed permanent check

No product test, package or packet was created or changed. No new regression test is proposed; the existing five-check charter and manual context review covered this rerun.

Durable observation retained only in this report: source maps must name new factual claims such as a contact number or inventory scope; a visible unknown should be replaced by direct shopper guidance only when that guidance stops asserting the unresolved fact. A keyword such as “approve” or “verify” needs context because a shopper can approve a repair or verify a vehicle's configuration.

## Coverage limits, cleanup, and learning

- Source mapping was checked against all six supplied packets; external claim truth was not independently researched. HTTP 200 establishes link status under the requested contract, not factual accuracy of the destination.
- Internal-link scope matches rerun2: every internal href in authored `#content-main`. DealerOn template/navigation links outside the authored blocks, not-yet-published canonical URLs without authored hrefs, responsive/console behavior and public deployment were outside this charter.
- Nine Spirit Lake and four MotorHappy/dealer-process operational questions remain packet-side. They do not produce unsupported affirmative claims in current visible copy. This QA PASS does not close those business questions or grant publication approval.
- The pre-existing untracked `WAVE2-DIRECTIVE.md` and rerun/rerun2/rerun3/rerun4 reports were preserved. The matching repository digest confirms that they and the packages/packets were unchanged.
- No package, packet, draft, product test, dependency, configuration, Git commit or deployment was modified.
- Opened: Short-lived Python/shell and curl command processes only, plus the Glyph preflight command. Closed: All exited normally or, for the preflight, returned its recorded failure; no ongoing process was left by this run.
- No browser tab, GUI app, server, SSH connection/tunnel, watcher or background service was started. No program needed a separate shutdown, and no application or service remains open from this work.
- No automatic memory, learning-store or telemetry helper was run; relevant learning is retained in this report only.

## Final verdict

**PASS.** All six packages pass all five checks at `d0c0e5b0f8f188dd4867a28ae3c641f1ad3f8aa5`: **30/30 page-check combinations**, **18/18 FAQ pairs**, **26/26 final-200 internal href occurrences**, and **12/12 metadata-length checks**. The prior About Us mapping gaps and maintenance voice failure are closed on the tested files. Only the requested report was written.
