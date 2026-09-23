import json, urllib.request, re
from html.parser import HTMLParser

class TextExtract(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0; self.parts = []; self.h1s = []; self.in_h1 = 0; self.title = ""
        self.in_title = 0
    def handle_starttag(self, tag, attrs):
        if tag in ("script","style","noscript"): self.skip += 1
        if tag == "h1": self.in_h1 += 1
        if tag == "title": self.in_title += 1
    def handle_endtag(self, tag):
        if tag in ("script","style","noscript") and self.skip: self.skip -= 1
        if tag == "h1": self.in_h1 = max(0, self.in_h1-1)
        if tag == "title": self.in_title = max(0, self.in_title-1)
    def handle_data(self, data):
        if self.skip: return
        if self.in_h1: self.h1s.append(data.strip())
        if self.in_title: self.title += data
        t = data.strip()
        if len(t) > 40: self.parts.append(t)

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"})
    html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8","ignore")
    p = TextExtract(); p.feed(html)
    return {"url": url, "title": p.title.strip(), "h1s": p.h1s[:3], "text_chars": sum(len(x) for x in p.parts), "paragraphs": p.parts[:12]}

import json as j
urls = j.load(open("/tmp/comp_urls.json"))
out = []
errors = []
for u in urls:
    try:
        out.append(fetch(u))
    except Exception as e:
        errors.append((u, str(e)[:60]))
print("errors:", errors)
j.dump(out, open("/tmp/comp_scrapes.json","w"), indent=1)
print("scraped:", len(out), "pages;", [o["text_chars"] for o in out])
