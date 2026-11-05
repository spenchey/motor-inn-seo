from __future__ import annotations

import argparse
import json
import urllib.request
from pathlib import Path


BRIEF = """Rewrite this one section for a skeptical Carroll, Iowa truck shopper.
Keep it plain, warm, a little wry, and specific.
Do not invent claims.
Section target: "What does car trim level mean?"
Current sentence:
A trim level is the version a buyer selects within the model. A base trim gets the essentials; higher trims add comfort, capability, or technology.
Return only the rewritten section text, no preamble."""


def call_glm(prompt: str, out_path: Path) -> None:
    endpoint = "http://127.0.0.1:8899/v1/chat/completions"
    payload = {"model": "GLM-5.3-Flash-EXL3", "messages": [{"role": "user", "content": prompt}], "max_tokens": 450}
    data = json.dumps(payload).encode()
    req = urllib.request.Request(endpoint, data=data, headers={"Content-Type": "application/json", "Authorization": "Bearer test"})
    body = json.load(urllib.request.urlopen(req, timeout=120))
    out_path.write_text(body["choices"][0]["message"]["content"])


def call_gemma(prompt: str, out_path: Path) -> None:
    endpoint = "http://127.0.0.1:11434/api/generate"
    payload = {"model": "gemma3:12b", "prompt": prompt, "stream": False}
    data = json.dumps(payload).encode()
    req = urllib.request.Request(endpoint, data=data, headers={"Content-Type": "application/json"})
    body = json.load(urllib.request.urlopen(req, timeout=180))
    out_path.write_text(body["response"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--brief", default="brain/research/trim-levels/model-brief.txt")
    parser.add_argument("--outdir", default="brain/reports/model-writeoff-2026-11-05-samples")
    parser.add_argument("--models", default="gemma")
    args = parser.parse_args()
    prompt = Path(args.brief).read_text()
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    for model in args.models.split(","):
        out_path = outdir / f"{model}.md"
        if model == "glm":
            call_glm(prompt, out_path)
        elif model == "gemma":
            call_gemma(prompt, out_path)
    print(f"saved to {outdir}")


if __name__ == "__main__":
    main()
