"""Offline fixtures are synthetic test data, never production source evidence."""
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import atomic_json, draft_digest, read_json
from page_generator import generate, generate_job, validate_draft, _Inspector, _qa


def fixture_job():
    now = datetime.now(timezone.utc).isoformat()
    description = "Read the service information for the example dealership in this offline test fixture, with verified source references and related resources."
    claim = "This dealership record is synthetic data for offline testing."
    url = "https://fixture.invalid/contact"
    return {"slug": "test-page-alpha", "title": "Example Dealership Service Information", "target_query": "example dealership service",
            "cluster": "service", "owner_host": "fixture.invalid", "target_url": "https://fixture.invalid/test-page-alpha",
            "meta_description": description, "outline": ["Service information"], "destination": "dealeron", "fixture_only": True,
            "gsc_check": {"status": "checked"}, "topology_status": "verified",
            "source_evidence": [{"id": "fixture-record", "source_type": "DealerVault", "verified": True,
                                 "url": "https://fixture.invalid/source", "retrieved_at": now,
                                 "claims": [description, claim, url, "Example contact information", "Example Dealership", "https://fixture.invalid/"]}],
            "sections": [{"heading": "Service information", "claims": [{"text": claim, "evidence_ids": ["fixture-record"]}]}],
            "faq": [{"question": "Where can I read the record?", "answer": claim, "evidence_ids": ["fixture-record"]}],
            "internal_links": [{"anchor": "Example contact information", "url": url, "http_status": 200,
                                "canonical": url, "checked_at": now, "evidence_ids": ["fixture-record"]}],
            "business": {"name": "Example Dealership", "url": "https://fixture.invalid/", "evidence_ids": ["fixture-record"]}}


class PageGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "pipeline"
        self.job = fixture_job()

    def pending(self, job=None):
        job = self.job if job is None else job
        path = self.root / "queue" / "pending" / f"{job['slug']}.json"
        atomic_json(path, job)
        return path

    def test_complete_fixture_moves_only_to_drafts(self):
        pending = self.pending()
        result = generate(self.root)
        self.assertEqual(result["generated"], 1, result)
        directory = self.root / "drafts" / self.job["slug"]
        self.assertEqual({p.name for p in directory.iterdir()}, {"index.html", "meta.json", "evidence.md", "qa-report.json"})
        self.assertFalse(pending.exists())
        marker = read_json(self.root / "queue" / "drafts" / f"{self.job['slug']}.json")
        self.assertTrue(marker["qa_passed"])
        self.assertEqual(marker["draft_digest"], draft_digest(directory))
        self.assertFalse(marker["publication_authorized"])
        self.assertTrue(read_json(directory / "qa-report.json")["passed"])
        self.assertNotIn("noindex", (directory / "index.html").read_text())
        self.assertNotIn("Research draft", (directory / "index.html").read_text())
        inspector = _Inspector()
        inspector.feed((directory / "index.html").read_text())
        schema = json.loads(inspector.schemas[0])
        self.assertEqual([x["@type"] for x in schema["@graph"]], ["Article", "FAQPage", "LocalBusiness"])
        self.assertIn(self.job["sections"][0]["claims"][0]["text"], (directory / "evidence.md").read_text())
        self.assertFalse((self.root / "queue" / "approved").exists())

    def test_unsupported_claim_stays_pending(self):
        self.job["sections"][0]["claims"][0]["text"] = "Guaranteed financing with no credit check."
        path = self.pending()
        result = generate(self.root)
        self.assertEqual(result["blocked"], 1)
        self.assertTrue(read_json(path)["qa_errors"])
        self.assertFalse((self.root / "queue" / "drafts" / f"{self.job['slug']}.json").exists())

    def test_unverified_and_stale_sources_are_blocked(self):
        for field, value in [("verified", False), ("source_type", "invented"), ("retrieved_at", "2000-01-01T00:00:00Z")]:
            with self.subTest(field=field):
                job = deepcopy(self.job)
                job["source_evidence"][0][field] = value
                self.assertEqual(generate_job(self.root, job)["status"], "blocked")

    def test_source_expiry_overrides_fresh_retrieval_timestamp(self):
        for value in [(datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat(),
                      "invalid", None, "2999-01-01T00:00:00"]:
            with self.subTest(valid_until=value):
                job = deepcopy(self.job)
                job["source_evidence"][0]["valid_until"] = value
                result = generate_job(self.root, job)
                self.assertEqual(result["status"], "blocked", result)
                self.assertFalse((self.root / "queue" / "drafts" / f"{job['slug']}.json").exists())
        self.job["source_evidence"][0]["valid_until"] = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
        self.assertEqual(generate_job(self.root, self.job)["status"], "draft")
        directory = self.root / "drafts" / self.job["slug"]
        self.assertTrue(validate_draft(directory)["passed"])
        meta = read_json(directory / "meta.json")
        meta["source_evidence"][0]["valid_until"] = (datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat()
        atomic_json(directory / "meta.json", meta)
        self.assertFalse(validate_draft(directory)["passed"])

    def test_missing_reference_is_blocked(self):
        self.job["sections"][0]["claims"][0]["evidence_ids"] = ["missing"]
        self.assertEqual(generate_job(self.root, self.job)["status"], "blocked")

    def test_title_meta_and_mobile_qa(self):
        self.job["title"] = "Short"
        self.job["meta_description"] = "Too short"
        result = generate_job(self.root, self.job)
        self.assertEqual(result["status"], "blocked")
        report = read_json(self.root / "drafts" / self.job["slug"] / "qa-report.json")
        self.assertFalse(report["checks"]["title_length"])
        self.assertFalse(report["checks"]["meta_description_length"])
        report = _qa('<script src="https://evil.invalid/x"></script>', fixture_job(), [])
        self.assertFalse(report["checks"]["no_external_dependencies"])
        self.assertFalse(report["checks"]["mobile_viewport"])

    def test_html_and_jsonld_are_escaped(self):
        evil = '</script><script src="https://evil.invalid/x">alert(1)</script>&'
        self.job["source_evidence"][0]["claims"].append(evil)
        self.job["sections"][0]["claims"][0]["text"] = evil
        self.job["faq"][0]["answer"] = evil
        result = generate_job(self.root, self.job)
        self.assertEqual(result["status"], "draft", result)
        html = (self.root / "drafts" / self.job["slug"] / "index.html").read_text()
        self.assertNotIn('<script src="https://evil.invalid/x">', html)
        parser = _Inspector()
        parser.feed(html)
        self.assertEqual(len(parser.schemas), 1)
        self.assertEqual(json.loads(parser.schemas[0])["@graph"][0]["articleBody"], evil)

    def test_broken_noncanonical_and_stale_links_block(self):
        for field, value in [("http_status", 404), ("canonical", "https://fixture.invalid/wrong"), ("checked_at", "2000-01-01T00:00:00Z")]:
            with self.subTest(field=field):
                job = deepcopy(self.job)
                job["internal_links"][0][field] = value
                self.assertEqual(generate_job(self.root, job)["status"], "blocked")

    def test_path_traversal_cannot_write(self):
        self.job["slug"] = "../../outside"
        self.assertEqual(generate_job(self.root, self.job)["status"], "blocked")
        self.assertFalse((Path(self.temp.name) / "outside").exists())

    def test_no_faq_or_business_does_not_fabricate_schema(self):
        self.job.pop("business")
        self.job["faq"] = []
        self.assertEqual(generate_job(self.root, self.job)["status"], "draft")
        parser = _Inspector()
        parser.feed((self.root / "drafts" / self.job["slug"] / "index.html").read_text())
        self.assertEqual([x["@type"] for x in json.loads(parser.schemas[0])["@graph"]], ["Article"])

    def test_review_state_is_immutable(self):
        self.assertEqual(generate_job(self.root, self.job)["status"], "draft")
        directory = self.root / "drafts" / self.job["slug"]
        before = draft_digest(directory)
        self.job["title"] = "Modified Example Dealership Information"
        self.assertEqual(generate_job(self.root, self.job)["status"], "blocked")
        self.assertEqual(draft_digest(directory), before)

    def test_used_inventory_requires_staging_read(self):
        self.job["cluster"] = "used inventory"
        result = generate_job(self.root, self.job)
        self.assertEqual(result["status"], "blocked")
        self.assertTrue(any("BLOCKED-STAGING-READ" in x for x in result["errors"]))

    def test_editorial_title_allowed_but_unsupported_promotion_rejected(self):
        self.job["title"] = "Guaranteed Best Dealership in Carroll"
        self.assertEqual(generate_job(self.root, self.job)["status"], "blocked")

    def test_filename_slug_mismatch_stays_pending(self):
        path = self.root / "queue" / "pending" / "different-slug.json"
        atomic_json(path, self.job)
        self.assertEqual(generate(self.root)["blocked"], 1)
        self.assertTrue(path.exists())

    def test_malformed_types_block_without_draft(self):
        for key in ("title", "source_evidence", "sections", "faq", "internal_links", "business"):
            with self.subTest(key=key):
                job = deepcopy(self.job)
                job[key] = 3
                self.assertEqual(generate_job(self.root, job)["status"], "blocked")

    def test_publish_revalidation_is_read_only_and_detects_tampering(self):
        self.assertEqual(generate_job(self.root, self.job)["status"], "draft")
        directory = self.root / "drafts" / self.job["slug"]
        before = draft_digest(directory)
        self.assertTrue(validate_draft(directory)["passed"])
        self.assertEqual(before, draft_digest(directory))
        path = directory / "index.html"
        path.write_text(path.read_text().replace("Related resources", "Unsupported extra claim"))
        self.assertFalse(validate_draft(directory)["passed"])

    def test_publish_revalidation_rejects_stale_source_and_missing_citations(self):
        self.assertEqual(generate_job(self.root, self.job)["status"], "draft")
        directory = self.root / "drafts" / self.job["slug"]
        (directory / "evidence.md").write_text("No citations")
        self.assertFalse(validate_draft(directory)["passed"])
        meta = read_json(directory / "meta.json")
        meta["source_evidence"][0]["retrieved_at"] = "2000-01-01T00:00:00Z"
        atomic_json(directory / "meta.json", meta)
        self.assertFalse(validate_draft(directory)["passed"])

    def test_unresolved_blockers_stay_pending_even_with_verified_copy(self):
        self.job["blockers"] = ["GSC access unavailable"]
        pending = self.pending()
        self.assertEqual(generate(self.root)["blocked"], 1)
        self.assertTrue(pending.exists())
        self.assertTrue(any("unresolved blockers" in x for x in read_json(pending)["qa_errors"]))

    def test_production_requires_gsc_and_crawl_topology(self):
        self.job.pop("fixture_only")
        self.job.pop("gsc_check")
        self.job["topology_status"] = "candidate-needs-crawl-review"
        self.assertEqual(generate_job(self.root, self.job)["status"], "blocked")
        self.job["gsc_check"] = {"status": "checked"}
        self.assertEqual(generate_job(self.root, self.job)["status"], "blocked")
        self.job["topology_status"] = "verified"
        self.assertEqual(generate_job(self.root, self.job)["status"], "draft")

    def test_content_posts_are_left_to_importer(self):
        self.job["kind"] = "content_post"
        path = self.pending()
        before = path.read_bytes()
        self.assertEqual(generate(self.root)["generated"], 0)
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual(generate_job(self.root, self.job)["status"], "skipped")
        self.assertFalse((self.root / "drafts").exists())

    def crawl_job(self):
        job = deepcopy(self.job)
        link = job["internal_links"][0]
        row = {"id": "live-link", "source_type": "SiteCrawl", "scope": "links", "verified": True,
               "url": link["url"], "canonical": link["url"], "http_status": 200,
               "response_sha256": "a" * 64, "retrieved_at": link["checked_at"], "checked_at": link["checked_at"],
               "claims": [link["url"], link["anchor"]]}
        job["source_evidence"].append(row)
        link["evidence_ids"] = [row["id"]]
        return job

    def test_site_crawl_can_verify_technical_links_only(self):
        job = self.crawl_job()
        self.assertEqual(generate_job(self.root, job)["status"], "draft")
        self.assertTrue(validate_draft(self.root / "drafts" / job["slug"])["passed"])

    def test_site_crawl_cannot_support_dealership_body_or_business(self):
        for field in ("body", "business", "meta", "faq", "title"):
            with self.subTest(field=field):
                job = self.crawl_job()
                row = job["source_evidence"][-1]
                if field == "body":
                    claim = job["sections"][0]["claims"][0]
                    row["claims"].append(claim["text"])
                    claim["evidence_ids"] = [row["id"]]
                elif field == "business":
                    row["claims"].extend([job["business"]["name"], job["business"]["url"]])
                    job["business"]["evidence_ids"] = [row["id"]]
                elif field == "meta":
                    job["source_evidence"][0]["claims"].remove(job["meta_description"])
                    row["claims"].append(job["meta_description"])
                elif field == "faq":
                    row["claims"].append(job["faq"][0]["answer"])
                    job["faq"][0]["evidence_ids"] = [row["id"]]
                else:
                    job["title"] = "Guaranteed Best Dealership in Carroll"
                    row["claims"].append(job["title"])
                self.assertEqual(generate_job(self.root, job)["status"], "blocked")

    def test_site_crawl_requires_exact_current_technical_proof(self):
        for key, value in [("scope", "facts"), ("http_status", 302), ("canonical", "https://fixture.invalid/wrong"),
                           ("response_sha256", "invalid"), ("checked_at", "2000-01-01T00:00:00Z"),
                           ("retrieved_at", "2000-01-01T00:00:00Z")]:
            with self.subTest(key=key):
                job = self.crawl_job()
                job["source_evidence"][-1][key] = value
                self.assertEqual(generate_job(self.root, job)["status"], "blocked")

    def test_site_crawl_proof_cannot_verify_another_destination(self):
        job = self.crawl_job()
        row = job["source_evidence"][-1]
        row["url"] = row["canonical"] = "https://fixture.invalid/different-page"
        self.assertEqual(generate_job(self.root, job)["status"], "blocked")

    def filtered_inventory_job(self):
        job = self.crawl_job()
        row = job["source_evidence"][-1]
        link = job["internal_links"][0]
        url = "https://fixture.invalid/searchnew.aspx?Make=Toyota&Model=Tundra"
        canonical = "https://fixture.invalid/searchnew.aspx"
        anchor = "Browse Toyota Tundra inventory"
        row.update(url=url, canonical=canonical, final_url=url, requested_url=url,
                   canonical_scope="parent-inventory", canonical_verified=True, canonical_http_status=200,
                   filter_verified=True, intended_make="Toyota", intended_model="Tundra",
                   visible_heading="New Toyota Tundra inventory", claims=[url, anchor])
        link.update(url=url, canonical=canonical, anchor=anchor)
        return job

    def test_verified_filtered_inventory_parent_canonical_allowed(self):
        job = self.filtered_inventory_job()
        result = generate_job(self.root, job)
        self.assertEqual(result["status"], "draft", result)
        directory = self.root / "drafts" / job["slug"]
        self.assertTrue(validate_draft(directory)["passed"])
        self.assertIn("Make=Toyota&amp;Model=Tundra", (directory / "index.html").read_text())
        self.assertIn("not a separately indexable destination", (directory / "evidence.md").read_text())

    def test_filtered_inventory_rejects_wrong_host_path_or_missing_filter_proof(self):
        for key, value in [("canonical", "https://another.invalid/searchnew.aspx"),
                           ("canonical", "https://fixture.invalid/different-path"),
                           ("canonical", "https://fixture.invalid/searchnew.aspx?Make=Toyota"),
                           ("canonical_verified", False), ("canonical_http_status", 404),
                           ("filter_verified", False), ("visible_heading", "New Vehicles"),
                           ("intended_model", "Tacoma"),
                           ("requested_url", "https://fixture.invalid/searchnew.aspx?Make=Toyota&Model=Tacoma")]:
            with self.subTest(key=key, value=value):
                job = self.filtered_inventory_job()
                job["source_evidence"][-1][key] = value
                if key == "canonical":
                    job["internal_links"][0][key] = value
                self.assertEqual(generate_job(self.root, job)["status"], "blocked")

    def test_job_level_filtered_flags_cannot_replace_crawl_proof(self):
        job = self.filtered_inventory_job()
        proof = job["source_evidence"][-1]
        for key in ("canonical_scope", "canonical_verified", "canonical_http_status", "filter_verified"):
            job["internal_links"][0][key] = proof.pop(key)
        self.assertEqual(generate_job(self.root, job)["status"], "blocked")


if __name__ == "__main__":
    unittest.main()
