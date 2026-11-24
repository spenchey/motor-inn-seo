# MOT-3708 used-Carroll round-3 adversarial QA re-run — 2026-11-24

**Verdict: FAIL.** The round-2 unsupported-claim quotes were removed, metadata and phone checks pass, and 40 of 41 internal-link occurrences return final HTTP 200. The batch still fails: all four pages miss the VOICE-DNA short-declarative and one-obvious-next-step rules, three pages contain new factual process claims that are neither source-mapped nor flagged, and one used-car-dealer link returns final HTTP 404. No draft, REVIEW packet, or package file was changed.

## Scope and method

- Reviewed commit `d49af83` on branch `seo/mot3708-used-carroll-2026-11-24`.
- Compared each `content/drafts/page-packages/2026-11-24/bundle/*/02_fragment.html` with its draft and adjacent REVIEW packet in `content/drafts/seo/`.
- Re-searched the current drafts and fragments for every unsupported quote identified in the round-2 report.
- Treated advice and subjective fit guidance as non-factual. Staff behavior, dealership process, inventory status, pricing, and service-capability statements required an explicit REVIEW-packet source mapping or `[NEEDS-VERIFY]` flag.
- Searched the four packaged fragments for FAQPage / JSON-LD. None is packaged, so FAQPage is a note only.
- Judged shopper voice only on the customer-facing fragments. REVIEW and package-control language was not treated as customer copy.
- Fetched every internal `href` occurrence with `curl -Ls` against `https://www.motorinnofcarroll.com`; redirects were followed and the required final status was HTTP 200.
- Parsed the four metadata JSON files with `jq` and counted exact title and meta-description characters.
- Scanned the customer-facing drafts, fragments, titles, and meta descriptions for phone-like strings. The only customer phone is `712-792-5000`.

## Per-page PASS/FAIL

| Page | Claims mapped or flagged | FAQPage | Shopper voice | Internal hrefs | Meta length | Phone | Overall |
|---|---|---|---|---|---|---|---|
| `car-dealerships-carroll-iowa` | **PASS** — current factual claims are covered by the packet's brand, location, inventory, service, town, and live-path mappings; all round-2 quoted claims are gone | **NOTE** — none packaged | **FAIL** — one 49-word sentence and several competing actions instead of one obvious next step | **PASS** — 11/11 final HTTP 200 | **PASS** — 55 / 144 | **PASS** | **FAIL** |
| `used-car-dealer-carroll-iowa` | **FAIL** — written-trade and pre-visit payment-discussion promises are not established by the packet's proof that trade/finance pages exist | **NOTE** — none packaged | **FAIL** — one 29-word sentence and competing browse, trade, calculator, call, test-drive, and hours actions | **FAIL** — 12/13 final HTTP 200; one final HTTP 404 | **PASS** — 55 / 147 | **PASS** | **FAIL** |
| `used-inventory` | **FAIL** — bringing a trade vehicle to a visit is an operational claim not mapped or flagged in the packet | **NOTE** — none packaged | **FAIL** — one 27-word sentence and competing browse, VDP, budget, calculator, call, trade, and test-drive actions | **PASS** — 11/11 final HTTP 200 | **PASS** — 53 / 138 | **PASS** | **FAIL** |
| `used-suvs` | **FAIL** — the promise that a shopper can ask to drive two SUVs back to back is not mapped or flagged in the packet | **NOTE** — none packaged | **FAIL** — two sentences over 25 words and competing browse, call, test-drive, budget, calculator, and trade actions | **PASS** — 6/6 final HTTP 200 | **PASS** — 56 / 142 | **PASS** | **FAIL** |

## Round-2 unsupported-claim repair

All 11 exact customer-facing passages quoted in the round-2 FAIL report are absent from the current drafts and packaged fragments:

- `car-dealerships-carroll-iowa`: all 3 quoted passages are gone or rewritten.
- `used-car-dealer-carroll-iowa`: both dealership-versus-independent-lot generalizations are gone.
- `used-inventory`: both staff-process promises are gone.
- `used-suvs`: all 4 vehicle-class / demand generalizations are gone or rewritten as shopper guidance.

The `.bak-r2` files still preserve old text as historical backups; they are not the scoped `02_fragment.html` deliverables and were not scored.

## New factual-claim blockers

### `used-car-dealer-carroll-iowa`

The REVIEW packet maps the existence of trade, finance, calculator, and test-drive paths. A live path does not substantiate these more specific staff/process promises in `02_fragment.html:13`:

> “You can ask for a written trade figure on your current vehicle.”

> “You can talk payment ranges before you visit.”

These need a direct operational source mapping or a `[NEEDS-VERIFY]` flag.

### `used-inventory`

The packet maps that trade appraisal exists, but not this visit-process statement in `02_fragment.html:19`:

> “You can also bring the vehicle with you when you visit.”

### `used-suvs`

The packet maps the test-drive form, but the form's existence does not substantiate this two-vehicle staff/process promise in `02_fragment.html:23`:

> “Deciding between sizes? Ask to drive two back to back.”

The `$180` doc-fee statements are not counted as unsupported because their REVIEW packets map them to the brand kit and separately flag live-disclaimer verification.

## FAQPage note

No packaged fragment contains `FAQPage`, JSON-LD, or schema markup. This is a note, not a failure. The used-car-dealer REVIEW packet asks whether FAQPage should be built later, but no FAQ schema is in the scoped deliverable.

## Shopper-voice blockers

No fragment contains VOICE-DNA banned marketing language, `[NEEDS-VERIFY]`, or visible editor/production terms such as `draft`, `review`, `publish`, `production`, `schema`, `SEO`, or `DealerOn`. The H2s are shopper questions and generally answer first.

All four pages still miss the two explicit VOICE-DNA rules at issue in round 2: short declaratives and one obvious next step per page.

- `car-dealerships-carroll-iowa`: the four-part comparison sentence is 49 words. The page sends shoppers to hours, inventory, trade, finance, phone, contact, and test drive.
- `used-car-dealer-carroll-iowa`: the dated most-viewed sentence is 29 words. The page sends shoppers to inventory lists, VDPs, trade, calculator, phone, test drive, and hours.
- `used-inventory`: the most-viewed sentence is 27 words. The page mixes body-style lists, VDPs, budget, calculator, phone, trade, and test drive.
- `used-suvs`: the most-viewed sentence is 29 words and the four-item inspection sentence is 28 words. The page mixes list browsing, VDPs, phone, test drive, budget, calculator, and trade.

## Live internal-link result

The fresh run checked all 41 authored link occurrences across 20 unique destinations. Forty occurrences returned final HTTP 200. One occurrence returned final HTTP 404:

- `used-car-dealer-carroll-iowa/02_fragment.html:9` — HTTP 404 — `https://www.motorinnofcarroll.com/used-Carroll-2024-Toyota-Grand+Highlander+Hybrid+MAX+Platinum-5TDADAB57RS001101`

The same vehicle link works on the other two pages because those paths use `Grand+Highlander-Hybrid` rather than the broken `Grand+Highlander+Hybrid`. Five immediate rechecks of the broken path also returned final HTTP 404.

## REVIEW-packet hygiene note

Each REVIEW packet still contains a stale pre-round-3 Internal-link plan that says the old 404 routes returned 200. A later Round 3 section in the same packet correctly retracts that claim and lists the replacement routes. The packets therefore contradict themselves even though the current fragments mostly use the corrected links.

## Clean checks

- All four metadata JSON files parse.
- Meta titles are within 50–60 characters: 55, 55, 53, and 56.
- Meta descriptions are within 120–158 characters: 144, 147, 138, and 142.
- The only customer-facing phone is `712-792-5000`.
- The round-2 unsupported-claim quotes do not appear in any current draft or scoped fragment.

**FINAL VERDICT: FAIL — 0 of 4 pages pass; do not publish this batch until the new unsupported process claims, VOICE-DNA misses, broken Grand Highlander URL, and contradictory REVIEW-packet link plans are resolved.**
