# MOT-3708 approval package — used-inventory refresh + Carroll cluster (2026-11-24)

Status: DRAFTS ONLY — draft-needs-owner-approval on every page. No publish, no DealerOn send, no emails sent (04_dealeron_email_draft.txt files are request drafts for Spencer to approve and send).

## What is in the package

| Page | Slug | Action | Draft | page_gate.py (round 3) | Codex adversarial |
|---|---|---|---|---|---|
| Used inventory refresh | /used-inventory | Replace custom intro section only; listings module untouched | content/drafts/seo/used-inventory-refresh.md | PASS (exit 0, 2026-11-24) | round 2 FAIL -> round 3 fixes -> see brain/reports/ |
| Used SUVs refresh | /used-suvs | Replace custom intro section only; listings module untouched | content/drafts/seo/used-suvs-refresh.md | PASS | same |
| Car dealerships Carroll refresh | /car-dealerships-carroll-iowa | Full custom-content replacement; corrects live phone (712-522-2526) and "since 1934" defects | content/drafts/seo/car-dealerships-carroll-iowa-refresh.md | PASS | same |
| Used car dealer Carroll (new) | /used-car-dealer-carroll-iowa | New page (URL returned 404 on 2026-11-24; confirm slug with DealerOn) | content/drafts/seo/used-car-dealer-carroll-iowa.md | PASS | same |

Per-page bundle for DealerOn: bundle/<slug>/{01_placement_note.txt, 02_fragment.html, 03_metadata.json, 04_dealeron_email_draft.txt}. Metadata: titles 53-56 chars, descriptions 138-147 chars (adversarial-verified). Round-2 fragments preserved as bundle/<slug>/02_fragment.html.bak-r2; round-1 bundles in _bundle-r1/.

## Why (data of record)
- /used-inventory: pos 9.3, 16 clicks / 572 impressions (GSC week Nov 9-15, synthesis); 1,330 views, 171s avg; used_vdp conv 1,849; organic bounce 0.4%; mobile 71% of sessions.
- 'carroll iowa car dealerships' cluster: pos 10.6, 14 clicks / 49 impr; /car-dealership-carroll-iowa 2,337s avg time proves the format.
- TRAPS respected: no investment in /searchused.aspx, /service-area, leadless blog posts (brain/STATE.md).
- Discrepancy flagged [NEEDS-VERIFY]: audits/audit-2026-11-23.md top-pages table shows 12 clicks / 580 impr / pos 10.9 for /used-inventory - confirm which GSC pull is canonical.

## Queue coordination
Folded into the wave-2 queue (register rows F-all-page-draft-unpublished-f6f160 / -7c7f82): this batch joins the same owner ask; nothing duplicated (content/drafts/seo/QUEUE.md, committed).

## QA trail
1. Round 1: drafts + page_gate PASS (commit 352b0cd).
2. Round 2: codex editorial review + adversarial FAIL (claims, voice, 16 broken link occurrences — report brain/reports/mot3708-used-carroll-2026-11-24-codex-adversarial-2026-11-24.md, commit 310f652).
3. Round 3: unsupported claims cut (every cut quoted in the REVIEW packets), broken links replaced with verified live URLs (each re-fetched 2026-11-24), VOICE-DNA short-sentence pass, fresh-eyes reader (GLM-5.3-Flash): 17 findings, 11 fixed, 6 left (documented in used-inventory-refresh-REVIEW.md). page_gate PASS x4.
4. Codex adversarial re-run on round 3: <PENDING — fill with report path and verdict before this goes to Spencer>.

## Decisions Spencer owns (3 per page, in each REVIEW packet)
1. Copy OK for the live page replacement (listings module untouched)?
2. Keep or cut the dated "most-viewed vehicles (Nov 9-15)" VDP section?
3. OK for the DealerOn request to add the planned inbound links from already-ranking pages (/car-maintenance-by-mileage, /vehicle-trim-levels-explained)?

Nothing goes live without Spencer's approval.
