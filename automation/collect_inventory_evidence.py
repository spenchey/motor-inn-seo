#!/usr/bin/env python3
"""Collect fresh Carroll inventory aggregates from the existing DealerVault S3 feed.

Read-only S3; no new credentials, Athena jobs, raw-file copies, or VIN/price output.
Uses the already-installed DealerVault boto3 client only for authenticated S3 reads.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter
import csv
from datetime import datetime, timedelta, timezone
import hashlib
import io
import json
from pathlib import Path
import re
import sys

try:
    from .common import atomic_json, utcnow
except ImportError:
    from common import atomic_json, utcnow

REPO = Path(__file__).resolve().parents[1]
RUNTIME = Path('/Users/spencerheywood/Library/Application Support/MotorInn/DealerVault/runtime')
MAPPING_PATH = RUNTIME / 'scripts/check_motorinn_fresh_inventory_source_freshness.py'
BUCKET = 'motorinn-dealervault-raw'
REGION = 'us-east-2'
SOURCE_ID = 'dealervault-inventory-snapshot'
MAX_AGE_HOURS = 48


def verified_mapping(path: Path = MAPPING_PATH) -> dict:
    """Read existing runtime mapping constants without executing its code."""
    raw = path.read_bytes()
    tree = ast.parse(raw.decode())
    values = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    values[target.id] = node.value.value
    if (values.get('EXPECTED_SOURCE_DEALER'), values.get('EXPECTED_STORE')) != ('DVD56054', '9'):
        raise ValueError('Unrecognized DealerVault rooftop/store mapping')
    if 'Carroll Store 9' not in (ast.get_docstring(tree) or ''):
        raise ValueError('Missing explicit Carroll mapping evidence')
    return {'path': str(path), 'sha256': hashlib.sha256(raw).hexdigest(), 'dealer_id': 'DVD56054', 'location': '9', 'store_name': 'Motor Inn of Carroll', 'mapping_basis': 'Existing runtime identifies DVD56054 / location 9 as Carroll Store 9'}


def make_evidence(raw: bytes, key: str, modified: datetime, mapping: dict, now: datetime | None = None) -> dict:
    now = now or datetime.now(timezone.utc)
    age = now - modified
    if age < timedelta(0) or age > timedelta(hours=MAX_AGE_HOURS):
        raise ValueError('Inventory source timestamp is future-dated or older than 48 hours')
    match = re.fullmatch(r'raw/dealervault/year=(\d{4})/month=(\d{2})/day=(\d{2})/DVD56054_(\d{8})_\d{4}_INV\.csv', key)
    if not match:
        raise ValueError('Unexpected inventory source key')
    feed_date = datetime.strptime(match[4], '%Y%m%d').date()
    if feed_date != datetime(int(match[1]), int(match[2]), int(match[3])).date() or not 0 <= (now.date() - feed_date).days <= 3:
        raise ValueError('Inventory feed date is stale or inconsistent with partition')
    if mapping.get('dealer_id') != 'DVD56054' or mapping.get('location') != '9':
        raise ValueError('Unrecognized mapping')
    reader = csv.DictReader(io.StringIO(raw.decode('utf-8-sig')), delimiter='\t')
    required = {'DV Dealer ID', 'Vendor Dealer ID', 'Location', 'Vehicle Status', 'Vehicle Type', 'VIN', 'Make', 'Model', 'Vehicle Style'}
    if not required.issubset(reader.fieldnames or []):
        raise ValueError('Inventory feed missing required columns')
    rows = list(reader)
    if len(rows) < 40:
        raise ValueError('Inventory feed below 40-row completeness floor')
    vins, makes, types, groups = set(), Counter(), Counter(), Counter()
    for row in rows:
        if any(row.get(field, '').strip() != expected for field, expected in [('DV Dealer ID', 'DVD56054'), ('Vendor Dealer ID', 'DVD56054'), ('Location', '9')]):
            raise ValueError('Mixed or unknown inventory store mapping')
        vin = row.get('VIN', '').strip().upper()
        if not re.fullmatch(r'[A-HJ-NPR-Z0-9]{17}', vin) or vin in vins:
            raise ValueError('Inventory has duplicate or invalid VIN identity')
        vins.add(vin)
        if row.get('Vehicle Status', '').strip() != 'A':
            raise ValueError('Unsupported inventory status; manual source-owner review required')
        make = row.get('Make', '').strip().upper()
        vehicle_type = row.get('Vehicle Type', '').strip()
        if not re.fullmatch(r'[A-Z][A-Z0-9 &-]{0,40}', make) or vehicle_type not in {'N', 'U'}:
            raise ValueError('Unsupported make/type in inventory source')
        makes[make] += 1
        types[vehicle_type] += 1
        model, style = row['Model'].strip().upper(), row['Vehicle Style'].strip().upper()
        if not model or not style or any(not re.fullmatch(r'[A-Z0-9 /&.-]{1,80}', value) for value in (model, style)):
            raise ValueError('Unsupported model/style in inventory source')
        groups[(vehicle_type, make, model, style)] += 1
    stamp = modified.astimezone(timezone.utc).isoformat()
    observation = modified.astimezone(timezone.utc).strftime('%B %d, %Y at %H:%M UTC')
    claims = [f'The Motor Inn of Carroll DealerVault inventory snapshot received on {observation} listed {len(rows)} vehicles.']
    claims.extend(f'The same {observation} inventory snapshot listed {count} {make.title()} vehicles.' for make, count in sorted(makes.items()))
    claims.append('This is a dated inventory snapshot; vehicle availability may have changed since it was received.')
    source = {'id': SOURCE_ID, 'source_type': 'DealerVault', 'sourceType': 'DealerVault', 'verified': True,
              'url': f'https://{BUCKET}.s3.{REGION}.amazonaws.com/{key}', 's3_uri': f's3://{BUCKET}/{key}',
              'retrieved_at': now.isoformat(), 'modified_at': stamp, 'valid_until': (modified + timedelta(hours=MAX_AGE_HOURS)).isoformat(),
              'sha256': hashlib.sha256(raw).hexdigest(), 'claims': claims,
              'note': 'Private raw source; only aggregate approved facts are exported. No live availability guarantee.'}
    return {'schema_version': 1, 'status': 'verified', 'retrieved_at': now.isoformat(),
            'feed': {**source, 'dealer_id': 'DVD56054', 'location': '9', 'row_count': len(rows)},
            'mapping_evidence': mapping, 'source_evidence': [source],
            'facts': [{'text': claim, 'evidence_ids': [SOURCE_ID]} for claim in claims],
            'aggregates': {'by_make': dict(sorted(makes.items())), 'by_type_code': dict(sorted(types.items())), 'groups': [{'type_code': key[0], 'make': key[1], 'model': key[2], 'style': key[3], 'count': count} for key, count in sorted(groups.items())]},
            'publication_authorized': False}


def collect(client, mapping: dict, now: datetime | None = None) -> dict:
    now = now or datetime.now(timezone.utc)
    for back in range(4):
        day = now.date() - timedelta(days=back)
        prefix = f'raw/dealervault/year={day.year}/month={day.month:02d}/day={day.day:02d}/'
        candidates = []
        for page in client.get_paginator('list_objects_v2').paginate(Bucket=BUCKET, Prefix=prefix):
            candidates.extend(obj for obj in page.get('Contents', []) if re.search(r'/DVD56054_\d{8}_\d{4}_INV\.csv$', obj['Key']))
        if candidates:
            latest = max(candidates, key=lambda obj: (obj['LastModified'], obj['Key']))
            response = client.get_object(Bucket=BUCKET, Key=latest['Key'])
            raw = response['Body'].read(8 * 1024 * 1024 + 1)
            if len(raw) > 8 * 1024 * 1024:
                raise ValueError('Inventory object exceeds bounded 8 MiB read')
            return make_evidence(raw, latest['Key'], response['LastModified'], mapping, now)
    raise ValueError('No mapped DealerVault inventory feed in the last three days')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=REPO / 'pipeline/inputs/inventory-evidence.json')
    args = parser.parse_args()
    try:
        mapping = verified_mapping()
        sys.path.insert(0, str(RUNTIME / '.deps/dealervault'))
        import boto3
        from botocore.config import Config
        client = boto3.client('s3', region_name=REGION, config=Config(connect_timeout=8, read_timeout=20, retries={'max_attempts': 2}))
        result = collect(client, mapping)
        atomic_json(args.output, result)
        print(json.dumps({'status': 'verified', 'output': str(args.output), 'row_count': result['feed']['row_count'], 'source_sha256': result['feed']['sha256']}))
        return 0
    except Exception as exc:
        # Replace an old success with an explicit failed read, preventing stale-success reuse.
        failure = {'status': 'blocked', 'retrieved_at': utcnow(), 'source_evidence': [], 'facts': [], 'error_type': type(exc).__name__, 'error': str(exc)[:500], 'publication_authorized': False}
        atomic_json(args.output, failure)
        print(json.dumps(failure))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
