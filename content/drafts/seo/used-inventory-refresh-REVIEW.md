# REVIEW PACKET — used-inventory-refresh (MOT-3708 item 1)

Batch: mot3708-used-carroll-2026-11-24 | Draft: content/drafts/seo/used-inventory-refresh.md
Status: draft-needs-owner-approval. Action: REPLACE the custom content section of the live /used-inventory page; the DealerOn inventory listings module stays untouched.

## Why this page, why now (queue row)
NOW row from the weekly synthesis 2026-11-23 (Jeeves, findings/reports/digital-synthesis-2026-11-23.md), Spencer's direction in #sales: /used-inventory holds pos 9.3 with 16 clicks / 572 impressions (GSC week Nov 9-15); engagement is strong (1,330 views, 171s avg; used_vdp conversions 1,849; organic bounce 0.4%), so the gap is visibility/copy, not demand. Mobile is 71% of sessions - copy is written short-paragraph, answer-first for phone reading. Note: audits/audit-2026-11-23.md top-pages table shows slightly different GSC page figures (12 clicks / 580 impr, pos 10.9); the synthesis numbers are the task-of-record figures - [NEEDS-VERIFY] which pull Spencer wants quoted.
TRAPS respected: no investment in /searchused.aspx or /service-area (brain/STATE.md TRAPS rows) - this draft links only to owned content URLs and live body-style pages, never the trap URLs (searchused.aspx appears in the DealerOn nav chrome only, which we do not touch).

## Competitor gap (10x method)
Top SERP/AI answers for 'used car dealer carroll iowa' and 'car dealerships in carroll iowa' (brain/ai-visibility/ai-vis-2026-11-23.md, brain/competitor-read-2026-09-23.md): Choice Auto, Wittrock Motor, Pro Auto, Car Stop lead AI citations; Motor Inn 0/4 on the used-dealer query. Their pages are generic lot listicles. Gaps we win on: (1) a live list that IS the answer (DealerOn SRP), (2) named current vehicles as concrete proof, (3) body-style routing that answers the shopper's real first question (cars vs SUV vs truck), (4) trade + finance + test-drive next steps in one stop. The current live copy has NO links to specific vehicles; the refresh fixes that with the two most-viewed used VDPs.

## Metadata
- Title (53 chars): Used Cars, SUVs and Trucks in Carroll, IA | Motor Inn  [unchanged from live; already in spec]
- Meta description (138 chars): Shop used cars, SUVs and trucks in Carroll, IA at Motor Inn Auto Group. See the current list, narrow by body style, and call 712-792-5000.
- Canonical: /used-inventory (unchanged)

## Claim contract
May say (sourced): two brands under one roof, Toyota and Chevrolet live SRP pages (live site nav); address 1526 Le Clark Road, Carroll IA 51401 (BRAND-FACTS.json); phone 712-792-5000 (BRAND-FACTS.json); family-owned since 1937 (BRAND-CORE.md, Spencer first-hand 2026-11-03); vehicle cards show current price/details (live page behavior); body-style pages exist and list live stock (verified HTTP 200 2026-11-24); trade appraisal, financing, payment calculator, test-drive scheduling exist (URLs verified 200 2026-11-24); the two named VDPs were the most-viewed used vehicles in GA4 week Nov 9-15 (audits/audit-2026-11-23.md top-pages table) and both URLs returned 200 on 2026-11-24.
Must not say: days-on-lot or popularity pressure ('selling fast', 'won't last', 'popular'), invented prices/payments, 'best/top' superlatives, one-owner or clean-history guesses, any other phone number.
Needs checking first: the two VDP links at publish time (inventory turns); whether the 'most-viewed' line stays in the refresh or is stripped to age-proof the copy.

## Internal-link plan
Outbound in draft (all verified HTTP 200 on 2026-11-24): /used-cars, /used-suvs, /used-crossovers, /used-trucks, /used-vans, /under-20000, /paymentcalc.aspx, /finance-locations.html, /trade.aspx, /testdrive.aspx?type=Used, plus the two VDPs.
VDP link anchors: '2017 Toyota RAV4 Hybrid XLE', '2024 Toyota Grand Highlander Hybrid MAX Platinum'.
Inbound FROM already-ranking pages (for the DealerOn request, anchors chosen): /car-maintenance-by-mileage (pos 8.0, 938 impr/wk) anchor 'shop used vehicles in Carroll' -> /used-inventory; /vehicle-trim-levels-explained (pos 8.5, 1,676 impr/wk) anchor 'compare live used inventory by trim' -> /used-inventory; /car-dealerships-carroll-iowa (cluster page, refreshed in this batch) anchor 'used inventory' -> /used-inventory.

## Sources
- findings/reports/digital-synthesis-2026-11-23.md (task data, week Nov 9-15)
- audits/audit-2026-11-23.md (GA4/GSC week tables; VDP most-viewed rows)
- brain/STATE.md (TRAPS, target queue)
- doctrine/BRAND-FACTS.json, BRAND-CORE.md (phone, address, 1937)
- Live fetches 2026-11-24: /used-inventory (current copy), all outbound hrefs HTTP 200

## [NEEDS-VERIFY] list
1. [NEEDS-VERIFY: re-verify the two VDP URLs return 200 on the day DealerOn publishes; swap to whatever the current top used VDPs are at publish time.]
2. [NEEDS-VERIFY: synthesis says 16 clicks/572 impr pos 9.3; audit table says 12/580 pos 10.9 - same page, different pulls. Confirm which GSC pull is canonical before quoting externally.]

## Fresh-eyes reader
(filled after the pass; see PACKAGE.md / adversarial report)

## 3 approval questions for Spencer
1. Copy OK as the replacement custom section on /used-inventory (listings module untouched)?
2. Keep or cut the 'most-viewed this week' sentence naming the two VDPs? (Keeps the page concrete; ages fast.)
3. OK for the DealerOn request to also add the three inbound links listed above from the maintenance and trim-levels pages?
