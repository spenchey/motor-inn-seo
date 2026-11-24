import datetime
import json
import os
import tempfile
import unittest

import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ai_referrals as ar

TODAY = datetime.date(2026, 11, 24)


def fake_run(fail=False):
    def run(start, end, dims, metrics):
        if fail:
            raise ar.AiReferralError("down")
        run.calls.append((start, end, tuple(dims)))
        if dims == ["sessionSource", "sessionMedium"]:
            return [
                {"sessionSource": "google", "sessionMedium": "organic", "sessions": 300},
                {"sessionSource": "bing", "sessionMedium": "organic", "sessions": 100},
                {"sessionSource": "chatgpt.com", "sessionMedium": "ai-assistant", "sessions": 3},
                {"sessionSource": "chatgpt.com", "sessionMedium": "web", "sessions": 1},
                {"sessionSource": "perplexity.ai", "sessionMedium": "referral", "sessions": 2},
                {"sessionSource": "newbot", "sessionMedium": "ai-assistant", "sessions": 1},
            ]
        if dims == ["sessionSource", "eventName"]:
            return [
                {"sessionSource": "chatgpt.com", "eventName": "asc_form_submission", "eventCount": 1},
                {"sessionSource": "chatgpt.com", "eventName": "asc_click_to_call", "eventCount": 2},
                {"sessionSource": "chatgpt.com", "eventName": "asc_cta_interaction", "eventCount": 9},
                {"sessionSource": "google", "eventName": "asc_form_submission", "eventCount": 50},
                {"sessionSource": "newbot", "eventName": "asc_click_to_call", "eventCount": 1},
            ]
        return [
            {"sessionSource": "chatgpt.com", "landingPagePlusQueryString": "/new-toyota?x=1", "sessions": 2},
            {"sessionSource": "chatgpt.com", "landingPagePlusQueryString": "/new-toyota", "sessions": 1},
            {"sessionSource": "perplexity.ai", "landingPagePlusQueryString": "/contactus.aspx", "sessions": 2},
            {"sessionSource": "google", "landingPagePlusQueryString": "/", "sessions": 999},
        ]
    run.calls = []
    return run


class Classify(unittest.TestCase):
    def test_assistants(self):
        self.assertEqual(ar.classify_source("chatgpt.com"), "chatgpt")
        self.assertEqual(ar.classify_source("chat.openai.com"), "chatgpt")
        self.assertEqual(ar.classify_source("www.perplexity.ai"), "perplexity")
        self.assertEqual(ar.classify_source("gemini.google.com"), "gemini")
        self.assertEqual(ar.classify_source("copilot.microsoft.com"), "copilot")
        self.assertEqual(ar.classify_source("claude.ai"), "claude")

    def test_not_assistants(self):
        for s in ("google", "bing", "(direct)", "facebook", "search.google.com", "mailchimp", ""):
            self.assertIsNone(ar.classify_source(s, "organic"), s)

    def test_medium_catch_all(self):
        self.assertEqual(ar.classify_source("somenew.ai", "ai-assistant"), "other_ai")

    def test_google_is_not_gemini(self):
        self.assertIsNone(ar.classify_source("google.com", "referral"))


class Window(unittest.TestCase):
    def test_full_month(self):
        s, e = ar.month_window("2026-10", TODAY)
        self.assertEqual((s.isoformat(), e.isoformat()), ("2026-10-01", "2026-10-31"))

    def test_current_month_to_yesterday(self):
        s, e = ar.month_window("2026-11", TODAY)
        self.assertEqual(e.isoformat(), "2026-11-23")

    def test_bad_and_future(self):
        with self.assertRaises(ar.AiReferralError):
            ar.month_window("2026-13", TODAY)
        with self.assertRaises(ar.AiReferralError):
            ar.month_window("2027-01", TODAY)
        with self.assertRaises(ar.AiReferralError):
            ar.month_window("2026-11", datetime.date(2026, 11, 1))


class Pull(unittest.TestCase):
    def test_counts(self):
        b = ar.pull_month("2026-11", fake_run(), TODAY, "2026-11-24T06:00:00Z")
        self.assertEqual(b["sessions"]["value"], 7)
        self.assertEqual(b["leads"]["value"], 4)
        self.assertEqual(b["sessions"]["window"], "2026-11-01..2026-11-23")
        self.assertEqual(b["sessions"]["source"], "ga4:ai_referrals")
        self.assertEqual(b["by_source"]["chatgpt"], {"sessions": 4, "leads": 3})
        self.assertEqual(b["by_source"]["perplexity"], {"sessions": 2, "leads": 0})
        self.assertEqual(b["by_source"]["other_ai"], {"sessions": 1, "leads": 1})
        self.assertNotIn("google", b["by_source"])
        self.assertNotIn("bing", b["by_source"])

    def test_top_pages_merge_query_and_skip_non_ai(self):
        b = ar.pull_month("2026-11", fake_run(), TODAY)
        self.assertEqual(b["top_landing_pages"][0], {"path": "/new-toyota", "sessions": 3})
        self.assertEqual(len(b["top_landing_pages"]), 2)

    def test_failure_is_not_zero(self):
        b = ar.pull_month("2026-11", fake_run(fail=True), TODAY)
        self.assertEqual(b["sessions"], ar.NOT_VERIFIED)
        self.assertEqual(b["leads"], ar.NOT_VERIFIED)

    def test_zero_is_a_real_zero(self):
        def empty(*a):
            return []
        b = ar.pull_month("2026-10", empty, TODAY, "2026-11-24T06:00:00Z")
        self.assertEqual(b["sessions"]["value"], 0)
        self.assertEqual(b["by_source"], {})


class Summary(unittest.TestCase):
    def test_line(self):
        b = ar.pull_month("2026-11", fake_run(), TODAY)
        self.assertEqual(ar.summary_line("2026-11", b), "AI assistants sent 7 visits, 4 leads in November.")

    def test_singular(self):
        blk = {"sessions": {"value": 1}, "leads": {"value": 1}}
        self.assertEqual(ar.summary_line("2026-10", blk), "AI assistants sent 1 visit, 1 lead in October.")

    def test_not_verified(self):
        blk = {"sessions": ar.NOT_VERIFIED, "leads": ar.NOT_VERIFIED}
        self.assertIn("not verified", ar.summary_line("2026-10", blk))


class Main(unittest.TestCase):
    def test_merge_keeps_other_keys_and_months(self):
        with tempfile.TemporaryDirectory() as d:
            base = os.path.join(d, "b.json")
            with open(base, "w") as fh:
                json.dump({"month": "2026-11", "sites": {"group": {}}, "ai_answers": "not verified",
                           "ai_referrals": {"2026-09": {"sessions": ar.NOT_VERIFIED}}}, fh)
            out = os.path.join(d, "out.json")
            rc = ar.main(["--month", "2026-10", "--month", "2026-11", "--baseline", base, "--out", out],
                         run=fake_run(), today=TODAY)
            self.assertEqual(rc, 0)
            doc = json.load(open(out))
            self.assertEqual(doc["ai_answers"], "not verified")
            self.assertEqual(doc["sites"], {"group": {}})
            self.assertEqual(sorted(doc["ai_referrals"]), ["2026-09", "2026-10", "2026-11"])
            self.assertEqual(json.load(open(base))["ai_referrals"].keys(), {"2026-09"})  # input untouched

    def test_not_in_ai_answers_shape(self):
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "o.json")
            ar.main(["--month", "2026-10", "--out", out], run=fake_run(), today=TODAY)
            doc = json.load(open(out))
            self.assertIn("ai_referrals", doc)
            self.assertNotIn("ai_answers", doc)

    def test_bad_month_writes_nothing(self):
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "o.json")
            rc = ar.main(["--month", "nope", "--out", out], run=fake_run(), today=TODAY)
            self.assertEqual(rc, 1)
            self.assertFalse(os.path.exists(out))

    def test_only_aggregate_calls(self):
        run = fake_run()
        ar.pull_month("2026-10", run, TODAY)
        dims = {c[2] for c in run.calls}
        self.assertEqual(len(dims), 3)
        for d in dims:
            self.assertNotIn("userPseudoId", d)


if __name__ == "__main__":
    unittest.main()
