#!/usr/bin/env python3
"""Generate the 2026-11-23 DealerOn page packages from the page specs.

Usage (from repo root):  python3 content/page-packages/2026-11-23/_src/build.py
Writes content/page-packages/2026-11-23/<slug>/{brief,content,faq,meta}.md + schema.json
and content/page-packages/2026-11-23/ai/<slug>.md. Drafts only; nothing is published.
"""
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import facts as F  # noqa: E402
from pages_group import PAGES as G  # noqa: E402
from pages_chevy import PAGES as C  # noqa: E402
from pages_toyota import PAGES as T  # noqa: E402
from phrasing_map import SRC  # noqa: E402

PAGES = G + C + T
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
OUT = os.path.abspath(os.path.join(HERE, ".."))
GSC = os.path.join(ROOT, "ads", "gsc-keywords-12mo.json")
KW = os.path.join(ROOT, "ads", "gsc-ads-package-2026-11-22", "keywords.csv")


def load_evidence():
    rows = {r["query"]: r for r in json.load(open(GSC))}
    kw = {}
    with open(KW) as fh:
        for r in csv.DictReader(fh):
            kw[r["exact_keyword"].strip("[]")] = r
    return rows, kw


def canonical(p):
    return "https://" + F.STORES[p["store"]]["host"] + p["path"]


def address_schema():
    return {
        "@type": "PostalAddress",
        "streetAddress": F.ADDRESS["street"],
        "addressLocality": F.ADDRESS["city"],
        "addressRegion": F.ADDRESS["region"],
        "postalCode": F.ADDRESS["zip"],
        "addressCountry": "US",
    }


def dealer_node(key, node_id=None):
    s = F.STORES[key]
    n = {
        "@type": "AutoDealer",
        "@id": node_id or (s["url"] + "#dealer"),
        "name": s["name"],
        "url": s["url"],
        "telephone": F.PHONE_E164,
        "address": address_schema(),
        "openingHoursSpecification": F.HOURS_SCHEMA,
        "brand": [{"@type": "Brand", "name": b} for b in s["brands"]],
        "areaServed": {"@type": "City", "name": "Carroll, Iowa"},
    }
    if s.get("alt"):
        n["alternateName"] = s["alt"]
    return n


def build_schema(p):
    url = canonical(p)
    graph = []
    page = {
        "@type": "WebPage",
        "@id": url + "#webpage",
        "url": url,
        "name": p["title"],
        "description": p["meta"],
        "inLanguage": "en-US",
    }
    if p["store"] == "group":
        dealer = dealer_node("group")
        dealer["brand"] = [{"@type": "Brand", "name": "Toyota"}, {"@type": "Brand", "name": "Chevrolet"}]
        dealer["department"] = [
            {"@id": F.STORES["toyota"]["url"] + "#dealer"},
            {"@id": F.STORES["chevy"]["url"] + "#dealer"},
        ]
        graph.append(dealer)
        graph.append(dealer_node("toyota"))
        graph.append(dealer_node("chevy"))
    else:
        dealer = dealer_node(p["store"])
        dealer["parentOrganization"] = {"@type": "Organization", "name": F.STORES["group"]["name"], "url": F.STORES["group"]["url"]}
        graph.append(dealer)
    page["about"] = p.get("about") or {"@id": dealer["@id"]}
    page["publisher"] = {"@id": dealer["@id"]}
    graph.insert(0, page)
    graph.append({
        "@type": "FAQPage",
        "@id": url + "#faq",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in p["faq"]
        ],
    })
    return {"@context": "https://schema.org", "@graph": graph}


def visit_block(p):
    s = F.STORES[p["store"]]
    name = s["name"]
    lines = [
        "## Where do I find us?",
        "",
        f"{name} is at {F.ADDRESS_LINE}, {F.LANDMARK} in Carroll. Call {F.PHONE}.",
        "",
        f"- **Address:** {F.ADDRESS_LINE}",
        f"- **Phone:** {F.PHONE}",
        f"- **Sales hours:** {F.HOURS_TEXT}. Service hours are on the [hours page]({s['url']}hours.aspx).",
        "",
    ]
    return "\n".join(lines)


def build_content(p):
    out = []
    if p.get("placement"):
        out += [f"> **Placement (in-place update, not a new page):** {p['placement']}", ""]
    out += [f"# {p['h1']}", "", p["intro"].strip(), "", f"**{p['cta']}**", ""]
    for h2, body in p["sections"]:
        out += [f"## {h2}", "", body.strip(), ""]
    out += ["## What else do Carroll shoppers ask?", ""]
    for q, a in p["faq"]:
        out += [f"### {q}", "", a, ""]
    out.append(visit_block(p))
    out += [f"**{p['cta']}**", ""]
    return "\n".join(out)


def build_faq(p):
    out = [f"# FAQ: {p['h1']}", "", "Each answer stands alone (2-4 sentences) so an answer engine can quote it whole. Mirrors the FAQPage block in schema.json and the FAQ section of content.md.", ""]
    for q, a in p["faq"]:
        out += [f"## {q}", "", a, ""]
    return "\n".join(out)


def build_meta(p):
    url = canonical(p)
    return "\n".join([
        f"# Meta: {p['slug']}",
        "",
        f"- **Canonical URL:** {url}",
        f"- **Title ({len(p['title'])} chars):** {p['title']}",
        f"- **Meta description ({len(p['meta'])} chars):** {p['meta']}",
        f"- **og:title:** {p['og_title']}",
        f"- **og:description:** {p['og_desc']}",
        f"- **og:url:** {url}",
        "- **og:type:** website",
        "",
    ])


def build_brief(p, rows, kw):
    url = canonical(p)
    s = F.STORES[p["store"]]
    out = [
        f"# Brief: {p['slug']}",
        "",
        f"- **Site:** {s['host']} ({s['name']})",
        f"- **URL:** {url}",
        f"- **Status:** {p['status']}",
        f"- **Intent tier:** {p['tier']}",
        f"- **H1:** {p['h1']}",
        f"- **Primary query:** {p['queries'][0]}",
        f"- **AI mirror target (handoff only, not in the mirror file):** {s['ai_host']}",
        "",
        "## Routing decision",
        "",
        p["routing"].strip(),
        "",
        "## Source evidence (GSC, 12 months ending 2026-11-22)",
        "",
        "Source: `ads/gsc-keywords-12mo.json`. Every row in it is labeled `sc-domain:motorinnautogroup.com`. The Chevrolet property is BLOCKED for the service account (`siteUnverifiedUser` in `pipeline/cache/gsc-ebe12c…json`, 2026-10-19). The Toyota property has its own data, which these rows don't include. "
        "A ✓ in the Ads-40 column means the query is also one of the 40 exact-match terms in `ads/gsc-ads-package-2026-11-22/keywords.csv`, and that file's landing page is shown.",
        "",
        "| Query | Impressions | Clicks | Avg pos | Ads-40 | Current landing page (Ads-40 file) |",
        "|---|---:|---:|---:|:-:|---|",
    ]
    tot = 0
    for q in p["queries"]:
        r = rows.get(q)
        if not r:
            raise SystemExit(f"[{p['slug']}] query not in GSC export: {q!r}")
        tot += r["impressions"]
        k = kw.get(q)
        out.append(f"| {q} | {r['impressions']} | {r['clicks']} | {r['pos']:.1f} | {'✓' if k else ''} | {k['landing_page'] if k else ''} |")
    out += ["", f"Cluster total: **{tot:,} impressions** across {len(p['queries'])} queries.", ""]
    if p.get("ship_plan"):
        out += ["## Ship plan (house rule: one change per page per cycle, brain/BRIEF.md)", ""] + [f"{i}. {x}" for i, x in enumerate(p["ship_plan"], 1)] + [""]
    out += ["## Question phrasing sources", "",
            "Each H2 and FAQ question follows a real GSC query. Rows marked DERIVED are conversion or support questions with no direct GSC row (10+ impressions), answered from owner-verified facts.", "",
            "| Question | Where | GSC query it follows | Impressions |", "|---|---|---|---:|"]
    seen = set()
    for where, qs in (("H2", [h for h, _ in p["sections"]]), ("FAQ", [q for q, _ in p["faq"]])):
        for q in qs:
            if q not in SRC:
                raise SystemExit(f"[{p['slug']}] no phrasing source for: {q!r}")
            src = SRC[q]
            if src is None:
                out.append(f"| {q} | {where} | DERIVED | |")
            else:
                r = rows.get(src)
                if not r:
                    raise SystemExit(f"[{p['slug']}] phrasing source not in GSC: {src!r}")
                out.append(f"| {q} | {where} | {src} | {r['impressions']} |")
    out += [""]
    out += ["## Internal links (all verified in the 2026-11-05 sitemap snapshots in `brain/research/`)", "", "| Anchor | URL | Note |", "|---|---|---|"]
    for anchor, href, note in p["links"]:
        out.append(f"| {anchor} | {href} | {note} |")
    out += [""]
    if p.get("post_links"):
        out += ["## Cross-links to add after publish (target pages do not exist yet)", ""]
        out += [f"- {x}" for x in p["post_links"]] + [""]
    out += ["## Fact sources used in copy", ""] + [f"- {x}" for x in p["sources"]] + [""]
    if p.get("notes"):
        out += ["## Review notes for Spencer", ""] + [f"- {x}" for x in p["notes"]] + [""]
    return "\n".join(out), tot


def build_ai(p):
    s = F.STORES[p["store"]]
    url = canonical(p)
    out = [
        f"# {p['h1']}",
        "",
        f"> {p['ai_summary'].strip()}",
        "",
        f"- Canonical page: {url}",
        "",
        "## Questions and answers",
        "",
    ]
    for q, a in p["faq"]:
        out += [f"### {q}", "", a, ""]
    out += [
        "## Entity facts",
        "",
        f"- Name: {s['name']}" + (f" (also known as {s['alt']})" if s.get("alt") else ""),
        f"- Part of: {F.STORES['group']['name']}" if p["store"] != "group" else "- Stores: Motor Inn Toyota of Carroll; Motor Inn Chevrolet of Carroll (same address)",
        f"- Address: {F.ADDRESS_LINE}",
        f"- Phone: {F.PHONE}",
        f"- Brands: {', '.join(s['brands'])}",
        f"- Sales hours: {F.HOURS_TEXT}",
        f"- Website: {s['url']}",
        f"- Service: {s['service_url']}",
        "",
        "## Related pages",
        "",
    ]
    out += [f"- [{a}]({h})" for a, h, _ in p["links"]]
    out.append("")
    return "\n".join(out)


def main():
    rows, kw = load_evidence()
    os.makedirs(os.path.join(OUT, "ai"), exist_ok=True)
    totals = {}
    for p in PAGES:
        d = os.path.join(OUT, p["slug"])
        os.makedirs(d, exist_ok=True)
        brief, tot = build_brief(p, rows, kw)
        totals[p["slug"]] = tot
        files = {
            "brief.md": brief,
            "content.md": build_content(p),
            "faq.md": build_faq(p),
            "meta.md": build_meta(p),
            "schema.json": json.dumps(build_schema(p), indent=2, ensure_ascii=False) + "\n",
        }
        for name, body in files.items():
            with open(os.path.join(d, name), "w") as fh:
                fh.write(body)
        with open(os.path.join(OUT, "ai", p["slug"] + ".md"), "w") as fh:
            fh.write(build_ai(p))
    json.dump(
        [{"slug": p["slug"], "site": F.STORES[p["store"]]["host"], "ai_mirror_target": F.STORES[p["store"]]["ai_host"], "ai_status": "draft, not deployed", "url": canonical(p), "status": p["status"].split(".")[0], "impressions_12mo": totals[p["slug"]]} for p in PAGES],
        open(os.path.join(OUT, "_manifest.json"), "w"), indent=2)
    print(f"built {len(PAGES)} packages -> {OUT}")


if __name__ == "__main__":
    main()
