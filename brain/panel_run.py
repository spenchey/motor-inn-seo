#!/usr/bin/env python3
"""10-expert SEO panel scorer (Eric Siu panel) via local llama."""
import json, urllib.request, sys, subprocess, datetime

LLM = "http://100.67.25.103:8888/v1/chat/completions"
REPO = "/Users/spencerheywood/motor-inn-seo"
EXPERTS = ["Technical SEO Specialist","Content Strategist","Conversion Rate Optimizer",
 "Revenue Attribution Expert","Competitive Analyst","AI/AEO Specialist","Data Scientist",
 "Growth Hacker","Operations Expert","ROI Calculator"]

def llm(messages, temp=0.3, max_tokens=400):
    body = json.dumps({"model":"GLM-5.3-Flash-EXL3","messages":messages,
                       "temperature":temp,"max_tokens":max_tokens}).encode()
    req = urllib.request.Request(LLM, data=body, headers={"Content-Type":"application/json"})
    return json.load(urllib.request.urlopen(req, timeout=180))["choices"][0]["message"]["content"]

def sh(c): return subprocess.run(["bash","-lc",c],capture_output=True,text=True,timeout=60).stdout

target = sys.argv[1]
plan = open(target).read()
panel = open(f"{REPO}/brain/SEO-PANEL.md").read()
brief = open(f"{REPO}/brain/BRIEF.md").read()[:1500]

results = []
for e in EXPERTS:
    msgs = [
     {"role":"system","content":f"You are the {e} from this panel. Score the plan 0-100 on the criteria. Be harsh; dock vague claims. Reply EXACTLY:\nSCORE: <int>\nONE-LINE: <verdict>\nFIX: <weakest point>\n\nPanel:\n{panel[:1800]}\n\nBUSINESS:\n{brief}"},
     {"role":"user","content":plan[:6000]}]
    try:
        out = llm(msgs)
        score = int(str(out).split("SCORE:")[1].split("\n")[0].strip()[:3].strip())
        one = str(out).split("ONE-LINE:")[1].split("\n")[0].strip()[:140]
        fix = str(out).split("FIX:")[1].split("\n")[0].strip()[:140] if "FIX:" in out else ""
    except Exception as ex:
        score, one, fix = 0, f"parse err {ex}", ""
    results.append((e, score, one, fix))
    print(f"{e}: {score} | {one[:90]}")

mean = sum(s for _,s,_,_ in results)/len(results)
worst = min(results, key=lambda x:x[1])
print(f"MEAN: {mean:.0f} | MIN: {worst[0]} {worst[1]}")
logline = f"\n## PANEL {datetime.datetime.now().isoformat()[:16]} target={target} mean={mean:.0f}\n"
for e,s,o,f in results: logline += f"- {e}: {s} | {o}\n"
open(f"{REPO}/brain/LOG.md","a").write(logline)
json.dump({"mean":mean,"results":results}, open("/tmp/panel_last.json","w"))
