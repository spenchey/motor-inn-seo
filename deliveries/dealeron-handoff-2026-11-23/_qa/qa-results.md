# Handoff QA (2026-11-23)

Result: **PASS**, with 9 pages and zip contents matching the folder: True.

Static checks: body has no H1; H2s are questions; FAQ visible; JSON-LD equals schema.json; phone present; no banned or tracking numbers or workflow text; every link is in the live sitemaps; no IDs in the body. Full page: one H1; body inside #content-main; canonical; title/meta/H1 (new pages) or unchanged title/H1 (cycle-1 updates); contact form kept first; no new duplicate IDs; no 522-2526; assets absolute. Screenshots at 390px and 1280px come from headless Chromium loading the live DealerOn CSS/JS. They're for visual review; they don't measure overflow.

| Page | no_h1_in_body | h2_questions | faq_visible | jsonld_matches_schema | phone_present | no_banned_strings | links_live_in_sitemaps | no_ids_in_body | one_h1 | body_inside_content_main | canonical | title_unchanged_cycle1 | h1_unchanged_cycle1 | form_kept_and_first | no_new_duplicate_ids | no_banned_in_full | assets_absolute | screenshot_390 | screenshot_1280 | title | meta_description | h1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| contactus-carroll | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | n/a | n/a | n/a |
| used-cars-carroll-iowa | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | n/a | ✓ | ✓ | ✓ | ✓ | ✓ | n/a | n/a | n/a |
| chevy-dealer-carroll-iowa | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | n/a | n/a | n/a | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| chevy-suvs-for-sale-carroll-iowa | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | n/a | n/a | n/a | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| chevy-blazer-for-sale-carroll-iowa | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | n/a | n/a | n/a | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| chevy-trucks-for-sale-carroll-iowa | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | n/a | n/a | n/a | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| toyota-dealers-in-iowa | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | n/a | n/a | n/a | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| toyota-tacoma-tundra-for-sale-carroll-iowa | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | n/a | n/a | n/a | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| toyota-sequoia-sienna-for-sale-carroll-iowa | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | n/a | n/a | n/a | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

## Visual review notes (2026-11-23)
- /contactus.aspx preview: the live form stays first; the new block renders below it in the site's styles.
- motorinnofcarroll.com pages: the site-wide "Red Tag" promo banner (live template, dismissible) overlaps the top of the content area in screenshots and hides the H1 until it's closed. The live /aboutus.aspx shows the same; it isn't caused by this package.
- motorinnofcarroll.com header and footer print the site's own tracking numbers (877-...). That's DealerOn chrome, not package copy; the package body uses (712) 792-5000 only.
