# Staged DealerOn / www fix list — 2026-10-31

**Do not send without Spencer approval.** Current state is internal audit notes.

## Evidence snapshot

- **Scope:** `www.motorinnautogroup.com`, `www.motorinntoyotaofcarroll.com`, `www.motorinnofcarroll.com`.
- **Snapshot method:** fresh raw HTML/XML/robots crawl on 2026-10-31 using browser-like UA.
- **Report:** [brain/reports/local-seo-audit-2026-10-31.md](/Users/spencerheywood/motor-inn-seo/brain/reports/local-seo-audit-2026-10-31.md).

## Fix list for DealerOn / www only

1. **Complete the H1→H6 ladder.** On the live pages, at least one of H5 or H6 is missing on each `www` money page. Add content-bearing headings rather than decorative ones.
2. **Add keyword and variation in title/meta.** Current titles and metas sometimes only include one form. Repeat both keyword and variation as a natural sentence.
3. **Add `knowsAbout`.** Root schema currently has blank `knowsAbout` on all three www sites. Add `Thing` entries for the dealership, Toyota and Chevrolet, with `sameAs` to Wikipedia, Wikidata and Google Knowledge Graph or equivalent entity IDs.
4. **Audit image alt text.** Money pages have no-alt images. Add alt text that names the vehicle context and page intent. Do not keyword-stuff.
5. **Add an HTML sitemap.** All three `www` hosts have XML sitemaps but no visible human sitemap route surfaced in this audit. Add a `/sitemap` or `/sitemap.html` page and link it from footer.
6. **Fix internal 404s.** At minimum these currently return 404: `/used-cars`, `/service-locations.html`, `/contactus.html` and `/terms` on Toyota; `/used-cars`, `/service-locations.html` and `/terms` on Chevrolet; `/used-cars` and `/terms` on Auto Group. Convert to 301 or update internal links.
7. **Fix privacy/terms footers.** AG has both. Toyota and Chevrolet still lack usable `/terms`. Add terms pages and footer links.
8. **Add local business schema.** Use `AutoDealer` with the same NAP, sameAs, address and telephone on used inventory, service and contact paths.
9. **Build the hub layer.** Add services, location and blog hubs with each money page linked from its hub.
10. **Add breadcrumb schema.** BreadcrumbList on inventory, service and contact paths should reflect actual path structure.
11. **Ensure all pages are under 3 clicks from home.** Current sitemap.xml exists but click depth has not been verified with a full crawl.
12. **Standardize www URL form.** Prefer `https://www.*` everywhere and avoid any mixed non-www links.

## Do not do

- No emails.
- No live publishing from this repo.
- No GBP or GSC mutation without Spencer approval.
