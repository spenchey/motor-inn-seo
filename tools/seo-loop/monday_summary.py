"""Monday summary builder (SA-05).

Reads the findings register and the baselines file, prints one short
plain-English note to standard output. It changes no file and sends nothing.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import register  # noqa: E402  (frozen SA-01 module, placed beside this file)

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]
NOT_VERIFIED = "not verified"
NOTHING = "Nothing needs you this week."
WORD_LIMIT = 299
WINDOW_DAYS = 7
AI_VISITS_MAX_AGE_DAYS = 8  # AI visit numbers whose data ended longer ago than this are stale

GSC = "Google Search Console"
GA = "Google Analytics visits by site"
LEADS = "organic lead count"
CRM = "our CRM website leads"
GBP = "Google Business reviews and activity"
AI = "AI answers"
AI_VISITS = "AI assistant visits"
LISTINGS = ("gbp-toyota", "gbp-chevy", "gbp-group")

SITE_NAMES = {
    "group": "the Motor Inn group site",
    "toyota": "the Toyota site",
    "chevy": "the Chevrolet site",
    "gbp-toyota": "a Google Business listing",
    "gbp-chevy": "a Google Business listing",
    "gbp-group": "a Google Business listing",
    "mirror": "the inventory feed",
    "all": "all of our sites",
}

# Anything matching these is internal plumbing and must not reach Spencer.
_BANNED = [
    re.compile(r"\bF-[A-Za-z0-9_-]+"),                                  # finding ids
    re.compile(r"\b[\w.-]+\.(?:jsonl|json|md|py|csv|txt|html|sh|log)\b", re.I),  # file names
    re.compile(r"https?://", re.I),
    re.compile(r"(?:^|\s)[/~]\S"),                                      # paths
    re.compile(r"\S+/\S+/\S+"),
    re.compile(r"/Users|/Volumes|~/", re.I),
    re.compile(r"\b[A-Za-z]+(?:_[A-Za-z]+)+\b"),                       # status codes, snake_case
    re.compile(r"pending-spencer", re.I),
    re.compile(r"\b[a-z0-9]+(?:-[a-z0-9]+){2,}\b"),                    # slug-like ids
]


_EMAIL = re.compile(r"\S+@\S+")
_CARD_CODE = re.compile(r"\b[A-Za-z]{1,6}-\d+\b")
_PHONE = re.compile(r"(?<!\d)(?:\+?1[\s.-]*)?\(?\d{3}\)?[\s.-]*\d{3}[\s.-]*\d{4}(?!\d)")
OUR_PHONE = "7127925000"
NO_FINDINGS = "No findings are on record, so this report cannot confirm the sites are healthy."


def _has_private_detail(text: str) -> bool:
    if _EMAIL.search(text) or _CARD_CODE.search(text):
        return True
    for m in _PHONE.finditer(text):
        digits = re.sub(r"\D", "", m.group(0))
        if digits.startswith("1") and len(digits) == 11:
            digits = digits[1:]
        if digits != OUR_PHONE:
            return True
    return False


class SummaryError(Exception):
    pass


def _date_label(day) -> str:
    return "%s %d" % (MONTHS[day.month - 1], day.day)


def _plural(n: int, one: str, many: str) -> str:
    return one if n == 1 else many


def _words(text: str) -> int:
    return len(text.split())


def _load_json(path: str, what: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError) as exc:
        raise SummaryError("Cannot read the %s (%s). No summary was made." % (what, os.path.basename(path)))
    if not isinstance(data, dict):
        raise SummaryError("The %s is not in the expected shape. No summary was made." % what)
    return data


def _load_register(path: str) -> list:
    try:
        return register.load_rows(path, must_exist=True)
    except (register.RegisterError, OSError, UnicodeDecodeError):
        raise SummaryError("Cannot read the findings register. No summary was made.")


# ---------------------------------------------------------------------------
# Numbers
# ---------------------------------------------------------------------------

def _metric_number(block, site: str, key: str):
    """Return a number from baselines['sites'][site][key], or None if not verified."""
    try:
        metric = block["sites"][site][key]
    except (KeyError, TypeError):
        return None
    value = metric.get("value") if isinstance(metric, dict) else None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return value


def _leads_number(block):
    """Organic leads come from the three-site total only, never one site's number."""
    try:
        metric = block["organic_leads_total"]
    except (KeyError, TypeError):
        return None
    value = metric.get("value") if isinstance(metric, dict) else None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return value


def _crm_number(block):
    """Website leads the CRM logged in the same period (a check line, never the headline)."""
    try:
        metric = block["crm_website_leads"]
    except (KeyError, TypeError):
        return None
    value = metric.get("value") if isinstance(metric, dict) else None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return value


_WINDOW = re.compile(r"^(\d{4})-(\d{2})-(\d{2})\.\.(\d{4})-(\d{2})-(\d{2})$")


def _window_label(block, key: str) -> str:
    """' (November 1 to November 22)' from a metric window, or '' when it is missing or odd."""
    try:
        win = block[key]["window"]
        m = _WINDOW.match(win)
        a = _dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        b = _dt.date(int(m.group(4)), int(m.group(5)), int(m.group(6)))
    except (KeyError, TypeError, AttributeError, ValueError):
        return ""
    return " (%s to %s)" % (_date_label(a), _date_label(b))


def _site_leads_missing(block) -> bool:
    """True when the Toyota or Chevrolet organic lead number is not verified."""
    sites = block.get("sites") if isinstance(block, dict) else None
    sites = sites if isinstance(sites, dict) else {}
    for name in ("toyota", "chevy"):
        entry = sites.get(name)
        metric = entry.get("organic_leads") if isinstance(entry, dict) else None
        if not _metric_ok(metric):
            return True
    return False


def _metric_ok(metric) -> bool:
    """True when a metric object carries a real value (not missing, not 'not verified')."""
    if not isinstance(metric, dict):
        return False
    value = metric.get("value")
    if value is None or isinstance(value, bool):
        return False
    if isinstance(value, str) and value.strip().lower() in ("", NOT_VERIFIED):
        return False
    return True


def _unverified_sources(block, gsc, leads, today) -> list:
    """Plain names of every source with a metric that is missing or not verified."""
    out = []
    if any(v is None for v in gsc.values()):
        out.append(GSC)
    sites = block.get("sites") if isinstance(block, dict) else None
    if isinstance(sites, dict):
        ga_metrics = [m.get("ga4_organic_sessions_28d") for m in sites.values()
                      if isinstance(m, dict) and "ga4_organic_sessions_28d" in m]
        if any(not _metric_ok(m) for m in ga_metrics):
            out.append(GA)
    if leads is None:
        out.append(LEADS)
    if _crm_number(block) is None:
        out.append(CRM)
    listings = block.get("listings") if isinstance(block, dict) else None
    if not isinstance(listings, dict):
        listings = {}
    gbp_bad = False
    for name in LISTINGS:
        entry = listings.get(name)
        if not isinstance(entry, dict) or not entry:
            gbp_bad = True
            continue
        if any(not _metric_ok(m) for m in entry.values()):
            gbp_bad = True
    if gbp_bad:
        out.append(GBP)
    ai_metric = _ai_metric(block)
    if not _metric_ok(ai_metric) or not isinstance(ai_metric.get("value"), (int, float)):
        out.append(AI)
    if _ai_referrals_line(block, today).startswith(AI_VISITS):
        out.append(AI_VISITS)
    return out


def _ai_metric(block):
    """The AI-answers metric as written by the baseline reader: {value, window, source, pulled_at}."""
    return block.get("ai_answers") if isinstance(block, dict) else None


_RANGE = re.compile(r"(\d{4}-\d{2}-\d{2})\.\.(\d{4}-\d{2}-\d{2})")


def _window_dates(window):
    """(start, end) dates for a window written as YYYY-MM-DD..YYYY-MM-DD, else None."""
    m = _RANGE.fullmatch(window.strip()) if isinstance(window, str) else None
    if not m:
        return None
    try:
        start, end = _dt.date.fromisoformat(m.group(1)), _dt.date.fromisoformat(m.group(2))
    except ValueError:
        return None
    return (start, end) if start <= end else None


def _range_label(start, end) -> str:
    """Nov 1\u201323, or Oct 28\u2013Nov 3 when the window crosses a month."""
    first = "%s %d" % (MONTHS[start.month - 1][:3], start.day)
    if start == end:
        return first
    if (start.year, start.month) == (end.year, end.month):
        return "%s\u2013%d" % (first, end.day)
    return "%s\u2013%s %d" % (first, MONTHS[end.month - 1][:3], end.day)


def _ai_line(block) -> str:
    """One plain line on the AI answers number. We do not know what the number counts, so we only repeat it."""
    metric = _ai_metric(block)
    value = metric.get("value") if isinstance(metric, dict) else None
    if not _metric_ok(metric) or not isinstance(value, (int, float)):
        return "%s: %s." % (AI, NOT_VERIFIED)
    dates = _window_dates(metric.get("window"))
    window = _range_label(*dates) if dates else "window not stated"
    return "%s: %s (%s)." % (AI, _fmt(value), window)


def _ai_referrals_line(baselines, today) -> str:
    """One plain line on visits and leads that AI assistants sent, from the newest month in the block."""
    not_verified = "%s: %s." % (AI_VISITS, NOT_VERIFIED)
    block = baselines.get("ai_referrals") if isinstance(baselines, dict) else None
    months = sorted(k for k in block if isinstance(k, str) and re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", k)) \
        if isinstance(block, dict) else []
    if not months:
        return not_verified
    entry = block[months[-1]]
    counts, windows = [], []
    for key in ("sessions", "leads"):
        metric = entry.get(key) if isinstance(entry, dict) else None
        value = metric.get("value") if isinstance(metric, dict) else None
        ok = _metric_ok(metric) and isinstance(value, (int, float)) and float(value) == int(value) and value >= 0
        counts.append(int(value) if ok else None)
        windows.append(_window_dates(metric.get("window")) if ok else None)
    if None in counts or None in windows or windows[0] != windows[1]:
        return not_verified
    start, end = windows[0]
    if end > today:
        return not_verified
    if (today - end).days > AI_VISITS_MAX_AGE_DAYS:
        return "%s: %s (stale)." % (AI_VISITS, NOT_VERIFIED)
    visits, leads = counts
    return "AI assistants sent %d %s, %d %s (forms + calls), %s." % (
        visits, "visit" if visits == 1 else "visits",
        leads, "lead" if leads == 1 else "leads", _range_label(start, end))


def _fmt(value) -> str:
    if value is None:
        return NOT_VERIFIED
    if float(value) == int(value):
        return "{:,}".format(int(value))
    return "{:,.1f}".format(value)


def _trend(now, before) -> str:
    if now is None or before is None or before <= 0:
        return ""
    pct = int(round((now - before) * 100.0 / before))
    if pct >= 5:
        return " Google clicks are up %d%% on the last check." % pct
    if pct <= -5:
        return " Google clicks are down %d%% on the last check." % abs(pct)
    return " Google clicks are about the same as the last check."


# ---------------------------------------------------------------------------
# Plain wording
# ---------------------------------------------------------------------------

_ISO_DATE = re.compile(r"(?<![\w-])(\d{4})-(\d{2})-(\d{2})(?![\w-])")


def _plain_dates(text: str) -> str:
    """Write ISO dates in words, for example 2026-11-23 becomes November 23."""
    def swap(m):
        try:
            day = _dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            return m.group(0)
        return _date_label(day)
    return _ISO_DATE.sub(swap, text)


def _clean(text, known_check_ids):
    """Return text if it is plain English, else None (the caller uses a fallback)."""
    if not isinstance(text, str) or not text.strip():
        return None
    text = _plain_dates(" ".join(text.split()))
    # an ordinary three-word phrase, not a slug, so the slug guard below must not drop the whole line
    text = text.replace("question-and-answer", "question and answer")
    if _has_private_detail(text):
        return None
    # Our one phone number is allowed; hide it from the slug guard, then restore it.
    text = text.replace("712-792-5000", "\x00")
    for pattern in _BANNED:
        if pattern.search(text):
            return None
    text = text.replace("\x00", "712-792-5000")
    low = text.lower()
    for cid in known_check_ids:
        if cid and re.search(r"(?<![a-z0-9-])%s(?![a-z0-9-])" % re.escape(cid), low):
            return None
    return text


def _limit(text: str, max_words: int) -> str:
    parts = text.split()
    if len(parts) <= max_words:
        return text
    return " ".join(parts[:max_words]).rstrip(",;:-") + "..."


def _soften_action(text: str) -> str:
    text = re.sub(r"^\s*Spencer to ", "Please ", text)
    text = re.sub(r"^\s*Ask Spencer ", "Please tell us ", text)
    text = re.sub(r"^\s*Spencer decision:\s*", "Your decision is needed: ", text)
    return text


def _ask_sentence(row: dict, known_check_ids, max_words: int) -> str:
    title = _clean(row.get("title"), known_check_ids)
    if title is None:
        title = "A problem on %s needs a look" % SITE_NAMES.get(row.get("site"), "one of our sites")
    action = _clean(row.get("next_action"), known_check_ids)
    if action is not None:
        action = _clean(_soften_action(action), known_check_ids)
    if action is None:
        action = "Please take a look when you can"
    title = _limit(title.rstrip(".!? "), max_words)
    action = _limit(action.rstrip(".!? "), max_words)
    return "%s. %s." % (title, action)


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def _last_pass_date(row: dict):
    verified = row.get("verified")
    if not isinstance(verified, dict):
        return None
    stamps = []
    for p in verified.get("passes") or []:
        if isinstance(p, dict) and p.get("passed") and p.get("at"):
            stamps.append(p["at"])
    if not stamps and verified.get("at"):
        stamps.append(verified["at"])
    best = None
    for s in stamps:
        try:
            d = register.parse_timestamp(s).date()
        except register.RegisterError:
            continue
        if best is None or d > best:
            best = d
    return best


def build_message(rows, baselines, previous, today, week_start=None, note=None) -> str:
    window_start = today - _dt.timedelta(days=WINDOW_DAYS - 1)
    label_day = week_start if week_start is not None else window_start
    known_ids = sorted({r.get("check_id") for r in rows if isinstance(r.get("check_id"), str)})

    open_rows = [r for r in rows if not register.is_end_state(r.get("status"))]
    n_open = len(open_rows)
    oldest = max([register.age_days(r["first_seen"], today) for r in open_rows] or [0])
    new_n = sum(1 for r in rows
                if window_start <= register.parse_date(r["first_seen"], "first_seen") <= today)
    fixed_n = 0
    for r in rows:
        if r.get("status") == "verified_fixed":
            d = _last_pass_date(r)
            if d is not None and window_start <= d <= today:
                fixed_n += 1

    # Tier 1 asks come first (the runbook says tier 1 at once), then fix packets waiting for Spencer,
    # then the other asks; never more than three.
    every_ask = register.asks(rows, len(rows), today)
    first = [r for r in every_ask if r.get("tier") == 1]
    packet_asks = [r for r in every_ask if r not in first
                   and r.get("status") == "waiting_spencer" and r.get("fix_type") == "dealeron_request"]
    ask_rows = (first + packet_asks + [r for r in every_ask if r not in first and r not in packet_asks])[:3]
    tier1_open = any(r.get("tier") == 1 for r in open_rows)

    gsc = {k: _metric_number(baselines, k, "gsc_clicks_28d") for k in ("group", "toyota", "chevy")}
    leads = _leads_number(baselines)
    prev_group = _metric_number(previous, "group", "gsc_clicks_28d") if previous is not None else None

    if not rows:
        verdict = NO_FINDINGS
    elif tier1_open:
        verdict = "A serious problem on a main page is still open."
    elif ask_rows:
        verdict = "Mostly steady, but a few things need your answer."
    elif n_open:
        verdict = "Nothing urgent; the team is working through open items."
    else:
        verdict = "All clear."
    no_numbers = all(v is None for v in gsc.values()) and leads is None
    if no_numbers and rows:
        if tier1_open:
            verdict += " The traffic and lead numbers are not available yet."
        elif ask_rows:
            verdict = "The traffic and lead numbers are not available yet, and a few things need your answer."
        elif n_open:
            verdict = "The traffic and lead numbers are not available yet; the team is working through open items."
        else:
            verdict = "The traffic and lead numbers are not available yet, so this cannot be called all clear."
    verdict += _trend(gsc["group"], prev_group)

    not_verified = _unverified_sources(baselines, gsc, leads, today)

    def build(max_words: int) -> str:
        lines = ["Motor Inn search, week of %s. %s" % (_date_label(label_day), verdict)]
        lines.append(
            "Clicks over 28 days from %s: group %s, Toyota site %s, Chevrolet site %s."
            % (GSC, _fmt(gsc["group"]), _fmt(gsc["toyota"]), _fmt(gsc["chevy"])))
        site_note = " Toyota and Chevrolet sites: not verified." if (leads is not None and _site_leads_missing(baselines)) else ""
        lines.append(
            "Organic leads from Google search, counted as form sends and phone taps in Google Analytics: %s%s.%s"
            % (_fmt(leads), _window_label(baselines, "organic_leads_total") if leads is not None else "", site_note))
        crm = _crm_number(baselines)
        if crm is None:
            lines.append("Check against our CRM: %s." % NOT_VERIFIED)
        else:
            lines.append(
                "Check against our CRM: %s website leads%s from our own sites, from any source, "
                "so this is a ceiling for organic leads, not a count of them."
                % (_fmt(crm), _window_label(baselines, "crm_website_leads")))
        lines.append(_ai_line(baselines))
        lines.append(_ai_referrals_line(baselines, today))
        if note:
            lines.append(note)
        lines.append("Fixed and confirmed on the live site since last week: %d." % fixed_n)
        if n_open:
            lines.append("New this week: %d. Open now: %d. Oldest open problem: %d %s."
                         % (new_n, n_open, oldest, _plural(oldest, "day", "days")))
        else:
            lines.append("New this week: %d. Open now: 0." % new_n)
        if ask_rows:
            for i, row in enumerate(ask_rows, 1):
                lines.append("ASK %d: %s" % (i, _ask_sentence(row, known_ids, max_words)))
        elif rows:
            lines.append(NOTHING)
        waiting = [r for r in rows
                   if r.get("fix_type") == "dealeron_request"
                   and r.get("status") in ("sent", "verify_pending")]
        sent_dates = []
        for r in waiting:
            sent = r.get("sent")
            if isinstance(sent, dict) and sent.get("at"):
                try:
                    sent_dates.append(register.parse_date(sent["at"], "sent.at"))
                except register.RegisterError:
                    pass
        if waiting and sent_dates:
            lines.append("Waiting on DealerOn: %d, oldest sent %s." % (len(waiting), _date_label(min(sent_dates))))
        else:
            lines.append("Waiting on DealerOn: %d." % len(waiting))
        if not_verified:
            lines.append("Not verified this week: %s." % ", ".join(not_verified))
        return "\n".join(lines)

    for max_words in (25, 15, 8, 3):
        text = build(max_words)
        if _words(text) <= WORD_LIMIT:
            return text
    return text


_MONTH_FILE = re.compile(r"^(\d{4})-(0[1-9]|1[0-2])\.json$")


def _load_baselines_with_fallback(path: str):
    """Load the month's baselines file. When this month's file does not exist yet, use the newest
    earlier month in the same folder and say so in the note. Returns (data, note or None)."""
    if os.path.exists(path):
        return _load_json(path, "baselines file"), None
    folder = os.path.dirname(os.path.abspath(path))
    want = _MONTH_FILE.match(os.path.basename(path))
    if not want:
        return _load_json(path, "baselines file"), None  # raises the usual refusal
    this = (int(want.group(1)), int(want.group(2)))
    best = None
    try:
        names = os.listdir(folder)
    except OSError:
        names = []
    for name in names:
        m = _MONTH_FILE.match(name)
        if m and (int(m.group(1)), int(m.group(2))) < this:
            key = (int(m.group(1)), int(m.group(2)))
            if best is None or key > best[0]:
                best = (key, name)
    if best is None:
        return _load_json(path, "baselines file"), None  # nothing earlier either: usual refusal
    data = _load_json(os.path.join(folder, best[1]), "earlier baselines file")
    note = ("The numbers above come from the %s %d file; the %s %d file has not been built yet."
            % (MONTHS[best[0][1] - 1], best[0][0], MONTHS[this[1] - 1], this[0]))
    return data, note


# ---------------------------------------------------------------------------
# Command line
# ---------------------------------------------------------------------------

def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Print the Monday search summary for Spencer. Reads files, sends nothing, changes nothing.")
    p.add_argument("--register", required=True, help="path to register.jsonl")
    p.add_argument("--baselines", required=True, help="path to the baselines JSON for this month")
    p.add_argument("--previous-baselines", default=None, help="optional earlier baselines JSON, for the click trend")
    p.add_argument("--today", default=None, help="YYYY-MM-DD (default: system date)")
    p.add_argument("--week-start", default=None, help="YYYY-MM-DD for the heading (default: 6 days before today)")
    return p


def main(argv=None, out=None) -> int:
    out = out if out is not None else sys.stdout
    args = _parser().parse_args(argv)
    try:
        today = register.resolve_today(args.today)
        week_start = register.parse_date(args.week_start, "--week-start") if args.week_start else None
        rows = _load_register(args.register)
        baselines, note = _load_baselines_with_fallback(args.baselines)
        previous = _load_json(args.previous_baselines, "earlier baselines file") if args.previous_baselines else None
        text = build_message(rows, baselines, previous, today, week_start, note)
    except SummaryError as exc:
        sys.stderr.write("%s\n" % exc)
        return 1
    except (register.RegisterError, KeyError, ValueError, TypeError, AttributeError) as exc:
        sys.stderr.write("The inputs could not be read as expected (%s). No summary was made.\n" % exc)
        return 1
    out.write(text + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
