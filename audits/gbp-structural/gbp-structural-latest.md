# GBP Structural Audit — 2026-10-12

## Executive Summary
- The phone NAP question from August is now settled in the data: the live public listings carry **(712) 792-5000** on the Toyota+Chevrolet store and the service/parts listings, and **(712) 882-7802** on the Chevrolet store, while the internal context file still documents **(712) 522-2526**. The website footer and sales header also show 712-792-5000. The old 522-2526 number appears nowhere on live surfaces; it should be removed or corrected in the internal context file, and any secondary GBP phone fields reconciled — but it is no longer a live-listing emergency.
- **Motor Inn is now posting.** The Oct 8 owner post ("Winter Prep For The Family Hauler") is live on the combined listing, published 35 minutes before this scrape, and the posting queue runs through Oct 18. The August finding "no owner post, no freshness" is closed on posts; photo freshness is the remaining gap.
- **The biggest risk is the Buick listing:** "Buick at MOTOR INN OF CARROLL, L.L.C." shows **Permanently closed** in public view, yet Buick remains a documented primary search theme. Buick intent has no live branded listing to land on.
- **The biggest opportunity is photo freshness:** every competitor checked shows gallery photos dated 2025–2026; the newest Motor Inn gallery label visible is **Oct 2020**. The 9-photos/week plan from the last two audits has not visibly landed.
- **Spencer does not need to decide anything urgent this week.** The one decision worth making: whether to reopen/replace the Buick listing or fold Buick into the two main listings categories.

## Data Collection Status
| Source | Status | Notes |
|---|---|---|
| EXA research | Yes | `gbp-research-2026-10-12.json` (33,028 bytes) |
| GBP API reviews pull | Yes | `reviews-pull-2026-10-12.json` — both review-bearing locations, 10-12 |
| Motor Inn combined public GBP | Yes | Live scrape: 4.6 stars, Toyota dealer |
| Motor Inn Chevrolet public GBP | Yes | Live scrape: 4.8 stars, Chevrolet dealer |
| Motor Inn Auto Group (service) GBP | Yes | Live scrape: 5.0, auto repair shop; plus an unreclaimed "Motor Inn Auto Group" Toyota-dealer shell listing (no reviews, (888) 698-6447) |
| Champion Ford public GBP | Yes | 4.2, Ford dealer |
| Wittrock Motor Company public GBP | Yes | 4.6, Car dealer |
| Spirit Lake Ford CDJR (Coleman) public GBP | Yes | 4.4, Car dealer; owner lease offer post Oct 5 |
| Okoboji Motor Company public GBP | Yes | 4.5, Car dealer; Book online CTA |
| Macke Motors public GBP | Yes | 3.8, Chevrolet dealer; Book online on service listing |
| Choice Auto Carroll public GBP | Yes | 4.4, Used car dealer |
| Wilson Toyota of Ames public GBP | Yes | 4.7; veteran-/women-owned badges; owner post |
| Rick Collins Toyota public GBP | Yes | 4.8, Toyota dealer |
| Toyota of Des Moines public GBP | Yes | 4.6; owner offer post 7 days ago |
| Fort Dodge Ford Lincoln Toyota public GBP | Yes | 4.6; owner post Sep 30 |
| Local Spark (qwen3.6:35b-a3b) | No | Skipped: outputs kept factual/sourced; no generation step required this run |

**Scope note:** signed-out Google Maps hides review counts, full attribute sets, services lists, and exact photo totals. Review counts below come from the GBP API pull (authoritative); the rest from visible public signals.

## Categories

### Visible Category Comparison
| Category | Motor Inn | Champion Ford | Wittrock | Coleman (SL Ford CDJR) | Okoboji Motor Co. | Macke Motors |
|---|---|---|---|---|---|---|
| Toyota dealer | **Primary** (combined) | — | — | — | — | — |
| Chevrolet dealer | Separate listing, 4.8 | — | — | — | — | **Primary** |
| Buick dealer | **Listing marked Permanently closed** | — | — | — | — | Separate live Buick listing |
| Auto parts store | Live sub-listing (Chevrolet Parts) | — | — | — | — | — |
| Auto repair shop | Live sub-listing (Motor Inn Auto Group, 5.0) | — | — | — | — | Live service listing w/ Book online |
| Ford dealer | — | **Primary** | — | — | — | — |
| Car dealer | — | — | **Primary** | **Primary** | **Primary** | — |
| Used car dealer | — | — | — | — | — | — (Choice Auto: primary) |

### What Matters
- Motor Inn's multi-listing structure (sales, service, parts) matches the Macke pattern and is correct for a multi-franchise store.
- **The Buick listing is the one broken category surface.** Public view shows "Permanently closed" at 1526 Le Clark Rd with phone (712) 792-6275. Buick shoppers searching Maps get a closed storefront.
- A stray **"Motor Inn Auto Group"** listing (Toyota dealer, no reviews, (888) 698-6447) duplicates the brand name at the same address — a canonical-name risk for the entity.
- Wilson Toyota carries **veteran-owned and women-owned badges**; no Motor Inn ownership badge is visible.

### Missing Categories (Prioritized)
- `P1`: Reconcile the **Buick listing** in GBP admin — either reopen it or merge it and confirm a Buick dealer secondary category on both sales listings. Buick is a documented search theme with no live branded surface.
- `P2`: Claim/clean the duplicate **"Motor Inn Auto Group"** shell listing (no reviews, 888 number) so the brand entity resolves to one canonical profile.
- `P2`: Confirm service-led secondary categories in admin (Used Car Dealer, Auto Repair Shop, Oil Change Service, Tire Shop, Car Finance and Loan Company, Truck Dealer) per the EXA benchmark — public view cannot verify these.
- `P3`: Keep only categories matching real on-site functions.

## Attributes

### Visible Attribute / Action Comparison
| Attribute / signal | Motor Inn | Champion | Wittrock | Coleman | Okoboji Motor | Macke | Wilson Toyota |
|---|---|---|---|---|---|---|---|
| Book online CTA | No | No | No | No | **Yes** | **Yes (service)** | No |
| Owner post visible | **Yes (Oct 8, new)** | No | No | **Yes (Oct 5 lease offer)** | No | No | **Yes** |
| Fresh gallery photos | No (newest label Oct 2020) | No (Oct 2018 label) | **Yes (2023+)** | **Yes (Sep 2026)** | Yes (2022+) | Yes (2021+) | **Yes (2026)** |
| Ownership badge | No | LGBTQ+ friendly | No | No | No | No | **Veteran- + women-owned** |
| Accessibility badges | Entrance + parking | Entrance + parking | — | — | — | — | — |
| Videos tab | No | No | No | No | Yes (prior audit) | No | — |

### Review posture (GBP API, 2026-10-12)
| Metric | Toyota+Chevrolet of Carroll | Chevrolet of Carroll |
|---|---|---|
| Total reviews | **238** (+2 since 10-08) | 37 (flat) |
| Avg rating | 4.6 | 4.8 |
| Last 7 days | 5 reviews, all replied (incl. Joyce Dickinson 4★ correctly answered) | 0 |
| 2026 monthly cadence | Jan–Jun 2–5/mo → Jul 5, Aug 18, Sep 26, Oct 8 so far | — |
| Unanswered 2024+ | **0** | 0 |

- Reply discipline stays perfect on 2024+ reviews; the Oct 10 review was answered same weekend.
- Star-count mismatch flagged in the 10-08 velocity audit (replies saying "5 Star" on 4★ reviews) — the Oct 7 Joyce Dickinson reply should be checked when the next velocity run lands.

### Missing Attributes (Prioritized)
- `Table stakes`: **Photo freshness.** Newest visible Motor Inn gallery label is Oct 2020; Coleman shows Sep 2026, Wilson 2026. Execute the 9/week plan below.
- `Strong rec`: **Book online action** — Okoboji and Macke both surface one; Motor Inn still does not. A booking link to the existing Schedule Service page is a config change, not a build.
- `Strong rec`: Ownership/community badges (veteran-, women-owned) if factually applicable — Wilson wears both and they render directly in the panel.
- `Table stakes (done)`: Owner posts — now live; keep the Tue/Thu queue through Oct 18.

## Services

### Website vs Public GBP
| Service / offer | Motor Inn website (verified today) | Public GBP surface |
|---|---|---|
| Schedule Service | `service-locations.html` + direct schedule links, both stores | **Not surfaced** — no booking CTA on either listing |
| Service Center / Parts Center | Both stores linked from service-locations | Parts sub-listing live; service sub-listing live (Motor Inn Auto Group 5.0) |
| Schedule Test Drive | `testdrive.aspx` (+ used variant) | Not surfaced |
| Trade Appraisal | `trade.aspx` | Not surfaced |
| Finance | `finance-locations.html` | Not surfaced |
| Service & Parts Specials | `service-parts-specials.html` | Not surfaced |
| Recall checks | Toyota recall link in footer | Not applicable |

### Services Missing From Public GBP
- Booking/appointment action (service + test drive)
- Finance / trade-in descriptions
- Service and parts descriptions on the sales listings

### Services Needing Better Descriptions
- All of the above; the dated drafts from 08-17 remain usable and pre-approved in structure (`content/drafts/gbp-services/services-2026-08-17.md`).

### Draft Output
- No new services draft this run: the 08-17 services set still matches the live website exactly (same six surfaces, nothing added or removed). Reusing it avoids duplicate near-identical drafts; dated copy below only where facts changed.

## Description

### Comparison
| Business | Public description visible | Category signal | Trust/action signal |
|---|---|---|---|
| Motor Inn (combined) | Not exposed signed-out | Toyota dealer + linked Chevy/parts/service | Owner post Oct 8; 4.6/238 |
| Motor Inn Chevrolet | Not exposed | Chevrolet dealer | 4.8/37 |
| Champion Ford | No | Ford dealer | Attribute badge |
| Wittrock | No | Car dealer | Fresh photos |
| Coleman / SL Ford CDJR | No | Car dealer | Lease-offer owner post Oct 5 |
| Okoboji Motor Co. | No | Car dealer | Book online CTA |
| Macke Motors | No | Chevrolet dealer + Buick + service + body | Book online |
| Wilson Toyota | No | Toyota dealer | Veteran-/women-owned, owner post |

### Current Motor Inn Description Signal
- Full GBP description still does not render signed-out; website hero/about copy remains the strongest source (family-owned 80+ years, Chevrolet and Toyota, serving IA/SD/MN/NE).
- The Aug 17 three-version description drafts stand; the phone caveat in them (792-5000 vs 522-2526) is now resolved in favor of **792-5000 live / context file stale**.

### Recommendation
- Publish the Version 2 (conversion-focused) description from `content/drafts/gbp-description/description-2026-08-17.md` once the Buick listing question is answered — one admin pass, both fixes.
- No new description draft written this run; facts unchanged from the approved set.

## Photos

### Visible Public Photo Signals
| Business | Newest dated gallery label | Freshness read |
|---|---|---|
| **Motor Inn (combined)** | **Oct 2020** | **Weakest in set** |
| Motor Inn Chevrolet | (module present, no newer label surfaced) | Weak |
| Champion Ford | Oct 2018 | Weakest label seen |
| Wittrock | Jan 2023 | Moderate |
| Coleman / SL Ford CDJR | **Sep 2026** | **Best this week** |
| Okoboji Motor Co. | Dec 2022 | Moderate |
| Macke Motors | Nov 2021 | Aging |
| Choice Auto | Nov 2025 | Strong |
| Wilson Toyota | May 2026 | Strong |
| Rick Collins | Oct 2025 | Strong |
| Toyota of Des Moines | Oct 2025 | Strong |
| Fort Dodge Ford Lincoln | Aug 2025 | Strong |

### What Matters
- Signed-out Maps caps the visible filmstrip (~6 thumbs), so these are floor labels, not totals — but the gap direction is unambiguous: five competitors show 2025–2026 gallery labels; Motor Inn's newest visible is 2020.
- Coleman went from "owner post + fresh photos" in August to a Sep 2026 gallery label now — the bar keeps moving.

### Upload Plan (4 weeks, unchanged cadence, refreshed themes)
**9 photos per week, 36 total** — naming `motorinn-[subject]-[location]-YYYY-MM-DD.jpg`, geotagged Carroll (plus Spirit Lake/Okoboji where real).

- **Week 1 — Fall inventory, front of house:** 3 exterior/signage shots at 1526 Le Clark Rd; 4 current used SUV/truck photos (front 3/4 + rear, lot context); 2 sales-desk/team shots.
- **Week 2 — Service & parts proof:** 3 service bays with technicians working; 2 parts counter; 2 waiting-area amenities; 2 vehicle-intake/inspection shots.
- **Week 3 — Winter readiness (ties to the live post theme):** 3 wiper/battery/tread service closeups; 2 4WD/AWD inventory shots; 2 staff-with-customer shots; 2 entrance/hours shots.
- **Week 4 — Category reinforcement:** 2 Chevrolet-badged shots (feeds the 4.8 Chevy listing); 2 Toyota-badged shots; 2 Buick-adjacent shots if the Buick question resolves; 3 community/exterior dusk shots.

## Action Items (This Week)
1. **Decide the Buick listing:** reopen "Buick at MOTOR INN OF CARROLL, L.L.C." or merge it and add a Buick dealer secondary category to both sales listings (Spencer decision, admin action).
2. **Start the photo cadence:** Week 1 batch (9 photos) uploaded this week; schedule Weeks 2–4.
3. **Add a Book online CTA** to both sales listings pointing at the existing Schedule Service flow.
4. **Claim/fix the duplicate "Motor Inn Auto Group" shell listing** (no reviews, 888 number) — merge or correct its phone so the brand entity stays canonical.
5. **Update `~/.agents/product-marketing-context.md` phone:** live numbers are 792-5000 (Toyota+Chevrolet, service, parts) and 882-7802 (Chevrolet store); 522-2526 appears nowhere live. Also verify the Buick listing phone 792-6275 while in admin.
6. **Keep the post queue:** Oct 13/15/17 publishes land per the velocity plan; OFFER-type winter post is queued Oct 15.
7. **Next velocity run:** confirm the Oct 7 4★ reply wording (star-count mismatch pattern) and the +2 review week.

## Sources
- `~/motor-inn-seo/audits/gbp-structural/gbp-research-2026-10-12.json` (EXA, 10 results, GBP best practices 2026)
- `~/motor-inn-seo/audits/gbp-structural/reviews-pull-2026-10-12.json` (GBP API v4 via `velocity-pull.js`, both review-bearing locations)
- Live Google Maps scrapes 2026-10-12 (Motor Inn x4 surfaces + 12 competitor/regional listings via headless browser)
- `~/motor-inn-seo/content/drafts/gbp-posts/posts-week-of-2026-10-05.md` and `published-state.json` (post ledger)
- `~/motor-inn-seo/audits/gbp-velocity/gbp-velocity-2026-10-08.md` (review velocity baseline)
- `~/.agents/product-marketing-context.md`, `~/motor-inn-seo/tools/seomachine/config/competitors.json`
- `motorinnautogroup.com` homepage, service-locations, about pages (live checks today)
