# MOT-3708 used-Carroll round-6 adversarial QA re-run — 2026-11-24

**Verdict: PASS.** All four pages pass every required check. The two round-5 blockers are resolved: the used-inventory budget sentence now stays within the mapped “vehicles under $20,000” wording, and the used-car-dealer closing now keeps the phone call as the single CTA while describing the test-drive form declaratively.

## Scope and method

- Reviewed HEAD `5b2a3bc` on branch `seo/mot3708-used-carroll-2026-11-24`, after the round-5 report at `brain/reports/mot3708-used-carroll-2026-11-24-codex-adversarial-r5-2026-11-24.md`.
- Re-read all four packaged `02_fragment.html` files, matching SEO drafts, and REVIEW packets. Each SEO draft exactly matches its package `_pages` copy.
- Required each factual customer-facing claim to be source-mapped in its REVIEW packet or explicitly flagged `[NEEDS-VERIFY]`. Shopper-fit advice and comparison questions were treated as guidance, not factual claims.
- Judged voice against `brain/VOICE-DNA.md`: short shopper language, no banned wording, one obvious next step, and the phone CTA early and repeated once. Descriptive inline links were not counted as competing CTAs.
- Fetched every internal `href` occurrence with `curl -Ls` against `https://www.motorinnofcarroll.com`, followed redirects, and required final HTTP 200. All passed on the first valid attempt, so no failure rechecks were needed.
- Parsed all four `03_metadata.json` files and counted exact title and meta-description characters.
- Scanned the customer-facing drafts, packaged fragments, and metadata for phone-like strings. REVIEW packets are audit documentation and intentionally quote a forbidden historical number; that number is not present in customer-facing copy.

## Per-page PASS/FAIL

| Page | Claims mapped or flagged | FAQPage | Shopper voice | Internal hrefs | Meta length | Phone | Overall |
|---|---|---|---|---|---|---|---|
| `car-dealerships-carroll-iowa` | **PASS** — location, brands, 1937, inventory, service, trade/finance paths, and towns are mapped; comparison questions are shopper guidance | **NOTE** — none packaged | **PASS** — phone CTA appears early and is repeated once; all other links are declarative | **PASS** — 11/11 final HTTP 200 | **PASS** — 55 / 144 | **PASS** | **PASS** |
| `used-car-dealer-carroll-iowa` | **PASS** — inventory, dated most-viewed units, on-site service/parts, trade/payment/test-drive paths, towns, and doc-fee wording are mapped or flagged | **NOTE** — none packaged | **PASS** — phone CTA appears early and is repeated once; the test-drive form and hours are now declarative, not competing instructions | **PASS** — 13/13 final HTTP 200 | **PASS** — 55 / 147 | **PASS** | **PASS** |
| `used-inventory` | **PASS** — live-list behavior, body-style routes, dated most-viewed units, under-$20,000 list wording, payment/trade/test-drive paths, and related publish-time cautions are mapped or flagged | **NOTE** — none packaged | **PASS** — phone CTA appears early and is repeated once; linked resources remain descriptive | **PASS** — 11/11 final HTTP 200 | **PASS** — 53 / 138 | **PASS** | **PASS** |
| `used-suvs` | **PASS** — live-list behavior, dated most-viewed units, doc fee, budget, trade, and test-drive paths are mapped or flagged; size-fit copy is shopper guidance | **NOTE** — none packaged | **PASS** — phone CTA appears early and is repeated once; other linked resources are descriptive | **PASS** — 6/6 final HTTP 200 | **PASS** — 56 / 142 | **PASS** | **PASS** |

## Batch evidence

- All 41 authored internal-link occurrences returned final HTTP 200 on the first valid fetch: 11, 13, 11, and 6 by page order above.
- No packaged fragment contains `FAQPage`, JSON-LD, or schema markup. This is a note only, not a failure.
- All four metadata JSON files parse. Titles are within 50–60 characters and meta descriptions are within 120–158 characters.
- Every packaged fragment contains the phone CTA twice: once early and once later.
- The only phone in customer-facing drafts, packaged fragments, and metadata is `712-792-5000`.
- No VOICE-DNA banned wording appears in the packaged fragments.

**FINAL VERDICT: PASS — 4 of 4 pages pass all required round-6 checks; no shipping blocker was found in the reviewed scope.**
