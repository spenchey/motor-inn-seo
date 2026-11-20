#!/usr/bin/env python3
"""Three-site watch for Motor Inn (SA-03).

Reads a small set of public pages on the group, Toyota and Chevrolet sites with
read-only GET requests and writes SEO problems as finding candidates, one JSON
object per line. A page that could not be read is reported in the run summary
as not observed and produces no finding.

Finding candidate: {check_id, site, surface, target, observed, expected, source[, verify]}
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from typing import Any, Callable, Dict, List, Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

USER_AGENT = "MotorInnSEOSiteWatch/1.0"
MIN_DELAY_SECONDS = 5.0
TIMEOUT_SECONDS = 20
MAX_BODY_BYTES = 2_000_000
MAX_REDIRECTS = 3
SOURCE = "site_watch.py"
HERE = os.path.dirname(os.path.abspath(__file__))

# BEGIN ROBOTS BOT LIST (group names the robots.txt parser looks up)
NAMED_BOTS = (
    "GPTBot",
    "ClaudeBot",
    "OAI-SearchBot",
    "ChatGPT-User",
    "Claude-SearchBot",
    "PerplexityBot",
    "Googlebot",
    "Bingbot",
)
# END ROBOTS BOT LIST

BUSINESS_TYPES = {
    "automotivebusiness", "autodealer", "autorepair", "autobodyshop",
    "localbusiness", "organization", "cardealer",
}
BLOCKED_STATUSES_NOT_OBSERVED = (403, 429)  # bot protection or rate limit: not a verdict

FetchFn = Callable[[str], Dict[str, Any]]


# ---------------------------------------------------------------- fetching

def host_of(url: str) -> str:
    return (urllib.parse.urlsplit(url).hostname or "").lower()


def build_request(url: str) -> urllib.request.Request:
    """The only place a request is built. Plain GET, honest User-Agent."""
    return urllib.request.Request(
        url, method="GET",
        headers={"User-Agent": USER_AGENT, "Accept": "text/html,text/plain,application/xml;q=0.9,*/*;q=0.5"})


class _AllowlistRedirect(urllib.request.HTTPRedirectHandler):
    def __init__(self, allowed_hosts, limit=MAX_REDIRECTS):
        self.allowed_hosts = set(allowed_hosts)
        self.limit = limit
        self.count = 0

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.count += 1
        if self.count > self.limit:
            raise urllib.error.URLError("too many redirects")
        if host_of(newurl) not in self.allowed_hosts:
            raise urllib.error.URLError("redirect to a host outside the allowlist")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


class LiveFetcher:
    """Rate-limited GET fetcher. Tests replace the whole fetch function instead."""

    def __init__(self, allowed_hosts, min_delay=MIN_DELAY_SECONDS, timeout=TIMEOUT_SECONDS,
                 clock=time.monotonic, sleep=time.sleep, opener_factory=None):
        self.allowed_hosts = set(allowed_hosts)
        self.min_delay = max(float(min_delay), MIN_DELAY_SECONDS)
        self.timeout = timeout
        self.clock = clock
        self.sleep = sleep
        self.opener_factory = opener_factory
        self._last: Optional[float] = None

    def _wait(self) -> None:
        if self._last is not None:
            gap = self.clock() - self._last
            if gap < self.min_delay:
                self.sleep(self.min_delay - gap)
        self._last = self.clock()

    def __call__(self, url: str) -> Dict[str, Any]:
        if host_of(url) not in self.allowed_hosts:
            return _result(url, error="host not on the allowlist; not requested")
        self._wait()
        req = build_request(url)
        if self.opener_factory:
            opener = self.opener_factory(req)
        else:
            opener = urllib.request.build_opener(_AllowlistRedirect(self.allowed_hosts))
        try:
            resp = opener.open(req, timeout=self.timeout)
            return _from_response(url, resp, resp.getcode())
        except urllib.error.HTTPError as exc:
            return _from_response(url, exc, exc.code)
        except Exception as exc:  # timeout, DNS, refused, TLS, redirect refusal
            return _result(url, error="%s: %s" % (type(exc).__name__, exc))
        finally:
            self._last = self.clock()


def _from_response(url, resp, status):
    try:
        raw = resp.read(MAX_BODY_BYTES)
    except Exception as exc:
        return _result(url, error="%s: %s" % (type(exc).__name__, exc))
    headers = {k.lower(): v for k, v in resp.headers.items()} if resp.headers else {}
    final = getattr(resp, "url", None) or getattr(resp, "geturl", lambda: url)()
    return _result(url, status=status, headers=headers, body=raw.decode("utf-8", "replace"), final_url=final)


def _result(url, status=None, headers=None, body="", final_url=None, error=None):
    return {"url": url, "final_url": final_url or url, "status": status,
            "headers": headers or {}, "body": body, "error": error}


def fixture_fetcher(fixtures_dir: str) -> FetchFn:
    """No network. fixtures_dir/index.json maps url -> {status, headers, file | error}."""
    with open(os.path.join(fixtures_dir, "index.json"), encoding="utf-8") as fh:
        index = json.load(fh)

    def fetch(url: str) -> Dict[str, Any]:
        entry = index.get(url)
        if entry is None:
            return _result(url, error="no fixture for this address")
        if entry.get("error"):
            return _result(url, error=entry["error"])
        body = ""
        if entry.get("file"):
            with open(os.path.join(fixtures_dir, entry["file"]), encoding="utf-8") as fh:
                body = fh.read()
        return _result(url, status=int(entry.get("status", 200)),
                       headers={k.lower(): v for k, v in entry.get("headers", {}).items()},
                       body=body, final_url=entry.get("final_url"))
    return fetch


# ---------------------------------------------------------------- html parsing

class PageParser(HTMLParser):
    SKIP = {"script", "style", "noscript", "template", "head", "title"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title_parts: List[str] = []
        self.robots_meta: List[str] = []
        self.canonicals: List[str] = []
        self.h1s: List[str] = []
        self.jsonld: List[str] = []
        self.itemtypes: List[str] = []
        self.text_parts: List[str] = []
        self._in_title = False
        self._title_done = False
        self._in_h1 = False
        self._h1_buf: List[str] = []
        self._in_jsonld = False
        self._jsonld_buf: List[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "title" and not self._title_done:
            self._in_title = True
        elif tag == "meta" and a.get("name", "").lower() == "robots":
            self.robots_meta.append(a.get("content", ""))
        elif tag == "link" and "canonical" in a.get("rel", "").lower().split():
            self.canonicals.append(a.get("href", ""))
        elif tag == "h1":
            self._in_h1, self._h1_buf = True, []
        elif tag == "script" and a.get("type", "").lower().split(";")[0].strip() == "application/ld+json":
            self._in_jsonld, self._jsonld_buf = True, []
        if a.get("itemtype"):
            self.itemtypes.append(a["itemtype"])
        if tag == "body":
            self._skip_depth = 0  # a missing </head> must not hide the page text
        if tag in self.SKIP and tag not in ("title", "head"):
            self._skip_depth += 1
        elif tag == "head":
            self._skip_depth += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
            self._title_done = True
        elif tag == "h1" and self._in_h1:
            self._in_h1 = False
            self.h1s.append(" ".join("".join(self._h1_buf).split()))
        elif tag == "script" and self._in_jsonld:
            self._in_jsonld = False
            self.jsonld.append("".join(self._jsonld_buf))
        if tag in self.SKIP and tag not in ("title",) and self._skip_depth > 0:
            self._skip_depth -= 1

    def handle_data(self, data):
        if self._in_title:
            self.title_parts.append(data)
        if self._in_jsonld:
            self._jsonld_buf.append(data)
        if self._in_h1:
            self._h1_buf.append(data)
        if self._skip_depth == 0:
            self.text_parts.append(data)


def parse_page(html: str) -> Dict[str, Any]:
    p = PageParser()
    try:
        p.feed(html)
        p.close()
    except Exception:
        pass
    nodes: List[dict] = []
    invalid = 0
    for blob in p.jsonld:
        try:
            _walk(json.loads(blob.strip()), nodes)
        except ValueError:
            invalid += 1
    return {
        "title": " ".join("".join(p.title_parts).split()),
        "robots_meta": [m.strip() for m in p.robots_meta],
        "canonicals": [c.strip() for c in p.canonicals],
        "h1s": p.h1s,
        "nodes": nodes,
        "invalid_jsonld": invalid,
        "itemtypes": p.itemtypes,
        "text": " ".join(" ".join(p.text_parts).split()),
    }


def _walk(obj, out):
    if isinstance(obj, list):
        for x in obj:
            _walk(x, out)
    elif isinstance(obj, dict):
        if "@type" in obj:
            out.append(obj)
        for v in obj.values():
            if isinstance(v, (dict, list)):
                _walk(v, out)


def _types(node) -> List[str]:
    t = node.get("@type")
    if isinstance(t, str):
        return [t]
    return [x for x in t if isinstance(x, str)] if isinstance(t, list) else []


PHONE_RE = re.compile(r"(?<![\d])(?:\+?1[\s.\-]?)?\(?([2-9]\d{2})\)?[\s.\-]\s?([2-9]\d{2})[\s.\-]([0-9]{4})(?![\d])")


def norm_phone(raw: str) -> str:
    digits = re.sub(r"\D", "", raw or "")
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    if len(digits) == 10:
        return "%s-%s-%s" % (digits[:3], digits[3:6], digits[6:])
    return (raw or "").strip()


def phones_in_text(text: str) -> List[str]:
    seen: List[str] = []
    for m in PHONE_RE.finditer(text):
        n = "%s-%s-%s" % m.groups()
        if n not in seen:
            seen.append(n)
    return seen


def norm_url(u: str) -> str:
    s = urllib.parse.urlsplit(u.strip())
    path = s.path.rstrip("/") or ""
    return "%s%s" % ((s.hostname or "").lower(), path.lower())


# ---------------------------------------------------------------- robots.txt

def parse_robots(text: str) -> Dict[str, Any]:
    groups: List[Dict[str, Any]] = []
    sitemaps: List[str] = []
    cur: Optional[Dict[str, Any]] = None
    last_was_agent = False
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key, val = key.strip().lower(), val.strip()
        if key == "user-agent":
            if cur is None or not last_was_agent:
                cur = {"agents": [], "rules": []}
                groups.append(cur)
            cur["agents"].append(val.lower())
            last_was_agent = True
            continue
        last_was_agent = False
        if key == "sitemap":
            sitemaps.append(val)
        elif key in ("allow", "disallow") and cur is not None:
            cur["rules"].append((key == "allow", val))
    return {"groups": groups, "sitemaps": sitemaps}


def bot_blocked(parsed: Dict[str, Any], bot: str) -> bool:
    """True when the group that applies to this bot disallows the whole site."""
    named = [g for g in parsed["groups"] if bot.lower() in g["agents"]]
    groups = named or [g for g in parsed["groups"] if "*" in g["agents"]]
    rules = [r for g in groups for r in g["rules"]]
    disallow_all = any((not allow) and path in ("/", "/*") for allow, path in rules)
    allow_all = any(allow and path in ("/", "/*") for allow, path in rules)
    return disallow_all and not allow_all


# ---------------------------------------------------------------- config

def load_json(path: str):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def allowed_hosts_from(expected: dict) -> Dict[str, str]:
    """host -> site key, from the three base URLs in expected-sites.json."""
    return {host_of(cfg["base_url"]): key for key, cfg in expected["sites"].items()}


def validate_urls(urls_cfg: dict, expected: dict) -> List[str]:
    problems: List[str] = []
    hosts = allowed_hosts_from(expected)
    if len(hosts) != 3:
        problems.append("expected-sites.json must name exactly 3 hosts")
    limit = int(urls_cfg.get("max_urls_per_host", 12))
    if limit > 12:
        problems.append("max_urls_per_host above 12")
    if set(urls_cfg.get("hosts", {})) != set(expected["sites"]):
        problems.append("urls.json hosts differ from expected-sites.json sites")
    for site, block in urls_cfg.get("hosts", {}).items():
        if site not in expected["sites"]:
            continue
        keys = {k["id"]: k for k in expected["sites"][site]["key_urls"]}
        entries = block.get("urls", [])
        if len(entries) > min(limit, 12):
            problems.append("%s: %d URLs, more than %d" % (site, len(entries), min(limit, 12)))
        if sum(1 for e in entries if e.get("tripwire")) != 3:
            problems.append("%s: tripwire set is not exactly 3" % site)
        if block.get("host") not in hosts or hosts.get(block.get("host")) != site:
            problems.append("%s: host not on the allowlist" % site)
        for e in entries:
            k = keys.get(e.get("id"))
            if k is None:
                problems.append("%s/%s: id is not in expected-sites key_urls" % (site, e.get("id")))
                continue
            if e.get("url") != k["url"]:
                problems.append("%s/%s: url differs from expected-sites" % (site, e["id"]))
            if bool(e.get("needs_confirmation")) != bool(k.get("needs_confirmation")):
                problems.append("%s/%s: needs_confirmation differs from expected-sites" % (site, e["id"]))
            if host_of(e.get("url", "")) not in hosts:
                problems.append("%s/%s: host not on the allowlist" % (site, e["id"]))
            if e.get("kind") not in ("page", "robots", "llms", "sitemap"):
                problems.append("%s/%s: unknown kind" % (site, e["id"]))
        ids = [e.get("id") for e in entries]
        if len(ids) != len(set(ids)):
            problems.append("%s: duplicate ids" % site)
        for tid in expected["sites"][site].get("tripwire", []):
            ent = next((e for e in entries if e.get("id") == tid), None)
            if ent is None or not ent.get("tripwire"):
                problems.append("%s: tripwire differs from expected-sites (%s)" % (site, tid))
    return problems


def list_urls(urls_cfg: dict) -> Dict[str, Any]:
    out: Dict[str, Any] = {"hosts": {}}
    for site, block in urls_cfg["hosts"].items():
        out["hosts"][site] = {
            "host": block["host"],
            "url_count": len(block["urls"]),
            "tripwire_count": sum(1 for e in block["urls"] if e["tripwire"]),
            "urls": [{"id": e["id"], "url": e["url"], "kind": e["kind"], "tripwire": e["tripwire"],
                      "needs_confirmation": e["needs_confirmation"]} for e in block["urls"]],
        }
    out["host_count"] = len(out["hosts"])
    return out


# ---------------------------------------------------------------- analysis

class Collector:
    def __init__(self, catalog_ids):
        self.catalog_ids = set(catalog_ids)
        self.findings: List[Dict[str, str]] = []
        self._seen = set()

    def add(self, check_id, site, target, observed, expected, verify=None):
        if check_id not in self.catalog_ids:
            raise ValueError("check_id not in checks.json: %s" % check_id)
        key = (check_id, site, target)
        if key in self._seen:
            return
        self._seen.add(key)
        row = {"check_id": check_id, "site": site, "surface": "web", "target": target,
               "observed": observed, "expected": expected, "source": SOURCE}
        if verify:
            row["verify"] = verify
        self.findings.append(row)


def all_pending_phones(expected: dict) -> Dict[str, str]:
    """Every number awaiting a ruling on any site or listing; applies to all three sites."""
    out: Dict[str, str] = {}
    blocks = list(expected.get("sites", {}).values()) + list(expected.get("listings", {}).values())
    for blk in blocks:
        for p in blk.get("observed_phones", []):
            if p.get("review_state") == "pending-spencer":
                out[norm_phone(p["number"])] = p["review_state"]
    return out


def _known_phones(site_cfg: dict, pending_all: Optional[Dict[str, str]] = None) -> Tuple[str, Dict[str, str]]:
    main = norm_phone(site_cfg.get("approved_main_phone", ""))
    pending = dict(pending_all or {})
    for p in site_cfg.get("observed_phones", []):
        if p.get("review_state") == "pending-spencer":
            pending[norm_phone(p["number"])] = p["review_state"]
    return main, pending


def analyze_page(col: Collector, site: str, site_cfg: dict, url: str, final_url: str,
                 headers: Dict[str, str], html: str, faq_expected: bool, summary: Dict[str, Any],
                 pending_all: Optional[Dict[str, str]] = None) -> None:
    page = parse_page(html)
    main_phone, pending = _known_phones(site_cfg, pending_all)
    title = page["title"]

    # noindex: robots meta tag or X-Robots-Tag header
    bits = []
    for m in page["robots_meta"]:
        if "noindex" in m.lower():
            bits.append('robots meta tag: "%s"' % m)
    xrt = headers.get("x-robots-tag", "")
    if "noindex" in xrt.lower():
        bits.append('X-Robots-Tag header: "%s"' % xrt)
    if bits:
        col.add("meta-noindex", site, url, "; ".join(bits),
                "index,follow: no noindex in the robots meta tag or the X-Robots-Tag header",
                verify={"type": "meta_robots", "url": url, "assert": "index,follow"})

    # placeholder page
    canon_path = urllib.parse.urlsplit(page["canonicals"][0]).path.lower() if page["canonicals"] else ""
    if "platformpage" in title.lower() or canon_path.endswith("/platformpage.aspx"):
        col.add("placeholder-page-indexed", site, url,
                'Title "%s"; canonical "%s"' % (title, page["canonicals"][0] if page["canonicals"] else "none"),
                "A real page at this address, not the platform placeholder")

    # title leads with another town
    rule = site_cfg.get("title_rule", {})
    for town in rule.get("must_not_lead_with", []):
        if title.lower().startswith(town.lower()):
            col.add("title-leads-other-city", site, url, 'Title: "%s"' % title,
                    "Page title leads with Carroll, Iowa",
                    verify={"type": "title_not_contains", "url": url, "assert": title[:len(town)]})
            break

    # canonical
    if not page["canonicals"]:
        col.add("canonical-wrong", site, url, "No canonical tag on the page",
                "The page's own address (%s) named as its preferred address" % final_url)
    else:
        c = page["canonicals"][0]
        abs_c = urllib.parse.urljoin(final_url, c)
        if norm_url(abs_c) != norm_url(final_url):
            other = host_of(abs_c) != host_of(final_url)
            col.add("canonical-wrong", site, url,
                    'Canonical points at "%s"%s' % (abs_c, " (a different host)" if other else ""),
                    "The page's own address (%s) as its preferred address" % final_url)

    # JSON-LD
    biz = [n for n in page["nodes"] if any(t.lower() in BUSINESS_TYPES for t in _types(n))]
    # Department entries ("Sales", "Service", "Parts") are nested under a business node's
    # "department" key. They are not the business name, so the name check skips them.
    # The phone check below still reads every business node, departments included.
    dept_ids = set()
    for n in page["nodes"]:
        d = n.get("department")
        for x in (d if isinstance(d, list) else [d]):
            if isinstance(x, dict):
                dept_ids.add(id(x))
    named_biz = [n for n in biz if id(n) not in dept_ids]
    exp_name = site_cfg.get("schema_name", {}).get("expected")
    if exp_name:
        bad = sorted({str(n["name"]).strip() for n in named_biz
                      if isinstance(n.get("name"), str) and n["name"].strip().casefold() != exp_name.casefold()})
        if bad:
            col.add("schema-name-mismatch", site, url,
                    "Business name in page markup: %s" % ", ".join('"%s"' % b for b in bad),
                    'Business name in page markup is "%s"' % exp_name)
    sch_phones: List[str] = []
    for n in page["nodes"]:
        if n in biz or "contactpoint" in [t.lower() for t in _types(n)]:
            tel = n.get("telephone")
            for t in (tel if isinstance(tel, list) else [tel]):
                if isinstance(t, str) and t.strip() and norm_phone(t) not in sch_phones:
                    sch_phones.append(norm_phone(t))
    for ph in sch_phones:
        if ph in pending:
            summary["pending_phones_seen"].append({"site": site, "url": url, "number": ph, "where": "page markup"})
    odd = [p for p in sch_phones if p != main_phone and p not in pending]
    if odd:
        col.add("schema-phone-mismatch", site, url,
                "Phone in page markup: %s" % ", ".join(odd),
                "Phone in page markup is %s" % main_phone)

    # FAQ
    has_faq = any("faqpage" in [t.lower() for t in _types(n)] for n in page["nodes"]) or \
        any("faqpage" in it.lower() for it in page["itemtypes"])
    if faq_expected and not has_faq:
        col.add("faq-schema-missing", site, url, "No FAQPage markup found on the page",
                "FAQPage markup (question and answer) on the page")

    # phones in visible text
    seen = phones_in_text(page["text"])
    for ph in seen:
        if ph in pending:
            summary["pending_phones_seen"].append({"site": site, "url": url, "number": ph, "where": "page text"})
    odd_text = [p for p in seen if p != main_phone and p not in pending]
    if odd_text:
        col.add("unexpected-phone-on-page", site, url,
                "Numbers on the page that are not on the reviewed list: %s" % ", ".join(odd_text),
                "Page shows the main number %s" % main_phone)

    summary["page_observations"].append({
        "site": site, "url": url, "title": title, "robots_meta": page["robots_meta"],
        "x_robots_tag": xrt, "canonical": page["canonicals"][0] if page["canonicals"] else None,
        "h1_count": len(page["h1s"]), "h1": page["h1s"][:3], "has_faq_markup": has_faq,
        "schema_phones": sch_phones, "text_phones": seen, "invalid_jsonld_blocks": page["invalid_jsonld"]})


def not_observed(res: Dict[str, Any]) -> Optional[str]:
    if res.get("error"):
        return res["error"]
    st = res.get("status")
    if st is None:
        return "no response"
    if st >= 500 or st in BLOCKED_STATUSES_NOT_OBSERVED:
        return "HTTP %d" % st
    return None


def check_llms(col, site, url, res, summary):
    body = (res.get("body") or "").lstrip()
    soft404 = body[:15].lower().startswith(("<!doctype", "<html"))
    if res["status"] in (404, 410) or (res["status"] == 200 and (not body or soft404)):
        col.add("llms-txt-missing", site, url,
                "HTTP %d%s" % (res["status"], " with an empty or web-page body" if res["status"] == 200 else ""),
                "HTTP 200 with a plain-text guide file")


def check_sitemap(col, site, url, res):
    body = (res.get("body") or "")[:2000].lower()
    ok = res["status"] == 200 and ("<urlset" in body or "<sitemapindex" in body)
    if res["status"] in (404, 410) or (res["status"] == 200 and not ok):
        col.add("sitemap-missing", site, url, "HTTP %d%s" % (res["status"], "" if res["status"] != 200 else ", not a sitemap file"),
                "HTTP 200 with a list of pages")


def check_robots(col, site, url, res, summary):
    parsed = parse_robots(res.get("body") or "")
    blocked = [b for b in NAMED_BOTS if bot_blocked(parsed, b)]
    if res["status"] == 200 and blocked:
        col.add("ai-bot-blocked", site, url, "Whole site disallowed for: %s" % ", ".join(blocked),
                "No rule turns away the named AI and search crawlers")
    return parsed


def run(checks: list, expected: dict, urls_cfg: dict, mode: str, fetch: FetchFn):
    col = Collector([c["check_id"] for c in checks])
    allow = allowed_hosts_from(expected)
    summary: Dict[str, Any] = {"mode": mode, "checked": [], "not_observed": [], "skipped_needs_confirmation": [],
                               "status_notes": [], "pending_phones_seen": [], "page_observations": [],
                               "notes": []}
    fetched: Dict[str, Dict[str, Any]] = {}
    pending_all = all_pending_phones(expected)

    def get(url):
        if host_of(url) not in allow:
            summary["not_observed"].append({"url": url, "reason": "host not on the allowlist; not requested"})
            return None
        if url not in fetched:
            fetched[url] = fetch(url)
        res = fetched[url]
        reason = not_observed(res)
        if reason:
            summary["not_observed"].append({"url": url, "reason": reason})
            return None
        summary["checked"].append(url)
        return res

    for site, block in urls_cfg["hosts"].items():
        site_cfg = expected["sites"][site]
        sitemap_slot_used = False
        robots_parsed = None
        for e in block["urls"]:
            if mode == "tripwire" and not e["tripwire"]:
                continue
            if mode == "full" and e["needs_confirmation"]:
                summary["skipped_needs_confirmation"].append({"site": site, "id": e["id"], "url": e["url"]})
                continue
            res = get(e["url"])
            if res is None:
                continue
            kind = e["kind"]
            if kind == "page":
                if res["status"] == 200:
                    analyze_page(col, site, site_cfg, e["url"], res.get("final_url") or e["url"],
                                 res["headers"], res["body"], bool(e.get("faq")), summary, pending_all)
                else:
                    summary["status_notes"].append({"url": e["url"], "status": res["status"]})
                    if 400 <= res["status"] < 500:
                        final = res.get("final_url") or e["url"]
                        via = "" if final == e["url"] else " (after a redirect to %s)" % final
                        col.add("key-page-http-error", site, e["url"], "HTTP %d%s" % (res["status"], via),
                                "HTTP 200 with the real page",
                                verify={"type": "http_status", "url": e["url"], "assert": "200"})
            elif kind == "robots":
                robots_parsed = check_robots(col, site, e["url"], res, summary)
            elif kind == "llms":
                check_llms(col, site, e["url"], res, summary)
            elif kind == "sitemap":
                sitemap_slot_used = True
                check_sitemap(col, site, e["url"], res)
        if mode == "full" and not sitemap_slot_used:
            declared = [s for s in (robots_parsed or {}).get("sitemaps", []) if host_of(s) in allow]
            if declared:
                res = get(declared[0])
                if res is not None:
                    check_sitemap(col, site, declared[0], res)
            elif robots_parsed is not None:
                summary["notes"].append("%s: robots.txt declares no sitemap on an allowlisted host; sitemap not checked" % site)
            else:
                summary["notes"].append("%s: robots.txt not read; sitemap address unknown, not checked" % site)
    summary["finding_count"] = len(col.findings)
    return col.findings, summary


# ---------------------------------------------------------------- cli

def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        description="Read-only three-site SEO watch. Writes finding candidates, one JSON object per line.")
    ap.add_argument("--checks", default=os.path.join(HERE, "fixtures", "checks.json"),
                    help="SA-02 checks.json (check IDs)")
    ap.add_argument("--expected", default=os.path.join(HERE, "fixtures", "expected-sites.json"),
                    help="SA-02 expected-sites.json")
    ap.add_argument("--urls", default=os.path.join(HERE, "urls.json"), help="urls.json")
    ap.add_argument("--out", help="file for finding candidates (required unless --dry-run or --list-urls)")
    ap.add_argument("--mode", choices=["tripwire", "full"], default="tripwire")
    ap.add_argument("--fixtures", help="folder of saved pages with index.json; no network is used")
    ap.add_argument("--dry-run", action="store_true", help="print findings to stdout, write no file; summary goes to stderr")
    ap.add_argument("--list-urls", action="store_true", help="print the URL plan and exit; no requests")
    return ap


def main(argv: Optional[List[str]] = None, fetch: Optional[FetchFn] = None) -> int:
    args = build_parser().parse_args(argv)
    checks = load_json(args.checks)
    expected = load_json(args.expected)
    urls_cfg = load_json(args.urls)
    problems = validate_urls(urls_cfg, expected)
    if problems:
        for p in problems:
            print("urls.json problem: " + p, file=sys.stderr)
        return 2
    if args.list_urls:
        print(json.dumps(list_urls(urls_cfg), indent=2))
        return 0
    if not args.out and not args.dry_run:
        print("--out is required unless --dry-run or --list-urls", file=sys.stderr)
        return 2
    if fetch is None:
        fetch = fixture_fetcher(args.fixtures) if args.fixtures else LiveFetcher(allowed_hosts_from(expected))
    findings, summary = run(checks, expected, urls_cfg, args.mode, fetch)
    text = "".join(json.dumps(f, sort_keys=True) + "\n" for f in findings)
    if args.dry_run:
        sys.stdout.write(text)
        print(json.dumps(summary, indent=2), file=sys.stderr)
    else:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
