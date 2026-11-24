# AI referrals (visits and leads from AI assistants)

Read-only. No cron line is installed for it.

`ai_referrals.py` asks the existing GA4 reader (`~/clawd/scripts/no-model/ga4-cli.py`, property 364125348)
for three aggregate reports per month (source x medium sessions; source x event counts; source x landing page
sessions), keeps the rows whose source is an AI assistant, and writes:

    "ai_referrals": {"2026-11": {"sessions": {value, window, source, pulled_at},
                                 "leads":    {value, window, source, pulled_at},
                                 "by_source": {"chatgpt": {"sessions": 4, "leads": 0}},
                                 "top_landing_pages": [{"path": "/new-toyota", "sessions": 3}]}}

It is a separate block from `ai_answers` (which means "did an AI answer name us").
A failed GA4 call gives the text `not verified`, never 0.

## Use

    python3 -I ai_referrals.py --month 2026-10 --month 2026-11 \
        --baseline baselines/2026-11.json --out baselines/2026-11.json

Prints one line per month: `AI assistants sent 7 visits, 4 leads (forms + calls), Nov 1–23.`
Other keys and other months in the file are kept. The current month runs to yesterday.

## Definitions
- Assistant sources: chatgpt.com / chat.openai.com, perplexity.ai, gemini.google.com, copilot.microsoft.com,
  claude.ai, grok, deepseek, you.com, phind, meta.ai, poe, plus any source GA4 labels medium `ai-assistant`.
- Bing organic is NOT counted (a Bing search click, not a Copilot answer; GA4 cannot split them).
- Lead = `asc_form_submission` + `asc_click_to_call` event counts from those sources. A visit that did both
  counts twice, so leads is an upper bound by at most that overlap. Leads never exceed visits for one assistant.
- Visits where the assistant hid its referrer land in "direct" and are not counted. This is a floor.

## Run order and the Monday summary
- `ai_referrals.py` must run AFTER `baseline.py`. `baseline.py` rebuilds the whole file from its schema and drops
  any block it does not know, so an `ai_referrals` block written before it would be lost.
- `monday_summary.py` reads the newest month in the block and prints
  `AI assistants sent N visits, M leads (forms + calls), Nov 1–23.` When the baselines file has no
  `ai_referrals` block, or the newest month has a number that is not verified, it prints
  `AI assistant visits: not verified.` When the data ended more than 8 days before the summary date it prints
  `AI assistant visits: not verified (stale).`

## Tests
    python3 -I -m unittest discover -s tools/seo-loop/tests -t tools/seo-loop
