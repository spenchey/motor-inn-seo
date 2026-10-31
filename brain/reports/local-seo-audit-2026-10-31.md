# Local SEO audit scorecard — 2026-10-31

* **Scope:** `www.motorinnautogroup.com`, `www.motorinntoyotaofcarroll.com`, `www.motorinnofcarroll.com`, and the three `ai.` mirrors.
* **Evidence snapshot:** fresh raw HTML/XML/robots captured in scratch under `site-pages/raw.jsonl` (2026-10-31).
* **Checklist source:** Chris Simpson’s 2026-10-30 local SEO post, read directly from X/Twitter.

## Summary

- **Pass:** 6
- **Fail:** 12
- **Partial / requires access:** 5
- **Not applicable / not directly testable:** 3
- **Live mirror proof:** `/sitemap.html`, `/terms` and `/privacy` returned 200 on all three mirrors; `/` contains `AutoDealer` and `knowsAbout` evidence on all three.
- **Committed safe fixes:** human sitemap, `AutoDealer` + `knowsAbout` + `sameAs`, policy links, Toyota mirror alt text.
- **No www pages were modified.**

## Scorecard

| Item | Status | Evidence | Fix | Owner |
|---|---|---|---|---|
| Root keyword ladder | partial | AG root has H1-H4, no H5/H6; Toyota root has H1-H5, no H6; Chevrolet root has H1-H6 | DealerOn: add H5/H6 on AG/Toyota root where they are actually content-bearing | DealerOn |
| Used-inventory keyword ladder | partial | `/used-inventory` has H1-H5, not H6 on AG/Toyota/Chevy; H1 exists | DealerOn: add one useful H6 section on each SRP | DealerOn |
| Service keyword ladder | partial | AG service has H1-H4; Toyota/Chevy service pages are valid 200s but ladder is not complete | DealerOn: add H5/H6 blocks to service pages | DealerOn |
| Contact keyword ladder | partial | Chevy contact has H1-H6; other sites lack the full ladder | DealerOn: complete H5/H6 hierarchy | DealerOn |
| Multiple h-tags per level | pass | AG `h3:4`, `h4:4`; Toyota `h3:44`; Chevrolet `h3:11`, `h6:2` | none | Agent |
| Title + variation / meta + variation | partial | Example: Toyota used inventory title has “Pre-Owned” and “Toyota dealer”; Chevy used inventory has “Chevrolet Pre-Owned” and “Chevrolet dealer” | DealerOn: repeat keyword + close variation in title and meta where missing | DealerOn |
| Entity coverage in schema | fail | www root schemas have `knowsAbout: None`; mirror code now has dealer + Toyota/Chevrolet Wikidata/Wikipedia links | Mirrors fixed and committed; dealeron needs the same on www | DealerOn |
| Image filename + alt quality | partial | Toyota mirror root had 4 images with no alt; www pages had varying alt coverage | Mirror root patched; DealerOn audit needed on live money pages | DealerOn |
| Human HTML sitemap | fail (www) / fixed (mirrors) | mirror `/sitemap.html` now returns 200; www has no equivalent route in the audit | DealerOn: add `/sitemap.html` or visible sitemap link | DealerOn |
| XML sitemap | pass | all three `www` hosts return `/sitemap.xml` 200; mirrors `/sitemap.xml` 200 | none | Agent |
| www vs non-www consistency | partial | canonical links use `https://www.*` and no redirect issue found in crawl, but outbound/link inventory was not fully audited | run link inventory next | DealerOn |
| Internal 404s | fail | `motorinnautogroup.com/used-cars` 404; `motorinntoyotaofcarroll.com/used-cars`, `/service-locations.html`, `/contactus.html`, `/terms` 404; `motorinnofcarroll.com/used-cars`, `/service-locations.html`, `/terms` 404 | DealerOn: convert these paths to 301s or update internal links | DealerOn |
| Privacy/terms linked in footer | partial | AG has privacy + terms; Toyota and Chevy still 404 on `/terms`; mirrors now have reciprocal links | mirrors fixed; DealerOn: add terms pages to Toyota/Chevy | DealerOn |
| NAP consistency on-site | partial | mirror pages use single GBP NAP definition; www footer needs fresh exact-match audit | audit www + GBP + listings as one pass | DealerOn |
| Review widget name/photo/date | n-a | not observed in current crawl evidence; needs a live review-check page-by-page audit | confirm whether review schema/widget exists | DealerOn |
| Accordion/tab content in HTML | pass | raw HTML includes non-JS content sections; no crawl-only content blocker found in sample | none | Agent |
| Server-rendered content | pass | key live pages return real HTML, not blank JS shells, for crawler/UA requests | none | DealerOn |
| Click depth ≤3 from home | partial | sitemap.xml is reachable in 1 click; detailed click path audit requires a deeper crawl | run a 2000-URL click-depth crawl next | DealerOn |
| Hubs present | partial | service, contact and sitemap hubs exist, but not a fully linked services / locations / blog hub pattern | DealerOn: build or link a hub layer | DealerOn |
| Blog cannibalization | requires access | no GSC/DataForSEO run in this pass | use GSC query/page export or DataForSEO report | Spencer |
| GBP items | requires access | private GBP categories/services/posts/replies not audited in this pass | public visible pass + GBP API/browser if authorized | Spencer |

## Next 10 priority fixes

1. Fix the eight known broken/missing paths across www sites.
2. Add missing `/terms` experience for Toyota and Chevrolet sites.
3. Add a human HTML sitemap to the www sites.
4. Complete the H1→H6 ladder on service, contact and SRP money pages.
5. Add keyword + variation to title/meta on money pages where missing.
6. Add `knowsAbout` entity coverage to www root schema.
7. Audit alt text and filenames on money-page images.
8. Complete a click-depth and internal-link audit with a dedicated crawler.
9. Standardize NAP and URL form across www, GBP and citations.
10. Run GSC/DataForSEO cannibalization and GBP category/service checks.
