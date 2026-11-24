#!/usr/bin/env python3
"""Turn one read-only Google Analytics pull into the leads.json input that baseline.py reads.

Spencer's approved "organic leads" definition (2026-11-24): the events asc_form_submission and
asc_click_to_call, counted where the session channel group is "Organic Search", for the whole
Google Analytics property. The CRM website-lead count is an optional second number, shown as a
check line and never added to the headline.

Input: the JSON that `ga4-cli.py report` prints for dimensions eventName, sessionDefaultChannelGroup,
hostName and metric eventCount. Reads files only; makes no network calls. Stdlib only.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
import tempfile

EVENTS = ("asc_form_submission", "asc_click_to_call")  # exactly the approved events; nothing else counts
CHANNEL = "Organic Search"
SITE_HOSTS = {
    "group": "www.motorinnautogroup.com",
    "toyota": "www.motorinntoyotaofcarroll.com",
    "chevy": "www.motorinnofcarroll.com",
}
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class LeadsError(Exception):
    pass


def _check_date(text, label):
    if not isinstance(text, str) or not DATE.match(text):
        raise LeadsError("%s must look like YYYY-MM-DD" % label)
    try:
        datetime.datetime.strptime(text, "%Y-%m-%d")
    except ValueError:
        raise LeadsError("%s is not a real date" % label)


def build(rows, start, end, property_id, pulled_at, crm_count=None, crm_source=None):
    _check_date(start, "--start")
    _check_date(end, "--end")
    if start > end:
        raise LeadsError("--start is after --end")
    if not isinstance(rows, list):
        raise LeadsError("the pull must be a JSON list of rows")
    window = "%s..%s" % (start, end)
    total = 0
    per_site = dict((name, 0) for name in SITE_HOSTS)
    host_seen = set()  # a site is "measured" only if the property recorded any event on its host
    for row in rows:
        if not isinstance(row, dict):
            raise LeadsError("a row is not an object")
        for key in ("eventName", "sessionDefaultChannelGroup", "hostName", "eventCount"):
            if key not in row:
                raise LeadsError("a row is missing %s" % key)
        count = row["eventCount"]
        if isinstance(count, bool) or not isinstance(count, int) or count < 0:
            raise LeadsError("eventCount must be a whole number, not negative")
        host_seen.add(row["hostName"])
        if row["sessionDefaultChannelGroup"] == CHANNEL and row["eventName"] in EVENTS:
            total += count
            for name, host in SITE_HOSTS.items():
                if row["hostName"] == host:
                    per_site[name] += count
    source = ("Google Analytics property %s, events %s, channel %s"
              % (property_id, " + ".join(EVENTS), CHANNEL))
    out = {}
    for name, host in SITE_HOSTS.items():
        if host in host_seen:  # unmeasured sites are left out, so baseline.py writes "not verified"
            out[name] = {"organic_leads": {"value": per_site[name], "window": window,
                                           "source": source + ", host " + host, "pulled_at": pulled_at}}
    allnode = {"organic_leads_total": {"value": total, "window": window,
                                       "source": source + " (whole property)", "pulled_at": pulled_at}}
    if crm_count is not None:
        if isinstance(crm_count, bool) or not isinstance(crm_count, int) or crm_count < 0:
            raise LeadsError("--crm-count must be a whole number, not negative")
        allnode["crm_website_leads"] = {
            "value": crm_count, "window": window,
            "source": crm_source or "CRM lead source table, own-website class, counts only",
            "pulled_at": pulled_at}
    out["all"] = allnode
    return out


def write_atomic(path, payload):
    folder = os.path.dirname(os.path.abspath(path))
    os.makedirs(folder, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".leads-", suffix=".tmp", dir=folder)
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


def main(argv=None):
    p = argparse.ArgumentParser(description="Build leads.json for baseline.py from a Google Analytics pull. No network calls.")
    p.add_argument("--ga4-report", required=True, help="JSON from ga4-cli report (eventName, sessionDefaultChannelGroup, hostName, eventCount)")
    p.add_argument("--start", required=True, help="first day of the pulled window, YYYY-MM-DD")
    p.add_argument("--end", required=True, help="last day of the pulled window, YYYY-MM-DD")
    p.add_argument("--property", default="364125348", help="Google Analytics property id, for the source text")
    p.add_argument("--pulled-at", default=None, help="ISO-8601 time of the pull (default: now, UTC)")
    p.add_argument("--crm-count", type=int, default=None, help="CRM website leads for the same window (counts only)")
    p.add_argument("--crm-source", default=None, help="how the CRM count was made")
    p.add_argument("--out", required=True, help="leads.json to write")
    a = p.parse_args(argv)
    pulled = a.pulled_at or datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        with open(a.ga4_report, "r", encoding="utf-8") as fh:
            rows = json.load(fh)
        payload = build(rows, a.start, a.end, a.property, pulled, a.crm_count, a.crm_source)
        write_atomic(a.out, payload)
    except (LeadsError, OSError, ValueError) as exc:
        sys.stderr.write("refused: %s\n" % exc)
        return 1
    print("wrote %s: organic leads total %s" % (a.out, payload["all"]["organic_leads_total"]["value"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
