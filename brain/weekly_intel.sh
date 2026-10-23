#!/bin/bash
cd /Users/spencerheywood/motor-inn-seo
P=/Users/spencerheywood/motor-inn-seo/.venv/bin/python
$P brain/gap_run.py >> pipeline/logs/weekly-intel.log 2>&1
$P brain/ai_visibility_run.py >> pipeline/logs/weekly-intel.log 2>&1
git add brain/gap brain/ai-visibility brain/LOG.md 2>/dev/null
git commit -m "weekly intel auto $(date +%F)" --quiet || true
echo "=== run $(date) ===" >> pipeline/logs/weekly-intel.log
