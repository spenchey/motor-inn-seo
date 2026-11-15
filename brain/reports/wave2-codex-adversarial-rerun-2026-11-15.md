# Wave 2 Codex Adversarial QA Rerun

- Date: 2026-11-15
- Branch: `main`
- Revision under test: `81f88649061c86b12cdc0364ee6b05d556662f92`
- Mode: Full, report-only
- Scope: Six named Wave 2 HTML packages and their six matching `*-REVIEW.md` packets
- Stop condition: All five requested checks completed for all six pages, or any blocked coverage recorded

**Overall verdict: FAIL.** Three packages pass all five checks. Three still expose visible editor, approval, or source-review language and therefore fail the shopper-voice check. No package or review packet was changed.

## Charters

### 1. Factual and numerical claim support

- Contract: Every factual or numerical claim passes only when its packet or footer identifies a relevant fetched source, or the copy carries `[NEEDS-VERIFY]`. Recommendations and subjective fit advice are exempt.
- Risk: Unsupported facts could reach shoppers as if verified.
- Entrypoint: The six named `index.html` files, their matching review packets, and the prior Wave 2 adversarial report.
- Isolation: Read-only local-file inspection at commit `81f8864`; no content edits.
- Exit condition: Every page is classified PASS or FAIL with each unsupported claim quoted or located.
- Commands and inputs: Static file reads plus structured extraction of visible copy, footer sources, and packet fetch evidence.

### 2. FAQPage schema parity

- Contract: Every `FAQPage` JSON block parses; every schema question appears visibly with identical wording after case/whitespace normalization; every visible answer substantively matches its schema answer.
- Risk: Broken or hidden-only schema can mislead search engines and diverge from shopper-facing copy.
- Entrypoint: JSON-LD and visible FAQ sections in each named HTML file.
- Isolation: Local parse and comparison only.
- Exit condition: Parse, question parity, and answer parity recorded for each page.
- Commands and inputs: HTML parser plus JSON parser; no browser or package mutation.

### 3. Shopper voice

- Contract: Visible copy follows `brain/VOICE-DNA.md` and contains no editor or production language.
- Risk: Internal instructions or publishing notes could leak into shopper-facing copy.
- Entrypoint: Visible authored text in each named HTML file.
- Isolation: Static read only.
- Exit condition: PASS or each visible production-language phrase identified.
- Commands and inputs: Voice guide read and visible-text scan with manual review.

### 4. Internal link health

- Contract: Every internal `motorinnautogroup.com` href in the authored blocks returns HTTP 200 after redirects with `curl -L`.
- Risk: Shoppers could reach broken dealership pages.
- Entrypoint: Internal hrefs extracted from the six authored HTML blocks.
- Isolation: Read-only public HTTP GETs; no forms, logins, or writes.
- Exit condition: Final status recorded for every unique authored internal URL, with page-level failures mapped back to their source page.
- Commands and inputs: `curl -L`, 20-second per-URL timeout, standard user agent.

### 5. Search metadata length

- Contract: Title is 50-60 characters and meta description is 120-158 characters.
- Risk: Search snippets may truncate or fail the delivery requirement.
- Entrypoint: Each HTML `<title>` and `<meta name="description">`.
- Isolation: Local parse only.
- Exit condition: Exact text and character counts recorded for all six pages.
- Commands and inputs: HTML parser and Unicode character counts.

## Per-page verdict

| Page | 1. Claims sourced or flagged | 2. FAQPage | 3. Shopper voice | 4. Authored internal hrefs | 5. Title / meta | Overall |
|---|---|---|---|---|---|---|
| `aboutus-augment-spirit-lake` | **PASS** — the packet maps the About Us and inventory facts and the copy carries all 9 Spirit Lake unknowns as `[NEEDS-VERIFY]` | **PASS** — JSON parses; 3/3 questions have identical visible wording after case/whitespace normalization; all 3 answers agree | **FAIL** — visible copy still says “owner confirmation,” “owner-approved,” “after the team confirms,” “confirmed for listing,” “published yet,” and “owner-gated” | **PASS** — 6/6 occurrences; all 5 unique URLs returned final 200 | **PASS** — 52 / 151 | **FAIL** |
| `heavy-duty-vs-light-duty-trucks` | **PASS** — Ford sources cover ratings, maximums, percentages, and labels; Ford/Chevrolet sources cover class naming; daily-use wording is configuration advice | **PASS** — parses; 3/3 questions and answers match | **PASS** — no banned phrase or visible editor/production language found | **PASS** — 4/4 occurrences; all returned final 200 | **PASS** — 52 / 136 | **PASS** |
| `highlander-vs-grand-highlander` | **PASS** — Toyota sources cover both 2026 models and the packet maps all six computed deltas | **PASS** — parses; 3/3 questions and answers match, including the repaired third-row question | **FAIL** — the visible source footer says “Recheck the model-year selector before approval.” | **PASS** — 4/4 occurrences; all returned final 200 | **PASS** — 54 / 139 | **FAIL** |
| `toyota-rav4-carroll-iowa` | **PASS** — official Toyota product sources cover the 2026 facts; the fetched January 5, 2026 sales source now supports the popularity/demand framing | **PASS** — parses; 3/3 questions and answers match | **PASS** — no banned phrase or visible editor/production language found | **PASS** — 4/4 occurrences; all returned final 200 | **PASS** — 50 / 131 | **PASS** |
| `trim-levels-explained` | **PASS** — Toyota, Kelley Blue Book, FTC, and Ford sources now cover upholstery, the general trim definition, used-vehicle identification, and truck-rating cautions | **PASS** — parses; 3/3 questions and answers match | **PASS** — no banned phrase or visible editor/production language found | **PASS** — 4/4 occurrences; all returned final 200 | **PASS** — 55 / 139 | **PASS** |
| `used-car-maintenance-mileage` | **PASS** — Toyota, FTC, and AAA sources cover the no-fixed-mileage position, schedules, inspection/history guidance, warning signs, and corrosion; 4 Motor Inn/MotorHappy unknowns remain flagged | **PASS** — parses; 3/3 questions and answers match | **FAIL** — visible copy discusses “the query behind this section,” checking an original source, permission, and a public URL before summarizing | **PASS** — 4/4 occurrences; all returned final 200 | **PASS** — 52 / 151 | **FAIL** |

Result: **3 PASS, 3 FAIL.** The package set therefore remains **FAIL** under the rule that one failed check fails the page.

## Contract outcomes

| Contract and source | Exact probe / evidence | Expected → observed | Outcome |
|---|---|---|---|
| Factual/numerical support, user rubric and six packets | Static authored-copy extraction plus packet/footer source-map review at `81f8864`; packet evidence in capture 010 | Every non-exempt claim maps to a relevant fetched source or `[NEEDS-VERIFY]` → all six pages met that standard | **PASS** |
| FAQPage parsing and visible parity, user rubric | JSON parse and normalized heading/answer comparison in captures 001 and 011 | All blocks parse; every question is visibly identical ignoring case/whitespace; answers agree → 6 blocks parsed, 18/18 questions matched, 18/18 answers substantively matched | **PASS** |
| Shopper voice, `brain/VOICE-DNA.md` | Visible authored-text extraction and manual review in captures 001 and 011 | No editor/production language → About Us, Highlander, and maintenance contain visible production language | **FAIL** |
| Authored internal links, user rubric | Eight separate `curl -L` probes, captures 002-009 | Final HTTP 200 for every destination → 8/8 unique URLs returned 200, covering all 26 href occurrences | **PASS** |
| Title/meta lengths, user rubric | Unicode character counts in captures 001 and 011 | Title 50-60; description 120-158 → all 6/6 title and 6/6 description lengths passed | **PASS** |

No browser or visual score applies to this functional/static QA run.

## Findings

### W2-RERUN-001: About Us augmentation still speaks to editors

- Classification / severity: Content defect; release-blocking under the requested shopper-voice rule.
- Expected: Visible copy addresses shoppers in short, direct language and contains no internal approval, publication, or implementation instructions.
- Observed: The page says “owner confirmation” (`index.html:887`), “owner-approved” (`:891`), “after the team confirms” (`:895,899`), “confirmed for listing” (`:903`), “published yet” (`:907`), and “owner-gated” (`:914`). These are production-state notes, not shopper answers.
- Evidence: `deliveries/site-packages/2026-11-15/motorinnautogroup/aboutus-augment-spirit-lake/index.html:887-914`; static evidence captures 001 and 011.
- Confirmation: The exact static extraction was replayed on unchanged inputs; captures 001 and 011 contain identical observations and the page SHA-256 remained `76667b8a47157258ea50c7604e28a8ed4e0d92bb8b0aa424abcd7d2d061ed9e3`.
- Next action: Rewrite or remove the editor-facing sentences while retaining the 9 required `[NEEDS-VERIFY]` flags until owner approval.

### W2-RERUN-002: Highlander source footer contains an approval instruction

- Classification / severity: Content defect; release-blocking under the requested shopper-voice rule.
- Expected: The visible source footer identifies sources without telling an editor what to recheck before approval.
- Observed: The footer ends, “Recheck the model-year selector before approval.” (`index.html:923`).
- Evidence: `deliveries/site-packages/2026-11-15/motorinnautogroup/highlander-vs-grand-highlander/index.html:923`; static evidence captures 001 and 011.
- Confirmation: The exact static extraction was replayed on unchanged inputs; captures 001 and 011 contain identical observations and the page SHA-256 remained `d370cf670d0a43e1fd132a5760a185c519cec27ce531df807fa0ca543e1e11dc`.
- Next action: Keep the recheck instruction in the review packet only; remove it from visible page copy.

### W2-RERUN-003: Maintenance page still exposes source-review instructions

- Classification / severity: Content defect; release-blocking under the requested shopper-voice rule.
- Expected: Visible copy answers the MotorHappy question for shoppers or clearly says the advice is unverified without exposing the research workflow.
- Observed: The page says “The query behind this section names another outlet; Motor Inn is checking that original source before repeating any of its advice” (`index.html:897`), followed by a visible instruction to identify the source and obtain permission or a public URL before summarizing (`:898`).
- Evidence: `deliveries/site-packages/2026-11-15/motorinnautogroup/used-car-maintenance-mileage/index.html:897-898`; static evidence captures 001 and 011.
- Confirmation: The exact static extraction was replayed on unchanged inputs; captures 001 and 011 contain identical observations and the page SHA-256 remained `302ae4ee788e5cdf1a4a431145c4c743193e705f627215744d6e52b2b6db9bd0`.
- Next action: Move the query/source/permission note to the review packet. Leave a shopper-facing answer or a concise `[NEEDS-VERIFY]` flag in the page.

## Claim-support specifics

- About Us: the packet identifies the fetched production About Us and inventory pages (`aboutus-augment-spirit-lake-REVIEW.md:35-40`) and lists the 9 flagged Spirit Lake unknowns (`:42-53`). **PASS.**
- Heavy-duty trucks: Ford sources map the 13,500-, 2,440-, 40,000-, 8,000-, 10%, and 15% values, while Ford/Chevrolet map class naming (`heavy-duty-vs-light-duty-trucks-REVIEW.md:29-36`). The daily-use language is configuration advice. **PASS.**
- Highlander: Toyota sources map both models' dimensions, seating, cargo values, and all six computed deltas (`highlander-vs-grand-highlander-REVIEW.md:32-36`). **PASS.**
- RAV4: Toyota sources map the 2026 product facts, and the fetched 2025 year-end sales result now supports the popularity/demand framing (`toyota-rav4-carroll-iowa-REVIEW.md:27-32`). **PASS.**
- Trim levels: Toyota covers upholstery; Kelley Blue Book covers the general definition; FTC covers used-vehicle confirmation; Ford covers configuration-dependent truck ratings (`trim-levels-explained-REVIEW.md:29-36`). **PASS.**
- Maintenance: Toyota supports the schedule and no-fixed-endpoint framing; FTC supports inspection/history guidance; AAA supports warning signs and corrosion; the four Motor Inn/MotorHappy unknowns remain flagged (`used-car-maintenance-mileage-REVIEW.md:27-42`). **PASS.**

## FAQPage specifics

All six `FAQPage` blocks parsed. Each contains three questions. All 18 questions appear visibly with the same wording after case and whitespace normalization, and all 18 schema answers agree in substance with the visible answers. The Highlander repair is present: “How much third-row legroom does the Grand Highlander add?” now appears word-for-word in the visible FAQ at `index.html:921`.

## Internal-link results

The authored blocks contain 26 internal href occurrences using 8 unique URL strings. Each unique string was fetched once with `curl -L`, a 20-second URL timeout, and redirects enabled. Repeated strings inherit the same live result.

| URL | Final status | Final URL / redirects |
|---|---:|---|
| `https://www.motorinnautogroup.com/2022-toyota-rav4-carroll-ia` | 200 | same URL; 0 redirects |
| `https://www.motorinnautogroup.com/aboutus.aspx` | 200 | same URL; 0 redirects |
| `https://www.motorinnautogroup.com/blog/heavy-duty-vs-light-duty-trucks` | 200 | same URL; 0 redirects |
| `https://www.motorinnautogroup.com/car-maintenance-by-mileage` | 200 | same URL; 0 redirects |
| `https://www.motorinnautogroup.com/highlander-vs-grand-highlander` | 200 | same URL; 0 redirects |
| `https://www.motorinnautogroup.com/searchall.aspx` | 200 | same URL; 0 redirects |
| `https://www.motorinnautogroup.com/searchused.aspx` | 200 | `https://www.motorinnautogroup.com/used-inventory`; 1 redirect |
| `https://www.motorinnautogroup.com/vehicle-trim-levels-explained` | 200 | same URL; 0 redirects |

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

- QA evidence bundle: `/Users/spencerheywood/Glyph/scratch/codex/2026-11-wave2-adversarial-rerun/run-20261115T182159Z/evidence.json`
- Evidence SHA-256: `977063e9039f37e573536b0fb7491aeb981459f17700b59104d551e639d4044b`
- Runtime/native tools: Python 3, BeautifulSoup 4.12.3, JSON parser, and `curl -L`.
- Fixture ownership/destinations: read-only repository inputs at `81f8864`; owned QA evidence under Glyph scratch.
- Probe budget: unbounded full functional mode with 30-second capture limits and 20-second per-URL curl limits.
- Guarded command time: 3.280 seconds across captures 001-011.
- Total session elapsed: unmeasured; final report writes and cleanup were not complete when this field was assembled.
- Stop reason: all five requested checks completed for all six packages.

Checkpoints:

- [checkpoint 002](/Users/spencerheywood/Glyph/scratch/codex/2026-11-wave2-adversarial-rerun/run-20261115T182159Z/exploration-002.json) — first live internal URL returned 200.
- [checkpoint 003](/Users/spencerheywood/Glyph/scratch/codex/2026-11-wave2-adversarial-rerun/run-20261115T182159Z/exploration-003.json) — About Us returned 200.
- [checkpoint 004](/Users/spencerheywood/Glyph/scratch/codex/2026-11-wave2-adversarial-rerun/run-20261115T182159Z/exploration-004.json) — truck blog returned 200.
- [checkpoint 005](/Users/spencerheywood/Glyph/scratch/codex/2026-11-wave2-adversarial-rerun/run-20261115T182159Z/exploration-005.json) — maintenance guide returned 200.
- [checkpoint 006](/Users/spencerheywood/Glyph/scratch/codex/2026-11-wave2-adversarial-rerun/run-20261115T182159Z/exploration-006.json) — Highlander comparison returned 200.
- [checkpoint 007](/Users/spencerheywood/Glyph/scratch/codex/2026-11-wave2-adversarial-rerun/run-20261115T182159Z/exploration-007.json) — all-inventory endpoint returned 200.
- [checkpoint 008](/Users/spencerheywood/Glyph/scratch/codex/2026-11-wave2-adversarial-rerun/run-20261115T182159Z/exploration-008.json) — used-inventory endpoint redirected once and returned 200.
- [checkpoint 009](/Users/spencerheywood/Glyph/scratch/codex/2026-11-wave2-adversarial-rerun/run-20261115T182159Z/exploration-009.json) — trim-level guide returned 200.
- [checkpoint 010](/Users/spencerheywood/Glyph/scratch/codex/2026-11-wave2-adversarial-rerun/run-20261115T182159Z/exploration-010.json) — packet/source-map evidence was retained.
- [checkpoint 011](/Users/spencerheywood/Glyph/scratch/codex/2026-11-wave2-adversarial-rerun/run-20261115T182159Z/exploration-011.json) — static inspection replay confirmed the same voice defects on unchanged inputs.

## Coverage limits, hygiene, and learning

- Source relevance was checked against the supplied packets and footer maps. The factual truth of each external source was not independently re-researched because the requested contract requires an identified relevant fetched source, not a fresh external-source audit.
- The eight unique internal URLs cover all 26 href occurrences. Identical repeated URL strings were not re-fetched for each duplicate occurrence.
- The untracked pre-existing `WAVE2-DIRECTIVE.md` was not read or changed.
- No repository-native automated package-QA command is documented; this report used isolated static parsing and live curl probes without installing dependencies.
- No product code, package, packet, test, configuration, commit, browser, GUI app, server, tunnel, watcher, or background process was created or left running.
- Durable learning retained in this report: source footers are visible shopper copy and must receive the same production-language check as body content.

## Final verdict

**FAIL.** The fix pass resolves the previous internal-link failures, the Highlander FAQ mismatch, the RAV4 demand-source gap, and the earlier truck/trim/maintenance source-map gaps. It does not clear shopper voice: `aboutus-augment-spirit-lake`, `highlander-vs-grand-highlander`, and `used-car-maintenance-mileage` still contain visible production language.
