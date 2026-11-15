# REVIEW: heavy-duty-vs-light-duty-trucks

Status: `draft-needs-owner-approval`
Draft: `content/drafts/seo/heavy-duty-vs-light-duty-trucks-draft.html`

## Competitor gap and page-vs-blog decision

Phase 1 used the approved fallback because no reliable top three could be extracted. The production blog has unrelated tire copy under its heavy-duty definition, unsourced capability ranges, and no payload-budget explanation. The draft supplies direct everyday-use and real-world-capability answers, defines ratings, explains hitch weight, and gives an exact-truck checklist.

**Build the dedicated page.** The intent is an evergreen comparison and decision resource. Keep the blog as a supporting article; do not redirect or canonicalize it in Phase 2. A separate page gives the durable answer asset clean question structure and sourced tables/checks, while the broken blog can be repaired later without preserving its errors.

## Metadata

- Title: `Heavy-Duty vs. Light-Duty Trucks for Daily Use`
- Meta description: `Compare light-duty and heavy-duty trucks for daily driving, payload, towing, hitch weight, and exact-truck rating checks before you buy.`
- Slug: `heavy-duty-vs-light-duty-trucks`
- Primary query: `how does a light duty full size truck compare to a heavy duty model for everyday use`

## Internal-link plan and HTTP proof

| Already-ranking source page | Proposed anchor | Target href / gate | Proof (2026-11-15) |
|---|---|---|---|
| `/blog/heavy-duty-vs-light-duty-trucks` | `compare light-duty and heavy-duty trucks for real loads` | New page after deployment; source currently curl `200` | Source `200`; do not add until new href returns `200` |
| `/vehicle-trim-levels-explained` | `check the truck's exact configuration and ratings` | New page after deployment; source currently curl `200` | Source `200`; do not add until new href returns `200` |
| `/car-maintenance-by-mileage` | `light-duty versus heavy-duty daily use` | New page after deployment; source currently curl `200` | Source `200`; do not add until new href returns `200` |

The only href placed in this draft, `https://www.motorinnautogroup.com/searchall.aspx`, returned curl `200`. The not-yet-deployed canonical cannot honestly be recorded as `200`; the insertion gate explicitly requires a curl `200` before links are added.

## Sources and every-number map

- 2026 F-150: 13,500-lb maximum towing and 2,440-lb maximum payload: https://www.ford.com/trucks/f150/features/payload-trailering/ (curl `200`)
- 2026 Super Duty: 40,000-lb maximum gooseneck towing and 8,000-lb maximum payload: https://www.ford.com/trucks/super-duty/2026/specs/ (curl `200`)
- 2026 Ford tow guide: 10% conventional tongue load; 15% fifth-wheel/gooseneck pin load; payload/GAWR/GVWR qualifications: https://www.ford.com/content/dam/brand_ford/en_us/brand/towing/pdf/2026-Ford-RV-and-Trailer-Towing-Guide-v3.pdf (curl `200`)
- Model-number families 150/1500, 250/2500, and 350/3500 are naming examples, not capability claims. No GM or Ram specification is stated in this draft.

## NEEDS-VERIFY

Count from pre-flight grep: **0**.

## Approval questions for Spencer

1. Do you approve the dedicated-page decision while retaining the blog as a supporting URL?
2. Is the Ford-only worked capability comparison acceptable, or do you want parallel GM and Ram maximums added after configuration-level review?
3. Should the one CTA remain all inventory or point to used trucks once the exact filter is verified?
