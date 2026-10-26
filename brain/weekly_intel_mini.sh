#!/bin/bash
cd $HOME/motor-inn-seo
P=/usr/bin/python3
$P brain/gap_run.py >> pipeline/logs/weekly-intel.log 2>&1
$P brain/ai_visibility_run.py >> pipeline/logs/weekly-intel.log 2>&1
git add brain/gap brain/ai-visibility brain/LOG.md 2>/dev/null
git -c user.name="jeeves-mini" -c user.email="jeeves@mini.local" commit -m "weekly intel auto $(date +%F)" --quiet || true
echo "=== mini run $(date) ===" >> pipeline/logs/weekly-intel.log
