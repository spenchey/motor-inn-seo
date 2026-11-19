#!/usr/bin/env python3
"""SA-04 packet builder: turns register findings into ready-to-approve drafts for Spencer.

Writes local files only. It never sends anything and never changes the register.
Usage: python3 -I packet.py --register PATH --ids ID[,ID...] --out DIR [--today YYYY-MM-DD]
"""
from __future__ import annotations

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import public_wording as pw  # noqa: E402  (shared wording rules, SA-19)
import register  # noqa: E402  (frozen SA-01 module, placed beside this file)

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(HERE, "templates")
DRAFT_LINE = "DRAFT: needs Spencer's OK in chat"
DEALERON_CAP = 5
TEMPLATE_FOR = {
    "dealeron_request": "dealeron_request.md",
    "gbp_edit": "gbp_edit.md",
    "content_draft": "content_draft.md",
    "spencer_decision": "spencer_decision.md",
}
REFUSED_STATUSES = ("sent", "verify_pending", "verified_fixed", "wont_fix")
BRAND_LABEL = {"toyota": "Toyota", "chevrolet": "Chevrolet", "both": "Motor Inn"}

NOT_FINAL_WORDS = ("spencer", "to approve", "to be confirmed", "tbd", "needs confirmation",
                   "needs_confirmation", "unverified", "not verified", "[needs fact]")

WHY_BY_TIER = {
    1: "This can keep an important page out of search results, or show shoppers wrong information. It comes first.",
    2: "The page is listed, but it cannot rank or turn visitors into leads as well as it should.",
    3: "This is a slow-burn problem that holds back search results over time.",
    4: "This is a small polish item. It is not urgent.",
}


class PacketRefused(Exception):
    """A plain-English reason the packet was not built."""


# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------

def load_template(fix_type: str) -> dict:
    path = os.path.join(TEMPLATE_DIR, TEMPLATE_FOR[fix_type])
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    parts = {}
    current = None
    for line in text.splitlines():
        m = re.match(r"^=== (HEAD|ITEM|FOOT) ===$", line)
        if m:
            current = m.group(1)
            parts[current] = []
        elif current:
            parts[current].append(line)
    for key in ("HEAD", "ITEM", "FOOT"):
        if key not in parts:
            raise PacketRefused("template %s is missing its %s section" % (TEMPLATE_FOR[fix_type], key))
    out = {k: "\n".join(v).strip("\n") for k, v in parts.items()}
    if out["HEAD"].splitlines()[0] != DRAFT_LINE:
        raise PacketRefused("template %s does not start with the DRAFT line" % TEMPLATE_FOR[fix_type])
    return out


def fill(template: str, values: dict) -> str:
    return re.sub(r"\{\{(\w+)\}\}", lambda m: str(values.get(m.group(1), m.group(0))), template)


def describe_verify(verify) -> str:
    if not isinstance(verify, dict) or not verify.get("type"):
        return "A person checks it by hand, because no automatic check is set yet."
    kind = verify.get("type")
    want = verify.get("assert")
    url = verify.get("url")
    where = " at %s" % url if url else ""
    texts = {
        "meta_robots": "We load the page%s and confirm its search-engine tag reads: %s.",
        "title_contains": "We load the page%s and confirm its title contains: %s.",
        "title_leads_with": "We load the page%s and confirm its title begins with: %s.",
        "title_not_contains": "We load the page%s and confirm its title no longer contains: %s.",
        "html_contains": "We load the page%s and confirm it contains: %s.",
        "html_not_contains": "We load the page%s and confirm it no longer contains: %s.",
        "jsonld_equals": "We load the page%s and confirm its structured data says: %s.",
        "http_status": "We request the page%s and confirm it answers with status: %s.",
        "gbp_field_equals": "We read the Google listing and confirm this field matches: %s.",
    }
    if kind == "manual":
        return "A person checks it by hand once the change is made."
    tmpl = texts.get(kind)
    if tmpl is None:
        return "A person checks it by hand."
    if kind == "gbp_field_equals":
        return tmpl % want
    if kind == "title_leads_with":
        return tmpl % ("", want)
    return tmpl % (where, want)


def item_values(row: dict, n: int, mask_observed: bool = False) -> dict:
    """mask_observed hides what the page shows today and its address, which are not our own wording."""
    verify = row.get("verify") if isinstance(row.get("verify"), dict) else None
    url = (verify or {}).get("url") or row.get("target")
    current = row["observed"]
    if mask_observed:
        current = "[current value]"
        url = "[page address]"
        if verify is not None and verify.get("url"):
            verify = dict(verify)
            verify["url"] = "[page address]"
    return {
        "n": n,
        "title": row["title"],
        "url": url,
        "current": current,
        "wanted": row["expected"],
        "why": WHY_BY_TIER.get(row["tier"], WHY_BY_TIER[3]),
        "evidence_date": row["last_seen"],
        "verify": describe_verify(verify),
    }


def packet_brand(rows: list) -> str:
    concrete = sorted(set(r["brand"] for r in rows if r["brand"] != "both"))
    return concrete[0] if len(concrete) == 1 else "both"


def render_packet(fix_type: str, rows: list, today: str, part: int = 1, parts: int = 1,
                  mask_observed: bool = False) -> str:
    tpl = load_template(fix_type)
    brand_label = BRAND_LABEL[packet_brand(rows)]
    items = []
    email_items = []
    for n, row in enumerate(rows, 1):
        vals = item_values(row, n, mask_observed)
        items.append(fill(tpl["ITEM"], vals))
        email_items.append(
            "%d. %s\n   Page: %s\n   Today it shows: %s\n   Please change it to: %s"
            % (n, vals["title"], vals["url"], vals["current"], vals["wanted"]))
    common = {
        "count": len(rows), "item_word": "item" if len(rows) == 1 else "items", "today": today,
        "brand_label": brand_label, "part": part, "parts": parts, "cap": DEALERON_CAP,
        "email_items": "\n\n".join(email_items),
    }
    chunks = [fill(tpl["HEAD"], common), "\n\n".join(items), fill(tpl["FOOT"], common)]
    text = "\n\n".join(chunks).rstrip("\n") + "\n"
    if text.splitlines()[0] != DRAFT_LINE:
        raise PacketRefused("internal error: packet does not start with the DRAFT line")
    return text


def check_own_wording(fix_type: str, rows: list, today: str, part: int, parts: int) -> list:
    """Our own wording is the whole packet with each page's current value and address masked out."""
    text = render_packet(fix_type, rows, today, part, parts, mask_observed=True)
    return ["our own wording breaks the shared wording rules: %s" % p
            for p in pw.check_public_text(text, packet_brand(rows))]


# ---------------------------------------------------------------------------
# Selection and rules
# ---------------------------------------------------------------------------

def tier_hold_open(all_rows: list) -> list:
    return [r for r in all_rows
            if r.get("tier") in (1, 2) and not register.is_end_state(r.get("status"))]


def select_rows(all_rows: list, ids: list) -> list:
    by_id = {r.get("id"): r for r in all_rows}
    problems = []
    chosen = []
    seen = set()
    for rid in ids:
        if rid in seen:
            continue
        seen.add(rid)
        row = by_id.get(rid)
        if row is None:
            problems.append("%s: not found in the register" % rid)
        else:
            chosen.append(row)
    if problems:
        raise PacketRefused("; ".join(problems))
    return chosen


def check_rows(all_rows: list, rows: list) -> None:
    problems = []
    for row in rows:
        rid = row.get("id")
        for p in register.validate_row(row):
            problems.append("%s: register row is invalid: %s" % (rid, p))
        if row.get("fix_type") == "internal_repair":
            problems.append("%s: internal repairs are not public packets" % rid)
        if row.get("status") in REFUSED_STATUSES:
            problems.append("%s: already %s, so no new packet" % (rid, row.get("status")))
        if row.get("brand") in BRAND_LABEL:
            for key, label in (("title", "title"), ("expected", "wanted value"), ("next_action", "next action")):
                for p in pw.check_public_text(row.get(key) or "", row.get("brand")):
                    problems.append("%s: the %s breaks the shared wording rules: %s" % (rid, label, p))
        if row.get("fix_type") == "dealeron_request":
            for key, label in (("expected", "wanted value"), ("title", "title")):
                low = (row.get(key) or "").lower()
                hits = [w for w in NOT_FINAL_WORDS if w in low]
                if hits:
                    problems.append(
                        "%s: this DealerOn item needs final wording before it can go to a vendor: the %s "
                        "still holds a working note (%s). Write the exact wording first."
                        % (rid, label, ", ".join(hits)))
    if any(r.get("tier") == 4 for r in rows):
        open_top = tier_hold_open(all_rows)
        if open_top:
            problems.append("tier 4 hold: %d tier 1 or 2 item(s) are still open (first: %s); "
                            "cosmetic packets wait" % (len(open_top), open_top[0].get("id")))
    brands = set(r.get("brand") for r in rows)
    if "toyota" in brands and "chevrolet" in brands:
        problems.append("make wall: this batch mixes Toyota and Chevrolet rows; build them separately")
    if problems:
        raise PacketRefused("\n".join(problems))


def plan_packets(rows: list) -> list:
    """Returns [(fix_type, [rows], part, parts)] in a stable order."""
    plan = []
    for fix_type in ("dealeron_request", "gbp_edit", "content_draft", "spencer_decision"):
        group = [r for r in rows if r["fix_type"] == fix_type]
        if not group:
            continue
        if fix_type == "dealeron_request":
            chunks = [group[i:i + DEALERON_CAP] for i in range(0, len(group), DEALERON_CAP)]
        else:
            chunks = [group]
        for k, chunk in enumerate(chunks, 1):
            plan.append((fix_type, chunk, k, len(chunks)))
    return plan


def build(register_path: str, ids: list, out_dir: str, today: str) -> list:
    """Validates everything first, then writes. Returns the files written."""
    all_rows = register.load_rows(register_path)
    rows = select_rows(all_rows, ids)
    if not rows:
        raise PacketRefused("no finding IDs were given")
    check_rows(all_rows, rows)
    plan = plan_packets(rows)
    problems = []
    rendered = []
    counters = {}
    for fix_type, chunk, part, parts in plan:
        for p in check_own_wording(fix_type, chunk, today, part, parts):
            problems.append("%s packet: %s" % (fix_type, p))
        counters[fix_type] = counters.get(fix_type, 0) + 1
        folder = os.path.join(out_dir, "%s-%s-%02d" % (today, fix_type.replace("_", "-"), counters[fix_type]))
        rendered.append((folder, render_packet(fix_type, chunk, today, part, parts)))
    if problems:
        raise PacketRefused("\n".join(problems))
    for folder, _ in rendered:
        if os.path.exists(folder):
            raise PacketRefused("%s already exists; nothing was written. Use a new --out folder." % folder)
    written = []
    for folder, text in rendered:
        os.makedirs(folder)
        path = os.path.join(folder, "PACKET.md")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        written.append(path)
    return written


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Build ready-to-approve packets from register findings. Writes local files only; never sends anything.")
    p.add_argument("--register", required=True, help="path to register.jsonl (read only)")
    p.add_argument("--ids", required=True, help="comma-separated finding IDs")
    p.add_argument("--out", required=True, help="folder to write packet folders into")
    p.add_argument("--today", default=None, help="YYYY-MM-DD (tests and replays should pass it)")
    return p


def main(argv=None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        today = register.resolve_today(args.today).isoformat()
        ids = [i.strip() for i in args.ids.split(",") if i.strip()]
        written = build(args.register, ids, args.out, today)
    except (PacketRefused, register.RegisterError) as exc:
        sys.stderr.write("REFUSED: %s\n" % exc)
        return 1
    for path in written:
        sys.stdout.write("wrote %s\n" % path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
