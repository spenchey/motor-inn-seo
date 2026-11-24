#!/usr/bin/env python3
"""Monday morning refresh of the numbers the Monday summary reads.

Read-only and free. It reads Google Analytics, Google Search Console and a counts-only
slice of the CRM capture, then rebuilds this month's baselines file. It sends and
posts nothing. Python 3.9, standard library only.

Order matters: baseline.py rebuilds the whole file and drops blocks it does not know,
so ai_referrals.py runs AFTER it.

The reporting month is the month of yesterday. On a normal Monday that is this month.
On a Monday that is the 1st (for example 2027-02-01) there is no finished day in the new
month yet, so last month is refreshed and the summary falls back with its own note.

Anything a reader cannot give is written as the text "not verified", never as 0.
Every input file is overwritten on every run, so a failed pull can never leave last
week's number behind.
"""
from __future__ import annotations

import argparse
import calendar
import datetime as dt
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import ai_referrals  # noqa: E402
import baseline  # noqa: E402
import build_leads_input  # noqa: E402

NOT_VERIFIED = "not verified"
GA4_PROPERTY = "364125348"
DEFAULT_GA4_CLI = "~/clawd/scripts/no-model/ga4-cli.py"
DEFAULT_GSC_CLI = "~/clawd/scripts/no-model/gsc-cli.py"
DEFAULT_GSC_PYTHON = "/opt/homebrew/bin/python3.14"  # the python that has the Google libraries
DEFAULT_CRM_DB = "~/motorinn-lead-response/data/leads.db"
GSC_SITES = (
    ("group", "sc-domain:motorinnautogroup.com"),
    ("toyota", "https://www.motorinntoyotaofcarroll.com/"),
    ("chevy", "https://www.motorinnofcarroll.com/"),
)
GSC_LAG_DAYS = 3        # Search Console data settles about two days late
GSC_WINDOW_DAYS = 28
CRM_MAX_AGE_HOURS = 48  # older than this and the CRM capture is not trusted
CENTRAL = "America/Chicago"


class ReaderError(Exception):
    """A reader could not give a verified number."""


# ---------------------------------------------------------------------------
# Plain helpers
# ---------------------------------------------------------------------------

def _now():
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log(msg):
    print("%s %s" % (_now(), msg), flush=True)


def fail(msg):
    sys.stderr.write("%s FAILED: %s\n" % (_now(), msg))
    sys.stderr.flush()


def utc_stamp():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def reporting_month(today):
    """(year, month) of yesterday: the newest month that has at least one finished day."""
    y = today - dt.timedelta(days=1)
    return y.year, y.month


def month_text(ym):
    return "%04d-%02d" % ym


def previous_month(ym):
    year, month = ym
    return (year - 1, 12) if month == 1 else (year, month - 1)


def leads_window(today):
    """First of the reporting month through yesterday."""
    y = today - dt.timedelta(days=1)
    return y.replace(day=1), y


def gsc_window(today):
    end = today - dt.timedelta(days=GSC_LAG_DAYS)
    return end - dt.timedelta(days=GSC_WINDOW_DAYS - 1), end


def write_json(path, payload):
    folder = os.path.dirname(os.path.abspath(path))
    os.makedirs(folder, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".refresh-", suffix=".tmp", dir=folder)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def load_config(path):
    """Optional JSON config kept beside the live data (never in git)."""
    if not path or not os.path.isfile(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError) as exc:
        raise SystemExit("cannot read config %s: %s" % (path, exc))
    if not isinstance(data, dict):
        raise SystemExit("config %s must be a JSON object" % path)
    return data


# ---------------------------------------------------------------------------
# Readers
# ---------------------------------------------------------------------------

def _num(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return value


def gsc_clicks_reader(python, cli):
    """Return fn(site, start, end) -> int clicks, using the read-only Search Console reader."""
    py = os.path.expanduser(python)
    script = os.path.expanduser(cli)

    def run(site, start, end):
        cmd = [py, script, "--site", site, "-s", start, "-e", end, "query", "-l", "1"]
        try:
            proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  encoding="utf-8", errors="replace", timeout=120)
        except (OSError, subprocess.SubprocessError) as exc:
            raise ReaderError("Search Console reader did not run: %s" % exc)
        if proc.returncode != 0:
            said = " ".join((proc.stderr or "").split())[:160]
            raise ReaderError("Search Console reader failed: %s" % (said or "no message"))
        try:
            data = json.loads(proc.stdout)
        except ValueError:
            raise ReaderError("Search Console reader gave output that is not JSON")
        rows = data.get("rows") if isinstance(data, dict) else None
        if not rows:  # no row means no verified number; it is never read as 0
            raise ReaderError("Search Console returned no rows")
        clicks = _num(rows[0].get("clicks")) if isinstance(rows[0], dict) else None
        if clicks is None or clicks < 0:
            raise ReaderError("Search Console gave no usable clicks number")
        return int(round(clicks))

    return run


_FRAC = re.compile(r"\.(\d+)")


def _six_digits(match):
    return "." + match.group(1).ljust(6, "0")[:6]  # Python 3.9 reads fractions of exactly 3 or 6 digits


def _central_date(text):
    """CRM timestamps are ISO, with or without an offset, sometimes with 7-digit fractions.
    A timestamp with no offset is Central time."""
    from zoneinfo import ZoneInfo
    s = _FRAC.sub(_six_digits, str(text or "").strip().replace("Z", "+00:00"))
    d = dt.datetime.fromisoformat(s)  # ValueError for anything odd
    if d.tzinfo is None:
        d = d.replace(tzinfo=ZoneInfo(CENTRAL))
    return d.astimezone(ZoneInfo(CENTRAL)).date()


def crm_count_reader(db_path, now=None):
    """Return fn(start, end) -> int: own-website opportunities created in the window.

    Counts only. It opens the landed CRM capture read-only, selects opportunity ids and
    creation times (no names, emails, phones or VINs) and never touches the contact table.
    """
    path = os.path.expanduser(db_path)

    def run(start, end):
        if not os.path.isfile(path):
            raise ReaderError("CRM capture database not found")
        uri = "file:%s?mode=ro" % urllib.parse.quote(path)
        try:
            con = sqlite3.connect(uri, uri=True, timeout=30)
        except sqlite3.Error as exc:
            raise ReaderError("CRM capture could not be opened read-only: %s" % exc)
        try:
            newest = con.execute("select max(fetched_at) from lead_source").fetchone()[0]
            try:
                stamp = dt.datetime.fromisoformat(str(newest).replace("Z", "+00:00"))
                if stamp.tzinfo is None:
                    stamp = stamp.replace(tzinfo=dt.timezone.utc)
            except (TypeError, ValueError):
                raise ReaderError("CRM capture has no readable freshness time")
            current = now or dt.datetime.now(dt.timezone.utc)
            if current - stamp > dt.timedelta(hours=CRM_MAX_AGE_HOURS):
                raise ReaderError("CRM capture is older than %d hours" % CRM_MAX_AGE_HOURS)
            odd = con.execute(
                "select count(*) from crm_opportunity o join lead_source ls on ls.opportunity_id = o.opportunity_id "
                "where ls.channel_class = 'owned_web' and (o.created_date is null or o.created_date not like '____-__-__%')"
            ).fetchone()[0]
            if odd:  # a date we cannot place would silently undercount
                raise ReaderError("some CRM creation times are not in the expected format")
            floor = (start - dt.timedelta(days=1)).isoformat()
            seen = set()
            for opp_id, created in con.execute(
                    "select o.opportunity_id, o.created_date from crm_opportunity o "
                    "join lead_source ls on ls.opportunity_id = o.opportunity_id "
                    "where ls.channel_class = 'owned_web' and o.created_date >= ?", (floor,)):
                try:
                    day = _central_date(created)
                except ValueError:
                    raise ReaderError("a CRM creation time could not be read")
                if start <= day <= end:
                    seen.add(opp_id)
            return len(seen)
        except sqlite3.Error as exc:
            raise ReaderError("CRM capture query failed: %s" % exc)
        finally:
            con.close()

    return run


# ---------------------------------------------------------------------------
# Input files
# ---------------------------------------------------------------------------

def unverified_leads():
    doc = {name: {"organic_leads": NOT_VERIFIED} for name in build_leads_input.SITE_HOSTS}
    doc["all"] = {"organic_leads_total": NOT_VERIFIED, "crm_website_leads": NOT_VERIFIED}
    return doc


def make_leads_doc(ga_rows, start, end, crm_count, pulled_at):
    """leads.json content. ga_rows None means the Google Analytics pull failed."""
    crm_source = ("CRM capture, read-only, opportunities whose lead source class is own-website, "
                  "counts only")
    if ga_rows is None:
        doc = unverified_leads()
        if crm_count is not None:
            doc["all"]["crm_website_leads"] = {
                "value": crm_count, "window": "%s..%s" % (start, end),
                "source": crm_source, "pulled_at": pulled_at}
        return doc
    doc = build_leads_input.build(ga_rows, start.isoformat(), end.isoformat(), GA4_PROPERTY,
                                  pulled_at, crm_count, crm_source)
    if crm_count is None:
        doc["all"]["crm_website_leads"] = NOT_VERIFIED
    return doc


def make_gsc_doc(results, start, end, pulled_at):
    """results maps site name to clicks, or None when that site could not be read."""
    window = "%s..%s" % (start, end)
    doc = {}
    for name, _ in GSC_SITES:
        clicks = results.get(name)
        if clicks is None:
            doc[name] = {"gsc_clicks_28d": NOT_VERIFIED}
        else:
            doc[name] = {"gsc_clicks_28d": {
                "value": clicks, "window": window,
                "source": "Google Search Console, clicks, %s" % dict(GSC_SITES)[name],
                "pulled_at": pulled_at}}
    return doc


# ---------------------------------------------------------------------------
# The run
# ---------------------------------------------------------------------------

def plan(today, root):
    ym = reporting_month(today)
    month = month_text(ym)
    folder = os.path.join(root, "findings", "baselines")
    l_start, l_end = leads_window(today)
    g_start, g_end = gsc_window(today)
    months = [month_text(previous_month(ym)), month]
    return {
        "today": today.isoformat(),
        "month": month,
        "baseline": os.path.join(folder, "%s.json" % month),
        "inputs": os.path.join(folder, "inputs-%s" % month),
        "leads_window": (l_start, l_end),
        "gsc_window": (g_start, g_end),
        "ai_months": months,
        "first_of_month_note": today.day == 1,
    }


def run_refresh(root, today, ga4_rows, gsc_clicks, crm_count, ai_cli, dry_run=False):
    """Do the refresh. Returns (exit_code, problems). The readers are passed in so tests can stub them."""
    p = plan(today, root)
    l_start, l_end = p["leads_window"]
    g_start, g_end = p["gsc_window"]
    log("Monday refresh for %s: month %s, leads %s..%s, Search Console %s..%s"
        % (today, p["month"], l_start, l_end, g_start, g_end))
    if p["first_of_month_note"]:
        log("Today is the 1st: the new month has no finished day, so %s is refreshed." % p["month"])
    log("baselines file: %s" % os.path.relpath(p["baseline"], root))
    log("AI-assistant months, one call each: %s" % ", ".join(p["ai_months"]))
    if dry_run:
        log("dry run: no reader was called and nothing was written")
        return 0, []

    problems = []
    pulled_at = utc_stamp()
    os.makedirs(p["inputs"], exist_ok=True)

    # keep a dated copy of the file we are about to replace (copy only; nothing is deleted)
    if os.path.isfile(p["baseline"]):
        hist = os.path.join(os.path.dirname(p["baseline"]), "_history")
        os.makedirs(hist, exist_ok=True)
        shutil.copy2(p["baseline"], os.path.join(
            hist, "%s.%s.json" % (p["month"], dt.datetime.now().strftime("%Y%m%dT%H%M%S"))))

    # 1. organic leads (Google Analytics) and the CRM check number
    rows = None
    try:
        rows = ga4_rows(l_start.isoformat(), l_end.isoformat(),
                        ["eventName", "sessionDefaultChannelGroup", "hostName"], ["eventCount"])
    except ai_referrals.AiReferralError as exc:
        problems.append("Google Analytics leads pull: %s" % exc)
    if rows is not None and len(rows) == 0:  # an empty pull is not a verified zero
        problems.append("Google Analytics leads pull: returned no rows")
        rows = None
    crm = None
    try:
        crm = crm_count(l_start, l_end)
    except ReaderError as exc:
        problems.append("CRM check count: %s" % exc)
    try:
        doc = make_leads_doc(rows, l_start, l_end, crm, pulled_at)
    except build_leads_input.LeadsError as exc:
        problems.append("Google Analytics leads data: %s" % exc)
        doc = make_leads_doc(None, l_start, l_end, crm, pulled_at)
    write_json(os.path.join(p["inputs"], "leads.json"), doc)
    log("leads.json written (leads %s, CRM %s)"
        % ("verified" if doc["all"]["organic_leads_total"] != NOT_VERIFIED else NOT_VERIFIED,
           "verified" if crm is not None else NOT_VERIFIED))

    # 2. Search Console clicks, one site at a time
    results = {}
    for name, site in GSC_SITES:
        try:
            results[name] = gsc_clicks(site, g_start.isoformat(), g_end.isoformat())
        except ReaderError as exc:
            results[name] = None
            problems.append("Search Console clicks (%s): %s" % (name, exc))
    write_json(os.path.join(p["inputs"], "gsc.json"), make_gsc_doc(results, g_start, g_end, pulled_at))
    log("gsc.json written (%s)" % ", ".join(
        "%s %s" % (n, "verified" if results[n] is not None else NOT_VERIFIED) for n, _ in GSC_SITES))

    # 3. rebuild the whole baselines file
    code = baseline.main(["--month", p["month"], "--inputs", p["inputs"], "--out", p["baseline"]])
    if code != 0:
        problems.append("baseline.py refused to build %s" % p["month"])
        return 1, problems

    # 4. AI-assistant visits, AFTER the rebuild, one month per call
    for month in p["ai_months"]:
        argv = ["--month", month, "--baseline", p["baseline"], "--out", p["baseline"], "--ga4-cli", ai_cli]
        try:
            code = ai_referrals.main(argv, run=ga4_rows, today=today)
        except ai_referrals.AiReferralError as exc:  # pragma: no cover (main catches it)
            code = 1
            fail(str(exc))
        if code != 0:
            problems.append("AI-assistant visits for %s were not written" % month)
    # a month that came back as the text "not verified" is also a reader failure worth a line
    try:
        with open(p["baseline"], "r", encoding="utf-8") as fh:
            block = (json.load(fh).get("ai_referrals") or {})
        for month in p["ai_months"]:
            if isinstance(block.get(month), dict) and block[month].get("sessions") == NOT_VERIFIED:
                problems.append("AI-assistant visits for %s: Google Analytics pull failed" % month)
    except (OSError, ValueError):
        problems.append("could not re-read the baselines file after the AI step")
    return (1 if problems else 0), problems


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    root_default = os.path.dirname(os.path.dirname(HERE))
    ap = argparse.ArgumentParser(description="Refresh the Monday summary numbers (read-only).")
    ap.add_argument("--root", default=root_default, help="repo folder that holds findings/")
    ap.add_argument("--config", default=None, help="JSON config (default: findings/seo-loop.config.json)")
    ap.add_argument("--dry-run", action="store_true", help="print the plan; call no reader, write nothing")
    ap.add_argument("--today", default=None, help="YYYY-MM-DD; only allowed with --dry-run")
    a = ap.parse_args(argv)

    if a.today and not a.dry_run:
        sys.stderr.write("refused: --today is only for --dry-run (a real refresh must use the real date)\n")
        return 2
    try:
        today = dt.date.fromisoformat(a.today) if a.today else dt.date.today()
    except ValueError:
        sys.stderr.write("refused: --today must look like YYYY-MM-DD\n")
        return 2
    root = os.path.abspath(os.path.expanduser(a.root))
    cfg = load_config(a.config or os.path.join(root, "findings", "seo-loop.config.json"))
    ga4_cli = cfg.get("ga4_cli", DEFAULT_GA4_CLI)
    code, problems = run_refresh(
        root, today,
        ga4_rows=ai_referrals.ga4_runner(ga4_cli),
        gsc_clicks=gsc_clicks_reader(cfg.get("gsc_python", DEFAULT_GSC_PYTHON), cfg.get("gsc_cli", DEFAULT_GSC_CLI)),
        crm_count=crm_count_reader(cfg.get("crm_db", DEFAULT_CRM_DB)),
        ai_cli=ga4_cli, dry_run=a.dry_run)
    if problems:
        for item in problems:
            fail(item)
        fail("REFRESH RESULT: PARTIAL, the summary will show 'not verified' for the items above")
    elif not a.dry_run:
        log("REFRESH RESULT: ok")
    return code


if __name__ == "__main__":
    sys.exit(main())
