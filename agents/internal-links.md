# 8. Internal and cross-site link plan

## Purpose
Help Carroll-area shoppers move between relevant choices and reach a working dealership action.

## Inputs
Current crawl, topical map, reviewed briefs, confirmed inventory filters, hours/contact/scheduler URLs for each franchise.

## Exact steps
1. Resolve each source and destination to its final URL; record HTTP status, canonical, indexability and owning host. Do not assume a candidate path exists.
2. Add a contextual reciprocal recommendation from `/used-suvs` to `/used-trucks` and from `/used-trucks` to `/used-suvs` when useful for comparing hauling, passenger and cargo needs. Use descriptive anchors such as “browse used trucks in Carroll”; avoid identical exact-match anchors sitewide.
3. Connect each Toyota model page to its current Toyota model inventory; each Chevrolet model page to matching Chevrolet inventory. Check that filters persist and the result is the intended make/model. Do not route a new Tundra page to used Chevrolet stock.
4. Connect each service page to that franchise's verified service hours and contact page, plus the working appointment flow. Label sales and service hours distinctly. Preserve the existing scheduler destination; do not invent one.
5. Link trade-in and sell-to-us pages only where the action fits. Route financing links to the verified secure application. Link inventory pages back to relevant model information when it helps purchase decisions.
6. Prefer permanent categories over transient vehicle detail URLs. Use vehicle links only with a freshness check and an explicit replacement/removal rule after sale. Do not create links to expired VDPs, 404s, redirect chains or tracking URLs.
7. For cross-host journeys among the three sites, record `cross-site` (not same-site internal). Clearly name Toyota/Chevrolet destination. Do not add sitewide reciprocal keyword links or link to AI proxies as consumer inventory pages.
8. Propose exact insertion location, anchor and destination with a reason. Review orphan permanent pages and aim for a logical path within three navigation clicks of the home page where practical. Save a patch plan only.

## Output artifact path
`/Users/spencerheywood/motor-inn-seo/agents/runs/RUN_DATE/internal-links.csv`
Columns: `source_url,section,anchor,destination_url,final_url,link_type,purpose,http_status,canonical,checked_at,inventory_expiry_rule,approval_status`.

## Verification checklist
- [ ] Used-SUVs <-> used-trucks rules covered.
- [ ] Model -> matching inventory and service -> hours/contact covered.
- [ ] Final destinations and filters verified; no sold-vehicle dead ends.
- [ ] Same-site versus cross-site classified accurately.
- [ ] No changes applied and no proxy touched.
