# GBP Structural Audit — 2026-08-03

## Executive Summary
- This week's run recovered live public Google Maps views for Motor Inn, Champion Ford, Wittrock Motor Company, Spirit Lake Ford - Chrysler - Dodge - Jeep - Ram, and Okoboji Motor Company. That is better than July's scrape failures, but Google still hides most edit-level GBP fields unless the profile is opened in an admin or signed-in view.
- The biggest public gap is profile richness. Champion Ford shows a visible attribute badge and an owner post, Coleman shows a current owner post and a test-drive CTA, and Okoboji shows a booking CTA. Motor Inn's public listing mainly shows the Toyota dealer profile plus linked Chevrolet, Buick, and parts sub-listings at the same address.
- Next, Spencer should use the dated draft files from this run to tighten categories, service descriptions, and photo uploads inside GBP, then confirm the hidden fields that public Maps still does not expose.
- Spencer needs to decide whether to keep leaning on the sales-led store profile or add a stronger service-led listing setup. Today's competitor signals still favor stores that surface service or booking actions directly in Google.

## Data Collection Status
| Source | Status | Notes |
|---|---|---|
| EXA research | Yes | `gbp-research-2026-08-03.json` saved successfully |
| Motor Inn Toyota/Chevrolet public GBP | Yes | Public limited view scraped successfully |
| Motor Inn Chevy/Buick/GMC search results | Yes | Search results and linked sub-listings scraped successfully |
| Champion Ford public GBP | Yes | Public limited view scraped successfully |
| Wittrock Motor Company public GBP | Yes | Public limited view scraped successfully |
| Spirit Lake Ford - Chrysler - Dodge - Jeep - Ram public GBP | Yes | Public limited view scraped successfully |
| Okoboji Motor Company public GBP | Yes | Public limited view scraped successfully |
| GBP share link scrape | Partial | Share-link retry failed with Firecrawl proxy tunnel error |
| Local Spark (`qwen3.6:35b-a3b`) | No | Requested Spark host was unreachable from this runner |

**Important note:** Today's comparison is grounded to the public Google Maps pages Firecrawl could load. Those pages reliably exposed names, primary categories, hours, addresses, phone numbers, website/deep links, a few badges or CTAs, and some post snippets. They did **not** expose secondary categories, full attribute sets, services lists, full descriptions, or total photo counts for most listings.

## Categories

### Visible Category Comparison
| Category | Motor Inn | Champion Ford | Wittrock | Coleman | Okoboji Motor Company |
|---|---|---|---|---|---|
| Toyota dealer | Primary on combined store | — | — | — | — |
| Chevrolet dealer | Linked sub-listing at same address | — | — | — | — |
| Buick dealer | Linked result at same address | — | — | — | — |
| Auto parts store | Linked sub-listing at same address | — | — | — | — |
| Ford dealer | — | Primary | — | — | — |
| Car dealer | — | — | Primary | Primary | Primary |

### What Matters
- Motor Inn's public combined listing surfaces as **Toyota dealer**, which is good for Toyota intent.
- Motor Inn's search results also surface **Chevrolet dealer**, **Buick dealer**, and **Auto parts store** at the same Carroll address, which confirms Google already understands multiple dealership functions at this location.
- No public **GMC** category signal surfaced today.
- Three competitor listings still surface with the generic **Car dealer** primary category instead of a make-specific one.

### Missing Categories (Prioritized)
- `P1`: Confirm that the Chevy/Buick/GMC store has a live **GMC dealer** category signal in GBP. It did not surface publicly today.
- `P1`: Confirm that both Motor Inn stores use all relevant secondary categories in GBP admin. Public Maps did not expose them, so this is an admin check, not a guessed gap.
- `P2`: If not already set in GBP admin, verify and add service-led secondary categories aligned with today's EXA benchmark set: `Used Car Dealer`, `Auto Repair Shop`, `Oil Change Service`, `Tire Shop`, `Car Finance and Loan Company`, `Truck Dealer`, and `Auto Parts Store`.
- `P3`: Only keep categories that match a real on-site function. The EXA benchmark still supports full category coverage, but irrelevant categories dilute relevance.

## Attributes

### Visible Attribute Comparison
| Attribute / signal | Motor Inn | Champion Ford | Wittrock | Coleman | Okoboji Motor Company |
|---|---|---|---|---|---|
| Visible attribute badge | No public badge seen | `LGBTQ+ friendly` badge visible | No public badge seen | No public badge seen | No public badge seen |
| Booking CTA on GBP | No | No | No | No | `Book online` visible |
| Service or appointment deep link visible from GBP | No deep service link on public page | `service-appointment` link visible | No | No | Booking link points to service scheduling |
| Test-drive CTA visible from GBP | No | No | No | `testdrive.aspx` link visible | No |
| Owner post visible | No | Yes, dated Feb 27, 2026 | No | Yes, dated Jul 9, 2026 | No |

### What Matters
- Champion Ford and Coleman both expose more active public signals than Motor Inn today.
- Okoboji's `Book online` button is the clearest service-action gap in the comparison set.
- Standard GBP attributes such as financing, trade-in, Wi-Fi, accessibility, and service amenities were not exposed in today's public view for most listings.

### Missing Attributes (Prioritized)
- `Table stakes`: Add or verify a public-facing booking or service-action path if GBP supports it for Motor Inn's service workflow. Okoboji already surfaces one.
- `Table stakes`: Keep an owner post live. Champion and Coleman both show public post activity; Motor Inn did not surface one today.
- `Strong rec`: Confirm in GBP admin that Motor Inn has all accurate operational attributes turned on, especially financing, test drives, trade-ins, service department, parts department, and online appointments where supported.
- `Differentiator`: Add accessibility and waiting-area amenities only if true on site. Public Maps did not expose them today, so these need admin verification.

## Services

### Website vs Public GBP Comparison
| Service / offer | Motor Inn | Champion Ford | Wittrock | Coleman | Okoboji Motor Company |
|---|---|---|---|---|---|
| Service scheduling | Website has `Schedule Service` for Toyota and Chevy stores; not visible on public GBP | Visible service-appointment deep link | Not visible | Not visible | Visible booking CTA |
| Parts department | Website has parts center links; parts sub-listing also surfaced in Google results | Not visible | Not visible | Not visible | Not visible |
| Test drive | Website has test-drive pages for new and used inventory | Not visible | Not visible | Visible test-drive deep link | Not visible |
| Finance / trade | Website has finance locations and trade appraisal | Not visible | Not visible | Financing promo visible in owner post | Not visible |
| Service center | Website has Toyota and Chevy service center links | Not visible | Not visible | Not visible | Implied by booking CTA, not listed as text |
| New / used vehicle sales | Website clearly exposes new and used inventory sections | Inventory promo visible in owner post | Not visible in public GBP | New-inventory post visible | Not visible in public GBP |

### Services Missing From Public GBP
- Service scheduling
- Parts center description
- Service center description
- Test-drive description
- Finance / trade-in description
- New vehicle sales description
- Used vehicle sales description

### Services Needing Better Descriptions
- Every Motor Inn service that exists on the website but does not surface with useful copy in public GBP today.

### Draft Output
- Dated service descriptions saved to `~/motor-inn-seo/content/drafts/gbp-services/services-2026-08-03.md`

## Description

### Comparison Table
| Business | Public description visible today | Category signal | Service-area signal | Trust or action signal | Recommendation |
|---|---|---|---|---|---|
| Motor Inn | No full GBP description visible | Toyota dealer + linked Chevy/Buick/parts results | Carroll address visible; website also references Carroll County and surrounding communities | Website headline says "Your Trusted Chevrolet & Toyota Dealership in Carroll, Iowa" and says Motor Inn has served the area for over 85 years | Rewrite and publish a fuller GBP description |
| Champion Ford | No full description visible | Ford dealer | Carroll address visible | Attribute badge + owner post + service deep link | Stronger public activity than Motor Inn |
| Wittrock | No full description visible | Car dealer | Carroll address visible | Minimal public signals | Generic |
| Coleman | No full description visible | Car dealer | Spirit Lake address visible | Current owner post + test-drive CTA | Strong public conversion cues |
| Okoboji Motor Company | No full description visible | Car dealer | Spirit Lake address visible | Booking CTA | Strong service-action cue |

### Current Motor Inn Description Signal
- The full GBP description did not surface in today's public Google Maps view.
- The current website hero copy is the strongest available source for replacement language: Motor Inn is a trusted Chevrolet and Toyota dealership in Carroll, Iowa serving Carroll County and surrounding communities with new vehicles, used cars, and dependable service for over 85 years.

### Recommendation
- Rewrite the GBP description now. Public Maps did not show enough brand, service, trust, or service-area detail for Motor Inn.
- Dated description drafts saved to `~/motor-inn-seo/content/drafts/gbp-description/description-2026-08-03.md`

## Photos

### Visible Public Photo Signals
| Metric | Motor Inn | Champion Ford | Wittrock | Coleman | Okoboji Motor Company |
|---|---|---|---|---|---|
| Lead image visible | Yes | Yes | Yes | Yes | Yes |
| Photos module visible | Yes | Yes | Yes | Yes | No dedicated module shown, only add-photo prompt |
| Public photo count visible | No | No | No | No | No |
| Dated owner media or post visible | No | Yes, Feb 27, 2026 | No | Yes, Jul 9, 2026 | No |
| Public freshness signal | Weak | Better than Motor Inn | Weak | Best in this set today | Moderate due to booking CTA, not photos |

### What Matters
- Public photo counts are still hidden, so today we cannot confirm exact totals or last-30-day upload counts from the public view alone.
- Competitors with visible public activity also show stronger action cues.
- Motor Inn needs a predictable weekly upload rhythm regardless of the hidden count.

### Upload Plan Summary
- Upload **6 photos per week for 4 weeks**: 3 sales/inventory, 2 service/parts, 1 people/community.
- Dated photo plan saved to `~/motor-inn-seo/content/drafts/gbp-photos/photo-plan-2026-08-03.md`

## Action Items (This Week)
1. Add or verify a service-action path in GBP for Motor Inn. Okoboji already exposes booking and Champion exposes a service appointment link.
2. Publish one fresh owner post this week. Champion and Coleman both surfaced public post activity; Motor Inn did not.
3. Paste the dated service descriptions and one of the dated GBP descriptions from this run into GBP admin.
4. Confirm the hidden category and attribute fields inside GBP admin for both Motor Inn store profiles, especially GMC visibility and all service-related secondary categories.
5. Start the four-week photo plan immediately and keep the naming convention and geotagging rules intact.

## Sources
- `~/motor-inn-seo/audits/gbp-structural/gbp-research-2026-08-03.json`
- `~/motor-inn-seo/.firecrawl/gbp-structural/motor_inn_combined.json`
- `~/motor-inn-seo/.firecrawl/gbp-structural/motor_inn_chevy.json`
- `~/motor-inn-seo/.firecrawl/gbp-structural/champion_ford.json`
- `~/motor-inn-seo/.firecrawl/gbp-structural/wittrock.json`
- `~/motor-inn-seo/.firecrawl/gbp-structural/coleman.json`
- `~/motor-inn-seo/.firecrawl/gbp-structural/okoboji_toyota.json`
- `~/motor-inn-seo/.firecrawl/gbp-structural/motorinn-home.json`
- `~/motor-inn-seo/.firecrawl/gbp-structural/motorinn-service.json`
- `~/motor-inn-seo/.firecrawl/gbp-structural/motorinn-finance.json`
