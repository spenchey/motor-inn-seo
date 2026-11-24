#!/usr/bin/env python3
"""Monday delivery: render the summary, save it, and DM it to Spencer.

    render (monday_summary.py)  ->  save findings/summaries/summary-<date>.txt  ->  Slack DM

Rules
- It sends only on a real Monday (the wall clock, not --today) unless --force is given.
- --dry-run does everything except the Slack call: it never loads the sender, never looks
  for a token, and prints what it would send.
- If the render fails, the DM is one line: "SEO summary failed this week, see summary.log".
- If the DM fails, the failure is written loudly to stderr and to findings/logs/summary.log,
  and the exit code is 1.
- The Slack user id and the path of the existing sender are read from the config file
  (findings/seo-loop.config.json, never in git). The sender is the one the price-drop job
  already uses: its post_dm and resolve_token functions are imported, so no token handling
  lives here.

Python 3.9, standard library only.
"""
from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
FAILED_LINE = "SEO summary failed this week, see summary.log"


def _now():
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def loud(msg, log_path=None):
    line = "%s !!! %s" % (_now(), msg)
    sys.stderr.write(line + "\n")
    sys.stderr.flush()
    if log_path:
        try:
            with open(log_path, "a", encoding="utf-8") as fh:
                fh.write(line + "\n")
        except OSError:
            pass


def info(msg):
    print("%s %s" % (_now(), msg), flush=True)


def reporting_month(today):
    y = today - dt.timedelta(days=1)
    return "%04d-%02d" % (y.year, y.month)


def load_config(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError) as exc:
        raise RuntimeError("cannot read config %s: %s" % (path, exc))
    if not isinstance(data, dict):
        raise RuntimeError("config %s must be a JSON object" % path)
    return data


def render(root, today_arg):
    """Run monday_summary.py. Returns (text or None, stderr text)."""
    today = dt.date.fromisoformat(today_arg) if today_arg else dt.date.today()
    base = os.path.join(root, "findings", "baselines", "%s.json" % reporting_month(today))
    cmd = [sys.executable, "-I", os.path.join(HERE, "monday_summary.py"),
           "--register", os.path.join(root, "findings", "register.jsonl"),
           "--baselines", base]
    if today_arg:
        cmd += ["--today", today_arg]
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              encoding="utf-8", errors="replace", timeout=120)
    except (OSError, subprocess.SubprocessError) as exc:
        return None, "could not run the summary: %s" % exc
    text = proc.stdout.strip()
    if proc.returncode != 0 or not text:
        return None, proc.stderr.strip() or "the summary printed nothing"
    return text, proc.stderr.strip(), base


def stale_note(base, today_arg, today):
    """On a real run, say so when the numbers were not rebuilt this morning."""
    if today_arg or not os.path.isfile(base):
        return None
    last = dt.date.fromtimestamp(os.path.getmtime(base))
    if last == today:
        return None
    return "Note: the numbers were not refreshed this morning (last refreshed %d/%d)." % (last.month, last.day)


def load_sender(path):
    """Import the existing sender by path. Writes no bytecode into its folder."""
    path = os.path.expanduser(path or "")
    if not path or not os.path.isfile(path):
        raise RuntimeError("the Slack sender file named in the config was not found")
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("existing_slack_sender", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    for name in ("post_dm", "resolve_token"):
        if not callable(getattr(mod, name, None)):
            raise RuntimeError("the Slack sender has no %s" % name)
    return mod


def send_dm(cfg, text):
    user = cfg.get("slack_user_id")
    if not isinstance(user, str) or not user:
        raise RuntimeError("config has no slack_user_id")
    sender = load_sender(cfg.get("slack_sender_path"))
    token = sender.resolve_token()
    if not token:
        raise RuntimeError("no Slack token available to the sender")
    return sender.post_dm(text, user, token)


def write_text(path, text):
    folder = os.path.dirname(os.path.abspath(path))
    os.makedirs(folder, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".summary-", suffix=".tmp", dir=folder)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):  # cron runs with a plain locale; keep the dashes readable
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    root_default = os.path.dirname(os.path.dirname(HERE))
    ap = argparse.ArgumentParser(description="Render the Monday summary, save it, DM it to Spencer.")
    ap.add_argument("--root", default=root_default, help="repo folder that holds findings/")
    ap.add_argument("--config", default=None, help="JSON config (default: findings/seo-loop.config.json)")
    ap.add_argument("--dry-run", action="store_true", help="do everything except the Slack call; print what would be sent")
    ap.add_argument("--dry-run-out", default=None, help="with --dry-run: also write the text to this file")
    ap.add_argument("--today", default=None, help="YYYY-MM-DD for the summary date (needs --dry-run or --force)")
    ap.add_argument("--force", action="store_true", help="send even if today is not Monday or was already sent")
    a = ap.parse_args(argv)

    root = os.path.abspath(os.path.expanduser(a.root))
    logs = os.path.join(root, "findings", "logs")
    summary_log = os.path.join(logs, "summary.log")
    wall = dt.date.today()

    if a.today:
        try:
            dt.date.fromisoformat(a.today)
        except ValueError:
            sys.stderr.write("refused: --today must look like YYYY-MM-DD\n")
            return 2
        if not a.dry_run and not a.force:
            sys.stderr.write("refused: --today without --dry-run needs --force\n")
            return 2
    if not a.dry_run and wall.weekday() != 0 and not a.force:
        sys.stderr.write("refused: today is not Monday, so nothing is sent (use --force to override)\n")
        return 3

    today = dt.date.fromisoformat(a.today) if a.today else wall
    day = today.isoformat()
    out_path = os.path.join(root, "findings", "summaries", "summary-%s.txt" % day)
    marker = os.path.join(root, "findings", "summaries", ".dm-sent-%s" % day)

    if not a.dry_run and os.path.exists(marker) and not a.force:
        sys.stderr.write("refused: the summary for %s was already sent (use --force to send again)\n" % day)
        return 3

    result = render(root, a.today)
    ok = result[0] is not None
    if ok:
        text, err, base = result
        if err:
            with open(summary_log, "a", encoding="utf-8") as fh:
                fh.write("%s %s\n" % (_now(), err))
        note = stale_note(base, a.today, today)
        if note:
            text = text + "\n" + note
    else:
        text = FAILED_LINE
        loud("the summary could not be made: %s" % result[1], summary_log if os.path.isdir(logs) else None)

    if a.dry_run:
        info("[dry-run] nothing sent; the sender was not loaded and no token was looked up")
        info("[dry-run] the %s message would be:" % ("SUMMARY" if ok else "FAILURE"))
        print(text)
        if a.dry_run_out:
            write_text(a.dry_run_out, text)
            info("[dry-run] text copied to %s" % a.dry_run_out)
        return 0 if ok else 1

    if ok:
        write_text(out_path, text)
        info("saved %s" % os.path.relpath(out_path, root))
    try:
        cfg = load_config(a.config or os.path.join(root, "findings", "seo-loop.config.json"))
        reply = send_dm(cfg, text)
    except Exception as exc:  # the DM must never fail quietly
        loud("DM NOT SENT: %s: %s. The Monday SEO summary did not reach Spencer."
             % (type(exc).__name__, exc), summary_log)
        return 1
    try:
        write_text(marker, json.dumps({"sent_at": _now(), "ts": (reply or {}).get("ts")}))
    except OSError as exc:
        loud("DM was sent but the sent-marker could not be written: %s" % exc, summary_log)
    info("DM sent (%d characters)%s" % (len(text), "" if ok else ", failure notice"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
