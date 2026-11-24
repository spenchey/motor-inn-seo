# REVIEW PACKET — used-suvs-refresh (MOT-3708 item 1)

Batch: mot3708-used-carroll-2026-11-24 | Draft: content/drafts/seo/used-suvs-refresh.md
Status: draft-needs-owner-approval. Action: REPLACE the custom content section of the live /used-suvs page; the DealerOn inventory listings module stays untouched.

## Why this page, why now (queue row)
Companion row to the /used-inventory NOW item in the 2026-11-23 synthesis: /used-suvs drew 119 views / 39 users / 125s avg (GA4 week Nov 9-15, audits/audit-2026-11-23.md) and sat at pos 23.5 in the 2026-09-23 baseline (brain/STATE.md) - a refresh of buyer-intent copy on an already-used page, which the 'fix before write' rule favors. Same TRAPS discipline as item 1: no links to trap URLs.

## Competitor gap (10x method)
SERP/AI read for used-SUV and used-dealer queries (brain/competitor-read-2026-09-23.md, brain/ai-visibility/ai-vis-2026-11-23.md) shows generic 'quality used SUVs' filler. Gaps exploited: size-choice guidance (compact/midsize/three-row mapped to Iowa use - winter AWD, lake towing), named current units as proof, the $180-doc-fee price-transparency answer block, and one CTA (call or test drive) instead of competing CTAs.

## Metadata
- Title (56 chars): Used SUVs for Sale in Carroll, IA | Motor Inn Auto Group  [unchanged from live]
- Meta description (142 chars): Used SUVs and crossovers for sale in Carroll, IA. Compare the current list at Motor Inn Auto Group and set up a test drive. Call 712-792-5000.
- Canonical: /used-suvs (unchanged)

## Claim contract
May say (sourced): SUV/crossover stock list lives on the page (live behavior, 200 on 2026-11-24); address, phone, 1937 lineage (BRAND-FACTS.json / BRAND-CORE.md); the two named VDPs as 'recent examples on the lot' (GA4 most-viewed week Nov 9-15; URLs 200 on 2026-11-24); 'price shown on our vehicle pages includes the $180 doc fee' (motorinn-brand-kit facts rule; brand kit v2.2 adopted 2026-11-03); trade, financing, payment calculator, test-drive paths (URLs 200 on 2026-11-24); under-$20,000 list exists (/under-20000, 200).
Must not say: specific towing/payload numbers for an unnamed unit, condition or history claims for a vehicle not quoted from its records, 'AWD available now' as a stock promise, aging/popularity pressure, any other phone number.
Needs checking first: doc-fee sentence against the exact live VDP price disclaimer DealerOn renders (confirm the site really shows price including the $180 doc fee, not +fee); VDP link freshness at publish.

## Internal-link plan
Outbound (all 200 on 2026-11-24): the two VDPs, /new-suvs, /under-20000, /paymentcalc.aspx, /finance-locations.html, /trade.aspx, /testdrive.aspx?type=Used.
Inbound FROM ranking pages (anchors for DealerOn): /used-inventory refresh (this batch) anchors 'used SUVs' / 'used crossovers'; /car-dealerships-carroll-iowa refresh (this batch) anchor 'used SUVs'; /vehicle-trim-levels-explained anchor 'compare used SUV trims on the lot' -> /used-suvs.

## Sources
- findings/reports/digital-synthesis-2026-11-23.md; audits/audit-2026-11-23.md; brain/STATE.md
- motorinn-brand-kit v2.2 (doc-fee fact, phone, 1937)
- Live fetches 2026-11-24: /used-suvs current copy; all hrefs HTTP 200

## [NEEDS-VERIFY] list
1. [NEEDS-VERIFY: confirm the live VDP price disclaimer shows the price including the $180 doc fee exactly as the brand kit states before the doc-fee sentence ships.]
2. [NEEDS-VERIFY: re-verify the two VDP URLs return 200 at publish time.]

## Fresh-eyes reader
(filled after the pass; see PACKAGE.md / adversarial report)

## 3 approval questions for Spencer
1. Copy OK as the replacement custom section on /used-suvs?
2. Is the $180-doc-fee sentence something you want stated on inventory pages, or trimmed to 'full price in writing'?
3. OK to name the RAV4 Hybrid and Grand Highlander Hybrid as recent examples, with the publish-time freshness check?
