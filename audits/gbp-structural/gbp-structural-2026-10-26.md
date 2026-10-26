# GBP Structural Audit — 2026-10-26

## Executive Summary
- **One thing changed this week, and it is good: the review engine on the primary listing is the hottest it has been all quarter.** Six new reviews landed between Oct 20–24 (all 5★, all answered same-day to next-day), bringing the primary listing to **252 total at 4.6** — up from 246 on Oct 19 and 238 on Oct 12. The weekly count has now risen four straight weeks (4 → 5 → 8 → 6). The Chevrolet listing is flat at **37 / 4.8** (nine weeks without a new review) and the Oct 8 winter-prep owner post is still live and visible on the combined listing.
- **The biggest risk is exactly where it has been for three straight audits: photo freshness.** The newest dated image in the public galleries is still **Oct 2020 (combined)** and **May 2023 (Chevrolet)** — no gallery movement since the 10-12 audit, so the Week 1–2 photo batches from the standing plan have still not visibly landed. Every active competitor now shows a 2025–2026 gallery label (Coleman Sep 2026, Fort Dodge Sep 2026, Wilson May 2026, Rick Collins / Toyota of Des Moines Oct 2025, Choice Auto Nov 2025). Every week this slips, competitors look more alive in the map pack.
- **The second standing gap is also unchanged: no Book online CTA** on either sales listing, while Okoboji Motor Co. and Macke both carry one, and the **Buick listing is still Permanently closed** with "Claim this business" showing.
- **Spencer does not need to decide anything urgent.** The two cheap admin decisions carried since 10-12 remain open: (1) reopen the Buick listing or merge it and set Buick dealer as a secondary category; (2) claim/merge the duplicate review-less "Motor Inn Auto Group" shell listing (888 number).
- **What should be done next:** upload the carried Week 1 photo batch (9 photos) this week, add Book online to both sales listings, and add a review ask to the Chevrolet checkout flow — the 4.8 listing has been stuck at 37 reviews since Sep 6.

## Data Collection Status
| Source | Status | Notes |
|---|---|---|
| EXA research | Yes | `gbp-research-2026-10-26.json` (33,601 bytes) |
| GBP API reviews pull | Yes | `reviews-pull-2026-10-26.json` — both review-bearing locations, 10-26 |
| Motor Inn combined public GBP | Yes | Live scrape: 4.6, Toyota dealer; owner post visible ("4 days ago") |
| Motor Inn Chevrolet public GBP | Yes | Live scrape: 4.8, Chevrolet dealer; nested under combined store |
| Motor Inn Auto Group (service) GBP | Yes | 5.0, auto repair shop, 792-5000 |
| Chevrolet Parts sub-listing | Yes | 0 reviews, (712) 882-7492, photo label Feb 2022 |
| Buick listing | Yes | Still **Permanently closed**, (712) 792-6275, Claim this business, posting turned off |
| Competitor public GBPs | 10 of 11 | Okoboji Toyota resolves to Okoboji Motor Company signed-out (same-address entity, per config note); all others scraped clean |
| Gallery date probes | Yes | Viewer-level first-visible labels, signed-out floor |
| Local Spark (qwen3.6:35b-a3b) | Skipped | No generation step required; all output sourced to scrapes/API |

**Scope note:** signed-out Maps hides full attribute sets, services lists, and complete photo inventories. Review counts come from the GBP API (authoritative). Gallery dates are viewer-visible floors, not full inventories. Photo-count-per-gallery was not retrievable signed-out this run (viewer exposes no total); date floors only.

## Categories

### Visible Category Comparison (2026-10-26)
| Category | Motor Inn | Champion Ford | Wittrock | Coleman (SL Ford CDJR) | Okoboji Motor Co. | Macke Motors |
|---|---|---|---|---|---|---|
| Toyota dealer | **Primary (combined)** | — | — | — | — | — |
| Chevrolet dealer | Separate listing 4.8 | — | — | — | — | **Primary** |
| Buick dealer | **Listing Permanently closed** | — | — | — | — | Separate live Buick listing (5.0) |
| Auto parts store | Live (Chevrolet Parts, 0 reviews) | — | — | — | — | — |
| Auto repair shop | Live (Motor Inn Auto Group 5.0) | — | — | — | — | Live service + body shop listings |
| Ford dealer | — | **Primary** | — | **Primary** | — | — |

**Gap:** the Buick hole is now in its tenth documented week. Macke runs a live, 5.0-rated standalone Buick listing one town over — Buick buyers searching Maps near Carroll find a closed page where ours should be. The zero-reviews parts sub-listing is correct as a service category but contributes nothing to the pack.

## Attributes

### Visible Attribute / Action Comparison (2026-10-26)
| Attribute / signal | Motor Inn | Champion | Wittrock | Coleman | Okoboji | Wilson | Choice |
|---|---|---|---|---|---|---|---|
| Book online CTA | **No** | No | No | No | **Yes** | No | No |
| Owner post visible | **Yes (Oct 8 winter pkg)** | No | No | **Yes (Bronco Sport lease, Oct 5–Nov 2)** | No | **Yes (Tacoma offer, Oct 15–31)** | No |
| Newest gallery label | **Oct 2020 / May 2023 (Chevy)** | Oct 2018 | Jan 2023 | **Sep 2026** | Dec 2022 | **May 2026** | Nov 2025 |
| Accessibility badges | Entrance + parking | Entrance + parking | — | Entrance + parking | **Entrance + parking + restroom + seating** | Entrance + parking | — |

### Review posture (GBP API, 2026-10-26)
| Metric | Toyota+Chevrolet (…817758) | Chevrolet (…902964) |
|---|---|---|
| Total / rating | **252 / 4.6** | 37 / 4.8 |
| New since 10-19 | **+6 (Oct 20, 21×3, 22, 24)** | 0 |
| Weekly velocity (W40→W43) | 4 → 5 → 8 → 6 | flat since Aug 28 |
| 2026 reply coverage | **100% (88/88)** | 100% |
| Reply lag, last 20 | 0–5 days | 41–470 days (no recent reviews to answer) |

**Gap:** booking CTAs remain the visible action-surface gap vs Okoboji/Macke; the Chevrolet listing's nine-week review drought is now the longest on record and needs a process fix (ask at delivery), not a posts fix.

## Services

### Website vs Public GBP (website re-verified 2026-10-26)
- motorinnautogroup.com confirms: **Schedule Service** (`serviceappmt.aspx`, 200), Service/parts specials page, service-locations. The public GBP still surfaces none of this as named services or a booking link.
- The drafted service descriptions (`services-2026-08-17.md`: Service Center, Parts Center, Schedule Service, New/Used Sales, Test Drive, Trade, Finance) still match the live site exactly and remain ready to load the moment the Book online link is configured.
- Competitor services visibility is unchanged: Okoboji's Book online plus Macke's service/body-shop listing structure remain the local best practice.

## Description

### Public description signal (2026-10-26)
- No competitor exposed a full public description this run; the comparison remains action-signal-based (table above).
- The three grounded rewrites in `description-2026-08-17.md` remain valid and within the 750-char limit; their phone caveat is resolved (792-5000 correct). **Publish Version 2 (conversion-focused) in the same admin pass as the Book online CTA** — one edit session, two fixes.

## Photos

### Visible gallery floors (photo-viewer probe, 2026-10-26)
| Business | First visible dated label | Freshness read |
|---|---|---|
| **Motor Inn combined** | **Oct 2020** | **Weakest active** — 3rd straight week unchanged |
| Motor Inn Chevrolet | **May 2023** | Weak — unchanged |
| Chevrolet Parts sub-listing | Feb 2022 | Weak |
| Champion Ford | Oct 2018 | Weakest label in set (but inactive poster) |
| Wittrock | Jan 2023 | Moderate |
| Coleman / SL Ford CDJR | **Sep 2026** | **Best in set** |
| Okoboji Motor Co. | Dec 2022 | Moderate |
| Macke Motors | (service-led) | Aging |
| Choice Auto | Nov 2025 | Strong |
| Wilson Toyota | May 2026 | Strong |
| Rick Collins Toyota | Oct 2025 | Strong |
| Toyota of Des Moines | Oct 2025 | Strong |
| Fort Dodge Ford Lincoln | **Sep 2026** | Strong — moved Aug→Sep since 10-12 |

### Upload Plan (4 weeks, 9/week, 36 total) — carried, dates held
Naming `motorinn-[subject]-[location]-YYYY-MM-DD.jpg`, geotag Carroll (Spirit Lake/Okoboji only where real). Full plan: `content/drafts/gbp-photos/photo-plan-2026-10-12.md`.

- **Week 1 — Fall inventory, front of house (upload by Fri 2026-10-30):** 3 exterior/signage at 1526 Le Clark Rd; 4 current used SUV/truck photos; 2 sales-desk/team shots.
- **Week 2 — Service & parts proof (by Fri 2026-11-06):** 3 service bays working; 2 parts counter; 2 waiting-area; 2 intake/inspection.
- **Week 3 — Winter readiness (by Fri 2026-11-13):** 3 battery/wiper/tread closeups; 2 4WD/AWD inventory; 2 staff-with-customer; 2 entrance/hours.
- **Week 4 — Category reinforcement (by Fri 2026-11-20):** 2 Chevrolet-badged; 2 Toyota-badged; 2 Buick-adjacent if resolved; 3 community/dusk.

## Action Items (This Week)
1. **Upload Week 1 photos (9) by Fri 2026-10-30** — third reissue of the same batch; the gallery floors have not moved since 10-12. This remains the single highest-leverage structural fix.
2. **Add Book online CTA** to both sales listings → `serviceappmt.aspx`. Config change in admin; the services copy is already drafted.
3. **Reply cadence holds — nothing pending.** All 2026 reviews answered; keep same-day on the primary.
4. **Buick decision (Spencer, admin):** reopen `Buick at MOTOR INN OF CARROLL, L.L.C.` or merge it and set Buick dealer as a secondary category on both sales listings. Tenth week open.
5. **Duplicate shell:** claim/merge the review-less `Motor Inn Auto Group` listing (888 number) so the brand entity resolves canonically.
6. **Chevrolet review ask:** nine weeks flat at 37 on the 4.8 listing — add a review request to the Chevrolet delivery/checkout flow this week.
7. **Posts queue:** next posts per the velocity plan; the Oct 8 winter pkg stays live through the 31st; competitor owner posts (Coleman Bronco lease thru Nov 2, Wilson Tacoma thru Oct 31) justify an OFFER post this week.

## Sources
- `~/motor-inn-seo/audits/gbp-structural/gbp-research-2026-10-26.json` (EXA)
- `~/motor-inn-seo/audits/gbp-structural/reviews-pull-2026-10-26.json` (GBP API v4, both review-bearing locations, 2026-10-26)
- Live Google Maps scrapes 2026-10-26: `scrapes-2026-10-26/` (Motor Inn ×5 surfaces, 11 competitor lookups, About-tab attribute probes, photo-viewer date probes)
- `~/motor-inn-seo/content/drafts/gbp-posts/published-state.json` (15-post ledger)
- `content/drafts/gbp-services/services-2026-08-17.md`, `content/drafts/gbp-description/description-2026-08-17.md`, `content/drafts/gbp-photos/photo-plan-2026-10-12.md`
- `~/motor-inn-seo/audits/gbp-velocity/gbp-velocity-latest.md` (velocity baseline)
- `~/.agents/product-marketing-context.md`, `~/motor-inn-seo/tools/seomachine/config/competitors.json`
- `motorinnautogroup.com` service pages (live curl checks 2026-10-26)
