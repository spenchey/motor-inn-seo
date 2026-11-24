# MOT-3708 used-Carroll round-2 adversarial QA — 2026-11-24

**Verdict: FAIL.** All four pages fail the factual-claim, voice, and live-link checks. No draft, REVIEW packet, or package file was changed.

## Scope and method

- Reviewed commit `e504aa9c2e8c25d2853a855c5d32c4475f75f749` on branch `seo/mot3708-used-carroll-2026-11-24`.
- Compared each `content/drafts/page-packages/2026-11-24/bundle/*/02_fragment.html` with its draft and adjacent REVIEW packet in `content/drafts/seo/`.
- Treated recommendations and clearly subjective fit advice as non-factual. A dealership capability, customer-behavior statement, category generalization, or staff-process promise required a relevant source mapping in the REVIEW packet or a `[NEEDS-VERIFY]` flag.
- Searched every package file and matching draft for `FAQPage` / JSON-LD. None is present, so FAQ is a build-time note and does not fail a page.
- Judged voice only on the customer-facing body. Front matter, REVIEW packets, placement notes, metadata records, and email drafts were not treated as customer copy.
- Fetched every internal `href` occurrence from each fragment against `https://www.motorinnofcarroll.com` with `curl -Ls`, redirects enabled. The required result was final HTTP 200.
- Parsed all four metadata JSON files with `jq` and counted the exact title and description characters.
- Scanned the customer-facing drafts, fragments, and metadata for phone-like strings. The only phone found was `712-792-5000`.

## Per-page PASS/FAIL

| Page | Claims mapped or flagged | FAQPage | Shopper voice | Internal hrefs | Meta length | Phone | Overall |
|---|---|---|---|---|---|---|---|
| `car-dealerships-carroll-iowa` | **FAIL** — 3 unsupported behavior/process passages | **NOTE** — none packaged; build-time decision | **FAIL** — no editor language, but long sentences and many competing next steps conflict with VOICE-DNA | **FAIL** — 5 of 11 occurrences return 404 | **PASS** — 55 / 144 | **PASS** | **FAIL** |
| `used-car-dealer-carroll-iowa` | **FAIL** — 2 unsupported dealership/independent-lot generalizations | **NOTE** — none packaged; build-time decision | **FAIL** — no editor language, but long sentences and many competing next steps conflict with VOICE-DNA | **FAIL** — 4 of 13 occurrences return 404 | **PASS** — 55 / 147 | **PASS** | **FAIL** |
| `used-inventory` | **FAIL** — 2 unsupported staff-process promises | **NOTE** — none packaged; build-time decision | **FAIL** — no editor language, but long sentences and many competing next steps conflict with VOICE-DNA | **FAIL** — 5 of 11 occurrences return 404 | **PASS** — 53 / 138 | **PASS** | **FAIL** |
| `used-suvs` | **FAIL** — 4 unsupported vehicle-fit/demand passages | **NOTE** — none packaged; build-time decision | **FAIL** — no editor language, but long sentences, jargon, and many competing next steps conflict with VOICE-DNA | **FAIL** — 2 of 7 occurrences return 404 | **PASS** — 56 / 142 | **PASS** | **FAIL** |

## Unsupported factual claims — exact customer-facing quotes

### `car-dealerships-carroll-iowa`

The REVIEW packet maps Motor Inn's brands, address, phone, dealership count, towns served, and the existence of linked services. It does not map these staff-process or shopper-behavior assertions (`02_fragment.html:17,21`):

> “Ask and we can walk you through both.”

> “Shoppers regularly weigh a new Silverado against a used one, or a new Highlander against a used one, and the listing pages make that easy to start at home.”

> “For payment ranges, the finance pages and a call to 712-792-5000 get you numbers to weigh before you decide anything.”

### `used-car-dealer-carroll-iowa`

The packet maps Motor Inn's on-site service, parts, trade, payment, and inventory capabilities. It does not source the categorical dealership-versus-independent-lot claims (`02_fragment.html:13`):

> “A dealership handles more of the purchase in one place.”

> “An independent lot can sell you a vehicle; most cannot service it.”

### `used-inventory`

The packet maps the existence of inventory, trade, calculator, and test-drive paths. It does not map these promises about what staff will do (`02_fragment.html:13,25`):

> “Tell us what caught your eye and we will point you at the closest match we can find.”

> “We will tell you what to bring and when to come by.”

### `used-suvs`

The packet maps the live list, named VDP traffic, doc-fee statement, and linked shopping paths. It labels size guidance as a content gap but gives no source for these vehicle-class and buyer-demand assertions (`02_fragment.html:7,13`):

> “Compact crossovers handle commuting and tight parking.”

> “Midsize SUVs add second-row room for kids and gear.”

> “Three-row SUVs carry six to eight people, and the largest ones are the ones shoppers look at for towing campers or boats on weekend trips.”

> “Iowa winters make all-wheel drive a common request.”

The `$180` doc-fee sentences are not counted as unsupported: each is mapped to the brand kit and separately flagged for live-disclaimer verification in its REVIEW packet.

## FAQPage build-time notes

- `car-dealerships-carroll-iowa`: no FAQPage JSON-LD is packaged.
- `used-car-dealer-carroll-iowa`: no FAQPage JSON-LD is packaged. Its REVIEW packet asks whether one should be built, but no schema is in the deliverable.
- `used-inventory`: no FAQPage JSON-LD is packaged.
- `used-suvs`: no FAQPage JSON-LD is packaged.

These are notes, not failures. If FAQPage is added at build time, every schema question must use the identical visible wording and each answer must substantively match the visible answer.

## Shopper-voice findings

No body contains a VOICE-DNA banned phrase or visible terms such as `draft`, `review`, `publish`, `schema`, `SEO`, `[NEEDS-VERIFY]`, or `DealerOn`. All H2s are shopper questions and their opening sentences attempt a direct answer.

The bodies still miss two explicit VOICE-DNA rules: short declaratives and one obvious next step per page, repeated once.

- `car-dealerships-carroll-iowa` contains five sentences over 25 words, including a 50-word inventory-comparison sentence. It sends shoppers to hours, six inventory paths, trade, finance, contact, test drive, and repeated calls.
- `used-car-dealer-carroll-iowa` contains a 36-word service/process sentence and a 29-word VDP sentence. It asks shoppers to browse five list types, call, use trade and payment tools, schedule a test drive, and check hours.
- `used-inventory` contains two sentences over 25 words, including a 28-word test-drive sentence. It mixes body-style browsing, budget, calculator, trade, call, and test-drive actions.
- `used-suvs` contains four sentences over 25 words and uses `driveline`, which is less plain than the surrounding shopper language. It mixes test drive, call, new-SUV comparison, budget, calculator, and trade actions.

## Live internal-link failures

The live run checked all 42 authored link occurrences (20 unique destinations). Twenty-six occurrences returned final HTTP 200; 16 occurrences across 9 unique destinations returned final HTTP 404. The failures below are grouped by page so every failed occurrence is accounted for.

### `car-dealerships-carroll-iowa` — 5 failures

- HTTP 404 — `https://www.motorinnofcarroll.com/new-toyota`
- HTTP 404 — `https://www.motorinnofcarroll.com/new-chevrolets.html`
- HTTP 404 — `https://www.motorinnofcarroll.com/used-trucks`
- HTTP 404 — `https://www.motorinnofcarroll.com/used-suvs`
- HTTP 404 — `https://www.motorinnofcarroll.com/finance-locations.html`

### `used-car-dealer-carroll-iowa` — 4 failures

- HTTP 404 — `https://www.motorinnofcarroll.com/used-suvs`
- HTTP 404 — `https://www.motorinnofcarroll.com/used-trucks`
- HTTP 404 — `https://www.motorinnofcarroll.com/used-vans`
- HTTP 404 — `https://www.motorinnofcarroll.com/under-20000`

### `used-inventory` — 5 failures

- HTTP 404 — `https://www.motorinnofcarroll.com/used-suvs`
- HTTP 404 — `https://www.motorinnofcarroll.com/used-crossovers`
- HTTP 404 — `https://www.motorinnofcarroll.com/used-trucks`
- HTTP 404 — `https://www.motorinnofcarroll.com/used-vans`
- HTTP 404 — `https://www.motorinnofcarroll.com/under-20000`

### `used-suvs` — 2 failures

- HTTP 404 — `https://www.motorinnofcarroll.com/new-suvs`
- HTTP 404 — `https://www.motorinnofcarroll.com/under-20000`

This directly contradicts the four REVIEW packets' statements that these outbound links returned 200 on 2026-11-24.

## Clean checks

- All four metadata JSON files parse.
- All four meta titles are within 50–60 characters: 55, 55, 53, and 56.
- All four meta descriptions are within 120–158 characters: 144, 147, 138, and 142.
- The only phone in customer-facing body and metadata copy is `712-792-5000`.
- Both dated VDP URLs return final HTTP 200 in all six occurrences.
- `/used-inventory` returns final HTTP 200 after redirecting to `/searchused.aspx` in all three occurrences.

**FINAL VERDICT: FAIL — 0 of 4 pages pass; do not publish this batch until the unsupported claims, VOICE-DNA misses, and all 16 broken link occurrences are resolved.**
