#!/usr/bin/env python3
"""Weekly keyword-gap v2: competitor ranks, we don't. Buyer-intent."""
import json, os, csv, datetime, base64, urllib.request

CREDS = "/Users/spencerheywood/.config/motorinn/dataforseo.env"
OUT = "/Users/spencerheywood/motor-inn-seo/brain/gap"
os.makedirs(OUT, exist_ok=True)
ME = "motorinnautogroup.com"
COMPETITORS = ["choiceauto.biz","wittrockmotor.com","proautosales.net","billionauto.com"]
BUYER = ("used","new","truck","suv","sedan","toyota","chevrolet","silverado","tacoma",
         "highlander","equinox","blazer","colorado","traverse","financ","lease","trade",
         "test drive","oil change","servic","dealer")

def auth():
    txt = open(CREDS).read()
    u = [l.split("=",1)[1].strip() for l in txt.splitlines() if l.startswith("DATAFORSEO_USERNAME")][0]
    p = [l.split("=",1)[1].strip() for l in txt.splitlines() if l.startswith("DATAFORSEO_PASSWORD")][0]
    return "Basic "+base64.b64encode(f"{u}:{p}".encode()).decode()

def post(path, data):
    req = urllib.request.Request("https://api.dataforseo.com"+path,
        data=json.dumps(data).encode(), headers={"Authorization":auth(),"Content-Type":"application/json"})
    d = json.load(urllib.request.urlopen(req, timeout=120))
    if d.get("status_code") != 20000: raise RuntimeError(d.get("status_message"))
    return d["tasks"][0].get("result") or []

rows=[]
for comp in COMPETITORS:
    res = post("/v3/dataforseo_labs/google/domain_intersection/live",
        [{"target1":comp,"target2":ME,"location_code":2840,"language_code":"en",
          "intersections":False,"limit":200}])
    n=0
    for r in res:
        for it in r.get("items",[]) or []:
            info = it.get("keyword_data",{})
            kw = (info.get("keyword") or "")
            kl = kw.lower()
            me = it.get("first_domain_serp_element") or {}
            th = it.get("second_domain_serp_element") or {}
            thpos = me.get("rank_absolute") or 999
            mypos = th.get("rank_absolute") or 999
            # gap = competitor ranks well, we rank absent or worse
            if thpos > 30: continue
            if mypos < 999 and mypos <= thpos: continue
            if not any(b in kl for b in BUYER): continue
            rows.append({"competitor":comp,"keyword":kw,"their_pos":thpos,"our_pos":mypos,
                         "volume":(info.get("keyword_info") or {}).get("search_volume") or 0,
                         "url":(th.get("url") or "")[:120]})
            n+=1
    print(f"{comp}: kept {n}")

best={}
for r in rows:
    k=r["keyword"]
    c=best.get(k)
    if not c or (r["their_pos"],-r["volume"])<(c["their_pos"],-c["volume"]): best[k]=r
rows=sorted(best.values(), key=lambda r:(-(r["volume"] or 0), r["their_pos"]))

today=datetime.date.today().isoformat()
with open(f"{OUT}/gap-{today}.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=["keyword","volume","competitor","their_pos","our_pos","url"])
    w.writeheader()
    for r in rows[:80]: w.writerow(r)

top="\n".join(f"- {r['keyword']} (vol {r['volume']}, {r['competitor']} pos {r['their_pos']}, we: {r['our_pos'] if r['our_pos']<999 else 'absent'})" for r in rows[:15])
open(f"{OUT}/gap-{today}.md","w").write(
    f"# Keyword gap {today}\n\nCompetitor ranks top-30, we don't (or worse). Buyer-intent.\n\n## Top opportunities\n{top}\n\nFull: gap-{today}.csv ({len(rows)} uniq)\n")
print(f"UNIQUE GAPS: {len(rows)}")
print(top)
