# GBP Velocity Audit — 2026-10-01

## Method note (migration)
- Runbook tool `gstack-browse` remains unavailable; this run used the **GBP API directly** (owner OAuth + configured fallback, same credential stack as the daily review-reply job) via a one-off pull script on nada-mini. Data below is from `mybusiness.googleapis.com/v4` + `mybusinessbusinessinformation.googleapis.com/v1` — not screen-scraped, so totals are exact, not panel estimates.
- Locations covered: **Motor Inn Toyota and Chevrolet of Carroll** (locations/14730652758503817758, the review-bearing primary listing) and **Motor Inn Chevrolet of Carroll** (locations/2099693230539902964). The posts-publisher listing (locations/1983269944339166584, "Motor Inn Auto Group") carries the localPosts and **0 reviews** — that is why the old 08-27 audit's "204 live reviews" figure does not match API counts; the two audits measured different listings.
- Competitor panels were not re-scraped this cycle (API has no competitor reviews access); 08-27 competitor baselines carried forward and flagged as such.

## Executive Summary
- **Review velocity is real and now precisely measurable: 47 reviews since Jul 1 on the primary listing** (2 in July, 18 in Aug, 26 in Sep, 1 so far in Oct). That is **~23/month across Aug–Sep** on the API surface. The mid-August review-ask re-energization is holding: Sep was the best month measured to date (26).
- **Reply discipline fixed itself.** Median reply lag on reviews since Jul 1 is **~1.0 day** (was 1–2 months in the 08-27 audit). Slowest recent reply was 6.9 days (Monica Schiltz). 49 of the last 50 primary-listing reviews have replies.
- **Reply quality is the remaining gap.** Owner replies (David Bremser) are prompt but overwhelmingly generic "Thank you … We appreciate you/your business" formulas; recent Jeeves-drafted replies (Chas, Ron Sitzmann) name the service and are noticeably better. Two templates now coexist on the listing; converge on the specific one.
- **Posting cadence confirmed from the API: 5 posts LIVE on the profile** (Sep 8, 10, 15, 17, 20 publish dates, all STANDARD updates). The 08-27 "0 visible posts" finding was a surface limitation — posts are live and the Tue/Thu cadence held through Sep 20. **Nothing has been published since Sep 21 — next 2 weeks (Oct 6–17) are the gap this run fills.**
- **Two unanswered reviews exist right now**: Jerry Rupiper (5★, Oct 1, names Nathan Pudenz + Amy) on the primary listing and john ross (4★, Aug 28, no text) on the Chevy sublisting — the latter is 34 days old.

## Review Velocity

### Motor Inn (API-exact, 2026-10-01)
| Metric | Toyota+Chevrolet of Carroll | Chevrolet of Carroll |
|---|---|---|
| Total reviews (API) | **230** | **37** |
| Avg rating (API) | **4.6** | **4.8** |
| Last 50: ratings | 47×5★, 3×4★ | 32×5★, 4×4★, 1×2★ |
| Last 50: replied | 49/50 | 36/37 |
| Reviews since Jul 1 | 47 (~23/mo Aug-Sep) | 1 (Aug 28) |
| Monthly volume | Jul 2 · Aug 18 · Sep 26 · Oct 1 | — |

### Gap analysis (baselines carried from 08-27 audit — competitor panels NOT re-verified this cycle)
- Spirit Lake Ford benchmark: 370 (08-27 figure). Motor Inn primary+Chevy API total: **267**. Gap ≈ 103 (was ~166 on the old surface match-up).
- At the observed ~23/month this closes in roughly 4–5 months if the benchmark stands still. **Velocity status: P2 (maintain the ask — it is working).**
- Combined avg rating across the two listings (volume-weighted): ≈ 4.64.

## Review Response Analysis (last 30 replies, primary listing)
- **Lag:** median ~1.0 day since Jul 1; p90 ≈ 2.5 days; worst recent 6.9 days. Fixed from the 1–2-month lag flagged 08-27. Status: healthy.
- **Two voice regimes are live on the listing:**
  1. Owner/GM replies (Bremser): prompt, warm, but formulaic — "Thank you [name] for the 5 star review! We appreciate you/your business very much! David Bremser-General Manager." Zero service/vehicle/place specificity. (Sue England, Arlis Bahnsen, Steve Dvorak, Jack Cue, Sarah Spiker, Scott Plendl, Geneva Rajski, Chris Goodwin.)
  2. Jeeves-drafted replies: name the exact service ("oil change and tire rotation"), reflect the reviewer's own words, sign "The Motor Inn team." (Chas, Ron Sitzmann.) This is the quality bar from the 08-27 templates and it is working — converge all replies on this pattern.
- **Specificity:** 17 of 49 last-50 replies mention Motor Inn/Carroll; ~2 name staff or service. The 08-27 rule ("every reply names a service, a vehicle line, or a place") is still not the default in the GM replies.
- **Errors to stop:** a 4★ review (Don Herrig) was answered with "Thank you for … 5 Star review" — mismatched star count reads sloppy. "Bahnsen's" apostrophe error. The "We appreciate you and your business" formula appears in most GM replies.
- **Negative handling:** only one 2★ in the fetched set (Charles McGinn, Oct 2025) — answered with the apology template. No fresh negatives to triage this cycle.

## GBP Posts Audit (API, localPosts on the publisher listing)
| Metric | Finding |
|---|---|
| Posts LIVE | **5** (created Sep 14/17/21, publish dates Sep 8/10/15/17/20) |
| Types | All STANDARD updates; no OFFER or EVENT types used yet |
| Cadence | Tue+Thu schedule held Sep 8–20; **no post since Sep 21** |
| Draft queue state | `posts-week-of-2026-09-07` fully published per `published-state.json` (5/5 LIVE) |

## Posting Pattern Forensics
1. **Our own cadence data beats competitor forensics this cycle:** the five Sep posts went out Tue/Thu and all reached LIVE state within 1–6 days of their publish dates. The mechanism works; the pipeline just stopped after Sep 20.
2. Competitor baselines (08-27, carried forward): Spirit Lake Ford 370 reviews / active surface; Wittrock 262; Okoboji Toyota 1,012. No fresh competitor panels this run — marked N/V rather than guessed.
3. EXA `marketing-content` research re-run 2026-10-01 (5 fresh sources). Signals that change this week's copy:
   - **GBP is now a grounding source for AI search** (Quické Marketing on Google's 2026 industry playbooks; Nullstacks on profiles feeding AI summaries/Ask Maps): specific, structured, answer-shaped post copy beats promotional fluff — write posts that answer the questions buyers actually ask.
   - **Time-limited, concrete offers convert; vague ones get ignored** (Piedmont Avenue: "10% off oil changes this week" > "discounts available"). Oct theme: winter-prep service with a concrete window.
   - **Tuesday–Thursday remains the engagement peak**; weekend only as flex. Consistent with our own Tue/Thu results.
   - **100–150 words, image reinforces message, CTA button mandatory, CTA destination matched to intent** — reconfirms the standing house rules.
   - Note: Sterling Sky testing (via nadacreative) shows posts don't move *pack ranking* — they drive engagement/CTR on the listing surface. Set expectations accordingly: we post for the humans on the profile, not the algorithm.
4. October seasonal window (house calendar): **fall maintenance → winter prep, harvest-season truck service, new model year.** First frost typically mid-October in Carroll — battery/heat/defrost/tire urgency is real now, and harvest is still running.

## Action Items (This Week)
1. **Reply to the two open reviews today** — Jerry Rupiper (names Nathan and Amy; use the staff-naming template) and john ross (4★, no text, 34 days old; use the 4-star acknowledgment template). Templates attached in this run's responses file.
2. **Close the posting gap:** publish the Oct 6–17 queue drafted this run (6 posts, Tue/Thu, one OFFER-type post among them). Nothing live since Sep 21.
3. **Converge reply voice:** ask David Bremser to adopt the Jeeves-drafted pattern — name the service/vehicle/staff the reviewer mentioned, skip "We appreciate you and your business," fix star-count mismatches. The daily draft loop already produces this quality; use its drafts.
4. Keep the review ask running at current strength — ~23/month is the observed rate and it holds the gap-closure path. No change.
5. **P1 URGENT: no.** Nothing in this cycle's findings meets the P1 bar (velocity healthy, no unanswered negative, lag fixed). #seo-monitoring not paged.

## Keyword Phrases for Review Requests
- great service · easy process · helpful people · worth the drive · clear communication · straight answers

## Sources Used This Run
- GBP API v4 + Business Information API pull, 2026-10-01 15:05 CDT (owner OAuth verified, fallback credentials used; script retained at /tmp/gbp-audit-pull.js on nada-mini, data snapshot /tmp/gbp-audit-data.json)
- localPosts API listing on accounts/103311538387100102575/locations/1983269944339166584
- EXA `marketing-content` preset re-run 2026-10-01 via `~/clawd/scripts/no-model/exa-preset.sh`
- Prior audit `gbp-velocity-2026-08-27.md` for competitor baselines (carried forward, not re-verified)
