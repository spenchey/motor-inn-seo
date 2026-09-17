#!/bin/sh
# Refresh sources and drafts, then reconcile approvals even when individual stages block.
set -eu
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PYTHON=${MOTORINN_PYTHON:-/Library/Frameworks/Python.framework/Versions/3.13/bin/python3.13}
PIPELINE_ROOT="$SCRIPT_DIR/../pipeline"
CONFIG="$SCRIPT_DIR/config.json"
while [ "$#" -gt 0 ]; do
  case "$1" in
    --root)
      [ "$#" -ge 2 ] || { echo 'Missing --root path' >&2; exit 2; }
      PIPELINE_ROOT=$2
      shift 2
      ;;
    --config)
      [ "$#" -ge 2 ] || { echo 'Missing --config path' >&2; exit 2; }
      CONFIG=$2
      shift 2
      ;;
    *) echo "Unsupported approval-sync argument: $1" >&2; exit 2 ;;
  esac
done
STATUS=0
"$PYTHON" "$SCRIPT_DIR/collect_inventory_evidence.py" --output "$PIPELINE_ROOT/inputs/inventory-evidence.json" || STATUS=$?
"$PYTHON" "$SCRIPT_DIR/content_builder.py" --root "$PIPELINE_ROOT" --config "$CONFIG" || STATUS=$?
"$PYTHON" "$SCRIPT_DIR/page_generator.py" --root "$PIPELINE_ROOT" || STATUS=$?
"$PYTHON" "$SCRIPT_DIR/approval_sync.py" --root "$PIPELINE_ROOT" --config "$CONFIG" || STATUS=$?
exit "$STATUS"
