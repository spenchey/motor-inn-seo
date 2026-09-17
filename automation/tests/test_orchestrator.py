"""Driver admission checks: existing intents, GSC holds, weekly cap, source gaps."""
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import atomic_json, read_json, utcnow
from orchestrator import orchestrate
from test_end_to_end import ResearchFixture


class DriverTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / 'pipeline'
        self.candidate = {'slug': 'page-alpha', 'cluster': 'Service/tires', 'owner_host': 'www.fixture.invalid',
                          'target_url': 'https://www.fixture.invalid/page-alpha', 'target_query': 'service carroll',
                          'gsc_property': 'site', 'estimated_hours': 3, 'relevance': .5, 'outline': ['Services']}
        self.candidates = self.base / 'candidates.json'
        atomic_json(self.candidates, [self.candidate])
        self.config = {'runbook_directory': str(Path(__file__).resolve().parents[2] / 'agents'),
                       'candidate_path': str(self.candidates), 'verified_content_path': str(self.base / 'missing.json'),
                       'jobs_per_week': 1, 'dataforseo': ResearchFixture.config}
        self.snapshot = {'properties': {'site': {'status': 'ok', 'query_rows': [], 'page_rows': []}}}
        self.client = ResearchFixture(self.root)

    def run_driver(self):
        return orchestrate(self.root, self.config, client=self.client, snapshot=self.snapshot)

    def test_missing_content_is_explicit_pending_blocker(self):
        self.assertEqual(self.run_driver()['queued'], ['page-alpha'])
        job = read_json(self.root / 'queue/pending/page-alpha.json')
        self.assertTrue(job['blockers'])
        self.assertFalse(job['source_evidence'])
        self.assertEqual(job['gsc_check']['status'], 'checked')
        self.assertFalse(job['publication_authorized'])

    def test_existing_owner_holds_before_serp_spend(self):
        self.snapshot['properties']['site']['page_rows'] = [
            {'keys': ['service carroll', 'https://www.fixture.invalid/service'], 'impressions': 80}]
        result = self.run_driver()
        self.assertEqual(result['queued'], [])
        self.assertEqual(result['held'][0]['reason'], 'HOLD-EXISTING-OWNER')
        self.assertEqual(self.client.calls, ['volume'])

    def test_no_gsc_never_claims_clear_cannibalization(self):
        self.snapshot['properties'] = {}
        result = self.run_driver()
        self.assertEqual(result['queued'], [])
        self.assertEqual(result['held'][0]['reason'], 'BLOCKED-GSC')

    def test_legacy_job_counts_toward_weekly_limit(self):
        atomic_json(self.root / 'queue/ready/older-slug.json', {'slug': 'older-slug', 'created_at': utcnow()})
        self.assertEqual(self.run_driver()['queued'], [])
        self.assertEqual(self.client.calls, [])

    def test_same_query_hostname_alias_does_not_duplicate(self):
        atomic_json(self.root / 'queue/pending/older-slug.json', {'slug': 'older-slug',
                    'owner_host': 'fixture.invalid', 'target_query': 'service carroll'})
        self.assertEqual(self.run_driver()['queued'], [])
        self.assertEqual(self.client.calls, [])

    def test_unknown_cluster_rejected_before_provider_calls(self):
        self.candidate['cluster'] = 'Invented franchise'
        atomic_json(self.candidates, {'candidates': [self.candidate]})
        with self.assertRaisesRegex(ValueError, 'cluster absent'):
            self.run_driver()
        self.assertEqual(self.client.calls, [])

    def test_pending_research_refresh_does_not_consume_another_weekly_job(self):
        path = self.root / 'queue/pending/page-alpha.json'
        atomic_json(path, {**self.candidate, 'created_at': utcnow(), 'blockers': [
            'DATAFORSEO-TASK-FAILED:[40101]', 'VERIFIED-CONTENT-MISSING']})
        result = self.run_driver()
        self.assertEqual(result['queued'], [])
        self.assertEqual(result['refreshed'][0]['status'], 'refreshed')
        self.assertEqual(result['weekly_remaining'], 0)
        self.assertEqual(read_json(path)['blockers'], ['VERIFIED-CONTENT-MISSING'])

    def test_refresh_failure_keeps_old_research_and_fact_fields(self):
        path = self.root / 'queue/pending/page-alpha.json'
        atomic_json(path, {**self.candidate, 'created_at': utcnow(), 'search_evidence': {'old': 'retained'},
                          'sections': [{'preserved': 'source-builder'}]})
        def fail(*args):
            raise RuntimeError('DATAFORSEO-TASK-FAILED:[40101]')
        self.client.call = fail
        result = self.run_driver()
        self.assertEqual(result['refreshed'][0]['status'], 'blocked')
        job = read_json(path)
        self.assertEqual(job['search_evidence'], {'old': 'retained'})
        self.assertEqual(job['sections'], [{'preserved': 'source-builder'}])
        self.assertTrue(job['blockers'])


if __name__ == '__main__':
    unittest.main()
