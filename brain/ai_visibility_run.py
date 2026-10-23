#!/usr/bin/env python3
"""AI-visibility run: does AI cite us for money queries? Prioritized fix output."""
import json, base64, urllib.request, datetime, os

CREDS = "/Users/spencerheywood/.config/motorinn/dataforseo.env"
OUT = "/Users/spencerheywood/motor-inn-seo/brain/ai-visibility"
os.makedirs(OUT, exist_ok=True)
QUERIES = [
 "best used car dealer carroll iowa",
 "car dealerships in carroll iowa",
 "toyota service carroll iowa",
 "should I buy from motor inn carroll iowa",
]
ME = ("motorinn","carroll")

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
                refs.append((src,title))
    return refs

today=datetime.date.today().isoformat()
lines=[f"# AI visibility {today}\n"]
allrows=[]
for q in QUERIES:
    refs=ai_mode(q)
    us=[r for r in refs if any(m in (r[0]+r[1]).lower() for m in ME)]
    lines.append(f"## {q}\n")
    for src,t in refs[:8]: lines.append(f"- {src} | {t}")
    lines.append(f"**WE: {len(us)} of {len(refs)}**\n")
    allrows+=refs
# prioritized fix: top cited domains where we're absent
from collections import Counter
cnt=Counter(s for s,t in allrows)
miss=[(s,c) for s,c in cnt.most_common(10) if not any(m in s.lower() for m in ME)]
lines.append("## Prioritized fixes (cited often, we absent)\n")
for s,c in miss[:5]: lines.append(f"- Get onto/into: {s} (cited {c}x across queries)")
open(f"{OUT}/ai-vis-{today}.md","w").write("\n".join(lines))
print("\n".join(lines[-9:]))
print("saved", f"{OUT}/ai-vis-{today}.md")
