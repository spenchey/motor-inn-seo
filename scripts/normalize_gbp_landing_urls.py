#!/usr/bin/env python3
"""Normalize Motor Inn Google Business Profile landing URLs.

The SEO audits showed GBP links pointing at /Contactus/Carroll with UTM
parameters. This utility gives Rory's recurring SEO/GEO run a deterministic
way to flag and rewrite those links before handoff or live publishing.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from urllib.parse import urlparse, urlunparse


CONTACT_PATH = "/Contactus/Carroll"
SITE_ROOT = "https://www.motorinnautogroup.com"
DEFAULT_CANONICAL_URL = f"{SITE_ROOT}/used-inventory"
NEW_TOYOTA_URL = f"{SITE_ROOT}/new-toyota"


def canonical_gbp_url(raw_url: str, context: str = "") -> str:
    """Return a query-free canonical GBP landing URL."""
    if not raw_url:
        return raw_url

    parsed = urlparse(raw_url)
    path = parsed.path.rstrip("/")
    context_lc = f"{raw_url} {context}".lower()

    if path.lower() == CONTACT_PATH.lower():
        if "toyota" in context_lc or "new" in context_lc:
            return NEW_TOYOTA_URL
        return DEFAULT_CANONICAL_URL

    if parsed.query and "utm_" in parsed.query.lower():
        return urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", "", parsed.fragment))

    return raw_url


def collect_context(row: dict[str, object]) -> str:
    return " ".join(str(value) for value in row.values() if value is not None)


def normalize_json(path: Path) -> tuple[object, list[dict[str, str]]]:
    payload = json.loads(path.read_text())
    changes: list[dict[str, str]] = []

    def visit(node: object, parent_context: str = "") -> object:
        if isinstance(node, dict):
            context = f"{parent_context} {collect_context(node)}"
            return {key: visit_value(key, value, context) for key, value in node.items()}
        if isinstance(node, list):
            return [visit(item, parent_context) for item in node]
        return node

    def visit_value(key: str, value: object, context: str) -> object:
        if isinstance(value, str) and ("url" in key.lower() or value.startswith(("http://", "https://"))):
            normalized = canonical_gbp_url(value, context)
            if normalized != value:
                changes.append({"field": key, "before": value, "after": normalized})
            return normalized
        return visit(value, context)

    return visit(payload), changes


def normalize_csv(path: Path) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fieldnames = reader.fieldnames or []

    changes: list[dict[str, str]] = []
    for index, row in enumerate(rows, start=1):
        context = collect_context(row)
        for field in fieldnames:
            value = row.get(field, "")
            if "url" not in field.lower() and not value.startswith(("http://", "https://")):
                continue
            normalized = canonical_gbp_url(value, context)
            if normalized != value:
                row[field] = normalized
                changes.append({"row": str(index), "field": field, "before": value, "after": normalized})

    return rows, changes


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for field in row:
            if field not in fieldnames:
                fieldnames.append(field)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="CSV or JSON export containing GBP landing URLs")
    parser.add_argument("--output", type=Path, help="Write normalized output here")
    parser.add_argument("--check", action="store_true", help="Fail if any URL would change")
    args = parser.parse_args()

    if args.input.suffix.lower() == ".json":
        normalized, changes = normalize_json(args.input)
        serialized = json.dumps(normalized, indent=2, ensure_ascii=False) + "\n"
        if args.output and not args.check:
            args.output.write_text(serialized)
    elif args.input.suffix.lower() == ".csv":
        normalized, changes = normalize_csv(args.input)
        if args.output and not args.check:
            write_csv(args.output, normalized)
    else:
        raise SystemExit("Input must be .csv or .json")

    print(json.dumps({"input": str(args.input), "changes": changes, "changeCount": len(changes)}, indent=2))
    return 1 if args.check and changes else 0


if __name__ == "__main__":
    raise SystemExit(main())
