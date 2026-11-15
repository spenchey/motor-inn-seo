# Wave 2 Codex adversarial QA — 2026-11-15

**Verdict: FAIL.** All six packages fail at least one required check. No page source or review packet was changed.

## Method

- Scope: all six `deliveries/site-packages/2026-11-15/motorinnautogroup/*/index.html` files and all ten `content/drafts/seo/*-REVIEW.md` packets. The six matching packets supplied the page-level source maps; the four unrelated packets did not affect a page verdict.
- Claims: a factual or numerical statement passes only when the packet/footer identifies a relevant source or the copy carries `[NEEDS-VERIFY]`. Recommendations and clearly subjective fit advice were not treated as factual claims.
- FAQ: every `FAQPage` block had to parse as JSON. Each schema question had to appear visibly with the same wording, ignoring case and whitespace; its answer also had to agree with the visible answer.
- Voice: the authored content was checked against the sentence, audience, and anti-slop rules in `brain/VOICE-DNA.md`, not just the ten banned terms. Visible drafting instructions and source-review commentary fail because they speak to editors instead of shoppers.
- Links: all 48 unique internal website destinations were fetched with redirects enabled; same-page fragments were checked against document IDs. A matching local package folder does not rescue an absolute website link that returns 404.
- Metadata: the repository's documented targets were used: title 50–60 characters and meta description 120–158 characters (`brain/reports/seo-hygiene-audit-2026-11-15.md:7`).

## PASS/FAIL by page

| Page | Claims sourced or flagged | FAQPage | Voice / AI tells | Internal hrefs | Title / meta | Overall |
|---|---|---|---|---|---|---|
| `aboutus-augment-spirit-lake` | **PASS** — Spirit Lake entity, NAP, filter, transfer, service, and inspection unknowns are flagged; inventory/About Us facts have sources | **PASS** — parses; 3/3 questions and answers match visible copy | **FAIL** — visible copy contains editor instructions such as “the page should,” “do not copy,” and “avoid a blanket quality promise” | **FAIL** — 2 authored link occurrences return 404 | **PASS** — 52 / 151 | **FAIL** |
| `heavy-duty-vs-light-duty-trucks` | **FAIL** — daily-use, ride/parking, and truck-class statements are neither mapped to a source nor flagged | **PASS** — parses; 3/3 questions and answers match visible copy | **PASS** — direct shopper voice; 0 banned phrases or visible production notes | **FAIL** — 2 authored link occurrences return 404 | **PASS** — 52 / 136 | **FAIL** |
| `highlander-vs-grand-highlander` | **PASS** — OEM dimension/seating values and all computed deltas are mapped in the packet | **FAIL** — parses, but only 2/3 schema questions are visibly asked with the same wording | **PASS** — direct shopper voice; 0 banned phrases or visible production notes | **FAIL** — 2 authored link occurrences return 404 | **PASS** — 54 / 139 | **FAIL** |
| `toyota-rav4-carroll-iowa` | **FAIL** — popularity/demand claims lack dated demand evidence or a flag | **PASS** — parses; 3/3 questions and answers match visible copy | **FAIL** — visible copy says “this draft” twice and discusses what evidence should count instead of staying in shopper voice | **FAIL** — 1 authored link occurrence returns 404 | **PASS** — 50 / 131 | **FAIL** |
| `trim-levels-explained` | **FAIL** — sources cover RAV4 upholstery, not the general trim/package and truck-capability claims | **PASS** — parses; 3/3 questions and answers match visible copy | **FAIL** — the public copy exposes “this draft does not call it leather” | **FAIL** — 2 authored link occurrences return 404 | **PASS** — 55 / 139 | **FAIL** |
| `used-car-maintenance-mileage` | **FAIL** — Toyota schedule sources do not cover several reliability, diagnosis, corrosion, and inspection assertions | **PASS** — parses; 3/3 questions and answers match visible copy | **FAIL** — visible copy exposes query analysis, “this Motor Inn draft,” “safe answer,” and approval instructions | **FAIL** — 2 authored link occurrences return 404 | **PASS** — 52 / 151 | **FAIL** |

## Five worst issues

1. **Eleven authored internal-link occurrences are broken across all six pages.** Three unique absolute URLs returned HTTP 404: `/heavy-duty-vs-light-duty-trucks`, `/toyota-rav4-carroll-iowa`, and `/used-car-maintenance-mileage`. The broken occurrences are grouped on `aboutus-augment-spirit-lake/index.html:915`, `heavy-duty-vs-light-duty-trucks/index.html:922`, `highlander-vs-grand-highlander/index.html:924`, `toyota-rav4-carroll-iowa/index.html:914`, `trim-levels-explained/index.html:920`, and `used-car-maintenance-mileage/index.html:925`. The packets say links to new pages must wait for a successful live fetch; see `heavy-duty-vs-light-duty-trucks-REVIEW.md:23-27`, `toyota-rav4-carroll-iowa-REVIEW.md:21-25`, and `used-car-maintenance-mileage-REVIEW.md:21-25`.

2. **Four packages expose internal drafting or approval language to shoppers.** The About Us augmentation tells editors what “the page should” say and says “do not copy” and “avoid a blanket quality promise” (`aboutus-augment-spirit-lake/index.html:888,903-908`). The RAV4 and trim pages refer to “this draft” (`toyota-rav4-carroll-iowa/index.html:889,899`; `trim-levels-explained/index.html:896`). The maintenance page exposes query analysis, a “safe answer,” and approval gating (`used-car-maintenance-mileage/index.html:897-909`). These are obvious production artifacts even though none uses a literal VOICE-DNA banned phrase.

3. **The RAV4 page makes unsupported demand/popularity claims in high-visibility fields.** The title says “Why It Stays Popular” (`index.html:6`), the meta description says demand “stays strong” (`index.html:14`), the lead says the RAV4 “draws broad demand” (`index.html:882`), and the FAQ schema says it has “broad appeal” (`index.html:916`). The packet acknowledges that demand needs to be separated from product facts (`toyota-rav4-carroll-iowa-REVIEW.md:8`), but its source map contains only product specifications and upholstery sources (`:29-31`). These statements need dated sales/shopping evidence or `[NEEDS-VERIFY]`.

4. **Three pages have factual coverage wider than their source maps.** The truck packet maps Ford maximums and tongue/pin percentages, not daily-driving behavior or the 150/1500 versus 250/2500/350/3500 classification (`heavy-duty-vs-light-duty-trucks/index.html:882-894`; packet `:31-34`). The trim sources cover 2026 RAV4 upholstery, not general model/trim/package, truck-rating, or used-identification rules (`trim-levels-explained/index.html:882-912`; packet `:31-32`). The maintenance sources cover Toyota scheduling, not the broader reliability, warning-sign, diagnostic, corrosion, and inspection claims (`used-car-maintenance-mileage/index.html:882-906,921-923`; packet `:29-31`).

5. **The Highlander FAQ schema contains a question that is not visibly asked.** JSON parses, but `How much third-row legroom does the Grand Highlander add?` appears only in schema (`highlander-vs-grand-highlander/index.html:926`). The visible page instead asks `Which has more third-row legroom?` (`:899`). The answer is substantively consistent, but the question-name match is only 2/3.

## Clean checks

- All six title tags and all six meta descriptions are within the repository's stated length ranges.
- All six FAQPage JSON objects parse successfully; five pages have 3/3 visible question-name matches and Highlander has 2/3.
- None of the ten literal banned terms/phrases in `brain/VOICE-DNA.md:11-12` appears in the authored blocks. Four pages still fail voice because they expose internal production language.
- Of 48 unique internal website destinations, 45 returned HTTP 200 after redirects and three returned HTTP 404. All 30 same-page fragment links resolve to existing IDs.
