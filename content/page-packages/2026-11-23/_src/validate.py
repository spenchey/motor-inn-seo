#!/usr/bin/env python3
"""Quality gate for the 2026-11-23 page packages. Exit 1 on any failure.

Usage (from repo root): python3 content/page-packages/2026-11-23/_src/validate.py
"""
import json
import os
import re
import sys
from urllib.parse import urlsplit

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build import PAGES, OUT, ROOT, canonical  # noqa: E402

SITEMAPS = {
    "www.motorinnautogroup.com": "live-https_www_motorinnautogroup_com_sitemap_xml.html",
    "www.motorinntoyotaofcarroll.com": "live-https_www_motorinntoyotaofcarroll_com_sitemap_xml.html",
    "www.motorinnofcarroll.com": "live-https_www_motorinnofcarroll_com_sitemap_xml.html",
}
# URLs evidenced live by GSC but absent from the sitemap snapshot.
EXTRA_LIVE = set()
BANNED = ["unleash", "elevate", "seamless", "journey", "discover the difference", "unparalleled",
          "state-of-the-art", "competitive", "commitment to excellence", "and more!", "click here",
          "bad credit", "buick", "gmc", "needs-verify", "lowest price", "best price", "#1", "number one",
          "guarantee", "522-2526", "522 2526", "will have the", "already knows", "ready when you arrive",
          "offers are posted", "does not post fixed numbers", "request one online", "or use the [test drive page]", "target ai host", "not deployed", "ai-markdown-proxy", "hybrid powertrain", "lists all of them", "?type=used"]
ALLOWED_NUM = {"1526", "51401", "712", "792", "5000", "30", "20,000", "15,000", "20K", "1500", "2500HD",
               "3500HD", "2500", "2027", "150", "2", "8:00", "5:30", "7:00", "3:00", "4", "1"}
FILES = ["brief.md", "content.md", "faq.md", "meta.md", "schema.json"]


def sitemap_urls():
    live = set(EXTRA_LIVE)
    for host, f in SITEMAPS.items():
        t = open(os.path.join(ROOT, "brain", "research", f)).read()
        for u in re.findall(r"https://www\.[a-z]+\.com/[^<\"\s]*", t):
            s = urlsplit(u)
            live.add((s.netloc, s.path.rstrip("/") or "/"))
    return live


def sentences(a):
    return [x for x in re.split(r"(?<=[.!?])\s+(?=[A-Z])", a.strip()) if x]


def main():
    live = sitemap_urls()
    fails, warns = [], []
    for p in PAGES:
        slug = p["slug"]
        d = os.path.join(OUT, slug)
        def bad(msg):
            fails.append(f"[{slug}] {msg}")
        for f in FILES:
            if not os.path.isfile(os.path.join(d, f)):
                bad(f"missing {f}")
        ai = os.path.join(OUT, "ai", slug + ".md")
        if not os.path.isfile(ai):
            bad("missing ai md")
        if len(p["title"]) > 60:
            bad(f"title {len(p['title'])} > 60")
        if len(p["meta"]) > 155:
            bad(f"meta {len(p['meta'])} > 155")
        if len(p["og_desc"]) > 200:
            bad("og desc too long")
        # schema
        try:
            sch = json.load(open(os.path.join(d, "schema.json")))
        except Exception as e:  # noqa: BLE001
            bad(f"schema.json invalid: {e}")
            continue
        faqnode = [n for n in sch["@graph"] if n["@type"] == "FAQPage"][0]
        sq = [q["name"] for q in faqnode["mainEntity"]]
        faqmd = open(os.path.join(d, "faq.md")).read()
        fq = re.findall(r"^## (.+)$", faqmd, re.M)
        content = open(os.path.join(d, "content.md")).read()
        cq = re.findall(r"^### (.+)$", content, re.M)
        if not (sq == fq == cq):
            bad("FAQ mismatch between schema/faq.md/content.md")
        if not 3 <= len(sq) <= 6:
            bad(f"FAQ count {len(sq)} not 3-6")
        for q, a in p["faq"]:
            n = len(sentences(a))
            if not 2 <= n <= 4:
                bad(f"FAQ answer has {n} sentences: {q}")
        # H2s are questions
        for h2 in re.findall(r"^## (.+)$", content, re.M):
            if not h2.endswith("?"):
                bad(f"H2 not a question: {h2}")
        # customer-facing text checks
        cust = content + "\n" + open(ai).read() + "\n" + json.dumps(sch) + "\n" + open(os.path.join(d, "meta.md")).read()
        low = cust.lower()
        for w in BANNED:
            if w in low:
                bad(f"banned term '{w}'")
        if content.count("!") > 1:
            bad("more than one exclamation mark")
        if "(712) 792-5000" not in content:
            bad("canonical phone missing from content.md")
        for tracking in ["877-775-6741", "877-733-5984", "513-1061", "513-1075", "513-1068", "513-1035"]:
            if tracking in cust:
                bad(f"tracking number printed: {tracking}")
        # numbers in copy (strip URLs and phone) must be on the allow list
        stripped = re.sub(r"\(https?://[^)]+\)|https?://\S+", "", content)
        stripped = stripped.replace("(712) 792-5000", "").replace("IA 51401", "")
        for tok in re.findall(r"\$?\d[\d,:]*[A-Za-z]*", stripped):
            t = tok.lstrip("$").rstrip(",")
            if t not in ALLOWED_NUM:
                bad(f"unlisted number in copy: {tok}")
        # links
        for u in set(re.findall(r"\((https://www\.[^)\s]+)\)", content + open(ai).read())):
            s = urlsplit(u)
            key = (s.netloc, s.path.rstrip("/") or "/")
            if key not in live:
                bad(f"link not in sitemap snapshot: {u}")
            if s.query:
                warns.append(f"[{slug}] filtered link needs click-test: {u}")
        for anchor, href, _ in p["links"]:
            s = urlsplit(href)
            if (s.netloc, s.path.rstrip("/") or "/") not in live:
                bad(f"brief link not live: {href}")
        # brand-host consistency: page host must match store
        if urlsplit(canonical(p)).netloc not in SITEMAPS:
            bad("unknown host")
        if (urlsplit(canonical(p)).netloc, p["path"]) in live and p["status"].startswith("NEW"):
            bad("marked NEW but URL already in sitemap")
    print(f"checked {len(PAGES)} packages")
    for w in sorted(set(warns)):
        print("WARN", w)
    for f in fails:
        print("FAIL", f)
    print("RESULT:", "PASS" if not fails else f"FAIL ({len(fails)})")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
