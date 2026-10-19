# GBP Structural Audit — 2026-10-19

## Executive Summary
- **The weekly cadence is holding and the data is stable week-over-week.** The structural picture is the same as 10-12 with one meaningful improvement: the review engine is still running hot (**+8 reviews since 10-12 on the primary listing, 13 since Oct 5, 246 total**), reply discipline remains near-perfect, and the Oct 8 winter-readiness owner post is live and visible on the combined listing.
- **The biggest risk is unchanged: photo freshness.** The newest dated image in the Motor Inn public gallery is still **Oct 2020** (combined) / **May 2023** (Chevrolet), while every active competitor now shows 2025–2026 gallery labels — Coleman Sep 2026, Wilson May 2026, Choice Auto Nov 2025, Rick Collins Oct 2025, Toyota of Des Moines Oct 2025, Fort Dodge Aug 2025. The Week 1 photo batch (due Fri Oct 17) has **not visibly landed**; zero new gallery images appear since the 10-12 audit.
- **The second standing gap is also unchanged: no Book online CTA** on either sales listing, while Okoboji and Macke both carry one.
- **Spencer does not need to decide anything urgent.** The two decisions carried from 10-12 remain open and cheap: (1) Buick listing — reopen it or merge it and add a Buick secondary category; (2) the duplicate "Motor Inn Auto Group" shell listing (Toyota dealer, no reviews, (888) 698-6447) still sits unreclaimed next to the 5.0-rated service listing.
- **What should be done next:** upload the Week 1 photo batch this week (9 photos, plan below), add the Book online link in GBP admin, and answer the two open review replies (both 5★, Oct 17) to keep the reply streak at 100% for 2026.

## Data Collection Status
| Source | Status | Notes |
|---|---|---|
| EXA research | Yes | `gbp-research-2026-10-19.json` (33,713 bytes, 10 results) |
| GBP API reviews pull | Yes | `reviews-pull-2026-10-19.json` — both review-bearing locations, 10-19 |
| Motor Inn combined public GBP | Yes | Live scrape: 4.6 (246), Toyota dealer, owner post visible |
| Motor Inn Chevrolet public GBP | Yes | Live scrape: 4.8 (37), Chevrolet dealer |
| Motor Inn Auto Group (service) GBP | Yes | 5.0 (1), auto repair shop; plus unreclaimed shell listing (0 reviews, (888) 698-6447) |
| Chevrolet Parts / Service sub-listings | Yes | Parts: 0 reviews, (712) 882-7492; Service: 0 reviews, (712) 882-7925 |
| Buick listing | Yes | Still **Permanently closed**, (712) 792-6275, "Claim this business" showing |
| Competitor public GBPs (10) | Yes | Champion, Wittrock, Coleman/SL Ford CDJR, Okoboji Motor Co., Macke (×2 geos), Choice Auto, Wilson, Rick Collins, Toyota DSM, Fort Dodge |
| Gallery date probes (viewer-level) | Yes | First/last visible capture dates per listing (signed-out floor) |
| Local Spark (qwen3.6:35b-a3b) | Skipped | Same as 10-12: no generation step required; all output sourced to scrapes/API |

**Scope note:** signed-out Maps hides full attribute sets, services lists, and complete photo inventories. Review counts come from the GBP API (authoritative); gallery dates are viewer-visible floors, not totals.

## Categories

### Visible Category Comparison (2026-10-19)
| Category | Motor Inn | Champion Ford | Wittrock | Coleman (SL Ford CDJR) | Okoboji Motor Co. | Macke Motors |
|---|---|---|---|---|---|---|
| Toyota dealer | **Primary** (combined) | — | — | — | — | — |
| Chevrolet dealer | Separate listing 4.8 | — | — | — | — | **Primary** |
| Buick dealer | **Listing Permanently closed** | — | — | — | — | Separate live Buick listing (5.0) |
| Auto parts store | Live (Chevrolet Parts) | — | — | — | — | — |
| Auto repair shop | Live (Motor Inn Auto Group 5.0) | — | — | — | — | Live service + body shop listings |
| Ford dealer | — | **Primary** | — | **Primary** | — | — |
| Car dealer | — | — | **Primary** | — | **Primary** | — |

### What changed since 10-12
- Nothing structural. The same three entity issues stand: Buick closed-listing, duplicate Motor Inn Auto Group shell, and no ownership badges.

### Missing Categories (Prioritized) — carried
- `P1`: Buick listing reconciliation in admin (reopen, or merge + secondary category on both sales listings).
- `P2`: Claim/clean the duplicate **Motor Inn Auto Group** shell (Toyota dealer, no reviews, 888 number).
- `P2`: Confirm service-led secondary categories in admin (per EXA/GP benchmark: Used Car Dealer, Auto Repair Shop, Oil Change Service, Tire Shop, Car Finance and Loan Company, Truck Dealer).

## Attributes

### Visible Attribute / Action Comparison (2026-10-19)
| Attribute / signal | Motor Inn | Champion | Wittrock | Coleman | Okoboji | Macke | Wilson |
|---|---|---|---|---|---|---|---|
| Book online CTA | **No** | No | No | No | **Yes** | **Yes (service)** | No |
| Owner post visible | **Yes (Oct 8 winter pkg, "4 days ago")** | No | No | **Yes (Oct 5 lease offer + gallery)** | No | No | **Yes (Oct 15 Tacoma offer)** |
| Newest gallery label | **Oct 2020 (combined) / May 2023 (Chevy)** | Oct 2018 | Jan 2023 | **Sep 2026** | Dec 2022 | Nov 2021 | **May 2026** |
| Ownership/community badge | None | LGBTQ+ friendly | — | — | — | — | **Veteran- + women-owned** |
| Accessibility badges | Entrance + parking | Entrance + parking | — | — | Entrance+restroom+seating | — | Entrance + parking |

### Review posture (GBP API, 2026-10-19)
| Metric | Toyota+Chevrolet of Carroll | Chevrolet of Carroll |
|---|---|---|
| Total reviews | **246** (+8 since 10-12; +13 since Oct 5) | 37 (flat since Aug) |
| Avg rating | 4.6 | 4.8 |
| Last 7 days | **+8** | 0 |
| Unanswered 2026 | **2** (both 5★, Oct 17: Troy Kluender, Paula Cross) | 0 |
| Reply lag (last 30) | 28/30 replied, median ~1.1 days | — |

- **Reply streak: 28 of last 30 primary reviews answered, median lag ~1.1 days — healthy. The only 2026 gaps are the two Oct 17 5★ reviews; answer both this week to hold 100% on the year.**
- Chevrolet listing flat at 37 since late August — no new reviews in 7+ weeks. The 4.8 listing is an asset going stale; any review-request push should route Chevrolet customers there. (Same finding as 10-12; now 7 weeks confirmed.)

### Missing Attributes (Prioritized)
- `Table stakes`: **Photo freshness** — the Week 1 batch did not land. Plan reissued below, dates moved.
- `Strong rec`: **Book online CTA** on both sales listings → existing Schedule Service flow. Okoboji/Macke carry it; we still do not. Config change, not a build.
- `Carried`: ownership badges if factually applicable (Wilson wears veteran- + women-owned).

## Services

### Website vs Public GBP (website re-verified 2026-10-19)
| Service / offer | motorinnautogroup.com (live check today) | Public GBP surface |
|---|---|---|
| Schedule Service | `service-locations.html` — present | **Not surfaced** — no booking CTA on either listing |
| Service / Parts Center | linked from service-locations | Parts sub-listing live; service sub-listing live (5.0) |
| Schedule Test Drive | present | Not surfaced |
| Trade Appraisal | present | Not surfaced |
| Finance | 18 refs on service page; finance pages live | Not surfaced |
| Service & Parts Specials | present | Not surfaced |

### Services Missing From Public GBP — unchanged
- Booking/appointment actions (service + test drive)
- Finance / trade-in descriptions
- Service and parts descriptions on the sales listings

### Draft status
- The **2026-08-17 services and description drafts remain factually current** (website surfaces unchanged; phone resolution 792-5000/882-7802 already reflected). No new drafts written this run; reuse `content/drafts/gbp-services/services-2026-08-17.md` and `content/drafts/gbp-description/description-2026-08-17.md` (Version 2) at admin time.

## Description

### Public description signal (2026-10-19)
| Business | Public description visible | Note |
|---|---|---|
| Motor Inn (combined) | Not exposed signed-out | Owner post Oct 8 visible instead |
| Motor Inn Chevrolet | Not exposed | 4.8/37 |
| Competitors (all checked) | Not exposed signed-out | — |

- Signed-out Maps does not render the business description for any listing in this set — unchanged from both prior audits. The description check is admin-side only; the approved Version 2 draft stands ready.

## Photos

### Visible gallery floors (photo-viewer probe, 2026-10-19)
| Business | Photo count (public) | First visible dated label | Freshness read |
|---|---|---|---|
| **Motor Inn combined** | **67** | **Oct 2020** | **Weakest active** |
| Motor Inn Chevrolet | (module, viewer probe) | **May 2023** | Weak |
| Chevrolet Parts sub-listing | 8 | Feb 2022 | Weak |
| Champion Ford | 13 | Oct 2018 | Weakest label seen |
| Wittrock | 32 | Jan 2023 | Moderate |
| Coleman / SL Ford CDJR | 89 | **Sep 2026** | **Best in set** |
| Okoboji Motor Co. | 67 | Dec 2022 | Moderate |
| Macke Motors | (service-led) | Nov 2021 | Aging |
| Choice Auto | 21 | Nov 2025 | Strong |
| Wilson Toyota | 388 | May 2026 | Strong |
| Rick Collins Toyota | 89 | Oct 2025 | Strong |
| Toyota of Des Moines | 278 | Oct 2025 | Strong |
| Fort Dodge Ford Lincoln | 1184 | Aug 2025 | Strong |

### What matters
- **Zero gallery movement on Motor Inn since 10-12** — the Week 1 upload did not happen. Five competitors sit at 2025–2026 labels; our sales-listing floors are 2020/2023.
- Chevrolet listing photo module dates to May 2023; parts sub-listing Feb 2022. The 4.8-rated store deserves current imagery too.

### Upload Plan (4 weeks, 9/week, 36 total) — reissued, dates moved
Naming `motorinn-[subject]-[location]-YYYY-MM-DD.jpg`, geotag Carroll (Spirit Lake/Okoboji only where real).

- **Week 1 — Fall inventory, front of house (upload by Fri 2026-10-23):** 3 exterior/signage at 1526 Le Clark Rd; 4 current used SUV/truck photos (front 3/4 + rear, lot context); 2 sales-desk/team shots.
- **Week 2 — Service & parts proof (by Fri 2026-10-30):** 3 service bays working; 2 parts counter; 2 waiting-area; 2 intake/inspection.
- **Week 3 — Winter readiness (by Fri 2026-11-06):** 3 battery/wiper/tread closeups; 2 4WD/AWD inventory; 2 staff-with-customer; 2 entrance/hours.
- **Week 4 — Category reinforcement (by Fri 2026-11-13):** 2 Chevrolet-badged; 2 Toyota-badged; 2 Buick-adjacent if resolved; 3 community/dusk.

## Action Items (This Week)
1. **Upload Week 1 photos (9) by Fri 2026-10-23** — the carried Week 1 set, two weeks late. This is the single highest-leverage structural fix left.
2. **Reply to the two Oct 17 5★ reviews** (Troy Kluender, Paula Cross) — keeps 2026 reply coverage at 100%.
3. **Add Book online CTA** to both sales listings → Schedule Service. Config change in admin.
4. **Buick decision (Spencer, admin):** reopen `Buick at MOTOR INN OF CARROLL, L.L.C.` (still showing Permanently closed + Claim this business) or merge it and set Buick dealer as a secondary category on both sales listings.
5. **Duplicate shell:** claim/merge the review-less `Motor Inn Auto Group` Toyota-dealer listing (888 number) so the brand entity resolves canonically.
6. **Chevrolet review nudge:** 7 weeks flat at 37 on the 4.8 listing — add a review ask to the Chevrolet delivery/checkout flow.
7. **Posts queue:** next posts per the velocity plan; the Oct 8 winter pkg stays live through the 31st.

## Sources
- `~/motor-inn-seo/audits/gbp-structural/gbp-research-2026-10-19.json` (EXA, 10 results)
- `~/motor-inn-seo/audits/gbp-structural/reviews-pull-2026-10-19.json` (GBP API v4, both review-bearing locations, 2026-10-19)
- Live Google Maps scrapes 2026-10-19: `scrapes-2026-10-19/` (Motor Inn ×5 surfaces + 10 competitor listings + About-tab probes + photo-viewer date probes)
- `~/motor-inn-seo/content/drafts/gbp-posts/published-state.json` (15-post ledger; newest publish 2026-10-15)
- `~/motor-inn-seo/content/drafts/gbp-services/services-2026-08-17.md`, `content/drafts/gbp-description/description-2026-08-17.md`, `content/drafts/gbp-photos/photo-plan-2026-10-12.md`
- `~/motor-inn-seo/audits/gbp-velocity/gbp-velocity-latest.md` (review-velocity baseline + reply-lag method)
- `~/.agents/product-marketing-context.md`, `~/motor-inn-seo/tools/seomachine/config/competitors.json`
- `motorinnautogroup.com` service-locations page (live curl check 2026-10-19)
