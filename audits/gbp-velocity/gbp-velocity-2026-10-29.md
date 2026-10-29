# GBP Velocity Audit — 2026-10-29

## Method note
- GBP API v4 via `mybusiness.googleapis.com/v4`, refresh-token flow from `~/.config/google-business-profile/credentials.json` on nada-mini (`/Users/spencerheywood`). Raw pull archived at `audits/gbp-velocity/reviews-pull-2026-10-29.json`; localPosts scan at `audits/gbp-velocity/localposts-scan-2026-10-29.json`.
- Locations unchanged: review-bearing primary **Toyota+Chevrolet of Carroll** (`14730652758503817758`, "7758") and **Chevrolet of Carroll** (`2099693230539902964`, "2964"); posts publisher listing `1983269944339166584` ("6584", historical only, zero reviews).
- No review duplicates in the pull (0 of 254 on a (author, createTime) key check).
- Competitor panels: 10-26 scrape snapshots on nada-mini (`/tmp/gbp1026/*.txt`) give ratings only (no review counts surfaced in the limited Maps view). 08-27 count baselines carried, flagged as such — unchanged practice.
- Note: `/tmp` artifacts on nada-mini are pruned aggressively; both JSONs now live in the repo.

## Executive Summary
- **Review velocity: strong and still the best program stretch on record.** 24 reviews October MTD on the primary (Sep closed 26, Aug 18). Trailing-30d = 25, trailing-60d = 50. **P1 URGENT: no.**
- **Reply discipline: 49/50 of last-50 primary reviews had replies coming into this run; the one gap (Teresa Quass, 4★, Oct 28, no text) was answered during this run and verified. 2026 reply coverage is 100% again.**
- **Star-count hygiene improved:** Joyce Dickinson's 4★ (Oct 7) is now correctly answered as a "4 Star review" (the earlier Don Herrig 4★-as-5★ pattern did not recur in the last 25 replies). GM manual path holding.
- **Posting: every slot through Nov 5 is LIVE** on both review-bearing listings — the 10-22 week file (6 posts incl. the carried flex) fully published and verified. Nothing due remains unpublished; publisher dry-run confirms 0 pending.
- **Voice: 19/20 of last-20 replies name a service/staff/place/vehicle** — best yet (2/20 → 6/20 → 15/16 → 19/20).
- **Chevrolet listing still flat at 37 reviews** — now ~9 weeks with zero new reviews and no owner-side movement on the delivery-flow ask. Highest-leverage review action available; carried, owner action.

## 1. Review Teardown (Motor Inn, API-exact 2026-10-29)
| Metric | Toyota+Chevrolet of Carroll | Chevrolet of Carroll |
|---|---|---|
| Total reviews (API) | **254** (+3 wk; 251 on 10-22) | **37** (flat ~9 weeks) |
| Avg rating (listing) | 4.6 | 4.8 |
| Last-50 avg | **4.92** (46×5★, 4×4★) | — |
| Last-50 replied | 49/50 → **50/50 after this run** | 37/37 |
| 30 / 60 / 90-day | **25 / 50 / 68** | 0 / 0 / 1 |
| 2026 monthly | Aug 18 · Sep 26 · **Oct 24 MTD** | Aug 1 · since — none |

Weekly cadence (primary, last 8 full weeks): 8, 7, 4, 3, 6, 4, 10, 3 — average ~5.6/week; the mid-August ask remains the engine.

**Top services mentioned (last 90d, texted reviews):** service department generally (16), oil change (3), tires, brakes, pickup/delivery, battery. Sales-side: vehicle found/ordered, trade-in, no-pressure.

**Staff named (last 90d):** Nate/Nathan (Pudenz/Sporrer merged theme, 10), Amy (3), Matt (3), Kyle (2), Wayne, Rick, Lisa (1 each).

**Geographic mentions:** light — Carroll ×2 in 90d; reviews are service-led, not place-led. No surrounding-town names in the window.

**Negative/complaint themes (last 120d):** essentially none — zero 1–3★ since Oct 2025; the only friction signal is the Aug 13 service-department quote-vs-invoice episode, which was fully remediated (refund received 8/17, reviewer satisfied) and produced the standing "quote in writing" lesson.

**5★ keyword phrases to train customers on:** great service · friendly staff (by name) · quick/timely service · professional and knowledgeable · no pressure · straight answers · took care of everything.

### Competitor snapshot (ratings from 10-26 Maps scrapes; counts = 08-27 carry, NOT re-verified)
| Dealer | Rating now | Count (8-27 carry) |
|---|---|---|
| Champion Ford Carroll | 4.2 | — |
| Wittrock Carroll | 4.6 | 262 |
| Coleman Co | 4.4 | — |
| Macke Motors | 3.8 | — |
| Okoboji Toyota | 4.5 | 1,012 |
| Toyota of Des Moines | 4.6 | — |
| Wilson Toyota Ames | 4.7 | — |
| Rick Collins Toyota | 4.8 | — |
| Fort Dodge Ford Lincoln Toyota | 4.7 | — |
| Choice Auto Carroll | 4.4 | — |
| **Motor Inn (combined, volume-weighted)** | **≈4.65** | **291 (254+37)** |

## 2. Review Response Analysis
- **Lag:** median ~1.25d, p90 ~5.3d (last 39 replied) — unchanged from 10-22; healthy, no process change.
- **Unanswered inventory:** the single 2026 gap (Teresa Quass 4★, Oct 28) was closed this run — reply PUT 200, verified via listing re-pull (`REPLIED 2026-10-29`). Reply text states "four stars" matching the record.
- **Voice:** 19/20 name service/staff/place; the one miss is a short Aug 17 thanks. Streak is a standing habit, not a fluke — keep it.
- **Star-count match:** last-25 replied reviews show correct star language (Joyce 4★ fixed Oct 7). Standing item resolved in practice; keep the star value in draft headers.
- **Negative handling:** nothing to triage — zero ≤3★ in 60d.

## 3. GBP Posts Audit (API localPosts, 2026-10-29)
| Surface | LIVE | Newest LIVE |
|---|---|---|
| 7758 (review listing A) | 11 | **2026-10-22 batch** — incl. Deer Season (10-29 slot), Preheat (10-27), Trade-In (10-25), Winter-vehicle (11-03), Parts counter (11-05) all LIVE now |
| 2964 (review listing B) | 11 | same set, mirrored |
| 6584 (publisher listing) | 7 | 2026-10-08 (historical; review-listing copies are the live surface) |

- All 7 posts of the 10-22 week file are LIVE on both review listings; topicType STANDARD throughout; CTAs correctly mapped (CALL ×3, BOOK ×2, SHOP, LEARN_MORE).
- `publish-gbp-posts.mjs --dry-run`: "parsed 5; 3 due; 0 unpublished" — **ledger and live state agree; nothing owed.**
- The Oct 15 winter-readiness OFFER posts expired on schedule Oct 31 window (still LIVE, fine — Google leaves STANDARD/OFFER up; no action).

## 4. Posting Pattern Forensics
1. **Cadence held through the busiest stretch:** 10-12 (×2), 10-15 (×2 + offer), 10-22 (×7 batch incl. future-dated slots). Effective publish dates run 10-20 → 11-05 with no gap; the Sep-style drought has not recurred since the publisher resumed 10-08.
2. **Batching works:** the 10-22 seven-post batch cleared two weeks of slots in one run and all posts verified LIVE. Keep Thursday runs as the single clearing point; drift ≤3d bound intact (future-dated slots go live immediately per Google behavior — noted, harmless).
3. **Angle rotation on schedule:** freeze/tires → trade-in → preheat economics → deer/brakes → Thanksgiving travel → 4WD used → parts counter. Service, inventory, and FAQ alternated; no two consecutive posts same angle.
4. Competitor activity baselines unchanged (08-27 carry; 10-19 structural audit re-verified activity). Our gap is Chevrolet-listing reviews + Spirit Lake photos, both owner-side.
5. **EXA `marketing-content` re-run 2026-10-29 (10 sources, hotel-vertical heavy — directional only):** same three constants as prior runs — weekly minimum posting, concrete time-bounded offers, 100–150 words with matched CTA. The answer-shaped-copy pattern (AI Overviews quote GBP posts) remains correct; our posts already lead with concrete claims. New nuance repeated: connect IG/FB in GBP settings so social posts surface on the profile — owner settings change, carried.

## Action Items
1. ~~Reply to Teresa Quass 4★~~ — **done this run**, verified.
2. ~~Publish due posts~~ — **none due; week fully live through Nov 5.** Next content block (week of 11-09) drafted this run — see `content/drafts/gbp-posts/posts-week-of-2026-10-29.md`.
3. **Chevrolet review ask (owner, ~9 weeks):** 37 flat since late August. Add the review ask to Chevrolet delivery/checkout. Unchanged; still the highest-leverage review action.
4. **Star hygiene:** holding; keep exact star value in draft headers.
5. **Structural handoffs:** per 10-19 audit — photo batch, book-online CTA, Buick listing decision, duplicate shell claim. Not repeated here.
6. **P1 URGENT: no.** Velocity strong, zero unanswered, lag single-digit. #seo-monitoring not paged.

## Keyword Phrases for Review Requests
great service · friendly staff by name · quick and professional · no pressure · straight answers · worth the drive

## Sources Used This Run
- GBP API v4 pulls 2026-10-29 ~15:00–15:40 CT from nada-mini: reviews both locations (`reviews-pull-2026-10-29.json`), localPosts ×3 listings, one reply PUT + verification re-pull, publisher dry-run.
- `publish-gbp-posts.mjs --dry-run` (ledger `published-state.json` at 29 entries; all 10-22-week slots present and verified LIVE).
- Competitor ratings: 10-26 Maps scrapes `/tmp/gbp1026/*.txt` (counts carried from 08-27, flagged).
- EXA `marketing-content` preset 2026-10-29 via `~/clawd/scripts/no-model/exa-preset.sh` (10 sources).
- Prior audit `gbp-velocity-2026-10-22.md` for baselines and carried items.
