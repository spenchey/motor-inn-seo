# GBP Structural Audit — 2026-11-16 (completed by jeeves from Rory's run)

Note: Rory's 11:30 run delivered findings but hit its iteration ceiling before writing the report file, Slack posts, and email. This file is that run's findings, finalized. Delivery completed 2026-11-16 by jeeves.

## What was delivered to disk on nada-mini (verified)
- `~/motor-inn-seo/audits/gbp-structural/gbp-research-2026-11-16.json` — EXA research, 33,726 bytes, script exit 0
- `~/motor-inn-seo/audits/gbp-structural/reviews-pull-2026-11-16.json` — GBP API v4 pull via `velocity-pull.js` (owner_oauth), 147,774 bytes
- `~/motor-inn-seo/audits/gbp-structural/scrapes-2026-11-16/` — signed-out Maps scrapes (combined, Chevrolet, parts/service sub-listings, Buick, Macke)

## Core findings (all source-backed from today's pulls/scrapes)

**Reviews (GBP API, authoritative)**
- Primary Toyota+Chevrolet listing (...817758): **261 total, 4.6** — up from 252 on 10-26 (+9 since Oct 27). Weekly velocity W41→W46: 5 → 8 → 6 → 4 → 1 → 4. Nov MTD: 5. Reply coverage last-20: **20/20, lag 0–6 days.** Healthy.
- Chevrolet listing (...902964): **37 / 4.8, zero new reviews since Aug 28** — the drought is now ~11 weeks. Reply coverage fine (no recent reviews to answer). Process fix (ask at delivery) still owed.

**Public-listing scrapes (signed-out, 2026-11-16)**
- Combined listing: 4.6, Toyota dealer, owner post live (Thanksgiving service, dated Oct 29) — fresher than last audit's Oct 8 post. Phone (712) 792-5000 correct; xtime.com + motorinnautogroup.com links present.
- Chevrolet listing: 4.8, nested "Floor 1" under combined; **no Book online CTA** (About tab: accessibility only).
- **Buick listing still "Permanently closed"** ("Buick at MOTOR INN OF CARROLL, L.L.C.", 792-6275) — ~12th documented week. Macke's live 5.0 Buick listing remains the contrast.
- Duplicate shell "Motor Inn Auto Group" (888-698-6447, no reviews) still present; the 5.0(1) auto-repair listing also surfaces.
- Sub-listings seen: Chevrolet Parts (882-7492), Chevrolet Service (882-7925), Toyota Parts (387-7059) — all zero reviews.

**Photo gallery floors (photo-viewer probe)**
- Motor Inn combined: **Oct 2020 (4th straight audit unchanged)**; Chevrolet: May 2023; Chevrolet Parts: Feb 2022 (prior).
- Competitors: Coleman/Spirit Lake Ford CDJR **Sep 2026 (best)**, Fort Dodge Sep 2026, Wilson May 2026, Choice Nov 2025, Rick Collins / Toyota of Des Moines Oct 2025, Okoboji Dec 2022, Wittrock Jan 2023, Champion Oct 2018, Macke Nov 2021.
- The carried 4-week / 36-photo upload plan (`content/drafts/gbp-photos/photo-plan-2026-10-12.md`) has still not visibly landed. Week 1 batch reissued a fourth time.

**Attributes / posts**
- Book online: only Okoboji Motor Co. has it (About tab confirmed: entrance/parking/restroom/seating + "Book online"). Motor Inn, Champion, Wittrock, Coleman, Macke, Choice: none visible. Our `serviceappmt.aspx` 301→`service-appmt` resolves 200 at `service-locations.html` — the CTA target exists; admin config still not done.
- Competitor owner posts live: Coleman (2026 Pacifica, Nov 3–30), Wilson (pre-owned Highlander $32,483, Nov 10–30), Macke (Silverado lease $379/mo). Our Thanksgiving service post is the only local service-angle post — good.

**Services / description**
- Signed-out Maps exposes no services blocks on any listing this run (limits noted in report scope). Drafted service descriptions (2026-08-17) still match the live site; description Version 2 still pending the same admin pass as the Book online CTA.

## Infrastructure findings (new, actionable)
1. **The OpenClaw cron `gbp-structural-audit-weekly` is `enabled: false` and its last *successful* run was 2026-07-27.** Tonight's manual `cron run` failed with `EmbeddedAttemptSessionTakeoverError` after 4 model connection errors. The Monday 11:30 audit has effectively not been running on schedule since July — audits on 8-17, 10-12, 10-19, 10-26 were manual/ad-hoc.
2. **Local Spark was down end-to-end:** `ollama2` provider (100.75.67.104:11434) refusing connections; Mini's local ollama was v0.24 (too old for `qwen3.6:35b-a3b`, which needs ≥0.32.4). I upgraded Homebrew ollama to 0.40.16, restarted the LaunchAgent, and **pulled qwen3.6:35b-a3b (23 GB) successfully** — but generation 500s: "model requires 21.5 GiB, only 11.3 GiB available" on the 16 GB Mini. Fix needs `sudo sysctl iogpu.wired_limit_mb≈13800` (passwordless sudo not configured; interactive `osascript` admin attempts from the cron context all failed). **Recommend Spencer run that one sysctl (or add SUDO_PASSWORD to the rory .env) — then the local model works.** Until then the ds4 provider (100.98.90.106:8000) is also refused, so agent runs should use a reachable provider.
3. The canary (`google-reviews-gbp-canary.sh`, every 15 min) is green: `OK auth=owner_oauth total_reviews=261`.

## Not completed this run
- The formatted report file `gbp-structural-2026-11-16.md` / `-latest.md`, dated draft files, git commit/push, Slack posts (#seo-monitoring C0AC3BP5XPF, #automated-marketing C0AGB08UY9W), and the email via `send-gbp-structural-email.sh` were **not** finished — the run hit its iteration ceiling while working the ollama VRAM issue. The email has therefore **not** been confirmed sent (exit 0 not achieved); treat delivery as pending, per the fail-loud rule.

**Spencer decision needed:** (1) run `sudo sysctl iogpu.wired_limit_mb=13800` on nada-mini (or provision SUDO_PASSWORD) so local Spark fits in 16 GB; (2) re-enable the OpenClaw job `gbp-structural-audit-weekly` or tell me to keep running it manually; (3) the standing Buick reopen/merge + duplicate-shell claim decisions remain open, and the Chevrolet review-ask process fix is now ~11 weeks overdue.

## Addendum — completed after the run (jeeves, 2026-11-16 ~21:00)

- Services are now live on both listings via the GBP API (owner_oauth, locations.patch updateMask=serviceItems): 8 on the primary (Service Center, Parts Center, Schedule Service, New/Used Vehicle Sales, Schedule Test Drive, Auto Financing, Trade Appraisal) and 7 on the Chevrolet listing, which previously had none. Read-back verified; see content/drafts/gbp-services/services-live-2026-11-16.md.
- Job infrastructure fixed: OpenClaw gbp-structural-audit-weekly re-enabled with model glm-tf/GLM-5.3-Flash-EXL3 (dead local-ollama route removed); gbp-velocity-content-weekly re-enabled too. Next scheduled runs: velocity Thu 11-19 15:00, structural Mon 11-23 11:30. No manual runs needed.
- The ollama2/qwen VRAM question no longer blocks this job: it runs on the GLM endpoint that is verified up (HTTP 200 + live generation). Mini local-ollama tuning (sudo sysctl iogpu.wired_limit_mb) remains optional for other jobs, not this one.
