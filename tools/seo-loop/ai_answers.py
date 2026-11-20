#!/usr/bin/env python3
"""AI-answer capture v2 for Motor Inn (Carroll, Iowa).

For each shopper question, records whether an AI search answer cites or mentions
Motor Inn: CITED, MENTIONED, ABSENT or NOT OBSERVED. Counts are over observed
answers only. Read README.md first.

Nothing here sends, posts or publishes. The only network use is one function,
http_post(), which tests replace. --dry-run and --fixtures never call it.
"""
from __future__ import annotations

import argparse
import base64
import datetime
import hashlib
import json
import math
import os
import re
import sys
import time
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

HERE = os.path.dirname(os.path.abspath(__file__))

CITED = "CITED"
MENTIONED = "MENTIONED"
ABSENT = "ABSENT"
NOT_OBSERVED = "NOT OBSERVED"

HARD_CEILING_TOTAL = 25.0   # dollars a month, every DataForSEO use
HARD_CEILING_AI = 15.0      # dollars a month, AI answers
DEFAULT_ROW_LIMIT = 10
DEFAULT_CACHE_DAYS = 7
DEFAULT_TIMEOUT = 60


class GuardError(Exception):
    """A spend-guard, config or ledger problem. The call is refused."""


class ConfigError(GuardError):
    """The config is unusable. main() exits 1; nothing is called or written."""


# ---------------------------------------------------------------- network
def http_post(url, headers, body, timeout):
    """The ONLY place a socket is opened. Tests replace this function.

    Returns the decoded JSON response. Raises on any error or timeout.
    """
    import urllib.request
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310
        return json.loads(resp.read().decode("utf-8"))


# ---------------------------------------------------------------- loading
def load_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def load_is_us(path=None):
    return load_json(path or os.path.join(HERE, "is_us.json"))


def load_questions(path):
    data = load_json(path)
    qs = list(data.get("questions", []))
    probe = data.get("entity_probe")
    # The entity probe is asked first, every run. It is not one of the 30.
    return ([probe] if probe else []) + qs


def validate_config(cfg):
    """Return the config with defaults filled in, or raise GuardError."""
    loc = cfg.get("location")
    if not isinstance(loc, dict) or not loc:
        raise GuardError("config has no 'location'; set location_name or location_coordinate")
    keys = [k for k in ("location_name", "location_coordinate") if loc.get(k)]
    if len(keys) != 1:
        raise GuardError("config location needs exactly one of location_name or location_coordinate")
    if "location_name" in keys:
        if str(loc["location_name"]).strip().lower() in ("united states", "us", "usa", "united states of america"):
            raise GuardError("a country-wide location is not allowed; use Iowa or Carroll coordinates")
    out = dict(cfg)
    out.setdefault("base_url", "https://api.dataforseo.com")
    out.setdefault("language_code", "en")
    out["row_limit"] = int(cfg.get("row_limit", DEFAULT_ROW_LIMIT))
    out["cache_days"] = int(cfg.get("cache_days", DEFAULT_CACHE_DAYS))
    out["timeout_s"] = int(cfg.get("timeout_s", DEFAULT_TIMEOUT))
    out["ceiling_total_usd"] = min(float(cfg.get("ceiling_total_usd", HARD_CEILING_TOTAL)), HARD_CEILING_TOTAL)
    out["ceiling_ai_usd"] = min(float(cfg.get("ceiling_ai_usd", HARD_CEILING_AI)), HARD_CEILING_AI)
    plats = cfg.get("platforms")
    if not isinstance(plats, list) or not plats:
        raise ConfigError("config has no 'platforms' list; list each platform to call, nothing is assumed")
    for p in plats:
        est = p.get("est_cost_usd") if isinstance(p, dict) else None
        if isinstance(est, bool) or not isinstance(est, (int, float)) or not math.isfinite(est) or est <= 0:
            raise ConfigError("platform %s has no positive 'est_cost_usd' in config; refusing before any call"
                              % (p.get("name", "?") if isinstance(p, dict) else "?"))
    out["platforms"] = plats
    uf = cfg.get("usage_file")
    out["usage_file"] = uf if isinstance(uf, str) and uf.strip() else None
    return out


def get_auth_header(cfg):
    """Read the credential from the environment variable the config names.

    The value is never printed or written. It may be 'login:password' or an
    already-encoded Basic token.
    """
    name = cfg.get("credential_env")
    if not name:
        raise GuardError("config must name an environment variable in 'credential_env'")
    val = os.environ.get(name)
    if not val:
        raise GuardError("environment variable %s is not set" % name)
    if ":" in val:
        val = base64.b64encode(val.encode("utf-8")).decode("ascii")
    return {"Authorization": "Basic " + val, "Content-Type": "application/json"}


# ---------------------------------------------------------------- ledger
COUNTED_PROVIDERS = ("dataforseo",)
OTHER_KNOWN_PROVIDERS = ("semrush", "exa", "firecrawl", "ahrefs", "google", "gsc", "ga4")


def _entry_date(e):
    """Return 'YYYY-MM' from a string date or timestamp key, else None."""
    for k in ("date", "ts", "timestamp", "day", "at"):
        v = e.get(k)
        if isinstance(v, str) and len(v) >= 10 and v[10:11] in ("", "T", " "):
            try:
                d = datetime.date.fromisoformat(v[:10])
            except ValueError:
                return None
            return d.strftime("%Y-%m")
    return None


def _entry_cost(e):
    v = None
    for k in ("cost_usd", "cost", "usd", "amount_usd"):
        if k in e:
            v = e[k]
            break
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return None
    v = float(v)
    if math.isnan(v) or math.isinf(v) or v < 0:
        return None
    return v


def _ledger_entries(text):
    """Return [(label, parsed_or_exception)] with a plain label for each entry."""
    stripped = text.strip()
    if stripped[:1] == "[" or (stripped[:1] == "{" and '"entries"' in stripped and "\n{" not in stripped):
        try:
            obj = json.loads(stripped)
        except ValueError:
            raise GuardError("ledger is not valid JSON")
        items = obj.get("entries") if isinstance(obj, dict) else obj
        if not isinstance(items, list):
            raise GuardError("ledger has no list of entries")
        return [("entry %d" % (i + 1), e) for i, e in enumerate(items)]
    out = []
    for n, ln in enumerate(text.splitlines(), 1):
        if not ln.strip():
            continue
        try:
            out.append(("line %d" % n, json.loads(ln)))
        except ValueError:
            out.append(("line %d" % n, None))
    return out


def read_ledger(path, month, allow_missing_or_empty=False):
    """Return (total_usd, ai_usd) spent in `month` (YYYY-MM).

    Fails closed. Refuses (GuardError, naming the line) when the file is
    missing, empty or unreadable, or any entry cannot be fully understood: no
    parseable date, an unknown provider spelling, no purpose, or a cost that is
    non-numeric, negative, NaN or infinite. Every entry is checked, whatever
    its month. A purpose starting with "ai" counts toward the AI ceiling.
    `allow_missing_or_empty` is for our own usage file only.
    """
    try:
        with open(path, "r", encoding="utf-8") as fh:
            text = fh.read()
    except FileNotFoundError:
        if allow_missing_or_empty:
            return 0.0, 0.0
        raise GuardError("ledger %s is missing; refusing to spend" % os.path.basename(path))
    except (OSError, UnicodeDecodeError) as exc:
        raise GuardError("ledger unreadable (%s); refusing to spend" % exc.__class__.__name__)
    if not text.strip():
        if allow_missing_or_empty:
            return 0.0, 0.0
        raise GuardError("ledger is empty; refusing to spend")
    total = ai = 0.0
    for label, e in _ledger_entries(text):
        if not isinstance(e, dict):
            raise GuardError("ledger %s is not a readable entry; refusing to spend" % label)
        m = _entry_date(e)
        if m is None:
            raise GuardError("ledger %s has a missing or unreadable date; refusing to spend" % label)
        prov = e.get("provider")
        if not isinstance(prov, str) or prov.strip().lower() not in COUNTED_PROVIDERS + OTHER_KNOWN_PROVIDERS:
            raise GuardError("ledger %s has an unknown provider; refusing to spend" % label)
        c = _entry_cost(e)
        if c is None:
            raise GuardError("ledger %s has a cost that is not a plain number of zero or more; refusing to spend"
                             % label)
        purpose = e.get("purpose", e.get("use"))
        if not isinstance(purpose, str) or not purpose.strip():
            raise GuardError("ledger %s has no purpose; refusing to spend" % label)
        if prov.strip().lower() not in COUNTED_PROVIDERS or m != month:
            continue
        total += c
        if purpose.strip().lower().replace("-", "_").startswith("ai"):
            ai += c
    return total, ai


# ---- account spend as Mac mini 2 really records it (formats copied, not invented) ----
# Two folders written by the DealerVault runtime on Mac mini 2, both named for a UTC day:
#   dataforseo-provider-usage/YYYY-MM-DD.json   one receipt a day, from the free account-usage call
#   dataforseo-costs/YYYY-MM-DD.jsonl           one line per governed paid call
# `--ledger` is a folder that holds a copy of both. This script never writes there.
PROVIDER_USAGE_CONTRACT = "motorinn-dataforseo-provider-usage.v1"
PROVIDER_USAGE_SOURCE = "dataforseo_account_usage"
RECEIPT_DIR = "dataforseo-provider-usage"
GOVERNED_DIR = "dataforseo-costs"


def _money(v):
    """A plain finite number of zero or more (not text, not true/false), else None."""
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return None
    v = float(v)
    if not math.isfinite(v) or v < 0:
        return None
    return v


def _opt_money(obj, key, what):
    """A field the owner's code reads with a default of 0: absent is 0, present must be a plain number."""
    if key not in obj:
        return 0.0
    v = _money(obj[key])
    if v is None:
        raise GuardError("%s has an unreadable '%s'; refusing to spend" % (what, key))
    return v


def _day_files(folder, suffix, what):
    """{date: path} for the day-named files in `folder`. Refuses a missing, unreadable or empty folder."""
    try:
        names = sorted(os.listdir(folder))
    except OSError:
        raise GuardError("%s folder is missing or unreadable (%s); refusing to spend"
                         % (what, os.path.basename(os.path.normpath(folder)) or folder))
    found = {}
    for n in names:
        if n.startswith(".") or not n.endswith(suffix):
            continue
        stem = n[:-len(suffix)]
        try:
            day = datetime.date.fromisoformat(stem)
        except ValueError:
            day = None
        if day is None or day.isoformat() != stem:
            raise GuardError("%s file %s is not named for a date; refusing to spend" % (what, n))
        path = os.path.join(folder, n)
        if not os.path.isfile(path):
            raise GuardError("%s %s is not a file; refusing to spend" % (what, n))
        found[day] = path
    if not found:
        raise GuardError("%s folder has no files; refusing to spend" % what)
    return found


def _read_text(path, what):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except (OSError, UnicodeDecodeError) as exc:
        raise GuardError("%s unreadable (%s); refusing to spend" % (what, exc.__class__.__name__))


def read_receipt(path, day):
    """Read one daily receipt. Returns (actual, floor, ledger_at_reconciliation, account_hash_or_None)."""
    what = "receipt %s" % day.isoformat()
    try:
        obj = json.loads(_read_text(path, what))
    except ValueError:
        raise GuardError("%s is not valid JSON; refusing to spend" % what)
    if not isinstance(obj, dict):
        raise GuardError("%s is not an object; refusing to spend" % what)
    if obj.get("contractVersion") != PROVIDER_USAGE_CONTRACT:
        raise GuardError("%s has an unknown contractVersion; refusing to spend" % what)
    if obj.get("source") != PROVIDER_USAGE_SOURCE:
        raise GuardError("%s has an unknown source; refusing to spend" % what)
    if obj.get("usageDate") != day.isoformat():
        raise GuardError("%s usageDate does not match its file name; refusing to spend" % what)
    actual = _money(obj.get("actualCostUsd"))
    if actual is None:
        raise GuardError("%s has an actualCostUsd that is not a plain number of zero or more; refusing to spend"
                         % what)
    floor = _opt_money(obj, "budgetFloorUsd", what)
    at = _opt_money(obj, "ledgerSpentAtReconciliationUsd", what)
    h = obj.get("accountIdHash")
    if h is not None and (not isinstance(h, str) or len(h) != 64 or any(c not in "0123456789abcdef" for c in h)):
        raise GuardError("%s has an unreadable accountIdHash; refusing to spend" % what)
    return actual, floor, at, h


def read_governed_day(path, day):
    """Sum actualCostUsd over one governed-ledger day file. Any line that cannot be read refuses."""
    what = "governed ledger %s" % day.isoformat()
    total = 0.0
    for n, ln in enumerate(_read_text(path, what).splitlines(), 1):
        if not ln.strip():
            continue
        try:
            obj = json.loads(ln)
        except ValueError:
            raise GuardError("%s line %d is not valid JSON; refusing to spend" % (what, n))
        c = _money(obj.get("actualCostUsd")) if isinstance(obj, dict) else None
        if c is None:
            raise GuardError("%s line %d has no plain actualCostUsd of zero or more; refusing to spend" % (what, n))
        total += c
    return total


def day_spend(ledger_total, receipt):
    """One UTC day's account spend. The owner's own formula (dataforseo_costs.spent_today), unchanged.

    The receipt is one snapshot taken once a day; governed calls recorded after it are added on top;
    never less than the governed ledger itself. With no receipt only the governed ledger is known.
    """
    if receipt is None:
        return ledger_total
    actual, floor, at, _h = receipt
    later_local = max(0.0, ledger_total - at)
    baseline = max(actual, floor)
    return max(ledger_total, baseline + later_local)


def outside_spend(mirror_dir, today):
    """Month-to-date account spend from the copied Mac mini 2 folders, summed over UTC days.

    Refuses when either folder is missing, unreadable or empty, when any day from the 1st to the day
    before `today` has no receipt (a missing day is never read as zero), or when any file of the month
    cannot be fully understood. Files of other months are not read.
    """
    receipts = _day_files(os.path.join(mirror_dir, RECEIPT_DIR), ".json", "provider-usage receipt")
    governed = _day_files(os.path.join(mirror_dir, GOVERNED_DIR), ".jsonl", "governed ledger")
    month = today.strftime("%Y-%m")
    first = today.replace(day=1)
    missing = []
    d = first
    while d < today:
        if d not in receipts:
            missing.append(d.isoformat())
        d += datetime.timedelta(days=1)
    if missing:
        raise GuardError("no provider-usage receipt for %d day(s) this month (%s); a missing day is not zero; "
                         "refusing to spend" % (len(missing), ", ".join(missing[:6]) + (", ..." if len(missing) > 6 else "")))
    total = 0.0
    hashes = set()
    for day in sorted(set(receipts) | set(governed)):
        if day.strftime("%Y-%m") != month:
            continue
        rec = read_receipt(receipts[day], day) if day in receipts else None
        if rec is not None and rec[3]:
            hashes.add(rec[3])
        led = read_governed_day(governed[day], day) if day in governed else 0.0
        total += day_spend(led, rec)
    if len(hashes) > 1:
        raise GuardError("receipts this month name more than one account; refusing to spend")
    return total


def spent_this_month(mirror_dir, usage_path, today):
    """(total, ai) month-to-date for the month of `today`.

    Outside spend (every DataForSEO user on the account; receipts carry no purpose, so all of it also
    counts toward the AI ceiling) plus our own fixed usage file. Our own calls can show up in both a later
    receipt and the usage file: that counts them twice, which is safe and over-cautious.
    """
    outside = outside_spend(mirror_dir, today)
    own_t = own_a = 0.0
    if usage_path:
        own_t, own_a = read_ledger(usage_path, today.strftime("%Y-%m"), allow_missing_or_empty=True)
    return outside + own_t, outside + own_a


def record_usage(usage_path, today, platform_name, qid, cost, note=None):
    """Append one usage line and fsync it. Called BEFORE the paid call."""
    rec = {"date": today.isoformat(), "provider": "dataforseo", "purpose": "ai_answers",
           "cost_usd": float(cost), "platform": platform_name, "question_id": qid}
    if note:
        rec["note"] = note
    with open(usage_path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec) + "\n")
        fh.flush()
        os.fsync(fh.fileno())


def check_spend(total, ai, cost, cfg):
    """Raise GuardError unless spent + cost stays within both ceilings.

    cost must be a positive number. At the ceiling there is no room.
    """
    if isinstance(cost, bool) or not isinstance(cost, (int, float)) or not math.isfinite(cost) or cost <= 0:
        raise GuardError("no positive cost estimate for this call; refusing")
    if round(total + cost, 6) > cfg["ceiling_total_usd"]:
        raise GuardError("monthly ceiling: $%.2f spent + $%.3f call would pass $%.2f total"
                         % (total, cost, cfg["ceiling_total_usd"]))
    if round(ai + cost, 6) > cfg["ceiling_ai_usd"]:
        raise GuardError("AI-answers ceiling: $%.2f spent + $%.3f call would pass $%.2f"
                         % (ai, cost, cfg["ceiling_ai_usd"]))


# ---------------------------------------------------------------- classification
def host_of(url):
    try:
        h = (urlparse(url if "//" in url else "//" + url).hostname or "").lower().rstrip(".")
    except ValueError:
        return ""
    return h[4:] if h.startswith("www.") else h


def _sentences(text):
    return [s for s in re.split(r"(?<=[.!?])\s+|\n+", text or "") if s.strip()]


def _brand_from_sentence(sentence):
    low = sentence.lower()
    t = "toyota" in low
    c = "chevrolet" in low or "chevy" in low
    if t and not c:
        return "toyota"
    if c and not t:
        return "chevy"
    return "group"


def is_our_source(src, is_us):
    """Return brand if the source is ours (exact host or exact listing URL), else None."""
    url = src.get("url") or src.get("link") or ""
    if url in is_us.get("listing_urls", []):
        return "group"
    host = host_of(url) or host_of(src.get("domain") or "")
    return is_us["hosts"].get(host)


def find_name_mentions(text, is_us):
    """Return a list of (brand, matched text) where our name appears.

    Exact names count anywhere. The loose name 'Motor Inn' counts only inside
    a sentence that also contains 'Carroll'. 'Carroll' alone never counts.
    """
    hits = []
    covered = []
    names = sorted(is_us["names"].items(), key=lambda kv: -len(kv[0]))
    for name, brand in names:
        for m in re.finditer(r"(?<![\w])" + re.escape(name) + r"(?![\w])", text or "", re.I):
            if any(m.start() >= a and m.end() <= b for a, b in covered):
                continue
            covered.append((m.start(), m.end()))
            hits.append((brand, m.group(0)))
    loose = is_us.get("loose_name", "Motor Inn")
    town = is_us.get("town", "Carroll")
    for s in _sentences(text):
        if re.search(r"(?<![\w])" + re.escape(loose) + r"(?![\w])", s, re.I) and \
                re.search(r"(?<![\w])" + re.escape(town) + r"(?![\w])", s, re.I):
            hits.append((_brand_from_sentence(s), loose))
    return hits


def find_rivals(answer, is_us):
    """Other businesses named for the town (never counted as us)."""
    kws = [k.lower() for k in is_us.get("rival_keywords", [])]
    town = is_us.get("town", "Carroll")
    rivals = []
    for src in answer.get("sources", []):
        if is_our_source(src, is_us):
            continue
        title = src.get("title") or ""
        host = host_of(src.get("url") or "")
        if town.lower() in title.lower() or town.lower() in host:
            rivals.append(title or host)
    pat = re.compile(r"((?:[A-Z][\w&'.-]*\s+){0,2}" + re.escape(town) + r"(?:\s+[A-Z][\w&'.-]*){0,3})")
    ours = [n.lower() for n in is_us["names"]]
    for m in pat.finditer(answer.get("text") or ""):
        cand = m.group(1).strip().rstrip(".,")
        words = [w.lower() for w in re.findall(r"[\w']+", cand)]
        if cand.lower() in ours or "motor inn" in cand.lower():
            continue
        if any(w in kws for w in words if w != town.lower()):
            rivals.append(cand)
    seen = []
    for r in rivals:
        if r not in seen:
            seen.append(r)
    return seen


def classify(answer, is_us):
    """Classify one captured answer.

    `answer` is {"observed": bool, "text": str, "sources": [{url,title,domain}], "reason": str}.
    Returns {"state", "brand", "cited_hosts", "mention_texts", "rivals", "notes"}.
    """
    if not answer.get("observed"):
        return {"state": NOT_OBSERVED, "brand": None, "cited_hosts": [], "mention_texts": [],
                "rivals": [], "notes": [answer.get("reason", "not captured")]}
    text = answer.get("text") or ""
    sources = answer.get("sources") or []
    cited = []
    for s in sources:
        b = is_our_source(s, is_us)
        if b:
            cited.append((b, host_of(s.get("url") or "")))
    mentions = find_name_mentions(text, is_us)
    rivals = find_rivals(answer, is_us)
    notes = []
    low = text.lower()
    if mentions and any(w in low for w in is_us.get("confusion_words", [])):
        notes.append("answer also uses motel or lodging words: check for a name mix-up")
    if cited:
        return {"state": CITED, "brand": cited[0][0], "cited_hosts": sorted(set(h for _, h in cited)),
                "mention_texts": [m for _, m in mentions], "rivals": rivals, "notes": notes}
    if mentions:
        return {"state": MENTIONED, "brand": mentions[0][0], "cited_hosts": [],
                "mention_texts": [m for _, m in mentions], "rivals": rivals, "notes": notes}
    return {"state": ABSENT, "brand": None, "cited_hosts": [], "mention_texts": [],
            "rivals": rivals, "notes": notes}


# ---------------------------------------------------------------- response parsing
def parse_response(resp):
    """Turn a DataForSEO-style response into the answer shape.

    Only the answer text and cited references are read. Any non-success status,
    or a response with no answer text and no references, is NOT observed.
    """
    try:
        if not isinstance(resp, dict):
            return {"observed": False, "reason": "response was not an object"}
        top = resp.get("status_code")
        if top is not None and int(top) != 20000:
            return {"observed": False, "reason": "api status %s" % top}
        tasks = resp.get("tasks") or []
        if not tasks:
            return {"observed": False, "reason": "no tasks in response"}
        task = tasks[0]
        if int(task.get("status_code", 0)) != 20000:
            return {"observed": False, "reason": "task status %s" % task.get("status_code")}
        texts, sources = [], []
        for result in task.get("result") or []:
            _walk_items(result.get("items") or [], texts, sources)
        text = "\n".join(t for t in texts if t).strip()
        if not text and not sources:
            return {"observed": False, "reason": "no AI answer appeared"}
        return {"observed": True, "text": text, "sources": sources,
                "cost": task.get("cost")}
    except (ValueError, TypeError, AttributeError) as exc:
        return {"observed": False, "reason": "unreadable response (%s)" % exc.__class__.__name__}


def _walk_items(items, texts, sources):
    for it in items:
        if not isinstance(it, dict):
            continue
        typ = str(it.get("type", ""))
        if typ in ("ai_overview", "ai_mode", "ai_overview_element", "ai_mode_element", "ai_overview_expanded_element") \
                or "references" in it or "markdown" in it:
            t = it.get("markdown") or it.get("text")
            if t:
                texts.append(t)
            for r in it.get("references") or []:
                if isinstance(r, dict) and (r.get("url") or r.get("domain")):
                    sources.append({"url": r.get("url") or "", "title": r.get("title") or r.get("source") or "",
                                    "domain": r.get("domain") or ""})
        for key in ("items", "ai_overview_items"):
            if isinstance(it.get(key), list):
                _walk_items(it[key], texts, sources)


# ---------------------------------------------------------------- cache
def cache_key(platform, question_text, cfg):
    blob = json.dumps([platform["name"], question_text, cfg["location"], cfg["language_code"], cfg["row_limit"]],
                      sort_keys=True)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:32]


def cache_read(cache_dir, key, now, days):
    path = os.path.join(cache_dir, key + ".json")
    try:
        with open(path, "r", encoding="utf-8") as fh:
            obj = json.load(fh)
        age = now - float(obj["cached_at"])
    except (OSError, ValueError, KeyError, TypeError):
        return None
    return obj["response"] if age <= days * 86400 else None


def cache_write(cache_dir, key, now, response):
    os.makedirs(cache_dir, exist_ok=True)
    with open(os.path.join(cache_dir, key + ".json"), "w", encoding="utf-8") as fh:
        json.dump({"cached_at": now, "response": response}, fh)


# ---------------------------------------------------------------- requests
def build_request(platform, question_text, cfg):
    """Only the fields the call uses. Row limit set on every call."""
    body = {"keyword": question_text, "language_code": cfg["language_code"], "depth": cfg["row_limit"]}
    body.update(cfg["location"])
    body.update(platform.get("extra") or {})
    return cfg["base_url"].rstrip("/") + platform["endpoint"], [body]


def fixture_response(fx_dir, qid, platform):
    path = os.path.join(fx_dir, "%s.%s.json" % (qid, platform["name"]))
    if not os.path.exists(path):
        return None
    return load_json(path)


# ---------------------------------------------------------------- run
def plan_calls(questions, cfg, cache_dir, now):
    """List planned calls: [(question, platform, cached_bool)]."""
    plan = []
    for q in questions:
        for p in cfg["platforms"]:
            if not p.get("enabled", True):
                continue
            hit = cache_read(cache_dir, cache_key(p, q["text"], cfg), now, cfg["cache_days"]) is not None
            plan.append((q, p, hit))
    return plan


def summarize(rows):
    """Counts over observed answers only. The entity probe E0 is left out."""
    def blank():
        return {"observed": 0, "cited": 0, "mentioned": 0, "absent": 0, "not_observed": 0}
    counts = {"all": blank()}
    for r in rows:
        if r["question_id"] == "E0":
            continue
        for key in ("all", r["question_brand"]):
            c = counts.setdefault(key, blank())
            if r["state"] == NOT_OBSERVED:
                c["not_observed"] += 1
                continue
            c["observed"] += 1
            c[{CITED: "cited", MENTIONED: "mentioned", ABSENT: "absent"}[r["state"]]] += 1
    for c in counts.values():
        c["named"] = c["cited"] + c["mentioned"]
        c["text"] = "named in %d of %d observed answers" % (c["named"], c["observed"])
    return counts


def run(args, out=None):
    out = out or sys.stdout
    is_us = load_is_us(args.is_us)
    questions = load_questions(args.questions)
    cfg = validate_config(load_json(args.config))
    # The account's days are UTC days (receipts and governed ledger files are named that way).
    today = (datetime.date.fromisoformat(args.today) if args.today
             else datetime.datetime.now(datetime.timezone.utc).date())
    month = today.strftime("%Y-%m")
    now = time.time()
    cache_dir = os.path.join(args.out, "cache")
    plan = plan_calls(questions, cfg, cache_dir, now)
    live = [(q, p) for q, p, hit in plan if not hit]
    est = sum(float(p.get("est_cost_usd", 0)) for q, p in live)

    usage_path = cfg["usage_file"]
    if usage_path and not os.path.isabs(usage_path):
        usage_path = os.path.join(os.path.dirname(os.path.abspath(args.config)), usage_path)
    if not usage_path and not args.fixtures and not args.dry_run:
        raise ConfigError("config has no 'usage_file'; every paid call is recorded there first")
    ledger_total = ledger_ai = None
    ledger_problem = None
    try:
        ledger_total, ledger_ai = spent_this_month(args.ledger, usage_path, today)
    except GuardError as exc:
        ledger_problem = str(exc)

    if args.dry_run:
        print("DRY RUN: no network, no files written.", file=out)
        print("location: %s" % json.dumps(cfg["location"], sort_keys=True), file=out)
        print("questions: %d  platforms: %d  planned rows: %d  cached (free): %d  live calls: %d"
              % (len(questions), len([p for p in cfg["platforms"] if p.get("enabled", True)]),
                 len(plan), len(plan) - len(live), len(live)), file=out)
        for q, p in live:
            print("CALL %s  %s  est $%.3f  row limit %d" % (q["id"], p["name"], float(p.get("est_cost_usd", 0)),
                                                         cfg["row_limit"]), file=out)
        print("estimated cost: $%.3f" % est, file=out)
        if ledger_problem:
            print("ledger: %s (a live run would refuse)" % ledger_problem, file=out)
        else:
            print("ledger %s: $%.2f of $%.2f total, $%.2f of $%.2f AI answers"
                  % (month, ledger_total, cfg["ceiling_total_usd"], ledger_ai, cfg["ceiling_ai_usd"]), file=out)
            try:
                if live:
                    check_spend(ledger_total, ledger_ai, est, cfg)
            except GuardError as exc:
                print("WOULD REFUSE: %s" % exc, file=out)
        return 0

    headers = None
    if not args.fixtures:
        if ledger_problem:
            print("REFUSED: %s" % ledger_problem, file=out)
            return 3
        headers = get_auth_header(cfg)

    os.makedirs(args.out, exist_ok=True)
    session = 0.0
    rows = []
    refused = False
    for q, p, hit in plan:
        qb = q.get("brand", "group")
        row = {"question_id": q["id"], "question_brand": qb, "department": q.get("department"),
               "group": q.get("group"), "platform": p["name"], "label": p.get("label", "observed"),
               "location": cfg["location"], "from_cache": False}
        key = cache_key(p, q["text"], cfg)
        resp = None
        if args.fixtures:
            resp = fixture_response(args.fixtures, q["id"], p)
            answer = parse_response(resp) if resp is not None else {"observed": False, "reason": "no fixture"}
        else:
            resp = cache_read(cache_dir, key, now, cfg["cache_days"])
            if resp is not None:
                row["from_cache"] = True
                answer = parse_response(resp)
            elif refused:
                answer = {"observed": False, "reason": "spend guard refused"}
            else:
                cost = float(p["est_cost_usd"])
                try:
                    # Re-read everything each call: other runs and a crash leave their spend in the files.
                    t_now, a_now = spent_this_month(args.ledger, usage_path, today)
                    check_spend(t_now, a_now, cost, cfg)
                except GuardError as exc:
                    refused = True
                    print("REFUSED: %s" % exc, file=out)
                    answer = {"observed": False, "reason": "spend guard refused"}
                else:
                    url, body = build_request(p, q["text"], cfg)
                    record_usage(usage_path, today, p["name"], q["id"], cost)  # written and fsynced first
                    session += cost
                    try:
                        resp = http_post(url, headers, body, cfg["timeout_s"])
                    except Exception as exc:  # any error or timeout is NOT OBSERVED; cost stays counted
                        resp = None
                        answer = {"observed": False, "reason": "call failed (%s)" % exc.__class__.__name__}
                    else:
                        answer = parse_response(resp)
                        actual = answer.get("cost")
                        if isinstance(actual, (int, float)) and not isinstance(actual, bool) \
                                and math.isfinite(actual) and actual > cost:
                            record_usage(usage_path, today, p["name"], q["id"], actual - cost, "adjustment")
                            session += actual - cost
                        if answer.get("observed"):
                            cache_write(cache_dir, key, now, resp)
                    print("running cost this run: $%.3f" % session, file=out)
        res = classify(answer, is_us)
        row.update({"state": res["state"], "brand": res["brand"], "cited_hosts": res["cited_hosts"],
                    "mention_texts": res["mention_texts"], "rivals": res["rivals"], "notes": res["notes"]})
        if not answer.get("observed"):
            row["reason"] = answer.get("reason")
        rows.append(row)

    counts = summarize(rows)
    result = {"baseline_id": "B2", "date": today.isoformat(), "location": cfg["location"],
              "rows": rows, "counts": counts, "run_cost_usd": round(session, 4),
              "ledger_month": month}
    with open(os.path.join(args.out, "ai_answers-%s.json" % today.isoformat()), "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=1)
        fh.write("\n")
    print("Motor Inn AI answers, %s: %s. Run cost $%.3f." % (today.isoformat(), counts["all"]["text"], session),
          file=out)
    for k in sorted(counts):
        if k != "all":
            print("  %s: %s" % (k, counts[k]["text"]), file=out)
    return 3 if refused else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Record whether AI search answers cite or mention Motor Inn.")
    ap.add_argument("--questions", required=True, help="questions JSON (questions.B2.json)")
    ap.add_argument("--config", required=True, help="config JSON: location, credential_env, platforms")
    ap.add_argument("--ledger", required=True,
                    help="folder holding a copy of Mac mini 2's dataforseo-provider-usage/ and dataforseo-costs/ "
                         "(read only; a missing, empty or unreadable folder or a missing day refuses)")
    ap.add_argument("--out", required=True, help="output folder (results and cache)")
    ap.add_argument("--dry-run", action="store_true", help="print planned calls and cost; open no socket")
    ap.add_argument("--fixtures", help="folder of saved responses; no network call is made")
    ap.add_argument("--is-us", help="override is_us.json")
    ap.add_argument("--today", help="YYYY-MM-DD (default: today, UTC)")
    args = ap.parse_args(argv)
    try:
        return run(args)
    except ConfigError as exc:
        print("CONFIG ERROR: %s" % exc, file=sys.stderr)
        return 1
    except GuardError as exc:
        print("REFUSED: %s" % exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
