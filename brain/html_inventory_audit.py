#!/usr/bin/env python3
"""Crawlability audit for live inventory on the three Motor Inn public hosts.

Usage:
python3 brain/html_inventory_audit.py
Reads the public sitemap for each site, crawls the reachable static HTML anchors, and lists
vehicle-detail URLs that are not reachable through any static anchor yet. This is evidence for
a DealerOn crawlability case if needed.
"""
import re, sys
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup

SITES = [
    "https://www.motorinnautogroup.com",
    "https://www.motorinntoyotaofcarroll.com",
    "https://www.motorinnofcarroll.com",
]
VEHICLE_RE = re.compile(r"/(?:(?:new|used)-[A-Za-z0-9-]+|vehicle)/", re.I)

def fetch(url: str, timeout: int = 15) -> str:
    resp = requests.get(url, timeout=timeout, headers={"User-Agent": "MotorInn-CrawlabilityAudit/1.0"}, allow_redirects=True)
    resp.raise_for_status()
    return resp.text

def sitemap_vehicle_urls(soup: BeautifulSoup) -> list[str]:
    """Vehicle-detail URLs found in the public sitemap."""
    return [loc.text.strip() for loc in soup.find_all("loc") if VEHICLE_RE.search(urlparse(loc.text.strip()).path)]


def static_hrefs(html: str | BeautifulSoup) -> set[str]:
    soup = html if isinstance(html, BeautifulSoup) else BeautifulSoup(html, "html.parser")
    return {a.get("href") for a in soup.find_all("a") if a.get("href")}

def js_only_pages(vehicle_urls: Iterable[str], static_links: Iterable[str]) -> list[str]:
    return sorted(set(vehicle_urls) - set(static_links))


def reachable_vehicle_urls(site: str, urls: Iterable[str]) -> set[str]:
    out: set[str] = set()
    for candidate in urls:
        try:
            html = fetch(candidate)
        except Exception as exc:
            print(f"fetch_error\t{candidate}\t{exc}", file=sys.stderr)
            continue
        for href in static_hrefs(html):
            absolute = urljoin(candidate, href)
            if VEHICLE_RE.search(urlparse(absolute).path):
                out.add(absolute.split("?")[0])
    return out

def audit_site(site: str) -> list[str]:
    xml = fetch(f"{site}/sitemap.xml")
    vehicle_urls = sitemap_vehicle_urls(BeautifulSoup(xml, "xml"))
    static_urls = urlparse_reachable(site)
    return js_only_pages((u.split("?")[0] for u in vehicle_urls), static_urls)



def main() -> int:
    out = Path("brain/reports/inventory-crawlability-audit.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Inventory crawlability audit", "", "Vehicle-detail URLs in the sitemap that are reachable only through JS on the audited pages. A URL here is still crawlable if it is linked from another unseeded page.",
             "This is evidence for a DealerOn case if the pattern repeats across pages.", ""]  # noqa: E501
    for site in SITES:
        try:
            missing = audit_site(site)
        except Exception as exc:
            lines.append(f"## {site} — audit failed ({exc})")
            lines.append("See the exception output above for the exact fetch failure.")
            continue
        lines.extend([f"## {site}", "", f"{len(missing)} vehicle URLs not found in the audited static anchors.", "", *missing, ""])
    out.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    print(f"HTML\t{out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
