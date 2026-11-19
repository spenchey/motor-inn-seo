# GBP Velocity Audit — 2026-11-19

- Primary **Toyota+Chevrolet of Carroll** (`14730652758503817758`, "7758") · **Chevrolet of Carroll** (`2099693230539902964`, "2964") · publisher `1983269944339166584` ("6584", historical).
- Pull: GBP API v4, acct `1155…880` (fallback cred), 2026-11-19 ~15:00 CT; raw `reviews-pull-2026-11-19.json` + `localposts-scan-2026-11-19.json` archived beside this file.
- Competitor panels: **carried** (10-26 scrape / 08-27 counts, unverified — headless limits per 11-02 notes; not re-scraped).
- EXA `marketing-content`: silent exit again (1 line, no output, 4th cycle) — angles carried per standing practice.
- Brand kit checks (motorinn-brand loader): answered silently against every line below; no offer terms used this run (no new drafts).

## Executive Summary
- **Review velocity: Nov now 11 in 19 days (weekly buckets 11-01: 1, 11-08: 4, 11-15: 6) — running above Oct's record-month pace in week terms; trailing-30d 21 (was 20 on 11-12), 7d 8. Cooling concern closed; P1 URGENT: no.**
- **Reply coverage: 2 unanswered, both from today (Terry Striegel 5★ 16:28Z, Ken Tegels 5★ 16:17Z — Ken's names Kyle in service). Left to Jeeves' approval lane per 11-17 rule; counted, not touched. Everything older is answered: coverage 265/267 (99.3%); last-50 primary 48/50.**
- **Response lag: median 28.3h / p90 138.8h across 47 replied of last 50 (p90 improved from ~5.8d — the legacy max item and Amanda-reply weekend gap aged out of the window). Median inside the 2-day bar; 48h-or-better on every reply since Nov 1.**
- **Posting: 17/17 LIVE on both review listings, newest 2026-10-29 batch (slots through Nov 27). December block (week-of-11-05 file): 6 posts, 5 approved by Spencer 11-18, 1 pending (Post 3, trade appraisal, Dec 15 — `Approval: pending` line restored this run after the 11-18 approval pass omitted it). Dry-run: `parsed 6; 5 approved; 0 due; publishing 0`. Nothing publishes until Spencer's OK; nothing owed until Dec 1.**
- **Chevrolet listing (2964): flat 37, ~12 wks. Owner-side review-ask at delivery remains the #1 review action. Carried.**
- **Voice: 9 of last-18 replies name service/staff/place by anchor (50%); bar unchanged (default = named anchor every reply). The two newest unanswered reviews literally hand us the anchor: Kyle, by name, twice.**

## 1. Review Teardown (API-exact 2026-11-19)
| Metric | Toyota+Chevrolet of Carroll (7758) | Chevrolet of Carroll (2964) |
|---|---|---|
| Total reviews (API) | **267** (+7 since 11-12) | **37** (flat ~12 wks) |
| Avg rating (listing) | 4.6 | 4.8 |
| Last 7d / 30d | 8 / **21** | 0 / 0 |
| Last 60d / 90d | 43 / 47 (est. from pull window) | 0 / 1 |
| Velocity/mo (30d) | ~21 | ~0 |
| Star mix (last 50) | 46×5★, 3×4★, 1×1★ | 32×5★, 4×4★, 1×2★ (hist) |

Nov weekly buckets: 1 / 4 / 6 (week of 11-15 still running) — the 11-05 dip is fully closed; Nov projects ~18–20, second-best month on record behind Oct 26. Weekly sequence since Oct: 3/5/8/6/4/1/3/4/6.

One 1★ this cycle: Amanda Holloway 11-17 (trade-in offer + payoff-question friction; Yukon, remote appraisal). **Replied same-week with a substantive explanation (payoff → accurate payments; remote-appraisal risk pricing; oil-consumption check from Carfax) and an open invite to re-run the numbers in person — text verified in pull. Model reply for the trade-friction theme.**

Negative themes: no recurring pattern (1 non-5 in last 50). Positive: service/knowledge/friendly dominate; staff named unprompted in review text: Kyle ×2 (RAV4 walkaround; "knows all the f…eatures"), Matt (service, "goes the extra mile"), earlier Rick/Sandy/Ashlee body-shop.

### Competitor snapshot (CARRIED — 10-26 ratings / 08-27 counts, unverified)
| Dealer | Rating | Count (carry) |
|---|---|---|
| Champion Ford Carroll | 4.2 | — |
| Wittrock Carroll | 4.6 | 262 |
| Coleman Co (Spirit Lake FCDJR) | 4.4 | — |
| Macke Motors | 3.8 | — |
| Okoboji Toyota | 4.5 | 1,012 |
| **Motor Inn combined (vol-wtd)** | **≈4.65** | **304 (267+37)** |

## 2. Review Response Analysis
- **Replies audited: last-50 primary. 48 replied / 2 unanswered (both today's — Jeeves' lane). Lag distribution (47 measurable, 0–720h): median 28.3h, p90 138.8h, max ~300h. p90 improvement is window composition, not process change; every reply since Nov 1 ≤48h — the real health signal.**
- **No replies written by this run (11-17 rule). The two unanswered go to Jeeves' draft lane with the Kyle anchor handed to them on a plate.**
- **Templates: standing libraries (10-29 + 11-05) remain valid; no new band needed — 5★/4★/1–2★ each hold 3 live variations, unique first words, no "We appreciate your feedback". No new template file this cycle.**
- Star hygiene: last-8 replies spot-checked against `starRating` — wording matches (no "5 Star" on a 4-star). Clean.

## 3. GBP Posts Audit (API localPosts, 2026-11-19)
| Surface | LIVE | Newest LIVE |
|---|---|---|
| 7758 (review listing A) | 17 | 2026-10-29 batch (slots thru Nov 27) |
| 2964 (review listing B) | 17 | mirrored |
| 6584 (publisher, historical) | 7 | 2026-10-08 |

- Publisher dry-run 2026-11-19: `parsed 6; 5 approved; 0 due but NOT approved; 0 due+approved; 0 unpublished; publishing 0`. Ledger == live; **next slot Dec 1.**
- **Draft hygiene fix this run: Post 3 (Dec 15 trade appraisal) was the only one of the 6 missing its `Approval:` line after Spencer's 11-18 approval pass — restored as `**Approval:** pending` (never self-approved); `--list-pending` now reports exactly 1 pending, matching the file.**
- All STANDARD topicType; CTAs mapped (Book Now / Book Appointment / Learn More / Call Now / Browse Inventory). No OFFER posts in window; the two live offers (OFR-202611-01/02, exp 11-30) are untouched and unadvertised — fine, they were never slated for GBP.

## 4. Posting Pattern Forensics
1. Our cadence holds: Tue/Thu core + Sunday flex, 2–3/wk, 17 consecutive slots live with zero gaps since Oct 15. Dec block pre-drafted through Dec 28.
2. Angle rotation verified across Dec block: battery → holiday service → trade → tread math → quiet-week used → parts counter; no two consecutive posts share an angle.
3. Competitor posting baselines unchanged (carry 10-19 structural check; re-scrape blocked per 11-02 notes).
4. EXA carry (10-29, 10 sources): weekly minimum posting, concrete time-bounded offers, 100–150 words + matched CTA, answer-shaped copy. Dec block conforms.
5. EXA 11-12 addendum carries unchanged: UTM-tagging on post links and a monthly OFFER-format post remain open decisions for Spencer — not cron changes.

## Risk checks (own listings, per skill — read-only)
- Name/address/phone: no changes observed in API fields this cycle; phones stand as recorded 10-15 (Carroll 792-5000 combined / Chevy 882-7802; Spirit Lake 336-2701). Listing-phones config file absent from `~/motor-inn-seo/config/` — numbers verified from skill record + prior API pulls instead. **Owner to confirm: none new.**
- Website/buttons/messages/suggested-edits: not re-walked this cycle (browser checks hit the 11-02 captcha walls from this host; last full walk 10-26 structural). No change signals in API data.

## Action Items
1. **2 unanswered reviews (today, both 5★, one names Kyle)** → Jeeves' approval lane. Count only; this job drafts nothing for them (standing templates cover 5★).
2. **Spencer: 1 post awaiting OK — Post 3, "The Trade Number…", Dec 15, CTA Learn More.** Say OK in Slack; a directed session applies the approve line. Nothing else pending until the December block runs.
3. **Chevrolet review ask (owner, ~12 wks)**: 37 flat. Add the ask to Chevrolet delivery/checkout. Carried.
4. p90 reply-lag improvement noted; no action — recent replies all ≤48h. Weekend-coverage glance only.
5. **P1 URGENT: no.** #seo-monitoring not paged.

## Sources Used This Run
- GBP API v4 pulls 2026-11-19 ~15:00 CT from nada-mini (fallback cred refresh → reviews ×2, localPosts ×3); raw JSON archived in `audits/gbp-velocity/`.
- Publisher `--dry-run` + `--list-pending` (read-only; nothing published, no approve run).
- Prior audits 11-12 / 11-05 for baselines and carries. Competitor figures carried flagged (unverified this run).
- Brand context via `~/Glyph/projects/motorinn-brand/bin/brand_context.py` (skill's `~/motorinn-brand/...` path does not exist on this host — noted for the skill's next edit).
- EXA `marketing-content`: silent exit (1 line stdout), 4th consecutive cycle — carried, not blocking.
