#!/bin/bash
# Weekly queue production; launchd provides the schedule. No content producer launches.
set -uo pipefail
ROOT=/Users/spencerheywood/motor-inn-seo
PYTHON=/Library/Frameworks/Python.framework/Versions/3.13/bin/python3.13
export TZ=America/Chicago
cd "$ROOT" || exit 1
status=0
"$PYTHON" "$ROOT/automation/collect_inventory_evidence.py" || status=1
"$PYTHON" "$ROOT/automation/content_builder.py" || status=1
"$PYTHON" "$ROOT/automation/orchestrator.py" "$@" || status=1
# Research may discover own-host destinations; refresh pending jobs once after planning.
"$PYTHON" "$ROOT/automation/content_builder.py" || status=1
"$PYTHON" "$ROOT/automation/import_content_posts.py" --all-october || status=1
# Draft existing valid jobs even when fresh research/import reports a blocker.
"$PYTHON" "$ROOT/automation/page_generator.py" || status=1
exit "$status"
