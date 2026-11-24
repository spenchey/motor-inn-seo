# REVIEW PACKET — used-car-dealer-carroll-iowa (MOT-3708 item 2, NEW page)

Batch: mot3708-used-carroll-2026-11-24 | Draft: content/drafts/seo/used-car-dealer-carroll-iowa.md
Status: draft-needs-owner-approval. Action: NEW page at /used-car-dealer-carroll-iowa (URL returned 404 on 2026-11-24).

## Why this page (queue row)
AI-answer gap: 'best used car dealer carroll iowa' returns 4 competitor citations and zero Motor Inn (brain/ai-visibility/ai-vis-2026-11-23.md, WE: 0 of 4; same 0/4 in the 11-16 and 11-09 runs). The synthesis (2026-11-23) directs local-intent cluster expansion off the proven /car-dealership-carroll-iowa format. Our title deliberately avoids 'best' (title-superlative gate rule); the page earns the citation by answering the dealer-choice question.
Dedup boundary (checked before drafting): /used-cars-carroll-iowa (wave-1 draft, inventory-browse intent, unpublished), /best-place-to-buy-used-car-carroll-iowa (wave-1 geo-answer draft, unpublished), /used-inventory (live SRP), /car-dealership-carroll-iowa (live 'which dealership' page, brand-agnostic across new+used). This page is the used-side dealer-choice answer: dealer vs independent lot, what to ask any used dealer, and the live list as proof. No URL or H1 collision.

## Competitor gap (10x method)
Cited rivals for the query (ai-vis-2026-11-23): Car Stop LLC, Choice Auto, Wittrock Motor Company, Pro Auto Sales & Service - all independents. Gap none of them can copy: a used lot attached to both new franchises with service/parts on-site, a trade appraisal lane and a doc-fee-inclusive listed price. The draft states those as checkable facts and ends every section with the shopper's next step.

## Metadata
- Title (55 chars): Used Car Dealer in Carroll, Iowa | Motor Inn Auto Group
- Meta description (147 chars): Used car dealer in Carroll, Iowa: used cars, trucks and SUVs at Motor Inn Auto Group, 1526 Le Clark Rd, with service on the same lot. 712-792-5000.
- Canonical slug: /used-car-dealer-carroll-iowa

## Claim contract
May say (sourced): address/phone/51401 (BRAND-FACTS.json); used inventory lives at /used-inventory with per-vehicle price cards (verified 200, 2026-11-24); body-style lists exist (all 200); two named most-viewed VDPs week Nov 9-15 (audit-2026-11-23.md; 200 on 2026-11-24); 'service and parts departments on the same lot' (live nav Service & Parts Locations; Motor Inn is a full-line dealership - also GBP category Toyota dealer, STATE.md NAP check); trade/finance/payment-calc/test-drive paths (200); doc-fee-inclusive pricing (brand kit v2.2); towns served (VOICE-DNA).
Must not say: 'best', '#1', rival names with verdicts, reconditioning/inspection process specifics we haven't sourced from ops ('multi-point inspection' claim is NOT made - only 'service or reconditioning records for that exact unit' as something the shopper may ask for), days-on-lot or pressure wording.
Needs checking first: DealerOn confirmation that /used-car-dealer-carroll-iowa is the slug they will build (BRAND-FACTS.json: never invent a landing URL; use the URL DealerOn confirms); doc-fee sentence verified against the live VDP disclaimer; VDP link freshness at publish.

## Internal-link plan
Outbound (200 on 2026-11-24): /used-inventory, /used-cars, /used-suvs, /used-trucks, /used-vans, /under-20000, two VDPs, /trade.aspx, /finance-locations.html, /paymentcalc.aspx, /testdrive.aspx?type=Used, /hours.aspx.
Inbound FROM ranking pages (anchors for DealerOn): /used-inventory refresh anchor 'what to ask a used car dealer' -> new page; /car-dealer-comparison-carroll-iowa.html (1,592s avg engagement) anchor 'used car dealer in Carroll' -> new page; /car-maintenance-by-mileage anchor not pitched here to avoid over-linking one source page (it already links the used-inventory refresh).

## Sources
- brain/ai-visibility/ai-vis-2026-11-23.md (0/4 gap, rival citations - evidence only, rivals not named in the customer copy)
- brain/competitor-read-2026-09-23.md; audits/audit-2026-11-23.md; brain/STATE.md NAP check
- doctrine/BRAND-FACTS.json; motorinn-brand-kit v2.2; brain/VOICE-DNA.md
- Live fetches 2026-11-24: slug 404 check; all outbound hrefs HTTP 200

## [NEEDS-VERIFY] list
1. [NEEDS-VERIFY: DealerOn confirms slug /used-car-dealer-carroll-iowa before publish.]
2. [NEEDS-VERIFY: confirm live VDP price disclaimer wording matches the $180-doc-fee sentence.]
3. [NEEDS-VERIFY: re-verify both VDP URLs at publish time.]


## Round 3 fixes (2026-11-24, after codex adversarial FAIL round 2)
Round-2 adversarial report: brain/reports/mot3708-used-carroll-2026-11-24-codex-adversarial-2026-11-24.md (verdict FAIL, all 4 pages). Fixes applied in round-3 draft (editorial_round: 3):
- Links: the round-2 link-verification claim was WRONG (see used-inventory REVIEW). /used-suvs, /used-trucks, /used-vans, /under-20000 return 404. Round 3 uses /searchused.aspx?BodyStyle=SUV|Truck|Van and /under-20k.html - re-fetched 2026-11-24, final HTTP 200.
- Claims cut (codex-quoted): "A dealership handles more of the purchase in one place." and "An independent lot can sell you a vehicle; most cannot service it." - the dealership-vs-independent comparison section was rewritten as "What does buying from Motor Inn include?" (only sourced capabilities, no comparison).
- Voice: long sentences split; "the whole purchase" softened to "the purchase happens on one lot"; editor-caveat and sermon lines trimmed (fresh-eyes).
- page_gate.py round 3: PASS (exit 0), 2026-11-24.

## Fresh-eyes reader
fresh-eyes reader (GLM-5.3-Flash on spark-a664:8888, brief+draft only, 2026-11-24): 17 findings across the batch, 11 fixed, 6 left (see used-inventory REVIEW for the six).

## 3 approval questions for Spencer
1. Approve this as the new used-side dealer-choice page?
2. 'How is a dealership different from an independent used lot?' answers without naming rivals - keep that framing?
3. Want an FAQPage JSON-LD derived from the five question H2s at build time (as the wave-2 pages carried), or is the plain DealerOn page enough?
