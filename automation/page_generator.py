#!/usr/bin/env python3
"""Render evidence-bound, offline page drafts; never infer dealership facts."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone, timedelta
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import parse_qsl, urlsplit

try:
    from .common import atomic_json, read_json, utcnow, validate_slug, lock, draft_digest
except ImportError:
    from common import atomic_json, read_json, utcnow, validate_slug, lock, draft_digest

SOURCE_TYPES = {"DealerVault", "GSC", "DataForSEO"}
LINK_SOURCE_TYPE = "SiteCrawl"
MAX_AGE = timedelta(days=7)


def _fresh(value: object) -> bool:
    try:
        stamp = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        age = datetime.now(timezone.utc) - stamp
        return timedelta(minutes=-5) <= age <= MAX_AGE
    except (ValueError, TypeError):
        return False


def _unexpired(value: object) -> bool:
    try:
        stamp = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return stamp > datetime.now(timezone.utc)
    except (ValueError, TypeError):
        return False


def _url(value: object) -> bool:
    try:
        parsed = urlsplit(str(value))
        return (parsed.scheme == "https" and bool(parsed.hostname)
                and not parsed.username and not parsed.password
                and not parsed.fragment and not any(c.isspace() for c in str(value)))
    except ValueError:
        return False


def _verified_parent_inventory(row: dict) -> bool:
    """A filtered inventory destination can canonicalize to its checked parent.

    This validates crawl proof, never a link/job-level assertion. The filtered
    destination is useful navigation; it is not a separately indexable page.
    """
    if (row.get("source_type") != LINK_SOURCE_TYPE or row.get("scope") != "links"
            or row.get("canonical_scope") != "parent-inventory"
            or row.get("canonical_verified") is not True or row.get("canonical_http_status") != 200
            or row.get("filter_verified") is not True
            or row.get("final_url") != row.get("url")
            or not all(_url(row.get(key)) for key in ("url", "canonical", "requested_url"))):
        return False
    destination, canonical, requested = [urlsplit(row[key]) for key in ("url", "canonical", "requested_url")]
    if (not destination.query or canonical.query
            or (destination.scheme, destination.netloc, destination.path) != (canonical.scheme, canonical.netloc, canonical.path)
            or (requested.scheme, requested.netloc, requested.path) != (destination.scheme, destination.netloc, destination.path)
            or sorted(parse_qsl(requested.query, keep_blank_values=True)) != sorted(parse_qsl(destination.query, keep_blank_values=True))):
        return False
    filters = {key.lower(): value.lower() for key, value in parse_qsl(destination.query)}
    heading = row.get("visible_heading")
    if not isinstance(heading, str):
        return False
    for field in ("make", "model"):
        intended = row.get("intended_" + field)
        if (not isinstance(intended, str) or not intended.strip()
                or filters.get(field) != intended.lower()
                or not re.search(r"(?<!\w)" + re.escape(intended) + r"(?!\w)", heading, re.I)):
            return False
    return True


def _json_script(value: object) -> str:
    # HTML parsers end script elements on </script>, even inside JSON strings.
    return (json.dumps(value, ensure_ascii=False).replace("&", "\\u0026")
            .replace("<", "\\u003c").replace(">", "\\u003e")
            .replace("\u2028", "\\u2028").replace("\u2029", "\\u2029"))


def _validate(job: dict) -> tuple[list[str], dict, list[tuple[str, list[str]]]]:
    errors: list[str] = []
    evidence: dict = {}
    cited: list[tuple[str, list[str]]] = []
    if job.get("blockers"):
        errors.append("Job retains unresolved blockers: " + str(job["blockers"]))
    gsc = job.get("gsc_check")
    if not isinstance(gsc, dict) or gsc.get("status") != "checked":
        errors.append("GSC cannibalization check must be checked before generating a production draft")
    if job.get("topology_status") != "verified":
        errors.append("Link topology requires verified crawl review")
    for key in ("title", "target_query", "cluster", "owner_host", "target_url", "meta_description"):
        if not isinstance(job.get(key), str) or not job[key].strip():
            errors.append(f"Missing nonempty {key}")
    if errors:
        return errors, evidence, cited
    if not 30 <= len(job["title"]) <= 60:
        errors.append("Title must contain 30-60 characters")
    if not 120 <= len(job["meta_description"]) <= 158:
        errors.append("Meta description must contain 120-158 characters")
    if not _url(job["target_url"]) or urlsplit(job["target_url"]).hostname != job["owner_host"]:
        errors.append("Target URL must use HTTPS and belong to owner_host")
    if not isinstance(job.get("destination"), str) or job["destination"] not in {"dealeron", "ai-proxy"}:
        errors.append("Unknown publication destination")
    outline = job.get("outline")
    if not isinstance(outline, list) or not outline or any(not isinstance(x, str) or not x.strip() for x in outline):
        errors.append("Outline must contain nonempty headings")
    rows = job.get("source_evidence")
    if not isinstance(rows, list) or not rows:
        errors.append("Missing source evidence")
        rows = []
    for row in rows:
        if not isinstance(row, dict):
            errors.append("Invalid evidence row")
            continue
        eid = row.get("id")
        if not isinstance(eid, str) or not re.fullmatch(r"[A-Za-z0-9_.:-]{1,120}", eid) or eid in evidence:
            errors.append("Missing, unsafe, or duplicate evidence ID")
            continue
        if (not isinstance(row.get("source_type"), str) or row["source_type"] not in SOURCE_TYPES | {LINK_SOURCE_TYPE} or not _url(row.get("url"))
                or not _fresh(row.get("retrieved_at")) or row.get("verified") is not True
                or ("valid_until" in row and not _unexpired(row["valid_until"]))
                or not isinstance(row.get("claims"), list)
                or any(not isinstance(c, str) or not c.strip() for c in row.get("claims", []))):
            errors.append(f"Evidence {eid} is unverified, stale, or malformed")
            continue
        if row["source_type"] == LINK_SOURCE_TYPE and (
                row.get("scope") != "links" or row.get("http_status") != 200
                or (row.get("canonical") != row["url"] and not _verified_parent_inventory(row))
                or not _fresh(row.get("checked_at"))
                or not isinstance(row.get("response_sha256"), str)
                or not re.fullmatch(r"[a-f0-9]{64}", row["response_sha256"])):
            errors.append(f"Evidence {eid} lacks current, canonical HTTP 200 link verification")
            continue
        evidence[eid] = row

    def support(text: object, refs: object = None, label: str = "Claim", *, allow_links: bool = False) -> None:
        if not isinstance(text, str) or not text.strip():
            errors.append(f"{label} is empty")
            return
        if refs is None:
            refs = [eid for eid, row in evidence.items() if text in row["claims"]
                    and (row["source_type"] in SOURCE_TYPES or allow_links)]
        if (not isinstance(refs, list) or not refs
                or any(not isinstance(eid, str) or eid not in evidence for eid in refs)):
            errors.append(f"{label} has missing or invalid evidence references")
        elif not allow_links and any(evidence[eid]["source_type"] not in SOURCE_TYPES for eid in refs):
            errors.append(f"{label} cannot use technical link evidence for dealership facts")
        elif not any(text in evidence[eid]["claims"] for eid in refs):
            errors.append(f"{label} is not a verbatim supported source claim")
        else:
            cited.append((text, refs))

    def editorial(text: object, label: str) -> None:
        # Quantities, comparative marketing and affirmative assertions are facts,
        # even when put in headings or phrased as a question.
        factual = r"\d|\b(best|lowest|cheapest|largest|leading|guaranteed|award|certified|offers?|provides?|has|have|available|free|save|in stock|we are|we're|is open)\b"
        if isinstance(text, str) and re.search(factual, text, re.I):
            support(text, label=label)

    editorial(job["title"], "Title")
    support(job["meta_description"], label="Meta description")
    sections = job.get("sections")
    if not isinstance(sections, list) or not sections:
        errors.append("Missing supported page sections")
        sections = []
    for section in sections:
        if not isinstance(section, dict) or not isinstance(section.get("heading"), str) or not section["heading"].strip():
            errors.append("Invalid section heading")
            continue
        if isinstance(outline, list) and section["heading"] not in outline:
            errors.append("Section heading absent from outline")
        editorial(section["heading"], "Section heading")
        claims = section.get("claims")
        if not isinstance(claims, list) or not claims:
            errors.append("Every section needs supported claims")
            continue
        for claim in claims:
            if not isinstance(claim, dict):
                errors.append("Malformed section claim")
                continue
            support(claim.get("text"), claim.get("evidence_ids", []))
    faq = job.get("faq", [])
    if not isinstance(faq, list):
        errors.append("FAQ must be a list")
        faq = []
    for item in faq:
        if not isinstance(item, dict) or not isinstance(item.get("question"), str) or not item["question"].strip():
            errors.append("Invalid FAQ question")
            continue
        support(item.get("answer"), item.get("evidence_ids", []), "FAQ answer")
        editorial(item["question"], "FAQ question")
    links = job.get("internal_links", [])
    if not isinstance(links, list) or not links:
        errors.append("At least one verified contextual link is required")
        links = []
    for link in links:
        if not isinstance(link, dict):
            errors.append("Malformed internal link")
            continue
        url, anchor = link.get("url"), link.get("anchor")
        refs = link.get("evidence_ids", [])
        parent_proof = any(
            isinstance(eid, str) and eid in evidence and evidence[eid].get("url") == url
            and evidence[eid].get("canonical") == link.get("canonical")
            and _verified_parent_inventory(evidence[eid])
            for eid in (refs if isinstance(refs, list) else []))
        if (not _url(url) or link.get("http_status") != 200 or not _fresh(link.get("checked_at"))
                or (link.get("canonical") != url and not parent_proof)):
            errors.append("Link needs a current 200 final URL and matching canonical or verified filtered-inventory parent")
        if not isinstance(anchor, str) or len(anchor.split()) < 2 or anchor.lower() in {"click here", "read more", "learn more"}:
            errors.append("Link anchor must describe the destination")
        support(url, link.get("evidence_ids", []), "Link URL", allow_links=True)
        support(anchor, link.get("evidence_ids", []), "Link anchor", allow_links=True)
        for eid in link.get("evidence_ids", []) if isinstance(link.get("evidence_ids"), list) else []:
            row = evidence.get(eid) if isinstance(eid, str) else None
            if row and row["source_type"] == LINK_SOURCE_TYPE and row["url"] != url:
                errors.append("Technical link evidence must verify this exact destination")
        if _url(url):
            host = urlsplit(url).hostname
            if host.startswith("ai."):
                errors.append("AI proxies must not be consumer inventory destinations")
            if any(k.lower().startswith(("utm_", "gclid", "fbclid")) for k in urlsplit(url).query.split("&")):
                errors.append("Tracking URLs cannot be contextual links")
            if host != job["owner_host"] and not any(brand in str(anchor).lower() for brand in ("toyota", "chevrolet")):
                errors.append("Cross-site anchors must name Toyota or Chevrolet")
            if re.search(r"/(?:new|used)[-/].*\d{8,}|/vehicle/|vin=", url, re.I) and not link.get("inventory_expiry_rule"):
                errors.append("Vehicle detail links require a sale replacement/removal rule")
    business = job.get("business")
    if business is not None:
        if not isinstance(business, dict):
            errors.append("Business must be a supported entity")
        else:
            support(business.get("name"), business.get("evidence_ids", []), "Business name")
            support(business.get("url"), business.get("evidence_ids", []), "Business URL")
            if not _url(business.get("url")) or urlsplit(str(business.get("url"))).hostname != job["owner_host"]:
                errors.append("Business entity must belong to the page owner")
    scope = " ".join(str(job.get(k, "")) for k in ("cluster", "target_query", "target_url"))
    if re.search(r"\bused\b|searchused", scope, re.I) and job.get("staging_read_status") != "verified":
        errors.append("BLOCKED-STAGING-READ: used-inventory pages need the staged package comparison")
    return errors, evidence, cited


def _render(job: dict) -> str:
    e = escape
    sections = "\n".join("<section><h2>" + e(s["heading"]) + "</h2>" + "".join(
        "<p>" + e(c["text"]) + "</p>" for c in s["claims"]) + "</section>" for s in job["sections"])
    faq = job.get("faq", [])
    if faq:
        sections += '<section aria-label="Frequently asked questions"><h2>Frequently asked questions</h2>' + "".join(
            "<h3>" + e(f["question"]) + "</h3><p>" + e(f["answer"]) + "</p>" for f in faq) + "</section>"
    links = "".join('<li><a href="' + e(link["url"], quote=True) + '">' + e(link["anchor"]) + "</a>" +
                    (" <span>(cross-site)</span>" if urlsplit(link["url"]).hostname != job["owner_host"] else "") + "</li>"
                    for link in job["internal_links"])
    graph: list[dict] = [{"@type": "Article", "@id": job["target_url"] + "#article",
                         "headline": job["title"], "description": job["meta_description"],
                         "mainEntityOfPage": job["target_url"],
                         "articleBody": "\n".join(c["text"] for s in job["sections"] for c in s["claims"])}]
    if faq:
        graph.append({"@type": "FAQPage", "@id": job["target_url"] + "#faq", "mainEntity": [
            {"@type": "Question", "name": f["question"], "acceptedAnswer": {"@type": "Answer", "text": f["answer"]}} for f in faq]})
    if job.get("business"):
        b = job["business"]
        graph.append({"@type": "LocalBusiness", "@id": b["url"].rstrip("/") + "/#organization", "name": b["name"], "url": b["url"]})
        graph[0]["publisher"] = {"@id": graph[-1]["@id"]}
    schema = _json_script({"@context": "https://schema.org", "@graph": graph})
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(job['title'])}</title>
<meta name="description" content="{e(job['meta_description'], quote=True)}">
<link rel="canonical" href="{e(job['target_url'], quote=True)}">
<style>body{{font:1.1rem/1.65 system-ui,sans-serif;margin:0;color:#172735;background:#fff}}main{{max-width:60rem;margin:auto;padding:clamp(1rem,4vw,3rem)}}h1{{line-height:1.15;font-size:clamp(1.9rem,5vw,3rem)}}h2{{line-height:1.25}}a{{color:#084da2;overflow-wrap:anywhere}}p{{max-width:70ch}}li{{margin-block:.65rem}}</style>
<script type="application/ld+json">{schema}</script></head>
<body><main>
<article><h1>{e(job['title'])}</h1>{sections}</article>
<nav aria-label="Related dealership resources"><h2>Related resources</h2><ul>{links}</ul></nav>
</main></body></html>
'''


class _Inspector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.h1 = 0
        self.viewport = False
        self.canonical = []
        self.external_dependencies = []
        self.schemas: list[str] = []
        self.active_schema = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.h1 += tag == "h1"
        if tag == "meta" and attrs.get("name") == "viewport":
            self.viewport = "width=device-width" in attrs.get("content", "")
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical.append(attrs.get("href"))
        if (any(k.startswith("on") for k in attrs) or tag in {"iframe", "object", "embed"}
                or attrs.get("src") or (tag == "link" and attrs.get("rel") != "canonical")
                or (tag == "script" and attrs.get("type") != "application/ld+json")):
            self.external_dependencies.append(tag)
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self.active_schema = True
            self.schemas.append("")

    def handle_data(self, data):
        if self.active_schema:
            self.schemas[-1] += data

    def handle_endtag(self, tag):
        if tag == "script":
            self.active_schema = False


def _qa(html: str, job: dict, errors: list[str]) -> dict:
    parser = _Inspector()
    parser.feed(html)
    schema_ok = False
    try:
        schemas = [json.loads(s) for s in parser.schemas]
        schema_ok = len(schemas) == 1 and schemas[0]["@graph"][0]["@type"] == "Article"
    except (ValueError, KeyError, TypeError, IndexError):
        pass
    checks = {"evidence_verified": not errors, "json_ld_parses": schema_ok,
              "title_length": isinstance(job.get("title"), str) and 30 <= len(job["title"]) <= 60,
              "meta_description_length": isinstance(job.get("meta_description"), str) and 120 <= len(job["meta_description"]) <= 158,
              "mobile_viewport": parser.viewport, "single_h1": parser.h1 == 1,
              "canonical_matches_owner": parser.canonical == [job.get("target_url")],
              "no_external_dependencies": not parser.external_dependencies,
              "final_candidate_indexable": 'name="robots"' not in html,
              "no_fabricated_claims": not errors}
    return {"passed": all(checks.values()), "checks": checks, "errors": errors, "approval_required": True,
            "checked_at": utcnow(), "publication_authorized": False,
            "limitations": ["Live target page and existing DealerOn schema require pre-publication compatibility review.",
                            "Evidence is validated against recorded source claims; no network checks run during rendering."]}


def validate_draft(directory: Path) -> dict:
    """Revalidate source freshness and exact evidence-bound rendering, read-only."""
    directory = Path(directory)
    try:
        job = read_json(directory / "meta.json")
        if not isinstance(job, dict):
            raise ValueError("Draft metadata must be an object")
        errors, _, cited = _validate(job)
        html = (directory / "index.html").read_text(encoding="utf-8")
        evidence_text = (directory / "evidence.md").read_text(encoding="utf-8")
        if not errors and html != _render(job):
            errors.append("Rendered HTML does not match the supported metadata")
        for claim, refs in cited:
            if claim.replace("```", "` ` `") not in evidence_text or any(eid not in evidence_text for eid in refs):
                errors.append("Evidence document is missing a claim or citation")
        return _qa(html, job, errors)
    except (ValueError, TypeError, KeyError, OSError) as exc:
        return {"passed": False, "checks": {}, "errors": [str(exc)], "checked_at": utcnow(), "publication_authorized": False}


def generate_job(root: Path, job: dict) -> dict:
    """Generate one draft under the caller's queue lock. Leave failures pending."""
    root = Path(root)
    slug = job.get("slug")
    if job.get("kind") == "content_post":
        return {"slug": slug, "status": "skipped", "reason": "Content-post importer owns this draft"}
    try:
        validate_slug(slug)
    except (ValueError, TypeError) as exc:
        return {"slug": slug, "status": "blocked", "errors": [str(exc)]}
    directory = root / "drafts" / slug
    pending = root / "queue" / "pending" / f"{slug}.json"
    draft_queue = root / "queue" / "drafts" / f"{slug}.json"
    if any((root / "queue" / status / f"{slug}.json").exists() for status in ("drafts", "approved", "ready", "rejected", "hold")):
        return {"slug": slug, "status": "blocked", "errors": ["Job already has a review or publication state; refusing overwrite"]}
    errors, evidence, cited = _validate(job)
    html = _render(job) if not errors else ""
    report = _qa(html, job, errors)
    directory.mkdir(parents=True, exist_ok=True)
    atomic_json(directory / "qa-report.json", report)
    if not report["passed"]:
        failed = dict(job, status="pending", qa_passed=False, qa_errors=report["errors"] or [k for k, v in report["checks"].items() if not v], updated_at=utcnow())
        atomic_json(pending, failed)
        return {"slug": slug, "status": "blocked", "errors": failed["qa_errors"]}
    # These are local artifacts only. The queue marker is committed last.
    (directory / "index.html").write_text(html, encoding="utf-8")
    meta = dict(job, status="research-draft", approval_required=True, publication_authorized=False,
                canonical_candidate=job["target_url"], generated_at=utcnow())
    atomic_json(directory / "meta.json", meta)
    lines = [f"# Evidence: {slug}", "", "Publication status: NOT AUTHORIZED.", "",
             "Every public factual string below is copied verbatim from recorded verified source claims.", "",
             "## Claim citations", ""]
    for number, (claim, refs) in enumerate(cited, 1):
        lines.extend([f"### Claim {number}", "", "```text", claim.replace("```", "` ` `"), "```", "", "Evidence: " + ", ".join(refs), ""])
    lines.extend(["## Sources", ""])
    for eid, row in evidence.items():
        lines.extend([f"- {eid}: {row['source_type']}; retrieved {row['retrieved_at']}; {row['url']}"])
    lines.extend(["", "## Link verification", ""])
    for link in job["internal_links"]:
        kind = "same-site" if urlsplit(link["url"]).hostname == job["owner_host"] else "cross-site"
        lines.append(f"- {kind}: {link['url']}; HTTP {link['http_status']}; canonical {link['canonical']}; checked {link['checked_at']}")
        if link["canonical"] != link["url"]:
            lines.append("  Filtered inventory navigation with verified parent canonical; not a separately indexable destination.")
    (directory / "evidence.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    marker = dict(job, status="draft", qa_passed=True, draft_digest=draft_digest(directory),
                  drafted_at=utcnow(), approval_required=True, publication_authorized=False)
    marker.pop("qa_errors", None)
    atomic_json(draft_queue, marker)
    pending.unlink(missing_ok=True)
    return {"slug": slug, "status": "draft", "draft_digest": marker["draft_digest"]}


def generate(root: Path) -> dict:
    root = Path(root)
    results = []
    with lock(root, "queue"):
        for path in sorted((root / "queue" / "pending").glob("*.json")):
            try:
                job = read_json(path)
                if not isinstance(job, dict) or job.get("slug") != path.stem:
                    raise ValueError("Queue filename must match job slug")
                if job.get("kind") == "content_post":
                    continue
                results.append(generate_job(root, job))
            except (ValueError, TypeError, KeyError, OSError) as exc:
                results.append({"slug": path.stem, "status": "blocked", "errors": [str(exc)]})
    return {"generated": sum(r["status"] == "draft" for r in results), "blocked": sum(r["status"] == "blocked" for r in results), "jobs": results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1] / "pipeline")
    args = parser.parse_args()
    result = generate(args.root)
    print(json.dumps(result, indent=2))
    return 1 if result["blocked"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
