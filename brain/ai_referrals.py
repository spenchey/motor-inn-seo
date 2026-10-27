#!/usr/bin/env python3
"""AI referral traffic counts from GA4 property 364125348 (read-only)."""
import json, re
from pathlib import Path
import sys; sys.path.insert(0, "/Users/spencerheywood/Documents/motorinn-ga4")
from ga4_common import mint_sa, run_report

MATCH = re.compile(r"(?i)(chatgpt|openai|perplexity|copilot|gemini|edgeservices)")

def main():
    at = mint_sa()
    r = run_report(
        dims=["sessionSource"], mets=["sessions"],
        date_ranges=[{"startDate": "28daysAgo", "endDate": "yesterday"}],
        dim_filter={"filter": {
            "fieldName": "sessionSource",
            "stringFilter": {"matchType": "PARTIAL_REGEXP", "caseSensitive": False,
              "value": "(?i)(chatgpt|openai|perplexity|copilot|gemini|edgeservices)"}}},
        at=at,
    )
    for row in r.get("rows", []):
        src = row["dimensionValues"][0]["value"]
        if MATCH.search(src):
            print(f"{src}\t{row['metricValues'][0]['value']}")

if __name__ == "__main__":
    main()
