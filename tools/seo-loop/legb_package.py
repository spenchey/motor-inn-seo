#!/usr/bin/env python3
"""Leg B packager: turns gate-passing drafts into a DealerOn file bundle.

Each page gets exactly 4 files in its own folder: placement note, paste-ready
HTML fragment, metadata file, DealerOn email draft. Nothing is sent or posted;
the email draft has no recipient and no send step. Up to 6 pages per batch; any
page that fails the gate blocks the whole batch.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import sys
from string import Template
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import page_gate  # noqa: E402
import public_wording as pw  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = os.path.join(HERE, "templates")
MAX_PAGES = 6
PAGE_SUFFIXES = (".md", ".markdown", ".html", ".htm")
NOTE_NAME = "01_placement_note.txt"
FRAGMENT_NAME = "02_fragment.html"
METADATA_NAME = "03_metadata.json"
EMAIL_NAME = "04_dealeron_email_draft.txt"
EMAIL_FIRST_LINE = "DRAFT: needs Spencer's OK in chat"
BRAND_LABEL = {"toyota": "Motor Inn Toyota", "chevrolet": "Motor Inn Chevrolet",
               "both": "Motor Inn (Toyota and Chevrolet)"}
META_DESC_MAX = 170


class Refused(Exception):
    pass


# ---------------------------------------------------------------- HTML fragment

def _inline(s: str) -> str:
    s = html.escape(s, quote=True)
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<em>\1</em>", s)
    return s


def markdown_to_html(text: str) -> str:
    _, rest = page_gate._strip_front_matter(text)
    out: List[str] = []
    para: List[str] = []
    items: List[str] = []
    list_tag = ""

    def flush_para() -> None:
        if para:
            out.append("<p>%s</p>" % _inline(" ".join(para)))
            del para[:]

    def flush_list() -> None:
        nonlocal list_tag
        if items:
            out.append("<%s>\n%s\n</%s>" % (list_tag, "\n".join("  <li>%s</li>" % _inline(i) for i in items), list_tag))
            del items[:]
        list_tag = ""

    for line in rest.splitlines():
        s = line.strip()
        m = re.match(r"(#{1,6})\s+(.*?)\s*#*\s*$", s)
        ul = re.match(r"[-*+]\s+(.*)", s)
        ol = re.match(r"\d+\.\s+(.*)", s)
        if not s:
            flush_para()
            flush_list()
        elif m:
            flush_para()
            flush_list()
            n = len(m.group(1))
            out.append("<h%d>%s</h%d>" % (n, _inline(m.group(2)), n))
        elif ul or ol:
            flush_para()
            tag = "ul" if ul else "ol"
            if list_tag and list_tag != tag:
                flush_list()
            list_tag = tag
            items.append((ul or ol).group(1))  # type: ignore[union-attr]
        else:
            flush_list()
            para.append(s)
    flush_para()
    flush_list()
    return "\n\n".join(out) + "\n"


def html_to_fragment(text: str) -> str:
    m = re.search(r"<body[^>]*>(.*)</body>", text, re.S | re.I)
    frag = m.group(1) if m else text
    frag = re.sub(r"<!doctype[^>]*>", "", frag, flags=re.I)
    frag = re.sub(r"<head\b.*?</head>", "", frag, flags=re.S | re.I)
    frag = re.sub(r"<(script|style|iframe|form)\b.*?</\1>", "", frag, flags=re.S | re.I)
    frag = re.sub(r"</?(?:html|body)[^>]*>", "", frag, flags=re.I)
    frag = re.sub(r"<title>.*?</title>", "", frag, flags=re.S | re.I)
    frag = re.sub(r"\son\w+\s*=\s*(?:\"[^\"]*\"|'[^']*')", "", frag, flags=re.I)
    return frag.strip() + "\n"


# ---------------------------------------------------------------- helpers

def _slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def _template(name: str) -> Template:
    with open(os.path.join(TEMPLATES, name), "r", encoding="utf-8") as fh:
        return Template(fh.read())


def list_pages(pages_dir: str) -> List[str]:
    if not os.path.isdir(pages_dir):
        raise Refused("pages folder not found: %s" % pages_dir)
    names = sorted(n for n in os.listdir(pages_dir)
                   if n.lower().endswith(PAGE_SUFFIXES) and os.path.isfile(os.path.join(pages_dir, n)))
    return names


def load_meta(path: str) -> Dict[str, Dict[str, str]]:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError) as exc:
        raise Refused("cannot read meta file: %s" % exc)
    pages = data.get("pages", data) if isinstance(data, dict) else None
    if not isinstance(pages, dict):
        raise Refused('meta file must be a JSON object, optionally under a "pages" key')
    return pages


# ---------------------------------------------------------------- main flow

def package_batch(pages_dir: str, out_dir: str, meta_path: str) -> Tuple[int, List[str]]:
    msgs: List[str] = []
    try:
        names = list_pages(pages_dir)
        if not names:
            raise Refused("no pages (.md or .html) found in %s" % pages_dir)
        if len(names) > MAX_PAGES:
            raise Refused("refused: %d pages found, the batch limit is %d. Nothing was written." % (len(names), MAX_PAGES))
        meta = load_meta(meta_path)

        prepared: List[Dict[str, object]] = []
        failures = 0
        slugs: Dict[str, str] = {}
        for name in names:
            entry = meta.get(name)
            if not isinstance(entry, dict):
                raise Refused("no metadata entry for %s in the meta file" % name)
            brand = str(entry.get("brand", ""))
            if brand not in ("toyota", "chevrolet", "both"):
                raise Refused("%s: meta brand must be toyota, chevrolet or both" % name)
            desc = str(entry.get("meta_description", "")).strip()
            if not desc:
                raise Refused("%s: meta_description is required" % name)
            if len(desc) > META_DESC_MAX:
                raise Refused("%s: meta_description is %d characters; the limit is %d" % (name, len(desc), META_DESC_MAX))
            placement = str(entry.get("placement", "")).strip()
            if not placement:
                raise Refused("%s: placement is required" % name)
            with open(os.path.join(pages_dir, name), "r", encoding="utf-8") as fh:
                text = fh.read()
            is_html = page_gate.is_html_file(name, text)
            result = page_gate.check_page(text, brand, is_html)
            title = str(result["title"])
            fields = {
                "meta_title": str(entry.get("meta_title") or title),
                "meta_description": desc,
                "placement": placement,
                "target_query": str(entry.get("target_query", "")),
            }
            slug = _slugify(str(entry.get("slug") or os.path.splitext(name)[0]))
            # the URL slug and the file name are public wording too (slug views are read by public_wording)
            fields["url_slug"] = slug
            fields["source_file_name"] = os.path.splitext(name)[0]
            meta_fail = page_gate.check_meta_text(fields, brand)
            bad = [r for r in result["rules"] if not r["passed"]] + meta_fail  # type: ignore[union-attr]
            if not slug:
                raise Refused("%s: could not make a URL slug" % name)
            if slug in slugs:
                raise Refused("%s and %s would share the slug %s" % (slugs[slug], name, slug))
            slugs[slug] = name
            if bad:
                failures += 1
                msgs.append("FAIL %s" % name)
                for r in bad:
                    msgs.append("  - %s: %s" % (r["rule"], r["reason"]))
                continue
            prepared.append({"name": name, "text": text, "is_html": is_html, "brand": brand,
                             "result": result, "fields": fields, "slug": slug, "title": title})
            msgs.append("PASS %s" % name)

        if failures:
            msgs.append("BLOCKED: %d of %d page(s) failed the gate. Nothing was written." % (failures, len(names)))
            return 1, msgs

        for p in prepared:
            target = os.path.join(out_dir, str(p["slug"]))
            if os.path.exists(target):
                raise Refused("output folder already exists: %s (nothing was written)" % target)

        for p in prepared:
            folder = os.path.join(out_dir, str(p["slug"]))
            os.makedirs(folder)
            fields = p["fields"]  # type: ignore[assignment]
            result = p["result"]  # type: ignore[assignment]
            fragment = html_to_fragment(str(p["text"])) if p["is_html"] else markdown_to_html(str(p["text"]))
            warns = [("%s x%d" % (w["phrase"], w["count"])) if w["count"] else str(w["phrase"])
                     for w in result["warnings"]]
            gate_lines = "\n".join("  [PASS] %s: %s" % (r["rule"], r["reason"]) for r in result["rules"])
            subs = {
                "title": p["title"], "brand_label": BRAND_LABEL[str(p["brand"])], "slug": p["slug"],
                "placement": fields["placement"], "target_query": fields["target_query"] or "(not given)",
                "meta_title": fields["meta_title"], "meta_description": fields["meta_description"],
                "fragment_name": FRAGMENT_NAME, "metadata_name": METADATA_NAME,
                "gate_result": "PASS (%d of %d rules)" % (len(result["rules"]), len(result["rules"])),
                "gate_lines": gate_lines, "warnings": "; ".join(warns) if warns else "none",
            }
            metadata = {
                "slug": p["slug"], "brand": p["brand"], "title": p["title"],
                "meta_title": fields["meta_title"], "meta_description": fields["meta_description"],
                "placement": fields["placement"], "target_query": fields["target_query"],
                "source_file": p["name"],
                "source_sha256": hashlib.sha256(str(p["text"]).encode("utf-8")).hexdigest(),
                "gate": {"passed": True, "rules": result["rules"], "warnings": result["warnings"]},
                "status": "draft, needs Spencer's OK in chat",
            }
            email = _template("dealeron_email.txt.tmpl").safe_substitute(subs)
            if not email.startswith(EMAIL_FIRST_LINE + "\n"):
                raise Refused("email template must start with: " + EMAIL_FIRST_LINE)
            files = {
                NOTE_NAME: _template("placement_note.txt.tmpl").safe_substitute(subs),
                FRAGMENT_NAME: fragment,
                METADATA_NAME: json.dumps(metadata, indent=2) + "\n",
                EMAIL_NAME: email,
            }
            for fname, content in files.items():
                with open(os.path.join(folder, fname), "w", encoding="utf-8") as fh:
                    fh.write(content)
            msgs.append("WROTE %s (4 files)" % folder)
        msgs.append("DONE: %d page(s) packaged. Drafts only; nothing was sent." % len(prepared))
        return 0, msgs
    except Refused as exc:
        msgs.append(str(exc))
        return 2, msgs
    except (OSError, UnicodeDecodeError) as exc:
        msgs.append("error: %s" % exc)
        return 2, msgs


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Package up to 6 gate-passing pages as a DealerOn file bundle (4 files per page). Sends nothing.")
    ap.add_argument("--pages", required=True, help="folder of .md/.html drafts")
    ap.add_argument("--out", required=True, help="folder to write the bundle into")
    ap.add_argument("--meta", required=True, help="JSON file: per page brand, placement, meta_description, optional slug/meta_title/target_query")
    args = ap.parse_args(argv)
    code, msgs = package_batch(args.pages, args.out, args.meta)
    for m in msgs:
        print(m, file=sys.stderr if code else sys.stdout)
    return code


if __name__ == "__main__":
    sys.exit(main())
