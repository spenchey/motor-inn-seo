# GBP Velocity Audit — 2026-05-18

## Executive Summary
- Review velocity: 8.5/month (estimated, same as last week — no fresh scrape data available)
- Posting cadence: on track (2 posts this week vs target 2)
- ⚠️ Data source note: GBP scraping blocked by Google (429 on firecrawl, JS-only on Maps, browser attachOnly). Numbers below are extrapolated from 2026-05-14 audit. Fresh scrape requires either (a) Chrome with remote debugging on port 9222 for browser tool, or (b) Spencer manually providing review/post counts from the GBP dashboard.
- Structural audit was updated 2026-05-18 with industry research and a manual checklist (saved to `gbp-structural/gbp-structural-2026-05-18.md`).

## Review Velocity (estimated, from 2026-05-14 baseline)
| Metric | Motor Inn | Champion Ford | Wittrock Motor | Coleman Auto | Okoboji Toyota | Macke Motors |
|--------|-----------|---------------|----------------|--------------|----------------|--------------|
| Total reviews | 126 | 353.5* | 219.4* | 187.3* | 159.8* | 93.5* |
| Avg rating | 4.6 | 4.4 | 4.5 | 4.3 | 4.7 | 4.2 |
| Last 30d | 10* | 27.3* | 19.9* | 13.6* | 21.9* | 5.8* |
| Velocity/mo | 8.5* | 31.0* | 22.2* | 13.8* | 24.3* | 6.2* |

*Estimated — not refreshed from live scrape. Values carried forward from 2026-05-14.

### Gap Analysis
- Reviews needed/month to catch Champion Ford (top competitor) in 6mo: 34.0
- Current Motor Inn velocity: 8.5/month
- **Status:** P1 URGENT (velocity < 50% of top competitor)

## Review Response Quality (estimated)
| Metric | Motor Inn | Champion Ford | Wittrock Motor | Coleman Auto | Okoboji Toyota | Macke Motors |
|--------|-----------|---------------|----------------|--------------|----------------|--------------|
| Response rate | 72%* | 90%* | 85%* | 80%* | 88%* | 70%* |
| Avg word count | 15* | 18* | 15* | 14* | 16* | 10* |
| Neg handling | apologize + resolve | apologize + resolve | apologize + resolve | apologize + resolve | apologize + resolve | ignore |

*Estimated — not refreshed from live scrape.

### Response Rate: 72% (target: 100%)

## GBP Posts (estimated)
| Metric | Motor Inn | Champion Ford | Wittrock Motor | Coleman Auto | Okoboji Toyota | Macke Motors |
|--------|-----------|---------------|----------------|--------------|----------------|--------------|
| Posts (90d) | 6* | 15.5* | 11.1* | 8.4* | 13.3* | 5.4* |
| Posts/week | 1.0* | 1.4* | 1.0* | 0.8* | 1.2* | 0.5* |
| Types used | offer, update | offer, update | offer, event | update | offer, update, event | offer |

*Estimated — not refreshed from live scrape.

### Motor Inn posting status: 2 posts this week / target 2

## Website Traffic (actual, from weekly SEO audit)
- Sessions: 2,240 (+8.1% WoW)
- Users: 2,011 (+7.7% WoW)
- Organic share: 21% of traffic
- Top non-brand query: "carroll toyota" — position 4.1, 7 clicks, 28 impressions
- High-opportunity: "carroll iowa car dealerships" — position 19.0, 7 clicks, 43 impressions (page 2!)

## Action Items (This Week)
1. **Unblock GBP scraping** — Spencer: start Chrome with `--remote-debugging-port=9222` so the browser tool can attach and scrape GBP listings directly.
2. **Coleman Auto GBP URL** — Spencer: provide Coleman Auto's Google Maps share link so we can add it to `competitors.json`.
3. Draft 2 GBP posts for next week (Tuesday and Thursday).
4. Continue responding to pending reviews — target 85%+ response rate.
5. Prioritize internal linking to push "carroll iowa car dealerships" from page 2 to page 1.

## Data Quality Note
All GBP-specific metrics in this audit are **estimates** based on the 2026-05-14 scrape, which succeeded. The 2026-05-18 scrape failed due to:
1. Firecrawl: Google returns 429/CAPTCHA on share link redirects
2. web_fetch: Google Maps renders client-side JS (empty HTML response)
3. browser tool: Chrome not running with `--remote-debugging-port=9222` (attachOnly mode)

The fix is straightforward: launch Chrome with debugging enabled, and the browser tool can navigate to competitor GBP listings directly using the logged-in user profile (which has Google auth cookies). This bypasses the CAPTCHA wall. I'll handle this once Chrome is available on port 9222.
