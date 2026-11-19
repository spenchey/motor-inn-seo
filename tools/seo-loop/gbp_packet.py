#!/usr/bin/env python3
"""Print a one-page approval packet for Google Business post drafts.

Read-only: reads one drafts file and an optional approvals file, and prints
plain text. It never publishes, edits, sends or writes anything. A draft's
approval line is only a claim; a post counts as approved only when the
approvals file holds a matching record (contract rule T6). Public wording
rules come only from the shared public_wording module (SA-19).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import public_wording  # noqa: E402

DRAFT_LINE = "DRAFT: needs Spencer's OK in chat"
DECISION_HEADING = "Ready for Spencer's decision"
LISTINGS = ("toyota", "chevrolet", "group")
HEADER_KEYS = {"type", "publish date", "approval", "target keyword", "image"}
CTA_KEYS = {"cta button", "cta link"}
TAIL_KEYS = CTA_KEYS | {"image"}
COPY_KEY = "copy"
ALL_KEYS = HEADER_KEYS | CTA_KEYS | {COPY_KEY}
RECORD_FIELDS = ("by", "when", "quote", "draft_file")
DRAFT_NAME_RE = re.compile(r"^posts-week-of-\d{4}-\d{2}-\d{2}\.md$")
POST_RE = re.compile(r"^###\s+Post\s+(\d+):\s*(.*?)\s*$")
FIELD_RE = re.compile(r"^\*\*([^*]+?):\*\*\s*(.*)$")
OFFER_END_RE = re.compile(r"offer\s+ends:?\**\s*(\d{4}-\d{2}-\d{2})", re.I)


def parse_day(text):
    """Return a date for YYYY-MM-DD text, or None if it is not a real date."""
    try:
        return datetime.strptime(text.strip(), "%Y-%m-%d").date()
    except (ValueError, AttributeError):
        return None


def approval_hash(post):
    """sha256 of 'publish date|title|copy|CTA button|CTA link' for the post's current text.

    Publish date, title, button label and link are stripped. The copy is its
    non-blank lines, trailing spaces removed, joined with newlines. This is the
    only place the approval key is built.
    """
    parts = [
        first_value(post["header"], "publish date"),
        post["title"].strip(),
        "\n".join(line.rstrip() for line in post["copy_zone"]),
        first_value(post["tail"], "cta button"),
        first_value(post["tail"], "cta link"),
    ]
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()


EXTRA_TEXT_MSG = ("Extra text found after the button fields. A post with extra text there "
                  "never counts as approved.")


def _flag_extra(post):
    """Record extra text after the CTA fields (anything but the Image field)."""
    post["extra_after_cta"] = True
    if EXTRA_TEXT_MSG not in post["problems"]:
        post["problems"].append(EXTRA_TEXT_MSG)


def _add_field(post, store, key, value, label):
    values = store.setdefault(key, [])
    values.append(value)
    if len(values) == 2:
        post["problems"].append('Field "%s" appears more than once.' % label)


def parse_posts(text):
    """Split a drafts file into posts.

    Header fields are read only above **Copy:**. CTA fields are read only
    after the copy ends. Any other field-like line is post text and is
    reported as a problem. A post heading before a post's CTA fields is
    reported, and the text after it is read as a new post.
    """
    posts = []
    post = None
    zone = "header"  # header | copy | tail
    for raw in text.splitlines():
        line = raw.rstrip()
        m = POST_RE.match(line)
        if m:
            if post is not None and zone in ("header", "copy"):
                post["problems"].append("A post heading appears before this post's CTA fields. "
                                        "The text after it was read as a new post.")
            post = {"number": int(m.group(1)), "title": m.group(2),
                    "header": {}, "tail": {}, "copy_lines": [], "copy_zone": [],
                    "copy_seen": False, "problems": [], "extra_after_cta": False}
            posts.append(post)
            zone = "header"
            continue
        if post is None:
            continue
        # After the CTA fields, a "## " heading starts file-level notes. They are
        # not post text, up to the next "### Post" heading. Inside the copy a
        # "## " line is still copy and is checked.
        if zone in ("tail", "closed") and line.startswith("## "):
            zone = "notes"
            continue
        if zone == "notes":
            continue
        if zone in ("tail", "closed") and line.strip() == "---":
            zone = "closed"  # the post's closing rule; plain text after it is extra text
            continue
        fm = FIELD_RE.match(line)
        key = fm.group(1).strip().lower() if fm else None
        if key in ALL_KEYS:
            value = fm.group(2).strip()
            label = key.capitalize()
            if zone == "header":
                if key == COPY_KEY:
                    zone = "copy"
                    post["copy_seen"] = True
                    if value:
                        post["copy_lines"].append(value)
                        post["copy_zone"].append(value)
                elif key in HEADER_KEYS:
                    _add_field(post, post["header"], key, value, label)
                else:
                    post["problems"].append('"%s" appears before the copy. Treated as post text.' % label)
                    post["copy_lines"].append(line)
                    post["copy_zone"].append(line)
            elif zone == "copy":
                if key in CTA_KEYS:
                    zone = "tail"
                    _add_field(post, post["tail"], key, value, label)
                else:
                    post["problems"].append('Field-like line inside the post text ("%s"). '
                                            'Treated as text, not as a field.' % label)
                    post["copy_lines"].append(line)
                    post["copy_zone"].append(line)
            elif key == "image":  # tail or closed: the only line allowed after the button fields
                _add_field(post, post["tail"], key, value, label)
            elif key in CTA_KEYS and zone == "tail":
                _add_field(post, post["tail"], key, value, label)
            else:  # any other field-like line after the button fields is extra text
                _flag_extra(post)
                post["problems"].append('Field-like line after the CTA fields ("%s"). '
                                        'Treated as text, not as a field.' % label)
                post["copy_lines"].append(line)
            continue
        if zone == "copy" and line.strip():
            post["copy_lines"].append(line)
            post["copy_zone"].append(line)
        elif zone in ("tail", "closed") and line.strip():
            _flag_extra(post)
            post["copy_lines"].append(line)
    return posts


def first_value(store, key):
    values = store.get(key) or []
    return values[0].strip() if values else ""


def claims_approved(post):
    """The draft's approval line. This is only a claim, never an approval."""
    return re.match(r"approved\b", first_value(post["header"], "approval"), re.I) is not None


def valid_record(record, file_name):
    if not isinstance(record, dict):
        return False
    if record.get("draft_file") != file_name:
        return False
    return all(isinstance(record.get(k), str) and record[k].strip() for k in RECORD_FIELDS)


def summary_of(post):
    for line in post["copy_lines"]:
        text = line.strip()
        if text:
            return text if len(text) <= 140 else text[:137].rstrip() + "..."
    return "(no copy)"


def check_post(post, listing, today):
    """Return plain-English problems for a post. Empty list means clean."""
    problems = list(post["problems"])
    copy_text = "\n".join(post["copy_lines"])
    title = post["title"]
    if not post["copy_seen"]:
        problems.append("The Copy field is missing.")
    elif not copy_text.strip():
        problems.append("Copy is empty.")

    pub_text = first_value(post["header"], "publish date")
    pub_day = parse_day(pub_text) if pub_text else None
    if not pub_text:
        problems.append("Publish date is missing.")
    elif pub_day is None:
        problems.append("Publish date is not a real date (use YYYY-MM-DD).")
    elif today is not None and pub_day < today:
        problems.append("Publish date has already passed.")

    if pub_day is not None:
        for m in OFFER_END_RE.finditer(title + "\n" + copy_text):
            end_day = parse_day(m.group(1))
            if end_day is not None and end_day < pub_day:
                problems.append("Offer ends %s, before the publish date %s."
                                % (end_day.isoformat(), pub_day.isoformat()))

    fields = [("Title", [title]),
              ("Copy", [copy_text]),
              ("Button label", post["tail"].get("cta button", [])),
              ("Button link", post["tail"].get("cta link", [])),
              ("Image", post["header"].get("image", []) + post["tail"].get("image", []))]
    for label, values in fields:
        for value in values:
            for problem in public_wording.check_public_text(value, listing):
                problems.append("%s: %s" % (label, problem))
    return problems


def _approval_record_for(post, approvals, file_name):
    key = approval_hash(post)
    record = approvals.get(key)
    return record if valid_record(record, file_name) else None


def build_packet(text, file_name, listing, today, approvals=None, approvals_note=None):
    """Build the packet. approvals maps hash -> record; None or {} means nothing is approved."""
    approvals = approvals or {}
    posts = parse_posts(text)
    hashes = {approval_hash(p) for p in posts}
    # Records for this draft that match no current post text.
    unmatched = [(k, r) for k, r in approvals.items()
                 if isinstance(r, dict) and r.get("draft_file") == file_name and k not in hashes]

    out = [DRAFT_LINE, "File: %s" % file_name, "Listing: %s" % listing,
           "Checked against date: %s" % today.isoformat()]
    if listing == "group":
        out.append("Make check: not run (group listing; pass --listing toyota or chevrolet)")
    out.append(approvals_note or "Approvals file: not given. Nothing counts as approved.")
    out.append("")

    clean_approved, ready, unclean_decision, blocks = [], [], [], []
    for post in posts:
        record = _approval_record_for(post, approvals, file_name)
        matched = record is not None
        # Extra text after the button fields means no approval counts (X4).
        approved = matched and not post["extra_after_cta"]
        problems = check_post(post, listing, today)
        if approved and not problems:
            clean_approved.append(str(post["number"]))
            continue
        pub = first_value(post["header"], "publish date") or "(missing)"
        status = "Approved on record" if approved else "Not approved: listed for Spencer's decision"
        link = first_value(post["tail"], "cta link") or "(none)"
        block = ["Post %d | %s | %s | %s" % (post["number"], pub, post["title"], status),
                 "  Summary: %s" % summary_of(post),
                 "  Button link: %s" % link]
        if not approved:
            # A record is tied to a post by its optional title field. Without
            # one, a changed post cannot be identified and gets the plain claim message.
            changed = any(r.get("title") == post["title"] for _, r in unmatched)
            if matched:
                block.append("  Approval on record does not count: extra text was found "
                             "after the button fields.")
            elif changed:
                block.append("  Wording changed after approval: the approval on record "
                             "no longer matches this post's text.")
            elif claims_approved(post):
                block.append("  Draft says approved, but no matching approval is on record.")
        if problems:
            block.append("  Verdict: Fix")
            if approved:
                block.append("  Do not publish: an approval is on record, but the post has problems.")
            block.extend("    - %s" % p for p in problems)
            if not approved:
                unclean_decision.append(str(post["number"]))
        else:
            block.append("  Verdict: Ready")
            ready.append(post)
        blocks.append(block)

    if not posts:
        out.append("No posts found in this file.")
        out.append("")
    if clean_approved:
        out.append("Approved on record and clean (not listed for decision): post %s"
                   % ", ".join(clean_approved))
        out.append("")
    for block in blocks:
        out.extend(block)
        out.append("")
    out.append(DECISION_HEADING)
    if ready:
        for post in ready:
            out.append("  Post %d: %s" % (post["number"], post["title"]))
    else:
        out.append("  None. No post without an approval on record is clean.")
    if unclean_decision:
        out.append("Also listed for decision, with problems: post %s" % ", ".join(unclean_decision))
    return "\n".join(out) + "\n"


def load_approvals(path):
    """Read approvals.json. Returns (records, note). Never writes.

    A missing, unreadable or malformed file means nothing counts as approved.
    """
    name = os.path.basename(path)
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return {}, ("Approvals file missing or unreadable (%s). "
                    "Nothing counts as approved." % type(exc).__name__)
    if not isinstance(data, dict):
        return {}, "Approvals file is not a JSON object. Nothing counts as approved."
    return data, "Approvals file: %s (%d records)" % (name, len(data))


def latest_draft(drafts_dir):
    names = sorted(n for n in os.listdir(drafts_dir) if DRAFT_NAME_RE.match(n))
    return names[-1] if names else None


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Print a plain approval packet for GBP post drafts. Read-only.")
    parser.add_argument("--drafts-dir", required=True,
                        help="folder holding posts-week-of-YYYY-MM-DD.md files")
    parser.add_argument("--file", help="draft file name inside --drafts-dir (default: newest)")
    parser.add_argument("--listing", choices=LISTINGS, default="group",
                        help="which listing the posts go to (default: group)")
    parser.add_argument("--today", help="YYYY-MM-DD used for the date checks (default: system date)")
    parser.add_argument("--approvals", metavar="PATH",
                        help="approvals.json; read only. Without a matching record nothing is approved")
    args = parser.parse_args(argv)

    if args.today is not None:
        today = parse_day(args.today)
        if today is None:
            parser.error("--today must be a real date in YYYY-MM-DD form")
    else:
        today = date.today()
    if args.file is not None and os.path.basename(args.file) != args.file:
        parser.error("--file takes a file name, not a path")

    try:
        name = args.file or latest_draft(args.drafts_dir)
    except OSError as exc:
        sys.stderr.write("cannot read drafts folder: %s\n" % exc)
        return 2
    if not name:
        sys.stderr.write("no posts-week-of-YYYY-MM-DD.md file found in %s\n" % args.drafts_dir)
        return 2
    try:
        text = Path(os.path.join(args.drafts_dir, name)).read_text(encoding="utf-8")
    except OSError as exc:
        sys.stderr.write("cannot read draft file: %s\n" % exc)
        return 2

    if args.approvals is None:
        approvals, note = {}, None
    else:
        approvals, note = load_approvals(args.approvals)
    sys.stdout.write(build_packet(text, name, args.listing, today, approvals, note))
    return 0


if __name__ == "__main__":
    sys.exit(main())
