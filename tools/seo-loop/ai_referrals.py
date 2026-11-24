#!/usr/bin/env python3
"""Monthly count of visits and leads that came from AI assistants.

Read-only. Uses the existing GA4 reader (ga4-cli.py, GA4 property 364125348)
and writes an `ai_referrals` block into a baselines file:

    "ai_referrals": {"2026-11": {"sessions": <metric>, "leads": <metric>,
                                 "by_source": {...}, "top_landing_pages": [...]}}

This is NOT the `ai_answers` block (that one means "did an AI answer name us").
Here the number is "an AI assistant sent a person to the site". Standard
library only, Python 3.9. Sends, posts and publishes nothing. Aggregate counts
only: no per-person rows are ever read into the output.
"""
from __future__ import annotations

import argparse
import calendar
import datetime
import json
import os
import re
import subprocess
import sys
import tempfile

NOT_VERIFIED = "not verified"
SOURCE_NAME = "ga4:ai_referrals"
DEFAULT_GA4_CLI = "~/clawd/scripts/no-model/ga4-cli.py"
LEAD_EVENTS = ("asc_form_submission", "asc_click_to_call")
MONTH_RE = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")
TOP_PAGES = 5

# host fragment (matched against the lower-cased GA4 session source) -> assistant
# Bing organic search is deliberately NOT here: a "bing" source is a search click,
# not a Copilot answer, and cannot be split in GA4.
ASSISTANT_RULES = (
    ("chatgpt", ("chatgpt.com", "chat.openai.com", "openai.com", "chatgpt")),
    ("perplexity", ("perplexity.ai", "perplexity")),
    ("gemini", ("gemini.google.com", "bard.google.com", "gemini")),
    ("copilot", ("copilot.microsoft.com", "copilot.cloud.microsoft", "copilot")),
    ("claude", ("claude.ai", "claude.com")),
    ("grok", ("grok.com", "x.ai")),
    ("deepseek", ("chat.deepseek.com", "deepseek")),
    ("you.com", ("you.com",)),
    ("phind", ("phind.com",)),
    ("meta_ai", ("meta.ai",)),
    ("poe", ("poe.com",)),
)
AI_MEDIUMS = ("ai-assistant", "ai_assistant")


class AiReferralError(Exception):
    """A refusal. Nothing is written."""


def classify_source(source, medium=""):
    """Return the assistant name for a GA4 session source/medium, or None."""
    src = (source or "").strip().lower()
    med = (medium or "").strip().lower()
    if src.startswith("www."):
        src = src[4:]
    for name, needles in ASSISTANT_RULES:
        for needle in needles:
            if "." in needle:
                if src == needle or src.endswith("." + needle):
                    return name
            elif needle in src:
                return name
    if med in AI_MEDIUMS:
        return "other_ai"
    return None


def month_window(month, today=None):
    """Return (start, end) dates for a month; the current month ends yesterday."""
    if not MONTH_RE.match(month or ""):
        raise AiReferralError("month must look like YYYY-MM (got %r)" % (month,))
    year, mon = int(month[:4]), int(month[5:])
    start = datetime.date(year, mon, 1)
    end = datetime.date(year, mon, calendar.monthrange(year, mon)[1])
    today = today or datetime.date.today()
    if start > today:
        raise AiReferralError("month %s has not started yet" % month)
    yesterday = today - datetime.timedelta(days=1)
    if end > yesterday:
        end = yesterday
    if end < start:
        raise AiReferralError("month %s has no finished day yet" % month)
    return start, end


def ga4_runner(cli_path):
    """Return fn(start, end, dims, metrics) -> list of dict, using the GA4 reader."""
    cli = os.path.expanduser(cli_path)

    def run(start, end, dims, metrics):
        cmd = [cli, "report", "-s", start, "-e", end, "-d", ",".join(dims),
               "-m", ",".join(metrics), "-l", "100000", "-f", "json"]
        try:
            proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  universal_newlines=True, timeout=180)
        except (OSError, subprocess.SubprocessError) as exc:
            raise AiReferralError("GA4 reader did not run: %s" % exc)
        if proc.returncode != 0:
            raise AiReferralError("GA4 reader failed: %s" % proc.stderr.strip()[:200])
        try:
            rows = json.loads(proc.stdout)
        except ValueError:
            raise AiReferralError("GA4 reader gave output that is not JSON")
        if not isinstance(rows, list):
            raise AiReferralError("GA4 reader gave an unexpected shape")
        return rows

    return run


def _num(value):
    if isinstance(value, bool):
        return 0
    if isinstance(value, (int, float)):
        return int(value)
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def _clean_path(path):
    path = (path or "").split("?", 1)[0].split("#", 1)[0]
    return path or "/"


def pull_month(month, run, today=None, pulled_at=None):
    """Pull one month. Returns the block for that month.

    If a GA4 call fails the numbers are the text "not verified", never zero.
    """
    start, end = month_window(month, today)
    window = "%s..%s" % (start.isoformat(), end.isoformat())
    pulled_at = pulled_at or datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    s, e = start.isoformat(), end.isoformat()

    def metric(value):
        return {"value": value, "window": window, "source": SOURCE_NAME, "pulled_at": pulled_at}

    try:
        src_rows = run(s, e, ["sessionSource", "sessionMedium"], ["sessions"])
        ev_rows = run(s, e, ["sessionSource", "eventName"], ["eventCount"])
        lp_rows = run(s, e, ["sessionSource", "landingPagePlusQueryString"], ["sessions"])
    except AiReferralError:
        return {"sessions": NOT_VERIFIED, "leads": NOT_VERIFIED,
                "by_source": NOT_VERIFIED, "top_landing_pages": NOT_VERIFIED}

    by_source = {}
    medium_of = {}
    for row in src_rows:
        name = classify_source(row.get("sessionSource"), row.get("sessionMedium"))
        if name:
            by_source.setdefault(name, {"sessions": 0, "leads": 0})
            by_source[name]["sessions"] += _num(row.get("sessions"))
            medium_of[(row.get("sessionSource") or "").lower()] = name
    # events and landing rows carry only the source: resolve it the same way,
    # falling back to the name found through the medium above
    def name_for(source):
        return classify_source(source) or medium_of.get((source or "").lower())

    for row in ev_rows:
        if row.get("eventName") in LEAD_EVENTS:
            name = name_for(row.get("sessionSource"))
            if name:
                by_source.setdefault(name, {"sessions": 0, "leads": 0})
                by_source[name]["leads"] += _num(row.get("eventCount"))
    pages = {}
    for row in lp_rows:
        if name_for(row.get("sessionSource")):
            p = _clean_path(row.get("landingPagePlusQueryString"))
            pages[p] = pages.get(p, 0) + _num(row.get("sessions"))
    top = sorted(pages.items(), key=lambda kv: (-kv[1], kv[0]))[:TOP_PAGES]
    return {
        "sessions": metric(sum(v["sessions"] for v in by_source.values())),
        "leads": metric(sum(v["leads"] for v in by_source.values())),
        "by_source": {k: by_source[k] for k in sorted(by_source)},
        "top_landing_pages": [{"path": p, "sessions": n} for p, n in top],
    }


def _metric_value(block, key):
    node = block.get(key) if isinstance(block, dict) else None
    if isinstance(node, dict) and isinstance(node.get("value"), (int, float)) \
            and not isinstance(node.get("value"), bool):
        return int(node["value"])
    return None


def summary_line(month, block):
    """One plain sentence for the Monday summary."""
    label = datetime.date(int(month[:4]), int(month[5:]), 1).strftime("%B")
    sessions, leads = _metric_value(block, "sessions"), _metric_value(block, "leads")
    if sessions is None or leads is None:
        return "AI assistant visits for %s: not verified." % label
    return "AI assistants sent %d %s, %d %s in %s." % (
        sessions, "visit" if sessions == 1 else "visits",
        leads, "lead" if leads == 1 else "leads", label)


def load_json(path):
    if not path or not os.path.isfile(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError) as exc:
        raise AiReferralError("cannot read %s: %s" % (path, exc))
    if not isinstance(data, dict):
        raise AiReferralError("%s: top level must be a JSON object" % path)
    return data


def merge_block(doc, month, block):
    """Add this month to doc['ai_referrals'] without touching any other key."""
    out = dict(doc)
    existing = out.get("ai_referrals")
    merged = dict(existing) if isinstance(existing, dict) else {}
    merged[month] = block
    out["ai_referrals"] = {k: merged[k] for k in sorted(merged)}
    return out


def write_atomic(path, payload):
    out_dir = os.path.dirname(os.path.abspath(path))
    os.makedirs(out_dir, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".ai-referrals-", suffix=".tmp", dir=out_dir)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def main(argv=None, run=None, today=None):
    p = argparse.ArgumentParser(description=(
        "Read-only: count monthly visits and leads from AI assistants via GA4 and "
        "add an ai_referrals block to a baselines file."))
    p.add_argument("--month", action="append", required=True,
                   help="YYYY-MM; repeat for several months")
    p.add_argument("--baseline", default=None,
                   help="existing baselines JSON to start from (kept as is, plus ai_referrals)")
    p.add_argument("--out", required=True, help="file to write")
    p.add_argument("--ga4-cli", default=DEFAULT_GA4_CLI, help="path to the GA4 reader")
    args = p.parse_args(argv)

    runner = run or ga4_runner(args.ga4_cli)
    try:
        doc = load_json(args.baseline or (args.out if os.path.isfile(args.out) else None))
        lines = []
        for month in args.month:
            block = pull_month(month, runner, today=today)
            doc = merge_block(doc, month, block)
            lines.append(summary_line(month, block))
        write_atomic(args.out, doc)
    except AiReferralError as exc:
        sys.stderr.write("refused: %s\n" % exc)
        return 1
    except OSError as exc:
        sys.stderr.write("write failed: %s\n" % exc)
        return 1
    for line in lines:
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
