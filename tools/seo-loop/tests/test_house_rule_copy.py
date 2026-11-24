"""A3: the house-rule-copy catalog entry and its first finding candidate. No network."""
from __future__ import annotations

import io
import json
import os
import re
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PKG not in sys.path:
    sys.path.insert(0, PKG)

import ingest_reports  # noqa: E402
import register  # noqa: E402

FIX = os.path.join(PKG, "tests", "fixtures")
CHECKS = os.path.join(PKG, "..", "..", "findings", "checks.json")
ADD = os.path.join(FIX, "house-rule-copy.check.json")
CAND = os.path.join(FIX, "candidates", "candidates-house-rule-2026-11-23.jsonl")
OWNERS = ("rory", "rory-ai-search", "rory-copy-seo", "rory-performance", "rory-compliance", "jeeves",
          "holmes", "emily-design", "emily-qa", "coordinator", "spencer")
FIELDS = ["check_id", "title", "plain_english", "tier", "fix_type", "owner", "surface", "brand_scope",
          "verify_template"]
CODE_IN_PLAIN = re.compile(r"[/\\_~`]|\.(txt|json|py|md|aspx|html|jsonl)\b|\bF-[a-z]|noindex|canonical|robots|schema|json|llms", re.I)


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


class HouseRuleCopyTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.reg = os.path.join(self.dir, "register.jsonl")
        self.inbox = os.path.join(self.dir, "inbox.jsonl")

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def entry(self):
        (e,) = load(ADD)
        return e

    def test_entry_matches_the_catalog_shape_and_the_merged_catalog(self):
        e = self.entry()
        self.assertEqual(sorted(e), sorted(FIELDS))
        self.assertEqual((e["surface"], e["fix_type"], e["owner"]), ("web", "dealeron_request", "rory-compliance"))
        self.assertIn(e["owner"], OWNERS)
        self.assertIn(e["tier"], register.TIERS)
        self.assertIn(e["fix_type"], register.FIX_TYPES)
        # the catalog template is generic: it carries no one-page literal (each finding brings its own rule)
        self.assertEqual(e["verify_template"]["type"], "manual")
        self.assertIn(e["verify_template"]["type"], register.VERIFY_TYPES)
        self.assertNotIn("camry", json.dumps(e).lower())
        merged = [c for c in load(CHECKS) if c["check_id"] == "house-rule-copy"]
        self.assertEqual(merged, [e])

    def test_plain_english_rules(self):
        e = self.entry()
        pe = e["plain_english"]
        self.assertIsNone(CODE_IN_PLAIN.search(pe))
        self.assertIsNone(re.search(r"\d", pe))
        self.assertEqual(len(re.findall(r"[.!?](\s|$)", pe)), 1)
        for c in load(CHECKS):
            if c["check_id"] != e["check_id"]:
                self.assertNotIn(c["check_id"], pe)

    def run_ingest(self):
        out, err = io.StringIO(), io.StringIO()
        argv = ["--register", self.reg, "--checks", CHECKS, "--inbox", self.inbox, "--candidates", CAND,
                "--today", "2026-11-23", "--test-mode"]
        with redirect_stdout(out), redirect_stderr(err):
            code = ingest_reports.main(argv)
        return code, out.getvalue(), err.getvalue()

    def test_candidate_ingests_as_one_new_row(self):
        code, out, err = self.run_ingest()
        self.assertEqual(code, 0, out + err)
        rows = register.load_rows(self.reg)
        self.assertEqual(len(rows), 1)
        r = rows[0]
        self.assertEqual(r["check_id"], "house-rule-copy")
        self.assertEqual(r["status"], "new")
        self.assertEqual(r["site"], "toyota")
        self.assertEqual(r["fix_type"], "dealeron_request")
        self.assertEqual(r["verify"]["type"], "html_not_contains")
        self.assertEqual(r["verify"]["assert"], "last chance at a gas-only Camry")
        self.assertTrue(r["verify"]["url"].endswith("/new-toyota-camry"))
        self.assertEqual(register.validate_rows(rows, base_dir=self.dir), [])
        self.assertFalse(os.path.exists(self.inbox) and os.path.getsize(self.inbox) > 0)

    def test_catalog_template_alone_gives_a_manual_rule(self):
        e = self.entry()
        rule = ingest_reports.verify_for(e, "https://example.test/p")
        self.assertEqual(rule, {"type": "manual", "url": "https://example.test/p",
                                "assert": e["verify_template"]["assert"]})
        self.assertEqual(ingest_reports.expected_for(e), e["verify_template"]["assert"])

    def test_candidate_rule_is_testable_and_catalog_text_is_not_a_machine_rule(self):
        import verify_fix
        (line,) = [ln for ln in open(CAND, encoding="utf-8").read().splitlines() if ln.strip()]
        c = json.loads(line)
        self.assertTrue(verify_fix.rule_is_testable(c["verify"], c["observed"]))
        self.assertFalse(verify_fix.rule_is_testable(c["verify"], "a different page text"))
        self.assertEqual(ingest_reports.expected_for(c), c["expected"])
        rule = ingest_reports.verify_for(self.entry(), c["target"], c["verify"])
        self.assertEqual(rule, c["verify"])

    def test_candidate_never_crosses_makes(self):
        (line,) = [ln for ln in open(CAND, encoding="utf-8").read().splitlines() if ln.strip()]
        c = json.loads(line)
        self.assertEqual(c["site"], "toyota")
        self.assertNotRegex(json.dumps(c).lower(), r"chevrolet|chevy|silverado")


if __name__ == "__main__":
    unittest.main()
