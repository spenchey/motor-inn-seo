#!/usr/bin/env python3
"""QA for the 2026-11-23 DealerOn handoff. Writes deliveries/dealeron-handoff-2026-11-23/_qa/.

Usage (repo root): python3 content/page-packages/2026-11-23/_src/handoff_qa.py [--screens]
Exit 1 on any failure.
"""
import json
import os
import re
import subprocess
import sys
import zipfile
from urllib.parse import urlsplit

from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build import PAGES, build_schema, canonical  # noqa: E402
from handoff import OUT, SITE_DIR, CHROME, CHROME_FOR, is_inplace  # noqa: E402
from validate import sitemap_urls  # noqa: E402

QA = os.path.join(OUT, "_qa")
SHELL = os.path.expanduser("~/Library/Caches/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-mac-arm64/chrome-headless-shell")
BAD = ["522-2526", "877-775-6741", "877-733-5984", "513-1061", "513-1075", "513-1068", "513-1035",
       "Placement (in-place", "draft-needs-owner-approval", "Target AI host"]


def norm(t):
    return re.sub(r"\s+", " ", t).strip()


def main(screens):
    live = sitemap_urls()
    os.makedirs(QA, exist_ok=True)
    rows, fails = [], []
    for p in PAGES:
        d = os.path.join(OUT, "pages", SITE_DIR[p["store"]], p["slug"])
        r = {"slug": p["slug"], "checks": {}}
        def chk(name, ok, detail=""):
            r["checks"][name] = "PASS" if ok else f"FAIL {detail}".strip()
            if not ok:
                fails.append(f"[{p['slug']}] {name}: {detail}")
        frag_src = open(os.path.join(d, "index.html")).read()
        frag = BeautifulSoup(frag_src, "html.parser")
        text = norm(frag.get_text(" "))
        chk("no_h1_in_body", frag.find("h1") is None)
        h2s = [norm(h.get_text()) for h in frag.find_all("h2")]
        chk("h2_questions", all(h.endswith("?") for h in h2s), str([h for h in h2s if not h.endswith("?")]))
        chk("faq_visible", all(norm(q) in text and norm(a) in text for q, a in p["faq"]))
        ld = [json.loads(s.string) for s in frag.find_all("script", type="application/ld+json")]
        chk("jsonld_matches_schema", len(ld) == 1 and ld[0] == build_schema(p))
        chk("phone_present", "(712) 792-5000" in text)
        low = frag_src
        chk("no_banned_strings", not any(b in low for b in BAD), str([b for b in BAD if b in low]))
        bad_links = []
        for a in frag.find_all("a", href=True):
            h = a["href"]
            if h.startswith("tel:"):
                continue
            s = urlsplit(h)
            if (s.netloc, s.path.rstrip("/") or "/") not in live:
                bad_links.append(h)
        chk("links_live_in_sitemaps", not bad_links, str(bad_links))
        ids = [el.get("id") for el in frag.find_all(id=True)]
        chk("no_ids_in_body", not ids, str(ids))
        # full html
        full_src = open(os.path.join(d, "full-html", "index.html")).read()
        full = BeautifulSoup(full_src, "html.parser")
        chrome = BeautifulSoup(open(os.path.join(CHROME, CHROME_FOR.get(p["slug"]) or CHROME_FOR[p["store"]]), errors="ignore").read(), "html.parser")
        h1s = full.find_all("h1")
        chk("one_h1", len(h1s) == 1, str(len(h1s)))
        cm = full.find(id="content-main")
        chk("body_inside_content_main", cm is not None and cm.find(attrs={"data-package": p["slug"]}) is not None)
        canon = (full.find("link", rel="canonical") or {}).get("href")
        chk("canonical", canon == canonical(p), str(canon))
        if is_inplace(p):
            chk("title_unchanged_cycle1", norm(full.title.get_text()) == norm(chrome.title.get_text()))
            chk("h1_unchanged_cycle1", norm(h1s[0].get_text()) == norm(chrome.find("h1").get_text()))
        else:
            chk("title", norm(full.title.get_text()) == p["title"])
            chk("meta_description", (full.find("meta", attrs={"name": "description"}) or {}).get("content") == p["meta"])
            chk("h1", norm(h1s[0].get_text()) == p["h1"])
        if p["slug"] == "contactus-carroll":
            form = full.find("form", id="ContactUsForm")
            block = full.find(attrs={"data-package": p["slug"]})
            pos = full_src.find('id="ContactUsForm"'), full_src.find('data-package="contactus-carroll"')
            chk("form_kept_and_first", form is not None and block is not None and 0 <= pos[0] < pos[1])
        dup = {}
        for el in full.find_all(id=True):
            dup[el["id"]] = dup.get(el["id"], 0) + 1
        dups = [k for k, v in dup.items() if v > 1]
        chrome_dups = {k for k, v in {e["id"]: sum(1 for _ in chrome.find_all(id=e["id"])) for e in chrome.find_all(id=True)}.items() if v > 1}
        new_dups = [k for k in dups if k not in chrome_dups]
        chk("no_new_duplicate_ids", not new_dups, str(new_dups))
        chk("no_banned_in_full", "522-2526" not in full_src, "522-2526 present")
        rel = [el.get("src") or el.get("href") for el in full.find_all(["script", "link"]) if (el.get("src") or el.get("href") or "").startswith("/") and not (el.get("src") or el.get("href")).startswith("//")]
        chk("assets_absolute", not rel, str(rel[:3]))
        if screens and os.path.exists(SHELL):
            for w in (390, 1280):
                png = os.path.join(QA, f"{p['slug']}-{w}.png")
                subprocess.run([SHELL, "--hide-scrollbars", f"--window-size={w},2400",
                                "--virtual-time-budget=8000", f"--screenshot={png}",
                                "file://" + os.path.join(d, "full-html", "index.html")],
                               capture_output=True, timeout=90)
                chk(f"screenshot_{w}", os.path.exists(png) and os.path.getsize(png) > 10000)
        rows.append(r)
    # zip contents
    with zipfile.ZipFile(OUT + ".zip") as z:
        names = set(z.namelist())
    expect = set()
    for base, _, files in os.walk(OUT):
        rel = os.path.relpath(base, OUT)
        if rel.split(os.sep)[0] in ("_chrome", "_qa"):
            continue
        expect |= {os.path.relpath(os.path.join(base, f), OUT) for f in files}
    zip_ok = names == expect
    if not zip_ok:
        fails.append(f"zip mismatch: missing {sorted(expect - names)[:5]} extra {sorted(names - expect)[:5]}")
    os.makedirs(QA, exist_ok=True)
    json.dump({"pages": rows, "zip_matches_folder": zip_ok, "fails": fails}, open(os.path.join(QA, "qa-results.json"), "w"), indent=2)
    names_ = list(rows[0]["checks"].keys())
    allnames = []
    for r in rows:
        for k in r["checks"]:
            if k not in allnames:
                allnames.append(k)
    md = ["# Handoff QA (2026-11-23)", "", f"Result: **{'PASS' if not fails else 'FAIL'}**, with {len(PAGES)} pages and zip contents matching the folder: {zip_ok}.", "",
          "Static checks: body has no H1; H2s are questions; FAQ visible; JSON-LD equals schema.json; phone present; no banned or tracking numbers or workflow text; every link is in the live sitemaps; no IDs in the body. "
          "Full page: one H1; body inside #content-main; canonical; title/meta/H1 (new pages) or unchanged title/H1 (cycle-1 updates); contact form kept first; no new duplicate IDs; no 522-2526; assets absolute. "
          "Screenshots at 390px and 1280px come from headless Chromium loading the live DealerOn CSS/JS. They're for visual review; they don't measure overflow.", "",
          "| Page | " + " | ".join(allnames) + " |", "|---|" + "---|" * len(allnames)]
    for r in rows:
        md.append(f"| {r['slug']} | " + " | ".join(("✓" if r['checks'].get(k) == "PASS" else (r['checks'].get(k) or "n/a")) for k in allnames) + " |")
    md += ["", "## Visual review notes (2026-11-23)",
           "- /contactus.aspx preview: the live form stays first; the new block renders below it in the site's styles.",
           "- motorinnofcarroll.com pages: the site-wide \"Red Tag\" promo banner (live template, dismissible) overlaps the top of the content area in screenshots and hides the H1 until it's closed. The live /aboutus.aspx shows the same; it isn't caused by this package.",
           "- motorinnofcarroll.com header and footer print the site's own tracking numbers (877-...). That's DealerOn chrome, not package copy; the package body uses (712) 792-5000 only."]
    if fails:
        md += ["", "## Failures"] + [f"- {f}" for f in fails]
    open(os.path.join(QA, "qa-results.md"), "w").write("\n".join(md) + "\n")
    print("\n".join(fails) if fails else "QA PASS")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main("--screens" in sys.argv)
