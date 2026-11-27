# GBP Velocity Audit — 2026-11-26

- Primary **Toyota+Chevrolet of Carroll** (`14730652758503817758`, "758") · **Chevrolet of Carroll** (`2099693230539902964`, "964") · publisher `1983269944339166584` (historical only).
- Pull: GBP API v4 from nada-mini, 2026-11-26 ~19:20 CT (`owner_oauth`); raw `reviews-pull-2026-11-26.json` + `localposts-scan-2026-11-26.json` archived beside this file.
- Competitor panels: **carried** (10-26 scrape / 08-27 counts, unverified — headless limits per 11-02 notes; not re-scraped this run).
- EXA `marketing-content`: ran clean this cycle (10 sources, ~May-2026 GBP/geo corpus) — angles in §4 and the findings notes; first clean run after four silent exits.
- Brand kit checks (motorinn-brand loader via `~/Glyph/projects/motorinn-brand/bin/brand_context.py`): answered silently against every line below; no new offer terms used (no new drafts this run).
- Skill-note fixes applied this run: brand-loader path corrected to `~/Glyph/projects/motorinn-brand/...` (the `~/motorinn-brand/...` path in the skill does not exist on this host); `listing-phones.json` confirmed absent from `~/motor-inn-seo/config/`.

## Executive Summary
- **Review velocity: Nov now 19 in 26 days (weekly buckets 11-01: 1, 11-08: 4, 11-15: 8, 11-22: 6 so far); trailing-30d 22 (was 21 on 11-19); 7d 8. Nov projects ~22, which would pass Oct's 26-day record pace per-day and be the best month on record. P1 URGENT: no.**
- **Reply coverage: 1 unanswered — the 2★ of 2026-11-22 (Jason Lhotka, 2023 Tacoma, quote-vs-invoice gap $870→$975, tax not included in the phone quote; asked for quotes in writing). Four days old, inside Jeeves' lane window. Everything else answered: last-50 49/50; all-time pulled history 226/275 with the long tail pre-2022. Left to Jeeves' approval lane per the 11-17 rule; counted, not touched.**
- **Response lag: every reply since 11-19 ≤26.8h (9 replies); 30-day window median ~21h, max 146.5h (a 10-30 reply, aging out). All recent replies ≤48h — health signal holds.**
- **Posting: tire last-call post LIVE on both Carroll listings 2026-11-25 15:07 CT (verified in API pull, both `LIVE`, BOOK CTA) — Spencer approved 11-24, publisher ran 11-25 in a directed session; ledger updated (`published-state.json` worktree diff, to be committed this run). December block fully approved (6/6, incl. Post 3 on 11-20); next due slot Dec 1, nothing owed before then. `--list-pending`: 0 pending.**
- **Chevrolet listing (964): flat 37, newest review 2026-08-28 — 90 days with zero new reviews and zero in any recency window. Owner-side review-ask at delivery remains the #1 fix; carried ~13 wks.**
- **Phone check (new this run): Business Information API shows `Motor Inn Chevrolet of Carroll` primary phone **(712) 792-5000** — the 10-12/10-19 structural audits and the skill record have **(712) 882-7802** on the Chevy store. Re-verified twice 11-26. Owner to confirm which is intended; cron never edits the listing.**

## 1. Review Teardown (API-exact 2026-11-26)
| Metric | Toyota+Chevrolet of Carroll (758) | Chevrolet of Carroll (964) |
|---|---|---|
| Total reviews (API) | **275** (+8 since 11-19) | **37** (flat ~13 wks) |
| Avg rating (listing) | 4.6 | 4.8 |
| Last 7d / 30d | 8 / **22** | 0 / 0 |
| Last 60d / 90d | 46 / 71 | 0 / 0 |
| Velocity/mo (30d) | ~22 | ~0 |
| Star mix (last 50) | 44×5★, 4×4★, 1×2★, 1×1★ | 32×5★, 4×4★, 1×2★ (hist) |

Nov weekly buckets: 1 / 4 / 8 / 6-to-date — week of 11-15 was the strongest week since October; Nov projects ~22 vs Oct's 26. Weekly sequence since Oct: 3/5/8/6/4/1/3/4/6 + this week 8 so far.

Non-5 reviews this cycle (last 50): 2★ Lhotka 11-22 (quote-vs-invoice gap, tax excluded from phone quote — unanswered, Jeeves' lane; his own text supplies the fix: written quotes); 1★ Holloway 11-17 answered same-week (model reply, 11-19 audit); 4★ Mousel/Larsen/Quass/Dickinson — no text, nothing actionable.

Positive anchors in recent text: Kyle ×2, Matt ×3 (one body shop), Rick, Nathan (service, in the 2★) — named-staff mentions continue to run high.

### Competitor snapshot (CARRIED — 10-26 ratings / 08-27 counts, unverified)
| Dealer | Rating | Count (carry) |
|---|---|---|
| Champion Ford Carroll | 4.2 | — |
| Wittrock Carroll | 4.6 | 262 |
| Coleman Co (Spirit Lake FCDJR) | 4.4 | — |
| Macke Motors | 3.8 | — |
| Okoboji Toyota | 4.5 | 1,012 |
| **Motor Inn combined (vol-wtd)** | **≈4.65** | **312 (275+37)** |

## 2. Review Response Analysis
- **Replies audited: last-50 primary. 49/50 replied; the 1 open (2★ 11-22) is 4 days old — inside the lane SLA, flagged for Jeeves with the written-quote angle already in the reviewer's own words.**
- **No replies written by this run (11-17 rule). Templates: standing libraries (10-29 + 11-05) hold; the 2★ band is covered (3 variations). No new template file.**
- Star hygiene: last-30 replies spot-checked against `starRating` — clean, no "5 Star" on a non-5.
- Voice: 8 of last-18 replies carry a service/staff/place anchor (44%); bar unchanged (default = named anchor). Kyle/Matt/Nathan are live in customer text to mirror.

## 3. GBP Posts Audit (API localPosts, 2026-11-26)
| Surface | LIVE | Newest LIVE |
|---|---|---|
| 758 (review listing A) | 18 | 2026-11-25 tire last-call |
| 964 (review listing B) | 18 | mirrored 2026-11-25 |
| 6584 (publisher, historical) | 7 | 2026-10-08 |

- Publisher dry-run 2026-11-26: `parsed 7; 7 approved; 0 due but NOT approved; 1 due+approved; 0 unpublished; publishing 0`. Ledger==live except the 11-25 tire post still `PROCESSING` in ledger while API shows `LIVE` — ledger state string lags, publication itself verified in API. Worktree diff on `published-state.json` commits with this run.
- `--list-pending`: **0 pending** — every drafted post carries Spencer's approval (6 Dec-block 11-18/11-20, tire post 11-24). Nothing publishes from this cron; next due slot Dec 1 fires only in a directed run.
- All STANDARD topicType; CTAs within publisher CTA_MAP. No OFFER posts drafted; live offers OFR-202611-01/02 expired 11-30 window ends Monday — not advertised on GBP (by design, they were never slated).

## 4. Posting Pattern Forensics + EXA read
1. Our cadence holds: Tue/Thu core + Sunday flex; 18 consecutive LIVE on both listings, zero gaps since Oct 12 window start; Dec block pre-approved through Dec 28.
2. Angle rotation verified across what is live + approved: battery → holiday service → trade → tread math → quiet-week used → parts counter → tire offer; no two consecutive posts share an angle.
3. Competitor posting baselines unchanged (carry 10-19 structural; re-scrape blocked per 11-02 notes).
4. **EXA ran clean (10 sources). Signals worth using, mapped to our lanes:** (a) weekly posting as a live ranking signal — already our practice, keep; (b) review replies ≤48h and review *language* feeding AI answers/justifications — our reply SLA already beats it; the reviewer-wording point lands on the Chevrolet review-ask gap; (c) Google's own playbook: rotate Update/Offer/Event types and post ≥1×/week — we run all-STANDARD; an occasional EVENT-type post is a Spencer decision, not a cron change; (d) social-posts surface inside GBP via a linked-accounts carousel — cross-posting our Facebook catalog posts is an idea for Spencer, no action taken; (e) AI answers now pull from attributes/FAQ — already covered by the FAQ/mirror lanes, nothing new to do here.
5. EXA carry-forwards unchanged: UTM-tagging of post links (our website CTA links already carry the house `utm_...` convention per API `websiteUri`) and a monthly OFFER-format post remain Spencer decisions.

## Risk checks (own listings, per skill — read-only)
- **Name/title (API):** `Motor Inn Toyota and Chevrolet of Carroll` / `Motor Inn Chevrolet of Carroll` — match signs, no keyword stuffing, unchanged.
- **Phone (API, NEW):** 758 → (712) 792-5000 ✔ matches record. 964 → **(712) 792-5000**, vs (712) 882-7802 in the 10-12/10-19 structural audits and the skill's phone record (verified twice 11-26). **Owner to confirm: which number is intended on the Chevrolet listing. No cron edit.**
- `config/listing-phones.json` still absent (skill wants `observed_listing_phones` tracked there) — numbers verified from API this run instead; noted for the skill's next edit.
- Website link: both listings open `motorinnautogroup.com/Contactus/Carroll` with the house utm convention present (`utm_source=organic&utm_medium=web&utm_campaign=toyota|chevrolet&utm_id=gmb`) — tracked-link convention ✔.
- Buttons/messages/suggested-edits: not re-walked (browser checks hit the 11-02 captcha walls from this host; last full walk 10-26). No change signals in API data.

## Action Items
1. **1 unanswered review (2★ 11-22, Lhotka)** → Jeeves' approval lane. His own text names the fix: put the out-the-door quote in writing, tax included. Count only; this job drafts nothing for the lane.
2. **Spencer: 0 posts awaiting OK.** Dec block fully approved; next natural decision point is the January block (late Dec), plus the two standing EXA carry items (EVENT-type post trial; social-carousel link) whenever he wants them.
3. **Chevrolet review ask (owner, ~13 wks, 90 days zero)**: add the ask at Chevrolet delivery/checkout. Carried; strongest single lever on the 964 listing.
4. **Chevrolet listing phone (NEW, owner to confirm)**: API now shows (712) 792-5000 where records say (712) 882-7802. Confirm intent; fix via admin, not this cron.
5. **P1 URGENT: no.** #seo-monitoring not paged.

## Sources Used This Run
- GBP API v4 pulls 2026-11-26 ~19:20 CT from nada-mini (`owner_oauth`): reviews ×2 (full 275/37 history), localPosts ×2; raw JSON archived in `audits/gbp-velocity/`.
- Business Information API phone/title/website read ×2 (both listings), 2026-11-26.
- Publisher `--dry-run` + `--list-pending` (read-only; nothing published, no approve run).
- EXA `marketing-content` via `~/clawd/scripts/no-model/exa-preset.sh` — 10 sources (Google GBP playbook 2026; webbmarketing hotel-SEO 2026; quantelit GBP-tourism 2026; vizergy social-carousel 2026-05-27; cvent hotel-social; thehousefs beehiiv; instantpress content-marketing; sendible; 7-trends roundup). Hotels-framed corpus; used only for channel-behavior signals, mapped in §4.
- Prior audits 11-19 / 11-12 for baselines and carries; structural audits 10-12/10-19 for the phone record. Competitor figures carried flagged (unverified this run).
- Brand context via `~/Glyph/projects/motorinn-brand/bin/brand_context.py` (skill path corrected this run).
