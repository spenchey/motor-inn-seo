#!/usr/bin/env python3
"""Audit the 8 source packages: CTAs, phones, brand mentions, section inventory."""
import re, glob, os

SRC = "/Users/spenchey/motorinn-dispatch/docs/generated/seo-pages/page-packages-2026-10"
for f in sorted(glob.glob(os.path.join(SRC, "*.html"))):
    if f.endswith("index.html"):
        continue
    html = open(f).read()
    name = os.path.basename(f)
    ctas = re.findall(r'<a href="(https://www\.motorinnautogroup\.com[^"]*)">([^<]+)</a>', html)
    phones = set(re.findall(r'\(\d{3}\)\s?\d{3}-\d{4}|\d{3}-\d{3}-\d{4}', html))
    brands = set(re.findall(r'Buick|GMC|Cadillac|Chrysler|Dodge|Jeep|Ram|Ford|Hyundai|Kia|Nissan|Honda|Mazda|Subaru|Volkswagen', html))
    faqs = len(re.findall(r'seo-faq-item', html))
    h1 = re.search(r'<h1>(.*?)</h1>', html)
    print(name)
    print("  H1:", h1.group(1) if h1 else None)
    print("  CTAs:", ctas[:8])
    print("  phones:", phones, "| brands:", brands or "none", "| faq items:", faqs)
