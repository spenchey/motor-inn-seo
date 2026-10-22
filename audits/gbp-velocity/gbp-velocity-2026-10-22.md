# GBP Velocity Audit — 2026-10-22

## Method note
- GBP API v4 via `mybusiness.googleapis.com/v4`, refresh-token flow from `~/.config/google-business-profile/credentials.json` (the stored access token is empty — always refresh). Pull data on nada-mini at `/tmp/gbp-audit-data-1022.json` (raw), this audit written from it.
- Locations unchanged: review-bearing primary **Toyota+Chevrolet of Carroll** (`14730652758503817758`) and **Chevrolet of Carroll** (`2099693230539902964`); posts publisher listing `1983269944339166584` (still zero reviews).
- Both accounts mirror the same locations; dedupe by (reviewer, createTime) before counting — the raw pull double-counts.
- Competitor panels not re-scraped (no API access); 08-27 baselines carried, flagged as such. Structural findings cross-checked against `audits/gbp-structural/gbp-structural-2026-10-19.md` (same week).

## Executive Summary
- **Review velocity: strong. 21 reviews in 2026 MTD on the primary listing (Sep closed at 25).** Oct is pacing to be the best month since the program started. The mid-August ask remains the engine; P2 maintain. **P1 URGENT: no.**
- **Reply discipline: 46/50 of the last-50 primary reviews have replies; median lag ~1.2d, p90 ~4.9d.** The four gaps (Dennis Deist, Amy Bice, Troy Kluender, Paula Cross — all 5★, Oct 17–21) were **answered live during this run and verified**. 2026 reply coverage is back to 100%.
- **Posting gap from the 10-08 audit is closed and holding:** the Oct 12/15 winter-readiness pair went live on the review listings and this run cleared the last two due posts from the 10-15 queue (Oct 20 + Oct 22 slots) — both verified LIVE. The 4-post week-of-10-15 queue is now fully published.
- **Reply voice continues to improve:** 15 of the last 16 replies name a service/staff/place/vehicle — best on record (2/20 → 6/20 → 15/16).
- **One recurring nit:** the Joyce Dickinson 4★ reply (Oct 7) says “5 star review … to get a 5 star review.” Star-count mismatch persists in GM-manual replies; keep the exact star value in the draft header (standing item).
- **Chevrolet listing still flat at 37 reviews since late August** — now ~8 weeks. The 4.8 listing is an asset idling; the structural audit’s delivery-flow review ask is the fix. Carried, owner action.

## Review Velocity
### Motor Inn (API-exact, 2026-10-22)
| Metric | Toyota+Chevrolet of Carroll | Chevrolet of Carroll |
|---|---|---|
| Total reviews (API) | **251** (+5 wk; 246 on 10-19) | **37** (flat ~8 weeks) |
| Avg rating (last 50) | **4.94** | 4.8 (listing) |
| Last 50: ratings | 48×5★, 2×4★ | — |
| Last 50: replied | **50/50 after this run’s 4 replies** | 37/37 |
| 2026 monthly | Jul —, Aug 4, Sep 25, **Oct 21 MTD** | Aug 1, since — none |

### Gap analysis (competitor baselines carried from 08-27 — NOT re-verified)
- Spirit Lake Ford benchmark 370 vs Motor Inn combined API **288** (251+37). Gap ≈ 82, shrinking ~1/month at current net. **P2 maintain.**
- Volume-weighted avg ≈ 4.65 across both listings.

## Review Response Analysis
- **Lag:** median ~1.2d, p90 ~4.9d on the primary (last 50). Healthy; no process change needed.
- **Unanswered inventory:** zero after this run. The four 2026 gaps were closed with replies posted 2026-10-22 ~20:15–20:30 UTC and verified by listing re-pull.
- **Voice regimes:** the specific-reply pattern (name the service/vehicle/staff/place) now dominates — 15/16 of last-20 replies. Recent exemplars: Wendy B (pickup at work), Grace (vehicle hunt), Peter Poland (names Amy/Nate/Wayne), Kim Pfannkuch (fast service). The two GM-signed formulaic replies (Karen Louise, Jean Lambertz) are polite but generic; acceptable tail.
- **Errors:** 1 star-count mismatch in last 20 (Joyce Dickinson 4★ answered with “5 star” language — a repeat of the Don Herrig pattern from 10-01). Draft template already keys off the true star; the manual path keeps drifting. Standing fix stands.
- **Negative handling:** no 1–3★ since Charles McGinn (Oct 2025, answered). Nothing to triage.

## GBP Posts Audit (API, localPosts)
| Surface | LIVE | Newest |
|---|---|---|
| Review listings (both) | 6 each | **2026-10-22** tire-check post (this run) |
| Publisher listing | 7 | 2026-10-08 (historical; review-listing copies are the live surface — matches the 10-08/10-15 pattern) |

- **Published this run (verified LIVE + searchUrl issued):** “The First Freeze Is A Vehicle Audit You Do Not Have To Fail” (Oct 20 slot, BOOK) and “What Your Tires Are Telling You At Every Stoplight” (Oct 22 slot, CALL) — each to both review-bearing listings.
- **Queue after this run:** Oct 25 Sunday flex (“The Trade-In Question Worth Asking Before Year-End”, trade-in CTA) remains **scheduled, not yet due** — the publisher needs a run on/after Oct 25. Then the week-of-10-26 slate below.
- **Publisher fix shipped this run:** `publish-gbp-posts.mjs` CTA_MAP lacked `book appointment`; added (mapped to BOOK, same as `book now`). The Oct 20 fatal is gone; ledger at 20 entries.
- **Types:** all STANDARD updates on the live surface; the OFFER-type winter-readiness package (expires Oct 31) went out Oct 15 and stays up through month end.

## Posting Pattern Forensics
1. **Cadence held:** 10-12, 10-15 (×2), 10-20, 10-22 — five posts in ten days across the paired listings, Tue/Thu core + Oct 25 flex queued. The Sep-style gap has not recurred since the publisher resumed 10-08.
2. **Timing drift is gone:** Oct 20 slot published Oct 22 (2-day drift, acceptable); the Oct 22 slot same-day. Keep the weekly Thursday run clearing due posts and the drift bound stays ≤3 days.
3. Competitor baselines unchanged (08-27 carry): Spirit Lake Ford 370 · Wittrock 262 · Okoboji Toyota 1,012. Structural audit 10-19 re-verified competitor *activity* (Coleman Sep 2026 photos, Wilson owner posts) — our structural gaps are there, not here.
4. EXA `marketing-content` re-run 2026-10-22 (10 sources, hotel-vertical heavy — treat as directional): consistent with three prior runs — **weekly minimum posting, concrete time-bounded offers, 100–150 words, matched CTA destination, answer-shaped copy that AI search can quote**; GBP now feeds AI Overviews/local recommendations directly, so the straight-answer copy pattern (which our posts already use) is the right shape. New nuance: connect IG/FB in GBP settings so social posts surface on the profile (carried from 10-08; owner settings change, not this run’s remit).
5. Seasonal window on schedule: first frost mid-Oct Carroll (hit this week), harvest running, winter-prep urgency real and now fully reflected in the live posts. Late-October → November angles: trade-in before year-end, 4WD/AWD need, service-before-travel Thanksgiving lane.

## Action Items
1. ~~Reply to the four unanswered 5★ reviews~~ — **done this run**, all four verified via re-pull. 2026 coverage 100% again.
2. ~~Publish due posts~~ — **done this run** (Oct 20 + Oct 22 slots live). **Owner action unchanged: run the publisher on/after Oct 25** for the Sunday flex post, or fold it into next Thursday’s run (Oct 29) — the flex post ages gracefully.
3. **Star-count mismatch (standing):** Joyce Dickinson-style “5 star” on a 4★. Keep exact star value in the daily draft header; GM manual path keeps drifting.
4. **Voice convergence:** 15/16 — bar met this cycle; keep the specific-reply pattern as default in drafts.
5. **Chevrolet review nudge (owner, carried ~8 weeks):** 37 flat since late August on the 4.8 listing. Add the review ask to Chevrolet delivery/checkout. Highest-leverage review action available.
6. **Structural handoffs (from 10-19 audit, unchanged):** Week 1 photo batch due **Fri 2026-10-23** (tomorrow); Book-online CTA; Buick listing decision; duplicate shell claim. Not repeated here — see that audit.
7. **P1 URGENT: no.** Velocity strong, zero unanswered, lag single-digit. #seo-monitoring not paged.

## Keyword Phrases for Review Requests
great service · easy process · friendly staff by name · worth the drive · straight answers · no pressure

## Sources Used This Run
- GBP API v4 pulls 2026-10-22 ~20:00–20:45 UTC: reviews both locations (`/tmp/gbp-audit-data-1022.json`), localPosts all three listings, four reply PUTs + verification re-pull, two localPosts creates + verification.
- `publish-gbp-posts.mjs --limit 4` (ledger `content/drafts/gbp-posts/published-state.json`, now 20 entries; CTA_MAP `book appointment` fix included in commit).
- EXA `marketing-content` preset 2026-10-22 via `~/clawd/scripts/no-model/exa-preset.sh` (10 sources).
- Prior audits `gbp-velocity-2026-10-08.md`, `gbp-structural-2026-10-19.md` for baselines and carried items.
