import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import atomic_json, utcnow
from providers import DataForSEO, gsc_snapshot, successful
from orchestrator import ai_observation, opportunity, query_evidence, read_clusters, read_questions


class ResearchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.policy = {'dailyHardCapUsd': .3, 'dailyAutoApproveUsd': .3,
            'endpointEstimatesUsd': {'kw_data_google_ads_search_volume': .2, 'serp_organic_live_advanced': .05, 'serp_screenshot': .02},
            'rules': {'maxKeywordBatchSize': 1000}}
        atomic_json(self.root / 'policy.json', self.policy)
        self.config = {'policy_path': str(self.root / 'policy.json')}
        self.response = {'status_code': 20000, 'cost': .1, 'tasks': [{'status_code': 20000, 'result': []}]}
        self.task = {'keywords': ['toyota carroll']}

    def test_cache_is_free_and_budget_is_conservative(self):
        calls = []
        client = DataForSEO(self.root, self.config, lambda *a: calls.append(a) or self.response)
        client.call('volume', self.task)
        client.call('volume', self.task)
        self.assertEqual(len(calls), 1)
        with self.assertRaisesRegex(RuntimeError, 'BUDGET-CAP'):
            client.call('volume', {'keywords': ['chevy carroll']})

    def test_unknown_request_never_retried_or_refunded(self):
        def fail(*args):
            raise TimeoutError('not logged')
        client = DataForSEO(self.root, self.config, fail)
        with self.assertRaisesRegex(RuntimeError, 'reservation retained'):
            client.call('volume', self.task)
        self.policy['dailyHardCapUsd'] = self.policy['dailyAutoApproveUsd'] = 2
        atomic_json(self.root / 'policy.json', self.policy)
        client = DataForSEO(self.root, self.config, lambda *a: self.response)
        with self.assertRaisesRegex(RuntimeError, 'AMBIGUOUS'):
            client.call('volume', self.task)

    def test_unexpected_price_blocks_further_requests(self):
        response = {**self.response, 'cost': .25}
        client = DataForSEO(self.root, self.config, lambda *a: response)
        client.call('volume', self.task)
        with self.assertRaisesRegex(RuntimeError, 'BUDGET-BLOCKED'):
            client.call('serp', {'keyword': 'new query', 'depth': 10})

    def test_endpoint_operators_and_depth_fail_before_spend(self):
        client = DataForSEO(self.root, self.config, lambda *a: self.fail('network'))
        for kind, task in [('labs', {}), ('serp', {'depth': 100}), ('volume', {'keywords': ['site:foo']}), ('volume', {'keywords': []})]:
            with self.assertRaises(ValueError):
                client.call(kind, task)
        self.assertFalse((self.root / 'cost-ledger.json').exists())

    def test_provider_error_cached_but_never_success(self):
        response = {**self.response, 'tasks': [{'status_code': 40501}]}
        client = DataForSEO(self.root, self.config, lambda *a: response)
        entry = client.call('volume', self.task)
        with self.assertRaises(RuntimeError):
            successful(entry)
        self.assertEqual(client.call('volume', self.task), entry)

    def test_unpriced_options_rejected_before_any_spend(self):
        client = DataForSEO(self.root, self.config, lambda *a: self.fail('network'))
        for kind, task in [
            ('serp', {'keyword': 'service', 'depth': 10, 'premium_option': True}),
            ('serp', {'keyword': 'service', 'depth': 10, 'load_async_ai_overview': 'true'}),
            ('volume', {'keywords': ['service'], 'priority': 2}),
            ('screenshot', {'task_id': 'task-1', 'browser_screen_scale_factor': 50}),
            ('screenshot', {'task_id': 'task-1', 'browser_screen_scale_factor': float('nan')}),
        ]:
            with self.subTest(task=task), self.assertRaises(ValueError):
                client.call(kind, task)
        self.assertFalse((self.root / 'cost-ledger.json').exists())

    def test_unknown_cost_preserves_response_and_cannot_be_reused(self):
        response = {k: v for k, v in self.response.items() if k != 'cost'}
        client = DataForSEO(self.root, self.config, lambda *a: response)
        with self.assertRaisesRegex(RuntimeError, 'UNKNOWN-COST'):
            client.call('volume', self.task)
        diagnostics = list((self.root / 'cache').glob('uncertain-response-*.json'))
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(json.loads(diagnostics[0].read_text())['response'], response)
        self.assertEqual(list((self.root / 'cache').glob('dataforseo-*.json')), [])
        self.policy['dailyHardCapUsd'] = self.policy['dailyAutoApproveUsd'] = 2
        atomic_json(self.root / 'policy.json', self.policy)
        client = DataForSEO(self.root, self.config, lambda *a: self.fail('uncertain paid retry'))
        with self.assertRaisesRegex(RuntimeError, 'AMBIGUOUS'):
            client.call('volume', self.task)

    def test_source_runbooks_and_scoring(self):
        agents = Path(__file__).resolve().parents[2] / 'agents'
        self.assertEqual(len(read_clusters(agents / 'topical-map.md')), 7)
        self.assertEqual(len(read_questions(agents / 'ai-mentions.md')), 20)
        self.assertEqual(opportunity(650, 3, 1)['priority_score'], 16)
        self.assertEqual(opportunity(650, 12, 1)['priority_score'], 8)
        self.assertIsNone(opportunity(None, 3, 1)['priority_score'])
        self.assertEqual(opportunity(0, 3, 1)['priority_score'], 0)

    def test_query_demand_not_duplicated_and_conflicts_hold(self):
        candidate = {'gsc_property': 'site', 'query_terms': ['used trucks'], 'target_query': 'used trucks carroll'}
        data = {'properties': {'site': {'status': 'ok', 'start_date': 'a', 'end_date': 'b',
            'query_rows': [{'keys': ['used trucks carroll'], 'impressions': 100}],
            'page_rows': [{'keys': ['used trucks carroll', '/a'], 'impressions': 80}, {'keys': ['used trucks carroll', '/b'], 'impressions': 40}]}}}
        result = query_evidence(candidate, data)
        self.assertEqual(result['demand'], 100)
        self.assertEqual(result['status'], 'HOLD-CANNIBALIZATION')
        self.assertEqual(query_evidence(candidate, {'properties': {}})['status'], 'BLOCKED-GSC')

    def test_no_overview_is_not_a_citation_gap(self):
        result = ai_observation({'id': 'Q01'}, [{'type': 'organic'}], utcnow())
        self.assertEqual(result['status'], 'NO_OVERVIEW')
        self.assertIsNone(result['citation_gap'])
        result = ai_observation({'id': 'Q01'}, [{'type': 'ai_overview', 'references': [{'url': 'https://www.motorinnautogroup.com/'}]}], utcnow())
        self.assertFalse(result['citation_gap'])

    def test_gsc_cache_and_no_credentials_copy(self):
        calls = []
        config = {'credential_path': '/remote/private.json', 'properties': ['site']}
        result = gsc_snapshot(self.root, config, lambda r: calls.append(r) or {'properties': {'site': {'status': 'ok'}}})
        gsc_snapshot(self.root, config, lambda r: self.fail('cache miss'))
        self.assertEqual(len(calls), 1)
        self.assertEqual(result['request']['credential_path'], '/remote/private.json')


if __name__ == '__main__':
    unittest.main()
