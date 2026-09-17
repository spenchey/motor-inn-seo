"""Offline safety and state-machine checks: no Slack sends, remote pushes or PRs."""
import hashlib
import hmac
import json
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch

from automation import approval_sync as approvals
from automation import publish_handler as publisher
from automation.common import atomic_json, read_json, draft_digest, utcnow


class ApprovalPublishTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "pipeline"
        self.receipt_key = self.base / "receipt.key"
        self.slack_key = self.base / "slack.key"
        for key in (self.receipt_key, self.slack_key):
            key.write_bytes(b"test-only-secret-not-a-live-credential-12345")
            key.chmod(0o600)
        self.config = {"approval": {"spencer_slack_user_id": "U_SPENCER", "slack_channel_id": "C_APPROVALS",
                        "receipt_key_path": str(self.receipt_key), "slack_signing_secret_path": str(self.slack_key)}}
        self.event_counter = 0
        self.slug = "test-page-alpha"
        self.directory = self.root / "drafts" / self.slug
        self.directory.mkdir(parents=True)
        self.meta = {"slug": self.slug, "title": "Test Page With Verified Evidence", "kind": "seo_page",
                     "target_platform": "dealeron", "site_url": "https://www.example.test/",
                     "source_evidence": [{"id": "source-1", "source_type": "GSC", "verified": True,
                                          "retrieved_at": utcnow(), "url": "https://example.test/"}]}
        (self.directory / "index.html").write_text("<!doctype html><title>Test</title><p>Review only.</p>")
        (self.directory / "evidence.md").write_text("Verified test source; offline fixture.\n")
        atomic_json(self.directory / "meta.json", self.meta)
        atomic_json(self.directory / "qa-report.json", {"passed": True})
        self.job = {**self.meta, "target_query": "test page", "estimated_volume": 10,
                    "outline": ["Test outline"], "qa_passed": True, "draft_digest": draft_digest(self.directory)}
        atomic_json(self.root / "queue" / "drafts" / f"{self.slug}.json", self.job)

    def event(self, decision="APPROVE", event_id="Ev1", user="U_SPENCER", extra=None):
        self.event_counter += 1
        event = {"type": "message", "user": user, "channel": "C_APPROVALS", "ts": f"1234.{self.event_counter:06d}",
                 "text": f"{decision} {self.slug} {self.job['draft_digest']}"}
        event.update(extra or {})
        return {"type": "event_callback", "event_id": event_id, "event": event}

    def record(self, envelope=None):
        body = json.dumps(envelope or self.event()).encode()
        timestamp = str(int(time.time()))
        signature = "v0=" + hmac.new(self.slack_key.read_bytes(), b"v0:" + timestamp.encode() + b":" + body, hashlib.sha256).hexdigest()
        return approvals.record_event(self.root, self.config, body, timestamp, signature)

    def approve(self):
        self.record()
        result = approvals.sync(self.root, self.config)
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["approved"], [self.slug])

    def test_authenticated_approval_moves_once(self):
        self.approve()
        self.assertFalse((self.root / "queue" / "drafts" / f"{self.slug}.json").exists())
        self.assertEqual(approvals.sync(self.root, self.config)["approved"], [])
        self.assertTrue((self.root / "handoffs" / "jeeves-approvals.json").is_file())

    def test_claimed_identity_without_slack_signature_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "signature"):
            approvals.record_event(self.root, self.config, json.dumps(self.event()).encode(), str(int(time.time())), "v0=forged")

    def test_malformed_receipt_does_not_crash_sync(self):
        atomic_json(self.root / "approvals" / "inbox" / "malformed.json", ["invalid"])
        result = approvals.sync(self.root, self.config)
        self.assertTrue(result["errors"])
        self.assertFalse(result["approved"])

    def test_other_user_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Spencer"):
            self.record(self.event(user="U_OTHER"))

    def test_edited_and_bot_messages_rejected(self):
        for extra in ({"subtype": "message_changed"}, {"bot_id": "B1"}, {"edited": {"ts": "1"}}):
            with self.subTest(extra=extra), self.assertRaisesRegex(ValueError, "original human"):
                self.record(self.event(extra=extra))

    def test_event_replay_rejected(self):
        self.record()
        with self.assertRaisesRegex(ValueError, "replay"):
            self.record()

    def test_old_slack_request_rejected(self):
        with self.assertRaisesRegex(ValueError, "timestamp"):
            approvals.record_event(self.root, self.config, b"{}", "1000000000", "v0=invalid")

    def test_approval_changed_body_rejected(self):
        self.record()
        (self.directory / "index.html").write_text("tampered")
        result = approvals.sync(self.root, self.config)
        self.assertEqual(result["approved"], [])
        self.assertIn("changed", result["errors"][0]["error"])

    def test_forged_jeeves_receipt_rejected(self):
        receipt = self.record()
        receipt["payload"]["decision"] = "REJECT"
        atomic_json(self.root / "approvals" / "inbox" / "Ev1.json", receipt)
        result = approvals.sync(self.root, self.config)
        self.assertIn("signature", result["errors"][0]["error"])
        self.assertFalse(result["approved"])

    def test_hold_and_reject_do_not_approve(self):
        self.record(self.event(decision="HOLD"))
        result = approvals.sync(self.root, self.config)
        self.assertEqual(result["hold"], [self.slug])
        self.assertEqual(result["approved"], [])

    def test_held_draft_can_be_explicitly_approved_later(self):
        self.record(self.event(decision="HOLD"))
        approvals.sync(self.root, self.config)
        self.record(self.event(event_id="Ev2"))
        result = approvals.sync(self.root, self.config)
        self.assertEqual(result["approved"], [self.slug])
        self.assertFalse((self.root / "queue" / "hold" / f"{self.slug}.json").exists())

    def test_latest_reject_wins_reverse_filename_order(self):
        self.record(self.event(event_id="Z_APPROVE"))
        self.record(self.event(decision="REJECT", event_id="A_REJECT"))
        result = approvals.sync(self.root, self.config)
        self.assertEqual(result["approved"], [])
        self.assertEqual(result["rejected"], [self.slug])
        self.assertFalse((self.root / "queue" / "approved" / f"{self.slug}.json").exists())

    def test_publisher_applies_pending_revocation_before_dispatch(self):
        self.approve()
        self.record(self.event(decision="REJECT", event_id="Ev2"))
        with patch("automation.publish_handler.run") as commands:
            result = publisher.publish(self.root, self.config)
        self.assertEqual(result["dealeron"], [])
        self.assertEqual(result["errors"], [])
        self.assertTrue((self.root / "queue" / "rejected" / f"{self.slug}.json").exists())
        commands.assert_not_called()

    def test_delayed_older_approval_cannot_override_reject(self):
        older = self.event(event_id="LateApprove")
        self.record(self.event(decision="REJECT", event_id="NewReject"))
        approvals.sync(self.root, self.config)
        self.record(older)
        result = approvals.sync(self.root, self.config)
        self.assertEqual(result["approved"], [])
        self.assertTrue((self.root / "queue" / "rejected" / f"{self.slug}.json").exists())

    def test_same_timestamp_conflict_refuses_approval(self):
        self.record(self.event(event_id="Approve", extra={"ts": "1234.100000"}))
        self.record(self.event(decision="REJECT", event_id="Reject", extra={"ts": "1234.100000"}))
        result = approvals.sync(self.root, self.config)
        self.assertEqual(result["approved"], [])
        self.assertEqual(result["rejected"], [self.slug])

    def test_display_distinguishes_missing_zero_and_content_volume(self):
        path = self.root / "queue" / "drafts" / f"{self.slug}.json"
        for volume, expected in ((None, "unavailable"), (0, "0")):
            self.job["estimated_volume"] = volume
            atomic_json(path, self.job)
            approvals.sync(self.root, self.config)
            report = (self.root / "APPROVALS-TODAY.md").read_text()
            self.assertIn(f"Estimated monthly volume (DataForSEO): {expected}", report)
        self.job.update(kind="content_post", title="October community update", estimated_volume=None)
        atomic_json(path, self.job)
        approvals.sync(self.root, self.config)
        report = (self.root / "APPROVALS-TODAY.md").read_text()
        self.assertIn("Content topic: October community update", report)
        self.assertIn("not applicable (content post)", report)

    def test_missing_configuration_fails_closed(self):
        result = approvals.sync(self.root, {})
        self.assertTrue(result["errors"])
        self.assertFalse(result["approved"])
        self.assertIn("APPROVE test-page-alpha", (self.root / "APPROVALS-TODAY.md").read_text())

    def test_unsafe_key_permissions_rejected(self):
        self.receipt_key.chmod(0o644)
        with self.assertRaisesRegex(ValueError, "0600"):
            self.record()

    def test_path_traversal_slug_rejected(self):
        self.job["slug"] = "../escape"
        with self.assertRaisesRegex(ValueError, "slug"):
            approvals.verify_draft(self.root, self.job)

    def test_failed_qa_cannot_approve(self):
        atomic_json(self.directory / "qa-report.json", {"passed": False})
        with self.assertRaisesRegex(ValueError, "QA"):
            self.record()

    def test_dealeron_packet_and_one_weekly_email_idempotent(self):
        self.approve()
        with patch("automation.page_generator.validate_draft", return_value={"passed": True}):
            result = publisher.publish(self.root, self.config)
        self.assertEqual(result["errors"], [])
        self.assertEqual(len(result["dealeron"]), 1)
        packet = self.root / "ready-for-dealeron" / self.slug
        self.assertEqual((packet / "index.html").read_bytes(), (self.directory / "index.html").read_bytes())
        result2 = publisher.publish(self.root, self.config)
        self.assertEqual(result2["dealeron"], [])
        self.assertEqual(len(list((self.root / "email-drafts").glob("*.md"))), 1)
        self.assertEqual(read_json(next((self.root / "handoffs").glob("jeeves-dealeron-*.json")))["status"], "prepared_not_sent")

    def test_final_html_preserves_all_approved_bytes(self):
        body = b'<p>Literal example:</p>\r\n<meta name="robots" content="noindex, nofollow">\r\n'
        (self.directory / "index.html").write_bytes(body)
        self.assertEqual(publisher.final_html(self.directory), body)

    def test_publisher_reruns_qa_and_blocks_failure(self):
        self.approve()
        with patch("automation.page_generator.validate_draft", return_value={"passed": False, "errors": ["render mismatch"]}):
            result = publisher.publish(self.root, self.config)
        self.assertEqual(result["dealeron"], [])
        self.assertIn("render mismatch", result["errors"][0]["error"])

    def test_unapproved_job_in_approved_folder_cannot_publish(self):
        atomic_json(self.root / "queue" / "approved" / f"{self.slug}.json", self.job)
        result = publisher.publish(self.root, self.config)
        self.assertFalse(result["dealeron"])
        self.assertTrue(result["errors"])

    def test_stale_source_blocks_publish(self):
        self.meta["source_evidence"][0]["retrieved_at"] = "2020-01-01T00:00:00+00:00"
        with self.assertRaisesRegex(ValueError, "stale"):
            publisher.source_check(self.job, self.meta)

    def test_changed_source_file_blocks_publish(self):
        source = self.base / "source.json"
        source.write_text("old")
        self.meta["source_evidence"][0].update(source_path=str(source), sha256=hashlib.sha256(b"old").hexdigest())
        publisher.source_check(self.job, self.meta)
        source.write_text("new")
        with self.assertRaisesRegex(ValueError, "changed"):
            publisher.source_check(self.job, self.meta)

    def test_ai_default_does_not_run_git(self):
        self.config["ai_proxy"] = {"repo_path": str(self.base), "remote": "origin", "base_branch": "main",
                                    "content_directory": "pages", "allowed_hosts": ["ai.example.test"]}
        self.meta["canonical_url"] = "https://ai.example.test/test-page-alpha/"
        with patch("automation.publish_handler.run") as command:
            result = publisher.ai_pr(self.root, self.config, self.job, self.directory, self.meta, execute=False)
        self.assertEqual(result["status"], "prepared_not_pushed")
        command.assert_not_called()
        self.assertTrue(result["branch"].startswith("seo/"))

    def test_ai_missing_config_blocks(self):
        with patch("automation.publish_handler.run") as command, self.assertRaisesRegex(ValueError, "Missing ai_proxy"):
            publisher.ai_pr(self.root, self.config, self.job, self.directory, self.meta, execute=True)
        command.assert_not_called()

    def test_ai_unapproved_job_never_runs_git(self):
        self.config["ai_proxy"] = {"repo_path": str(self.base), "remote": "origin", "base_branch": "main",
                                    "content_directory": "pages", "allowed_hosts": ["ai.example.test"]}
        self.meta["canonical_url"] = "https://ai.example.test/test-page-alpha/"
        with patch("automation.publish_handler.run") as command, self.assertRaises(ValueError):
            publisher.ai_pr(self.root, self.config, self.job, self.directory, self.meta, execute=True)
        command.assert_not_called()

    def test_content_exports_exact_payload_without_dealeron(self):
        content = "Approved October caption.\n"
        manifest = self.base / "manifest.json"
        manifest.write_text("{}")
        source = self.base / "draft.md"
        source.write_text(content)
        self.meta.update(upstream_manifest_path=str(manifest), upstream_manifest_sha256=hashlib.sha256(b"{}").hexdigest(),
                         kind="content_post", target_platform="content_post", content_files=[{
            "source_path": str(source),
            "path": "pieces/P1/draft.md", "role": "caption", "sha256": hashlib.sha256(content.encode()).hexdigest(), "text": content}])
        atomic_json(self.directory / "meta.json", self.meta)
        self.job.update(self.meta, draft_digest=draft_digest(self.directory))
        atomic_json(self.root / "queue" / "drafts" / f"{self.slug}.json", self.job)
        self.approve()
        result = publisher.publish(self.root, self.config)
        self.assertEqual(result["errors"], [])
        self.assertEqual(len(result["content_posts"]), 1)
        self.assertEqual((self.root / "ready-for-content" / self.slug / "content/pieces/P1/draft.md").read_text(), content)
        self.assertEqual(result["dealeron"], [])
        self.assertFalse((self.root / "email-drafts").exists())

    def test_fixture_cannot_publish(self):
        self.meta["fixture_only"] = True
        with self.assertRaisesRegex(ValueError, "Fixture"):
            publisher.source_check(self.job, self.meta)

    def test_content_path_traversal_rejected(self):
        with self.assertRaisesRegex(ValueError, "Unsafe"):
            publisher.relative_path("../../outside")


if __name__ == "__main__":
    unittest.main()
