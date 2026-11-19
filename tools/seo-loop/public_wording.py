"""Shared public-wording rules for Motor Inn (SA-19).

One module that every gate imports, so the word lists live in one place:
  normalize, visible_text, find_banned_wording, find_phones,
  find_other_make, check_public_text.

Standard library only. No network. Python 3.9 compatible.
"""
from __future__ import annotations

import argparse
import html
import re
import sys
import unicodedata
from typing import Iterable, List, Sequence
from urllib.parse import unquote

DEALER_PHONE = "7127925000"

# --------------------------------------------------------------------------
# Normalizing
# --------------------------------------------------------------------------

_INVISIBLE = dict.fromkeys(map(ord, "\u200b\u200c\u200d\u2060\ufeff\u00ad\u200e\u200f"), None)
_APOSTROPHES = dict.fromkeys(map(ord, "\u2018\u2019\u201b\u02bc\u2032`\u00b4"), "'")


def _unescape(text: str) -> str:
    """Decode HTML entities, repeating so &amp;nbsp; also decodes."""
    for _ in range(3):
        new = html.unescape(text)
        if new == text:
            break
        text = new
    return text


def _fold(text, lower: bool) -> str:
    if text is None:
        return ""
    text = str(text)
    text = _unescape(text)
    text = unicodedata.normalize("NFKC", text)
    text = text.translate(_INVISIBLE).translate(_APOSTROPHES)
    out = []
    for ch in text:
        cat = unicodedata.category(ch)
        if cat == "Pd" or ch == "\u2212":
            out.append("-")
        elif cat in ("Zs", "Zl", "Zp") or ch in "\t\r\n\x0b\x0c\u0085":
            out.append(" ")
        else:
            out.append(ch)
    text = re.sub(r"\s+", " ", "".join(out)).strip()
    return text.lower() if lower else text


def normalize(text) -> str:
    """NFKC, HTML entities decoded, every dash as '-', odd spaces as ' ',
    whitespace collapsed, lower-case."""
    return _fold(text, True)


_BLOCK_TAGS = frozenset(
    "address article aside blockquote br dd div dl dt fieldset figcaption figure footer form "
    "h1 h2 h3 h4 h5 h6 header hr li main nav ol p pre section table tbody td tfoot th thead tr "
    "ul title option summary details".split())
_COMMENT_RE = re.compile(r"<!--.*?(?:-->|$)", re.S)
_SCRIPT_RE = re.compile(r"<(script|style)\b[^>]*>.*?(?:</\1\s*>|$)", re.S | re.I)
_TAG_RE = re.compile(r"</?([A-Za-z][A-Za-z0-9:-]*)\b[^>]*>")
_MD_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\([^)]*\)")
_MD_LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")
_MD_ESCAPE_RE = re.compile(r"\\([*_~`\[\]()])")


def _tag_sub(m) -> str:
    return " " if m.group(1).lower() in _BLOCK_TAGS else ""


def _strip_markup(text) -> str:
    """Remove comments, script/style, tags and Markdown markers (case kept)."""
    if text is None:
        return ""
    text = str(text)
    text = _COMMENT_RE.sub(" ", text)
    text = _SCRIPT_RE.sub(" ", text)
    text = _TAG_RE.sub(_tag_sub, text)
    text = _MD_IMAGE_RE.sub(r"\1", text)
    text = _MD_LINK_RE.sub(r"\1", text)
    text = _MD_ESCAPE_RE.sub(r"\1", text)
    text = re.sub(r"[*~`]+", "", text)
    text = re.sub(r"(?<![A-Za-z0-9])_+|_+(?![A-Za-z0-9])", "", text)
    return text


def visible_text(text) -> str:
    """What a reader sees: tags, script/style content and Markdown emphasis
    markers removed, link text kept, entities decoded, whitespace collapsed.
    Case is kept. URLs are checked separately (see _views)."""
    return _fold(_strip_markup(text), False)


def _slug_view(norm_text: str) -> str:
    """Read URL separators as spaces so 'best-seller-silverado' is visible."""
    text = unquote(norm_text)
    return re.sub(r"\s+", " ", re.sub(r"[-_/.+?&=#:]+", " ", text)).strip()


def _views(text) -> List[str]:
    """Every form of the text a rule is checked against."""
    raw = normalize(unquote(str(text)) if text is not None else "")
    vis = normalize(_strip_markup(text))
    views = []
    for v in (raw, vis, _slug_view(raw), _slug_view(vis)):
        if v and v not in views:
            views.append(v)
    return views


# --------------------------------------------------------------------------
# Banned wording
# --------------------------------------------------------------------------

_S = r"[\s_-]+"      # a separator between words
_S0 = r"[\s_-]*"     # an optional separator (bestseller / best seller / best-seller)
_L = r"(?<![a-z0-9])"
_R = r"(?![a-z0-9])"

_BANNED_SOURCES = [
    # popularity and demand
    r"popular(?:ity)?",
    r"best" + _S0 + r"sell(?:er|ers|ing)",
    r"top" + _S0 + r"sell(?:er|ers|ing)",
    r"hot" + _S0 + r"sell(?:er|ers|ing)",
    r"#\s*1" + _S0 + r"sell(?:er|ers|ing)",
    r"(?:no\.?|number)\s*(?:1|one)" + _S0 + r"sell(?:er|ers|ing)",
    r"(?:fan|customer|crowd|shopper)" + _S0 + r"favou?rites?",
    r"sell(?:s|ing)" + _S + r"fast",
    r"sold" + _S + r"fast",
    r"(?:in" + _S + r")?high" + _S + r"demand",
    r"demand" + _S + r"(?:stays|remains|is|stay)" + _S + r"(?:strong|high)",
    r"fl(?:y|ies|ying)" + _S + r"off" + _S + r"(?:the" + _S + r")?(?:lot|shelves|shelf)",
    r"flying" + _S + r"off",
    r"won'?t" + _S + r"last",
    r"will" + _S + r"not" + _S + r"last",
    r"going" + _S + r"fast",
    r"beat" + _S + r"the" + _S + r"rush",
    # how long a vehicle has been on the lot
    r"days?" + _S + r"(?:on|at|in)" + _S + r"(?:the" + _S + r"|our" + _S + r"|a" + _S + r"|my" + _S + r")?(?:lot|stock|inventory)",
    r"ag(?:ed|ing)" + _S + r"(?:inventory|stock|units?|vehicles?)",
    r"(?:sit|sits|sitting|sat)" + _S + r"on" + _S + r"(?:the" + _S + r"|our" + _S + r"|a" + _S + r"|this" + _S + r")?lot",
    r"(?:been|being)" + _S + r"(?:on|at|sitting" + _S + r"on)" + _S + r"(?:the" + _S + r"|our" + _S + r")?lot",
    r"on" + _S + r"(?:the|our)" + _S + r"lot" + _S + r"for" + _S + r"\d+",
    r"been" + _S + r"(?:here|in" + _S + r"stock)" + _S + r"(?:for" + _S + r")?\d+" + _S + r"(?:days?|weeks?|months?)",
    r"oldest" + _S + r"(?:inventory|units?|stock)",
    r"must" + _S + r"go",
]
# '#1 selling' starts with a non-word character, so it has no left boundary.
_BANNED_RES = [re.compile((s if s.startswith("#") else _L + s) + _R, re.I) for s in _BANNED_SOURCES]


def _collapse(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().lower()


def find_banned_wording(text) -> List[str]:
    """Return the matched banned phrases (lower-case, no duplicates).

    Checks the normalized raw text, the visible text, and URL slugs with
    hyphens read as spaces."""
    found: List[str] = []
    for view in _views(text):
        for rx in _BANNED_RES:
            for m in rx.finditer(view):
                phrase = _collapse(m.group(0))
                if phrase not in found:
                    found.append(phrase)
    return found


# --------------------------------------------------------------------------
# Phones
# --------------------------------------------------------------------------

_SEP = r"[\s.\-/\u2022\u00b7)(]{0,4}"
_PHONE_RE = re.compile(
    r"(?<!\d)(?:\+?1" + _SEP + r")?\(?(\d{3})" + _SEP + r"(\d{3})" + _SEP + r"(\d{4})(?!\d)")


def _digits10(value) -> str:
    d = re.sub(r"\D", "", normalize(value))
    if len(d) == 11 and d.startswith("1"):
        d = d[1:]
    return d


def find_phones(text) -> List[str]:
    """Return every phone number as 10 digits, in order of appearance.

    Reads (712)882-7802, 712.882.7802, 712 882 7802, any dash, +1 prefixes,
    tel: links and bare digits. Checks raw text and visible text."""
    found: List[str] = []
    for view in (normalize(unquote(str(text))) if text is not None else "",
                 normalize(_strip_markup(text))):
        for m in _PHONE_RE.finditer(view):
            num = m.group(1) + m.group(2) + m.group(3)
            if num not in found:
                found.append(num)
    return found


# --------------------------------------------------------------------------
# Other make
# --------------------------------------------------------------------------

def _model(name: str) -> str:
    """Pattern for a model name: spaces or hyphens between words, optional plural."""
    parts = [re.escape(p) for p in name.split()]
    return r"[\s-]*".join(parts)


_CHEVROLET_NAMES = [
    "chevrolet", "chevy", "silverado", "colorado", "blazer", "equinox", "trax", "traverse",
    "tahoe", "suburban", "malibu", "corvette", "camaro", "trailblazer", "impala", "cruze",
    "sonic", "avalanche", "monte carlo", "el camino", "hhr", "express van", "city express",
    "bolt ev", "bolt euv",
]
_GM_NAMES = [
    "gmc", "gm", "gm financial", "general motors", "buick", "cadillac", "pontiac",
    "oldsmobile", "hummer", "onstar",
]
_TOYOTA_NAMES = [
    "toyota", "camry", "corolla", "corolla cross", "gr corolla", "crown", "crown signia",
    "prius", "rav4", "highlander", "grand highlander", "4runner", "sequoia", "land cruiser",
    "tacoma", "tundra", "sienna", "venza", "bz4x", "gr86", "supra", "gr supra", "avalon",
    "c-hr", "yaris", "mirai", "fj cruiser", "celica", "solara", "mr2", "prius prime",
    "toyota tacoma",
]

# 'bolt' alone is a Chevrolet model, but also hardware in a service sentence.
_BOLT = (r"(?<!lug )(?<!wheel )(?<!drain )(?<!axle )(?<!head )(?<!anchor )(?<!oil )(?<!u-)"
         r"bolt(?!s)(?![- ]?(?:pattern|on\b|in\b|up\b|holes?\b|torque))")


def _compile_names(names: Iterable[str], extra: Sequence[str] = ()):
    pats = []
    for n in names:
        if n == "gr86":
            pats.append(r"gr[\s-]*86")
        elif n == "bz4x":
            pats.append(r"bz[\s-]*4x")
        elif n == "rav4":
            pats.append(r"rav[\s-]*4")
        elif n == "4runner":
            pats.append(r"4[\s-]*runner")
        elif n == "c-hr":
            pats.append(r"c[\s-]*hr")
        elif n == "land cruiser":
            pats.append(r"land[\s-]*cruiser")
        elif n == "gm":
            pats.append(r"gm")
        else:
            pats.append(_model(n))
    pats.extend(extra)
    return re.compile(r"(?<![a-z0-9])(?:" + "|".join("(?:%s)" % p for p in pats) + r")(?:s|'s)?(?![a-z0-9])", re.I)


_CHEVY_RE = _compile_names(_CHEVROLET_NAMES + _GM_NAMES, extra=(_BOLT,))
_TOYOTA_RE = _compile_names(_TOYOTA_NAMES)


def _brand_key(brand) -> str:
    b = normalize(brand)
    if b in ("chevy", "chevrolet"):
        return "chevrolet"
    if b in ("toyota",):
        return "toyota"
    if b in ("both", "group", "motor inn", "motorinn"):
        return "both"
    raise ValueError("brand must be toyota, chevrolet or both, got %r" % (brand,))


def find_other_make(text, brand) -> List[str]:
    """Return mentions of the other make (whole words, any case).

    brand 'toyota' -> Chevrolet, Chevy, GM brands and Chevrolet model names.
    brand 'chevrolet' -> Toyota and Toyota model names.
    brand 'both' -> nothing."""
    key = _brand_key(brand)
    if key == "both":
        return []
    rx = _CHEVY_RE if key == "toyota" else _TOYOTA_RE
    found: List[str] = []
    for view in _views(text):
        for m in rx.finditer(view):
            word = _collapse(m.group(0))
            if word not in found:
                found.append(word)
    return found


# --------------------------------------------------------------------------
# One call for the gates
# --------------------------------------------------------------------------

def _pretty_phone(d: str) -> str:
    return "%s-%s-%s" % (d[:3], d[3:6], d[6:])


def check_public_text(text, brand, allowed_phones=(DEALER_PHONE,)) -> List[str]:
    """Return plain-English problems; an empty list means the wording is clean."""
    problems: List[str] = []
    for phrase in find_banned_wording(text):
        problems.append('Banned wording "%s": popularity, demand and how-long-on-the-lot '
                        "wording may not appear in public text." % phrase)
    key = _brand_key(brand)
    other = "Chevrolet" if key == "toyota" else "Toyota"
    for word in find_other_make(text, brand):
        problems.append('Mentions "%s", which belongs to %s. A %s page must not mention %s.'
                        % (word, other, key.capitalize(), other))
    allowed = set(_digits10(p) for p in allowed_phones)
    for num in find_phones(text):
        if num not in allowed:
            problems.append("Phone number %s is not an approved number. Only %s may appear."
                            % (_pretty_phone(num), ", ".join(_pretty_phone(a) for a in sorted(allowed)) or "none"))
    return problems


def _main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Check public Motor Inn wording from a file or stdin.")
    ap.add_argument("--brand", required=True, choices=["toyota", "chevrolet", "both"])
    ap.add_argument("--file", help="text file to check; default is stdin")
    args = ap.parse_args(argv)
    if args.file:
        with open(args.file, encoding="utf-8") as fh:
            data = fh.read()
    else:
        data = sys.stdin.read()
    problems = check_public_text(data, args.brand)
    for p in problems:
        print(p)
    print("RESULT: %s" % ("FAIL" if problems else "CLEAN"))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(_main())
