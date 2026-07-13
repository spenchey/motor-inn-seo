#!/usr/bin/env python3
"""
seo-toolkit-findings.py  (MOT-2431)

Deterministic findings synthesis for the SEO/GEO toolkit. Reads the analyzer
JSON written by run-seo-toolkit.sh and emits a prioritized markdown section.

NO LLM. Every finding is templated from analyzer output with fixed rules, and
cites the JSON file + field it came from. The optional rory-seo inspector pass
(scripts/rory-seo-inspect.sh) consumes the same JSON but never replaces this.

Usage: seo-toolkit-findings.py <toolkit-day-dir> --scope weekly|monthly --url URL
"""

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

# Checklist references shipped in tools/skills-sh/ (skills.sh assets).
CHECKLISTS = {
    "seo": "tools/skills-sh/marketingskills-seo-audit/SKILL.md",
    "geo": "tools/skills-sh/opc-seo-geo/SKILL.md",
}

# Schema types a dealership homepage is expected to expose (claude-seo
# schema/templates.json has ready JSON-LD templates for these).
EXPECTED_SCHEMA_HINTS = ("AutoDealer", "LocalBusiness", "AutomotiveBusiness")

MAX_PER_BUCKET = 8


def load(day_dir: Path, name: str):
    p = day_dir / f"{name}.json"
    if not p.is_file():
        return None
    try:
        with open(p) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("day_dir")
    ap.add_argument("--scope", default="weekly", choices=["weekly", "monthly"])
    ap.add_argument("--url", required=True)
    args = ap.parse_args()

    day = Path(args.day_dir)
    target_host = urlparse(args.url).netloc.lower()
    is_staging = target_host.endswith(".vercel.app")

    summary = load(day, "summary") or {}
    technical = load(day, "technical")
    crawlers = load(day, "crawlers")
    llmstxt = load(day, "llmstxt")
    onpage = load(day, "onpage")
    drift = load(day, "drift")
    citability = load(day, "citability")
    quality = load(day, "content-quality")
    sitemap = load(day, "sitemap")
    brand = load(day, "brand")

    p1, p2, p3 = [], [], []
    scores = []  # (analyzer, metric, value)

    # --- analyzer failures are always P1-visible -----------------------------
    for name in summary.get("failed", []):
        p1.append(f"[summary.json#failed] Analyzer `{name}` crashed this run — "
                  f"output missing; see run.log. No silent pass allowed.")

    # --- crawlers / robots ----------------------------------------------------
    if crawlers:
        if not crawlers.get("exists"):
            p1.append("[crawlers.json#exists] robots.txt missing — AI crawlers and "
                      "search bots have no directives at all.")
        blocked = sorted(k for k, v in (crawlers.get("ai_crawler_status") or {}).items()
                         if "DISALLOWED" in str(v).upper() or "BLOCKED" in str(v).upper())
        if blocked:
            p1.append(f"[crawlers.json#ai_crawler_status] AI crawlers blocked in "
                      f"robots.txt: {', '.join(blocked)} — kills GEO citability.")
        else:
            p3.append("[crawlers.json#ai_crawler_status] All tracked AI crawlers "
                      "allowed (GPTBot, ClaudeBot, PerplexityBot, CCBot, ...).")
        for sm in crawlers.get("sitemaps") or []:
            sm_host = urlparse(sm).netloc.lower()
            if sm_host and sm_host != target_host:
                p2.append(f"[crawlers.json#sitemaps] robots.txt Sitemap points at "
                          f"`{sm_host}` while the audited site is `{target_host}` — "
                          f"crawlers on this host are handed another domain's sitemap. "
                          f"Verify this is intended pre-cutover, and that it flips at cutover.")

    # --- llms.txt ---------------------------------------------------------------
    if llmstxt:
        exists = bool(llmstxt.get("exists") or (llmstxt.get("llms_txt") or {}).get("exists"))
        if not exists:
            p2.append(f"[llmstxt.json#exists] No llms.txt at {args.url.rstrip('/')}/llms.txt — "
                      f"generate one (geo-seo-claude llmstxt_generator.py has a generate mode); "
                      f"checklist: {CHECKLISTS['geo']}.")
        else:
            issues = llmstxt.get("issues") or llmstxt.get("errors") or []
            if issues:
                p2.append(f"[llmstxt.json#issues] llms.txt exists but has "
                          f"{len(issues)} validation issue(s): "
                          f"{'; '.join(str(i) for i in issues[:3])}")
            else:
                p3.append("[llmstxt.json#exists] llms.txt present and valid.")

    # --- technical (page fetch) --------------------------------------------------
    if technical:
        status = technical.get("status_code")
        if status and status != 200:
            p1.append(f"[technical.json#status_code] Homepage returned HTTP {status}.")
        if not technical.get("title"):
            p2.append("[technical.json#title] Homepage has no <title>.")
        if not technical.get("description"):
            p2.append("[technical.json#description] Homepage has no meta description.")
        canonical = technical.get("canonical")
        if not canonical:
            p2.append("[technical.json#canonical] Homepage has no canonical URL.")
        else:
            can_host = urlparse(str(canonical)).netloc.lower()
            if can_host and can_host != target_host:
                sev = p3 if is_staging else p1
                sev.append(f"[technical.json#canonical] Canonical points at `{can_host}` "
                           f"(audited host `{target_host}`)"
                           + (" — expected on staging pre-cutover; MUST flip at cutover."
                              if is_staging else " — cross-host canonical leaks equity."))
        meta_tags = {str(k).lower(): v for k, v in (technical.get("meta_tags") or {}).items()}
        headers_ci = {str(k).lower(): v for k, v in (technical.get("headers") or {}).items()}
        robots_meta = str(meta_tags.get("robots", "")).lower()
        x_robots = str(headers_ci.get("x-robots-tag", "")).lower()
        if "noindex" in robots_meta or "noindex" in x_robots:
            if is_staging:
                p3.append("[technical.json#meta_tags.robots] noindex present — expected "
                          "on the staging host; MUST be removed at cutover.")
            else:
                p1.append("[technical.json#meta_tags.robots] noindex on production homepage.")
        chain = technical.get("redirect_chain") or []
        if len(chain) > 1:
            p3.append(f"[technical.json#redirect_chain] {len(chain)} redirects before final URL.")

    # --- onpage (parse_html: h1=list[str], images=list[{src,alt}], schema=list[jsonld]) ---
    if onpage:
        h1s = onpage.get("h1") or []
        if isinstance(h1s, list):
            if len(h1s) == 0:
                p2.append("[onpage.json#h1] Homepage has no H1.")
            elif len(h1s) > 1:
                p3.append(f"[onpage.json#h1] {len(h1s)} H1 tags on homepage (want exactly 1).")
        imgs = onpage.get("images") or []
        if isinstance(imgs, list) and imgs:
            missing_alt = sum(1 for i in imgs if isinstance(i, dict) and not str(i.get("alt") or "").strip())
            if missing_alt > 0:
                p3.append(f"[onpage.json#images] {missing_alt}/{len(imgs)} image(s) missing alt text.")
        wc = onpage.get("word_count")
        if isinstance(wc, int):
            scores.append(("onpage", "homepage word count", wc))
            if wc < 300:
                p2.append(f"[onpage.json#word_count] Homepage has only {wc} words of "
                          f"indexable copy — thin for local intent queries.")
        schema_blocks = onpage.get("schema") or []
        types_found = []
        if isinstance(schema_blocks, list):
            for block in schema_blocks:
                if isinstance(block, dict):
                    t = block.get("@type") or block.get("type")
                    if isinstance(t, list):
                        types_found.extend(str(x) for x in t)
                    elif t:
                        types_found.append(str(t))
        scores.append(("onpage", "JSON-LD blocks on homepage", len(schema_blocks) if isinstance(schema_blocks, list) else 0))
        if args.scope == "monthly":
            if not schema_blocks:
                p2.append("[onpage.json#schema] No JSON-LD structured data on homepage — "
                          "start from tools/claude-seo/schema/templates.json (AutoDealer, "
                          "Vehicle, FAQPage).")
            elif not any(any(h in t for h in EXPECTED_SCHEMA_HINTS) for t in types_found):
                p2.append(f"[onpage.json#schema] JSON-LD present ({', '.join(sorted(set(types_found))[:6]) or 'untyped'}) "
                          f"but no dealer entity type ({'/'.join(EXPECTED_SCHEMA_HINTS)}).")

    # --- drift ---------------------------------------------------------------------
    if drift:
        if drift.get("error"):
            p3.append(f"[drift.json#error] Drift: {str(drift.get('error'))[:120]} "
                      f"(first run stores a baseline; comparisons start next run).")
        else:
            dsum = drift.get("summary") or {}
            crit, warn = int(dsum.get("critical", 0) or 0), int(dsum.get("warning", 0) or 0)
            scores.append(("drift", "critical changes vs baseline", crit))
            scores.append(("drift", "warning changes vs baseline", warn))
            triggered = [f for f in (drift.get("triggered_findings") or []) if isinstance(f, dict)]
            names = [str(f.get("rule") or f.get("name") or f.get("message") or "?")[:60]
                     for f in triggered][:6]
            if crit:
                p1.append(f"[drift.json#summary.critical] {crit} CRITICAL SEO element "
                          f"change(s) since last baseline: {', '.join(names) or 'see drift.json'}.")
            if warn:
                p2.append(f"[drift.json#summary.warning] {warn} warning-level drift "
                          f"change(s): {', '.join(names) or 'see drift.json'}.")
            if not crit and not warn:
                p3.append("[drift.json#summary] No SEO element drift vs last baseline.")

    # --- monthly-only analyzers -------------------------------------------------------
    if citability:
        overall = citability.get("average_citability_score")
        blocks = citability.get("all_blocks") or []
        n_blocks = citability.get("total_blocks_analyzed")
        if isinstance(n_blocks, int):
            scores.append(("citability", "content blocks analyzed", n_blocks))
        if isinstance(overall, (int, float)):
            scores.append(("citability", "average citability score (0-100)", round(overall, 1)))
            if overall < 50:
                p2.append(f"[citability.json#average_citability_score] Citability "
                          f"{round(overall,1)}/100 — AI engines are unlikely to quote this "
                          f"page; restructure toward self-contained 130-170 word answer "
                          f"passages ({CHECKLISTS['geo']}).")
        if isinstance(blocks, list) and blocks:
            worst = sorted((b for b in blocks if isinstance(b, dict) and isinstance(b.get("total_score"), (int, float))),
                           key=lambda b: b["total_score"])[:3]
            for b in worst:
                snippet = str(b.get("preview") or b.get("heading") or "")[:70].strip()
                p3.append(f"[citability.json#all_blocks] Low-citability block "
                          f"(score {b['total_score']}): \"{snippet}...\"")

    if quality:
        oq = quality.get("overall_quality")
        if isinstance(oq, (int, float)):
            scores.append(("content-quality", "overall quality (0-100)", oq))
            if oq < 60:
                p2.append(f"[content-quality.json#overall_quality] Homepage copy scores "
                          f"{oq}/100 on QRG heuristics (filler {quality.get('filler_score')}, "
                          f"AI-pattern {quality.get('ai_pattern_score')}) — rewrite toward "
                          f"specific, original dealer copy.")

    if sitemap is not None:
        count = sitemap.get("count", 0) if isinstance(sitemap, dict) else 0
        scores.append(("sitemap", "URLs discovered via sitemap", count))
        if count == 0:
            p2.append(f"[sitemap.json#count] No URLs discoverable from {target_host}'s "
                      f"sitemap — crawlers must link-crawl blind.")

    if brand:
        platforms = brand.get("platforms") or {}
        absent, errored = [], []
        for k, v in sorted(platforms.items()):
            if not isinstance(v, dict):
                continue
            if v.get("error"):
                errored.append(k)
                continue
            # brand_scanner emits presence booleans named has_* / mentioned_* /
            # cited_* per platform (e.g. has_channel, has_wikipedia_page).
            signals = [vv for kk, vv in v.items()
                       if str(kk).startswith(("has_", "mentioned_", "cited_"))]
            if signals and not any(s in (True, "True", "true") for s in signals):
                absent.append(k)
        if absent:
            p3.append(f"[brand.json#platforms] No confirmed brand-presence signal on: "
                      f"{', '.join(absent[:6])} — these correlate strongest with AI "
                      f"citations (YouTube 0.737); manual check URLs are in brand.json.")
        if errored:
            p3.append(f"[brand.json#platforms] Brand scan hit walls on: "
                      f"{', '.join(errored[:6])} (scrape blocked — not a finding, "
                      f"re-check next run).")

    # --- render ------------------------------------------------------------------------
    date = summary.get("date", "")
    lines = []
    lines.append(f"## GEO/SEO Toolkit Findings — {args.url} — {date} ({args.scope})")
    lines.append("")
    lines.append("_Deterministic analyzer battery (MOT-2431): vendored claude-seo + "
                 "geo-seo-claude (tools/PROVENANCE.md). Synthesis is templated from "
                 f"analyzer scores — no LLM in this path. Checklists: {CHECKLISTS['seo']}, "
                 f"{CHECKLISTS['geo']}._")
    lines.append("")
    for title, bucket in (("P1 — fix now", p1), ("P2 — this month", p2), ("P3 / info", p3)):
        lines.append(f"### {title}")
        lines.append("")
        if bucket:
            for item in bucket[:MAX_PER_BUCKET]:
                lines.append(f"- {item}")
            if len(bucket) > MAX_PER_BUCKET:
                lines.append(f"- ...plus {len(bucket) - MAX_PER_BUCKET} more (see analyzer JSON).")
        else:
            lines.append("- none")
        lines.append("")
    if scores:
        lines.append("### Analyzer scores")
        lines.append("")
        lines.append("| Analyzer | Metric | Value |")
        lines.append("|---|---|---:|")
        for a, m, v in scores:
            lines.append(f"| {a} | {m} | {v} |")
        lines.append("")
    lines.append(f"Machine output: `audits/toolkit/{date}/` (JSON per analyzer + summary.json).")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
