# AI referrals — GA4 segment spec + live report hook

## Definition
Session source matching the exact regex:

```
(?i)(chatgpt|openai|perplexity|copilot|gemini|edgeservices)
```

Matched case-insensitively against `sessionSource` only. `perplexity.ai` is covered by
`perplexity`; `edgeservices` covers Microsoft Copilot edge referrer plumbing.

## Live read method
GA4 Data API `runReport` against `properties/364125348`, using the service-account pattern
from `/Users/spencerheywood/Documents/motorinn-ga4/ga4_common.py`
(`mint_sa()` + `run_report()`).

## Exact request body
```json
{
  "dimensions": [{"name": "sessionSource"}],
  "metrics": [{"name": "sessions"}],
  "dateRanges": [{"startDate": "28daysAgo", "endDate": "yesterday"}],
  "limit": 50,
  "dimensionFilter": {
    "filter": {
      "fieldName": "sessionSource",
      "stringFilter": {
        "matchType": "PARTIAL_REGEXP",
        "caseSensitive": false,
        "value": "(?i)(chatgpt|openai|perplexity|copilot|gemini|edgeservices)"
      }
    }
  }
}
```

Note: Data API match type is `PARTIAL_REGEXP`, not `REGEX`.

## Weekly dashboard
`brain/ai_referrals.py` now also generates `brain/reports/ai-visits-latest.html` with a per-source sessions, users, and trend table. The existing weekly-intel launchd on this Mac calls the script each Monday; replicate the same call in `brain/weekly_intel_mini.sh` if that job is enabled on nada-mini.

## Reporting hook
`brain/ai_referrals.py` prints one `source<TAB>count` row per matched source. Add its
output to the weekly SEO/AI visibility digest in `agents/weekly-report.md`.

## Weekly per-source report
Current script produces:
- Console: `source<TAB>sessions<TAB>users<TAB>delta<TAB>trend`
- HTML: `brain/reports/ai-visits-latest.html` (no JS dependencies)

## Verification
Runbook has been tested live, read-only. Latest local run (2026-10-27) returned:
`chatgpt.com\t7` sessions in the last 28 days against property `364125348`.
