#!/usr/bin/env python3
"""Holmberg draft writer via our llama (GLM-5.3-Flash-EXL3 on spark-a664:8888)."""
import json, urllib.request, sys, os, subprocess, datetime

LLM = "http://100.67.25.103:8888/v1/chat/completions"
REPO = "/Users/spencerheywood/motor-inn-seo"

def llm(messages, temp=0.6, max_tokens=3000):
    body = json.dumps({"model":"GLM-5.3-Flash-EXL3","messages":messages,
                       "temperature":temp,"max_tokens":max_tokens}).encode()
    req = urllib.request.Request(LLM, data=body, headers={"Content-Type":"application/json"})
    d = json.load(urllib.request.urlopen(req, timeout=300))
    return d["choices"][0]["message"]["content"]

def sh(c):
    return subprocess.run(["bash","-lc",c], capture_output=True, text=True, timeout=120).stdout

slug = sys.argv[1]
rd = sh(f"cat {REPO}/brain/research/{slug}/research.md 2>/dev/null")
if not rd.strip():
    print("NO RESEARCH FILE for", slug); sys.exit(1)
voice = open(f"{REPO}/brain/VOICE-DNA.md").read()
brief = open(f"{REPO}/brain/BRIEF.md").read()
tmpl = open(f"{REPO}/brain/BRIEF.md") # placeholder
existing = sh(f"cat {REPO}/content/drafts/seo/{slug}-current.html 2>/dev/null")

sys.path.insert(0, f"{REPO}/.venv/lib/python3.13/site-packages")
msgs = [
 {"role":"system","content":f"You are the web writer for Motor Inn Auto Group (Carroll, Iowa Toyota+Chevrolet dealer). Follow the VOICE DNA and house rules exactly. Anti-slop ban list is binding. Every factual claim must carry its source URL from the research file, or the flag [NEEDS-VERIFY]. Never invent prices, payments, dates, awards.\n\nVOICE DNA:\n{voice}\n\nHOUSE RULES:\n{brief[:2500]}"},
 {"role":"user","content":f"RESEARCH FILE:\n{rd[:6000]}\n\nCURRENT PAGE (if any):\n{existing[:2000]}\n\nTASK: Write the full page copy as HTML. Structure: one H1; every H2 phrased as the real search query from research; FIRST sentence under each H2 answers it directly, evidence after; each section stands alone; ONE CTA; local entities correct (Carroll 51401). Output ONLY the HTML body content, no commentary."}
]
draft = llm(msgs)
today = datetime.date.today().isoformat()
os.makedirs(f"{REPO}/content/drafts/seo", exist_ok=True)
open(f"{REPO}/content/drafts/seo/{slug}-draft.html","w").write(draft)
sha = sh(f"cd {REPO} && git rev-parse --short HEAD:brain 2>/dev/null || echo na").strip()
review = f"""# REVIEW: {slug}
date: {today}
research_sha: {sha}
## Draft
{draft}
## Sources (from research)
see brain/research/{slug}/research.md
## Needs-verify items
(flagged inline above)
## Questions for Spencer
1. Voice OK?
2. Any claim to soften?
3. CTA right?
"""
open(f"{REPO}/content/drafts/seo/{slug}-REVIEW.md","w").write(review)
print("WROTE draft+review for", slug, len(draft), "chars")
