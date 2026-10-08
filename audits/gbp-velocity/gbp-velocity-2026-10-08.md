# GBP Velocity Audit — 2026-10-08

## Method note
- Same credential stack as the 2026-10-01 run: GBP API v4 via `mybusiness.googleapis.com/v4`, owner-OAuth + configured fallback (`~/.config/google-business-profile/credentials.json`), pull script retained at `/tmp/gbp-audit-pull-1008.js` on nada-mini. Data is API-exact, not screen-scraped.
- Locations: **Motor Inn Toyota and Chevrolet of Carroll** (locations/14730652758503817758, review-bearing primary) and **Motor Inn Chevrolet of Carroll** (locations/2099693230539902964). Posts live on the publisher listing (locations/1983269944339166584, zero reviews — unchanged).
- The stock `scripts/velocity-pull.js` still queries only the posts-publisher listing and returns 0 reviews on every credential; the 10-01 one-off pattern (per-location, both accounts) remains the working path.
- Competitor panels not re-scraped this cycle (API has no competitor review access); 08-27 baselines carried forward and flagged.

## Executive Summary
- **Review velocity: holding. 7 reviews Oct 1–8 on the primary listing** (Sep closed at 26, Aug 18). Run rate ~24/month — the mid-August ask is still working. **P2 maintain; not P1.**
- **Reply discipline: 50/50 of the last-50 primary reviews have replies**; median lag ~1.3 days (p90 6.6d). Healthy.
- **The one open action from 10-01 — john ross (4★, Aug 28, no text, 41 days) — is closed:** owner reply posted today 2026-10-08 20:05 UTC and verified live via re-pull.
- **Posting gap CLOSED.** Nothing had been live since Sep 21; today's run published the two due posts from the Oct 6–17 queue (both verified LIVE). 4 remain scheduled through Oct 18.
- **Reply quality is now the only thread:** 2 star-count mismatches in the last 20 (4★ answered as "5 Star"), and the GM voice remains formula-leaning (6/20 replies name a service/staff/place).

## Review Velocity

### Motor Inn (API-exact, 2026-10-08)
| Metric | Toyota+Chevrolet of Carroll | Chevrolet of Carroll |
|---|---|---|
| Total reviews (API) | **236** (+6 wk) | **37** (flat) |
| Avg rating (API) | **4.6** | **4.8** |
| Last 50: ratings | 46×5★, 4×4★ | 32×5★, 4×4★, 1×2★ |
| Last 50: replied | **50/50** | 36/37 (john ross → replied today) |
| Reviews since Oct 1 | 7 | 0 |
| Monthly since Jul | Jul 5 · Aug 18 · Sep 26 · Oct 7 | Aug 1 |

### Gap analysis (competitor baselines carried from 08-27 — NOT re-verified)
- Spirit Lake Ford benchmark: 370. Motor Inn combined API total: **273**. **Gap ≈ 97.**
- At ~24/month observed, closure in **~4 months** if the benchmark is static. **Status: P2 — keep the ask at current strength.**
- Combined volume-weighted avg rating: ≈ 4.63.

## Review Response Analysis
- **Lag:** median ~1.3d, p90 6.6d on the primary listing (the 2016-era max is a legacy outlier, not a process signal). Chevy sublisting medians are historical; its only fresh unanswered item is now handled.
- **Unanswered inventory:** zero unanswered reviews dated 2024+ across both listings after today's john ross reply. Older unanswered (2023 and earlier, incl. the one 1★ "S Fans") sit outside the daily pipeline's window — a one-off backlog sweep is optional, not urgent.
- **Voice regimes:** unchanged from 10-01. GM replies (Bremser) prompt but formulaic; the specific-reply pattern (name the service/vehicle/staff) appears in only ~6 of the last 20. Recent positives: Shelby Baumeiner (names Kyle), Brad Benton (service), Jerry Rupiper (names Nathan + Amy).
- **Errors to stop — star-count mismatches persist:** Joyce Dickinson and Don Herrig, both 4★, replied to as "5 Star review." Don Herrig's is a repeat from the 10-01 finding. The daily draft template keys off the actual star value; manual GM replies keep guessing.
- **Negative handling:** no new 1–3★ since Charles McGinn (Oct 2025, answered). Nothing to triage.

## GBP Posts Audit (API, localPosts on the publisher listing)
| Metric | Finding |
|---|---|
| LIVE posts now | **7** (5 from the Sep block + 2 published today) |
| Today's publishes | "The Battery Test Before The First Hard Freeze" (Oct 6 slot) and "Winter Prep For The Family Hauler" (Oct 8 slot) — both state LIVE, searchUrl issued |
| Types | All STANDARD; the OFFER-type winter-readiness post is queued Oct 15 |
| Cadence | Tue/Thu core + Sunday flex, per the 10-05 draft plan. Remaining queue: Oct 13, 15, 17 + Oct 18 flex |

## Posting Pattern Forensics
1. **Publisher mechanism confirmed end-to-end again:** `publish-gbp-posts.mjs --limit 2` published both due posts first try; ledger updated (`published-state.json`, 7 entries). The Sep gap was pipeline idle time, not breakage — the fix is simply running the publisher on schedule.
2. **The Oct 6/8 posts went out 2 days and 0 days after their nominal dates** — same-day-plus drift is acceptable; the Oct 13/15/17 trio needs the next run (or a daily cron hook on the publisher) to land on time.
3. Competitor baselines unchanged (08-27 carry-forward): Spirit Lake Ford 370 · Wittrock 262 · Okoboji Toyota 1,012. No fresh panels — marked N/V rather than guessed.
4. EXA `marketing-content` re-run 2026-10-08 (10 sources). Signals consistent with 10-01 and now triple-confirmed: **concrete time-bounded offers beat vague ones**; **Tue–Thu peak engagement**; **100–150 words, matched CTA destination**; **GBP copy now feeds AI search summaries — answer-shaped beats promotional**. New nuance this cycle: Google's "Social Media Updates" carousel pulls connected Instagram/Facebook posts into the profile — worth connecting the dealer accounts when the marketing team next touches GBP settings (no action taken; not in this run's remit).
5. Seasonal window unchanged: first frost mid-Oct Carroll, harvest running, winter-prep urgency real. The queued copy already carries it.

## Action Items
1. ~~Reply to john ross~~ — **done today**, verified live.
2. ~~Close the posting gap~~ — **done today** (2 published, 4 queued). **Owner action: ensure the publisher runs on/after Oct 13** so the remaining dated posts land; a daily `publish-gbp-posts.mjs` hook (idempotent, ledger-guarded) is the durable fix.
3. **Star-count mismatch fix:** the GM's manual replies keep miscounting stars (2 more this cycle). Fold the exact star value into the daily draft header so the human copy step can't drop it — the drafted replies already carry it.
4. **Voice convergence (standing):** nudge GM replies toward the specific-reply pattern; 6/20 is better than the 10-01 baseline but not the bar.
5. **Optional backlog sweep:** ~8 unanswered 2023-and-earlier reviews on the primary listing. Low value, zero risk — only if idle capacity appears.
6. **P1 URGENT: no.** Velocity healthy, zero unanswered 2024+ reviews, lag single-digit days. #seo-monitoring not paged.

## Keyword Phrases for Review Requests
- great service · easy process · friendly staff by name · worth the drive · straight answers · no pressure

## Sources Used This Run
- GBP API v4 pulls 2026-10-08 ~15:00–15:10 CDT: reviews for both locations (`/tmp/gbp-audit-data-1008.json`), localPosts on the publisher listing, one reply PUT (john ross) + verification re-pull, two localPosts creates + verification.
- `publish-gbp-posts.mjs --limit 2` (ledger `content/drafts/gbp-posts/published-state.json`).
- EXA `marketing-content` preset, 2026-10-08, via `~/clawd/scripts/no-model/exa-preset.sh` (10 sources).
- Prior audit `gbp-velocity-2026-10-01.md` for baselines and open-item carry.
