"""Content adapter contract tests: provenance, tamper, freshness and replay boundaries."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from automation.common import draft_digest
from automation.import_content_posts import import_manifest, inspect_manifest

NOW = datetime(2026, 9, 16, tzinfo=timezone.utc)


class ContentImportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.upstream = self.base / 'upstream'
        self.upstream.mkdir()
        self.pipeline = self.base / 'pipeline'
        self.content = '# Actual source draft\n\nApproved source statement. <script>test</script>\n'
        self.source = {'source_id': 'S1', 'url': 'https://example.org/source', 'status': 'verified', 'title': 'Source', 'claims_supported': ['Approved source statement.'], 'accessed_date': '2026-09-15', 'expires_at_utc': '2026-10-01T00:00:00Z'}
        self.write_manifest()

    def bound_file(self, path, text, role):
        file = self.upstream / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(text)
        return {'path': path, 'role': role, 'sha256': hashlib.sha256(text.encode()).hexdigest()}

    def write_manifest(self):
        source_file = self.bound_file('sources.json', json.dumps({'items': [self.source]}), 'source_registry')
        draft_file = self.bound_file('pieces/P1/draft.md', self.content, 'draft')
        self.manifest = {'package_id': 'OCT26-W40', 'iso_week': 'W40', 'authorship': {'author': 'Rory', 'source_sha256': 'original-author-hash'}, 'pieces': [{'piece_id': 'OCT26-W40-P1', 'kind': 'post', 'title': 'Actual post', 'channel_adaptations': ['facebook'], 'source_ids': ['S1'], 'files': [draft_file]}], 'package_files': [source_file]}
        self.path = self.upstream / 'manifest.json'
        self.path.write_text(json.dumps(self.manifest))

    def test_one_queue_immutable_copy_and_replay(self):
        original = self.path.read_bytes()
        result = import_manifest(self.path, self.pipeline, NOW)
        self.assertEqual(result[0]['status'], 'drafts')
        slug = result[0]['slug']
        meta = json.loads((self.pipeline / 'drafts' / slug / 'meta.json').read_text())
        self.assertEqual(meta['content_files'][0]['text'], self.content)
        self.assertEqual(meta['upstream_manifest'], self.manifest)
        wrapper = (self.pipeline / 'drafts' / slug / 'index.html').read_text()
        self.assertIn('&lt;script&gt;', wrapper)
        self.assertNotIn('<script>', wrapper)
        job = json.loads((self.pipeline / 'queue/drafts' / (slug + '.json')).read_text())
        self.assertEqual(job['draft_digest'], draft_digest(self.pipeline / 'drafts' / slug))
        self.assertFalse(job['publish_authorized'])
        self.assertFalse((self.pipeline / 'queue/pending' / (slug + '.json')).exists())
        self.assertEqual(import_manifest(self.path, self.pipeline, NOW)[0]['status'], 'already_imported')
        self.assertEqual(self.path.read_bytes(), original)
        self.assertFalse((self.pipeline / 'queue/approved').exists())

    def test_interrupted_pending_import_resumes(self):
        record = inspect_manifest(self.path, NOW)[0]
        pending = self.pipeline / 'queue/pending' / (record['slug'] + '.json')
        pending.parent.mkdir(parents=True)
        pending.write_text(json.dumps(dict(record, status='pending')))
        result = import_manifest(self.path, self.pipeline, NOW)
        self.assertEqual(result[0]['status'], 'drafts')
        self.assertFalse(pending.exists())

    def test_source_edit_invalidates_manifest(self):
        (self.upstream / 'pieces/P1/draft.md').write_text('tampered')
        with self.assertRaisesRegex(ValueError, 'SHA-256 mismatch'):
            import_manifest(self.path, self.pipeline, NOW)
        self.assertFalse((self.pipeline / 'queue').exists())

    def test_expired_source_stays_pending(self):
        self.source['expires_at_utc'] = '2026-09-01T00:00:00Z'
        self.write_manifest()
        result = import_manifest(self.path, self.pipeline, NOW)
        self.assertEqual(result[0]['status'], 'pending')
        self.assertIn('Expired source: S1', result[0]['errors'])
        self.assertFalse((self.pipeline / 'drafts').exists())

    def test_partial_source_stays_pending(self):
        self.source['status'] = 'partial'
        self.write_manifest()
        self.assertEqual(import_manifest(self.path, self.pipeline, NOW)[0]['status'], 'pending')

    def test_changed_copy_creates_new_review_version(self):
        first = import_manifest(self.path, self.pipeline, NOW)[0]['slug']
        self.content += '\nRevised copy.\n'
        self.write_manifest()
        second = import_manifest(self.path, self.pipeline, NOW)[0]['slug']
        self.assertNotEqual(first, second)
        self.assertEqual(len(list((self.pipeline / 'queue/drafts').glob('*.json'))), 2)

    def test_path_traversal_rejected(self):
        self.manifest['pieces'][0]['files'][0]['path'] = '../outside.md'
        self.path.write_text(json.dumps(self.manifest))
        with self.assertRaisesRegex(ValueError, 'Unsafe upstream path'):
            inspect_manifest(self.path, NOW)

    def test_source_cannot_escape_through_symlink(self):
        content_path = self.upstream / 'pieces/P1/draft.md'
        outside = self.base / 'outside.md'
        outside.write_text(self.content)
        content_path.unlink()
        content_path.symlink_to(outside)
        with self.assertRaisesRegex(ValueError, 'Unsafe upstream path'):
            inspect_manifest(self.path, NOW)

    def test_video_is_not_misrepresented_as_post(self):
        self.manifest['pieces'][0]['kind'] = 'video'
        self.path.write_text(json.dumps(self.manifest))
        self.assertEqual(inspect_manifest(self.path, NOW), [])


if __name__ == '__main__':
    unittest.main()
