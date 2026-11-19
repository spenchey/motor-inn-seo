#!/usr/bin/env python3
"""Reconcile organic leads (definition v1) from a GA4 export and a CRM export.

Reads two CSV files of totals, never customer data, and prints one table per
site, the CRM check line, and engagement actions kept apart. Prints text only.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys

NOT_VERIFIED = "not verified"
UNVERIFIED = "unverified"

SITES = [
    ("group", "Group site (motorinnautogroup.com)"),
    ("toyota", "Toyota site (motorinntoyotaofcarroll.com)"),
    ("chevy", "Chevrolet site (motorinnofcarroll.com)"),
]
PARTS = [
    ("form_leads", "Form leads"),
    ("phone_taps", "Phone taps"),
    ("service_bookings", "Service bookings"),
]

GA4_COLUMNS = ["month", "site", "channel", "event_name", "event_count"]
CRM_COLUMNS = ["month", "source", "lead_count"]

# Column-name tokens that mark customer data.
SENSITIVE_TOKENS = {
    "email", "emails", "phone", "phones", "mobile", "cell", "tel", "telephone",
    "address", "addresses", "vin", "customer", "customers", "contact",
    "contacts", "firstname", "lastname", "fullname", "fname", "lname",
    "zip", "zipcode", "ssn", "dob",
}
# "name" alone is sensitive; these words beside it make a harmless label
# such as event_name or source_name.
HARMLESS_NAME_PREFIXES = {"event", "source", "channel", "site", "host", "hostname", "page", "part"}


class InputError(Exception):
    """A problem with an input; the message never contains a cell value."""


def column_is_sensitive(col: str) -> bool:
    tokens = [t for t in re.split(r"[^a-z0-9]+", col.strip().lower()) if t]
    if not tokens:
        return False
    for t in tokens:
        if t in SENSITIVE_TOKENS:
            return True
    if "name" in tokens or "names" in tokens:
        others = [t for t in tokens if t not in ("name", "names")]
        if not others or not set(others) <= HARMLESS_NAME_PREFIXES:
            return True
    return False


def read_csv(path: str, label: str, required: list):
    """Return a list of dict rows. Refuses customer-data columns before reading any row."""
    try:
        with io.open(path, "r", encoding="utf-8-sig", newline="") as fh:
            reader = csv.reader(fh)
            try:
                header = next(reader)
            except StopIteration:
                raise InputError("%s file is empty" % label)
            header = [h.strip().lower() for h in header]
            bad = [h for h in header if column_is_sensitive(h)]
            if bad:
                raise InputError(
                    "%s file refused: it has customer-data column(s) %s. "
                    "Export totals only. No rows were read." % (label, ", ".join(sorted(set(bad))))
                )
            missing = [c for c in required if c not in header]
            if missing:
                raise InputError("%s file is missing column(s): %s" % (label, ", ".join(missing)))
            rows = []
            for lineno, rec in enumerate(reader, start=2):
                if not rec or all(not c.strip() for c in rec):
                    continue
                if len(rec) != len(header):
                    raise InputError("%s file line %d has the wrong number of columns" % (label, lineno))
                rows.append((lineno, dict(zip(header, rec))))
            return rows
    except (IOError, OSError) as exc:
        raise InputError("cannot read %s file: %s" % (label, exc.strerror or "error"))
    except UnicodeDecodeError:
        raise InputError("%s file is not readable text" % label)
    except csv.Error:
        raise InputError("%s file is not valid CSV" % label)


def to_count(value: str, label: str, lineno: int) -> int:
    try:
        n = int(value.strip().replace(",", ""))
    except ValueError:
        raise InputError("%s file line %d: count is not a whole number" % (label, lineno))
    if n < 0:
        raise InputError("%s file line %d: count is negative" % (label, lineno))
    return n


def load_map(path: str) -> dict:
    try:
        with io.open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (IOError, OSError) as exc:
        raise InputError("cannot read map file: %s" % (exc.strerror or "error"))
    except ValueError:
        raise InputError("map file is not valid JSON")
    if not isinstance(data, dict):
        raise InputError("map file must be a JSON object")
    return data


def _value(node, key):
    if isinstance(node, dict):
        return node.get(key, UNVERIFIED)
    return UNVERIFIED


def name_list(raw):
    """A confirmed mapping value is a non-empty list of strings; anything else is unverified."""
    if isinstance(raw, list) and raw and all(isinstance(x, str) and x.strip() for x in raw):
        return [x.strip().lower() for x in raw]
    return None


def resolve_map(m: dict) -> dict:
    channel_raw = _value(m.get("ga4_channel"), "value")
    channel = channel_raw.strip().lower() if isinstance(channel_raw, str) and channel_raw != UNVERIFIED else None
    split_ok = _value(m.get("site_split"), "value") == "verified"
    parts = m.get("parts") if isinstance(m.get("parts"), dict) else {}
    out = {
        "ga4_ready": bool(channel) and split_ok,
        "channel": channel,
        "parts": {},
        "crm_sources": name_list(_value(m.get("crm_check"), "crm_sources")),
        "engagement": name_list(_value(m.get("engagement_actions"), "ga4_events")),
    }
    for key, _label in PARTS:
        out["parts"][key] = name_list(_value(parts.get(key), "ga4_events"))
    return out


def sum_ga4(rows, month, rmap):
    """Return (per-site per-part counts, engagement total, skipped_unknown_site)."""
    counts = {s: {p: 0 for p, _ in PARTS} for s, _ in SITES}
    engagement = 0
    unknown_site = 0
    site_keys = set(counts)
    for lineno, r in rows:
        if r["month"].strip() != month:
            continue
        if rmap["channel"] is None or r["channel"].strip().lower() != rmap["channel"]:
            continue
        n = to_count(r["event_count"], "GA4", lineno)
        ev = r["event_name"].strip().lower()
        site = r["site"].strip().lower()
        if rmap["engagement"] and ev in rmap["engagement"]:
            engagement += n
        for key, _label in PARTS:
            names = rmap["parts"][key]
            if names and ev in names:
                if site in site_keys:
                    counts[site][key] += n
                else:
                    unknown_site += n
    return counts, engagement, unknown_site


def sum_crm(rows, month, sources):
    total = 0
    for lineno, r in rows:
        if r["month"].strip() != month:
            continue
        if r["source"].strip().lower() in sources:
            total += to_count(r["lead_count"], "CRM", lineno)
    return total


def table(title, cells):
    """cells: list of (label, value-string)."""
    width = max(len(l) for l, _ in cells)
    lines = [title]
    for label, val in cells:
        lines.append("  %s  %s" % (label.ljust(width), val))
    return "\n".join(lines)


def build_report(month, ga4_rows, crm_rows, rmap) -> str:
    ga4_counts = engagement = unknown_site = None
    if ga4_rows is not None:
        ga4_counts, engagement, unknown_site = sum_ga4(ga4_rows, month, rmap)

    def part_value(site, key):
        if not rmap["ga4_ready"] or rmap["parts"][key] is None or ga4_counts is None:
            return None
        return ga4_counts[site][key]

    out = ["Organic leads, %s (definition v1: form leads + phone taps + service bookings from unpaid search)" % month, ""]
    site_totals = {}
    for site, label in SITES:
        vals = [(plabel, part_value(site, key)) for key, plabel in PARTS]
        cells = [(plabel, NOT_VERIFIED if v is None else str(v)) for plabel, v in vals]
        if any(v is None for _, v in vals):
            total = None
        else:
            total = sum(v for _, v in vals)
        site_totals[site] = total
        cells.append(("Total", NOT_VERIFIED if total is None else str(total)))
        out.append(table(label, cells))
        out.append("")

    if any(t is None for t in site_totals.values()):
        all_total = None
    else:
        all_total = sum(site_totals.values())
    out.append(table("All three sites", [("Organic leads (A+B+C)", NOT_VERIFIED if all_total is None else str(all_total))]))
    out.append("")

    # CRM check line.
    if rmap["crm_sources"] is None:
        crm_total = None
        crm_line = "CRM check: %s (the list of CRM sources that mean website organic is not confirmed)." % NOT_VERIFIED
    else:
        crm_total = sum_crm(crm_rows, month, set(rmap["crm_sources"]))
        if all_total is None:
            crm_line = ("CRM check: %d CRM leads from the agreed website-organic sources. "
                        "Gap to Google Analytics: %s (Google Analytics total is not verified)." % (crm_total, NOT_VERIFIED))
        else:
            gap = crm_total - all_total
            if gap == 0:
                words = "equal"
            elif gap > 0:
                words = "CRM is higher by %d" % gap
            else:
                words = "Google Analytics is higher by %d" % (-gap)
            crm_line = ("CRM check: %d CRM leads from the agreed website-organic sources, "
                        "against %d organic leads from Google Analytics. Gap: %s." % (crm_total, all_total, words))
    out.append(crm_line)
    out.append("")

    # Kept apart.
    out.append("Not leads (shown apart, never added to the total above):")
    if rmap["engagement"] is None or not rmap["ga4_ready"] or engagement is None:
        eng = NOT_VERIFIED
    else:
        eng = str(engagement)
    out.append("  Engagement actions: %s" % eng)
    out.append("  Google Business Profile actions: not part of these inputs; report them under their own heading")
    if unknown_site:
        out.append("")
        out.append("Note: %d counted event(s) had a site label other than group, toyota or chevy and were left out." % unknown_site)
    return "\n".join(out) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Reconcile organic leads from a GA4 totals CSV and a CRM totals CSV. Totals only; "
        "files with customer-data columns are refused.")
    ap.add_argument("--ga4", required=True, help="GA4 CSV with columns: " + ",".join(GA4_COLUMNS))
    ap.add_argument("--crm", required=True, help="CRM CSV with columns: " + ",".join(CRM_COLUMNS))
    ap.add_argument("--map", required=True, help="lead_map.json")
    ap.add_argument("--month", required=True, help="YYYY-MM")
    ap.add_argument("--out", help="also write the report to this file")
    args = ap.parse_args(argv)

    try:
        if not re.match(r"^\d{4}-(0[1-9]|1[0-2])$", args.month):
            raise InputError("--month must look like YYYY-MM")
        rmap = resolve_map(load_map(args.map))
        ga4_rows = read_csv(args.ga4, "GA4", GA4_COLUMNS)
        crm_rows = read_csv(args.crm, "CRM", CRM_COLUMNS)
        report = build_report(args.month, ga4_rows, crm_rows, rmap)
        if args.out:
            try:
                with io.open(args.out, "w", encoding="utf-8") as fh:
                    fh.write(report)
            except (IOError, OSError) as exc:
                raise InputError("cannot write --out file: %s" % (exc.strerror or "error"))
    except InputError as exc:
        sys.stderr.write("error: %s\n" % exc)
        return 1
    sys.stdout.write(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
