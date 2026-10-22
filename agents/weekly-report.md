# 14. Weekly SEO/AI-visibility report (Holmberg step 6)

## Purpose
One weekly digest: what changed, what to prioritize, next actions. Read-only; delivered to
Spencer's chat by the existing goal-loop cron (no approvals needed to REPORT).

## Sources (all existing)
- GSC: clicks/imps/pos delta WoW per property (goal-loop check data)
- GA4 x GSC join: killer_pages.py rerun; key events delta
- AI visibility: DataForSEO AI-Mode spot-check on 3 money queries ($0.006/wk cap)
- Bing WMT AI Performance report (once access granted; skip until then)
- Pipeline: drafts awaiting approval; pages published; research files opened
- DealerOn cases: open items from brain/LOG.md

## Format (strict, <=25 lines)
WEEK OF <date>
1. Numbers: clicks x (+/-d), imps y, leads z (key events), AI-cited q/s
2. Published: <pages/changes with commit refs>
3. Ranking movers: top 3 up/down w/ urls
4. AI citations: who got cited for money queries; us yes/no
5. Blocked on DealerOn: <case, days>
6. Needs Spencer: <approvals, logins - max 2 items>
7. Next week plan: <one change per active page; new targets>

## Delivery
Append to brain/reports/week-YYYY-MM-DD.md AND push summary via goal-loop cron channel.
Never bury a NEEDS-VERIFY that blocks publish.
