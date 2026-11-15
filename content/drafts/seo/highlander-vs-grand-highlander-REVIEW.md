# REVIEW: highlander-vs-grand-highlander

Status: `draft-needs-owner-approval`
Draft: `content/drafts/seo/highlander-vs-grand-highlander-draft.html`

## Competitor gap and 10x result

The phase-1 audit found that the current page delays the answer, mixes model years, and makes unsourced comfort, inventory, fuel-economy, and price claims. The old package had duplicate IDs, malformed headings, and no computed deltas. This rewrite answers “yes” in sentence one, uses one model year, computes six useful differences, separates measurement from preference, removes availability promises, and keeps visible FAQ content aligned with schema.

## Metadata

- Title: `Highlander vs. Grand Highlander Size Comparison`
- Meta description: `See exactly how much bigger the 2026 Grand Highlander is than the Highlander, including length, wheelbase, cargo room, and third-row space.`
- Slug: `highlander-vs-grand-highlander`
- Primary query: `is the grand highlander bigger than the highlander`

## Internal-link plan and HTTP proof

| Already-ranking source page | Proposed anchor | Target href | Proof (2026-11-15) |
|---|---|---|---|
| `/vehicle-trim-levels-explained` | `Highlander and Grand Highlander size comparison` | `https://www.motorinnautogroup.com/highlander-vs-grand-highlander` | curl `200` |
| `/aboutus.aspx` | `compare Highlander and Grand Highlander dimensions` | `https://www.motorinnautogroup.com/highlander-vs-grand-highlander` | curl `200` |
| `/car-maintenance-by-mileage` | `see the Highlander size differences` | `https://www.motorinnautogroup.com/highlander-vs-grand-highlander` | curl `200` |

Draft CTA href `https://www.motorinnautogroup.com/searchall.aspx` returned curl `200`.

## Sources and every-number map

- 2026 Highlander: 194.9-in. length, 112.2-in. wheelbase, 28.0-in. third-row legroom, 16.0/48.4/84.3-cu.-ft. cargo, and up-to-8 seating: https://www.toyota.com/highlander/features/dimensions/6953/6956/ (curl `200`)
- 2026 Grand Highlander: 201.4-in. length, 116.1-in. wheelbase, 33.5-in. third-row legroom, 20.6/57.9/97.5-cu.-ft. cargo, and up-to-8 seating: https://www.toyota.com/grandhighlander/features/dimensions/6716/6724/6732/ (curl `200`; Toyota may roll the selector forward, so recheck model-year label at approval)
- Computed deltas from those OEM values: 6.5 in., 3.9 in., 5.5 in., 4.6 cu. ft., 9.5 cu. ft., and 13.2 cu. ft.

## NEEDS-VERIFY

Count from pre-flight grep: **0**.

## Approval questions for Spencer

1. Do you want this rewrite kept strictly to size, or should a separately sourced powertrain/towing section return?
2. Is “sit in both rows” acceptable advice without implying both models are currently in stock?
3. Should the CTA remain all inventory until stable model filters are confirmed?
