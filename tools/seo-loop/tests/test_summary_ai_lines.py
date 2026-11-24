"""Monday summary: the AI answers line and the AI assistant visits line. No network, no live files."""
from __future__ import annotations

import datetime as _dt
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
        self.assertIn("AI answers: 3 (Nov 16\u201322).", out)
        self.assertNotIn("observed", out)
        self.assertNotIn("named in", out)
        self.scan(out)

    def test_ai_answers_ignores_unknown_shapes(self):
        """Only the real {value, window, source, pulled_at} shape counts; engine blocks and 'total' do not."""
        ok = {"value": 3, "window": "2026-11-16..2026-11-22", "source": "s", "pulled_at": "2026-11-23T06:40:00Z"}
        self.assertEqual(monday_summary._ai_line({"ai_answers": {"total": ok}}), "AI answers: not verified.")
        self.assertEqual(monday_summary._ai_line({"ai_answers": {"chatgpt": ok}}), "AI answers: not verified.")
        self.assertEqual(monday_summary._ai_line({"ai_answers": "not verified"}), "AI answers: not verified.")
        self.assertEqual(monday_summary._ai_line({"ai_answers": dict(ok, value="not verified")}),
                         "AI answers: not verified.")
        self.assertEqual(monday_summary._ai_line({"ai_answers": dict(ok, value=True)}), "AI answers: not verified.")
        extra = dict(ok, named=3, observed=12)  # extra keys are never read
        self.assertEqual(monday_summary._ai_line({"ai_answers": extra}), "AI answers: 3 (Nov 16\u201322).")

    def test_ai_answers_window_wording(self):
        base = {"value": 5, "source": "s", "pulled_at": "p"}
        line = lambda w: monday_summary._ai_line({"ai_answers": dict(base, window=w)})
        self.assertEqual(line("2026-10-28..2026-11-03"), "AI answers: 5 (Oct 28\u2013Nov 3).")
        self.assertEqual(line("2026-11-03..2026-11-03"), "AI answers: 5 (Nov 3).")
        self.assertEqual(line("w"), "AI answers: 5 (window not stated).")

    def test_ai_answers_line_without_block(self):
        rc, out = run_main("b_noai.json")
        self.assertEqual(rc, 0)
        self.assertEqual(len([ln for ln in out.splitlines() if ln.startswith("AI answers:")]), 1)
        self.assertIn("AI answers: not verified.", out)
        self.assertIn("Not verified this week: AI answers, AI assistant visits.", out)
        self.scan(out)

    def test_ai_assistant_visits_line_with_block(self):
        rc, out = run_main("b_refs.json")
        self.assertEqual(rc, 0)
        self.assertIn("AI assistants sent 7 visits, 4 leads (forms + calls), Nov 1\u201323.", out)
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

    def referrals(self, window_end, today="2026-11-24"):
        win = "%s-01..%s" % (window_end[:7], window_end)
        metric = lambda v: {"value": v, "window": win, "source": "ga4:ai_referrals", "pulled_at": "p"}
        block = {"ai_referrals": {"2026-11": {"sessions": metric(4), "leads": metric(0)}}}
        return monday_summary._ai_referrals_line(block, _dt.date.fromisoformat(today))

    def test_referrals_line_shows_the_window(self):
        self.assertEqual(self.referrals("2026-11-23"), "AI assistants sent 4 visits, 0 leads (forms + calls), Nov 1\u201323.")

    def test_referrals_boundary_and_stale(self):
        # 8 days old is the limit and is still shown; 9 days is stale
        self.assertIn("AI assistants sent", self.referrals("2026-11-16"))
        self.assertEqual(self.referrals("2026-11-15"), "AI assistant visits: not verified (stale).")
        self.assertEqual(self.referrals("2026-10-31"), "AI assistant visits: not verified (stale).")

    def test_referrals_future_or_mismatched_window_is_not_verified(self):
        self.assertEqual(self.referrals("2026-11-30"), "AI assistant visits: not verified.")
        win_a, win_b = "2026-11-01..2026-11-23", "2026-11-01..2026-11-22"
        block = {"ai_referrals": {"2026-11": {
            "sessions": {"value": 4, "window": win_a, "source": "s", "pulled_at": "p"},
            "leads": {"value": 0, "window": win_b, "source": "s", "pulled_at": "p"}}}}
        self.assertEqual(monday_summary._ai_referrals_line(block, _dt.date(2026, 11, 24)),
                         "AI assistant visits: not verified.")

    def test_stale_referrals_are_listed_as_not_verified(self):
        block = {"ai_referrals": {"2026-10": {
            "sessions": {"value": 4, "window": "2026-10-01..2026-10-31", "source": "s", "pulled_at": "p"},
            "leads": {"value": 0, "window": "2026-10-01..2026-10-31", "source": "s", "pulled_at": "p"}}}}
        out = monday_summary._unverified_sources(block, {"group": 1, "toyota": 1, "chevy": 1}, 1, _dt.date(2026, 11, 24))
        self.assertIn(monday_summary.AI_VISITS, out)


if __name__ == "__main__":
    unittest.main()
