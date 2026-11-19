#!/usr/bin/env python3
"""Build the monthly baseline file (baselines/<yyyy-mm>.json).

Reads the pulled input files (gsc.json, ga4.json, gbp.json, leads.json,
ai_answers.json) from --inputs and writes one dated file. Makes no network
calls. Stdlib only, Python 3.9.
"""
from __future__ import annotations

import argparse
import datetime
import json
import math
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(HERE, "baseline.schema.json")

MONTH_RE = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")
WINDOW_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})\.\.(\d{4}-\d{2}-\d{2})$")
PULLED_RE = re.compile(
    r"^(\d{4}-\d{2}-\d{2})T([01]\d|2[0-3]):[0-5]\d(:[0-5]\d(\.\d{1,6})?)?"
    r"(Z|[+-]([01]\d|2[0-3]):?[0-5]\d)?$"
)
ALL_KEY = "all"  # entity key for top-level metrics in the input files


class BaselineError(Exception):
    """A refusal. The message names what is wrong. Nothing is written."""


def load_schema(path=SCHEMA_PATH):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            schema = json.load(fh)
    except (OSError, ValueError) as exc:
        raise BaselineError("cannot read schema %s: %s" % (path, exc))
    required = (
        "not_verified", "metric_fields", "sites", "listings",
        "site_metrics", "listing_metrics", "top_level_metrics", "input_files",
    )
    missing = [key for key in required if key not in schema]
    if missing:
        raise BaselineError("schema is missing: " + ", ".join(missing))
    return schema


def metric_file_map(schema):
    """Map each metric name to the one input file that carries it."""
    wanted = (
        list(schema["site_metrics"])
        + list(schema["listing_metrics"])
        + list(schema["top_level_metrics"])
    )
    mapping = {}
    for fname, metrics in schema["input_files"].items():
        for metric in metrics:
            if metric in mapping:
                raise BaselineError("schema maps %s to two input files" % metric)
            mapping[metric] = fname
    unmapped = [metric for metric in wanted if metric not in mapping]
    if unmapped:
        raise BaselineError("schema has no input file for: " + ", ".join(unmapped))
    return mapping


def _is_valid_window(text):
    match = WINDOW_RE.match(text)
    if not match:
        return False
    try:
        start = datetime.datetime.strptime(match.group(1), "%Y-%m-%d")
        end = datetime.datetime.strptime(match.group(2), "%Y-%m-%d")
    except ValueError:
        return False
    return start <= end


def _is_valid_pulled_at(text):
    match = PULLED_RE.match(text)
    if not match:
        return False
    try:
        datetime.datetime.strptime(match.group(1), "%Y-%m-%d")
    except ValueError:
        return False
    return True


def normalise_metric(obj, label, schema):
    """Return the metric as written to the baseline, or the not-verified text.

    Refuses (BaselineError) any metric object that lacks a field or has a
    bad value, window or timestamp. Never turns a missing value into zero.
    """
    not_verified = schema["not_verified"]
    if isinstance(obj, str) and obj == not_verified:
        return not_verified
    if not isinstance(obj, dict):
        raise BaselineError(
            '%s: must be a metric object or the text "%s"' % (label, not_verified)
        )
    fields = schema["metric_fields"]
    for field in fields:
        if field not in obj:
            raise BaselineError("%s: missing %s" % (label, field))
        if obj[field] is None:
            raise BaselineError("%s: %s is null" % (label, field))

    value = obj["value"]
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        raise BaselineError("%s: value must be a number or text" % label)
    if isinstance(value, float) and not math.isfinite(value):
        raise BaselineError("%s: value is not a finite number" % label)
    if isinstance(value, str) and not value.strip():
        raise BaselineError("%s: value is empty" % label)

    window = obj["window"]
    if not isinstance(window, str) or not _is_valid_window(window):
        raise BaselineError(
            "%s: window must look like YYYY-MM-DD..YYYY-MM-DD (got %r)" % (label, window)
        )
    source = obj["source"]
    if not isinstance(source, str) or not source.strip():
        raise BaselineError("%s: source is empty" % label)
    pulled_at = obj["pulled_at"]
    if not isinstance(pulled_at, str) or not _is_valid_pulled_at(pulled_at):
        raise BaselineError("%s: pulled_at must be ISO-8601 (got %r)" % (label, pulled_at))

    if isinstance(value, str) and value == not_verified:
        return not_verified
    return {field: obj[field] for field in fields}


def _read_input(path, fname):
    """Return the parsed input file, or None when the file is absent."""
    if not os.path.isfile(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except OSError as exc:
        raise BaselineError("%s: cannot read (%s)" % (fname, exc))
    except ValueError as exc:
        raise BaselineError("%s: not valid JSON (%s)" % (fname, exc))
    if not isinstance(data, dict):
        raise BaselineError("%s: top level must be a JSON object" % fname)
    return data


def build_payload(month, inputs_dir, schema=None):
    """Assemble the baseline dict. Returns (payload, counts)."""
    if schema is None:
        schema = load_schema()
    if not isinstance(month, str) or not MONTH_RE.match(month):
        raise BaselineError("--month must look like YYYY-MM (got %r)" % (month,))

    mapping = metric_file_map(schema)
    docs = {}
    for fname in schema["input_files"]:
        docs[fname] = _read_input(os.path.join(inputs_dir, fname), fname)

    counts = {"total": 0, "not_verified": 0}
    not_verified = schema["not_verified"]

    def resolve(metric, entity):
        counts["total"] += 1
        fname = mapping[metric]
        label = "%s / %s / %s" % (fname, entity, metric)
        result = not_verified
        doc = docs[fname]
        if doc is not None:
            node = doc.get(entity)
            if node is not None:
                if not isinstance(node, dict):
                    raise BaselineError("%s: %s must be an object" % (fname, entity))
                if metric in node:
                    result = normalise_metric(node[metric], label, schema)
        if result == not_verified:
            counts["not_verified"] += 1
        return result

    sites = {
        site: {metric: resolve(metric, site) for metric in schema["site_metrics"]}
        for site in schema["sites"]
    }
    listings = {
        listing: {metric: resolve(metric, listing) for metric in schema["listing_metrics"]}
        for listing in schema["listings"]
    }
    payload = {"month": month, "sites": sites, "listings": listings}
    for metric in schema["top_level_metrics"]:
        payload[metric] = resolve(metric, ALL_KEY)
    return payload, counts


def write_atomic(path, payload):
    """Write JSON to a temp file in the same folder, then os.replace it."""
    out_dir = os.path.dirname(os.path.abspath(path))
    os.makedirs(out_dir, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(prefix=".baseline-", suffix=".tmp", dir=out_dir)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp_path, path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Build baselines/<yyyy-mm>.json from pulled input files. No network calls."
    )
    parser.add_argument("--month", required=True, help="month to build, YYYY-MM")
    parser.add_argument(
        "--inputs", required=True,
        help="folder holding gsc.json, ga4.json, gbp.json, leads.json, ai_answers.json",
    )
    parser.add_argument("--out", required=True, help="output file, e.g. baselines/2026-11.json")
    args = parser.parse_args(argv)

    if not os.path.isdir(args.inputs):
        sys.stderr.write("warning: inputs folder not found: %s\n" % args.inputs)
    try:
        payload, counts = build_payload(args.month, args.inputs)
        write_atomic(args.out, payload)
    except BaselineError as exc:
        sys.stderr.write("refused: %s\n" % exc)
        return 1
    except OSError as exc:
        sys.stderr.write("write failed: %s\n" % exc)
        return 1
    print(
        "wrote %s: %d of %d metrics not verified"
        % (args.out, counts["not_verified"], counts["total"])
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
