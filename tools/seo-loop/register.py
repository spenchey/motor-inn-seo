#!/usr/bin/env python3
"""Findings register core for Motor Inn's SEO team (package SA-01).

The register is one JSON object per line in ``register.jsonl``. Each SEO problem
is recorded once (de-duplicated by fingerprint), has an owner and an age, and
cannot be marked fixed without proof. This file is both an importable module and
a command-line tool::

    python3 -I register.py --register register.jsonl add ...
    python3 -I register.py --register register.jsonl transition --id F-... --to triaged
    python3 -I register.py --register register.jsonl approve --by coordinator ...
    python3 -I register.py --register register.jsonl render
    python3 -I register.py --register register.jsonl asks --max 3
    python3 -I register.py --register register.jsonl validate

Standard library only, Python 3.9. Allowed values come from ``schema.json``
beside this file. No network code lives here.
"""
from __future__ import annotations

import argparse
import copy
import datetime as _dt
import hashlib
import json
import os
import re
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:  # advisory lock around read-modify-write; absent on some platforms
    import fcntl as _fcntl
except ImportError:  # pragma: no cover
    _fcntl = None

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(HERE, "schema.json")


class RegisterError(Exception):
    """A rule was broken. The register file is left untouched."""


# ---------------------------------------------------------------------------
# Schema (single source of allowed values)
# ---------------------------------------------------------------------------

def load_schema(path: str = SCHEMA_PATH) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


SCHEMA = load_schema()
FIELD_ORDER = list(SCHEMA["field_order"])
REQUIRED = list(SCHEMA["required"])
NEXT_ACTION_FIELDS = list(SCHEMA["required_unless_end_state"])
END_STATES = frozenset(SCHEMA["end_states"])
SITES = list(SCHEMA["enums"]["site"])
BRANDS = list(SCHEMA["enums"]["brand"])
TIERS = list(SCHEMA["enums"]["tier"])
FIX_TYPES = list(SCHEMA["enums"]["fix_type"])
STATUSES = list(SCHEMA["enums"]["status"])
VERIFY_TYPES = list(SCHEMA["enums"]["verify_type"])
APPROVAL_DECISIONS = list(SCHEMA["enums"]["approval_decision"])
APPROVER = SCHEMA["approval_rules"]["approver"]
APPROVAL_RECORDER = SCHEMA["approval_rules"]["recorded_by"]
APPROVAL_QUOTE_SOURCE = SCHEMA["approval_rules"]["quote_source"]
ALLOWED_WHERE = list(SCHEMA["approval_rules"]["allowed_where"])
PASSES_REQUIRED = int(SCHEMA["verification_rules"]["passes_required"])
MIN_HOURS_APART = float(SCHEMA["verification_rules"]["min_hours_apart"])
FAIL_TWICE_LIMIT = int(SCHEMA["fail_twice_limit"])
OVERDUE_DAYS = int(SCHEMA["verification_rules"]["overdue_days"])
EVIDENCE_DIR = SCHEMA["verification_rules"]["evidence_dir"]
TRIAGE_DEADLINE_DAYS = 7

# ---------------------------------------------------------------------------
# The one table of allowed status transitions
# ---------------------------------------------------------------------------

TRANSITIONS = {
    "new": {"triaged", "wont_fix", "blocked"},
    "triaged": {"packet_ready", "wont_fix", "blocked"},
    "packet_ready": {"waiting_spencer", "triaged", "wont_fix", "blocked"},
    "waiting_spencer": {"sent", "packet_ready", "wont_fix", "blocked"},
    "sent": {"verify_pending", "reopened", "blocked"},
    "verify_pending": {"verified_fixed", "reopened", "blocked"},
    "verified_fixed": {"reopened"},  # a regression
    "reopened": {"triaged", "packet_ready", "waiting_spencer", "wont_fix", "blocked"},
    "wont_fix": {"reopened"},  # Spencer changes his mind
    "blocked": {"triaged", "packet_ready", "waiting_spencer", "wont_fix"},
}

# Moving out of these states into "reopened" counts as a failed fix attempt.
_FAILED_ATTEMPT_FROM = frozenset({"sent", "verify_pending"})
# States that follow a send: they need a "fix" approval on the row.
SENT_STATES = frozenset({"sent", "verify_pending", "verified_fixed"})


def _check_tables() -> None:
    known = set(STATUSES)
    if set(TRANSITIONS) != known:
        raise RuntimeError("TRANSITIONS keys differ from schema.json statuses")
    for src, dsts in TRANSITIONS.items():
        if not dsts <= known:
            raise RuntimeError("TRANSITIONS[%s] has a status not in schema.json" % src)
    if not END_STATES <= known:
        raise RuntimeError("schema.json end_states not in statuses")


_check_tables()

# ---------------------------------------------------------------------------
# Dates and small helpers
# ---------------------------------------------------------------------------

_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_CHECK_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
_URL_RE = re.compile(r"^(https?)://([^/?#]*)([^?#]*)", re.IGNORECASE)


def parse_date(value, what: str = "date") -> _dt.date:
    if isinstance(value, _dt.date) and not isinstance(value, _dt.datetime):
        return value
    if not isinstance(value, str) or not _DATE_RE.match(value):
        raise RegisterError("%s must be YYYY-MM-DD, got %r" % (what, value))
    try:
        return _dt.date.fromisoformat(value)
    except ValueError:
        raise RegisterError("%s is not a real date: %r" % (what, value))


def resolve_today(today=None) -> _dt.date:
    """Injectable 'today'. The wall clock is read only when nothing is passed."""
    if today is None:
        return _dt.date.today()
    return parse_date(today, "today")


def now_utc(now=None, today=None) -> _dt.datetime:
    """Injectable clock. `now` wins; else a given `today` means 00:00 UTC of that
    day (replay mode); else the wall clock."""
    if now is not None:
        return parse_timestamp(now, "now")
    if today is not None:
        return parse_timestamp(resolve_today(today).isoformat(), "today")
    return _dt.datetime.now(_dt.timezone.utc)


def iso_z(dt: _dt.datetime) -> str:
    return dt.astimezone(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_timestamp(value, what: str = "timestamp") -> _dt.datetime:
    """ISO-8601 date-time; a trailing Z or no zone means UTC."""
    if isinstance(value, _dt.datetime):
        dt = value
    else:
        if not isinstance(value, str) or not value.strip():
            raise RegisterError("%s must be an ISO-8601 timestamp, got %r" % (what, value))
        text = value.strip()
        if text.endswith(("Z", "z")):
            text = text[:-1] + "+00:00"
        if _DATE_RE.match(text):
            text += "T00:00:00+00:00"
        try:
            dt = _dt.datetime.fromisoformat(text)
        except ValueError:
            raise RegisterError("%s is not an ISO-8601 timestamp: %r" % (what, value))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=_dt.timezone.utc)
    return dt


def _nonempty(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def age_days(first_seen: str, today=None) -> int:
    return max(0, (resolve_today(today) - parse_date(first_seen, "first_seen")).days)


def is_end_state(status: str) -> bool:
    return status in END_STATES


# ---------------------------------------------------------------------------
# Fingerprint and ID
# ---------------------------------------------------------------------------

def normalise_target(target: str) -> str:
    """URL targets: path lower-cased; query string, fragment and trailing slash
    removed (scheme and host are lower-cased too). A bare root path stays "/".
    Anything else (a listing ID) is only stripped of surrounding space."""
    if not isinstance(target, str):
        raise RegisterError("target must be a string")
    text = target.strip()
    if not text:
        raise RegisterError("target must not be empty")
    m = _URL_RE.match(text)
    if m:
        path = m.group(3).lower().rstrip("/")
        return "%s://%s%s" % (m.group(1).lower(), m.group(2).lower(), path)
    if text.startswith("/"):
        path = re.split(r"[?#]", text, 1)[0].lower().rstrip("/")
        return path or "/"
    return text


def make_fingerprint(site: str, surface: str, check_id: str, target: str) -> str:
    raw = "%s|%s|%s|%s" % (site, surface, check_id, normalise_target(target))
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()


def wording_hash(row: dict) -> str:
    """sha256 of title|target|expected: what Spencer approved."""
    raw = "%s|%s|%s" % (row.get("title"), row.get("target"), row.get("expected"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def make_id(site: str, check_id: str, fingerprint: str) -> str:
    return "F-%s-%s-%s" % (site, check_id, fingerprint[:6])


# ---------------------------------------------------------------------------
# Test registers and evidence files
# ---------------------------------------------------------------------------

def _temp_roots() -> list:
    roots = []
    for cand in (tempfile.gettempdir(), "/tmp", "/var/tmp"):
        real = os.path.realpath(cand)
        if real not in roots:
            roots.append(real)
    return roots


def is_test_register(path: str) -> bool:
    """True when `path` may be used with --test-mode. A register under a
    /findings/ folder is production-style, and so is any file named
    register.jsonl that is not inside a temp folder. Names are compared in lower
    case, so FINDINGS/REGISTER.JSONL is production too (macOS paths do not care
    about case). Shared with verify_fix.py."""
    real = os.path.realpath(path).replace(os.sep, "/").lower()
    if "/findings/" in real:
        return False
    if os.path.basename(real) == "register.jsonl":
        roots = [r.replace(os.sep, "/").lower() for r in _temp_roots()]
        return any(real == r or real.startswith(r + "/") for r in roots)
    return True


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def resolve_evidence(base_dir: str, evidence_path) -> str:
    """Absolute path of an evidence file. It must be a relative path under the
    register's evidence/ folder, with no '..' that escapes it. Raises RegisterError."""
    if not _nonempty(evidence_path):
        raise RegisterError("an evidence path is required")
    rel = evidence_path.strip()
    norm = os.path.normpath(rel)
    if os.path.isabs(rel) or norm.startswith("..") or not norm.startswith(EVIDENCE_DIR + os.sep):
        raise RegisterError("evidence path %r must be a relative path under %s/" % (evidence_path, EVIDENCE_DIR))
    root = os.path.realpath(os.path.join(base_dir, EVIDENCE_DIR))
    full = os.path.realpath(os.path.join(base_dir, norm))
    if not full.startswith(root + os.sep):
        raise RegisterError("evidence path %r leaves the %s/ folder" % (evidence_path, EVIDENCE_DIR))
    return full


def check_evidence_file(base_dir: str, evidence_path, evidence_sha256) -> str:
    """Return "" if the file exists under base_dir/evidence/ and matches the hash."""
    if not isinstance(evidence_sha256, str) or not re.match(r"^[0-9a-f]{64}$", evidence_sha256):
        return "evidence_sha256 is missing or not a sha256"
    try:
        full = resolve_evidence(base_dir, evidence_path)
    except RegisterError as exc:
        return str(exc)
    if not os.path.isfile(full):
        return "evidence file %s is missing" % evidence_path
    if sha256_file(full) != evidence_sha256:
        return "evidence file %s does not match its recorded hash" % evidence_path
    return ""


# ---------------------------------------------------------------------------
# File I/O (atomic)
# ---------------------------------------------------------------------------

def load_rows(path: str, must_exist: bool = True) -> list:
    if not os.path.exists(path):
        if must_exist:
            raise RegisterError("register file not found: %s" % path)
        return []
    rows = []
    with open(path, "r", encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except ValueError as exc:
                raise RegisterError("%s line %d is not valid JSON: %s" % (path, n, exc))
            if not isinstance(row, dict):
                raise RegisterError("%s line %d is not a JSON object" % (path, n))
            rows.append(row)
    return rows


def _ordered(row: dict) -> dict:
    out = {k: row[k] for k in FIELD_ORDER if k in row}
    for k in row:
        if k not in out:
            out[k] = row[k]
    return out


def atomic_write_text(path: str, text: str) -> None:
    """Temporary file in the same folder, fsync, then os.replace."""
    folder = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(prefix=".tmp-", suffix=".part", dir=folder)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def save_rows(path: str, rows: list) -> None:
    text = "".join(json.dumps(_ordered(r), ensure_ascii=False) + "\n" for r in rows)
    atomic_write_text(path, text)


class _Locked(object):
    """Advisory lock on '<register>.lock' for read-modify-write commands."""

    def __init__(self, path: str):
        self.path = path + ".lock"
        self.fh = None

    def __enter__(self):
        if _fcntl is not None:
            self.fh = open(self.path, "a")
            _fcntl.flock(self.fh, _fcntl.LOCK_EX)
        return self

    def __exit__(self, *exc):
        if self.fh is not None:
            try:
                _fcntl.flock(self.fh, _fcntl.LOCK_UN)
            finally:
                self.fh.close()
        return False


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

PASSING_HEX = re.compile(r"^[0-9a-f]{64}$")


def passing_times(verified) -> list:
    """Timestamps of the passing reads in `verified` (raises RegisterError on a bad stamp)."""
    out = []
    if isinstance(verified, dict) and isinstance(verified.get("passes"), list):
        for entry in verified["passes"]:
            if isinstance(entry, dict) and entry.get("passed") is True:
                out.append(parse_timestamp(entry.get("at"), "verified.passes.at"))
    return out


def sent_moment(sent):
    """The exact send time: sent.sent_at, else the sent.at date at 00:00 UTC."""
    if not isinstance(sent, dict):
        raise RegisterError("sent is missing")
    stamp = sent.get("sent_at") or sent.get("at")
    return parse_timestamp(stamp, "sent.sent_at")


def check_passes(verified, sent=None, verify=None) -> str:
    """Return "" if `verified` holds two real passing reads, both at or after the
    send moment and at least 24 h apart; else a plain-English reason. Every
    counted read needs an evidence path; reads on a manual rule need to have
    been recorded by the coordinator."""
    if not isinstance(sent, dict) or not (_nonempty(sent.get("at")) or _nonempty(sent.get("sent_at"))):
        return "sent is missing, so no read can be shown to follow the fix"
    try:
        sent_at = sent_moment(sent)
    except RegisterError as exc:
        return str(exc)
    if not isinstance(verified, dict):
        return "verified is missing"
    passes = verified.get("passes")
    if not isinstance(passes, list):
        return "verified.passes is not a list"
    manual = isinstance(verify, dict) and verify.get("type") == "manual"
    times = []
    for entry in passes:
        if not (isinstance(entry, dict) and entry.get("passed") is True):
            continue
        try:
            t = parse_timestamp(entry.get("at"), "verified.passes.at")
        except RegisterError as exc:
            return str(exc)
        if t < sent_at:
            continue
        if not _nonempty(entry.get("evidence_path")):
            continue
        if not re.match(r"^[0-9a-f]{64}$", str(entry.get("evidence_sha256"))):
            continue
        if manual and entry.get("by") != APPROVAL_RECORDER:
            continue
        times.append(t)
    if len(times) < PASSES_REQUIRED:
        return "needs %d passing reads with evidence, has %d" % (PASSES_REQUIRED, len(times))
    times.sort()
    gap = (times[-1] - times[0]).total_seconds() / 3600.0
    if gap < MIN_HOURS_APART:
        return "passing reads are %.1f hours apart, need at least %d" % (gap, MIN_HOURS_APART)
    return ""


def check_approval(approval, decision=None) -> str:
    """Return "" if `approval` is a well-formed Spencer approval (and, when
    `decision` is given, an approval for that decision), else a reason."""
    if not isinstance(approval, dict):
        return "approval is missing"
    if approval.get("decision") not in APPROVAL_DECISIONS:
        return "approval has no decision (%s)" % " or ".join(APPROVAL_DECISIONS)
    if decision is not None and approval["decision"] != decision:
        return "approval is for decision %r, not %r" % (approval["decision"], decision)
    if approval.get("recorded_by") != APPROVAL_RECORDER:
        return "approval was not recorded by the coordinator"
    by = approval.get("by")
    if not _nonempty(by) or by.strip().lower() != APPROVER.lower():
        return "approval is not from %s" % APPROVER
    where = approval.get("where")
    if not _nonempty(where):
        return "approval has no 'where'"
    if where not in ALLOWED_WHERE:
        return "approval 'where' must be exactly one of %s" % ", ".join(ALLOWED_WHERE)
    if not isinstance(approval.get("approved_hash"), str) or not PASSING_HEX.match(approval["approved_hash"]):
        return "approval has no approved_hash"
    if not _nonempty(approval.get("quote")):
        return "approval has no quote"
    if approval.get("quote_source") != APPROVAL_QUOTE_SOURCE:
        return "approval quote is not from Spencer's own message"
    try:
        parse_timestamp(approval.get("when"), "approval.when")
    except RegisterError as exc:
        return str(exc)
    return ""


def validate_row(row: dict) -> list:
    """Return a list of problems (empty list means the row is valid)."""
    errs = []
    if not isinstance(row, dict):
        return ["row is not an object"]
    for key in REQUIRED:
        if key not in row or row[key] is None or (isinstance(row[key], str) and not row[key].strip()):
            errs.append("missing required field '%s'" % key)
    for key in SCHEMA["nullable"]:
        if key not in row:
            errs.append("missing field '%s' (use null)" % key)

    def enum(key, allowed):
        if key in row and row[key] is not None and row[key] not in allowed:
            errs.append("%s=%r is not one of %s" % (key, row[key], allowed))

    enum("site", SITES)
    enum("brand", BRANDS)
    enum("fix_type", FIX_TYPES)
    enum("status", STATUSES)
    tier = row.get("tier")
    if tier is not None and (isinstance(tier, bool) or tier not in TIERS):
        errs.append("tier=%r is not one of %s" % (tier, TIERS))
    for key in ("seen_count", "age_days", "regressions", "failed_fix_attempts"):
        v = row.get(key)
        if v is not None and (isinstance(v, bool) or not isinstance(v, int) or v < 0):
            errs.append("%s must be a non-negative integer" % key)
    if isinstance(row.get("seen_count"), int) and row["seen_count"] < 1:
        errs.append("seen_count must be at least 1")
    for key in ("first_seen", "last_seen"):
        if row.get(key) is not None:
            try:
                parse_date(row[key], key)
            except RegisterError as exc:
                errs.append(str(exc))
    try:
        if parse_date(row["first_seen"]) > parse_date(row["last_seen"]):
            errs.append("first_seen is after last_seen")
    except (RegisterError, KeyError):
        pass
    if not isinstance(row.get("sources"), list) or not all(isinstance(s, str) for s in row.get("sources", [])):
        errs.append("sources must be a list of strings")
    cid = row.get("check_id")
    if isinstance(cid, str) and not _CHECK_ID_RE.match(cid):
        errs.append("check_id %r must be lower-case letters, digits and hyphens" % cid)

    # fingerprint and id must follow from the identity fields
    if all(_nonempty(row.get(k)) for k in ("site", "surface", "check_id", "target", "fingerprint", "id")):
        try:
            fp = make_fingerprint(row["site"], row["surface"], row["check_id"], row["target"])
            if row["target"] != normalise_target(row["target"]):
                errs.append("target is not normalised")
            if row["fingerprint"] != fp:
                errs.append("fingerprint does not match site|surface|check_id|target")
            if row["id"] != make_id(row["site"], row["check_id"], row["fingerprint"]):
                errs.append("id does not match F-<site>-<check_id>-<fingerprint[:6]>")
        except RegisterError as exc:
            errs.append(str(exc))

    status = row.get("status")
    if status not in END_STATES:
        for key in NEXT_ACTION_FIELDS:
            if not _nonempty(row.get(key)):
                errs.append("%s is required while status is %r" % (key, status))
        if _nonempty(row.get("next_action_due")):
            try:
                parse_date(row["next_action_due"], "next_action_due")
            except RegisterError as exc:
                errs.append(str(exc))

    if row.get("approval") is not None:
        reason = check_approval(row["approval"])
        if reason:
            errs.append("approval invalid: " + reason)
    if status == "wont_fix":
        reason = check_approval(row.get("approval"), "wont_fix")
        if reason:
            errs.append("wont_fix needs a wont_fix approval: " + reason)
    if status in SENT_STATES:
        reason = check_approval(row.get("approval"), "fix")
        if reason:
            errs.append("status %s needs a fix approval: %s" % (status, reason))
        elif row["approval"].get("approved_hash") != wording_hash(row):
            errs.append("approval does not match the current title, target and expected wording")
        elif _nonempty(row.get("waiting_since")):
            try:
                if parse_timestamp(row["approval"]["when"]) < parse_timestamp(row["waiting_since"]):
                    errs.append("approval is older than waiting_since")
            except RegisterError as exc:
                errs.append(str(exc))
    if status == "waiting_spencer":
        try:
            parse_timestamp(row.get("waiting_since"), "waiting_since")
        except RegisterError:
            errs.append("waiting_since is required while status is waiting_spencer")
    if row.get("waiting_since") is not None:
        try:
            parse_timestamp(row["waiting_since"], "waiting_since")
        except RegisterError as exc:
            errs.append(str(exc))
    if status == "verified_fixed":
        reason = check_passes(row.get("verified"), row.get("sent"), row.get("verify"))
        if reason:
            errs.append("verified_fixed without proof: " + reason)
    if row.get("verified") is not None:
        v = row["verified"]
        if not isinstance(v, dict) or not isinstance(v.get("passes"), list):
            errs.append("verified must be {at, evidence_path, passes[]}")
        else:
            for i, p in enumerate(v["passes"]):
                if not isinstance(p, dict) or not _nonempty(p.get("evidence_path")) \
                        or not re.match(r"^[0-9a-f]{64}$", str(p.get("evidence_sha256"))):
                    errs.append("verified.passes[%d] needs evidence_path and evidence_sha256" % i)
    if row.get("overdue_since") is not None:
        try:
            parse_timestamp(row["overdue_since"], "overdue_since")
        except RegisterError as exc:
            errs.append(str(exc))
    if row.get("verify") is not None:
        v = row["verify"]
        if not isinstance(v, dict) or v.get("type") not in VERIFY_TYPES:
            errs.append("verify.type must be one of %s" % VERIFY_TYPES)
    if row.get("sent") is not None and not isinstance(row["sent"], dict):
        errs.append("sent must be an object or null")
    elif isinstance(row.get("sent"), dict) and row["sent"].get("sent_at") is not None:
        try:
            parse_timestamp(row["sent"]["sent_at"], "sent.sent_at")
        except RegisterError as exc:
            errs.append(str(exc))
    return errs


def validate_rows(rows: list, base_dir=None) -> list:
    """Return (label, problem) pairs for every bad row, plus register-level ones.
    With `base_dir` (the register's folder) every recorded pass must also point
    at an existing evidence file whose sha256 matches."""
    bad = []
    seen_ids, seen_fps = {}, {}
    for n, row in enumerate(rows, 1):
        label = row.get("id") if isinstance(row, dict) and row.get("id") else "line %d" % n
        for problem in validate_row(row):
            bad.append((label, problem))
        if base_dir is not None and isinstance(row, dict) and isinstance(row.get("verified"), dict):
            for i, p in enumerate(row["verified"].get("passes") or []):
                if isinstance(p, dict):
                    reason = check_evidence_file(base_dir, p.get("evidence_path"), p.get("evidence_sha256"))
                    if reason:
                        bad.append((label, "verified.passes[%d]: %s" % (i, reason)))
        if isinstance(row, dict):
            if row.get("id") in seen_ids:
                bad.append((label, "duplicate id (also line %d)" % seen_ids[row["id"]]))
            seen_ids.setdefault(row.get("id"), n)
            if row.get("fingerprint") in seen_fps:
                bad.append((label, "duplicate fingerprint (also line %d)" % seen_fps[row["fingerprint"]]))
            seen_fps.setdefault(row.get("fingerprint"), n)
    return bad


# ---------------------------------------------------------------------------
# Operations (pure: they take and return rows; the CLI does the file I/O)
# ---------------------------------------------------------------------------

def find_row(rows: list, row_id: str) -> dict:
    for row in rows:
        if row.get("id") == row_id:
            return row
    raise RegisterError("no such finding: %s" % row_id)


def _due(today: _dt.date, days: int = TRIAGE_DEADLINE_DAYS) -> str:
    return (today + _dt.timedelta(days=days)).isoformat()


def add_finding(rows, *, site, surface, check_id, target, today=None, brand=None, tier=None,
                title=None, observed=None, expected=None, owner=None, fix_type=None,
                source=None, next_action=None, next_action_owner=None, next_action_due=None,
                verify=None):
    """Create a finding, or re-sight an existing one with the same fingerprint.

    Mutates `rows` and returns (row, outcome) where outcome is "created",
    "resighted" or "reopened"."""
    day = resolve_today(today)
    if site not in SITES:
        raise RegisterError("site must be one of %s" % SITES)
    if not _nonempty(surface):
        raise RegisterError("surface is required")
    if not isinstance(check_id, str) or not _CHECK_ID_RE.match(check_id):
        raise RegisterError("check_id must be lower-case letters, digits and hyphens")
    norm = normalise_target(target)
    fp = make_fingerprint(site, surface.strip(), check_id, norm)

    existing = None
    for row in rows:
        if row.get("fingerprint") == fp:
            existing = row
            break

    if existing is not None:
        row = existing
        row["seen_count"] = int(row.get("seen_count", 0)) + 1
        if _nonempty(source) and source not in row.setdefault("sources", []):
            row["sources"].append(source)
        if row.get("status") == "verified_fixed":
            try:
                reads = passing_times(row.get("verified"))
            except RegisterError:
                reads = []
            if reads and day <= max(reads).date():
                # the report predates the fix: count it, nothing else
                return row, "resighted"
        row["last_seen"] = max(parse_date(row["last_seen"], "last_seen"), day).isoformat()
        if _nonempty(observed):
            row["observed"] = observed
        row["age_days"] = age_days(row["first_seen"], day)
        outcome = "resighted"
        if row.get("status") == "verified_fixed":
            row["status"] = "reopened"
            row["regressions"] = int(row.get("regressions", 0)) + 1
            row["failed_fix_attempts"] = 0
            row["verified"] = None
            row["sent"] = None
            row["approval"] = None
            row["next_action"] = next_action or "Re-triage: the fix did not hold"
            row["next_action_owner"] = next_action_owner or "rory"
            row["next_action_due"] = next_action_due or _due(day)
            outcome = "reopened"
        problems = validate_row(row)
        if problems:
            raise RegisterError("; ".join(problems))
        return row, outcome

    missing = [k for k, v in (("brand", brand), ("tier", tier), ("title", title), ("observed", observed),
                              ("expected", expected), ("fix_type", fix_type)) if v in (None, "")]
    if missing:
        raise RegisterError("a new finding needs: %s" % ", ".join(missing))
    if isinstance(tier, str) and tier.isdigit():
        tier = int(tier)
    row = {
        "id": make_id(site, check_id, fp),
        "fingerprint": fp,
        "site": site,
        "brand": brand,
        "tier": tier,
        "title": title,
        "observed": observed,
        "expected": expected,
        "first_seen": day.isoformat(),
        "last_seen": day.isoformat(),
        "seen_count": 1,
        "age_days": 0,
        "owner": owner or "rory",
        "fix_type": fix_type,
        "status": "new",
        "next_action": next_action or "Triage: set tier, owner, fix type and next action",
        "next_action_owner": next_action_owner or "rory",
        "next_action_due": next_action_due or _due(day),
        "approval": None,
        "sent": None,
        "verify": verify,
        "verified": None,
        "sources": [source] if _nonempty(source) else [],
        "check_id": check_id,
        "surface": surface.strip(),
        "target": norm,
        "regressions": 0,
        "failed_fix_attempts": 0,
        "waiting_since": None,
        "overdue_since": None,
    }
    problems = validate_row(row)
    if problems:
        raise RegisterError("; ".join(problems))
    rows.append(row)
    return row, "created"


# Moves that keep a "fix" approval alive: the send itself and its verification.
_KEEP_APPROVAL = frozenset({("sent", "verify_pending"), ("verify_pending", "verified_fixed")})


def transition(rows, row_id, to, *, today=None, now=None, next_action=None, next_action_owner=None,
               next_action_due=None, sent_how=None):
    """Change a row's status through the allowed-transition table. Returns the
    updated row. The row's final status can differ from `to`: a second failed
    fix attempt lands in "blocked". `now` (ISO-8601) is the moment recorded as
    `sent.sent_at` and `waiting_since`."""
    day = resolve_today(today)
    moment = now_utc(now, today)
    if now is not None:
        day = moment.date()
    if to not in STATUSES:
        raise RegisterError("unknown status %r" % to)
    row = find_row(rows, row_id)
    old = row["status"]
    if to not in TRANSITIONS.get(old, set()):
        raise RegisterError("illegal transition %s -> %s (allowed: %s)"
                            % (old, to, ", ".join(sorted(TRANSITIONS.get(old, set()))) or "none"))
    new = copy.deepcopy(row)
    if to == "wont_fix":
        reason = check_approval(new.get("approval"), "wont_fix")
        if reason:
            raise RegisterError("wont_fix refused: " + reason)
    if to == "sent":
        appr = new.get("approval")
        reason = check_approval(appr, "fix")
        if reason:
            raise RegisterError("sent refused: " + reason)
        if appr.get("approved_hash") != wording_hash(new):
            raise RegisterError("sent refused: the title, target or expected wording changed after approval")
        try:
            since = parse_timestamp(new.get("waiting_since"), "waiting_since")
        except RegisterError:
            raise RegisterError("sent refused: the row has no waiting_since")
        if parse_timestamp(appr["when"]) < since:
            raise RegisterError("sent refused: the approval is older than the move into waiting_spencer")
        if moment < parse_timestamp(appr["when"]):
            raise RegisterError("sent refused: the send is timed before its approval")
    if to == "packet_ready" and int(new.get("tier", 0)) == 4:
        if any(r is not row and r.get("tier") in (1, 2) and not is_end_state(r.get("status")) for r in rows):
            raise RegisterError("packet_ready refused: a tier 4 row waits while any tier 1 or 2 row is open")
    if to == "verified_fixed":
        reason = check_passes(new.get("verified"), new.get("sent"), new.get("verify"))
        if reason:
            raise RegisterError("verified_fixed refused: " + reason)

    final = to
    if to == "reopened":
        if old == "verified_fixed":
            new["regressions"] = int(new.get("regressions", 0)) + 1
            new["failed_fix_attempts"] = 0
            new["verified"] = None
        elif old in _FAILED_ATTEMPT_FROM:
            new["failed_fix_attempts"] = int(new.get("failed_fix_attempts", 0)) + 1
            if new["failed_fix_attempts"] >= FAIL_TWICE_LIMIT:
                final = "blocked"
    if to == "reopened":
        new["approval"] = None  # approval is per action
    if old in _FAILED_ATTEMPT_FROM and (old, to) not in _KEEP_APPROVAL:
        new["approval"] = None  # leaving sent or verify_pending ends that action
    if to in ("reopened", "blocked") and old in _FAILED_ATTEMPT_FROM:
        new["verified"] = None
    if final == "blocked" and old in _FAILED_ATTEMPT_FROM:
        new["verified"] = None
    if to == "sent":
        new["sent"] = {"at": moment.date().isoformat(),
                       "sent_at": iso_z(moment), "how": sent_how or "not recorded"}
        new["verified"] = None
    if to == "waiting_spencer":
        new["waiting_since"] = iso_z(moment)
    if (old, to) != ("sent", "verify_pending"):
        new["overdue_since"] = None  # a new state is a new clock

    new["status"] = final
    defaults = {}
    if final == "blocked":
        fails = int(new.get("failed_fix_attempts", 0))
        what = ("%d fix attempts failed" % fails) if fails else "finding is blocked"
        defaults = {"next_action": "Spencer decision: %s" % what,
                    "next_action_owner": "spencer", "next_action_due": _due(day)}
    elif final == "reopened":
        defaults = {"next_action": "Re-triage: the fix did not hold", "next_action_owner": "rory",
                    "next_action_due": _due(day)}
    given = {"next_action": next_action, "next_action_owner": next_action_owner,
             "next_action_due": next_action_due}
    for key in NEXT_ACTION_FIELDS:
        if given[key]:
            new[key] = given[key]
        elif key in defaults:
            new[key] = defaults[key]
    new["age_days"] = age_days(new["first_seen"], day)
    problems = validate_row(new)
    if problems:
        raise RegisterError("%s -> %s refused: %s" % (old, to, "; ".join(problems)))
    row.clear()
    row.update(new)
    return row


def _add_read(row, entry):
    v = row.get("verified")
    if not isinstance(v, dict):
        v = {"at": None, "evidence_path": None, "passes": []}
    passes = [p for p in v.get("passes", []) if isinstance(p, dict)]
    if not any(p.get("at") == entry["at"] for p in passes):
        passes.append(entry)
    v["passes"] = passes
    v["at"] = entry["at"]
    v["evidence_path"] = entry["evidence_path"]
    row["verified"] = v


def _read_common(rows, row_id, at, evidence_path, now, today, who):
    at_dt = parse_timestamp(at, "at")
    if not _nonempty(evidence_path):
        raise RegisterError("%s refused: an evidence path is required" % who)
    if at_dt > now_utc(now, today):
        raise RegisterError("%s refused: the read time is in the future" % who)
    row = find_row(rows, row_id)
    if row.get("status") not in _FAILED_ATTEMPT_FROM:
        raise RegisterError("%s refused: status is %r, reads count only while sent or verify_pending"
                            % (who, row.get("status")))
    return row


def record_read(rows, row_id, at, evidence_path=None, evidence_sha256=None, now=None, today=None,
                base_dir=None):
    """Append one passing automatic read to `verified.passes`. In-process only
    (there is no command-line route): `verify_fix.py` calls it after saving the
    evidence file. Needs the evidence path and its sha256, and a time that is not
    in the future. Refused on manual (or missing) rules: use `record_manual_check`.
    With `base_dir` (the register's folder) the file must exist and match."""
    row = _read_common(rows, row_id, at, evidence_path, now, today, "record_read")
    rule = row.get("verify")
    if not isinstance(rule, dict) or rule.get("type") in (None, "manual"):
        raise RegisterError("record_read refused: the row has no machine rule; a manual rule needs "
                            "record_manual_check")
    if not isinstance(evidence_sha256, str) or not re.match(r"^[0-9a-f]{64}$", evidence_sha256):
        raise RegisterError("record_read refused: evidence_sha256 is required")
    if base_dir is not None:
        reason = check_evidence_file(base_dir, evidence_path, evidence_sha256)
        if reason:
            raise RegisterError("record_read refused: " + reason)
    _add_read(row, {"at": at.strip(), "passed": True, "evidence_path": evidence_path.strip(),
                    "evidence_sha256": evidence_sha256})
    return row


def record_manual_check(rows, row_id, evidence_path, by="coordinator", now=None, today=None,
                        base_dir=None):
    """Record a person's check on a `manual` rule, on a `sent` or `verify_pending`
    row. Coordinator only. The check is timed by the clock (there is no way to
    give a time except `now` in tests), and a second check less than 24 hours
    after the previous one on the row is refused. The evidence must be an
    existing file under `base_dir`/evidence/ (base_dir is the register's
    folder); its hash is stored."""
    if by != APPROVAL_RECORDER:
        raise RegisterError("record_manual_check refused: --by must be %s" % APPROVAL_RECORDER)
    moment = now_utc(now, today)
    at = iso_z(moment)
    row = _read_common(rows, row_id, at, evidence_path, now, today, "record_manual_check")
    previous = None
    verified = row.get("verified")
    for p in (verified.get("passes") if isinstance(verified, dict) else None) or []:
        if isinstance(p, dict) and p.get("by") == APPROVAL_RECORDER and p.get("passed") is True:
            t = parse_timestamp(p.get("at"), "verified.passes.at")
            if previous is None or t > previous:
                previous = t
    if previous is not None and moment - previous < _dt.timedelta(hours=MIN_HOURS_APART):
        raise RegisterError("record_manual_check refused: the previous manual check was less than %d hours ago"
                            % MIN_HOURS_APART)
    rule = row.get("verify")
    if not isinstance(rule, dict) or rule.get("type") != "manual":
        raise RegisterError("record_manual_check refused: the row's rule is not manual")
    if base_dir is None:
        raise RegisterError("record_manual_check refused: the register folder is needed to find the evidence file")
    try:
        full = resolve_evidence(base_dir, evidence_path)
    except RegisterError as exc:
        raise RegisterError("record_manual_check refused: %s" % exc)
    if not os.path.isfile(full):
        raise RegisterError("record_manual_check refused: evidence file %s does not exist" % evidence_path)
    _add_read(row, {"at": at, "passed": True, "evidence_path": evidence_path.strip(),
                    "evidence_sha256": sha256_file(full), "by": APPROVAL_RECORDER})
    return row


def clear_reads(rows, row_id):
    """Remove every recorded read. Not allowed on a verified_fixed row (reopen it first)."""
    row = find_row(rows, row_id)
    if row.get("status") == "verified_fixed":
        raise RegisterError("clear_reads refused: the finding is verified_fixed; reopen it instead")
    row["verified"] = None
    return row


def approve(rows, row_id, *, decision=None, by=None, approver=None, where=None, when=None, quote=None,
            quote_source=None, now=None, today=None):
    """Record Spencer's approval. The only code path that writes `approval`.

    A `fix` approval can be recorded only while the row is waiting_spencer, and
    its time may not be in the future or earlier than `waiting_since`. A
    `wont_fix` approval works from any non-end state. The approval stores a hash
    of the title, target and expected wording it covers."""
    if by != APPROVAL_RECORDER:
        raise RegisterError("approval refused: --by must be %s" % APPROVAL_RECORDER)
    if decision not in APPROVAL_DECISIONS:
        raise RegisterError("approval refused: --decision must be one of %s" % ", ".join(APPROVAL_DECISIONS))
    if not _nonempty(approver) or approver.strip().lower() != APPROVER.lower():
        raise RegisterError("approval refused: approver must be %s" % APPROVER)
    if where not in ALLOWED_WHERE:
        raise RegisterError("approval refused: --where must be exactly one of %s" % ", ".join(ALLOWED_WHERE))
    if not _nonempty(when):
        raise RegisterError("approval refused: --when is required")
    when_dt = parse_timestamp(when, "--when")
    if when_dt > now_utc(now, today):
        raise RegisterError("approval refused: --when is in the future")
    if not _nonempty(quote):
        raise RegisterError("approval refused: --quote must be Spencer's own words and not empty")
    if quote_source != APPROVAL_QUOTE_SOURCE:
        raise RegisterError("approval refused: --quote-source must be %s (relayed approvals are not accepted)"
                            % APPROVAL_QUOTE_SOURCE)
    row = find_row(rows, row_id)
    if is_end_state(row.get("status")):
        raise RegisterError("approval refused: the finding is already %s" % row.get("status"))
    if decision == "wont_fix" and row.get("status") in _FAILED_ATTEMPT_FROM:
        raise RegisterError("approval refused: a wont_fix approval cannot replace the fix approval on a row "
                            "that is %s" % row.get("status"))
    if decision == "fix":
        if row.get("status") != "waiting_spencer":
            raise RegisterError("approval refused: a fix approval is recorded only while the row is "
                                "waiting_spencer, not %r" % row.get("status"))
        try:
            since = parse_timestamp(row.get("waiting_since"), "waiting_since")
        except RegisterError:
            raise RegisterError("approval refused: the row has no waiting_since")
        if when_dt < since:
            raise RegisterError("approval refused: --when is earlier than the move into waiting_spencer")
    row["approval"] = {"decision": decision, "approved_hash": wording_hash(row), "by": APPROVER,
                       "where": where, "when": when.strip(), "quote": quote.strip(),
                       "quote_source": quote_source, "recorded_by": APPROVAL_RECORDER}
    return row


EXPECTED_LOCKED_STATES = frozenset({"sent", "verify_pending", "verified_fixed", "wont_fix"})


def set_expected(rows, row_id, expected, by=None, now=None, today=None):
    """Set the final wanted wording. Coordinator only. Refused once the row has
    been sent or closed. Changing the wording clears any approval, because
    Spencer approved the earlier wording; a row waiting for Spencer starts its
    wait again (waiting_since moves to now)."""
    if by != APPROVAL_RECORDER:
        raise RegisterError("set-expected refused: --by must be %s" % APPROVAL_RECORDER)
    if not _nonempty(expected):
        raise RegisterError("set-expected refused: expected text must not be empty")
    row = find_row(rows, row_id)
    if row.get("status") in EXPECTED_LOCKED_STATES:
        raise RegisterError("set-expected refused: status is %r" % row.get("status"))
    text = expected.strip()
    if text != row.get("expected"):
        row["expected"] = text
        row["approval"] = None
        if row.get("status") == "waiting_spencer":
            row["waiting_since"] = iso_z(now_utc(now, today))
    return row


# ---------------------------------------------------------------------------
# Views: asks and render
# ---------------------------------------------------------------------------

def _sort_key(row: dict, today: _dt.date):
    return (int(row["tier"]), -age_days(row["first_seen"], today), row["id"])


def is_overdue(row: dict, now=None, today=None) -> bool:
    """A sent or verify_pending row is overdue when it carries `overdue_since`,
    or when OVERDUE_DAYS have passed since `sent.sent_at` with no conclusion."""
    if is_end_state(row.get("status")):
        return False
    if row.get("overdue_since"):
        return True
    if row.get("status") in _FAILED_ATTEMPT_FROM:
        try:
            return now_utc(now, today) >= sent_moment(row.get("sent")) + _dt.timedelta(days=OVERDUE_DAYS)
        except RegisterError:
            return False
    return False


def find_overdue(rows, now=None, today=None) -> list:
    """Sent or verify_pending rows past OVERDUE_DAYS that are not flagged yet."""
    return [r for r in rows if r.get("status") in _FAILED_ATTEMPT_FROM and not r.get("overdue_since")
            and is_overdue(r, now, today)]


def flag_overdue(rows, row_id, next_action, next_action_owner, now=None, today=None):
    """Raise an overdue sent row without touching its status or approval: sets
    `overdue_since` and a new next action so the row reaches `asks`."""
    if not _nonempty(next_action) or not _nonempty(next_action_owner):
        raise RegisterError("flag_overdue refused: next_action and next_action_owner are required")
    row = find_row(rows, row_id)
    if row.get("status") not in _FAILED_ATTEMPT_FROM:
        raise RegisterError("flag_overdue refused: status is %r, only sent or verify_pending rows can be overdue"
                            % row.get("status"))
    moment = now_utc(now, today)
    if not row.get("overdue_since"):
        row["overdue_since"] = iso_z(moment)
    row["next_action"] = next_action.strip()
    row["next_action_owner"] = next_action_owner.strip()
    row["next_action_due"] = moment.date().isoformat()
    return row


def needs_spencer(row: dict, today=None) -> bool:
    if is_end_state(row.get("status")):
        return False
    if row.get("status") in _FAILED_ATTEMPT_FROM:
        return is_overdue(row, today=today)  # a sent row asks only once it is overdue
    return row.get("status") in ("waiting_spencer", "blocked") or row.get("fix_type") == "spencer_decision"


def asks(rows, max_n: int = 3, today=None) -> list:
    """At most `max_n` rows needing Spencer, tier then oldest first. Tier 4
    rows are held back while any tier 1 or 2 row is open."""
    day = resolve_today(today)
    if max_n < 0:
        raise RegisterError("--max must not be negative")
    open_rows = [r for r in rows if not is_end_state(r.get("status"))]
    urgent_open = any(r.get("tier") in (1, 2) for r in open_rows)
    pool = [r for r in open_rows if needs_spencer(r, today=today)]
    if urgent_open:  # the tier 4 hold never hides an overdue row
        pool = [r for r in pool if r.get("tier") != 4 or is_overdue(r, today=today)]
    # tier first, then overdue rows ahead of the rest of their tier, then oldest first
    pool.sort(key=lambda r: (int(r["tier"]), 0 if is_overdue(r, today=today) else 1,
                             -age_days(r["first_seen"], day), r["id"]))
    return pool[:max_n]


def render_markdown(rows, today=None) -> str:
    day = resolve_today(today)
    ordered = sorted(rows, key=lambda r: _sort_key(r, day))
    esc = lambda s: str(s if s is not None else "").replace("|", "\\|").replace("\n", " ")
    open_n = sum(1 for r in rows if not is_end_state(r["status"]))
    lines = [
        "# Findings register",
        "",
        "GENERATED by `register.py render` from `register.jsonl`. Do not edit by hand.",
        "",
        "As of %s: %d findings, %d open. Sorted by tier, then age (oldest first)." % (day.isoformat(), len(rows), open_n),
        "",
    ]
    tiers = sorted(set(int(r["tier"]) for r in ordered))
    for tier in tiers:
        lines += ["## Tier %d" % tier, "",
                  "| ID | Site | Title | Status | Age (days) | Seen | Owner | Next action | Owner | Due |",
                  "|---|---|---|---|---|---|---|---|---|---|"]
        for r in ordered:
            if int(r["tier"]) != tier:
                continue
            lines.append("| %s | %s | %s | %s | %d | %s | %s | %s | %s | %s |" % (
                esc(r["id"]), esc(r["site"]), esc(r["title"]), esc(r["status"]),
                age_days(r["first_seen"], day), esc(r["seen_count"]), esc(r["owner"]),
                esc(r.get("next_action")), esc(r.get("next_action_owner")), esc(r.get("next_action_due"))))
        lines.append("")
    if not rows:
        lines += ["No findings recorded.", ""]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Command line
# ---------------------------------------------------------------------------

WRITE_COMMANDS = frozenset({"add", "transition", "approve", "record-manual-check", "set-expected", "clear-reads"})


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Motor Inn SEO findings register (register.jsonl).")
    p.add_argument("--register", metavar="PATH", help="path to register.jsonl")
    p.add_argument("--today", metavar="YYYY-MM-DD",
                   help="override today's date; on write commands this needs --test-mode")
    p.add_argument("--test-mode", action="store_true",
                   help="allow --now/--today on write commands; refused for a production-style register")
    sub = p.add_subparsers(dest="command")

    a = sub.add_parser("add", help="create a finding, or re-sight one with the same fingerprint")
    a.add_argument("--site", required=True, choices=SITES)
    a.add_argument("--surface", required=True)
    a.add_argument("--check-id", required=True)
    a.add_argument("--target", required=True)
    a.add_argument("--brand", choices=BRANDS)
    a.add_argument("--tier", type=int, choices=TIERS)
    a.add_argument("--title")
    a.add_argument("--observed")
    a.add_argument("--expected")
    a.add_argument("--owner")
    a.add_argument("--fix-type", choices=FIX_TYPES)
    a.add_argument("--source", help="report path that sighted it")
    a.add_argument("--next-action")
    a.add_argument("--next-action-owner")
    a.add_argument("--next-action-due", metavar="YYYY-MM-DD")
    a.add_argument("--verify-json", help='JSON like {"type":"http_status","url":"...","assert":"200"}')

    t = sub.add_parser("transition", help="change a finding's status")
    t.add_argument("--id", required=True)
    t.add_argument("--to", required=True, choices=STATUSES)
    t.add_argument("--next-action")
    t.add_argument("--next-action-owner")
    t.add_argument("--next-action-due", metavar="YYYY-MM-DD")
    t.add_argument("--sent-how", help="how the request left (with --to sent)")
    t.add_argument("--now", metavar="ISO-8601", help="moment recorded as sent_at / waiting_since (default: the clock)")

    mc = sub.add_parser("record-manual-check", help="record a person's check on a manual rule (coordinator only)")
    mc.add_argument("--id", required=True)
    mc.add_argument("--evidence-path", help="existing file under the register's evidence/ folder (required)")
    mc.add_argument("--by", help="must be: coordinator")
    mc.add_argument("--now", metavar="ISO-8601")

    cr = sub.add_parser("clear-reads", help="remove every recorded read on a row")
    cr.add_argument("--id", required=True)

    ap = sub.add_parser("approve", help="record Spencer's approval (coordinator only)")
    ap.add_argument("--id", required=True)
    ap.add_argument("--decision", required=True, choices=APPROVAL_DECISIONS, help="what Spencer approved")
    ap.add_argument("--by", help="must be: coordinator")
    ap.add_argument("--approver", help="must be: Spencer")
    ap.add_argument("--where", help="exactly: chat or slack_dm")
    ap.add_argument("--now", metavar="ISO-8601")
    ap.add_argument("--when", help="ISO-8601 time of the approval")
    ap.add_argument("--quote", help="Spencer's own words")
    ap.add_argument("--quote-source", help="must be: own_message")

    rd = sub.add_parser("render", help="write the generated REGISTER.md view")
    rd.add_argument("--out", help="output path (default: REGISTER.md beside the register)")

    se = sub.add_parser("set-expected", help="set the final wanted wording (coordinator only; clears approval)")
    se.add_argument("--id", required=True)
    se.add_argument("--expected", required=True)
    se.add_argument("--by", help="must be: coordinator")
    se.add_argument("--now", metavar="ISO-8601")

    k = sub.add_parser("asks", help="rows that need Spencer, tier then oldest first")
    k.add_argument("--max", type=int, default=3, dest="max_n")
    k.add_argument("--json", action="store_true", help="print JSON instead of text lines")

    sub.add_parser("validate", help="check every row; exit non-zero and name each bad row")
    return p


def _json_arg(text, what):
    if text is None:
        return None
    try:
        value = json.loads(text)
    except ValueError as exc:
        raise RegisterError("%s is not valid JSON: %s" % (what, exc))
    if not isinstance(value, dict):
        raise RegisterError("%s must be a JSON object" % what)
    return value


def run(argv=None, out=None) -> int:
    out = out or sys.stdout
    parser = _build_parser()
    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help(out)
        return 2
    if not args.register:
        parser.error("--register PATH is required")
    path = args.register
    try:
        cmd = args.command
        if args.test_mode and not is_test_register(path):
            raise RegisterError("--test-mode is refused for %s: a production-style register is never "
                                "run on a made-up clock" % path)
        if cmd in WRITE_COMMANDS and (args.today or getattr(args, "now", None)) and not args.test_mode:
            raise RegisterError("--now and --today on a write command need --test-mode; "
                                "register writes use the system clock")
        today = resolve_today(args.today)
        if cmd == "validate":
            rows = load_rows(path)
            bad = validate_rows(rows, base_dir=os.path.dirname(os.path.abspath(path)))
            if bad:
                for label, problem in bad:
                    out.write("INVALID %s: %s\n" % (label, problem))
                out.write("FAIL: %d problem(s) in %d row(s)\n" % (len(bad), len(set(b[0] for b in bad))))
                return 1
            out.write("OK: %d rows valid\n" % len(rows))
            return 0
        if cmd == "asks":
            rows = load_rows(path)
            picked = asks(rows, args.max_n, today)
            if args.json:
                out.write(json.dumps([_ordered(r) for r in picked], ensure_ascii=False, indent=2) + "\n")
            else:
                for r in picked:
                    out.write("%s | tier %s | %d days old | %s | next: %s\n" % (
                        r["id"], r["tier"], age_days(r["first_seen"], today), r["title"], r.get("next_action")))
            return 0
        if cmd == "render":
            rows = load_rows(path)
            target = args.out or os.path.join(os.path.dirname(os.path.abspath(path)), "REGISTER.md")
            atomic_write_text(target, render_markdown(rows, today))
            out.write("wrote %s (%d rows)\n" % (target, len(rows)))
            return 0
        with _Locked(path):
            rows = load_rows(path, must_exist=(cmd != "add"))
            if cmd == "add":
                row, outcome = add_finding(
                    rows, site=args.site, surface=args.surface, check_id=args.check_id, target=args.target,
                    today=today, brand=args.brand, tier=args.tier, title=args.title, observed=args.observed,
                    expected=args.expected, owner=args.owner, fix_type=args.fix_type, source=args.source,
                    next_action=args.next_action, next_action_owner=args.next_action_owner,
                    next_action_due=args.next_action_due, verify=_json_arg(args.verify_json, "--verify-json"))
                out.write("%s %s (seen_count=%d)\n" % (outcome, row["id"], row["seen_count"]))
            elif cmd == "transition":
                row = transition(rows, args.id, args.to, today=args.today, now=args.now, next_action=args.next_action,
                                 next_action_owner=args.next_action_owner, next_action_due=args.next_action_due,
                                 sent_how=args.sent_how)
                out.write("%s now %s\n" % (row["id"], row["status"]))
            elif cmd == "record-manual-check":
                row = record_manual_check(rows, args.id, args.evidence_path, by=args.by,
                                          now=args.now, today=args.today,
                                          base_dir=os.path.dirname(os.path.abspath(path)))
                out.write("%s has %d recorded read(s)\n" % (row["id"], len(row["verified"]["passes"])))
            elif cmd == "clear-reads":
                row = clear_reads(rows, args.id)
                out.write("reads cleared on %s\n" % row["id"])
            elif cmd == "set-expected":
                row = set_expected(rows, args.id, args.expected, by=args.by, now=args.now, today=args.today)
                out.write("expected updated on %s\n" % row["id"])
            elif cmd == "approve":
                row = approve(rows, args.id, decision=args.decision, by=args.by, approver=args.approver, where=args.where,
                              when=args.when, quote=args.quote, quote_source=args.quote_source,
                              now=args.now, today=args.today)
                out.write("approval recorded on %s\n" % row["id"])
            else:  # pragma: no cover
                raise RegisterError("unknown command %s" % cmd)
            save_rows(path, rows)
        return 0
    except RegisterError as exc:
        sys.stderr.write("REFUSED: %s\n" % exc)
        return 1


def main(argv=None) -> int:
    return run(argv)


if __name__ == "__main__":
    sys.exit(main())
