#!/usr/bin/env python3
"""Verification pass 1: approved content integrity of designed pages vs sources."""
import re
import os

SRC = "/Users/spenchey/motorinn-dispatch/docs/generated/seo-pages/page-packages-2026-10"
OUT = os.path.join(SRC, "designed")

PAGES = [
    "used-trucks-carroll-iowa",
    "used-cars-carroll-iowa",
    "car-dealerships-carroll-iowa",
    "toyota-dealer-carroll-iowa",
    "best-place-to-buy-used-car-carroll-iowa",
    "new-vs-used-car-carroll-iowa",
    "auto-service-carroll-iowa",
    "where-to-service-toyota-carroll-iowa",
]

ok = True
for slug in PAGES:
    src = open(os.path.join(SRC, slug + ".html")).read()
    out = open(os.path.join(OUT, slug + ".html")).read()

    checks = {}
    # 1. comment block preserved
    cm = re.search(r'<!--\s*DealerOn copy/paste package.*?-->', src, re.S)
    checks['comment_block'] = (cm.group(0) in out) if cm else None
    # 2. title + meta desc + canonical preserved
    checks['title'] = re.search(r'<title>(.*?)</title>', src).group(1) in out
    checks['meta_desc'] = re.search(r'<meta name="description" content="([^"]*)"', src).group(1) in out
    checks['canonical'] = re.search(r'<link rel="canonical" href="([^"]*)"', src).group(1) in out
    # 3. all approved links preserved
    src_links = set(re.findall(r'href="(https://www\.motorinnautogroup\.com[^"]*)"', src))
    out_links = set(re.findall(r'href="(https://www\.motorinnautogroup\.com[^"]*)"', out))
    checks['all_src_links_present'] = src_links.issubset(out_links)
    missing = src_links - out_links
    # 4. JSON-LD schema preserved verbatim
    ld = re.search(r'(<script type="application/ld\+json">.*?</script>)', src, re.S).group(1)
    checks['faq_schema_verbatim'] = ld in out
    # 5. phone preserved
    checks['phone'] = '(712) 522-2526' in out
    # 6. address preserved
    checks['address'] = '1526 Le Clark Road' in out
    # 7. brand rule: no Buick/GMC
    checks['no_buick_gmc'] = ('Buick' not in out and 'GMC' not in out)
    # 8. all h2 sections preserved
    src_h2 = set(re.findall(r'<h2>(.*?)</h2>', src))
    out_h2 = set(re.findall(r'<h2>(.*?)</h2>', out))
    checks['all_h2_preserved'] = src_h2.issubset(out_h2)
    missing_h2 = src_h2 - out_h2
    # 9. FAQ Q&A text preserved
    src_faqs = re.findall(r'<div class="seo-faq-item">\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>', src, re.S)
    faq_ok = all((q.strip() in out) and (a.strip() in out) for q, a in src_faqs)
    checks['faq_qa_text'] = faq_ok

    status = all(v is True or v is None for v in checks.values())
    ok = ok and status
    print(slug, "PASS" if status else "FAIL",
          "" if status else {k: v for k, v in checks.items() if v not in (True, None)})
    if missing:
        print("  missing links:", missing)
    if missing_h2:
        print("  missing h2:", missing_h2)

print("\nALL PASS" if ok else "\nSOME FAILED")
