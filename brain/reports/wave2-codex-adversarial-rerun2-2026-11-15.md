# Wave 2 adversarial QA rerun 2

- Date: 2026-11-15
- Revision under test: `5e3a56b7c1ee0af88b22c254d06feffecf01021f`
- Mode: Full, report-only functional QA
- Scope: Six named HTML delivery packages and their six matching `*-REVIEW.md` packets
- Status: FAIL

**Overall verdict: FAIL.** Four packages pass all five checks. `aboutus-augment-spirit-lake` and `used-car-maintenance-mileage` still expose visible page-production, source-review, permission, or publication language. The Highlander footer defect is fixed. No package or review packet was changed.

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
- Entrypoint: Visible text extracted from each HTML file, with focused review of the three prior failures.
- Isolation: Static read and text extraction; no rewriting.
- Exit condition: Zero visible production-language leaks and no material voice violation, or the page fails with exact evidence.

### 4. Internal links

- Contract: Every `motorinnautogroup.com` HTTP(S) `href` in the six HTML files returns HTTP 200 after redirects using `curl -L`.
- Risk: Shoppers could land on broken internal destinations.
- Entrypoint: Deduplicated internal hrefs extracted from the exact HTML inputs.
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
| `aboutus-augment-spirit-lake` | **PASS** — the packet maps the current About Us and inventory sources; all 9 Spirit Lake unknowns remain `[NEEDS-VERIFY]` | **PASS** — JSON parses; 3/3 question wordings match visible headings; answers match in substance | **FAIL** — visible copy still talks about what is “stated on this page,” details being “listed yet,” and details that “will appear above once they are confirmed” | **PASS** — 6/6 occurrences returned final 200 | **PASS** — 52 / 151 | **FAIL** |
| `heavy-duty-vs-light-duty-trucks` | **PASS** — Ford sources map ratings and load percentages; Ford/Chevrolet sources map class naming | **PASS** — parses; 3/3 questions and answers match | **PASS** — no banned phrase or visible editor, production, approval, permission, or publication language found | **PASS** — 4/4 occurrences returned final 200 | **PASS** — 52 / 136 | **PASS** |
| `highlander-vs-grand-highlander` | **PASS** — Toyota sources map both 2026 models and the six computed deltas | **PASS** — parses; 3/3 questions and answers match | **PASS** — the prior “before approval” footer instruction is gone; no remaining production-language leak found | **PASS** — 4/4 occurrences returned final 200 | **PASS** — 54 / 139 | **PASS** |
| `toyota-rav4-carroll-iowa` | **PASS** — Toyota product, brochure, release, and dated sales sources map the visible facts | **PASS** — parses; 3/3 questions and answers match | **PASS** — no banned phrase or visible editor, production, approval, permission, or publication language found | **PASS** — 4/4 occurrences returned final 200 | **PASS** — 50 / 131 | **PASS** |
| `trim-levels-explained` | **PASS** — Toyota, Kelley Blue Book, FTC, and Ford sources map the visible claims | **PASS** — parses; 3/3 questions and answers match | **PASS** — no banned phrase or visible editor, production, approval, permission, or publication language found | **PASS** — 4/4 occurrences returned final 200 | **PASS** — 55 / 139 | **PASS** |
| `used-car-maintenance-mileage` | **PASS** — Toyota, FTC, and AAA sources map the advice; all 4 Motor Inn/MotorHappy unknowns remain `[NEEDS-VERIFY]` | **PASS** — parses; 3/3 questions and answers match | **FAIL** — visible copy still instructs someone to “obtain permission or a reliable public URL before summarizing” and discusses an inspection list that has “not [been] published ... yet” | **PASS** — 4/4 occurrences returned final 200 | **PASS** — 52 / 151 | **FAIL** |

Result: **4 PASS, 2 FAIL.** One failed check fails the page and the package set.

## Contract outcomes

| Contract and source | Exact probe / evidence | Expected → observed | Outcome |
|---|---|---|---|
| Claim support, user rubric and six review packets | Full packet reads plus exact packet capture 029 and page/footer extraction in captures 001 and 028 | Every factual claim maps to a relevant supplied source or `[NEEDS-VERIFY]` → all six pages met the contract | **PASS** |
| FAQPage parsing and visible parity, user rubric | JSON parse plus normalized visible heading/answer comparison in captures 001 and 028 | Six parseable blocks, exactly 3 entities each, 18/18 visible question-wording matches, and 18/18 substantively matching answers → observed | **PASS** |
| Shopper voice, `brain/VOICE-DNA.md` | Visible `#content-main` extraction, phrase scan, and manual review in captures 001 and 028 | Zero visible editor/production/approval language → two pages still contain it | **FAIL** |
| Internal link health, same authored-content scope as the prior report | 26 separate `curl -L` captures, 002-027 | Every internal href occurrence returns final HTTP 200 → 26/26 returned 200 | **PASS** |
| Title/meta length, user rubric | Unicode character counts in captures 001 and 028 | Title 50-60 and meta description 120-158 → all 6/6 titles and 6/6 descriptions passed | **PASS** |

No browser or visual score applies to this functional/static QA run.

## Findings

### W2-RERUN2-001: About Us augmentation still speaks about page production

- Classification / severity: Content defect; release-blocking under the requested zero-production-language rule.
- Expected: Visible copy speaks directly to shoppers and contains no page, editor, approval, or future-placement instructions.
- Observed: The page says the relationship “is not stated on this page yet” (`index.html:887`), repeatedly says information is “not listed yet” (`:891`, `:903`, `:907`), and says Spirit Lake details “will appear above once they are confirmed” (`:914`). These describe page state and future content placement, not the shopper’s answer.
- Evidence: `deliveries/site-packages/2026-11-15/motorinnautogroup/aboutus-augment-spirit-lake/index.html:887-914`; captures 001 and 028; file SHA-256 `85e09b583e1d64fa5121f44dad1fb0e87023f3531aab9d3256c36105ba7e59ca`.
- Confirmation: The static audit replay was byte-identical to the first observation; both observation files have SHA-256 `512fd4da382f9ed4234af8b43bf7b9cec29de5dde0f381b85901cf382ece1bb3`.
- Next action: Keep operational status and future-placement notes in the review packet. Visible copy should give the shopper-safe answer or the required `[NEEDS-VERIFY]` flag without referring to the page lifecycle.

### W2-RERUN2-002: Maintenance page still exposes source and permission workflow

- Classification / severity: Content defect; release-blocking under the requested zero-production-language rule.
- Expected: Visible copy answers shoppers or clearly marks an unknown without telling an editor how to research, obtain permission, or publish it.
- Observed: The MotorHappy paragraph visibly says to “obtain permission or a reliable public URL before summarizing its recommendations” (`index.html:897`). The page also says Motor Inn “has not published its list ... yet” (`:908`). The first sentence is a source-review instruction; the second is publication-state language.
- Evidence: `deliveries/site-packages/2026-11-15/motorinnautogroup/used-car-maintenance-mileage/index.html:897-909`; captures 001 and 028; file SHA-256 `a59cb9bc0ed129cb641d31b369aa3b28c34c517a6a35e1911f28792d80ea7965`.
- Confirmation: The static audit replay was byte-identical to the first observation; both observation files have SHA-256 `512fd4da382f9ed4234af8b43bf7b9cec29de5dde0f381b85901cf382ece1bb3`.
- Next action: Keep the permission, URL, summarization, and publication-status instructions in the review packet. Visible copy should retain only the shopper-facing fallback and required verification marker.

## Claim-support specifics

- About Us: the packet maps the current production About Us page and general used-inventory destination; the 9 Spirit Lake entity, location, inventory-filter, transfer, services, and inspection unknowns remain flagged. **PASS.**
- Heavy-duty trucks: Ford maps the 13,500-, 2,440-, 40,000-, 8,000-, 10%, and 15% figures; Ford/Chevrolet map class naming. **PASS.**
- Highlander: Toyota maps both models' dimensions, seating, cargo values, and all six computed deltas. **PASS.**
- RAV4: Toyota maps the 2026 product facts, while the dated 2025 year-end sales source maps the best-ever annual-sales framing. **PASS.**
- Trim levels: Toyota maps upholstery; Kelley Blue Book maps the general definition; FTC maps used-vehicle confirmation; Ford maps configuration-dependent truck cautions. **PASS.**
- Maintenance: Toyota maps vehicle-specific schedule guidance; FTC maps inspection/history guidance; AAA maps warning signs and corrosion; the four Motor Inn/MotorHappy unknowns remain flagged. **PASS.**

The contract here is source mapping against the supplied packets, not a fresh independent audit of every external source's factual truth.

## FAQPage specifics

All six `FAQPage` blocks parsed and contain exactly three entities. All 18 schema questions have a visible heading with the same wording after case/whitespace normalization. All 18 schema answers match the visible answers in substance. The matching visible question may be the page H1, an H2 section question, or an H3 in the FAQ section, as in the prior report.

## Internal-link results

The authored blocks contain 26 internal href occurrences. Every occurrence was fetched separately with `curl -L`, `--fail-with-body`, and a 20-second URL limit. All 26 returned final HTTP 200.

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

## Metadata specifics

| Page | Title length | Meta length | Result |
|---|---:|---:|---|
| `aboutus-augment-spirit-lake` | 52 | 151 | PASS |
| `heavy-duty-vs-light-duty-trucks` | 52 | 136 | PASS |
| `highlander-vs-grand-highlander` | 54 | 139 | PASS |
| `toyota-rav4-carroll-iowa` | 50 | 131 | PASS |
| `trim-levels-explained` | 55 | 139 | PASS |
| `used-car-maintenance-mileage` | 52 | 151 | PASS |

## Evidence and timing

- QA evidence bundle: `/Users/spencerheywood/Glyph/scratch/codex/2026-11-wave2-adversarial-rerun2/run-20261115T183935Z/evidence/evidence.json`
- Evidence SHA-256: `747d8357b149aebe554ea7dba6a5198dbe7d23f1168937c13ad75ea20b15b6a4`
- Runtime/native tools: Python 3, BeautifulSoup, JSON parser, and `curl -L`.
- Fixture ownership/destinations: read-only repository inputs at `5e3a56b7c1ee0af88b22c254d06feffecf01021f`; owned evidence moved to Glyph scratch.
- Probe budget: unbounded full functional mode with 30-second static/packet capture limits and 25-second link capture limits; each curl had a 20-second URL limit.
- Guarded command time: 8.206 seconds across 29 captures.
- Total session elapsed: unmeasured; report write, acknowledgement, and cleanup were not complete when this field was assembled.
- Stop reason: all five requested checks completed for all six packages.

Checkpoints:

- [checkpoint 002](/Users/spencerheywood/Glyph/scratch/codex/2026-11-wave2-adversarial-rerun2/run-20261115T183935Z/evidence/exploration-002.json) — About Us inventory href returned 200.
- [checkpoint 003](/Users/spencerheywood/Glyph/scratch/codex/2026-11-wave2-adversarial-rerun2/run-20261115T183935Z/evidence/exploration-003.json) — About Us source href returned 200.
- [checkpoint 004](/Users/spencerheywood/Glyph/scratch/codex/2026-11-wave2-adversarial-rerun2/run-20261115T183935Z/evidence/exploration-004.json) — repeated About Us inventory href returned 200.
- [checkpoint 005](/Users/spencerheywood/Glyph/scratch/codex/2026-11-wave2-adversarial-rerun2/run-20261115T183935Z/evidence/exploration-005.json) — About Us maintenance href returned 200.
- [checkpoint 006](/Users/spencerheywood/Glyph/scratch/codex/2026-11-wave2-adversarial-rerun2/run-20261115T183935Z/evidence/exploration-006.json) — About Us RAV4 href returned 200.
- [checkpoint 007](/Users/spencerheywood/Glyph/scratch/codex/2026-11-wave2-adversarial-rerun2/run-20261115T183935Z/evidence/exploration-007.json) — About Us trim href returned 200.
- [checkpoint 008](/Users/spencerheywood/Glyph/scratch/codex/2026-11-wave2-adversarial-rerun2/run-20261115T183935Z/evidence/exploration-008.json) — truck inventory href returned 200.
- [checkpoint 009](/Users/spencerheywood/Glyph/scratch/codex/2026-11-wave2-adversarial-rerun2/run-20261115T183935Z/evidence/exploration-009.json) — truck trim href returned 200.
- [checkpoint 010](/Users/spencerheywood/Glyph/scratch/codex/2026-11-wave2-adversarial-rerun2/run-20261115T183935Z/evidence/exploration-010.json) — truck maintenance href returned 200.
- [checkpoint 011](/Users/spencerheywood/Glyph/scratch/codex/2026-11-wave2-adversarial-rerun2/run-20261115T183935Z/evidence/exploration-011.json) — truck RAV4 href returned 200.
- [checkpoint 012](/Users/spencerheywood/Glyph/scratch/codex/2026-11-wave2-adversarial-rerun2/run-20261115T183935Z/evidence/exploration-012.json) — Highlander inventory href returned 200.
- [checkpoint 013](/Users/spencerheywood/Glyph/scratch/codex/2026-11-wave2-adversarial-rerun2/run-20261115T183935Z/evidence/exploration-013.json) — Highlander RAV4 href returned 200.
- [checkpoint 014](/Users/spencerheywood/Glyph/scratch/codex/2026-11-wave2-adversarial-rerun2/run-20261115T183935Z/evidence/exploration-014.json) — Highlander trim href returned 200.
- [checkpoint 015](/Users/spencerheywood/Glyph/scratch/codex/2026-11-wave2-adversarial-rerun2/run-20261115T183935Z/evidence/exploration-015.json) — Highlander maintenance href returned 200.
- [checkpoint 016](/Users/spencerheywood/Glyph/scratch/codex/2026-11-wave2-adversarial-rerun2/run-20261115T183935Z/evidence/exploration-016.json) — RAV4 inventory href returned 200.
- [checkpoint 017](/Users/spencerheywood/Glyph/scratch/codex/2026-11-wave2-adversarial-rerun2/run-20261115T183935Z/evidence/exploration-017.json) — RAV4 Highlander href returned 200.
- [checkpoint 018](/Users/spencerheywood/Glyph/scratch/codex/2026-11-wave2-adversarial-rerun2/run-20261115T183935Z/evidence/exploration-018.json) — RAV4 trim href returned 200.
- [checkpoint 019](/Users/spencerheywood/Glyph/scratch/codex/2026-11-wave2-adversarial-rerun2/run-20261115T183935Z/evidence/exploration-019.json) — RAV4 maintenance href returned 200.
- [checkpoint 020](/Users/spencerheywood/Glyph/scratch/codex/2026-11-wave2-adversarial-rerun2/run-20261115T183935Z/evidence/exploration-020.json) — trim inventory href returned 200.
- [checkpoint 021](/Users/spencerheywood/Glyph/scratch/codex/2026-11-wave2-adversarial-rerun2/run-20261115T183935Z/evidence/exploration-021.json) — trim RAV4 href returned 200.
- [checkpoint 022](/Users/spencerheywood/Glyph/scratch/codex/2026-11-wave2-adversarial-rerun2/run-20261115T183935Z/evidence/exploration-022.json) — trim Highlander href returned 200.
- [checkpoint 023](/Users/spencerheywood/Glyph/scratch/codex/2026-11-wave2-adversarial-rerun2/run-20261115T183935Z/evidence/exploration-023.json) — trim truck-blog href returned 200.
- [checkpoint 024](/Users/spencerheywood/Glyph/scratch/codex/2026-11-wave2-adversarial-rerun2/run-20261115T183935Z/evidence/exploration-024.json) — maintenance inventory href returned 200.
- [checkpoint 025](/Users/spencerheywood/Glyph/scratch/codex/2026-11-wave2-adversarial-rerun2/run-20261115T183935Z/evidence/exploration-025.json) — maintenance trim href returned 200.
- [checkpoint 026](/Users/spencerheywood/Glyph/scratch/codex/2026-11-wave2-adversarial-rerun2/run-20261115T183935Z/evidence/exploration-026.json) — maintenance RAV4 href returned 200.
- [checkpoint 027](/Users/spencerheywood/Glyph/scratch/codex/2026-11-wave2-adversarial-rerun2/run-20261115T183935Z/evidence/exploration-027.json) — maintenance truck-blog href returned 200.
- [checkpoint 028](/Users/spencerheywood/Glyph/scratch/codex/2026-11-wave2-adversarial-rerun2/run-20261115T183935Z/evidence/exploration-028.json) — static replay confirmed unchanged inputs and voice findings.
- [checkpoint 029](/Users/spencerheywood/Glyph/scratch/codex/2026-11-wave2-adversarial-rerun2/run-20261115T183935Z/evidence/exploration-029.json) — exact review packets and hashes retained.

## Discoveries and proposed permanent check

No product test was created in this report-only run.

| Discovery | Proposed case | Evidence | Disposition |
|---|---|---|---|
| Replacing explicit approval terms with “not listed yet” or “will appear above” can still leave visible page-lifecycle language; a `[NEEDS-VERIFY]` block can still contain source-review instructions. | Extend the existing static visible-text audit to flag page-state, future-placement, permission, summarization, and publication instructions in `#content-main`, then require manual review of every hit. | Findings W2-RERUN2-001 and W2-RERUN2-002; captures 001 and 028. | Proposed only; no test or package changed. |

Value: protects=shopper copy from editor and source-review instructions; fails_when=page-state, permission, summarization, or publication wording remains visible; why_new=the prior phrase list missed page-lifecycle wording; seam=none; no_claim=semantic voice quality beyond matched phrases still needs manual review

## Coverage limits, cleanup, and learning

- Source relevance was checked against the supplied packets and visible source maps. External source truth was not independently re-researched because the requested contract is source mapping, not a new source audit.
- Internal-link scope matches the prior report: all 26 `motorinnautogroup.com` href occurrences inside the authored `#content-main` blocks. DealerOn template/navigation links outside those authored blocks were not part of the prior contract and were not re-tested.
- The pre-existing untracked `WAVE2-DIRECTIVE.md` and prior untracked rerun report were not changed.
- The Glyph evidence copy was verified against the 175-file SHA-256 manifest. The temporary local evidence directory was moved to Trash and remains recoverable.
- No package, review packet, draft, test, configuration, dependency, commit, browser, GUI app, server, tunnel, watcher, or background service was created or changed.
- Durable learning retained here only: a voice fix is incomplete when it removes approval vocabulary but still tells shoppers where future content will appear or how an editor should obtain and summarize a source.

## Final verdict

**FAIL.** The round-2 commit clears the Highlander voice failure and leaves every claim, FAQ, link, title, and meta check passing. It does not clear shopper voice for `aboutus-augment-spirit-lake` or `used-car-maintenance-mileage`, so the six-package set is not ready under the requested all-checks-pass rule.
