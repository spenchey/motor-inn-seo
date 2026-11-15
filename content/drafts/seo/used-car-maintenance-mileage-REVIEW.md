# REVIEW: used-car-maintenance-mileage

Status: `draft-needs-owner-approval`
Draft: `content/drafts/seo/used-car-maintenance-mileage-draft.html`

## Competitor gap and 10x result

Phase 1 used the approved fallback after SERP extraction failed. Generic publishers often promise a lifespan range, while service pages turn mileage milestones into universal replacement lists. This draft answers that there is no fixed failure mileage, makes the exact manufacturer schedule primary, separates inspection from replacement, adds Iowa corrosion context, and refuses to borrow MotorHappy advice without a source. All Motor Inn process claims remain flagged as ordered.

## Metadata

- Title: `How Long Can a Car Last? High-Mileage Checklist`
- Meta description: `There is no fixed breakdown mileage. Use service records, the owner's maintenance schedule, condition, warning signs, and an inspection to judge a car.`
- Slug: `used-car-maintenance-mileage`
- Primary query: `how many miles can a car last before it breaks down`

## Internal-link plan and HTTP proof

| Already-ranking source page | Proposed anchor | Target href / gate | Proof (2026-11-15) |
|---|---|---|---|
| `/car-maintenance-by-mileage` | `how to judge a high-mileage used car` | New page after deployment | Source curl `200`; add only after target curl `200` |
| `/blog/maintenance-tips-for-high-mileage-vehicles` | `high-mileage maintenance and inspection checklist` | New page after deployment | Source curl `200`; add only after target curl `200` |
| `/aboutus.aspx` | `shop used cars with records and inspection details` | New page after deployment | Source curl `200`; add only after target curl `200` |

Draft CTA href `https://www.motorinnautogroup.com/searchused.aspx` returned curl `200` and resolved to `https://www.motorinnautogroup.com/used-inventory` with final HTTP `200`. The new canonical is correctly gated rather than described as deployed.

## Sources and every-number map

- The 60,000-, 90,000-, 100,000-, 150,000-, and 200,000-mile values are shopper-proposed review points from the query outline, not service recommendations. Toyota’s official schedule tool supports using the vehicle-specific factory schedule: https://www.toyota.com/owners/maintenance-schedule
- Toyota explains that exact maintenance comes from its Warranty and Maintenance Guide and that intervals depend on the vehicle: https://support.toyota.com/s/article/How-often-should-I-ma-10042?language=en_US
- Toyota guidance for maintenance beyond 120,000 miles says to continue the guide’s described interval pattern rather than use a universal end point: https://support.toyota.com/s/article/My-maintenance-guide-7903?language=en_US
- No public lifespan number appears in the draft.

## NEEDS-VERIFY

Count from pre-flight grep: **4**.

1. Identify the MotorHappy source behind the query and confirm whether it can be summarized.
2. Confirm whether every used vehicle receives a documented inspection and name the checklist.
3. Confirm which safety, maintenance, cosmetic, recall, history-report, and road-test steps apply to every vehicle versus only some vehicles.
4. Confirm who performs used-vehicle work and which records a shopper may review.

## Approval questions for Spencer

1. What is the exact, owner-approved used-vehicle inspection and reconditioning process?
2. Should MotorHappy be named only to clarify the query mismatch, or removed unless its source is found?
3. Should the single CTA go to used inventory or to a verified service/inspection contact flow?
