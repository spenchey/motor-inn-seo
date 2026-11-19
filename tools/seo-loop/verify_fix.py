#!/usr/bin/env python3
"""SA-06: fix checker.

After a fix request has been sent, read the live public page and decide whether
the problem is really gone. Reads public pages only (GET) and updates the local
register through register.py. Standard library only, Python 3.9.

Each read has one result:
  PASS          the page shows the wanted value
  FAIL          the right page loaded and does not show it
  NOT OBSERVED  we could not tell (timeout, DNS or connection error, 5xx, 401/403/429,
                final address differs from the rule's, page does not prove which page
                it is, host not on the allowlist, rule not testable, rule checked by a person)
A PASS needs proof of identity: the final URL's host and path equal the rule URL's,
and the page names that URL as its canonical (or a title_leads_with literal leads
its title). A NOT OBSERVED read never changes a row's status. The register is not
held while pages are fetched: results are applied afterwards under the register
lock, and only to rows that have not changed since the fetch. Evidence files live
under the register's evidence/ folder and are hashed before the read is recorded.
A sent row with no conclusive result 14 days after it was sent is flagged overdue
(status and approval kept); a conclusive FAIL at 14 days reopens it.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import argparse
import datetime as dt
import html.parser
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request

import register

USER_AGENT = "MotorInnSEOFixChecker/1.0"
ALLOWED_HOSTS = frozenset([
    "www.motorinnautogroup.com",
    "www.motorinntoyotaofcarroll.com",
    "www.motorinnofcarroll.com",
    "ai.motorinnautogroup.com",
    "ai.motorinntoyotaofcarroll.com",
    "ai.motorinnofcarroll.com",
])
TIMEOUT_SECONDS = 20
MIN_GAP_SECONDS = 5
MAX_FETCHES = 40
WAIT_HOURS = 24          # DealerOn caches pages for 6 hours; we wait a full day from the send
OVERDUE_AFTER_DAYS = 14  # a conclusive FAIL reopens the row; no conclusion flags it overdue
EVIDENCE_MAX_BYTES = 2048
CACHE_PARAM = "_cb"
BLOCKED_CODES = (401, 403, 429)
# Meta tag names that carry indexing directives (we only read them).
META_ROBOTS_NAMES = ("robots", "googlebot")

PASS = "PASS"
FAIL = "FAIL"
NOT_OBSERVED = "NOT OBSERVED"

MACHINE_RULES = ("meta_robots", "title_contains", "title_not_contains", "title_leads_with",
                 "html_contains", "html_not_contains", "jsonld_equals", "http_status")
UNOBSERVABLE_RULES = ("gbp_field_equals", "manual")
TEXT_RULES = ("title_contains", "title_not_contains", "title_leads_with", "html_contains", "html_not_contains")
NOT_CONTAINS_RULES = ("title_not_contains", "html_not_contains")
SENTENCE_RE = re.compile(r"\b(no longer|should|must|needs)\b", re.IGNORECASE)
MAX_TEXT_RULE_CHARS = 80
NOT_TESTABLE = "rule is not testable"


class FetchError(Exception):
    """The page could not be read (network problem, bad host, and so on)."""


# ---------------------------------------------------------------------------
# Fetching: one small function that tests replace
# ---------------------------------------------------------------------------

def host_allowed(url: str) -> bool:
    try:
        parts = urllib.parse.urlsplit(url)
    except ValueError:
        return False
    if parts.scheme not in ("http", "https"):
        return False
    host = (parts.hostname or "").lower()
    return host in ALLOWED_HOSTS


def build_url(url: str, now: dt.datetime) -> str:
    """Add a cache-busting query parameter, keeping any existing query."""
    parts = urllib.parse.urlsplit(url)
    query = [(k, v) for k, v in urllib.parse.parse_qsl(parts.query, keep_blank_values=True)
             if k != CACHE_PARAM]
    query.append((CACHE_PARAM, str(int(now.timestamp()))))
    return urllib.parse.urlunsplit((parts.scheme, parts.netloc, parts.path,
                                    urllib.parse.urlencode(query), ""))


class _SameSiteRedirects(urllib.request.HTTPRedirectHandler):
    """Follow redirects only to hosts on the allowlist."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not host_allowed(newurl):
            raise FetchError("redirected to a host outside the allowlist")
        return urllib.request.HTTPRedirectHandler.redirect_request(self, req, fp, code, msg, headers, newurl)


class _NoRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def normalise_headers(headers) -> dict:
    """Header names are case-insensitive: return {lower-case name: [values]}.
    Accepts a dict (values may be a string or a list) or a list of pairs."""
    pairs = headers.items() if isinstance(headers, dict) else (headers or [])
    out = {}
    for name, value in pairs:
        values = value if isinstance(value, (list, tuple)) else [value]
        out.setdefault(str(name).strip().lower(), []).extend(str(v) for v in values)
    return out


def fetch_page(url: str, timeout: int = TIMEOUT_SECONDS, follow_redirects: bool = True):
    """GET `url`. Returns (status_code, body_text, headers, final_url) where
    headers maps lower-cased names to lists of values and final_url is the
    address that answered after any redirects. Raises FetchError on any
    network problem. HTTP error codes are returned, not raised."""
    if not host_allowed(url):
        raise FetchError("host not on the allowlist")
    handler = _SameSiteRedirects() if follow_redirects else _NoRedirects()
    opener = urllib.request.build_opener(handler)
    req = urllib.request.Request(url, method="GET", headers={"User-Agent": USER_AGENT,
                                                             "Accept": "text/html,application/xhtml+xml,*/*;q=0.5"})
    try:
        resp = opener.open(req, timeout=timeout)
        status = resp.getcode()
        final_url = resp.geturl()
        raw = resp.read(3 * 1024 * 1024)
        headers = normalise_headers(resp.headers.items())
    except urllib.error.HTTPError as exc:
        status = exc.code
        # An error answer can come after redirects: report the address that really answered.
        final_url = exc.geturl() or url
        headers = normalise_headers(exc.headers.items() if exc.headers is not None else [])
        try:
            raw = exc.read(3 * 1024 * 1024)
        except Exception:
            raw = b""
    except FetchError:
        raise
    except Exception as exc:  # timeout, DNS, connection reset, bad SSL ...
        raise FetchError("%s: %s" % (type(exc).__name__, exc))
    return status, raw.decode("utf-8", errors="replace"), headers, final_url


def fixture_name(url: str) -> str:
    parts = urllib.parse.urlsplit(url)
    path = parts.path or "/"
    flat = re.sub(r"[^A-Za-z0-9._-]+", "_", path.strip("/")) or "index"
    return "%s__%s.html" % ((parts.hostname or "host").lower(), flat)


def make_fixture_fetcher(directory: str):
    """A fetcher that reads saved pages and opens no connection. A page named
    like fixture_name(url) is status 200; an optional sibling .status file holds
    another code, and an optional <fixture name>.headers.json holds response
    headers (none otherwise). A missing page behaves like a connection error."""
    def _fetch(url: str, timeout: int = TIMEOUT_SECONDS, follow_redirects: bool = True):
        if not host_allowed(url):
            raise FetchError("host not on the allowlist")
        path = os.path.join(directory, fixture_name(url))
        if not os.path.isfile(path):
            raise FetchError("no saved page for %s" % fixture_name(url))
        status = 200
        headers = {}
        sidecar = path[:-5] + ".status"
        if os.path.isfile(sidecar):
            with open(sidecar, "r", encoding="utf-8") as fh:
                status = int(fh.read().strip())
        head_file = path + ".headers.json"
        if os.path.isfile(head_file):
            with open(head_file, "r", encoding="utf-8") as fh:
                headers = normalise_headers(json.load(fh))
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return status, fh.read(), headers, url
    return _fetch


def pause(seconds: float) -> None:
    time.sleep(seconds)


# ---------------------------------------------------------------------------
# Reading a page
# ---------------------------------------------------------------------------

class _PageParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        html.parser.HTMLParser.__init__(self, convert_charrefs=True)
        self.title = None
        self._in_title = False
        self.robots = []          # content of the robots meta tag and the Google-specific one
        self.jsonld = []          # raw text of <script type="application/ld+json">
        self._in_ld = False
        self._ld_buf = []
        self.canonicals = []      # href of every <link rel="canonical">
        self.saw_tag = False

    def handle_starttag(self, tag, attrs):
        self.saw_tag = True
        a = dict((k.lower(), (v or "")) for k, v in attrs)
        if tag == "title" and self.title is None:
            self._in_title = True
            self.title = ""
        elif tag == "meta" and a.get("name", "").strip().lower() in META_ROBOTS_NAMES:
            self.robots.append(a.get("content", ""))
        elif tag == "script" and a.get("type", "").strip().lower() == "application/ld+json":
            self._in_ld = True
            self._ld_buf = []
        elif tag == "link" and "canonical" in a.get("rel", "").lower().split() and a.get("href", "").strip():
            self.canonicals.append(a["href"].strip())

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "script" and self._in_ld:
            self._in_ld = False
            self.jsonld.append("".join(self._ld_buf))

    def handle_data(self, data):
        if self._in_title and self.title is not None:
            self.title += data
        if self._in_ld:
            self._ld_buf.append(data)


def parse_page(body: str):
    """Return a parsed page, or None when the text is not a readable HTML page."""
    if not body or not body.strip() or "<" not in body:
        return None
    parser = _PageParser()
    try:
        parser.feed(body)
        parser.close()
    except Exception:
        return None
    return parser if parser.saw_tag else None


def _host_path(url: str):
    """(host, path) of an address, ignoring scheme, query, fragment and a
    trailing slash. None when it cannot be read."""
    try:
        parts = urllib.parse.urlsplit(url)
    except ValueError:
        return None
    if not parts.hostname:
        return None
    return parts.hostname.lower(), (parts.path or "/").rstrip("/") or "/"


def same_page(a: str, b: str) -> bool:
    ha, hb = _host_path(a or ""), _host_path(b or "")
    return ha is not None and ha == hb


def identity_problem(rule: dict, page, final_url: str) -> str:
    """Why this page does not prove it is the rule's page, or "" when it does:
    its canonical URL equals the rule URL (every canonical tag, at least one),
    or a title_leads_with literal leads its title."""
    ref = rule.get("url") or ""
    if page is None:
        return "page could not be read"
    if page.canonicals and all(same_page(urllib.parse.urljoin(final_url or ref, c), ref)
                               for c in page.canonicals):
        return ""
    if rule.get("type") == "title_leads_with":
        title = re.sub(r"\s+", " ", page.title or "").strip().lower()
        if title.startswith(str(rule.get("assert") or "").strip().lower()):
            return ""
    if page.canonicals:
        return "the page's canonical address is a different page"
    return "the page does not prove which page it is"


_DIRECTIVES = frozenset(("index", "noindex", "follow", "nofollow", "none", "all"))


def _robots_tokens(text: str) -> frozenset:
    tokens = set(t.strip().lower() for t in re.split(r"[,\s]+", text) if t.strip())
    if "none" in tokens:
        tokens.discard("none")
        tokens.update(("noindex", "nofollow"))
    if "all" in tokens:
        tokens.discard("all")
        tokens.update(("index", "follow"))
    return frozenset(tokens)


def _header_tokens(values) -> frozenset:
    """Directives from X-Robots-Tag values. A leading "agent:" prefix is
    dropped and its directives are counted for every agent (the strict reading)."""
    tokens = set()
    for value in values:
        text = value.strip()
        m = re.match(r"^([A-Za-z0-9_-]+)\s*:\s*(.*)$", text)
        if m and m.group(1).lower() not in _DIRECTIVES:
            text = m.group(2)
        for t in re.split(r"[,\s]+", text.lower()):
            if t in _DIRECTIVES:
                tokens.add(t)
    return _robots_tokens(",".join(sorted(tokens)))


def _walk_nodes(data):
    """Yield every dict inside a JSON-LD structure."""
    if isinstance(data, dict):
        yield data
        for value in data.values():
            for sub in _walk_nodes(value):
                yield sub
    elif isinstance(data, list):
        for item in data:
            for sub in _walk_nodes(item):
                yield sub


def _node_types(node: dict) -> list:
    t = node.get("@type")
    if isinstance(t, str):
        return [t]
    if isinstance(t, list):
        return [x for x in t if isinstance(x, str)]
    return []


def _values_at(node, path: list) -> list:
    current = [node]
    for key in path:
        nxt = []
        for item in current:
            if isinstance(item, dict) and key in item:
                val = item[key]
                nxt.extend(val if isinstance(val, list) else [val])
        current = nxt
    return current


def _snippet(text, limit: int = 300) -> str:
    text = re.sub(r"\s+", " ", str(text)).strip()
    return text[:limit]


# ---------------------------------------------------------------------------
# Rules. Each returns (result, matched_text)
# ---------------------------------------------------------------------------

def rule_is_testable(rule: dict, observed=None) -> bool:
    """False when the assert is empty; when a text rule holds a sentence (over
    80 characters, or the words no longer / should / must / needs); or when a
    `*_not_contains` rule's assert does not appear, ignoring case, in the
    finding's `observed` value (a literal we have actually seen on the page)."""
    value = rule.get("assert")
    value = "" if value is None else str(value)
    if not value.strip():
        return False
    rtype = rule.get("type")
    if rtype in TEXT_RULES:
        if len(value) > MAX_TEXT_RULE_CHARS or SENTENCE_RE.search(value):
            return False
    if rtype in NOT_CONTAINS_RULES:
        if observed is None or value.strip().lower() not in str(observed).lower():
            return False
    return True


def evaluate(rule: dict, status: int, body: str, headers=None, url=None, final_url=None, observed=None):
    rtype = rule.get("type")
    expected = rule.get("assert")
    expected = "" if expected is None else str(expected)

    if rtype not in MACHINE_RULES:
        return NOT_OBSERVED, "rule type %r is not checked by this script" % rtype
    if not rule_is_testable(rule, observed):
        return NOT_OBSERVED, NOT_TESTABLE
    if status >= 500:
        return NOT_OBSERVED, "server error %d" % status
    if status in BLOCKED_CODES:
        return NOT_OBSERVED, "blocked or rate limited (status %d)" % status

    # T1: whatever answered must be the rule's own address (host and path).
    ref = rule.get("url") or ""
    if _host_path(ref) is None:
        return NOT_OBSERVED, "the rule has no full address"
    final_url = final_url or ref
    if not same_page(final_url, ref):
        return NOT_OBSERVED, "redirected to a different page (%s)" % ("/".join(_host_path(final_url) or ("?", "?")))

    if rtype == "http_status":
        try:
            want = int(expected.strip())
        except ValueError:
            return NOT_OBSERVED, "rule value is not a status code"
        if want in BLOCKED_CODES:
            return NOT_OBSERVED, "status %d cannot be told from blocking" % want
        if status != 200:
            # No page to read: the address itself answered with this code.
            return (PASS if status == want else FAIL), "status %d" % status
        if want != 200:
            return FAIL, "status 200"
        problem = identity_problem(rule, parse_page(body), final_url)
        if problem:
            return NOT_OBSERVED, problem
        return PASS, "status 200"

    if status in (404, 410):
        return FAIL, "page returned status %d" % status
    if status != 200:
        return NOT_OBSERVED, "status %d" % status
    page = parse_page(body)
    problem = identity_problem(rule, page, final_url)
    if problem:
        return NOT_OBSERVED, problem

    if rtype == "meta_robots":
        want = _robots_tokens(expected)
        if not (want & {"index", "noindex", "follow", "nofollow"}):
            return NOT_OBSERVED, "rule value has no indexing directive"
        actual = frozenset().union(*[_robots_tokens(c) for c in page.robots]) if page.robots else frozenset()
        shown = ("meta " + ", ".join(page.robots)) if page.robots else "meta none (default index,follow)"
        header_values = normalise_headers(headers or {}).get("x-robots-tag", [])
        if header_values:
            actual = actual | _header_tokens(header_values)
            shown += "; X-Robots-Tag " + ", ".join(header_values)
        else:
            shown += "; X-Robots-Tag none"
        # T5: each wanted directive must not be countermanded; other directives are irrelevant.
        ok = True
        for directive, opposite in (("index", "noindex"), ("follow", "nofollow")):
            if directive in want and opposite in actual:
                ok = False
            if opposite in want and opposite not in actual:
                ok = False
        return (PASS if ok else FAIL), "robots: " + shown
    if rtype in ("title_contains", "title_not_contains", "title_leads_with"):
        title = re.sub(r"\s+", " ", page.title or "").strip()
        low, want = title.lower(), expected.strip().lower()
        if rtype == "title_leads_with":
            ok = low.startswith(want)
        elif rtype == "title_contains":
            ok = want in low
        else:
            ok = want not in low
        return (PASS if ok else FAIL), "title: " + title
    if rtype in ("html_contains", "html_not_contains"):
        idx = body.lower().find(expected.lower())
        if rtype == "html_contains":
            if idx < 0:
                return FAIL, "text not found"
            return PASS, body[max(0, idx - 40): idx + len(expected) + 40]
        if idx >= 0:
            return FAIL, body[max(0, idx - 40): idx + len(expected) + 40]
        return PASS, "text not present"
    if rtype == "jsonld_equals":
        return _jsonld_equals(page, expected)
    return NOT_OBSERVED, "unhandled rule"


def _jsonld_equals(page, expected: str):
    """assert form: [Type.]path.to.key=value, for example LocalBusiness.telephone=712-792-5000.
    PASS only when the key has a value and every value found for it matches."""
    if "=" not in expected:
        return NOT_OBSERVED, "rule value must look like Type.key=value"
    left, want = expected.split("=", 1)
    path = [p for p in left.strip().split(".") if p]
    want = want.strip()
    if not path:
        return NOT_OBSERVED, "rule value has no key"
    blocks, bad = [], 0
    for raw in page.jsonld:
        try:
            blocks.append(json.loads(raw))
        except ValueError:
            bad += 1
    if not blocks:
        if bad:
            return NOT_OBSERVED, "structured data could not be parsed"
        return FAIL, "no structured data on the page"
    nodes = [n for b in blocks for n in _walk_nodes(b)]
    typed = [n for n in nodes if path[0] in _node_types(n)]
    if typed and len(path) > 1:
        candidates, key_path = typed, path[1:]
    else:
        candidates, key_path = nodes, path
    seen = []
    for node in candidates:
        for val in _values_at(node, key_path):
            if isinstance(val, (dict, list)):
                continue
            seen.append(str(val).strip())
    if bad:
        return NOT_OBSERVED, "some structured data could not be parsed"
    if seen and all(v == want for v in seen):
        return PASS, "%s=%s" % (".".join(path), want)
    return FAIL, "%s found: %s" % (".".join(path), ", ".join(seen[:5]) if seen else "no value")


# ---------------------------------------------------------------------------
# Evidence
# ---------------------------------------------------------------------------

def _evidence_name(row_id: str, now: dt.datetime, result: str) -> str:
    stamp = now.strftime("%Y%m%dT%H%M%SZ")
    return "%s__%s__%s.json" % (re.sub(r"[^A-Za-z0-9._-]", "_", row_id), stamp,
                                result.lower().replace(" ", "_"))


def write_evidence(base_dir: str, row_id: str, url: str, now: dt.datetime, result: str, matched: str):
    """Save one read's evidence under <register folder>/evidence/. Returns
    (path relative to the register folder, sha256 of the file)."""
    directory = os.path.join(base_dir, register.EVIDENCE_DIR)
    os.makedirs(directory, exist_ok=True)
    matched = _snippet(matched, 600)
    while True:
        doc = {"url": url, "time": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "result": result, "matched": matched}
        text = json.dumps(doc, ensure_ascii=False, indent=1) + "\n"
        if len(text.encode("utf-8")) <= EVIDENCE_MAX_BYTES or not matched:
            break
        matched = matched[: max(0, len(matched) - 100)]
    name = _evidence_name(row_id, now, result)
    path = os.path.join(directory, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return "%s/%s" % (register.EVIDENCE_DIR, name), register.sha256_file(path)


def read_already_taken_today(directory: str, row_id: str, now: dt.datetime) -> bool:
    """True if a PASS or FAIL evidence file for this row is dated today (UTC)."""
    if not directory or not os.path.isdir(directory):
        return False
    prefix = re.sub(r"[^A-Za-z0-9._-]", "_", row_id) + "__" + now.strftime("%Y%m%d")
    for name in os.listdir(directory):
        if name.startswith(prefix) and (name.endswith("__pass.json") or name.endswith("__fail.json")):
            return True
    return False


# ---------------------------------------------------------------------------
# The run
# ---------------------------------------------------------------------------

def _iso(now: dt.datetime) -> str:
    return now.strftime("%Y-%m-%dT%H:%M:%SZ")


def _pass_on_day(row: dict, day: dt.date) -> bool:
    try:
        return any(t.astimezone(dt.timezone.utc).date() == day for t in register.passing_times(row.get("verified")))
    except register.RegisterError:
        return False


def unreadable_reason(rule: dict, observed) -> str:
    """Why this rule can never be machine-checked, or "" when it can."""
    rtype = rule.get("type")
    if rtype in UNOBSERVABLE_RULES or rtype not in MACHINE_RULES:
        return "rule type %s is checked by a person" % rtype
    if not host_allowed(rule.get("url") or ""):
        return "the address is not a full address on an allowed host"
    if not rule_is_testable(rule, observed):
        return NOT_TESTABLE
    return ""


_MONTHS = ("January", "February", "March", "April", "May", "June", "July", "August", "September",
           "October", "November", "December")


def _plain_date(sent_at) -> str:
    """'2026-11-10' becomes 'November 10'."""
    try:
        day = register.parse_date(str(sent_at)[:10], "sent date")
        return "%s %d" % (_MONTHS[day.month - 1], day.day)
    except register.RegisterError:
        return "an earlier date"


def _overdue_text(sent_at, reason: str = "") -> str:
    """One fixed plain sentence for the register's next action. The read reason
    (which can hold file names, URLs or codes) stays in the run output only."""
    return ("A person needs to check this fix on the live page; it was sent on %s and could not be "
            "confirmed automatically." % _plain_date(sent_at))


def _reopen_text(row: dict, sent_at: str):
    """Next action naming the date the request was sent. A second failed attempt
    lands in blocked, so the text asks Spencer in that case."""
    fails = int(row.get("failed_fix_attempts", 0)) + 1
    if fails >= register.FAIL_TWICE_LIMIT:
        return "spencer", ("Spencer decision: the fix requested on %s did not hold, second failed attempt" % sent_at)
    return "rory", ("Fix requested on %s did not hold after 14 days; ask again and quote that date" % sent_at)


def check_rows(rows: list, evidence_dir: str, now: dt.datetime, dry_run: bool = False, fetcher=None,
               use_pause: bool = True, out=None, register_path=None):
    """Check every sent / verify_pending row once. Returns (counts, changed).

    Pages are fetched first, without holding the register. With `register_path`
    the results are then applied under the register lock to a freshly loaded
    copy and saved there; otherwise they are applied to `rows`, which the
    caller saves. A result is applied only if the row's status and sent.sent_at
    are unchanged since the fetch. Evidence goes under the register's folder
    (the folder of `register_path`, else the parent of `evidence_dir`)."""
    out = out or sys.stdout
    fetch = fetcher if fetcher is not None else fetch_page
    base_dir = os.path.dirname(os.path.abspath(register_path if register_path else evidence_dir))
    evidence_dir = os.path.join(base_dir, register.EVIDENCE_DIR)
    counts = {"rows": 0, "pass": 0, "fail": 0, "not_observed": 0, "skipped": 0,
              "verified_fixed": 0, "reopened": 0, "overdue": 0, "fetches": 0}
    today = now.date()
    fetched_any = False
    work = []   # one dict per row that needs an action after the fetch phase

    def say(row_id, text):
        out.write("%s: %s\n" % (row_id, text))

    for row in rows:
        if row.get("status") not in ("sent", "verify_pending"):
            continue
        counts["rows"] += 1
        rid = row["id"]
        sent = row.get("sent")
        rule = row.get("verify")
        if not isinstance(sent, dict) or not isinstance(rule, dict):
            counts["skipped"] += 1
            say(rid, "skipped, row has no sent date or verify rule")
            continue
        try:
            sent_time = register.sent_moment(sent)
        except register.RegisterError as exc:
            counts["skipped"] += 1
            say(rid, "skipped, %s" % exc)
            continue
        eligible_at = sent_time + dt.timedelta(hours=WAIT_HOURS)
        if now < eligible_at:
            counts["skipped"] += 1
            say(rid, "skipped, too early (first read after %s)" % _iso(eligible_at))
            continue
        item = {"id": rid, "status": row["status"], "sent_at": sent.get("sent_at"), "sent_time": sent_time,
                "rule": rule, "observed": row.get("observed"), "kind": None}
        reason = unreadable_reason(rule, row.get("observed"))
        if reason:
            if now - sent_time >= dt.timedelta(days=OVERDUE_AFTER_DAYS):
                item["kind"], item["reason"] = "chase", reason
                work.append(item)
            else:
                counts["not_observed"] += 1
                say(rid, "NOT OBSERVED (%s), no status change" % reason)
            continue
        if _pass_on_day(row, today) or read_already_taken_today(evidence_dir, rid, now):
            counts["skipped"] += 1
            say(rid, "skipped, already read today")
            continue
        if counts["fetches"] >= MAX_FETCHES:
            counts["skipped"] += 1
            say(rid, "skipped, %d fetches already made this run" % MAX_FETCHES)
            continue
        url = build_url(rule["url"], now)
        if dry_run:
            counts["skipped"] += 1
            say(rid, "would read %s (rule %s)" % (url, rule.get("type")))
            continue

        if fetched_any and use_pause:
            pause(MIN_GAP_SECONDS)
        fetched_any = True
        counts["fetches"] += 1
        follow = not (rule.get("type") == "http_status" and str(rule.get("assert", "")).strip()[:1] == "3")
        try:
            got = fetch(url, TIMEOUT_SECONDS, follow)
            status, body = got[0], got[1]
            headers = got[2] if len(got) > 2 else {}
            final_url = got[3] if len(got) > 3 and got[3] else url
            result, matched = evaluate(rule, status, body, headers, url=url, final_url=final_url,
                                       observed=row.get("observed"))
        except Exception as exc:  # any failure to read is "not observed"
            result, matched = NOT_OBSERVED, "could not read the page: %s" % _snippet(exc, 120)
        item.update(kind="read", url=url, result=result, matched=matched)
        work.append(item)

    if dry_run or not work:
        return counts, False

    def apply(target_rows):
        changed = False
        for item in work:
            rid = item["id"]
            try:
                row = register.find_row(target_rows, rid)
            except register.RegisterError:
                row = None
            cur_sent = (row or {}).get("sent") or {}
            if (row is None or row.get("status") != item["status"]
                    or cur_sent.get("sent_at") != item["sent_at"]):
                counts["skipped"] += 1
                say(rid, "skipped, the row changed while pages were being read; result not applied")
                continue
            age = now - item["sent_time"]

            def raise_overdue(reason):
                """T4: flag, keeping status and approval. Returns True if the row changed."""
                if row.get("overdue_since"):
                    say(rid, "NOT OBSERVED (%s), already flagged overdue" % reason)
                    return False
                try:
                    register.flag_overdue(target_rows, rid, _overdue_text(cur_sent.get("at"), reason),
                                          "coordinator", now=_iso(now))
                except register.RegisterError as exc:
                    say(rid, "could not flag overdue: %s" % exc)
                    return False
                counts["overdue"] += 1
                say(rid, "NOT OBSERVED (%s), no conclusive result %d days after the request, flagged overdue "
                    "(status stays %s)" % (reason, age.days, row["status"]))
                return True

            if item["kind"] == "chase":
                counts["not_observed"] += 1
                if raise_overdue(item["reason"]):
                    changed = True
                continue
            result, matched, url = item["result"], item["matched"], item["url"]
            if result == NOT_OBSERVED:
                counts["not_observed"] += 1
                if age >= dt.timedelta(days=OVERDUE_AFTER_DAYS):
                    if raise_overdue(matched):
                        changed = True
                else:
                    say(rid, "NOT OBSERVED (%s), no status change" % matched)
                continue
            evidence, evidence_sha = write_evidence(base_dir, rid, url, now, result, matched)
            if result == FAIL:
                counts["fail"] += 1
                # A failed read breaks the run of passes: two passes must be consecutive.
                register.clear_reads(target_rows, rid)
                changed = True
                if age >= dt.timedelta(days=OVERDUE_AFTER_DAYS):
                    owner, action = _reopen_text(row, cur_sent.get("at"))
                    try:
                        register.transition(target_rows, rid, "reopened", today=today.isoformat(),
                                            now=_iso(now), next_action=action, next_action_owner=owner)
                        counts["reopened"] += 1
                        say(rid, "FAIL, still not fixed %d days after the request, row is now %s"
                            % (age.days, row["status"]))
                    except register.RegisterError as exc:
                        say(rid, "FAIL, could not reopen: %s" % exc)
                else:
                    say(rid, "FAIL at day %d (%s), earlier good reads cleared, logged only"
                        % (age.days, matched[:80]))
                continue
            counts["pass"] += 1
            try:
                if row["status"] == "sent":
                    register.transition(target_rows, rid, "verify_pending", today=today.isoformat(), now=_iso(now))
                register.record_read(target_rows, rid, _iso(now), evidence_path=evidence,
                                     evidence_sha256=evidence_sha, now=_iso(now), base_dir=base_dir)
                changed = True
            except register.RegisterError as exc:
                say(rid, "PASS but the register refused: %s" % exc)
                continue
            note = "PASS, one good read recorded"
            try:
                register.transition(target_rows, rid, "verified_fixed", today=today.isoformat(), now=_iso(now))
                counts["verified_fixed"] += 1
                note = "PASS, second good read 24 hours later, row is now verified_fixed"
            except register.RegisterError:
                pass
            say(rid, note)
        return changed

    if register_path is None:
        return counts, apply(rows)
    with register._Locked(register_path):
        fresh = register.load_rows(register_path)
        changed = apply(fresh)
        if changed:
            register.save_rows(register_path, fresh)
    return counts, changed


def totals_line(counts: dict, dry_run: bool) -> str:
    return ("TOTALS%s rows=%d pass=%d fail=%d not_observed=%d skipped=%d verified_fixed=%d reopened=%d "
            "overdue=%d fetches=%d"
            % (" (dry run)" if dry_run else "", counts["rows"], counts["pass"], counts["fail"],
               counts["not_observed"], counts["skipped"], counts["verified_fixed"], counts["reopened"],
               counts["overdue"], counts["fetches"]))


def test_mode_problem(args) -> str:
    """Why this combination of options is refused, or "" when it is allowed."""
    if (args.fixtures or args.now) and not args.test_mode:
        return "--fixtures and --now are for tests and need --test-mode"
    if args.test_mode and not register.is_test_register(args.register):
        return "--test-mode is refused on a production-style register"
    if args.evidence_dir:
        want = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(args.register)), register.EVIDENCE_DIR))
        if os.path.realpath(args.evidence_dir) != want:
            return "--evidence-dir must be the register's own %s/ folder" % register.EVIDENCE_DIR
    return ""


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Check live public pages and decide whether requested fixes worked.")
    p.add_argument("--register", required=True, help="path to register.jsonl")
    p.add_argument("--evidence-dir", default=None,
                   help="optional; if given it must be the evidence/ folder beside the register")
    p.add_argument("--now", default=None, help="ISO-8601 time to use instead of the clock (needs --test-mode)")
    p.add_argument("--dry-run", action="store_true", help="print what would happen; write and fetch nothing")
    p.add_argument("--fixtures", default=None, help="read saved pages from this folder (needs --test-mode)")
    p.add_argument("--test-mode", action="store_true",
                   help="allow --fixtures and --now; refused on a production-looking register")
    return p


def main(argv=None, fetcher=None, out=None) -> int:
    args = build_parser().parse_args(argv)
    out = out or sys.stdout
    problem = test_mode_problem(args)
    if problem:
        sys.stderr.write("refused: %s\n" % problem)
        return 1
    try:
        now = (register.parse_timestamp(args.now, "--now") if args.now
               else dt.datetime.now(dt.timezone.utc)).astimezone(dt.timezone.utc)
        rows = register.load_rows(args.register)
    except register.RegisterError as exc:
        sys.stderr.write("refused: %s\n" % exc)
        return 1
    use_pause = True
    if fetcher is None and args.fixtures:
        fetcher = make_fixture_fetcher(args.fixtures)
        use_pause = False
    try:
        counts, _changed = check_rows(rows, args.evidence_dir, now, dry_run=args.dry_run, fetcher=fetcher,
                                      use_pause=use_pause, out=out, register_path=args.register)
    except register.RegisterError as exc:
        sys.stderr.write("refused: %s\n" % exc)
        return 1
    out.write(totals_line(counts, args.dry_run) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
