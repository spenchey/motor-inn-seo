"""Monday summary: the AI answers line and the AI assistant visits line. No network, no live files."""
from __future__ import annotations

import io
import os
import re
import sys
import unittest

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PKG not in sys.path:
    sys.path.insert(0, PKG)

import monday_summary  # noqa: E402

FIX = os.path.join(PKG, "tests", "fixtures")
EMPTY = os.path.join(FIX, "empty.jsonl")
TODAY = "2026-11-24"


def run_main(baselines_name):
    out, err, old = io.StringIO(), io.StringIO(), sys.stderr
    sys.stderr = err
    try:
        rc = monday_summary.main(["--register", EMPTY, "--baselines", os.path.join(FIX, baselines_name),
                                  "--today", TODAY], out)
    finally:
        sys.stderr = old
    return rc, out.getvalue()


class AiLineTests(unittest.TestCase):
    def scan(self, out):
        self.assertNotRegex(out, r"\bF-|ai_answers|ai_referrals|\.json|\.jsonl|/Users")
        self.assertLess(len(out.split()), 300)

    def test_ai_answers_line_with_block(self):
        rc, out = run_main("b_ai.json")
        self.assertEqual(rc, 0)
        self.assertIn("AI answers: named in 3 of 12 observed answers.", out)
        self.assertNotIn("AI answers: not verified", out)
        self.scan(out)

    def test_ai_answers_line_without_block(self):
        rc, out = run_main("b_noai.json")
        self.assertEqual(rc, 0)
        self.assertEqual(len([ln for ln in out.splitlines() if ln.startswith("AI answers:")]), 1)
        self.assertIn("AI answers: not verified.", out)
        self.assertIn("Not verified this week: AI answers.", out)
        self.scan(out)

    def test_ai_assistant_visits_line_with_block(self):
        rc, out = run_main("b_refs.json")
        self.assertEqual(rc, 0)
        self.assertIn("AI assistants sent 7 visits, 4 leads in November.", out)
        self.assertNotIn("AI assistant visits: not verified", out)
        self.scan(out)

    def test_ai_assistant_visits_line_without_block(self):
        for name in ("b_noai.json", "b_ai.json"):
            rc, out = run_main(name)
            self.assertEqual(rc, 0)
            self.assertIn("AI assistant visits: not verified.", out)
            self.assertEqual(len(re.findall(r"^AI assistant", out, re.M)), 1)
            self.scan(out)

    def test_ai_assistant_visits_unverified_value_is_not_zero(self):
        rc, out = run_main("b_refs_nv.json")
        self.assertEqual(rc, 0)
        self.assertIn("AI assistant visits: not verified.", out)
        self.assertNotIn("AI assistants sent", out)


if __name__ == "__main__":
    unittest.main()
