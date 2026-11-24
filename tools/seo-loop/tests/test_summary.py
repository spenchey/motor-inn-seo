from __future__ import annotations

import copy
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PKG)

import monday_summary  # noqa: E402
import register  # noqa: E402

FIX = os.path.join(PKG, "tests", "fixtures")
REG = os.path.join(FIX, "register.jsonl")
BASE = os.path.join(FIX, "b.json")
TODAY = "2026-11-18"

NASTY_TITLES = [
    "Fix F-toyota-meta-noindex-f41ae2 now",
    "See reports/site-watch-2026-11-16.md for detail",
    "Edit /Us" "ers/someone/Glyph/scratch/register.jsonl",
    "status waiting_spencer needs verify_pending",
    "The meta-noindex check fails on the new page",
    "run build.py then open notes.md",
    "pending-spencer ruling on the phone",
]
CHECK_IDS = ["meta-noindex", "title-leads-other-city", "gbp-phone-differs", "faq-schema-missing"]


def run_main(register_path, baselines_path, *extra):
    out = io.StringIO()
    err = io.StringIO()
    old = sys.stderr
    sys.stderr = err
    try:
        rc = monday_summary.main(["--register", register_path, "--baselines", baselines_path,
                                  "--today", TODAY] + list(extra), out)
    finally:
        sys.stderr = old
    return rc, out.getvalue(), err.getvalue()


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def sample_rows():
    return register.load_rows(REG)


def write_rows(rows, directory, name="reg.jsonl"):
    path = os.path.join(directory, name)
    with open(path, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    return path


def big_rows(n=200):
    base = sample_rows()
    rows = []
    for i in range(n):
        r = copy.deepcopy(base[i % len(base)])
        r["id"] = "F-x-%d" % i
        r["tier"] = 1 + (i % 4)
        r["first_seen"] = "2026-%02d-%02d" % (9 + (i % 3), 1 + (i % 27))
        title = NASTY_TITLES[i % len(NASTY_TITLES)] if i % 2 == 0 else "word " * 150
        r["title"] = title
        r["check_id"] = CHECK_IDS[i % len(CHECK_IDS)]
        if i % 3 == 0:
            r["status"] = "waiting_spencer"
            r["next_action"] = "Spencer to OK F-toyota-meta-noindex-f41ae2 in reports/x.md " + "long " * 80
        rows.append(r)
    return rows


class SummaryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def banned_scan(self, text):
        self.assertNotRegex(text, r"\bF-")
        for bad in (".jsonl", ".md", ".py", "/Us" "ers", "waiting_spencer", "verify_pending",
                    "packet_ready", "verified_fixed", "dealeron_request", "spencer_decision",
                    "pending-spencer", "internal_repair", "wont_fix"):
            self.assertNotIn(bad, text)
        for cid in CHECK_IDS:
            self.assertNotIn(cid, text)

    def test_200_rows_under_300_words(self):
        path = write_rows(big_rows(200), self.tmp)
        rc, out, _ = run_main(path, BASE)
        self.assertEqual(rc, 0)
        self.assertLess(len(out.split()), 300)

    def test_never_more_than_three_asks(self):
        path = write_rows(big_rows(200), self.tmp)
        _, out, _ = run_main(path, BASE)
        asks = [l for l in out.splitlines() if l.startswith("ASK ")]
        self.assertEqual(len(asks), 3)
        self.assertEqual([a[:6] for a in asks], ["ASK 1:", "ASK 2:", "ASK 3:"])

    def test_empty_register(self):
        path = write_rows([], self.tmp)
        rc, out, _ = run_main(path, BASE)
        self.assertEqual(rc, 0)
        self.assertFalse([l for l in out.splitlines() if l.startswith("ASK")])
        self.assertIn("Open now: 0.", out)
        self.assertIn("Waiting on DealerOn: 0.", out)

    def test_missing_baseline_prints_not_verified(self):
        rc, out, _ = run_main(REG, os.path.join(FIX, "b_missing.json"))
        self.assertEqual(rc, 0)
        self.assertGreaterEqual(out.count("not verified"), 4)
        self.assertIn("Not verified this week: Google Search Console, organic lead count, our CRM website leads, "
                      "Google Business reviews and activity, AI answers, AI assistant visits.", out)
        self.assertNotRegex(out, r"group 0\b")

    def test_full_baseline_has_numbers_and_sources(self):
        _, out, _ = run_main(REG, BASE)
        self.assertIn("Google Search Console", out)
        self.assertIn("group 1,840", out)
        self.assertIn("Toyota site 1,100", out)
        self.assertIn("Chevrolet site 740", out)
        self.assertIn("Organic leads from Google search, counted as form sends and phone taps in Google Analytics: 37", out)
        self.assertNotIn("Organic leads from Google Analytics", out)
        # b.json has no review figures and an unverified AI answers entry.
        self.assertIn("Not verified this week: Google Business reviews and activity, AI answers, AI assistant visits.", out)

    def test_fully_verified_baseline_has_no_not_verified_line(self):
        _, out, _ = run_main(REG, os.path.join(FIX, "b_full.json"))
        self.assertNotIn("Not verified this week", out)
        self.assertNotIn("not verified", out)
        self.assertIn("Organic leads from Google search, counted as form sends and phone taps in Google Analytics: 37.", out)

    def _no_tier1_register(self):
        rows = sample_rows()
        for r in rows:
            if r.get("tier") == 1:
                r["tier"] = 2
        return write_rows(rows, self.tmp, "t2.jsonl")

    def test_all_not_verified_with_serious_problem_open(self):
        _, out, _ = run_main(REG, os.path.join(FIX, "b_all_nv.json"))
        self.assertIn("A serious problem on a main page is still open. "
                      "The traffic and lead numbers are not available yet.", out.splitlines()[0])

    def test_all_not_verified_fixture(self):
        _, out, _ = run_main(self._no_tier1_register(), os.path.join(FIX, "b_all_nv.json"))
        lines = out.splitlines()
        self.assertIn("Organic leads from Google search, counted as form sends and phone taps in Google Analytics: not verified.", out)
        self.assertNotIn("Organic leads from Google Analytics", out)
        self.assertNotIn("Mostly steady", out)
        self.assertNotIn("All clear", out)
        self.assertIn("not available yet", lines[0])
        last = lines[-1]
        for name in ("Google Search Console", "Google Analytics", "organic lead count",
                     "Google Business reviews and activity", "AI answers"):
            self.assertIn(name, last)
        self.assertNotRegex(last, r"\.json|gbp|ga4|gsc|leads_|ai_answers|/")
        self.assertLess(len(out.split()), 300)
        self.assertLessEqual(len([l for l in lines if l.startswith("ASK ")]), 3)

    def test_mixed_fixture_search_console_verified_others_not(self):
        _, out, _ = run_main(self._no_tier1_register(), os.path.join(FIX, "b_mixed.json"))
        lines = out.splitlines()
        self.assertIn("group 1,840", out)
        self.assertIn("Organic leads from Google search, counted as form sends and phone taps in Google Analytics: not verified.", out)
        last = lines[-1]
        self.assertTrue(last.startswith("Not verified this week:"))
        self.assertNotIn("Google Search Console", last)
        for name in ("Google Analytics", "organic lead count",
                     "Google Business reviews and activity", "AI answers"):
            self.assertIn(name, last)
        # one verified traffic number means the verdict is not replaced
        self.assertNotIn("not available yet", lines[0])
        self.assertIn("Mostly steady", lines[0])

    def test_verdict_steady_kept_when_numbers_verified(self):
        _, out, _ = run_main(REG, BASE)
        self.assertNotIn("not available yet", out)

    def test_body_has_no_ids_paths_or_status_codes(self):
        path = write_rows(big_rows(200), self.tmp)
        _, out, _ = run_main(path, BASE)
        self.banned_scan(out)
        _, out2, _ = run_main(REG, BASE)
        self.banned_scan(out2)

    def test_worst_case_still_readable(self):
        rows = sample_rows()[:1]
        rows[0]["title"] = "F-toyota-meta-noindex-f41ae2"
        rows[0]["next_action"] = "reports/site-watch.md waiting_spencer"
        path = write_rows(rows, self.tmp)
        _, out, _ = run_main(path, BASE)
        self.banned_scan(out)
        ask = [l for l in out.splitlines() if l.startswith("ASK 1:")][0]
        self.assertIn("Toyota site", ask)
        self.assertIn("Please take a look", ask)

    def test_asks_in_tier_then_age_order(self):
        rows = sample_rows()
        rc, out, _ = run_main(REG, BASE)
        want = register.asks(rows, 3, TODAY)
        got = [l for l in out.splitlines() if l.startswith("ASK ")]
        self.assertEqual(len(got), len(want))
        self.assertEqual(want[0]["tier"], 1)
        self.assertIn("New inventory page", got[0])
        self.assertIn("Chevrolet listing shows a different phone", got[1])
        self.assertIn("sitemap", got[2].lower())
        tiers = [r["tier"] for r in want]
        self.assertEqual(tiers, sorted(tiers))

    def test_age_order_inside_a_tier(self):
        base = sample_rows()[0]
        rows = []
        for i, (title, fs) in enumerate([("Younger problem", "2026-11-10"), ("Older problem", "2026-10-01"),
                                         ("Middle problem", "2026-10-20")]):
            r = copy.deepcopy(base)
            r["id"] = "F-t-%d" % i
            r["title"] = title
            r["first_seen"] = fs
            r["tier"] = 2
            rows.append(r)
        path = write_rows(rows, self.tmp)
        _, out, _ = run_main(path, BASE)
        asks = [l for l in out.splitlines() if l.startswith("ASK ")]
        self.assertIn("Older problem", asks[0])
        self.assertIn("Middle problem", asks[1])
        self.assertIn("Younger problem", asks[2])

    def test_register_unchanged(self):
        path = write_rows(big_rows(50), self.tmp)
        before = sha(path)
        before_dir = sorted(os.listdir(self.tmp))
        run_main(path, BASE)
        self.assertEqual(before, sha(path))
        self.assertEqual(before_dir, sorted(os.listdir(self.tmp)))
        b2 = sha(REG)
        run_main(REG, BASE)
        self.assertEqual(b2, sha(REG))

    def test_missing_or_unreadable_files_exit_1(self):
        rc, out, err = run_main(os.path.join(self.tmp, "nope.jsonl"), BASE)
        self.assertEqual((rc, out), (1, ""))
        self.assertTrue(err.strip())
        rc, out, _ = run_main(REG, os.path.join(self.tmp, "nope.json"))
        self.assertEqual((rc, out), (1, ""))
        bad = os.path.join(self.tmp, "bad.json")
        with open(bad, "w") as fh:
            fh.write("{not json")
        rc, out, _ = run_main(REG, bad)
        self.assertEqual((rc, out), (1, ""))
        badreg = os.path.join(self.tmp, "bad.jsonl")
        with open(badreg, "w") as fh:
            fh.write("{not json\n")
        rc, out, _ = run_main(badreg, BASE)
        self.assertEqual((rc, out), (1, ""))

    def test_dealeron_waiting_count_and_oldest_date(self):
        base = sample_rows()[0]
        rows = []
        for i, (st, at) in enumerate([("sent", "2026-11-12"), ("verify_pending", "2026-11-05"),
                                      ("sent", "2026-11-16"), ("packet_ready", None)]):
            r = copy.deepcopy(base)
            r["id"] = "F-d-%d" % i
            r["fix_type"] = "dealeron_request"
            r["status"] = st
            r["sent"] = {"at": at, "how": "x"} if at else None
            rows.append(r)
        other = copy.deepcopy(base)
        other["id"] = "F-d-9"
        other["fix_type"] = "gbp_edit"
        other["status"] = "sent"
        other["sent"] = {"at": "2026-10-01", "how": "x"}
        rows.append(other)
        path = write_rows(rows, self.tmp)
        _, out, _ = run_main(path, BASE)
        self.assertIn("Waiting on DealerOn: 3, oldest sent November 5.", out)

    def test_fixed_this_week_and_new_and_oldest(self):
        base = sample_rows()[0]
        fixed_in = copy.deepcopy(base)
        fixed_in.update(id="F-a", status="verified_fixed", next_action=None, next_action_owner=None,
                        next_action_due=None,
                        verified={"at": "2026-11-17", "evidence_path": "x",
                                  "passes": [{"at": "2026-11-15T10:00:00Z", "passed": True},
                                             {"at": "2026-11-17T10:00:00Z", "passed": True}]})
        fixed_old = copy.deepcopy(fixed_in)
        fixed_old.update(id="F-b", verified={"at": "2026-10-01", "evidence_path": "x",
                                             "passes": [{"at": "2026-10-01T10:00:00Z", "passed": True}]})
        new_row = copy.deepcopy(base)
        new_row.update(id="F-c", first_seen="2026-11-14", status="triaged", fix_type="content_draft")
        old_row = copy.deepcopy(base)
        old_row.update(id="F-d", first_seen="2026-10-09", status="triaged", fix_type="content_draft")
        path = write_rows([fixed_in, fixed_old, new_row, old_row], self.tmp)
        _, out, _ = run_main(path, BASE)
        self.assertIn("since last week: 1.", out)
        self.assertIn("New this week: 1. Open now: 2. Oldest open problem: 40 days.", out)

    def test_heading_and_week_start(self):
        _, out, _ = run_main(REG, BASE)
        self.assertTrue(out.startswith("Motor Inn search, week of November 12."))
        _, out, _ = run_main(REG, BASE, "--week-start", "2026-11-16")
        self.assertTrue(out.startswith("Motor Inn search, week of November 16."))

    def test_previous_baselines_trend(self):
        _, out, _ = run_main(REG, BASE, "--previous-baselines", os.path.join(FIX, "b_prev.json"))
        self.assertIn("Google clicks are up 15% on the last check.", out.splitlines()[0])

    def test_all_clear_when_no_open(self):
        base = sample_rows()[0]
        r = copy.deepcopy(base)
        r.update(status="wont_fix", next_action=None, next_action_owner=None, next_action_due=None)
        path = write_rows([r], self.tmp)
        _, out, _ = run_main(path, BASE)
        self.assertIn("All clear.", out)
        self.assertIn("Nothing needs you this week.", out)

    def _one_ask(self, next_action):
        r = sample_rows()[0]
        r["next_action"] = next_action
        path = write_rows([r], self.tmp)
        _, out, _ = run_main(path, BASE)
        return [l for l in out.splitlines() if l.startswith("ASK 1:")][0]

    def test_iso_date_in_next_action_keeps_meaning(self):
        ask = self._one_ask("Spencer to OK the DealerOn request by 2026-11-23")
        self.assertIn("Please OK the DealerOn request by November 23", ask)
        self.assertNotIn("Please take a look", ask)
        self.assertNotIn("2026-11-23", ask)

    def test_check_id_in_next_action_still_falls_back(self):
        ask = self._one_ask("Spencer to OK the meta-noindex fix by 2026-11-23")
        self.assertIn("Please take a look when you can", ask)
        self.assertNotIn("meta-noindex", ask)
        ask = self._one_ask("Handle F-toyota-meta-noindex-f41ae2 by 2026-11-23")
        self.assertIn("Please take a look when you can", ask)

    def test_s7_card_and_package_codes_use_fallback(self):
        ask = self._one_ask("Spencer to approve SC-02 per MOT-3612 before the SA-14 cutover")
        for code in ("SC-02", "MOT-3612", "SA-14"):
            self.assertNotIn(code, ask)
        self.assertIn("Please take a look when you can", ask)

    def test_s7_email_and_other_phone_use_fallback(self):
        fake = lambda a, b, c, sep="-": sep.join((a, b, c))  # fictional numbers, built so none is written out
        for text in ("Please call Jane Doe at (%s) %s %s about her complaint" % ("515", "555", "0142"),
                     "Write to jane.doe@example.com about it",
                     "Call %s today" % fake("712", "555", "0100"), "Call %s today" % fake("515", "555", "0142", ".")):
            ask = self._one_ask(text)
            self.assertIn("Please take a look when you can", ask, text)
            self.assertNotRegex(ask, r"555|@")

    def test_s7_our_own_phone_is_allowed(self):
        ask = self._one_ask("Please confirm the listing shows 712-792-5000")
        self.assertIn("712-792-5000", ask)
        self.assertNotIn("Please take a look", ask)

    def test_s8_leads_use_total_not_group(self):
        path = os.path.join(self.tmp, "b.json")
        data = {"sites": {"group": {"gsc_clicks_28d": {"value": 100}, "organic_leads": {"value": 3}}},
                "organic_leads_total": {"value": 47}}
        with open(path, "w") as fh:
            json.dump(data, fh)
        _, out, _ = run_main(REG, path)
        self.assertIn("in Google Analytics: 47.", out)
        self.assertNotIn("in Google Analytics: 3.", out)

    def test_s8_missing_total_is_not_verified_even_with_group_number(self):
        path = os.path.join(self.tmp, "b.json")
        data = {"sites": {"group": {"organic_leads": {"value": 3}}}}
        with open(path, "w") as fh:
            json.dump(data, fh)
        _, out, _ = run_main(REG, path)
        self.assertIn("in Google Analytics: not verified.", out)
        self.assertIn("Not verified this week:", out)
        self.assertIn("organic lead count", out.splitlines()[-1])

    def test_n2_empty_register_is_not_good_news(self):
        path = write_rows([], self.tmp)
        _, out, _ = run_main(path, BASE)
        self.assertIn("No findings are on record, so this report cannot confirm the sites are healthy.", out)
        self.assertNotIn("All clear", out)
        self.assertNotIn("Nothing needs you this week.", out)

    def test_n2_nothing_needs_you_only_when_findings_exist(self):
        r = sample_rows()[0]
        r.update(status="wont_fix", next_action=None, next_action_owner=None, next_action_due=None)
        path = write_rows([r], self.tmp)
        _, out, _ = run_main(path, BASE)
        self.assertIn("Nothing needs you this week.", out.splitlines())
        self.assertNotIn("No findings are on record", out)

    def test_cli_runs_isolated_from_other_folder(self):
        script = os.path.join(PKG, "monday_summary.py")
        res = subprocess.run([sys.executable, "-I", script, "--register", REG, "--baselines", BASE,
                              "--today", TODAY], cwd="/", stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             universal_newlines=True)
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn("Motor Inn search, week of", res.stdout)
        self.assertLess(len(res.stdout.split()), 300)

    def test_no_send_code_in_source(self):
        with open(os.path.join(PKG, "monday_summary.py"), encoding="utf-8") as fh:
            src = fh.read().lower()
        for word in ("smtplib", "sendmail", "slack", "mailchimp", "curl", "urllib", "socket", "subprocess"):
            self.assertNotIn(word, src)


if __name__ == "__main__":
    unittest.main()
