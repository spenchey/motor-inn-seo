# Wave 2 publish-readiness verdict

**Date:** 2026-11-15

**Source revision:** `7e1a2e3151687a292a53d2c7dfa59bbb20f932e7` (`motor-inn-seo`, `main`)

**Mirror revision reviewed:** `d3c3b045deb33833f14338f6456b60c73d5c5f53` (`ai-markdown-proxy`, `main`)

**Scope:** Readiness report only. No deployment, DealerOn change, email, or publish action was performed.

## Verdict

- **LEG A — ai.* mirrors: NOT-READY.** All six pages can be converted into the mirror's body-fragment format without reopening content QA, but none of those fragments or catalog records exists in `ai-markdown-proxy`. The shared catalog also lacks per-host page membership, and adding catalog rows alone would leave discovery outputs inconsistent.
- **LEG B — DealerOn www package: NOT-READY.** Every page has a full-chrome `index.html` and `metadata.json`, but every required handoff artifact is missing. All six metadata records also remain `draft-needs-owner-approval`. `/aboutus.aspx` is owner-frozen and must not be included in a publish request.

`READY` in this report means the leg can proceed without another build, routing decision, or approval. A page being technically transformable is not the same as being ready to publish.

The prior adversarial content verdict remains accepted as instructed: PASS 30/30 in `brain/reports/wave2-codex-adversarial-rerun5-2026-11-15.md`. This review did not re-litigate that content QA.

## LEG A / LEG B by page

| Page | LEG A | Intended ai.* mirror | LEG A blocker | LEG B | LEG B blocker or live-route condition |
|---|---|---|---|---|---|
| `aboutus-augment-spirit-lake` | **NOT-READY** | `ai.motorinnautogroup.com` only | Clean section can be extracted, but it has no H1 or house hero; no fragment/catalog record/site filter exists. | **NOT-READY** | `https://www.motorinnautogroup.com/aboutus.aspx` is live (200) and owner-frozen. Do not publish or alter it. |
| `heavy-duty-vs-light-duty-trucks` | **NOT-READY** | `ai.motorinnofcarroll.com` only | Clean article can be extracted, but it lacks the house hero; no fragment/catalog record/site filter exists. | **NOT-READY** | Proposed path is open (404), but the distinct live blog page at `/blog/heavy-duty-vs-light-duty-trucks` is 200 and must stay. Missing all handoff artifacts. |
| `highlander-vs-grand-highlander` | **NOT-READY** | `ai.motorinntoyotaofcarroll.com` only | Clean article can be extracted, but it lacks the house hero; no fragment/catalog record/site filter exists. | **NOT-READY** | Proposed path is already live (200) with the older 2024 page. This must be an explicitly approved in-place update, not a new-page request. Missing all handoff artifacts. |
| `toyota-rav4-carroll-iowa` | **NOT-READY** | `ai.motorinntoyotaofcarroll.com` only | Clean article can be extracted, but it lacks the house hero; no fragment/catalog record/site filter exists. | **NOT-READY** | Proposed path is open (404). The distinct `/2022-toyota-rav4-carroll-ia` page is live (200) and must stay. Missing all handoff artifacts. |
| `trim-levels-explained` | **NOT-READY** | `ai.motorinnautogroup.com` only | Clean article can be extracted, but it lacks the house hero; no fragment/catalog record/site filter exists. | **NOT-READY** | Canonical `/vehicle-trim-levels-explained` is already live (200). This must be an explicitly approved in-place update. Missing all handoff artifacts. |
| `used-car-maintenance-mileage` | **NOT-READY** | `ai.motorinnautogroup.com` only | Clean article can be extracted, but it lacks the house hero; no fragment/catalog record/site filter exists. | **NOT-READY** | Proposed path is open (404). The distinct `/car-maintenance-by-mileage` page is live (200) and must stay. Missing all handoff artifacts. |

The host assignment deliberately avoids publishing the same self-canonical article on all three mirrors. The group mirror receives group/general guidance, the Toyota mirror receives Toyota-model guidance, and the Chevrolet rooftop receives the truck-class guide. Cross-host discovery should use links, not three duplicate article copies. The current code cannot enforce this assignment.

## LEG A — ai.* mirrors

### Transformation feasibility

The six inputs are complete DealerOn-rendered documents. They are not mirror articles as-is: every file includes DealerOn header/footer chrome, `dealerOnTrack`, Typekit, scripts, and site-wide styles.

The content inside each file's `#content-main` is cleanly separable:

| Page | Extracted top-level nodes | H1 | H2 | `<aside class="hero">` | FAQ JSON-LD | DealerOn / Typekit markers in extracted fragment | Relative internal links |
|---|---|---:|---:|---:|---:|---:|---:|
| `aboutus-augment-spirit-lake` | `section`, `script` | 0 | 8 | 0 | 1 | 0 | 0 |
| `heavy-duty-vs-light-duty-trucks` | `article`, `script` | 1 | 9 | 0 | 1 | 0 | 0 |
| `highlander-vs-grand-highlander` | `article`, `script` | 1 | 8 | 0 | 1 | 0 | 0 |
| `toyota-rav4-carroll-iowa` | `article`, `script` | 1 | 7 | 0 | 1 | 0 | 0 |
| `trim-levels-explained` | `article`, `script` | 1 | 9 | 0 | 1 | 0 | 0 |
| `used-car-maintenance-mileage` | `article`, `script` | 1 | 10 | 0 | 1 | 0 | 0 |

All Motor Inn links inside those extracted fragments are already absolute live `https://www.motorinnautogroup.com/...` URLs; none is relative or points to an ai.* mirror. External OEM and consumer-source links may remain external. The accepted 30/30 QA report already covers their live-link health.

Therefore, each page is **transformable** as follows:

1. Extract only the children of `#content-main`; never copy the full `<html>`, `<head>`, DealerOn chrome, site-wide styles, Typekit, or `dealerOnTrack` code.
2. For the five article pages, move the existing H1 and opening direct-answer paragraph into the house `<aside class="hero">` block. Leave the question-led H2 sections, FAQ, sources, and related links in their present order.
3. For `aboutus-augment-spirit-lake`, create a house hero with an H1 from its metadata title and a short lead from its metadata/first direct answer, then keep the existing eight H2 sections. It is a mirror guide only; this does not authorize changing frozen `/aboutus.aspx`.
4. Retain the validated FAQPage JSON-LD alongside the mirror wrapper's generated Article JSON-LD, after confirming the visible FAQ and JSON-LD stay paired byte-for-meaning.
5. Keep every Motor Inn content link on a live `www.` URL. Add one host-aware contact CTA through `article_contact_url(site)` rather than placing a fixed group contact URL in each fragment.

### What happens if only catalog entries are added

There are two distinct failure modes:

- **Catalog row without `articles/<slug>.html`:** `/articles/<slug>` calls `read_text()` on the missing file and errors instead of serving an article.
- **Body files plus catalog rows, with no other code changes:** the article routes, appended `llms.txt` / `llms-full.txt` Guides section, `ai.txt`, and each `/links/<site>.html` Guides section update from `article_catalog()`. The following remain wrong or incomplete:

| Output | Current behavior | Result after catalog-only additions |
|---|---|---|
| Article routes | Catalog-driven, body loaded from `articles/<slug>.html` | New pages serve on **all three hosts**, including brand-mismatched hosts. |
| `llms.txt` and `llms-full.txt` | Dynamic Guides section uses the catalog | Rows appear on all three hosts; no host filtering. |
| `ai.txt` | Dynamic Guides section uses the catalog | Rows appear on all three hosts; no host filtering. |
| `/links/<site>.html` | Guides section uses the catalog | Rows appear on all three links pages; no host filtering. |
| `/sitemap.xml` | Uses hard-coded `DISCOVERY_PATHS`; only the existing used-truck article is hard-coded | Six new article URLs are omitted. |
| `/sitemap.html` | Built from hard-coded discovery paths | Six new article URLs are omitted. |
| Root discovery page | Lists hard-coded discovery paths | Six new article URLs are omitted. |
| Proxied-page hub footer | Hard-codes only `/articles/used-trucks-towing-iowa` | Six new guides are omitted. |
| `/feed.json` | Parses the static source `content/<site>/llms.txt`, not the dynamically appended Guides section | Six new guides are omitted. |
| `/llms?query=...`, JSON query, and MCP public-site search | Search documents include static pages, inventory, and offers; article fragments are not indexed | Agents cannot retrieve the new article text through query/search. |
| `skills.txt`, API catalog, agents card, MCP card | Describe capabilities/endpoints rather than individual guides | No per-article change is required, but they do not compensate for the omissions above. |
| `robots.txt` | Points crawlers to the sitemap | No article-specific edit is needed once the sitemap is fixed. |
| Article dates | Existing record uses global `ARTICLE_DATE_PUBLISHED = "2026-10-31"` | Reusing the constant would publish incorrect dates for wave 2. |

The current per-site contact rewrite is narrow: it rewrites only an exact group `/contactus` link in the fragment. None of these six extracted fragments contains that link, so catalog-only publication would not add a per-site contact link.

### Exact LEG A change list

Changes belong in `github.com/spenchey/ai-markdown-proxy`; none has been made by this report.

1. Add these six body fragments:
   - `articles/aboutus-augment-spirit-lake.html`
   - `articles/heavy-duty-vs-light-duty-trucks.html`
   - `articles/highlander-vs-grand-highlander.html`
   - `articles/toyota-rav4-carroll-iowa.html`
   - `articles/trim-levels-explained.html`
   - `articles/used-car-maintenance-mileage.html`
2. Give each fragment the transformation described above: house hero, question-led H2s, FAQ/source material retained, no DealerOn chrome, no `dealerOnTrack`, no Typekit, and no Motor Inn links except live absolute `www.` links.
3. Extend each catalog record with explicit host membership and dates. Use:
   - group only: `aboutus-augment-spirit-lake`, `trim-levels-explained`, `used-car-maintenance-mileage`
   - Chevrolet only: `heavy-duty-vs-light-duty-trucks`
   - Toyota only: `highlander-vs-grand-highlander`, `toyota-rav4-carroll-iowa`
   - `published: 2026-11-15`; add a separate modified date if the schema supports it.
4. Add `article_catalog_for_site(site)` (or equivalent) and use it in route lookup, `_article_catalog_sections`, related-links pages, sitemap generation, site-guide/root discovery, feed generation, and hub-footer guide links. A disallowed host must return 404 for that slug.
5. Replace the hard-coded article entry in `DISCOVERY_PATHS` and `add_hub_footer_links()` with site-filtered catalog iteration. Build each host's XML sitemap, HTML sitemap, and root discovery list from the same filtered source.
6. Make `/feed.json` consume the dynamic guide catalog directly, or parse `llms_content()` with duplicate protection. Do not continue parsing only the static source file.
7. Add article documents to the deterministic query/MCP search index with the article URL as source and plain visible text as body.
8. Append a host-aware contact CTA during rendering. Confirm these live targets: group `contactus.html` (200), Toyota `contactus.html` (redirects once to live `contactus.aspx`), and Chevrolet `contactus.aspx` (200).
9. Replace the single-slug test assumptions with a table-driven test covering all seven articles (the existing guide plus wave 2), allowed/disallowed hosts, title/meta/canonical, house hero, at least one H2, no forbidden chrome markers, live-www internal links, contact link, sitemap, HTML site guide, root discovery, `llms.txt`, `llms-full.txt`, `ai.txt`, links index, feed, and query/MCP search.
10. Run the full mirror test suite. The current targeted baseline is 2/2 passing for the one existing article; that does not validate wave 2.
11. Stop for owner review. Only after approval would the separate deployment sequence be `git push origin main` and `bash deploy.sh` with `/__health/full` plus per-host/per-page verification. This report does **not** authorize or perform that sequence.

## LEG B — DealerOn publish packaging

### Artifact census

The current wave-2 package directory contains exactly twelve files: six full-chrome `index.html` files and six `metadata.json` files.

| Page | Full-chrome `index.html` | `metadata.json` | Body-only HTML | `full-html/index.html` fallback | `PLACEMENT.md` |
|---|---:|---:|---:|---:|---:|
| `aboutus-augment-spirit-lake` | Exists | Exists | **Missing** | **Missing** | **Missing** |
| `heavy-duty-vs-light-duty-trucks` | Exists | Exists | **Missing** | **Missing** | **Missing** |
| `highlander-vs-grand-highlander` | Exists | Exists | **Missing** | **Missing** | **Missing** |
| `toyota-rav4-carroll-iowa` | Exists | Exists | **Missing** | **Missing** | **Missing** |
| `trim-levels-explained` | Exists | Exists | **Missing** | **Missing** | **Missing** |
| `used-car-maintenance-mileage` | Exists | Exists | **Missing** | **Missing** | **Missing** |

Batch-level status:

| Required artifact | Status |
|---|---|
| `metadata-all.csv` | **Missing** |
| `EMAIL-DRAFT.md` publish-request text | **Missing** |
| `README-DEALERON.md` handoff instructions | **Missing** |
| DealerOn handoff archive containing the page tree | **Missing** |

The existing `index.html` files are useful as sources for the full-page fallbacks, but they are not stored at the handoff's expected `pages/<page>/full-html/index.html` paths. They also cannot serve as the body-only files because they include DealerOn chrome and scripts.

The prior accepted handoff standard, proved by `deliveries/dealeron-handoff-2026-11-06.zip`, is:

```text
/pages/<page>/index.html                 body-only CMS paste
/pages/<page>/full-html/index.html       full-page fallback
/pages/<page>/PLACEMENT.md               path, metadata, breadcrumb, redirects, link obligations
/metadata-all.csv                        batch metadata
/README-DEALERON.md                      package instructions
/EMAIL-DRAFT.md                          exact publish request
```

### Live www route and canonical check

Direct HTTP checks were run on 2026-11-15 with finite connect/total timeouts.

| Wave-2 page | Requested canonical | Live status | Conflict / required treatment |
|---|---|---:|---|
| `aboutus-augment-spirit-lake` | `/aboutus.aspx` | 200 | Exact route is live and owner-frozen. **No change.** Current live title is `About Us | Motor Inn Auto Group in Carroll, Iowa`. |
| `heavy-duty-vs-light-duty-trucks` | `/heavy-duty-vs-light-duty-trucks` | 404 | Open path. Create a new standard content page. Keep the separate live 200 blog `/blog/heavy-duty-vs-light-duty-trucks`; no replacement and no redirect. |
| `highlander-vs-grand-highlander` | `/highlander-vs-grand-highlander` | 200 | Exact route is occupied by the older 2024 comparison. Update in place only after explicit approval; no redirect. |
| `toyota-rav4-carroll-iowa` | `/toyota-rav4-carroll-iowa` | 404 | Open path. Create a new page. Keep live `/2022-toyota-rav4-carroll-ia`; no replacement and no redirect. |
| `trim-levels-explained` | `/vehicle-trim-levels-explained` | 200 | Exact route is occupied by the current trim guide. Update in place only after explicit approval; no redirect. |
| `used-car-maintenance-mileage` | `/used-car-maintenance-mileage` | 404 | Open path. Create a new page. Keep live `/car-maintenance-by-mileage`; no replacement and no redirect. |

The live pages returned canonical tags matching the listed live routes. The three 404 proposed routes returned no competing page. These are route checks, not publication approval.

### Exact LEG B change list

1. Keep `aboutus-augment-spirit-lake` out of the publish set. Either omit it from the handoff archive entirely or include a conspicuous `HOLD-OWNER-FROZEN.md`; do not put `/aboutus.aspx` in `metadata-all.csv` or the publish-request count.
2. For each of the five publishable candidates, create `pages/<page>/index.html` from only the page-owned content in `#content-main`. Do not include DealerOn header, footer, Typekit, `dealerOnTrack`, or site-wide scripts.
3. Copy each current complete document to `pages/<page>/full-html/index.html` as the fallback, preserving the already accepted wave-2 content.
4. Create a `PLACEMENT.md` for every publishable page with the following exact route treatment:
   - `heavy-duty-vs-light-duty-trucks`: create `/heavy-duty-vs-light-duty-trucks`; breadcrumb `Home > Heavy-Duty vs. Light-Duty Trucks`; no redirects; preserve and cross-link the separate live blog.
   - `highlander-vs-grand-highlander`: update existing `/highlander-vs-grand-highlander` in place; breadcrumb `Home > Highlander vs. Grand Highlander`; no redirects; preserve the route and replace only its page body/title/meta after approval.
   - `toyota-rav4-carroll-iowa`: create `/toyota-rav4-carroll-iowa`; breadcrumb `Home > Toyota RAV4 in Carroll, Iowa`; no redirects; keep `/2022-toyota-rav4-carroll-ia` live and add a distinct contextual link rather than repointing it.
   - `trim-levels-explained`: update existing `/vehicle-trim-levels-explained` in place; breadcrumb `Home > Vehicle Trim Levels Explained`; no redirects; preserve all existing inbound links to that path.
   - `used-car-maintenance-mileage`: create `/used-car-maintenance-mileage`; breadcrumb `Home > High-Mileage Used-Car Guide`; no redirects; keep `/car-maintenance-by-mileage` live and add a distinct contextual link rather than repointing it.
5. Put each page's metadata title, meta description, canonical, breadcrumb, redirect rule, and exact internal-link obligations in its `PLACEMENT.md`. Do not infer replacement from a matching topic; state `create`, `update in place`, or `keep separate` exactly as above.
6. Build `metadata-all.csv` for the five publishable pages only. Use the current `metadata.json` title/meta/canonical values; record the store as group and the schema types actually present. Do not add the frozen About page.
7. Add `README-DEALERON.md` explaining body-only versus full-html fallback and repeating the frozen/keep-separate rules.
8. Add `EMAIL-DRAFT.md` requesting **five** pages, not six. It must explicitly say:
   - do not touch `/aboutus.aspx`;
   - keep `/blog/heavy-duty-vs-light-duty-trucks` live;
   - update Highlander and trim guides in place only;
   - create the heavy-duty, RAV4, and high-mileage routes;
   - keep the 2022 RAV4 and mileage-maintenance pages live;
   - pause and ask before changing any occupied path beyond those two approved in-place updates.
9. Re-run packaging validation against the archive: expected file count, metadata/HTML parity, body-only absence of DealerOn chrome, full-html presence, canonical uniqueness, and all `PLACEMENT.md` fields populated.
10. Obtain owner approval for the five-page request and separate explicit approval for the two in-place replacements. QA PASS and package completion are not publish approval.
11. Stop after producing the package and email draft. DealerOn contact and publication remain separate approved actions.

## Evidence summary

- `motor-inn-seo` was clean on `main` at `7e1a2e3` before this report was created.
- All six inputs and six metadata files were read from `deliveries/site-packages/2026-11-15/motorinnautogroup/`.
- The accepted 30/30 report at the named HEAD was used as the content-QA authority.
- `ai-markdown-proxy` was clean on `main` at `d3c3b04`; its current article route, catalog consumers, hard-coded discovery paths, feed source, query sources, tests, and Docker copy behavior were inspected.
- The mirror's existing article test completed 2/2 passing. It proves the current single article is exposed on all three hosts; it does not prove wave-2 readiness.
- The previous 2026-11-06 handoff archive was read to establish the actual DealerOn package standard.
- Live www checks established the 200/404 matrix and current canonical conflicts above.
- No repository other than this report was changed. No deployment command, push, email, DealerOn action, server, browser, tunnel, watcher, or background job was started.
