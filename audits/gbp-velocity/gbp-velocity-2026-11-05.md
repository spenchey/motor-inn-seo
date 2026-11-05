# GBP Velocity Audit — 2026-11-05

## Method note
- GBP API v4 via `mybusiness.googleapis.com/v4`, refresh-token flow from `~/.config/google-business-profile/credentials.json` on nada-mini. Raw pull archived: `audits/gbp-velocity/reviews-pull-2026-11-05.json` (both review locations, 50-row page on primary; full 37 on Chevrolet).
- Locations unchanged: primary **Toyota+Chevrolet of Carroll** (`14730652758503817758`, "7758"), **Chevrolet of Carroll** (`2099693230539902964`, "2964"), posts publisher `1983269944339166584` ("6584", historical).
- localPosts scan via owner account `115596490921363748880`, LIVE-state filter. Publisher dry-run checked (`parsed 6; 0 due; 0 unpublished`).
- Competitor panels: 2026 headless-browse restrictions from the nada-mini IP persist (Google SERP captcha, DDG anomaly loop, Yelp DataDome, BBB 403, Bing unquoted) — **ratings/counts carried from 10-26/08-27, flagged**; per standing practice, not re-scraped this run.
- EXA `marketing-content` re-run via `exa-preset.sh` produced no stdout this run (silent exit; noted below under carry-forward) — content angles carried from 10-22/10-29 findings, which remain directionally stable.

## Executive Summary
- **Review velocity: strong; October closed at 26 on the primary (best month on record; prior best Sep 26, Aug 18). Trailing-30d 20, 60d 41, 90d 48. Nov 1–5: 0 so far — normal early-month spacing, watch next week. P1 URGENT: no.**
- **Reply coverage: 100%. All 50 most-recent primary reviews have replies; zero unanswered inventory. The Oct 30 pair (Sandy, Trey) now fully answered — Trey's reply posted Nov 5 16:56 UTC during this cycle's window.**
- **Response lag: median ~30h / p90 ~5d across last-49 replied; Oct-since-20th cohort median ~46h. Within the standing 2-day target at median; p90 drifting vs the 10-01 1.25d median — worth a glance, not a process change.**
- **Posting: every slot through Nov 5 LIVE on both review listings (17 each) + 2 historical on 6584. Week-of-10-29 file (6 posts, Nov 10–27 slots) parsed 6/0-due/0-unpublished — nothing owed, ledger and live state agree.**
- **Voice: 11/20 of last-20 replies name staff/service/place by the strict matcher; hand-read shows the streak nearer 15–16/20 (short thanks-only replies are the miss). Slight dip from 19/20 — flag to GM path, not a crash.**
- **Chevrolet listing (2964): still flat at 37 reviews, zero new since Aug 28 — now ~10 weeks. Owner-side review-ask at delivery remains THE review action. Carried.**
- Star hygiene: last-20 replies sampled — star language matches record (incl. the Teresa 4★ fix). No mismatches found this run.

## 1. Review Teardown (API-exact 2026-11-05)
| Metric | Toyota+Chevrolet of Carroll (7758) | Chevrolet of Carroll (2964) |
|---|---|---|
| Total reviews (API) | **256** (+2 since 10-29) | **37** (flat ~10 wks) |
| Avg rating (listing) | 4.6 | 4.8 |
| Last-50 composition | 46×5★, 4×4★ (avg 4.92) | 32×5★, 4×4★, 1×2★ |
| 30 / 60 / 90-day | **20 / 41 / 48** | 0 / 0 / 1 |
| 2026 monthly | Sep 26 · **Oct 26 (record)** · Nov 0 MTD | Aug 1 · none since |
| Weekly (Mon-key, last 6) | 9/14:9 · 9/21:2 · 9/28:4 · 10/05:5 · 10/12:8 · 10/19:6 · 10/26:4 | — |

**Top themes in last-50 texted reviews:** service department quality (16), friendliness of staff (4+), speed/timeliness (3+), knowledge/professionalism (3), no-pressure sales, communication/follow-through, pickup-at-work convenience, phone-first handling of out-of-stock requests.

**Staff named (last 50):** Rick (2), Amy, Nate, plus merged theme Nate Pudenz. Staff-naming rate in reviews remains high — keep the ask attached to the advisor.

**Complaint themes:** none material — zero ≤3★ in last 60d on primary; single 2★ on Chevrolet dates to 2025. Quote-in-writing lesson (Aug) holding.

**5★ keyword phrases to train on (unchanged set, still correct):** great service · friendly staff by name · quick/timely · professional and knowledgeable · no pressure · straight answers · took care of everything.

### Competitor snapshot (CARRIED: ratings 10-26 scrape, counts 08-27 — not re-verified this run; see method note)
| Dealer | Rating | Count (carry) |
|---|---|---|
| Champion Ford Carroll | 4.2 | — |
| Wittrock Carroll | 4.6 | 262 |
| Coleman Co | 4.4 | — |
| Macke Motors | 3.8 | — |
| Okoboji Toyota | 4.5 | 1,012 |
| Wilson Toyota Ames | 4.7 | — |
| Rick Collins Toyota | 4.8 | — |
| Fort Dodge Ford Lincoln Toyota | 4.7 | — |
| Choice Auto Carroll | 4.4 | — |
| **Motor Inn (combined, volume-weighted)** | **≈4.65** | **293 (256+37)** |

Gap vs Wittrock (nearest count benchmark 262): −? — our 256+37=293 combined exceeds it on the combined listing; single-listing gap is a Chevrolet-listing problem (owner ask), not a velocity problem.

## 2. Review Response Analysis
- **Coverage:** 50/50 last-50 primary; 37/37 Chevrolet. **Zero unanswered.** Nothing to draft for immediate reply this run.
- **Lag:** median 30.1h, p90 127h (last-49 replied, lag<30d filter). Oct-20+ cohort: median 45.6h, p90 127h — the two long poles are weekend-spanning replies. Watch item only.
- **Reply activity since 10-30:** 2 (Sandy 5★ answered 10-31; Trey 5★ answered 11-05). Oct 28 Trey review sat 8 days before this reply — the p90 driver; no new gaps since.
- **Voice:** strict matcher 11/20; hand-read ~15/20 name service/staff/vehicle/place. Misses are 1-line thanks on textless 5★s. Keep the specific-anchor rule front of the GM path card.
- **Star hygiene:** verified across last-20 replies — star wording matches `starRating` incl. both 4★s. Closed loop.
- **Negative handling:** nothing to triage; zero ≤3★ in 60d.
- **Templates:** standing set (10-29) remains valid; no new variations required — all rules hold (unique first words, no "We appreciate your feedback", exact star counts). No new template file issued; `responses-2026-10-29.md` is current.

## 3. GBP Posts Audit (API localPosts, 2026-11-05)
| Surface | LIVE | Newest LIVE |
|---|---|---|
| 7758 (review listing A) | 17 | 2026-10-29 batch — 6 posts, slots Nov 10–27, all live incl. future-dated |
| 2964 (review listing B) | 17 | mirrored, same set |
| 6584 (publisher listing) | 2 visible in window | 2026-10-08 (historical only) |

- Publisher dry-run 2026-11-05: `parsed 6; 0 due; 0 unpublished`. **Ledger (29 entries) == live state. Nothing owed through Nov 27.**
- All posts STANDARD topicType; CTA mapping correct (CALL/BOOK/LEARN_MORE/SHOP per file).
- Oct 15 OFFER posts aged out of the visible window naturally; no action.

## 4. Posting Pattern Forensics
1. **Cadence: 17 live per review listing, slots through Nov 27 covered, zero gaps since the 10-08 publisher restart. The Sep-style drought is now 4 weeks dead.**
2. **Batch verification loop works:** 10-29 file → published 10-29/11-05 window → dry-run 0-due. Keep Thursday as the single clearing point.
3. **Angle rotation holding:** freeze/tires → deer/brakes → trade-window → Thanksgiving travel → Black Friday used → family-service. Next block (this run) rotates to cold-start economics / gift-deadline / pre-travel service / year-end trade tax angle / winter tire myth / parts stocking.
4. Competitor posting baselines unchanged (08-27/10-19 carry, structural audit re-verified activity 10-19).
5. **EXA `marketing-content` carry (10-29 run, 10 sources):** weekly minimum posting, concrete time-bounded offers, 100–150 words + matched CTA; answer-shaped copy for AI Overviews; link IG/FB in GBP settings (owner settings change — carried, untouched).

## Action Items
1. ~~Reply backlog~~ — **none; 100% coverage.**
2. ~~Publish due posts~~ — **none due through Nov 27.** Next block (weeks of 11-30/12-07) drafted this run: `content/drafts/gbp-posts/posts-week-of-2026-11-05.md`.
3. **Chevrolet review ask (owner, ~10 weeks):** 37 flat since Aug 28. Add review ask to Chevrolet delivery/checkout. Highest-leverage review action; unchanged.
4. **Nov watch:** 0 reviews Nov 1–5 on primary. If the week of 11-09 closes <3, re-check the ask flow at both desks before flagging.
5. **p90 reply lag** (8-day Trey gap) — weekend coverage glance only; medians healthy.
6. **Voice dip 19→~15/20:** remind GM path: name the service, the vehicle, or the human, every reply.
7. **P1 URGENT: no.** #seo-monitoring not paged.

## Sources Used This Run
- GBP API v4 pulls 2026-11-05 ~15:00 CT from nada-mini: reviews both locations (`reviews-pull-2026-11-05.json` archived), localPosts ×3 listings, publisher `--dry-run`.
- Prior audits `gbp-velocity-2026-10-29.md` / `2026-10-22.md` for baselines and carried items.
- Competitor ratings: 10-26 scrape carry + 08-27 counts, flagged unverified this run (headless browse restrictions, see method note).
- EXA preset: silent-run carry from 10-29 findings (this run's invocation produced no output; noted, not blocking).
