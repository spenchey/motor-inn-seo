# Goal tick 2 — 2026-09-21 ~13:55 CT

## Live check results
| Criterion | Result | Detail |
|---|---|---|
| C1 robots.txt | FAIL | GPTBot + ClaudeBot still `Disallow: *` |
| C2 legacy 301s | FAIL | /inventory, /used-vehicles, /specials, /service-department all 404 |
| C3 VDP h1 | FAIL (corrected) | true VDPs = /used-Carroll-<year>-<model>-<VIN>; static = ZERO h1 (title is JS-rendered h2.vehicle-title__text). Rendered-DOM check still pending |
| C4 og:image | FAIL | absent on homepage + all 3 VDPs (og:title/type/url/description present) |
| C5 FAQPage | FAIL | absent on homepage, VDPs, service-locations.html |
| C6 Chevy GSC | TAG FIXED, verify pending | live meta tag now ends TVOVI ✓ (DealerOn fixed truncation). Verify click needs logged-in GSC session — codex CLI auth dead (tokens expired 2026-06-18), headless Chrome not Google-logged-in |
| C7 Linear | OPEN | MOT-3222 Backlog, MOT-3223..3227 Todo |

## Actions taken
1. DealerOn email sent (MOT-3223 robots.txt): thread 1a0c550cd4cb1e40, logged + committed (ca5167c on motor-inn-seo, pushed to origin).
2. MOT-3223 commented with thread id (2 comments), MOT-3222 parent tick-status comment.
3. Nothing 14+ days old; no >48h threads yet → no re-pings.
4. Codex CC verify blocked by dead auth — next tick needs Spencer present for `codex login --device-auth` OR a logged-in Chrome session.

## Next tick
- Live re-checks; C2 redirects email (one per tick rule).
- 48h re-ping for C1 due 2026-09-23 ~14:00 CT if still failing.
