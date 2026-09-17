"""One isolated test-page-alpha journey; temporary artifacts are deleted after QA."""
import hashlib
import hmac
import json
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import atomic_json, read_json
from orchestrator import orchestrate
from page_generator import generate, validate_draft
from approval_sync import record_event, sync
from publish_handler import publish
from test_page_generator import fixture_job


class ResearchFixture:
    config = {'location_name': 'Iowa,UnitedStates', 'language_code': 'en'}

    def __init__(self, root):
        self.root = root
        self.calls = []

    def call(self, kind, task):
        self.calls.append(kind)
        if kind == 'volume':
            result = [{'keyword': q, 'search_volume': 50} for q in task['keywords']]
        elif kind == 'serp':
            result = [{'items': [{'type': 'organic', 'url': 'https://competitor.invalid/', 'title': 'Fixture result'}]}]
        else:
            result = [{'items': [{'image': 'https://api.dataforseo.com/fixture'}]}]
        return {'cache_key': 'fixture-' + kind, 'response': {'status_code': 20000, 'tasks': [
            {'id': 'fixture-task', 'status_code': 20000, 'result': result}]}}

    def save_screenshot(self, entry):
        path = self.root / 'cache' / 'fixture-screenshot.png'
        path.write_bytes(b'fixture only')
        return path


class EndToEndTests(unittest.TestCase):
    def test_one_sample_from_research_to_packet_then_remove(self):
        with tempfile.TemporaryDirectory(prefix='motorinn-e2e-') as temporary:
            base = Path(temporary)
            root = base / 'pipeline'
            job = fixture_job()
            # Synthetic sources stay inside TemporaryDirectory; no fixture enters the real pipeline.
            job.pop('fixture_only')
            job.update(cluster='Service/tires', gsc_property='fixture-property', estimated_hours=3, relevance=.5,
                       ai_question_ids=['Q07'], topology_status='verified')
            candidates = base / 'candidates.json'
            content = base / 'content.json'
            atomic_json(candidates, {'candidates': [job]})
            atomic_json(content, {job['slug']: job})
            keys = []
            for name in ('slack', 'receipt'):
                path = base / (name + '.key')
                path.write_bytes(b'isolated-synthetic-test-key-12345678')
                path.chmod(0o600)
                keys.append(path)
            config = {'runbook_directory': str(Path(__file__).resolve().parents[2] / 'agents'),
                      'candidate_path': str(candidates), 'verified_content_path': str(content), 'jobs_per_week': 1,
                      'dataforseo': ResearchFixture.config,
                      'approval': {'spencer_slack_user_id': 'U_TEST', 'slack_channel_id': 'C_TEST',
                                   'slack_signing_secret_path': str(keys[0]), 'receipt_key_path': str(keys[1])}}
            snapshot = {'properties': {'fixture-property': {'status': 'ok', 'query_rows': [], 'page_rows': []}}}
            client = ResearchFixture(root)
            queued = orchestrate(root, config, client=client, snapshot=snapshot)
            self.assertEqual(queued['errors'], [])
            self.assertEqual(queued['queued'], ['test-page-alpha'])
            self.assertEqual(generate(root)['generated'], 1)
            directory = root / 'drafts' / 'test-page-alpha'
            self.assertTrue(validate_draft(directory)['passed'])
            self.assertEqual(sync(root, config)['errors'], [])
            marker = read_json(root / 'queue/drafts/test-page-alpha.json')
            command = 'APPROVE test-page-alpha ' + marker['draft_digest']
            self.assertIn(command, (root / 'APPROVALS-TODAY.md').read_text())
            body = json.dumps({'type': 'event_callback', 'event_id': 'E_TEST_ALPHA', 'event': {
                'type': 'message', 'user': 'U_TEST', 'channel': 'C_TEST', 'ts': '123.456', 'text': command}}).encode()
            timestamp = str(int(time.time()))
            signature = 'v0=' + hmac.new(keys[0].read_bytes(), b'v0:' + timestamp.encode() + b':' + body, hashlib.sha256).hexdigest()
            record_event(root, config, body, timestamp, signature)
            self.assertEqual(sync(root, config)['approved'], ['test-page-alpha'])
            # No subprocess is permitted on the DealerOn path.
            with patch('publish_handler.run', side_effect=AssertionError('unexpected git/gh')):
                result = publish(root, config)
            self.assertEqual(result['errors'], [])
            packet = root / 'ready-for-dealeron/test-page-alpha'
            final = (packet / 'index.html').read_text()
            self.assertNotIn('content="noindex, nofollow"', final)
            self.assertNotIn('Research draft —', final)
            self.assertTrue(validate_draft(directory)['passed'], 'Approved source draft stays unchanged')
            self.assertEqual(len(list((root / 'email-drafts').glob('*.md'))), 1)
            self.assertEqual(publish(root, config)['dealeron'], [])
            self.assertEqual(orchestrate(root, config, client=client, snapshot=snapshot)['queued'], [])
            self.assertEqual(client.calls, ['volume', 'serp', 'screenshot', 'serp'])
            self.assertTrue((root / 'queue/ready/test-page-alpha.json').exists())
        self.assertFalse(base.exists(), 'Test page, secrets, queue states and packets must all be removed')


if __name__ == '__main__':
    unittest.main()
