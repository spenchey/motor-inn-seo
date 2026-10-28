#!/usr/bin/env python3
"""AI referral traffic from GA4 property 364125348 (read-only)."""
import json, re
from pathlib import Path
import sys; sys.path.insert(0, "/Users/spencerheywood/Documents/motorinn-ga4")
from ga4_common import mint_sa, run_report

MATCH = re.compile(r"(?i)(chatgpt|openai|perplexity|copilot|gemini|edgeservices)")
VALUE = "(?i)(chatgpt|openai|perplexity|copilot|gemini|edgeservices)"

def fetch_referrals(days_ago: int):
    """Return current or prior period rows as {source: {sessions, users}}."""
    at = mint_sa()
    start = f"{days_ago + 27}daysAgo"
    end = f"{days_ago}daysAgo"
    r = run_report(
        dims=["sessionSource"], mets=["sessions", "totalUsers"],
        date_ranges=[{"startDate": start, "endDate": end}],
        dim_filter={"filter": {
            "fieldName": "sessionSource",
            "stringFilter": {"matchType": "PARTIAL_REGEXP", "caseSensitive": False, "value": VALUE}}},
        at=at,
    )
    result = {}
    for row in r.get("rows", []):
        src = row["dimensionValues"][0]["value"]
        if MATCH.search(src):
            result[src] = {"sessions": int(row["metricValues"][0]["value"]), "users": int(row["metricValues"][1]["value"])}
    return result

def report_rows():
    current = fetch_referrals(0)
    prior = fetch_referrals(28)
    rows = []
    for src in sorted(set(current) | set(prior)):
        c = current.get(src, {"sessions": 0, "users": 0})
        p = prior.get(src, {"sessions": 0, "users": 0})
        delta = c["sessions"] - p["sessions"]
        pct = ((c["sessions"] / p["sessions"]) - 1) * 100 if p["sessions"] else (100.0 if c["sessions"] and not p["sessions"] else 0.0)
        arrow = "up" if delta > 0 else ("down" if delta < 0 else "flat")
        rows.append({
            "source": src, "sessions": c["sessions"], "users": c["users"],
            "prior_sessions": p["sessions"], "delta": delta,
            "trend": f"{arrow} {pct:+.1f}%",
            "trend_css": "trend-up" if delta > 0 else ("trend-down" if delta < 0 else "trend-flat"),
        })
    return rows

def write_html(rows):
    out = Path("brain/reports/ai-visits-latest.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    css = "body{font-family:-apple-system,'Helvetica Neue',Helvetica,Arial,sans-serif;color:#111;background:#fff;margin:0;padding:32px;}h1{font-weight:600;margin:0 0 4px;}p.summary{color:#555;margin:0 0 24px;}table{width:100%;border-collapse:collapse;font-size:14px;}th,td{text-align:left;padding:8px 12px;border-bottom:1px solid #ddd;}th{color:#555;font-size:12px;letter-spacing:.04em;text-transform:uppercase;}td.num{text-align:right;font-variant-numeric:tabular-nums;}.trend-up{color:#047857;}.trend-down{color:#b91c1c;}.trend-flat{color:#555;}.spark{display:inline-flex;gap:2px;align-items:flex-end;height:16px;}.spark i{display:block;width:3px;background:#0060e3;height:4px;}.spark i:nth-child(2){height:7px;}.spark i:nth-child(3){height:10px;}.spark i:nth-child(4){height:16px;}"
    lines = [
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>",
        "<meta name='viewport' content='width=device-width, initial-scale=1'>",
        "<title>AI referral traffic -- last 28 days</title>",
        f"<style>{css}</style></head><body>",
        "<h1>AI referral traffic</h1>",
        "<p class='summary'>GA4 property 364125348 -- last 28 days vs prior 28 days -- read-only -- regenerated weekly.</p>",
        "<table><thead><tr><th>Session source</th><th class='num'>Sessions</th><th class='num'>Users</th><th class='num'>Delta sessions</th><th>Trend</th><th>Sparkline</th></tr></thead><tbody>",
    ]
    for row in rows:
        lines.append(
            f"<tr><td>{row['source']}</td><td class='num'>{row['sessions']:,}</td><td class='num'>{row['users']:,}</td>"
            f"<td class='num'>{row['delta']:+,}</td><td class='{row['trend_css']}'>{row['trend']}</td>"
            f"<td><span class='spark' aria-hidden='true'><i></i><i></i><i></i><i></i></span></td></tr>"
        )
    lines += ["</tbody></table></body></html>", ""]
    out.write_text("\n".join(lines), encoding="utf-8")
    return out

def main():
    rows = report_rows()
    for row in rows:
        print(f"{row['source']}\t{row['sessions']}\t{row['users']}\t{row['delta']:+d}\t{row['trend']}")
    path = write_html(rows)
    print(f"HTML\t{path}")

if __name__ == "__main__":
    main()
