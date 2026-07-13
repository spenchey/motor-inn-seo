#!/bin/bash
#
# rory-seo-inspect.sh  (MOT-2443)
#
# Runs the rory-seo INSPECTOR (hermes profile, LOCAL qwen3.6 endpoint) over one
# day's deterministic toolkit output. The inspector interprets, dedupes against
# open Linear cards, ranks severity, and proposes cards. It may not invent
# scores — every claim must cite an analyzer JSON field.
#
# NOT part of the cron path. The scheduled weekly/monthly pipelines use the
# deterministic template (scripts/seo-toolkit-findings.py) — house rule: no
# LLM in cron paths that can be deterministic. Run this by hand, or wire it
# later as an explicitly separate cron step if Spencer approves.
#
# FAIL-LOUD: if the local endpoint is down, this exits nonzero with a clear
# message. There is NO cloud fallback, by design.
#
# Usage: rory-seo-inspect.sh [YYYY-MM-DD]   (default: today, America/Chicago)
#
# Output (into the toolkit day dir):
#   inspector-synthesis.md   — cited, prioritized synthesis
#   proposed-cards.json      — {"proposed_cards":[...]} for the pipeline to file
#
# Exit codes: 0 ok | 2 missing input | 3 endpoint down | 4 bad inspector output

set -uo pipefail
export PATH="/opt/homebrew/bin:/opt/homebrew/opt/node@24/bin:/Users/spencerheywood/.local/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

REPO="$HOME/motor-inn-seo"
VENV_PY="$REPO/tools/.venv-toolkit/bin/python"
HERMES="$HOME/.local/bin/hermes"
PROFILE="rory-seo"
ENDPOINT="http://100.75.67.104:11434/v1"   # keep in sync with the profile config.yaml
MODEL="qwen3.6:35b-a3b"
LINEAR_LIST="$HOME/clawd/scripts/linear/list.mjs"

DAY="${1:-$(TZ=America/Chicago date +%Y-%m-%d)}"
OUT="$REPO/audits/toolkit/$DAY"

log() { printf '[%s] %s\n' "$(date +%H:%M:%S)" "$*"; }

if [ ! -s "$OUT/summary.json" ]; then
  log "fatal: no toolkit output at $OUT (run scripts/run-seo-toolkit.sh first)"
  exit 2
fi

# --- preflight: LOCAL endpoint must be up; no fallback ------------------------
if ! curl -s -m 8 "$ENDPOINT/models" | grep -q "$MODEL"; then
  log "fatal: local model endpoint DOWN or missing $MODEL at $ENDPOINT."
  log "House rule: no cloud fallback. Fix the endpoint (fa5a Spark) and rerun."
  exit 3
fi

# --- assemble evidence ---------------------------------------------------------
PROMPT_FILE="$OUT/inspector-prompt.txt"
: >"$PROMPT_FILE"

append_file() { # <label> <path> <max-chars>
  local label="$1" path="$2" max="$3"
  {
    printf '\n===== %s =====\n' "$label"
    if [ -s "$path" ]; then
      head -c "$max" "$path"
      if [ "$(wc -c <"$path")" -gt "$max" ]; then printf '\n[truncated]\n'; fi
    else
      printf '(missing)\n'
    fi
  } >>"$PROMPT_FILE"
}

{
  printf 'INSPECTOR RUN — toolkit output %s.\n' "$DAY"
  printf 'Follow your SOUL contract exactly: cite [file#field] for every claim,\n'
  printf 'dedupe against the open Linear cards below, output EXACTLY two fenced\n'
  printf 'blocks (```markdown synthesis, then ```json proposed_cards). Do not use\n'
  printf 'any tools; everything you need is in this prompt.\n'
} >>"$PROMPT_FILE"

# Open Linear cards for dedupe (enrichment: absence is stated, never silent)
if command -v node >/dev/null 2>&1 && [ -f "$LINEAR_LIST" ]; then
  if OPEN_CARDS=$(node "$LINEAR_LIST" 2>/dev/null | head -60); then
    printf '\n===== OPEN LINEAR CARDS (dedupe against these) =====\n%s\n' "$OPEN_CARDS" >>"$PROMPT_FILE"
  else
    printf '\n===== OPEN LINEAR CARDS =====\nUNAVAILABLE this run — mark every proposal dedupe_of: null and say dedupe was not possible.\n' >>"$PROMPT_FILE"
  fi
else
  printf '\n===== OPEN LINEAR CARDS =====\nUNAVAILABLE this run — mark every proposal dedupe_of: null and say dedupe was not possible.\n' >>"$PROMPT_FILE"
fi

append_file "summary.json" "$OUT/summary.json" 4000
for j in technical crawlers llmstxt onpage drift citability content-quality sitemap brand; do
  [ -f "$OUT/$j.json" ] && append_file "$j.json" "$OUT/$j.json" 6000
done
append_file "findings.md (deterministic template — grade/extend it, cite what you change)" "$OUT/findings.md" 6000
append_file "checklist: marketingskills seo-audit" "$REPO/tools/skills-sh/marketingskills-seo-audit/SKILL.md" 4000
append_file "checklist: opc seo-geo" "$REPO/tools/skills-sh/opc-seo-geo/SKILL.md" 4000

# --- invoke the inspector (one-shot, local) -------------------------------------
log "invoking hermes profile $PROFILE ($MODEL @ $ENDPOINT)"
RAW="$OUT/inspector-raw.txt"
if ! "$HERMES" -p "$PROFILE" -z "$(cat "$PROMPT_FILE")" >"$RAW" 2>"$OUT/inspector-stderr.log"; then
  log "fatal: hermes one-shot failed (see $OUT/inspector-stderr.log). No fallback."
  exit 3
fi

# --- split + validate the two fenced blocks --------------------------------------
if ! "$VENV_PY" - "$RAW" "$OUT/inspector-synthesis.md" "$OUT/proposed-cards.json" <<'PY'
import json, re, sys
raw_path, md_path, cards_path = sys.argv[1:]
raw = open(raw_path).read()
blocks = re.findall(r"```(\w+)?\n(.*?)```", raw, re.DOTALL)
md = next((b for lang, b in blocks if (lang or "").lower() == "markdown"), None)
js = next((b for lang, b in blocks if (lang or "").lower() == "json"), None)
if js is None:
    sys.stderr.write("inspector output missing required json fenced block\n")
    sys.exit(1)
if md is None:
    # Local models often emit the synthesis as unfenced markdown before the
    # json block. Accept that iff it still honors the rest of the contract.
    head = raw.split("```json")[0].strip()
    head = re.sub(r"```(markdown)?\s*$", "", head).strip()
    if "Inspector Synthesis" in head:
        md = head
if md is None:
    sys.stderr.write("inspector output missing the synthesis block\n")
    sys.exit(1)
if "Inspector Synthesis" not in md or ".json#" not in md:
    sys.stderr.write("synthesis missing heading or [file#field] citations — contract violation\n")
    sys.exit(1)
cards = json.loads(js)
assert isinstance(cards.get("proposed_cards"), list), "proposed_cards missing"
for c in cards["proposed_cards"]:
    assert c.get("title") and c.get("severity") and c.get("evidence"), f"incomplete card: {c}"
open(md_path, "w").write(md.strip() + "\n")
open(cards_path, "w").write(json.dumps(cards, indent=2) + "\n")
print(f"cards proposed: {len(cards['proposed_cards'])}")
PY
then
  log "fatal: inspector output violated the contract (raw kept at $RAW)."
  log "The deterministic findings.md remains the source of truth."
  exit 4
fi

log "inspector synthesis: $OUT/inspector-synthesis.md"
log "proposed cards:      $OUT/proposed-cards.json (pipeline files these — inspector never does)"
exit 0
