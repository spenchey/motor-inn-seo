New task — soft 404 hunt on https://www.motorinnofcarroll.com/ (Chevy).

GSC flagged 'Soft 404' pages on this property (alert 2026-10-07). Use computer control
in Chrome (Spencer's profile, already logged into GSC):

1. Open https://search.google.com/search-console and select property
   https://www.motorinnofcarroll.com/ (URL-prefix version).
2. Go to Indexing > Pages > find the 'Soft 404' row, open it.
3. Export/list up to 20 affected example URLs (the table + any example list).
4. For 3 of those URLs, curl the live page: record HTTP status + <title> +
   whether primary content (vehicle info/inventory grid) actually renders.
5. Diagnose the pattern (e.g., sold-vehicle VDPs returning shell, empty search results,
   model-research stubs) — cite evidence per URL.
6. Write findings to /Users/spencerheywood/motor-inn-seo/brain/soft404-chevy-2026-10-07.md:
   URL list, per-URL evidence, pattern diagnosis, recommended fix.
7. Draft (do NOT send) an email to help@dealeron.com — ONE issue only (the soft-404
   pattern fix) — save to pipeline/drafts/soft404-fix-draft.md.
8. Append a 5-line summary to brain/LOG.md and git commit brain/ + pipeline/drafts/.

Rules: no logins, no password entry, change nothing in GSC, send no email.
Start now.