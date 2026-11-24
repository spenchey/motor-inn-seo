# MOT-3708 used-Carroll round-4 adversarial QA re-run — 2026-11-24

**Verdict: FAIL.** The round-3 mechanical blockers are resolved: the Grand Highlander link works, the unsupported process wording is removed or aligned to mapped paths, the four long sentences are split, and the REVIEW link plans match the current fragments. All 41 internal-link occurrences return final HTTP 200. Claims, metadata, phone, and no-FAQ checks pass. The batch still fails because every page offers several competing next steps instead of one obvious next step as required by `brain/VOICE-DNA.md`.

## Scope and method

- Reviewed HEAD `020f95a` on branch `seo/mot3708-used-carroll-2026-11-24`.
- Compared all four packaged `02_fragment.html` files with their drafts and REVIEW packets under `content/drafts/seo/`.
- Required factual customer-facing claims to have a source mapping in the REVIEW packet or a `[NEEDS-VERIFY]` flag.
- Treated shopper-fit advice and questions as guidance, not factual claims.
- Searched the packaged fragments for FAQPage, JSON-LD, editor/production language, and VOICE-DNA banned wording.
- Counted prose sentences after stripping HTML. No current prose sentence is over 25 words.
- Fetched every internal `href` occurrence with `curl -Ls` against `https://www.motorinnofcarroll.com`, followed redirects, and required final HTTP 200. A failure would have received three rechecks; none failed the first attempt.
- Parsed all four metadata JSON files and counted exact title and meta-description characters.
- Scanned customer-facing drafts, packaged fragments, and metadata for phone-like strings.

## Per-page PASS/FAIL

| Page | Claims mapped or flagged | FAQPage | Shopper voice | Internal hrefs | Meta length | Phone | Overall |
|---|---|---|---|---|---|---|---|
| `car-dealerships-carroll-iowa` | **PASS** — location, brands, 1937, inventory, service, trade/finance paths, and towns are mapped; comparison questions are shopper guidance | **NOTE** — none packaged | **FAIL** — short-sentence check passes, but hours, inventory, trade, finance, phone, contact, and test-drive actions compete | **PASS** — 11/11 final HTTP 200 | **PASS** — 55 / 144 | **PASS** | **FAIL** |
| `used-car-dealer-carroll-iowa` | **PASS** — inventory, dated most-viewed units, on-site service/parts, trade/payment/test-drive paths, towns, and doc-fee wording are mapped or flagged | **NOTE** — none packaged | **FAIL** — short-sentence check passes, but list browsing, payment, trade, phone, test drive, and hours actions compete | **PASS** — 13/13 final HTTP 200 | **PASS** — 55 / 147 | **PASS** | **FAIL** |
| `used-inventory` | **PASS** — live-list behavior, body-style paths, dated most-viewed units, budget, trade, and test-drive paths are mapped or flagged | **NOTE** — none packaged | **FAIL** — short-sentence check passes, but vehicle pages, body-style lists, budget, calculator, phone, trade, and test-drive actions compete | **PASS** — 11/11 final HTTP 200 | **PASS** — 53 / 138 | **PASS** | **FAIL** |
| `used-suvs` | **PASS** — live-list behavior, dated most-viewed units, doc fee, budget, trade, and test-drive paths are mapped or flagged; size-fit copy is shopper guidance | **NOTE** — none packaged | **FAIL** — short-sentence check passes, but listings, phone, test drive, budget, calculator, and trade actions compete | **PASS** — 6/6 final HTTP 200 | **PASS** — 56 / 142 | **PASS** | **FAIL** |

## Round-3 blocker recheck

- **Grand Highlander href: resolved.** The current path uses `Grand+Highlander-Hybrid+MAX+Platinum`. All three authored occurrences returned final HTTP 200.
- **Process-claim wording: resolved.** The used-car page replaces the written-trade and pre-visit-payment promises with REVIEW-mapped trade and payment paths. The used-inventory visit-process sentence is gone. The used-SUV two-vehicle back-to-back promise is gone.
- **Four long sentences: resolved.** Current maximum prose-sentence lengths are 21, 25, 21, and 21 words by page order in the table; none exceeds 25 words.
- **REVIEW link-plan contradiction: resolved.** Each Internal-link plan now lists the current verified paths rather than the removed 404 paths.

## FAQPage note

No packaged fragment contains FAQPage, JSON-LD, or schema markup. This is a note only, not a failure.

## Shopper-voice blocker

The fragments use shopper-facing language, question H2s, short sentences, and none of the VOICE-DNA banned marketing phrases. No editor or production language appears in the packaged copy.

The one-obvious-next-step rule still fails on all four pages. Each page tells the shopper to take several different actions. Internal links alone are not the issue; the copy repeatedly directs the shopper to browse, calculate, trade, call, contact, check hours, or schedule a test drive. No single action is clearly primary and repeated once.

## Clean checks

- All 41 authored internal-link occurrences returned final HTTP 200 on the first attempt.
- All four metadata JSON files parse.
- Meta titles are within 50–60 characters: 55, 55, 53, and 56.
- Meta descriptions are within 120–158 characters: 144, 147, 138, and 142.
- The only phone in customer-facing drafts, packaged fragments, and metadata is `712-792-5000`.
- All factual customer-facing claims are source-mapped in the adjacent REVIEW packet or covered by its `[NEEDS-VERIFY]` list.

**FINAL VERDICT: FAIL — 0 of 4 pages pass; the round-3 mechanical blockers are fixed, but all four pages still violate the required one-obvious-next-step rule.**
