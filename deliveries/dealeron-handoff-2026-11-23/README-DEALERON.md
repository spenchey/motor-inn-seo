# Motor Inn: DealerOn handoff (2026-11-23)

**Status: `draft-needs-owner-approval`.** Nothing in this package has been sent or published.

## What this is
Draft handoff for 9 pages from the 2026-11-23 page plan (`docs/page-plans/page-plan-2026-11-23.md`):
- 2 updates to existing pages on motorinnautogroup.com (cycle 1: body only)
- 4 new pages on motorinnofcarroll.com
- 3 new pages on motorinntoyotaofcarroll.com

| Site | Page | Action |
|---|---|---|
| www.motorinnautogroup.com | /contactus.aspx | update-existing (cycle 1: body only) |
| www.motorinnautogroup.com | /used-cars-carroll-iowa | update-existing (cycle 1: body only) |
| www.motorinnofcarroll.com | /chevy-dealer-carroll-iowa | new-page |
| www.motorinnofcarroll.com | /chevy-suvs-for-sale-carroll-iowa | new-page |
| www.motorinnofcarroll.com | /chevy-blazer-for-sale-carroll-iowa | new-page |
| www.motorinnofcarroll.com | /chevy-trucks-for-sale-carroll-iowa | new-page |
| www.motorinntoyotaofcarroll.com | /toyota-dealers-in-iowa | new-page |
| www.motorinntoyotaofcarroll.com | /toyota-tacoma-tundra-for-sale-carroll-iowa | new-page |
| www.motorinntoyotaofcarroll.com | /toyota-sequoia-sienna-for-sale-carroll-iowa | new-page |

## Layout
```text
pages/<site>/<slug>/index.html             body-only HTML: paste into the DealerOn content editor
pages/<site>/<slug>/PLACEMENT.md           exact path, title/meta/H1 rules, placement, redirects, links
pages/<site>/<slug>/full-html/index.html   full-page fallback (new pages) or placement preview (updates)
metadata-all.csv                           titles, metas, canonicals, H1s (+ cycle-2 values for updates)
EMAIL-DRAFTS/                              one email per issue (00-04), none sent
_chrome/                                   live pages captured 2026-11-23T18:29Z, used as the full-html template
_qa/                                       checks + screenshots (390px and 1280px)
```

## Email order (one issue per email)
0. `00-withdraw-old-contact-page.md`: withdraw the retired contact page from the 2026-11-06 handoff. **Send first.**
1. `01-group-site-content-updates.md`: /contactus.aspx block + /used-cars-carroll-iowa body.
2. `02-chevy-site-new-pages.md`: 4 new Chevy pages.
3. `03-toyota-site-new-pages.md`: 3 new Toyota pages.
4. `04-group-301s-after-01-live.md`: 301 three dealership URLs to /contactus.aspx, **only after 01 is live**.

## Before any of this is sent
- [ ] Spencer approves the copy (all 9 pages).
- [ ] Spot-check vehicle descriptions against toyota.com / chevrolet.com (Codex R1-009).
- [ ] Send 00 (withdrawal) before 01.
- [ ] After publish: click-test the model-filter links again, add the cross-links listed in each PLACEMENT.md, re-pull GSC (Chevy property needs the service-account access fix first).

## Source and QA
- Copy, schema and FAQ come from `content/page-packages/2026-11-23/` (generator `_src/build.py`, gate `_src/validate.py`). They passed the Codex adversarial gate (`brain/reports/2026-11-23-pages-codex-adversarial-rerun2-2026-11-23.md`) and the confirm pass.
- Handoff checks: `_qa/qa-results.md`.
- Rebuild: `python3 content/page-packages/2026-11-23/_src/handoff.py`.

## Contact
Spencer Heywood, Motor Inn Auto Group, (712) 792-5000
