#!/usr/bin/env python3
"""Build the LEG B DealerOn handoff for the 2026-11-23 page packages.

Usage (repo root): python3 content/page-packages/2026-11-23/_src/handoff.py
Reads the page specs (same source as build.py) and the live chrome captures in
deliveries/dealeron-handoff-2026-11-23/_chrome/, and writes
deliveries/dealeron-handoff-2026-11-23/ plus a zip next to it. Nothing is sent or published.
"""
import csv
import html
import io
import json
import os
import re
import sys
import zipfile

from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import facts as F  # noqa: E402
from build import PAGES, ROOT, build_schema, canonical  # noqa: E402

OUT = os.path.join(ROOT, "deliveries", "dealeron-handoff-2026-11-23")
CHROME = os.path.join(OUT, "_chrome")
CAPTURED = "2026-11-23T18:29Z"
SITE_DIR = {"group": "motorinnautogroup", "chevy": "motorinnofcarroll", "toyota": "motorinntoyotaofcarroll"}
# Chrome source per page: new pages reuse each host's live About Us inner page (DealerOn content template);
# in-place pages use the live target page itself.
CHROME_FOR = {"contactus-carroll": "group-contactus.html", "used-cars-carroll-iowa": "group-usedcars.html",
              "chevy": "chevy-aboutus.html", "toyota": "toyota-aboutus.html"}
STATUS = "draft-needs-owner-approval"


# ---------- markdown subset -> HTML ----------
def inline(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", lambda m: f'<a href="{html.escape(m.group(2))}">{m.group(1)}</a>', text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    return text


def blocks(md):
    out, items = [], []
    for raw in md.strip().split("\n"):
        line = raw.rstrip()
        if line.startswith("- "):
            items.append(f"<li>{inline(line[2:])}</li>")
            continue
        if items:
            out.append("<ul>" + "".join(items) + "</ul>")
            items = []
        if line:
            out.append(f"<p>{inline(line)}</p>")
    if items:
        out.append("<ul>" + "".join(items) + "</ul>")
    return "\n".join(out)


def is_inplace(p):
    return bool(p.get("placement"))


def body_html(p):
    """Body-only fragment for the DealerOn content editor."""
    s = F.STORES[p["store"]]
    parts = [f'<div class="mi-2026-11-23" data-package="{p["slug"]}">']
    if is_inplace(p):
        # Cycle 1: the page keeps its existing H1; the proposed heading is styled text only.
        parts.append(f'<p class="lead"><strong>{html.escape(p["h1"])}</strong></p>')
    parts.append(blocks(p["intro"]))
    parts.append(f'<p class="lead"><strong>{inline(p["cta"])}</strong></p>')
    for h2, body in p["sections"]:
        parts.append(f"<h2>{html.escape(h2)}</h2>\n{blocks(body)}")
    parts.append("<h2>What else do Carroll shoppers ask?</h2>")
    for q, a in p["faq"]:
        parts.append(f"<h3>{html.escape(q)}</h3>\n<p>{html.escape(a)}</p>")
    parts.append("<h2>Where do I find us?</h2>")
    parts.append(f"<p>{html.escape(s['name'])} is at {html.escape(F.ADDRESS_LINE)}, {F.LANDMARK} in Carroll. Call "
                 f'<a href="tel:+17127925000">{F.PHONE}</a>.</p>')
    parts.append("<ul>"
                 f"<li><strong>Address:</strong> {html.escape(F.ADDRESS_LINE)}</li>"
                 f'<li><strong>Phone:</strong> <a href="tel:+17127925000">{F.PHONE}</a></li>'
                 f"<li><strong>Sales hours:</strong> {html.escape(F.HOURS_TEXT)}. Service hours are on the "
                 f'<a href="{s["url"]}hours.aspx">hours page</a>.</li></ul>')
    parts.append(f'<p class="lead"><strong>{inline(p["cta"])}</strong></p>')
    parts.append('<script type="application/ld+json">' + json.dumps(build_schema(p), ensure_ascii=False, separators=(",", ":")) + "</script>")
    parts.append("</div>")
    return "\n".join(parts)


# ---------- full-page fallback ----------
def absolutize(soup, origin):
    for tag, attr in (("a", "href"), ("link", "href"), ("script", "src"), ("img", "src"), ("source", "srcset"), ("form", "action")):
        for el in soup.find_all(tag):
            v = el.get(attr)
            if isinstance(v, str) and v.startswith("/") and not v.startswith("//"):
                el[attr] = origin + v


def set_meta(soup, name, value, prop=False):
    key = "property" if prop else "name"
    el = soup.find("meta", attrs={key: name})
    if el is None:
        el = soup.new_tag("meta")
        el[key] = name
        soup.head.append(el)
    el["content"] = value


def full_html(p, fragment):
    host_origin = "https://" + F.STORES[p["store"]]["host"]
    src = CHROME_FOR.get(p["slug"]) or CHROME_FOR[p["store"]]
    soup = BeautifulSoup(open(os.path.join(CHROME, src), errors="ignore").read(), "html.parser")
    frag = BeautifulSoup(fragment, "html.parser")
    cm = soup.find(id="content-main")
    if cm is None:
        raise SystemExit(f"[{p['slug']}] no #content-main in {src}")
    if p["slug"] == "contactus-carroll":
        # Cycle 1: keep the live form block, add ours below it. Title/meta/H1 stay as they are live.
        cm.append(frag)
    else:
        live_h1 = cm.find("h1") if is_inplace(p) else None
        cm.clear()
        if live_h1 is not None:
            # Cycle 1 keeps the live H1 (it sits inside the editable body on this page).
            cm.append(live_h1)
        cm.append(frag)
        if not is_inplace(p):
            # New page: our title/meta/canonical/H1.
            soup.title.string = p["title"]
            set_meta(soup, "description", p["meta"])
            set_meta(soup, "og:title", p["og_title"], prop=True)
            set_meta(soup, "og:description", p["og_desc"], prop=True)
            set_meta(soup, "og:url", canonical(p), prop=True)
            link = soup.find("link", rel="canonical")
            if link is None:
                link = soup.new_tag("link", rel="canonical")
                soup.head.append(link)
            link["href"] = canonical(p)
            h1 = soup.find(id="content-description").find("h1")
            h1.string = p["h1"]
    absolutize(soup, host_origin)
    return str(soup)


# ---------- docs ----------
def placement(p):
    s = F.STORES[p["store"]]
    url = canonical(p)
    L = [f"# {p['slug']}: placement instructions", "",
         f"**Status:** `{STATUS}`. Do not publish until Spencer approves in writing.",
         f"**Site:** {s['host']} ({s['name']})",
         f"**URL path:** {p['path']}", f"**Canonical:** {url}", ""]
    if is_inplace(p):
        L += ["## Type: update to an EXISTING page (cycle 1 of 2)", "",
              p["placement"], "",
              "- **Keep the page's current title, meta description and H1 exactly as they are live.** The values in metadata-all.csv marked `cycle2_*` are for a later, separate request.",
              "- Paste `index.html` into the page's editable content region."]
        if p["slug"] == "contactus-carroll":
            L += ["- Place it **below the existing contact form**. The form must stay first on the page.",
                  "- Do not change the form, its fields or its consent text."]
        else:
            L += ["- Keep the page's existing H1 (\"Used cars in Carroll, Iowa\", which sits at the top of the editable body) exactly as it is.",
                  "- Replace everything in the body **below that H1** with `index.html`. This also removes the outdated phone number (712) 522-2526 that the live page currently shows three times."]
        L += ["- `full-html/index.html` is a **placement preview** built from the live page captured " + CAPTURED + ". It is for checking position only, not for upload."]
    else:
        L += ["## Type: NEW content page", "",
              "- Create a standard DealerOn content page at the path above using the site's existing header, nav and footer.",
              f"- **Page title:** {p['title']}",
              f"- **Meta description:** {p['meta']}",
              f"- **H1:** {p['h1']}",
              f"- Breadcrumb: Home > {p['h1'].split(':')[0]}",
              "- Paste `index.html` into the page body. `full-html/index.html` is a full-page fallback built on this site's live inner-page template (captured " + CAPTURED + ").",
              "- Do not add the page to the main navigation unless Spencer asks."]
    L += ["", "## Structured data",
          "- The body ends with one JSON-LD block (WebPage + AutoDealer + FAQPage). Keep it with the visible FAQ section, and keep the site's own sitewide schema too.", "",
          "## Redirects", "- None for this page in this request."]
    if p["slug"] == "contactus-carroll":
        L += ["- A **separate, later** request (EMAIL-DRAFTS/04) will 301 /car-dealerships-carroll-iowa, /car-dealerships-in-carroll-iowa.html and /car-dealership-carroll-iowa to /contactus.aspx. Do not do that as part of this page update."]
    L += ["", "## Internal links", "- Links inside the body point only to pages that already exist (checked against the live sitemaps and a live link check on 2026-11-23)."]
    if p.get("post_links"):
        L += ["- After this page is live, add these links (Spencer will confirm):"] + [f"  - {x}" for x in p["post_links"]]
    return "\n".join(L) + "\n"


def csv_rows():
    rows = []
    for p in PAGES:
        inplace = is_inplace(p)
        rows.append({
            "slug": p["slug"], "site": F.STORES[p["store"]]["host"], "url_path": p["path"], "canonical": canonical(p),
            "action": "update-existing (cycle 1: body only)" if inplace else "new-page",
            "title": "(keep live title)" if inplace else p["title"],
            "meta_description": "(keep live meta)" if inplace else p["meta"],
            "h1": "(keep live H1)" if inplace else p["h1"],
            "cycle2_title": p["title"] if inplace else "", "cycle2_meta": p["meta"] if inplace else "", "cycle2_h1": p["h1"] if inplace else "",
            "schema_types": "WebPage; AutoDealer; FAQPage", "faq_count": len(p["faq"]), "status": STATUS,
        })
    return rows


EMAILS = {
    "01-group-site-content-updates.md": ("www.motorinnautogroup.com", ["contactus-carroll", "used-cars-carroll-iowa"],
        "Content updates to 2 existing pages on motorinnautogroup.com",
        "Please update the body content of two existing pages on www.motorinnautogroup.com. **Do not change their titles, meta descriptions or H1s in this request.**\n\n"
        "1. **/contactus.aspx**: add the content in `pages/motorinnautogroup/contactus-carroll/index.html` **below the existing contact form**. The form stays first and unchanged.\n"
        "2. **/used-cars-carroll-iowa**: replace the current body copy with `pages/motorinnautogroup/used-cars-carroll-iowa/index.html`. This also removes an outdated phone number, (712) 522-2526, from the live page."),
    "02-chevy-site-new-pages.md": ("www.motorinnofcarroll.com", None,
        "4 new content pages on motorinnofcarroll.com (Motor Inn of Carroll)",
        "Please create four new content pages on www.motorinnofcarroll.com, using the site's existing header, nav and footer."),
    "03-toyota-site-new-pages.md": ("www.motorinntoyotaofcarroll.com", None,
        "3 new content pages on motorinntoyotaofcarroll.com",
        "Please create three new content pages on www.motorinntoyotaofcarroll.com, using the site's existing header, nav and footer."),
}


def email(fname, spec):
    host, slugs, subject, intro = spec
    pages = [p for p in PAGES if F.STORES[p["store"]]["host"] == host and (slugs is None or p["slug"] in slugs)]
    L = ["# DRAFT, NOT SENT", "",
         f"Status: `{STATUS}`. Send only after Spencer approves the copy. One issue per email (house rule).", "",
         "**To:** support@dealeron.com",
         f"**Subject:** {subject}", "", "---", "", "Hi DealerOn team,", "", intro, ""]
    if slugs is None:
        L += ["| URL path | Page title | Package folder |", "|---|---|---|"]
        L += [f"| {p['path']} | {p['title'].replace('|', chr(92) + '|')} | `pages/{SITE_DIR[p['store']]}/{p['slug']}/` |" for p in pages]
        L += [""]
    L += ["Everything is in the attached **dealeron-handoff-2026-11-23.zip**. Each page folder has `index.html` (paste into the body), `PLACEMENT.md` (exact path, title, meta and placement) and `full-html/index.html` (full-page fallback or placement preview). `metadata-all.csv` lists every title, meta and canonical.", "",
          "Please keep each page's FAQ section and its JSON-LD block together. Please confirm once the pages are live, and pause for our approval if any path already exists.", "",
          "Thanks,", "Spencer Heywood", "Motor Inn Auto Group", F.PHONE, ""]
    return "\n".join(L)


EMAIL_301 = """# DRAFT, NOT SENT. SEND ONLY AFTER 01 IS LIVE

Status: decided by Spencer on 2026-11-23. Send only after the /contactus.aspx content block (email 01) is live. One issue per email.

**To:** support@dealeron.com
**Subject:** 301 redirects: three dealership pages to /contactus.aspx (motorinnautogroup.com)

---

Hi DealerOn team,

On www.motorinnautogroup.com, please add permanent (301) redirects from these three pages to **https://www.motorinnautogroup.com/contactus.aspx**:

| From | To |
|---|---|
| /car-dealerships-carroll-iowa | /contactus.aspx |
| /car-dealerships-in-carroll-iowa.html | /contactus.aspx |
| /car-dealership-carroll-iowa | /contactus.aspx |

Please also update any site navigation or internal links that point at those three URLs so they point at /contactus.aspx directly, and remove the three URLs from the sitemap. No other changes.

Please confirm when the redirects are live.

Thanks,
Spencer Heywood
Motor Inn Auto Group
(712) 792-5000
"""


def readme(rows):
    L = ["# Motor Inn: DealerOn handoff (2026-11-23)", "",
         f"**Status: `{STATUS}`.** Nothing in this package has been sent or published.", "",
         "## What this is",
         "Draft handoff for 9 pages from the 2026-11-23 page plan (`docs/page-plans/page-plan-2026-11-23.md`):",
         "- 2 updates to existing pages on motorinnautogroup.com (cycle 1: body only)",
         "- 4 new pages on motorinnofcarroll.com",
         "- 3 new pages on motorinntoyotaofcarroll.com", "",
         "| Site | Page | Action |", "|---|---|---|"]
    L += [f"| {r['site']} | {r['url_path']} | {r['action']} |" for r in rows]
    L += ["", "## Layout", "```text",
          "pages/<site>/<slug>/index.html             body-only HTML: paste into the DealerOn content editor",
          "pages/<site>/<slug>/PLACEMENT.md           exact path, title/meta/H1 rules, placement, redirects, links",
          "pages/<site>/<slug>/full-html/index.html   full-page fallback (new pages) or placement preview (updates)",
          "metadata-all.csv                           titles, metas, canonicals, H1s (+ cycle-2 values for updates)",
          "EMAIL-DRAFTS/                              one email per issue (00-04), none sent",
          "_chrome/                                   live pages captured " + CAPTURED + ", used as the full-html template",
          "_qa/                                       checks + screenshots (390px and 1280px)",
          "```", "",
          "## Email order (one issue per email)",
          "0. `00-withdraw-old-contact-page.md`: withdraw the retired contact page from the 2026-11-06 handoff. **Send first.**",
          "1. `01-group-site-content-updates.md`: /contactus.aspx block + /used-cars-carroll-iowa body.",
          "2. `02-chevy-site-new-pages.md`: 4 new Chevy pages.",
          "3. `03-toyota-site-new-pages.md`: 3 new Toyota pages.",
          "4. `04-group-301s-after-01-live.md`: 301 three dealership URLs to /contactus.aspx, **only after 01 is live**.", "",
          "## Before any of this is sent",
          "- [ ] Spencer approves the copy (all 9 pages).",
          "- [ ] Spot-check vehicle descriptions against toyota.com / chevrolet.com (Codex R1-009).",
          "- [ ] Send 00 (withdrawal) before 01.",
          "- [ ] After publish: click-test the model-filter links again, add the cross-links listed in each PLACEMENT.md, re-pull GSC (Chevy property needs the service-account access fix first).", "",
          "## Source and QA",
          "- Copy, schema and FAQ come from `content/page-packages/2026-11-23/` (generator `_src/build.py`, gate `_src/validate.py`). They passed the Codex adversarial gate (`brain/reports/2026-11-23-pages-codex-adversarial-rerun2-2026-11-23.md`) and the confirm pass.",
          "- Handoff checks: `_qa/qa-results.md`.",
          "- Rebuild: `python3 content/page-packages/2026-11-23/_src/handoff.py`.", "",
          "## Contact", f"Spencer Heywood, Motor Inn Auto Group, {F.PHONE}", ""]
    return "\n".join(L)


def main():
    pages_root = os.path.join(OUT, "pages")
    for p in PAGES:
        d = os.path.join(pages_root, SITE_DIR[p["store"]], p["slug"])
        os.makedirs(os.path.join(d, "full-html"), exist_ok=True)
        frag = body_html(p)
        open(os.path.join(d, "index.html"), "w").write(frag + "\n")
        open(os.path.join(d, "full-html", "index.html"), "w").write(full_html(p, frag))
        open(os.path.join(d, "PLACEMENT.md"), "w").write(placement(p))
    rows = csv_rows()
    with open(os.path.join(OUT, "metadata-all.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    ed = os.path.join(OUT, "EMAIL-DRAFTS")
    os.makedirs(ed, exist_ok=True)
    withdraw = open(os.path.join(ROOT, "content", "drafts", "dealeron-withdraw-contactus-2026-11-23.md")).read()
    open(os.path.join(ed, "00-withdraw-old-contact-page.md"), "w").write(withdraw)
    for fname, spec in EMAILS.items():
        open(os.path.join(ed, fname), "w").write(email(fname, spec))
    open(os.path.join(ed, "04-group-301s-after-01-live.md"), "w").write(EMAIL_301)
    open(os.path.join(OUT, "README-DEALERON.md"), "w").write(readme(rows))
    # zip (excludes _chrome captures and _qa screenshots; DealerOn needs pages + docs only)
    zpath = OUT + ".zip"
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for base, _, files in os.walk(OUT):
            rel = os.path.relpath(base, OUT)
            if rel.split(os.sep)[0] in ("_chrome", "_qa"):
                continue
            for f in sorted(files):
                full = os.path.join(base, f)
                z.write(full, os.path.relpath(full, OUT))
    print(f"handoff built: {OUT} (+ {os.path.basename(zpath)})")


if __name__ == "__main__":
    main()
