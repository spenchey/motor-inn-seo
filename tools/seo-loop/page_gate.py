#!/usr/bin/env python3
"""Page quality gate for Motor Inn drafts (Markdown or HTML).

Checks a drafted page before the owner sees it. Prints pass or fail with a plain
reason per rule. Exit 0 only on pass. Reads one file; writes nothing; no network.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from html.parser import HTMLParser
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import public_wording as pw  # noqa: E402  shared banned-wording, phone and make-wall rules (SA-19)

OUR_PHONE = "7127925000"
OUR_PHONE_TEXT = "712-792-5000"
HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TELLS = os.path.join(HERE, "ai_tells.txt")

FILLER_OPENERS = re.compile(
    r"^(?:welcome|looking\s+for|are\s+you|have\s+you|when\s+it\s+comes\s+to|in\s+today|"
    r"if\s+you(?:'|’)?re|if\s+you\s+are|whether\s+you|here\s+at|thank\s+you|"
    r"we(?:'|’)?re\s+(?:excited|proud|glad|thrilled)|finding\s+the\s+right|"
    r"choosing\s+the\s+right|buying\s+a\s+(?:car|vehicle)\s+can)",
    re.I,
)
BRAND_WORDS = {"toyota", "chevrolet", "chevy", "gm", "gmc", "buick", "cadillac", "pontiac",
               "oldsmobile", "hummer", "general motors", "gm financial", "onstar"}
SUPERLATIVE_RE = re.compile(r"\b(?:best|top)\b", re.I)

RULE_ORDER = [
    "answer_first_40", "question_heading", "no_needs_fact", "phone_number",
    "no_banned_wording", "make_wall", "title_superlative",
]


def _norm(text: str) -> str:
    return (text.replace("’", "'").replace("‘", "'")
            .replace("“", '"').replace("”", '"'))


# ---------------------------------------------------------------- parsing

class _HtmlParts(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.headings: List[str] = []
        self.body: List[str] = []
        self._skip = 0
        self._in_title = False
        self._cur: Optional[List[str]] = None

    def handle_starttag(self, tag, attrs):  # noqa: ANN001
        if tag in ("script", "style"):
            self._skip += 1
        elif tag == "title":
            self._in_title = True
        elif re.fullmatch(r"h[1-6]", tag):
            self._cur = []

    def handle_endtag(self, tag):  # noqa: ANN001
        if tag in ("script", "style"):
            self._skip = max(0, self._skip - 1)
        elif tag == "title":
            self._in_title = False
        elif re.fullmatch(r"h[1-6]", tag) and self._cur is not None:
            self.headings.append(re.sub(r"\s+", " ", "".join(self._cur)).strip())
            self._cur = None
        elif tag in ("p", "li", "div", "br"):
            self.body.append("\n")

    def handle_data(self, data):  # noqa: ANN001
        if self._skip:
            return
        if self._in_title:
            self.title += data
        elif self._cur is not None:
            self._cur.append(data)
        else:
            self.body.append(data)


def _strip_front_matter(text: str) -> Tuple[Dict[str, str], str]:
    meta: Dict[str, str] = {}
    if text.startswith("---"):
        m = re.match(r"---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|$)", text, re.S)
        if m:
            for line in m.group(1).splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip().lower()] = v.strip().strip("\"'")
            return meta, text[m.end():]
    return meta, text


def _md_clean_inline(s: str) -> str:
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"^\s*(?:[-*+]|\d+\.)\s+", "", s)
    s = re.sub(r"^\s*>\s?", "", s)
    return re.sub(r"[*_`]", "", s)


def parse_page(text: str, is_html: bool) -> Dict[str, object]:
    """Return titles, headings, visible body text."""
    if is_html:
        p = _HtmlParts()
        p.feed(text)
        titles = [t for t in [re.sub(r"\s+", " ", p.title).strip()] if t]
        if p.headings:
            h1_first = p.headings[0]
            if h1_first not in titles:
                titles.append(h1_first)
        body = re.sub(r"[ \t]+", " ", "".join(p.body))
        return {"titles": titles, "headings": p.headings, "body": body}
    fm, rest = _strip_front_matter(text)
    titles = [fm["title"]] if fm.get("title") else []
    headings: List[str] = []
    body_lines: List[str] = []
    in_code = False
    for line in rest.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = re.match(r"\s{0,3}(#{1,6})\s+(.*?)\s*#*\s*$", line)
        if m:
            h = _md_clean_inline(m.group(2)).strip()
            headings.append(h)
            if len(m.group(1)) == 1 and h not in titles and len(titles) < 2:
                titles.append(h)
            body_lines.append("")
            continue
        body_lines.append(_md_clean_inline(line))
    return {"titles": titles, "headings": headings, "body": "\n".join(body_lines)}


# ---------------------------------------------------------------- rules
# Each rule returns (passed, reason).

_LONG_NUMBER_RE = re.compile(r"\+?\(?\d[\d\s().\u2010-\u2015/-]{8,}\d")


def _drop_phone_like(m: "re.Match[str]") -> str:
    """Blank out phone-sized digit runs so a phone number is not counted as an answer figure."""
    return " " if len(re.sub(r"\D", "", m.group(0))) >= 10 else m.group(0)


def rule_answer_first_40(body: str) -> Tuple[bool, str]:
    paras = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n|\n", body)]
    paras = [p for p in paras if p]
    flat = _norm(" ".join(paras))
    flat_no_phone = _LONG_NUMBER_RE.sub(_drop_phone_like, flat)
    words = flat_no_phone.split()
    if len(words) < 8:
        return False, "The page has almost no body text, so there is no direct answer."
    first40 = " ".join(words[:40])
    first_sentence = re.split(r"(?<=[.!?])\s+", _norm(paras[0]), 1)[0]
    if FILLER_OPENERS.match(first_sentence):
        return False, "The page opens with a welcome or warm-up line instead of the answer."
    if first_sentence.rstrip().endswith("?"):
        return False, "The first sentence is a question; the answer must come first."
    if re.match(r"^(?:yes|no)\b", first40, re.I):
        return True, "Opens with a yes/no answer."
    if re.search(r"\d", first40):
        return True, "The first 40 words carry a number."
    models = [w for w in pw.find_other_make(first40, "toyota") + pw.find_other_make(first40, "chevrolet")
              if w not in BRAND_WORDS]
    if models:
        return True, "The first 40 words name a specific model."
    return False, ("The first 40 words have no number, no model name and no yes/no, "
                   "so they do not answer anything specific.")


def rule_question_heading(headings: List[str]) -> Tuple[bool, str]:
    for h in headings:
        if h.strip().endswith("?"):
            return True, 'Question heading found: "%s".' % h.strip()[:80]
    return False, "No heading is phrased as a shopper's question (ending in a question mark)."


def rule_no_needs_fact(raw: str) -> Tuple[bool, str]:
    n = len(re.findall(r"\[\s*needs[\s_-]*fact[^\]]*\]", raw, re.I))
    if n:
        return False, "%d [NEEDS FACT] marker(s) remain; the owner must supply the fact." % n
    return True, "No [NEEDS FACT] markers."


def phone_numbers(raw: str) -> List[str]:
    return pw.find_phones(raw)


def rule_phone(raw: str) -> Tuple[bool, str]:
    nums = phone_numbers(raw)
    bad = [n for n in nums if n != OUR_PHONE]
    if bad:
        shown = ", ".join("%s-%s-%s" % (b[:3], b[3:6], b[6:]) for b in sorted(set(bad)))
        return False, "Phone number other than %s: %s." % (OUR_PHONE_TEXT, shown)
    if not nums:
        return True, "No phone number on the page (only %s is allowed)." % OUR_PHONE_TEXT
    return True, "Only %s appears." % OUR_PHONE_TEXT


def rule_banned_wording(raw: str) -> Tuple[bool, str]:
    found = pw.find_banned_wording(raw)
    if found:
        return False, "Banned aging or popularity wording found: " + ", ".join('"%s"' % f for f in found) + "."
    return True, "No aging or popularity wording."


def rule_make_wall(raw: str, brand: str) -> Tuple[bool, str]:
    found = pw.find_other_make(raw, brand)
    if brand == "both":
        return True, "Brand is 'both'; make wall not applied (owner reads that the two makes stay apart)."
    other = "Chevrolet" if brand == "toyota" else "Toyota"
    if found:
        return False, "%s page mentions %s: %s." % (brand.capitalize(), other, ", ".join('"%s"' % f for f in found))
    return True, "No %s models or offers on the %s page." % (other, brand.capitalize())


def rule_title_superlative(titles: List[str]) -> Tuple[bool, str]:
    if not titles:
        return False, "No title found (front matter title, H1 or <title>)."
    for t in titles:
        m = SUPERLATIVE_RE.search(pw.normalize(t))
        if m:
            return False, 'Title uses the superlative "%s": %s' % (m.group(0), t[:80])
    return True, "Title has no 'best' or 'top'."


# ---------------------------------------------------------------- warnings

def load_ai_tells(path: str) -> List[str]:
    tells: List[str] = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            s = line.strip()
            if s and not s.startswith("#"):
                tells.append(_norm(s).lower())
    return tells


def ai_tell_warnings(visible: str, tells: List[str]) -> List[Dict[str, object]]:
    text = _norm(visible)
    out: List[Dict[str, object]] = []
    for t in tells:
        rx = re.compile(r"(?<![A-Za-z0-9])" + re.sub(r"\\\s+|\\ ", r"\\s+", re.escape(t)) + r"\w*", re.I)
        n = len(rx.findall(text))
        if n:
            out.append({"phrase": t, "count": n})
    return out


# ---------------------------------------------------------------- driver

def check_page(text: str, brand: str, is_html: bool = False,
               tells_path: Optional[str] = None) -> Dict[str, object]:
    if brand not in ("toyota", "chevrolet", "both"):
        raise ValueError("brand must be toyota, chevrolet or both")
    parts = parse_page(text, is_html)
    body = str(parts["body"])
    # raw source plus the title text; public_wording also reads visible text and URL slugs
    public = text + "\n" + "\n".join(parts["titles"])  # type: ignore[arg-type]
    results = [
        ("answer_first_40",) + rule_answer_first_40(body),
        ("question_heading",) + rule_question_heading(list(parts["headings"])),  # type: ignore[arg-type]
        ("no_needs_fact",) + rule_no_needs_fact(text),
        ("phone_number",) + rule_phone(public),
        ("no_banned_wording",) + rule_banned_wording(public),
        ("make_wall",) + rule_make_wall(public, brand),
        ("title_superlative",) + rule_title_superlative(list(parts["titles"])),  # type: ignore[arg-type]
    ]
    visible = " ".join([str(parts["body"])] + list(parts["headings"]) + list(parts["titles"]))  # type: ignore[arg-type]
    warnings = ai_tell_warnings(visible, load_ai_tells(tells_path or DEFAULT_TELLS))
    if not phone_numbers(text):
        warnings.append({"phrase": "no phone number on page (%s expected)" % OUR_PHONE_TEXT, "count": 0})
    rules = [{"rule": r, "passed": ok, "reason": why} for r, ok, why in results]
    return {
        "brand": brand,
        "passed": all(r["passed"] for r in rules),
        "rules": rules,
        "warnings": warnings,
        "title": (list(parts["titles"]) or [""])[0],  # type: ignore[arg-type]
    }


def check_meta_text(fields: Dict[str, str], brand: str) -> List[Dict[str, object]]:
    """Run the shared wording rules over metadata fields and the URL slug. Returns failing rules only."""
    blob = " \n ".join(v for v in fields.values() if v)
    out = [{"rule": "meta_public_wording", "passed": False, "reason": p}
           for p in pw.check_public_text(blob, brand)]
    if fields.get("meta_title"):
        ok, why = rule_title_superlative([fields["meta_title"]])
        if not ok:
            out.append({"rule": "meta_title_superlative", "passed": False, "reason": why})
    return out


def is_html_file(path: str, text: str) -> bool:
    return path.lower().endswith((".html", ".htm")) or text.lstrip().lower().startswith(("<!doctype", "<html"))


def format_text(result: Dict[str, object], page: str) -> str:
    lines = ["Page: %s   Brand: %s" % (page, result["brand"])]
    for r in result["rules"]:  # type: ignore[union-attr]
        lines.append("%s  %s: %s" % ("PASS" if r["passed"] else "FAIL", r["rule"], r["reason"]))
    for w in result["warnings"]:  # type: ignore[union-attr]
        if w["count"]:
            lines.append('WARN  ai_tells: "%s" x%d' % (w["phrase"], w["count"]))
        else:
            lines.append("WARN  %s" % w["phrase"])
    lines.append("RESULT: %s" % ("PASS" if result["passed"] else "FAIL"))
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Page quality gate: checks a Markdown or HTML draft. Exit 0 only on pass.")
    ap.add_argument("--page", required=True, help="Markdown or HTML draft file")
    ap.add_argument("--brand", required=True, choices=["toyota", "chevrolet", "both"])
    ap.add_argument("--json", action="store_true", help="print the result as JSON")
    ap.add_argument("--tells", default=DEFAULT_TELLS, help="AI-tell word list (default: ai_tells.txt beside this script)")
    args = ap.parse_args(argv)
    try:
        with open(args.page, "r", encoding="utf-8") as fh:
            text = fh.read()
    except (OSError, UnicodeDecodeError) as exc:
        print("cannot read page: %s" % exc, file=sys.stderr)
        return 2
    try:
        result = check_page(text, args.brand, is_html_file(args.page, text), args.tells)
    except OSError as exc:
        print("cannot read word list: %s" % exc, file=sys.stderr)
        return 2
    if args.json:
        out = dict(result)
        out["page"] = args.page
        print(json.dumps(out, indent=2))
    else:
        print(format_text(result, args.page))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
