# Goal tick state — updated 2026-09-21 22:30 CT (tick 4, 4h cron)

## C1 robots.txt — PASS (DONE, MOT-3223 Done)
- GPTBot + ClaudeBot: Allow: * live. Evidence committed (f34719a on nada-mini repo).
- DealerOn case 01921347. DealerOn replied twice (17:21, 22:21 UTC) — acknowledgment + case table; both landed in TRASH. No action needed; fix already verified live.

## C2 legacy 301s — FAIL (email sent, awaiting)
- All 4 paths still 404 (verified 22:15 CT). Thread 1a0c64001906a92e sent 18:10 CT.
- 48h re-ping due: after 2026-09-23 ~18:00 CT. Too early this tick.

## C3 VDP h1 — FAIL (evidence strengthened this tick)
- True VDPs (/used-Carroll-...-VIN): static HTML has ZERO <h1>; title is JS-rendered into <h2 class="vehicle-title__text"> (confirmed live 8 VDPs from RSS, 22:20 CT).
- NOTE: /used/<VIN> short URLs 301 to searchused.aspx (an SRP with 1 h1) — do NOT use them as VDP evidence (baseline tick5.py pattern is wrong; use /used-Carroll- slug).
- Rendered-DOM check still blocked: codex CLI auth DEAD on this box (refresh token already used; `codex login --device-auth` needs Spencer present).
- No email yet — plan: collect rendered-DOM evidence, then send MOT-3225 email. If codex stays dead at next tick, send email with static evidence (0 h1 statically is stronger than baseline claim).

## C4 og:image — FAIL
- Homepage + true VDPs: og:title/type/url/description present, og:image ABSENT (re-verified 22:20 CT).
- VDPs carry <link rel="image_src" href="inventoryphotos/...jpg"> — DealerOn can map og:image to it.

## C5 FAQPage — FAIL
- No FAQPage JSON-LD on homepage, true VDPs, service-locations.html, newspecials.html (re-verified 22:20 CT).

## C6 Chevy GSC — TAG OK (ends _TVOVI, re-verified 22:20 CT); Verify click PENDING
- codex auth still dead (probe failed 22:25 CT with 'refresh token already used'). Human gate: Spencer runs `codex login --device-auth`.
- Evidence saved: pipeline/evidence/c6-chevy-tag-2026-09-21.txt (nada-mini repo + macbook copy).

## C7 Linear — MOT-3223 Done (evidence comment). MOT-3224 Todo (email thread commented). MOT-3225/3226/3227 Todo. Parent MOT-3222 Backlog w/ progress comment.
- Nothing 14+ days old (created 09-21). Escalation due ~2026-10-05.

## THIS TICK'S ACTIONS (tick 4)
- Live checks re-run: C1 PASS; C2/C4/C5 FAIL unchanged; C6 tag OK.
- No new DealerOn email sent this tick: C3 email intentionally deferred for rendered-DOM evidence (codex dead = human gate); C2 <48h so no re-ping. Zero emails would stall the queue — DECISION: send MOT-3225 email NEXT tick with static evidence if codex still dead.
- C6 evidence file committed.

## NEXT TICK (4h)
1. Re-run live checks (C3 via /used-Carroll- slug).
2. If codex auth still dead: send MOT-3225 email (one issue: VDP single-h1) using static 0-h1 evidence.
3. Watch for DealerOn replies on C2 thread (trash included).
4. C2 re-ping only after 2026-09-23 18:00 CT.

## KEY FACTS (stable)
- Repo: nada-mini ~/motor-inn-seo (this machine's ~/motor-inn-seo is NOT a git repo — scp files over).
- True VDP pattern: /used-Carroll-<year>-<make>-<model>-<VIN>; VINs enumerable from rss-usedinventory.aspx (needs browser UA else 403).
- Email: /opt/homebrew/bin/gog gmail send --body-file <f> --account spencer.heywood@motorinnmail.com --json.
- DealerOn replies land in TRASH — search 'from:help@dealeron.com newer_than:Nd' (trash included).
- Codex auth fix (Spencer, interactive): codex login --device-auth. Until then C6 verify + C3 rendered-DOM are human-gated.
