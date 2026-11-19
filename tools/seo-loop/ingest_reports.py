#!/usr/bin/env python3
"""Report ingest for Motor Inn's SEO findings register (package SA-10).

Normal mode reads ONLY the fenced block labelled FINDINGS-JSON in each report:
a JSON list of {check_id, site, target, observed}. Prose around the block is
never read for findings, and instruction-like text in a report is just data.

    python3 -I ingest_reports.py --register register.jsonl --checks checks.json \
        --inbox inbox.jsonl --report week-46.md --report week-47.md --today 2026-11-18

A known check_id goes through register.add_finding (tier, fix type, owner,
surface, title and expected wording come from the catalog). An unknown
check_id goes to the inbox (JSON lines, at most 10 per run); overflow is
recorded as one finding with check ID "inbox-over-cap".

--seed-map map_rules.json is the one-time backlog mode: keyword phrases in old
report text are folded onto check IDs. The block is not read in that mode.

Never calls approve. Never changes a status except through add_finding's own
re-sighting behaviour. Standard library only; no network code.
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import register  # noqa: E402

BLOCK_LABEL = "FINDINGS-JSON"
INBOX_CAP = 10
OVER_CAP_ID = "inbox-over-cap"
MAX_REPORT_BYTES = 2 * 1024 * 1024
MAX_FIELD_CHARS = 500
FORBIDDEN_NAME = "reviews-pull-*"
REMOVED = "[removed]"
DEFAULT_KNOWN_PHONES = frozenset(["7127925000"])  # the one number Motor Inn's own wording uses
KNOWN_PHONES = set(DEFAULT_KNOWN_PHONES)  # set for each run by load_known_phones()
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9\-]+(?:\.[A-Za-z0-9\-]+)*\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(?<![\d])(?:\+?1[\s.\-]?)?(?:\(\d{3}\)\s?|\d{3}[\s.\-])\d{3}[\s.\-]\d{4}(?![\d])"
                      r"|(?<![\d])(?:\+?1)?[2-9]\d{9}(?![\d])")
DATE_RE = re.compile(r"(?<!\d)(\d{4}-\d{2}-\d{2})(?!\d)")
REPORT_DATE_LINE = re.compile(r"^\s*report_date:\s*(\d{4}-\d{2}-\d{2})\s*$")


def phone_digits(text: str) -> str:
    digits = re.sub(r"\D", "", text)
    return digits[-10:] if len(digits) >= 10 else digits


def scrub(text, keep_phones=False):
    """Customer details never reach the register or inbox: e-mail addresses become [removed], and so does
    any phone number that is not on the known list. Personal names cannot be detected reliably (README).
    keep_phones=True leaves phone numbers as written: used for the observed value of site-watch candidates,
    where an unknown number on a public page is the thing Spencer has to rule on."""
    if not isinstance(text, str):
        return text
    text = EMAIL_RE.sub(REMOVED, text)
    if keep_phones:
        return text

    def phone(m):
        return m.group(0) if phone_digits(m.group(0)) in KNOWN_PHONES else REMOVED
    return PHONE_RE.sub(phone, text)


def load_known_phones(path) -> set:
    known = set(DEFAULT_KNOWN_PHONES)
    if not path:
        return known
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError) as exc:
        raise IngestError("cannot read expected-sites %s: %s" % (path, exc))

    def walk(node):
        if isinstance(node, dict):
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)
        elif isinstance(node, str):
            for m in PHONE_RE.finditer(node):
                known.add(phone_digits(m.group(0)))
    walk(data)
    return known


def date_from_name(path: str):
    """(date, None) from the one date in the file name, else (None, reason)."""
    found = sorted(set(DATE_RE.findall(os.path.basename(path))))
    good = []
    for d in found:
        try:
            register.parse_date(d)
        except register.RegisterError:
            continue
        good.append(d)
    if not good:
        return None, "no report date (no report_date line and no date in the file name)"
    if len(good) > 1:
        return None, "more than one date in the file name"
    return good[0], None


def check_not_future(date_text: str, today: str):
    if date_text > today:
        return "report date %s is after today (%s)" % (date_text, today)
    return None



# Used only when the catalog does not carry its own entry for the over-cap check.
LOCAL_CHECKS = {
    OVER_CAP_ID: {
        "check_id": OVER_CAP_ID,
        "title": "More unmatched report findings arrived in one run than the inbox holds",
        "plain_english": "A report run produced more findings than the catalog could place, so some were dropped from the inbox.",
        "tier": 3,
        "fix_type": "internal_repair",
        "owner": "rory",
        "surface": "ingest",
        "brand_scope": "both",
        "verify_template": {"type": "manual", "assert": "Inbox mapped or dropped, with a reason for each item"},
    }
}

ITEM_KEYS = ("check_id", "site", "target", "observed")


class IngestError(Exception):
    """The run cannot continue (bad argument, refused path)."""


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

def is_forbidden_path(path: str) -> bool:
    """True when the file name (or the name of what a link points at) matches reviews-pull-*."""
    names = [os.path.basename(path)]
    try:
        names.append(os.path.basename(os.path.realpath(path)))
    except OSError:
        pass
    return any(fnmatch.fnmatch(n.lower(), FORBIDDEN_NAME) for n in names)


def refuse_forbidden(paths) -> None:
    for p in paths:
        if p and is_forbidden_path(p):
            raise IngestError("refused: %s matches %s (review data is never read)" % (p, FORBIDDEN_NAME))


# ---------------------------------------------------------------------------
# Catalog
# ---------------------------------------------------------------------------

def load_catalog(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError) as exc:
        raise IngestError("cannot read catalog %s: %s" % (path, exc))
    if not isinstance(data, list):
        raise IngestError("catalog must be a JSON list")
    out = {}
    for entry in data:
        if isinstance(entry, dict) and isinstance(entry.get("check_id"), str):
            out[entry["check_id"]] = entry
    return out


def brand_for(site: str, entry: dict) -> str:
    if site in ("toyota", "gbp-toyota"):
        return "toyota"
    if site in ("chevy", "gbp-chevy"):
        return "chevrolet"
    scope = str(entry.get("brand_scope", "")).lower()
    if scope in ("toyota", "chevrolet"):
        return scope
    return "both"


def expected_for(entry: dict) -> str:
    if isinstance(entry.get("expected"), str) and entry["expected"].strip():
        return entry["expected"]
    vt = entry.get("verify_template")
    if isinstance(vt, dict) and str(vt.get("assert", "")).strip():
        return str(vt["assert"])
    return str(entry.get("plain_english") or entry.get("title") or "See the check catalog")


def verify_for(entry: dict, target: str, candidate_verify=None):
    """Rule precedence on creation: the candidate's own rule; else the catalog template with url = target
    (never a manual one); else a manual rule carrying the catalog description."""
    if candidate_verify:
        return dict(candidate_verify)
    vt = entry.get("verify_template")
    if isinstance(vt, dict) and vt.get("type") in register.VERIFY_TYPES and vt.get("type") != "manual" \
            and str(vt.get("assert", "")).strip():
        return {"type": vt["type"], "url": target, "assert": str(vt["assert"])}
    desc = ""
    if isinstance(vt, dict):
        desc = str(vt.get("assert", "")).strip()
    desc = desc or str(entry.get("plain_english") or entry.get("title") or "See the check catalog").strip()
    return {"type": "manual", "url": target, "assert": desc}


# ---------------------------------------------------------------------------
# Block reader
# ---------------------------------------------------------------------------

def extract_block(text: str):
    """Return (items, None, block_date) or (None, reason, None). Exactly one fenced FINDINGS-JSON block is
    required. A line `report_date: YYYY-MM-DD` inside the block gives the report date (block_date, else None)."""
    lines = text.splitlines()
    opens = [i for i, ln in enumerate(lines) if re.match(r"^\s{0,3}```\s*%s\s*$" % BLOCK_LABEL, ln)]
    if not opens:
        return None, "no FINDINGS-JSON block", None
    if len(opens) > 1:
        return None, "more than one FINDINGS-JSON block", None
    start = opens[0] + 1
    end = None
    for j in range(start, len(lines)):
        if re.match(r"^\s{0,3}```\s*$", lines[j]):
            end = j
            break
    if end is None:
        return None, "FINDINGS-JSON block is not closed", None
    body, dates = [], []
    for ln in lines[start:end]:
        m = REPORT_DATE_LINE.match(ln)
        if m:
            dates.append(m.group(1))
        else:
            body.append(ln)
    if len(set(dates)) > 1:
        return None, "FINDINGS-JSON block has two different report_date lines", None
    block_date = dates[0] if dates else None
    if block_date is not None:
        try:
            register.parse_date(block_date)
        except register.RegisterError:
            return None, "report_date is not a real date", None
    try:
        items = json.loads("\n".join(body))
    except ValueError:
        return None, "FINDINGS-JSON block is not valid JSON", None
    if not isinstance(items, list):
        return None, "FINDINGS-JSON block is not a list", None
    clean = []
    for n, item in enumerate(items, 1):
        if not isinstance(item, dict):
            return None, "item %d is not an object" % n, None
        for key in ITEM_KEYS:
            val = item.get(key)
            if not isinstance(val, str) or not val.strip():
                return None, "item %d has no usable %s" % (n, key), None
        if item["site"] not in register.SITES:
            return None, "item %d has an unknown site" % n, None
        clean.append({k: (scrub(item[k].strip())[:MAX_FIELD_CHARS] if k == "observed"
                      else scrub(item[k].strip()) if k == "target" else item[k].strip()) for k in ITEM_KEYS})
    return clean, None, block_date


def read_report(path: str):
    try:
        if os.path.getsize(path) > MAX_REPORT_BYTES:
            return None, "report is larger than %d bytes" % MAX_REPORT_BYTES
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read(), None
    except OSError as exc:
        return None, "cannot read report (%s)" % exc.__class__.__name__


# ---------------------------------------------------------------------------
# Finding candidates (JSON lines written by the three-site watch)
# ---------------------------------------------------------------------------

def read_candidates(path: str):
    """Return (items, None) or (None, reason). One bad line makes the whole file not ingested."""
    text, reason = read_report(path)
    if text is None:
        return None, reason
    items = []
    for n, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        try:
            cand = json.loads(line)
        except ValueError:
            return None, "line %d is not valid JSON" % n
        if not isinstance(cand, dict):
            return None, "line %d is not an object" % n
        for key in ("check_id", "site", "surface", "target", "observed"):
            val = cand.get(key)
            if not isinstance(val, str) or not val.strip():
                return None, "line %d has no usable %s" % (n, key)
        if cand["site"] not in register.SITES:
            return None, "line %d has an unknown site" % n
        for key in ("expected", "source"):
            if cand.get(key) is not None and not isinstance(cand.get(key), str):
                return None, "line %d has a non-text %s" % (n, key)
        verify = cand.get("verify")
        if verify is not None:
            if not isinstance(verify, dict):
                return None, "line %d has a verify that is not an object" % n
            for key in ("type", "url", "assert"):
                if not isinstance(verify.get(key), str) or not verify[key].strip():
                    return None, "line %d has a verify without %s" % (n, key)
            if verify["type"] not in register.VERIFY_TYPES:
                return None, "line %d has a verify with an unknown type" % n
            verify = {k: scrub(verify[k].strip()) for k in ("type", "url", "assert")}
        items.append({"check_id": cand["check_id"].strip(), "site": cand["site"], "surface": cand["surface"].strip(),
                      "target": scrub(cand["target"].strip()),
                      "observed": scrub(cand["observed"].strip(), keep_phones=True)[:MAX_FIELD_CHARS],
                      "expected": scrub((cand.get("expected") or "").strip())[:MAX_FIELD_CHARS],
                      "source": scrub((cand.get("source") or "").strip()), "verify": verify})
    return items, None


# ---------------------------------------------------------------------------
# Seed map (one-time backlog)
# ---------------------------------------------------------------------------

def load_seed_map(path: str, catalog: dict) -> list:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError) as exc:
        raise IngestError("cannot read seed map %s: %s" % (path, exc))
    rules = data.get("rules") if isinstance(data, dict) else None
    if not isinstance(rules, list) or not rules:
        raise IngestError("seed map needs a non-empty 'rules' list")
    out = []
    for n, rule in enumerate(rules, 1):
        if not isinstance(rule, dict):
            raise IngestError("seed rule %d is not an object" % n)
        cid = rule.get("check_id")
        if cid not in catalog:
            raise IngestError("seed rule %d names check_id %r that is not in the catalog" % (n, cid))
        phrases = rule.get("phrases")
        if not isinstance(phrases, list) or not phrases or not all(isinstance(p, str) and p.strip() for p in phrases):
            raise IngestError("seed rule %d needs a list of phrases" % n)
        if rule.get("site") not in register.SITES:
            raise IngestError("seed rule %d needs a valid site" % n)
        if not isinstance(rule.get("target"), str) or not rule["target"].strip():
            raise IngestError("seed rule %d needs a target" % n)
        out.append({"check_id": cid, "site": rule["site"], "target": rule["target"].strip(),
                    "phrases": [p.strip().lower() for p in phrases]})
    return out


def seed_items(text: str, rules: list) -> list:
    low = re.sub(r"\s+", " ", text.lower())
    items = []
    for rule in rules:
        for phrase in rule["phrases"]:
            if re.sub(r"\s+", " ", phrase) in low:
                items.append({"check_id": rule["check_id"], "site": rule["site"], "target": rule["target"],
                              "observed": "Backlog report mentions: %s" % phrase})
                break
    return items


# ---------------------------------------------------------------------------
# Inbox
# ---------------------------------------------------------------------------

def load_inbox(path: str) -> list:
    out = []
    if not os.path.exists(path):
        return out
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                try:
                    out.append(json.loads(line))
                except ValueError:
                    out.append({"unreadable": True})
    return out


def write_inbox(path: str, entries: list) -> None:
    text = "".join(json.dumps(e, ensure_ascii=False, sort_keys=True) + "\n" for e in entries)
    register.atomic_write_text(path, text)


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

def new_counts() -> dict:
    return {"created": 0, "resighted": 0, "reopened": 0, "inbox": 0, "already": 0, "dropped": 0, "not_ingested": None}


def ingest_items(items, report_path, rows, catalog, inbox_state, counts, today, candidate=False, run_seen=None) -> None:
    for item in items:
        entry = catalog.get(item["check_id"])
        if entry is None:
            key = (item["check_id"], item["site"], item["target"])
            if key in inbox_state["seen"]:
                counts["already"] += 1
                continue
            if inbox_state["added"] >= INBOX_CAP:
                counts["dropped"] += 1
                inbox_state["dropped"] += 1
                inbox_state.setdefault("overflow_source", report_path)
                continue
            inbox_state["seen"].add(key)
            inbox_state["added"] += 1
            inbox_state["entries"].append({"check_id": item["check_id"], "site": item["site"],
                                           "target": item["target"], "observed": item["observed"],
                                           "source": scrub(report_path), "report_date": today,
                                           "received": inbox_state["today"]})
            counts["inbox"] += 1
            continue
        add_known(rows, entry, item, item.get("source") or report_path if candidate else report_path, counts, today,
                  candidate=candidate, run_seen=run_seen)


def expected_text(entry, item, candidate) -> str:
    given = (item.get("expected") or "").strip()
    if given:
        return given
    if candidate and str(entry.get("plain_english", "")).strip():
        return str(entry["plain_english"])
    return expected_for(entry)


def add_known(rows, entry, item, source, counts, today, candidate=False, run_seen=None) -> None:
    source = scrub(source)
    surface = str(item.get("surface") or entry.get("surface") or "web")
    fp = register.make_fingerprint(item["site"], surface, item["check_id"], item["target"])
    if candidate:
        # site_watch stamps the same source on every run, so a source test would hide the next run;
        # a finding is counted once per run instead.
        if run_seen is not None:
            if fp in run_seen:
                counts["already"] += 1
                return
            run_seen.add(fp)
    else:
        for row in rows:
            if row.get("fingerprint") == fp and source in row.get("sources", []):
                counts["already"] += 1  # this report already counted for this finding
                return
    _row, outcome = register.add_finding(
        rows, site=item["site"], surface=surface, check_id=item["check_id"], target=item["target"],
        today=today, brand=brand_for(item["site"], entry), tier=entry.get("tier"),
        title=entry.get("title"), observed=item["observed"], expected=expected_text(entry, item, candidate),
        owner=entry.get("owner"), fix_type=entry.get("fix_type"), source=source,
        verify=verify_for(entry, item["target"], item.get("verify")))
    counts[outcome] += 1


def run_ingest(register_path, checks_path, inbox_path, reports, today=None, seed_map=None, out=None,
               candidates=(), expected_sites=None, test_mode=False) -> int:
    out = out or sys.stdout
    refuse_forbidden(list(reports) + list(candidates) + [register_path, checks_path, inbox_path, seed_map])
    if today and not test_mode:
        raise IngestError("refused: --today needs --test-mode; a real run always uses the system date")
    if test_mode and not register.is_test_register(register_path):
        raise IngestError("refused: --test-mode is not allowed for %s; a production-style register is never "
                          "run on a chosen date" % register_path)
    day =register.resolve_today(today).isoformat()
    KNOWN_PHONES.clear()
    KNOWN_PHONES.update(load_known_phones(expected_sites))
    catalog = load_catalog(checks_path)
    catalog_for_over_cap = dict(catalog)
    for cid, entry in LOCAL_CHECKS.items():
        catalog_for_over_cap.setdefault(cid, entry)
    rules = load_seed_map(seed_map, catalog) if seed_map else None

    with register._Locked(register_path):
        rows = register.load_rows(register_path, must_exist=False)
        existing_inbox = load_inbox(inbox_path)
        inbox_state = {"entries": [], "added": 0, "dropped": 0, "today": day,
                       "seen": set((e.get("check_id"), e.get("site"), e.get("target")) for e in existing_inbox)}
        results = []
        for path in reports:
            counts = new_counts()
            text, reason = read_report(path)
            items, rdate = None, None
            if text is not None:
                if rules is not None:
                    items = seed_items(text, rules)
                else:
                    items, reason, rdate = extract_block(text)
            if items is not None:
                if rdate is None:
                    rdate, reason = date_from_name(path)
                if rdate is not None:
                    reason = check_not_future(rdate, day)
                if rdate is None or reason is not None:
                    items = None
            if items is None:
                counts["not_ingested"] = reason
            else:
                ingest_items(items, path, rows, catalog, inbox_state, counts, rdate)
            results.append((path, counts))
        run_seen = set()
        for path in candidates:
            counts = new_counts()
            items, reason = read_candidates(path)
            rdate = None
            if items is not None:
                rdate, reason = date_from_name(path)
                if rdate is not None:
                    reason = check_not_future(rdate, day)
                if rdate is None or reason is not None:
                    items = None
            if items is None:
                counts["not_ingested"] = reason
            else:
                ingest_items(items, path, rows, catalog, inbox_state, counts, rdate, candidate=True, run_seen=run_seen)
            results.append((path, counts))

        if inbox_state["dropped"]:
            over = LOCAL_CHECKS[OVER_CAP_ID] if OVER_CAP_ID not in catalog else catalog[OVER_CAP_ID]
            item = {"check_id": OVER_CAP_ID, "site": "all", "target": "inbox",
                    "observed": "%d unmatched finding(s) arrived in one run; %d kept in the inbox, %d dropped"
                                % (inbox_state["added"] + inbox_state["dropped"], inbox_state["added"],
                                   inbox_state["dropped"])}
            add_known(rows, over, item, inbox_state["overflow_source"], new_counts(), day)

        problems = register.validate_rows(rows)
        if problems:
            for label, problem in problems:
                sys.stderr.write("INVALID %s: %s\n" % (label, problem))
            sys.stderr.write("REFUSED: register would be invalid; nothing written\n")
            return 1
        changed = any(c["not_ingested"] is None for _p, c in results)
        if changed:
            register.save_rows(register_path, rows)
            if inbox_state["entries"]:
                write_inbox(inbox_path, existing_inbox + inbox_state["entries"])

    for path, c in results:
        if c["not_ingested"] is not None:
            out.write("%s: not ingested (%s); nothing changed\n" % (path, c["not_ingested"]))
            continue
        line = "%s: created %d, re-sighted %d, reopened %d, sent to inbox %d, not ingested 0" % (
            path, c["created"], c["resighted"], c["reopened"], c["inbox"])
        extra = []
        if c["already"]:
            extra.append("already counted from this report or run %d" % c["already"])
        if c["dropped"]:
            extra.append("dropped over the inbox cap %d" % c["dropped"])
        out.write(line + (" (" + "; ".join(extra) + ")" if extra else "") + "\n")
    if inbox_state["dropped"]:
        out.write("inbox over cap: %d item(s) dropped; recorded as check %s\n" % (inbox_state["dropped"], OVER_CAP_ID))
    out.write("register valid: %d rows\n" % len(rows))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Read the FINDINGS-JSON block of audit reports into the findings register.")
    p.add_argument("--register", required=True, help="path to register.jsonl")
    p.add_argument("--checks", required=True, help="path to checks.json (the SA-02 catalog)")
    p.add_argument("--inbox", required=True, help="path to inbox.jsonl (unmatched findings, JSON lines)")
    p.add_argument("--report", action="append", nargs="+", default=[], metavar="FILE",
                   help="report file(s); several files after one flag, or repeat the flag")
    p.add_argument("--candidates", action="append", nargs="+", default=[], metavar="FILE",
                   help="finding candidates, JSON lines from site_watch.py; repeat for more")
    p.add_argument("--today", help="YYYY-MM-DD; tests and replays only, needs --test-mode; "
                                   "without it the system date is used")
    p.add_argument("--test-mode", action="store_true",
                   help="allow --today; refused unless the register is a test register (register.is_test_register)")
    p.add_argument("--expected-sites", help="expected-sites.json: phone numbers that may stay in stored text")
    p.add_argument("--seed-map", help="map_rules.json: one-time backlog mode (keyword phrases to check IDs)")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    args.report = [f for group in args.report for f in group]
    args.candidates = [f for group in args.candidates for f in group]
    if not args.report and not args.candidates:
        build_parser().error("give at least one --report or --candidates")
    try:
        return run_ingest(args.register, args.checks, args.inbox, args.report, args.today, args.seed_map,
                          candidates=args.candidates, expected_sites=args.expected_sites,
                          test_mode=args.test_mode)
    except IngestError as exc:
        sys.stderr.write("%s\n" % exc)
        return 1
    except register.RegisterError as exc:
        sys.stderr.write("REFUSED: %s\n" % exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
