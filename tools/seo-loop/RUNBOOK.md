# SEO findings loop: runbook for Mac mini 1

This is the plain-English guide for whoever keeps the Motor Inn search-findings loop running. It covers the three websites (the group site, the Toyota site and the Chevrolet site) and the three Google listings behind them.

Status: this runbook describes a loop that is built but not switched on. Every line in the proposed schedule starts with `#PAUSED`, so nothing runs until Spencer names each line. Nothing in this document has been run live.

## 1. What the loop does

The loop finds problems on the sites and listings, writes each problem down once, asks Spencer for approval before anything changes, and then checks the live site to see whether the fix worked.

The loop has four small pieces (the register, the packet builder, the fix checker and the Monday summary), fed by the watch and by the report ingest. The register holds every finding:

- A finding is one problem, written once. A problem that shows up again adds to its count. It does not make a new row.
- Nothing is marked fixed until the live page passes two checks at least a day apart.
- A message to Spencer is one short note on Monday, with at most three asks.

## 2. Where things live on Mac mini 1

| What | Where |
|---|---|
| Scripts | `$HOME/motor-inn-seo/tools/seo-loop/` |
| Watch URL list | `$HOME/motor-inn-seo/tools/seo-loop/urls.json` |
| Register (the one source of truth) | `$HOME/motor-inn-seo/findings/register.jsonl` |
| Generated register view | `$HOME/motor-inn-seo/findings/REGISTER.md` (made by hand, see section 4) |
| Check catalog and expected site facts | `$HOME/motor-inn-seo/findings/checks.json` and `expected-sites.json` |
| Watch output (one file per run) | `$HOME/motor-inn-seo/findings/watch/` |
| Report files from the lead's Monday job | `$HOME/motor-inn-seo/findings/reports/` |
| Unmatched findings waiting for triage | `$HOME/motor-inn-seo/findings/inbox.jsonl` |
| Monthly baselines | `$HOME/motor-inn-seo/findings/baselines/<yyyy-mm>.json` |
| Ready-to-approve packets | `$HOME/motor-inn-seo/findings/packets/` |
| Saved evidence (pages, dates, reads) | `$HOME/motor-inn-seo/findings/evidence/` |
| Monday summary text | `$HOME/motor-inn-seo/findings/summaries/` |
| Logs | `$HOME/motor-inn-seo/findings/logs/` |
| Backups of the schedule before any change | `$HOME/motor-inn-seo/_backups/` |
| Retired files | `$HOME/motor-inn-seo/_expired/<date>/` |

The register is written by the scripts, and by the coordinator's commands, on a daily schedule: the tripwire ingest (06:25), the Monday ingest (12:50) and the fix checker (13:10). Nobody edits it by hand. The catalog (`checks.json`, `expected-sites.json`) and the scripts change only through a pull request in the SEO repository (one branch, one review, one merge). The scripts never change the catalog.

Python is `/usr/bin/python3` (version 3.9). Every script is run with `-I`, which is the isolated mode. The scripts use only the standard library and make no changes outside the findings folder, except the watch, which only reads public pages.

## 3. What each script does

| Script | What it does | When it runs | What it writes | Owner |
|---|---|---|---|---|
| `site_watch.py` | Reads a small set of public pages on the three sites and writes problems it sees as candidate lines. Read-only. Waits at least 5 seconds between requests. Never reads a page it was not told to read. | Daily at 06:15 (tripwire, 9 pages). Monday at 06:30 (full, every page on the list plus the sitemap) | One watch file per run in `findings/watch/`. Each morning's tripwire file is ingested at 06:25; the Monday full file is ingested at 12:50 | rory |
| `register.py` | The only tool that changes the register. Adds a finding or updates a repeat sighting, moves a finding to its next status, records a passing read, records approval, shows what needs Spencer, and checks every row. | Run by hand, or by the other scripts | `register.jsonl`, and `REGISTER.md` when rendered | coordinator |
| `ingest_reports.py` | Reads the structured findings block at the end of each report, and the Monday full watch file (passed with `--candidates`). Prose is ignored. Known problems go into the register; unknown items go to the inbox, at most ten a run. It never reads the review pull files. | Monday at 12:50 | The register and the inbox | rory |
| `packet.py` | Writes ready-to-approve packets from register rows: DealerOn requests (at most five items each), Google listing edits, content drafts and Spencer decisions. Sends nothing. | By hand, when a row is ready for an ask | One folder per packet in `findings/packets/`, each starting with "DRAFT: needs Spencer's OK in chat" | rory |
| `verify_fix.py` | Reads the live page for each row that was sent. Marks a row proven only after two passes, at least a day apart. A fix that is not in place by day 14 reopens the row. A network error is "not observed" and changes nothing. | Daily at 13:10 | The register, and evidence files | rory |
| `monday_summary.py` | Writes the Monday note to a file: a one-line verdict, the numbers with their sources, what was fixed, what is open, at most three asks, and what is waiting on DealerOn. It has no sending code. | Monday at 13:00 | A text file in `findings/summaries/` | rory |
| `baseline.py` | Puts the monthly numbers into the baseline file. A missing number is written as "not verified". Nothing is estimated. | Once a month, by hand, once the input files exist | `findings/baselines/<yyyy-mm>.json` | rory-performance |
| `ai_answers.py` | Asks the fixed question set (30 questions) through the paid search provider and records whether Motor Inn was cited, mentioned or absent. Refuses to run if the spend limit would be passed. | Only after Spencer approves the question set, and dry run first | Raw answers (cached 7 days) and a usage file | rory-ai-search |

## 4. The weekly rhythm

| When | What happens | Owner |
|---|---|---|
| Every day, 06:15 | Tripwire watch of 9 key pages | rory |
| Every day, 06:25 | Ingest of that morning's tripwire file into the register | rory |
| Every day, 13:10 | Fix checker reads each sent fix again | rory |
| Monday, 06:30 | Full watch of all three sites | rory |
| Monday, before 12:50 | The lead's Monday job writes this week's report files into `findings/reports/`. Each report ends with its findings block. Unmatched items in the inbox are mapped, proposed as a new check, or dropped with a reason | rory |
| Monday, 12:50 | Report ingest, including this Monday's full watch file | rory |
| Monday, after ingest | Coordinator runs `register.py render` to refresh `REGISTER.md`, then reads the summary | Coordinator |
| Monday, 13:00 | Summary written to a file | rory |
| Monday, after the summary | Coordinator takes the asks (at most three) to Spencer in chat and records any approvals | Coordinator |
| First of the month | Baseline file built once the inputs exist. Organic-lead definition checked against both monthly reports | rory-performance |

Tier 1 problems (a money page dropped from the index, a wrong phone number in a live post) are written to the register the same morning, through the daily tripwire ingest. They then appear in the Monday summary. Same-day delivery of a tier 1 finding to Spencer is not built. No alert is turned on until he approves it (see section 10). Until then, nobody is told the same day.

## 4b. Report dates

Every report must say when it was written. The ingest uses that date, never the day it runs, so an old report cannot reopen a row that was fixed after it was written. A report needs one of these:

- a line `report_date: YYYY-MM-DD` inside its `FINDINGS-JSON` block, or
- exactly one date in its file name, such as `seo-health-2026-11-16.md`.

If neither is present, the report is `not ingested`. So is a report with an invalid date, two different dates, or a date after today. Candidate files (the watch files) take their date from the file name only. The watch file names in this runbook already carry the date.

## 4a. What seen_count means

`seen_count` counts sightings, not weeks. Each run that sees a problem adds one. A problem that is still there on five daily tripwire runs and then on the Monday full watch has `seen_count` 6, with one open row. `first_seen` and `age_days` do not change with sightings, so age still shows how long the problem has been open. A high count means the problem was seen often; it is not a new problem each time. The Monday summary counts open rows, not sightings.

Running the same file through ingest twice on one day counts twice. Do not re-run an ingest by hand without a reason.

The daily tripwire can fill the inbox faster than the Monday triage clears it, because all runs share the limit of ten new unmatched items a run. An "inbox over cap" finding then appears, and triage is due that week.

## 5. The finding-to-fix path

Each row goes through these steps in order. Each step has one owner.

| Step | Owner | What happens |
|---|---|---|
| 1. Sight | rory | A script or an audit report records the finding. A repeat sighting raises the count. |
| 2. Triage | rory | Sets tier, owner, fix type and next action. The deadline is seven days after first sighting. |
| 3. Packet | rory | Runs `packet.py` for the row. The row's owner checks the packet. The first line is "DRAFT: needs Spencer's OK in chat". |
| 4. Ask | coordinator | Puts the packet to Spencer in the Monday note (at most three asks a week; tier 1 at once). |
| 5. Decide | spencer | Says yes, no or wait, in his own words in chat. |
| 6. Record | coordinator | Records the approval with his exact words. Only the coordinator does this. |
| 7a. Send a DealerOn request or page package | spencer | Spencer sends the DealerOn email himself or OKs the send. The row is then marked sent by the coordinator. |
| 7b. Make the one approved Google listing edit | coordinator | Runs only the one approved command, then marks the row sent. |
| 8. Verify | rory (`verify_fix.py`) | Starts 24 hours after sent. Two passes at least 24 hours apart mark it verified. |
| 9. Chase | rory | A sent row with no conclusive result 14 days after sent (no pass and no fail) is flagged overdue. It keeps its current status and approval, and it appears in the asks with its next action and DealerOn ticket date. A conclusive fail after day 14 still reopens the row under the existing rules. |
| 10. Watch | rory | The tripwire and the weekly watch keep running. A repeat problem reopens the same row. |

A row that has failed two fix attempts moves to blocked, and Spencer decides what happens next.

## 5a. Closing a manual check

Some rules cannot be read by a script (their verify type is `manual`). A person closes them, and only the coordinator records the result. A manual check is closed this way:

1. Spencer's approval is recorded and the coordinator marks the row sent (see sections 5 and 6). Only then can a check be recorded.
2. Once the fix is in place, the coordinator checks the live page by hand and saves the evidence (a dated screenshot or saved page text) in `findings/evidence/`. The file must already exist there before the check is recorded; the register stores its hash, and `validate` fails any check whose file is missing or changed.
3. The coordinator records the check:

   `register.py --register findings/register.jsonl record-manual-check --id ID --at ISO-8601 --evidence-path PATH --by coordinator`

   The command is refused for any other `--by`, for a missing evidence path, for a row whose rule is not manual, and for a row that is not sent or verifying.
4. A manual row needs two passing checks, both after the send and at least 24 hours apart. The first check moves it to verifying; the second, at least 24 hours later, marks it verified fixed. A failed check or one without evidence does not count.
5. Nobody else records a manual check: not an agent, not Rory, and not Spencer's message on its own. A message from Spencer is still needed for any approval.

## 6. Approvals

- An approval is Spencer's own words in chat (this session or his Slack direct message).
- Approvals never come from Linear, from an agent's summary, or from a relay. The coordinator checks the source before recording.
- Only the coordinator writes approval fields. Other packages never record approval.
- **The control:** no schedule line or agent prompt may run `approve`, `record-manual-check`, `set-expected`, `transition --to sent`, or the publisher's `--approve`. Only the coordinator runs those, after reading Spencer's own message. A schedule line or agent prompt that does so is a defect: stop it and report it.
- Write commands take the time from the system clock. Never use `--now`, `--today` or `--test-mode` on the live register; they are for tests and replays only.
- An approval covers one action only. A "fix" approval never covers a "won't fix" decision, and the reverse is also true.
- The register refuses an approval whose location says Linear, an approver other than Spencer, an empty quote, or a quote source other than his own message.
- Approval is cleared whenever a row reopens, so an old yes never covers a new attempt.
- Nothing is sent, posted, published or changed on any site or listing without that approval. Packets and the Monday note are drafts until he says yes.

## 7. Pausing the loop

To pause everything, add `#PAUSED ` to the front of each active line in Mac mini 1's schedule. The six lines are the daily tripwire, the daily tripwire ingest, the Monday full watch, the Monday ingest, the Monday summary and the daily fix checker. Save a copy of the schedule before editing it, in `_backups/`.

To pause one piece only, change only that line.

Pausing does not undo anything. Rows keep their status. A paused fix checker means fixes stay in "sent" until it is turned back on.

## 8. Rolling back

- **Schedule:** restore the saved copy from `_backups/`, then check the lines match the copy.
- **Code:** revert the merged pull request in the SEO repository with a new commit. Do not delete files.
- **Register:** restore the last good `register.jsonl` from the repository history only with the coordinator's approval. Never edit rows by hand. Approvals in the restored file must still match Spencer's messages.
- **Moved files:** any file taken out of service goes to `_expired/<date>/`. Nothing is deleted with `rm`.

## 9. When a step fails

| What you see | What it means | What to do |
|---|---|---|
| A watch line says "not observed" | A page timed out, was unreachable, or returned a server error. | Nothing changes. Check again at the next run. Repeated misses go in the Monday note as "not verified". |
| `register.py validate` prints INVALID lines | A row breaks a rule. | Stop. Do not run ingest, the summary or the fix checker until fixed. Tell the coordinator the row ID. |
| A command seems to hang | The register lock waits silently for another run that is writing. No message is printed. | Wait for the other run to finish. Check the running processes before doing anything else. Do not delete the lock file. If nothing is running after ten minutes, the coordinator decides. |
| Ingest says "not ingested" for a report | The report has no findings block, the block is malformed, or the report has no usable date (see section 4b). | Nothing from that report is recorded. The report's owner fixes the job that writes it. |
| Inbox reaches its limit, and an "inbox over cap" finding appears | More unmatched items than the weekly limit. | Rory maps or drops each inbox item this week. |
| Summary script exits with an error | An input file is missing or unreadable. | The schedule's redirect creates the file before the script runs, so a failed run can leave an empty file in `summaries/`. Treat a zero-byte summary as no summary. The coordinator reads the register directly for the Monday note. |
| A number in the summary says "not verified" | The source file for that number was missing or incomplete. | Fix the source and rebuild the baseline. Never type a number in by hand. |
| `ai_answers.py` refuses with the spend limit | Running it would pass $25 total or $15 for AI answers this month. | Stop until next month or until Spencer raises the limit in chat. |
| Packet refused | The packet breaks a rule (for example, a Toyota row names a Chevrolet offer, or a phone number other than 712-792-5000 appears in our wording). | Fix the row or the wording and run again. A refused packet writes nothing. |

## 10. Things to close before go-live

**Required reading before any go-live step: `build/KNOWN-LIMITS.md`.** Three limits block named steps: live paid AI-answer capture (the spend guard is not matched to a real ledger), trusting the fix checker on live sites (page proof is untested against DealerOn's real missing and redirected pages), and relying on GBP approvals tied to exact wording (the publisher still trusts the draft's approval line).

These are gaps in this build. Each one must be closed, or Spencer must accept it in chat, before any line is unpaused.

1. **Report files.** The lead's Monday job and the other report jobs must write their reports into `findings/reports/` with the findings block at the end. Their prompts change under the Class B steps; until then, the ingest step has nothing to read.
2. **Spend ledger format.** The AI-answer script assumes a ledger format that has not been checked against the real ledger. Check it before the first live run.
3. **Baseline inputs.** `baseline.py` needs the search, analytics, listing and lead files pulled by other jobs. Those pulls are not built here.
4. **Organic-lead definition** needs Spencer's OK (decision 2 in the gap plan).
5. **`REGISTER.md`** is refreshed by hand on Mondays until a scheduled step exists.
6. **Monday note** is a file only. Sending it to Spencer is a separate go-live step that needs his OK.
7. **Same-day tier 1 delivery is not built.** A tier 1 finding (for example, a noindex on a money page) reaches the register on the morning of the tripwire run, but nothing alerts Spencer that day. Until he approves an alert in chat, tier 1 rows appear only in the register and in the Monday summary. Do not turn on any alert before his OK.

## 11. First-time setup on Mac mini 1 (before anything is unpaused)

1. Create the folders listed in section 2 (`findings/watch`, `findings/reports`, `findings/summaries`, `findings/logs`, `findings/evidence`, `findings/packets`, `findings/baselines`, `_backups`, `_expired`). The scripts do not create them.
2. Put the scripts in `tools/seo-loop/` and the checks and facts in `findings/`, all through the repository. The scripts to install are:
   - `register.py` and `schema.json` (the register; every other script imports them)
   - `site_watch.py` and `urls.json`
   - `ingest_reports.py` and `map_rules.json`
   - `verify_fix.py`
   - `monday_summary.py`
   - `packet.py` and its `templates/` folder
   - `baseline.py` and `baseline.schema.json`
   - `ai_answers.py`, `questions.B2.json` and `is_us.json` (do not schedule until Spencer approves the question set and the spend source is fixed)
   - `public_wording.py` from package SA-19 (the packet builder, page gate, page packager and GBP packet will not start without it)
   Check each install against the matching README before going live.
3. Run `register.py validate` on the seed register. It must exit 0.
4. Save the current schedule to `_backups/` and confirm it matches the live schedule.
5. Add the six proposed lines as paused lines, and check them with a dry run.
6. Unpause one line at a time, and only when Spencer names it.
