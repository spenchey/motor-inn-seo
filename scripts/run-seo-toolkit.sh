#!/bin/bash
#
# run-seo-toolkit.sh  (MOT-2431)
#
# Deterministic GEO/SEO analyzer battery for Motor Inn. Runs the vendored
# claude-seo + geo-seo-claude Python analyzers against the configured target
# URL and writes machine-readable output plus a deterministic findings section.
#
# HARD RULES:
#   - NO LLM anywhere in this script. Synthesis is deterministic templating
#     (scripts/seo-toolkit-findings.py). The optional inspector pass lives in
#     scripts/rory-seo-inspect.sh and is NOT called from here.
#   - Fail loud: exits nonzero if any analyzer crashes. Callers (weekly/monthly
#     clawd wrappers) own Slack escalation.
#
# Usage:
#   run-seo-toolkit.sh [--weekly|--monthly] [--url URL] [--outdir DIR]
#
# Output: ~/motor-inn-seo/audits/toolkit/YYYY-MM-DD/
#   technical.json crawlers.json llmstxt.json onpage.json drift.json
#   [monthly: citability.json content-quality.json sitemap.json brand.json]
#   summary.json findings.md run.log
#
# Config: ~/motor-inn-seo/config/seo-toolkit.env (SEO_TOOLKIT_URL swaps to
# https://www.motorinnautogroup.com at cutover).

set -uo pipefail

REPO="$HOME/motor-inn-seo"
TOOLS="$REPO/tools"
VENV_PY="$TOOLS/.venv-toolkit/bin/python"
CONFIG="$REPO/config/seo-toolkit.env"
GEO_SCRIPTS="$TOOLS/geo-seo-claude/scripts"
CS_SCRIPTS="$TOOLS/claude-seo/scripts"
FINDINGS_PY="$REPO/scripts/seo-toolkit-findings.py"

SCOPE="weekly"
URL_OVERRIDE=""
OUT_OVERRIDE=""

while [ $# -gt 0 ]; do
  case "$1" in
    --weekly) SCOPE="weekly" ;;
    --monthly) SCOPE="monthly" ;;
    --url) shift; URL_OVERRIDE="${1:-}" ;;
    --outdir) shift; OUT_OVERRIDE="${1:-}" ;;
    *) printf 'unknown argument: %s\n' "$1" >&2; exit 2 ;;
  esac
  shift
done

# --- config -----------------------------------------------------------------
if [ -f "$CONFIG" ]; then
  # shellcheck disable=SC1090
  source "$CONFIG"
fi
TARGET_URL="${URL_OVERRIDE:-${SEO_TOOLKIT_URL:-}}"
BRAND_NAME="${SEO_TOOLKIT_BRAND:-Motor Inn Auto Group}"
BRAND_DOMAIN="${SEO_TOOLKIT_BRAND_DOMAIN:-motorinnautogroup.com}"

if [ -z "$TARGET_URL" ]; then
  printf 'fatal: no target URL (set SEO_TOOLKIT_URL in %s or pass --url)\n' "$CONFIG" >&2
  exit 2
fi
if [ ! -x "$VENV_PY" ]; then
  printf 'fatal: toolkit venv missing at %s (see tools/PROVENANCE.md to rebuild)\n' "$VENV_PY" >&2
  exit 2
fi
if [ ! -f "$FINDINGS_PY" ]; then
  printf 'fatal: findings synthesizer missing at %s\n' "$FINDINGS_PY" >&2
  exit 2
fi

TODAY=$(TZ=America/Chicago date +%Y-%m-%d)
OUT="${OUT_OVERRIDE:-$REPO/audits/toolkit/$TODAY}"
mkdir -p "$OUT"
RUN_LOG="$OUT/run.log"

log() { printf '[%s] %s\n' "$(date +%H:%M:%S)" "$*" | tee -a "$RUN_LOG"; }

log "=== SEO toolkit $SCOPE run — $TODAY — $TARGET_URL ==="

FAILED=()
STATUSES=()   # "name:status" pairs for summary.json

record() { STATUSES+=("$1=$2"); }

# run_analyzer <name> <cmd...>  — capture stdout JSON to $OUT/<name>.json
run_analyzer() {
  local name="$1"; shift
  local out_file="$OUT/$name.json"
  log "analyzer $name: $*"
  if "$@" >"$out_file" 2>>"$RUN_LOG"; then
    if "$VENV_PY" -c "import json,sys; json.load(open(sys.argv[1]))" "$out_file" 2>>"$RUN_LOG"; then
      record "$name" "ok"
      return 0
    fi
    log "analyzer $name: wrote invalid JSON"
  else
    log "analyzer $name: exited nonzero"
  fi
  record "$name" "failed"
  FAILED+=("$name")
  return 1
}

# --- weekly (light) battery ---------------------------------------------------
# technical: page fetch analysis (status, redirects, meta, canonical, headers)
run_analyzer technical "$VENV_PY" "$GEO_SCRIPTS/fetch_page.py" "$TARGET_URL" page || true

# crawlers: robots.txt AI-crawler access (GPTBot, ClaudeBot, PerplexityBot, ...)
run_analyzer crawlers "$VENV_PY" "$GEO_SCRIPTS/fetch_page.py" "$TARGET_URL" robots || true

# llmstxt: llms.txt presence + validation
run_analyzer llmstxt "$VENV_PY" "$GEO_SCRIPTS/llmstxt_generator.py" "$TARGET_URL" validate || true

# onpage: fetch homepage HTML once, then parse SEO metadata out of it
HOMEPAGE_HTML="$OUT/homepage.html"
if "$VENV_PY" "$CS_SCRIPTS/fetch_page.py" "$TARGET_URL" --output "$HOMEPAGE_HTML" >>"$RUN_LOG" 2>&1 \
  && [ -s "$HOMEPAGE_HTML" ]; then
  record "homepage-fetch" "ok"
  run_analyzer onpage "$VENV_PY" "$CS_SCRIPTS/parse_html.py" "$HOMEPAGE_HTML" --url "$TARGET_URL" --json || true
else
  log "homepage fetch failed — onpage analyzer skipped (counted as failure)"
  record "homepage-fetch" "failed"
  record "onpage" "failed"
  FAILED+=("onpage")
fi

# drift: compare against last stored baseline, then store today's snapshot.
# First run has no baseline — that is a visible non-crash (baseline-created).
DRIFT_OUT="$OUT/drift.json"
if "$VENV_PY" "$CS_SCRIPTS/drift_compare.py" "$TARGET_URL" --skip-cwv >"$DRIFT_OUT" 2>>"$RUN_LOG"; then
  record "drift" "ok"
else
  if grep -qi "baseline" "$DRIFT_OUT" 2>/dev/null; then
    log "drift: no prior baseline — will store first baseline now"
    record "drift" "no-baseline"
  else
    log "drift: compare crashed"
    record "drift" "failed"
    FAILED+=("drift")
  fi
fi
if "$VENV_PY" "$CS_SCRIPTS/drift_baseline.py" "$TARGET_URL" --skip-cwv >"$OUT/drift-baseline.json" 2>>"$RUN_LOG"; then
  log "drift: baseline stored (~/.cache/claude-seo/drift/baselines.db)"
else
  log "drift: baseline store crashed"
  record "drift-baseline" "failed"
  FAILED+=("drift-baseline")
fi

# --- monthly (full sweep) additions -------------------------------------------
if [ "$SCOPE" = "monthly" ]; then
  # citability: AI-citation readiness scoring of content blocks
  run_analyzer citability "$VENV_PY" "$GEO_SCRIPTS/citability_scorer.py" "$TARGET_URL" || true

  # content-quality: QRG-aligned filler/AI-pattern/quality scoring of homepage
  if [ -s "$HOMEPAGE_HTML" ]; then
    run_analyzer content-quality "$VENV_PY" "$CS_SCRIPTS/content_quality.py" "$HOMEPAGE_HTML" --json --threshold 0 || true
  else
    record "content-quality" "failed"
    FAILED+=("content-quality")
  fi

  # sitemap: URL inventory reachable from the target's sitemap(s)
  run_analyzer sitemap "$VENV_PY" "$GEO_SCRIPTS/fetch_page.py" "$TARGET_URL" sitemap || true

  # brand: brand-mention presence on AI-cited platforms (public scrape; flaky
  # walls surface as a loud failure, never a silent pass)
  run_analyzer brand "$VENV_PY" "$GEO_SCRIPTS/brand_scanner.py" "$BRAND_NAME" "$BRAND_DOMAIN" || true
fi

# --- summary.json --------------------------------------------------------------
"$VENV_PY" - "$OUT/summary.json" "$TODAY" "$SCOPE" "$TARGET_URL" "${STATUSES[@]}" <<'PY' 2>>"$RUN_LOG"
import json, sys
out, today, scope, url, *pairs = sys.argv[1:]
statuses = {}
for p in pairs:
    k, _, v = p.partition("=")
    statuses[k] = v
doc = {
    "date": today,
    "scope": scope,
    "target_url": url,
    "analyzers": statuses,
    "failed": sorted([k for k, v in statuses.items() if v == "failed"]),
}
with open(out, "w") as f:
    json.dump(doc, f, indent=2)
print(json.dumps(doc["analyzers"]))
PY

# --- deterministic findings synthesis (NO LLM) ---------------------------------
if "$VENV_PY" "$FINDINGS_PY" "$OUT" --scope "$SCOPE" --url "$TARGET_URL" >"$OUT/findings.md" 2>>"$RUN_LOG" \
  && [ -s "$OUT/findings.md" ]; then
  log "findings written to $OUT/findings.md"
else
  log "fatal: findings synthesis failed"
  FAILED+=("findings")
fi

if [ "${#FAILED[@]}" -gt 0 ]; then
  log "=== done with FAILURES: ${FAILED[*]} (output in $OUT) ==="
  exit 1
fi
log "=== done — all analyzers ok (output in $OUT) ==="
exit 0
