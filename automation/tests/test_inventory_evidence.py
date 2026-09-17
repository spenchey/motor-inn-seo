"""Freshness, store isolation and privacy tests for aggregate-only feed evidence."""
from datetime import datetime, timedelta, timezone
import csv
import io
import json
from pathlib import Path
import tempfile
import unittest

from automation.collect_inventory_evidence import make_evidence, verified_mapping

NOW = datetime(2026, 9, 16, 15, tzinfo=timezone.utc)
KEY = 'raw/dealervault/year=2026/month=09/day=16/DVD56054_20260916_0808_INV.csv'
MAPPING = {'dealer_id': 'DVD56054', 'location': '9'}


def feed(count=40, location='9', duplicate=False):
    buf = io.StringIO()
    fields = ['DV Dealer ID', 'Vendor Dealer ID', 'Location', 'Vehicle Status', 'Vehicle Type', 'VIN', 'Make', 'Model', 'Vehicle Style', 'Cost', 'Internet Price']
    writer = csv.DictWriter(buf, fieldnames=fields, delimiter='\t')
    writer.writeheader()
    for n in range(count):
        writer.writerow({'DV Dealer ID': 'DVD56054', 'Vendor Dealer ID': 'DVD56054', 'Location': location, 'Vehicle Status': 'A', 'Vehicle Type': 'N', 'VIN': f'1AB2345678{0 if duplicate else n:07}', 'Make': 'TOYOTA', 'Model': 'TUNDRA', 'Vehicle Style': 'PICKUP', 'Cost': 'SECRET-COST', 'Internet Price': 'PRIVATE-PRICE'})
    return buf.getvalue().encode()


class InventoryEvidenceTests(unittest.TestCase):
    def test_timestamped_counts_without_private_fields(self):
        result = make_evidence(feed(), KEY, NOW - timedelta(hours=1), MAPPING, NOW)
        self.assertEqual(result['aggregates']['by_make'], {'TOYOTA': 40})
        self.assertEqual(result['feed']['row_count'], 40)
        self.assertEqual(result['source_evidence'][0]['valid_until'], '2026-09-18T14:00:00+00:00')
        serialized = json.dumps(result)
        for secret in ['SECRET-COST', 'PRIVATE-PRICE', '1AB23456780000000', 'VIN', 'Internet Price']:
            self.assertNotIn(secret, serialized)
        self.assertIn('September 16, 2026 at 14:00 UTC', result['facts'][0]['text'])
        self.assertFalse(result['publication_authorized'])

    def test_stale_source_is_not_revalidated_by_retrieval(self):
        with self.assertRaisesRegex(ValueError, 'older than 48 hours'):
            make_evidence(feed(), KEY, NOW - timedelta(hours=49), MAPPING, NOW)

    def test_future_source_refused(self):
        with self.assertRaisesRegex(ValueError, 'future-dated'):
            make_evidence(feed(), KEY, NOW + timedelta(seconds=1), MAPPING, NOW)

    def test_unknown_store_refused(self):
        with self.assertRaisesRegex(ValueError, 'unknown inventory store'):
            make_evidence(feed(location='8'), KEY, NOW, MAPPING, NOW)

    def test_short_feed_refused(self):
        with self.assertRaisesRegex(ValueError, '40-row'):
            make_evidence(feed(count=39), KEY, NOW, MAPPING, NOW)

    def test_duplicate_identity_refused(self):
        with self.assertRaisesRegex(ValueError, 'duplicate or invalid VIN'):
            make_evidence(feed(duplicate=True), KEY, NOW, MAPPING, NOW)

    def test_unknown_rooftop_filename_refused(self):
        with self.assertRaisesRegex(ValueError, 'Unexpected inventory source key'):
            make_evidence(feed(), KEY.replace('DVD56054', 'DVD99999'), NOW, MAPPING, NOW)

    def test_mapping_evidence_required_without_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'mapping.py'
            path.write_text('"""Carroll Store 9"""\nEXPECTED_SOURCE_DEALER="DVD56054"\nEXPECTED_STORE="9"\nraise RuntimeError("must not execute")\n')
            self.assertEqual(verified_mapping(path)['location'], '9')
            path.write_text('EXPECTED_SOURCE_DEALER="DVD56054"\nEXPECTED_STORE="8"\n')
            with self.assertRaisesRegex(ValueError, 'Unrecognized'):
                verified_mapping(path)


if __name__ == '__main__':
    unittest.main()
