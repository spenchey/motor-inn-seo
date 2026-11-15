# REVIEW: vehicle-trim-levels-explained

Status: `draft-needs-owner-approval`
Draft: `content/drafts/seo/trim-levels-explained-draft.html`

## Competitor gap and 10x result

Phase 1 found no reliable extractable SERP top three, so this uses the directive-approved flagged-query and existing-page fallback. The old page blurred model, trim, and package; treated changing trim names as a universal ladder; omitted the truck intent; and lacked trustworthy SofTex treatment. This rewrite adds a plain definition in sentence one, model/trim/package distinctions, truck-specific caution, Toyota-verified SofTex wording, a used-car identification checklist, question headings, and visible FAQ answers. It avoids capability advice based on badges.

## Metadata

- Title: `Vehicle Trim Levels Explained: Cars and Trucks`
- Meta description: `Learn what a vehicle trim level means, how trims differ from models and packages, and how to compare upholstery and features by model year.`
- Slug: `vehicle-trim-levels-explained` (preserves `/vehicle-trim-levels-explained`)
- Primary query: `what is a trim level on a car`

## Internal-link plan and HTTP proof

Add links **from** these already-ranking pages after the rewrite is approved:

| Source page | Proposed anchor | Target href | Proof (2026-11-15) |
|---|---|---|---|
| `/highlander-vs-grand-highlander` | `compare model and trim before you choose` | `https://www.motorinnautogroup.com/vehicle-trim-levels-explained` | curl `200` |
| `/blog/heavy-duty-vs-light-duty-trucks` | `what a truck trim level means` | `https://www.motorinnautogroup.com/vehicle-trim-levels-explained` | curl `200` |
| `/car-maintenance-by-mileage` | `verify a used vehicle's exact trim` | `https://www.motorinnautogroup.com/vehicle-trim-levels-explained` | curl `200` |

Draft CTA href proof: `https://www.motorinnautogroup.com/searchall.aspx` returned curl `200` with no redirect.

## Sources and number map

- 2026 RAV4 upholstery terminology and grade-level fabric/SofTex listings: https://www.toyota.com/rav4/features/interior/ (curl `200` on 2026-11-15)
- 2026 RAV4 brochure, including SofTex and synthetic-suede wording: https://www.toyota.com/content/dam/toyota/brochures/pdf/2026/2026_rav4_brochure_20260612_142557.pdf
- Trim/series as pre-packaged equipment levels (general definition): Kelley Blue Book values FAQ, https://www.kbb.com/faq/values/ (fetched 2026-11-15)
- Used-vehicle trim confirmation via Buyers Guide, window sticker, and VIN: FTC, "Buying a Used Car From a Dealer", https://consumer.ftc.gov/articles/buying-used-car-dealer (fetched 2026-11-15)
- Truck capability does not follow the trim name alone; configuration and labels rule: Ford RV and Trailer Towing Guide, https://www.ford.com/content/dam/brand_ford/en_us/brand/towing/pdf/2026-Ford-RV-and-Trailer-Towing-Guide-v3.pdf (curl `200`)
- Query evidence and impression counts used only in planning: `brain/reports/longtail-answers-2026-11-14.md`; no impression number appears in the public draft.

## Wave 2 fix pass (2026-11-15)

- On-page "Related guides" links repointed to live equivalents and re-verified curl `200`: `/2022-toyota-rav4-carroll-ia` and `/blog/heavy-duty-vs-light-duty-trucks` (both 2026-11-15).
- "this draft" production phrase removed from the SofTex paragraph.

## NEEDS-VERIFY

Count from pre-flight grep: **0**.

## Approval questions for Spencer

1. Is “equipment version” the clearest owner-approved definition, or do you prefer “equipment tier”?
2. Should the page keep Toyota’s “grade” terminology alongside the more common “trim” wording?
3. Is the single CTA to all inventory right, or should it point to a specific comparison workflow?
