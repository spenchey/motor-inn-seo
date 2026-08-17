# GBP Structural Audit — 2026-08-17

## Executive Summary
- **The biggest new signal this week is a phone NAP discrepancy on the live Motor Inn listing.** The public Google Business Profile shows **(712) 792-5000**, but the documented NAP in `product-marketing-context.md` is **(712) 522-2526**. An inconsistent phone number across the web weakens local ranking and confuses shoppers. This must be reconciled in GBP admin before anything else.
- **Competitor activity is accelerating while Motor Inn is flat.** Okoboji Motor Company (1,011 reviews) now surfaces a **Book online** CTA plus **Delivery** and a **Videos** tab; Macke Motors surfaces **Book online**; Wittrock and Choice Auto both posted photos within the last 1–3 weeks; Spirit Lake Ford CDJR runs a live owner post with a financing offer. Motor Inn showed none of these action or freshness signals today.
- **Next:** verify the correct phone number, enable/confirm a service-booking action, publish one owner post, and start the photo cadence. These are the highest-leverage moves.
- **Spencer needs to decide the phone number (792-5000 vs 522-2526)** and whether Motor Inn's GBP should surface a booking/service action and a GMC category signal.

## Data Collection Status
| Source | Status | Notes |
|---|---|---|
| EXA research | Yes | `gbp-research-2026-08-17.json` (31,567 bytes) saved |
| Motor Inn combined public GBP | Yes | Live scrape: 4.5 / 192 reviews, Toyota dealer |
| Champion Ford public GBP | Yes | Live scrape: 4.2 / 134 reviews, Ford dealer |
| Wittrock Motor Company public GBP | Yes | Live scrape: 4.6 / 261 reviews |
| Choice Auto Carroll public GBP | Yes | Live scrape: 4.4 / 123 reviews, used car dealer |
| Pro Auto Sales public GBP | Yes | Live scrape: 4.6 / 45 reviews, used car dealer |
| Okoboji Motor Company public GBP | Yes | Live scrape: 4.5 / 1,011 reviews |
| Spirit Lake Ford CDJR (Coleman) public GBP | Yes | Live scrape: 4.4 / 365 reviews |
| Macke Motors public GBP | Yes | Live scrape: 3.8 / 306 reviews, Chevrolet dealer |
| Local Spark (qwen3.6:35b-a3b) | No | Spark host unreachable from this runner; output produced locally and kept factual/sourced |

**Important note:** This run recovered live public Google Maps views for all 8 competitors plus Motor Inn — a full competitive sweep. Public Maps still hides most edit-level fields (secondary categories, full attribute sets, full services list, full descriptions, exact photo counts), so those comparisons remain grounded to visible signals plus the confirmed website offerings from the 08-03 run.

## Categories

### Visible Category Comparison
| Category | Motor Inn | Champion Ford | Wittrock | Coleman | Okoboji Motor Co. | Macke Motors |
|---|---|---|---|---|---|---|
| Toyota dealer | **Primary** (combined store) | — | — | — | — | — |
| Chevrolet dealer | Linked sub-listing at same address | — | — | — | — | **Primary** |
| Buick dealer | Linked result at same address | — | — | — | — | Separate listing (Buick at Macke) |
| Auto parts store | Linked sub-listing at same address | — | — | — | — | — |
| Ford dealer | — | **Primary** | — | — | — | — |
| Car dealer | — | — | **Primary** | **Primary** | **Primary** | — |
| Used car dealer | — | — | — | — | — | — |

### What Matters
- Motor Inn's combined listing surfaces as **Toyota dealer** — good for Toyota intent.
- Motor Inn search results also surface **Chevrolet dealer**, **Buick dealer**, and **Auto parts store** at the same Carroll address.
- **Macke Motors** (a direct Chevrolet competitor) runs a structured multi-listing setup: Chevrolet primary, plus separate Buick, service, and body-shop listings. Motor Inn has analogous linked sub-listings, which is the correct pattern for a multi-franchise store.
- No competitor surfaced a **GMC** category publicly, and no GMC signal surfaced for Motor Inn either.

### Missing Categories (Prioritized)
- `P1`: Confirm in GBP admin whether the Chevy/Buick/GMC store carries a live **GMC dealer** category signal. It did not surface publicly today, and GMC is a documented search theme.
- `P1`: Reconcile the **phone NAP** (792-5000 live vs 522-2526 documented) — this outranks category tweaks this week.
- `P2`: Verify in GBP admin that both stores use all relevant service-led secondary categories aligned with the EXA benchmark: `Used Car Dealer`, `Auto Repair Shop`, `Oil Change Service`, `Tire Shop`, `Car Finance and Loan Company`, `Truck Dealer`, `Auto Parts Store`.
- `P3`: Only keep categories that match a real on-site function.

## Attributes

### Visible Attribute / Action Comparison
| Attribute / signal | Motor Inn | Champion Ford | Wittrock | Coleman | Okoboji Motor Co. | Macke Motors |
|---|---|---|---|---|---|---|
| Visible attribute badge | No public badge seen | `LGBTQ+ friendly` visible | No public badge seen | No public badge seen | No public badge seen | No public badge seen |
| In-store pickup | Yes (public) | Yes | Yes | Yes | — | — |
| Delivery | No | Yes | Yes | Yes | Yes | — |
| Book online CTA | **No** | No | No | No | **Yes** | **Yes** |
| Videos module | No | No | No | No | **Yes** | No |
| Owner post visible | **No** | Yes (Feb 27) | No | **Yes (Aug 10)** | No | No |
| Fresh photos (<3 wks) | No signal | No | **Yes (5 days)** | — | **Yes (3 wks)** | — |

### What Matters
- **Okoboji and Macke both expose a booking action; Motor Inn does not.** This is the clearest structural gap.
- **Delivery** is now common across competitors (Champion, Wittrock, Coleman, Okoboji). Motor Inn's public listing did not show it — verify whether Motor Inn offers delivery and, if so, enable the attribute.
- Competitor owner posts and fresh photos are increasing; Motor Inn shows neither today.

### Missing Attributes (Prioritized)
- `Table stakes`: Add/confirm a **service-booking or online-appointment action** in GBP. Okoboji and Macke both surface one.
- `Table stakes`: **Publish a fresh owner post this week.** Three competitors showed post/photo freshness; Motor Inn showed none.
- `Strong rec`: Verify **Delivery** attribute — 4 competitors show it publicly.
- `Strong rec`: Confirm in GBP admin that Motor Inn has accurate operational attributes on: financing, test drives, trade-ins, service department, parts department, online appointments, Wi-Fi, and accessibility (where true on site).
- `Differentiator`: Add accessibility/waiting-area amenities only if true on site.

## Services

### Website vs Public GBP Comparison
| Service / offer | Motor Inn | Champion Ford | Wittrock | Coleman | Okoboji Motor Co. | Macke Motors |
|---|---|---|---|---|---|---|
| Service scheduling | Website has Schedule Service; **not visible on public GBP** | Service deep link visible | Not visible | Not visible | **Book online CTA** | **Book online CTA** |
| Parts department | Website has parts links; parts sub-listing surfaced | Not visible | Not visible | Not visible | Not visible | Not visible |
| Test drive | Website has test-drive pages | Not visible | Not visible | Visible deep link (prior) | Not visible | Not visible |
| Finance / trade | Website has finance + trade appraisal | — | — | Financing promo in owner post | — | — |
| Service center | Website has Toyota + Chevy service links | Not visible | Not visible | Not visible | Implied by booking | Implied by booking |

### Services Missing From Public GBP
- Service scheduling / booking action
- Parts center description
- Service center description
- Test-drive description
- Finance / trade-in description
- New vehicle sales description
- Used vehicle sales description

### Services Needing Better Descriptions
- Every Motor Inn service that exists on the website but does not surface with useful copy in public GBP today.

### Draft Output
- Dated service descriptions saved to `~/motor-inn-seo/content/drafts/gbp-services/services-2026-08-17.md`

## Description

### Comparison Table
| Business | Public description visible | Category signal | Service-area signal | Trust or action signal | Recommendation |
|---|---|---|---|---|---|
| Motor Inn | No full GBP description visible | Toyota dealer + linked Chevy/Buick/parts | Carroll address; website references Carroll County region | Website headline: "Your Trusted Chevrolet & Toyota Dealership in Carroll, Iowa," 85+ years | **Reconcile phone NAP first**, then rewrite/publish a fuller GBP description |
| Champion Ford | No full description | Ford dealer | Carroll | Attribute badge + owner post + service deep link | Stronger public activity |
| Wittrock | No full description | Car dealer | Carroll | Fresh photos | Active but generic |
| Coleman (Spirit Lake Ford CDJR) | No full description | Car dealer | Spirit Lake | Owner post with financing offer + Delivery | Strong public conversion cues |
| Okoboji Motor Co. | No full description | Car dealer | Spirit Lake | Booking CTA + Delivery + Videos + 1,011 reviews | Strongest service-action profile |
| Macke Motors | No full description | Chevrolet dealer | Lake City | Book online | Structured multi-listing model |

### Current Motor Inn Description Signal
- Full GBP description did not surface in the public view.
- Strongest replacement source: website hero copy (trusted Chevrolet and Toyota dealership in Carroll, Iowa, serving Carroll County and surrounding communities with new vehicles, used cars, and dependable service for over 85 years).

### Recommendation
- **Reconcile the phone NAP first** (792-5000 live vs 522-2526 documented). Then publish a fuller GBP description.
- Dated description drafts (3 versions) saved to `~/motor-inn-seo/content/drafts/gbp-description/description-2026-08-17.md`

## Photos

### Visible Public Photo Signals
| Metric | Motor Inn | Champion Ford | Wittrock | Coleman | Okoboji Motor Co. |
|---|---|---|---|---|---|
| Photos module visible | Yes | Yes | Yes | Yes | Yes (with Videos tab) |
| Public photo count | Hidden | Hidden | Hidden | Hidden | Hidden |
| Dated owner media | No | Yes (Feb 27) | **Yes (5 days)** | Owner post (Aug 10) | **Yes (3 weeks)** |
| Public freshness | Weak | Moderate | **Best this week** | Moderate | Strong (videos + recent) |

### What Matters
- Exact photo counts remain hidden, but **freshness velocity is now clearly measurable** and Motor Inn is behind.
- Wittrock (5 days), Choice Auto (12 days), and Okoboji (3 weeks, plus videos) are posting within the last 1–3 weeks. Motor Inn showed no comparable recent upload.
- Motor Inn needs a predictable weekly upload rhythm regardless of the hidden count.

### Upload Plan Summary
- Upload **9 photos per week for 4 weeks** (36 total) — a 50% velocity edge over the active competitors. Weeks: showroom/inventory → service/parts → community/trust → category reinforcement. Naming `motorinn-[service]-[location]-[YYYY-MM-DD].jpg`, geotagged to Carroll (and any Spirit Lake / Okoboji sites).
- Dated photo plan saved to `~/motor-inn-seo/content/drafts/gbp-photos/photo-plan-2026-08-17.md`

## Action Items (This Week)
1. **Verify the correct phone number** in GBP admin (live listing shows 792-5000; context documents 522-2526) — this is the top priority and needs Spencer's decision.
2. Add/confirm a **service-booking or online-appointment action** in GBP. Okoboji and Macke both surface one.
3. **Publish one fresh owner post** this week pointing to Schedule Service.
4. Verify **Delivery** attribute (4 competitors show it) and confirm GMC category signal in admin.
5. Start the **9-photos/week** upload plan immediately.

## Sources
- `~/motor-inn-seo/audits/gbp-structural/gbp-research-2026-08-17.json`
- Live Google Maps scrapes, 2026-08-17 (Motor Inn + 8 competitors via browser tool)
- `~/motor-inn-seo/audits/gbp-structural/gbp-structural-2026-08-03.md` (prior audit)
- `~/.agents/product-marketing-context.md`
- `motorinnautogroup.com` homepage, service-locations, Finance (from prior runs)