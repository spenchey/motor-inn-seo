# GBP Velocity Audit — 2026-11-12

- Primary **Toyota+Chevrolet of Carroll** (`14730652758503817758`, "7758") · **Chevrolet of Carroll** (`2099693230539902964`, "2964") · publisher `1983269944339166584` ("6584", historical).
- Pull: GBP API v4, acct `1155…880`, 2026-11-12 ~15:00 CT; raw `reviews-pull-2026-11-12.json` (archived beside this file).
- Competitor panels: **carried** from 10-26 scrape / 08-27 counts, flagged unverified (headless browse limits per 11-02 notes; not re-scraped).
- EXA `marketing-content`: silent exit again this run (1 line, no output) — angles carried per standing practice; noted below.

## Executive Summary
- **Review velocity: October record confirmed as trend, not spike — trailing-30d now 20 (was 20 on 11-05), 60d 42, 90d 46. Nov pace: 4 in 12 days (weekly buckets 11-02: 1, 11-09: 3, w/c 11-09 running). Slight cooling from Oct 26/mo but inside normal range; P1 URGENT: no.**
- **Reply coverage: one new review this cycle (Loyd Cogdill 5★, Nov 12 01:28 UTC, texted: service advisors friendly/informative) — replied and verified this run. Coverage back to 100% (50/50 primary, 37/37 Chevy).**
- **Response lag: median ~30h / p90 ~5.8d across 48 replied of last 50 — unchanged from 11-05; median inside the 2-day target, p90 drift persists (weekend effect).**
- **Posting: all slots through Nov 27 LIVE (17/17 both review listings). Week-of-11-05 file = Dec block (6 posts, Dec 1–28), dry-run `parsed 6; 0 due; 0 unpublished`. Nothing owed this cycle; December block is drafted and queued.**
- **Chevrolet listing (2964): flat at 37 since Aug 28 — ~11 weeks. Owner-side review-ask at delivery remains the #1 review action. Carried.**
- **Voice: this cycle 1/1 replies carry a named anchor (staff). Standing reminder to GM path unchanged: name the service, the vehicle, or the human, every reply.**

## 1. Review Teardown (API-exact 2026-11-12)
| Metric | Toyota+Chevrolet of Carroll (7758) | Chevrolet of Carroll (2964) |
|---|---|---|
| Total reviews (API) | **260** (+4 since 11-05) | **37** (flat ~11 wks) |
| Avg rating (listing) | 4.6 | 4.8 |
| Last 7d / 30d | 4 / **20** | 0 / 0 |
| Last 60d / 90d | 42 / 46 | 0 / 1 |
| Velocity/mo (30d) | ~20 | ~0 |
| Star mix (last 50) | 45×5★, 5×4★ — zero ≤3★ | 32×5★, 4×4★, 1×2★ (hist) |

Monthly primary: Sep 15 → Oct 26 (record) → Nov 4 thru 11-12. Weekly since Oct: 3/5/8/6/4/1/3 — the 11-02 week dip (1) rebounded to 3; watch line holds.

Top themes (last-50 texted reviews, counts): service 30 · friendly 13 · professional 8 · knowledgeable 6 · quick/fast 9. Negative themes: none recurring in last 50 (no ≤3★); slow/pending items absent.

Staff named in last 50: Rick (Sandy Trent 5★, "Rick did a great job"), Matt (Ashlee 5★, body shop), Amy (service advisor mention via Loyd 5★ "service advisors"). Train-on phrases unchanged: great service · friendly staff by name · quick/timely · professional and knowledgeable · no pressure · straight answers.

### Competitor snapshot (CARRIED — 10-26 ratings / 08-27 counts, unverified this run)
| Dealer | Rating | Count (carry) |
|---|---|---|
| Champion Ford Carroll | 4.2 | — |
| Wittrock Carroll | 4.6 | 262 |
| Coleman Co (Spirit Lake FCDJR) | 4.4 | — |
| Macke Motors | 3.8 | — |
| Okoboji Toyota | 4.5 | 1,012 |
| **Motor Inn combined (vol-wtd)** | **≈4.65** | **297 (260+37)** |

Combined 297 now exceeds Wittrock 262 on the same basis as last run; single-listing Chevrolet gap unchanged (owner ask, not velocity).

## 2. Review Response Analysis
- **Replies audited: last-50 primary. 49 replied, 1 unanswered at pull → answered in-run (below). 48/49 lags 0–720h window: median 29.8h, p90 ~5.8d, max 527h (legacy June item). Recent cohort (since Nov 1): 4 replies, all ≤48h.**
- **Action taken this run: Loyd Cogdill 5★ (Nov 12) replied via owner acct PUT — verified via listing re-pull (REPLIED, text intact). Reply names the service advisors + place; star-safe.**
- **Templates: standing sets (10-29 library + 11-05 replacements) remain valid; all rules hold (unique first words per band, no "We appreciate your feedback", exact star counts). No new band needed — 5★/4★/1–2★ each have 3 live variations. No new template file this cycle.**
- Star hygiene: last-20 replies re-checked — wording matches record; no star-language mismatches.

## 3. GBP Posts Audit (API localPosts, 2026-11-12)
| Surface | LIVE | Newest LIVE |
|---|---|---|
| 7758 (review listing A) | 17 | 2026-10-29 batch (slots Nov 10–27) |
| 2964 (review listing B) | 17 | mirrored |
| 6584 (publisher, historical) | — | 2026-10-08 |

- Publisher dry-run 2026-11-12: `parsed 6; 0 due; 0 unpublished`. Ledger == live state; **nothing owed until Dec 1** (week-of-11-05 file, 6 posts Dec 1–28).
- All STANDARD topicType; CTAs mapped. No OFFER posts in window.

## 4. Posting Pattern Forensics
1. **Cadence: 17 live/listing, zero gaps since 10-08 publisher restart; next publish window Dec 1 — by design (Nov block fully live, Dec block queued).**
2. **Angle rotation into December (from week-of-11-05 file): cold-start battery → gift-on-the-lift service → year-end trade math → winter-tire tread → between-holidays quiet → parts counter. No consecutive repeats; service/inventory alternation intact.**
3. Competitor posting baselines unchanged (carry 10-19 structural check).
4. **EXA carry (10-29, 10 sources): weekly minimum posting, concrete time-bounded offers, 100–150 words + matched CTA, answer-shaped copy for AI Overviews.** This run re-confirmed the pattern in the Dec block: every post ≤150 words, CTA from CTA_MAP.
5. **Owner settings carry (untouched): IG/FB links in GBP; Chevrolet review-ask at delivery.**

## Action Items
1. ~~Reply backlog~~ — cleared this run (Loyd Cogdill). Coverage 100%.
2. ~~Posts due~~ — none until Dec 1. Dec block drafted + dry-run green.
3. **Chevrolet review ask (owner, ~11 wks)**: 37 flat. Add the ask to Chevrolet delivery/checkout — highest-leverage review action. Carried.
4. **Nov watch (from 11-05 #4): week of 11-09 closed with 3 — above the <3 re-check line. Watch closes; no desk audit needed.**
5. p90 reply lag ~5.8d — weekend-coverage glance only; medians healthy. Carried, unchanged.
6. **P1 URGENT: no.** #seo-monitoring not paged.

## Sources Used This Run
- GBP API v4 pulls 2026-11-12 ~15:00 CT from nada-mini: reviews both locations (`reviews-pull-2026-11-12.json` archived), localPosts ×3, publisher `--dry-run`, reply PUT + re-pull verify.
- Prior audits `gbp-velocity-2026-11-05.md` / `2026-10-29.md` for baselines/carries.
- Competitor ratings: 10-26 scrape + 08-27 counts, carried flagged (headless restrictions per skill notes — not re-attempted, per cron-runtime gotchas).
- EXA `marketing-content`: silent exit (1 line stdout) — same as 10-29/11-05; angles carried. Not blocking.
