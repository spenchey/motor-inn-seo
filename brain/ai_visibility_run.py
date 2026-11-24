#!/usr/bin/env python3
"""AI-visibility run: does AI cite us for money queries? Prioritized fix output."""
import json, base64, urllib.request, datetime, os, re
from urllib.parse import urlparse

CREDS = "/Users/spencerheywood/.config/motorinn/dataforseo.env"
OUT = "/Users/spencerheywood/motor-inn-seo/brain/ai-visibility"
os.makedirs(OUT, exist_ok=True)
QUERIES = [
 "best used car dealer carroll iowa",
 "car dealerships in carroll iowa",
 "toyota service carroll iowa",
 "should I buy from motor inn carroll iowa",
]
# "Is this us": only our three sites (exact host, www./ai. stripped) or our own brand names.
# "Carroll" alone never counts (rivals are named for the town); neither does a bare
# "Toyota of Carroll". Rule: review/03_GAP_PLAN.md section 5.3 (2026-11-24 fix).
OUR_HOSTS = {"motorinnautogroup.com", "motorinntoyotaofcarroll.com", "motorinnofcarroll.com"}
NAME_RE = re.compile(r"\bmotor\s*inn\s+(auto|of\s+carroll|toyota|chevrolet)\b", re.I)

def _host_ours(h):
    h = (h or "").strip().lower().rstrip(".")
    if not h or " " in h: return False
    for pre in ("www.", "ai."):
        if h.startswith(pre): h = h[len(pre):]
    return h in OUR_HOSTS

def _host_of(url):
    """Host of a URL, or "" when it is empty or malformed (urlparse raises ValueError on some input)."""
    if not url: return ""
    try:
        return urlparse(url).hostname or ""
    except ValueError:
        return ""

def is_us(src, title, url="", domain=""):
    src, title, url, domain = (str(x) if x else "" for x in (src, title, url, domain))
    if _host_ours(_host_of(url)) or _host_ours(domain) or _host_ours(src): return True
    return bool(NAME_RE.search(src + " | " + title))

def auth():
    txt=open(CREDS).read()
    u=[l.split("=",1)[1].strip() for l in txt.splitlines() if l.startswith("DATAFORSEO_USERNAME")][0]
    p=[l.split("=",1)[1].strip() for l in txt.splitlines() if l.startswith("DATAFORSEO_PASSWORD")][0]
    return "Basic "+base64.b64encode(f"{u}:{p}".encode()).decode()

def ai_mode(q):
    req=urllib.request.Request("https://api.dataforseo.com/v3/serp/google/ai_mode/live/advanced",
        data=json.dumps([{"keyword":q,"location_code":2840,"language_code":"en"}]).encode(),
        headers={"Authorization":auth(),"Content-Type":"application/json"})
    d=json.load(urllib.request.urlopen(req,timeout=180))
    items=(d["tasks"][0].get("result") or [{}])[0].get("items",[]) or []
    refs=[]
    for it in items:
        if it.get("type")=="ai_overview":
            for ref in it.get("references",[]) or []:
                src=(ref.get("source") or "")[:60]; title=(ref.get("title") or "")[:70]
                refs.append((src,title,(ref.get("url") or ""),(ref.get("domain") or "")))
    return refs

today=datetime.date.today().isoformat()
lines=[f"# AI visibility {today}\n"]
allrows=[]
for q in QUERIES:
    refs=ai_mode(q)
    us=[r for r in refs if is_us(*r)]
    lines.append(f"## {q}\n")
    for src,t,_u,_d in refs[:8]: lines.append(f"- {src} | {t}")
    lines.append(f"**WE: {len(us)} of {len(refs)}**\n")
    allrows+=refs
# prioritized fix: top cited domains where we're absent
from collections import Counter
cnt=Counter(r[0] for r in allrows)
miss=[(s,c) for s,c in cnt.most_common(10) if not is_us(s,"")]
lines.append("## Prioritized fixes (cited often, we absent)\n")
for s,c in miss[:5]: lines.append(f"- Get onto/into: {s} (cited {c}x across queries)")
open(f"{OUT}/ai-vis-{today}.md","w").write("\n".join(lines))
print("\n".join(lines[-9:]))
print("saved", f"{OUT}/ai-vis-{today}.md")
