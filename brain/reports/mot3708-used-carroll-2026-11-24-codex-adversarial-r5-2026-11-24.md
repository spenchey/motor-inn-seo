# MOT-3708 used-Carroll round-5 adversarial QA re-run — 2026-11-24

**Verdict: FAIL.** Two of the four pages pass all required checks. The valid live-link run reached final HTTP 200 for all 41 internal-link occurrences. Metadata, packaged-FAQ, and phone checks pass across the batch. The remaining blockers are one explicit competing CTA on `used-car-dealer-carroll-iowa` and one new factual characterization on `used-inventory` that is not source-mapped or flagged in its REVIEW packet.

## Scope and method

- Reviewed HEAD `6d34a2b` on branch `seo/mot3708-used-carroll-2026-11-24`, using the round-4 report commit `8b15199` as the fixed point.
- Compared all four packaged `02_fragment.html` files with the matching drafts and REVIEW packets under `content/drafts/seo/`; the four package `_pages` copies exactly match their SEO drafts.
- Required every factual customer-facing claim to be source-mapped in the adjacent REVIEW packet or flagged `[NEEDS-VERIFY]`. Shopper-fit advice and comparison questions were treated as guidance, not factual claims.
- Judged the CTA rule exactly as written in `brain/VOICE-DNA.md`: one obvious next step, with the CTA early and repeated once. Descriptive inline links were not automatically counted as competing CTAs. An explicit instruction to take a second action was counted.
- Fetched every internal `href` occurrence with `curl -Ls` against `https://www.motorinnofcarroll.com`, followed redirects, and required final HTTP 200. All passed on the first valid path-by-path attempt, so no failure rechecks were needed.
- Parsed all four `03_metadata.json` files and counted exact title and meta-description characters.
- Scanned the customer-facing drafts, packaged fragments, and metadata for phone-like strings. REVIEW packets were treated as audit documentation because they intentionally quote a forbidden historical number.

## Per-page PASS/FAIL

| Page | Claims mapped or flagged | FAQPage | Shopper voice | Internal hrefs | Meta length | Phone | Overall |
|---|---|---|---|---|---|---|---|
| `car-dealerships-carroll-iowa` | **PASS** — location, brands, 1937, inventory, service, trade/finance paths, and towns are mapped; comparison questions are shopper guidance | **NOTE** — none packaged | **PASS** — the phone CTA appears early and is repeated once; remaining links are declarative | **PASS** — 11/11 final HTTP 200 | **PASS** — 55 / 144 | **PASS** | **PASS** |
| `used-car-dealer-carroll-iowa` | **PASS** — inventory, dated most-viewed units, on-site service/parts, trade/payment/test-drive paths, towns, and doc-fee wording are mapped or flagged | **NOTE** — none packaged | **FAIL** — the closing sentence says “Call … **or use** the test-drive scheduling form,” creating an explicit second CTA | **PASS** — 13/13 final HTTP 200 | **PASS** — 55 / 147 | **PASS** | **FAIL** |
| `used-inventory` | **FAIL** — “shows the **lowest-priced** used vehicles in one place” is a new factual characterization; its REVIEW packet maps the `/under-20k.html` link but does not source that stronger claim or flag it `[NEEDS-VERIFY]` | **NOTE** — none packaged | **PASS** — the phone CTA appears early and is repeated once; other linked resources are described declaratively | **PASS** — 11/11 final HTTP 200 | **PASS** — 53 / 138 | **PASS** | **FAIL** |
| `used-suvs` | **PASS** — live-list behavior, dated most-viewed units, doc fee, budget, trade, and test-drive paths are mapped or flagged; size-fit copy is shopper guidance | **NOTE** — none packaged | **PASS** — the phone CTA appears early and is repeated once; other linked resources are described declaratively | **PASS** — 6/6 final HTTP 200 | **PASS** — 56 / 142 | **PASS** | **PASS** |

## Batch evidence

- All 41 authored internal-link occurrences returned final HTTP 200 on the first valid path-by-path fetch: 11, 13, 11, and 6 by page order above.
- No packaged fragment contains `FAQPage`, JSON-LD, or schema markup. This is a note only, not a failure.
- All four metadata JSON files parse. Titles are within 50–60 characters and meta descriptions are within 120–158 characters.
- Every packaged fragment contains the phone CTA twice: once early and once later.
- The only phone in customer-facing drafts, packaged fragments, and metadata is `712-792-5000`.
- No VOICE-DNA banned marketing phrase appears in the packaged fragments.

**FINAL VERDICT: FAIL — 2 of 4 pages pass; `used-car-dealer-carroll-iowa` has an explicit competing test-drive CTA, and `used-inventory` has an unmapped, unflagged “lowest-priced” factual claim.**
