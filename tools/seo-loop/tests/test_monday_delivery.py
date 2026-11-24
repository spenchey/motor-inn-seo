"""Tests for the Monday refresh and the Monday delivery. No network, no Slack, no real CRM."""
from __future__ import annotations

import contextlib
import datetime as dt
import io
import json
import os
import shutil
import sqlite3
import sys
import tempfile
import unittest

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PKG)

import ai_referrals  # noqa: E402
import monday_refresh as mr  # noqa: E402
import send_monday_summary as sm  # noqa: E402

FIX = os.path.join(PKG, "tests", "fixtures")
NV = "not verified"


def ga4_stub(fail=False, empty=False):
    """Stand-in for the Google Analytics reader: answers the leads pull and the AI pulls."""
    def run(start, end, dims, metrics):
        if fail:
            raise ai_referrals.AiReferralError("GA4 reader failed: boom")
        if dims == ["eventName", "sessionDefaultChannelGroup", "hostName"]:
            if empty:
                return []
            return [
                {"eventName": "asc_form_submission", "sessionDefaultChannelGroup": "Organic Search",
                 "hostName": "www.motorinnautogroup.com", "eventCount": 6},
                {"eventName": "asc_click_to_call", "sessionDefaultChannelGroup": "Organic Search",
                 "hostName": "www.motorinnautogroup.com", "eventCount": 3},
                {"eventName": "asc_click_to_call", "sessionDefaultChannelGroup": "Direct",
                 "hostName": "www.motorinnautogroup.com", "eventCount": 50},
            ]
        if dims == ["sessionSource", "sessionMedium"]:
            return [{"sessionSource": "chatgpt.com", "sessionMedium": "referral", "sessions": 4}]
        if dims == ["sessionSource", "eventName"]:
            return [{"sessionSource": "chatgpt.com", "eventName": "asc_form_submission", "eventCount": 1}]
        return [{"sessionSource": "chatgpt.com", "landingPagePlusQueryString": "/x", "sessions": 4}]
    return run


def gsc_stub(chevy_fails=True, all_fail=False):
    def run(site, start, end):
        if all_fail or (chevy_fails and "motorinnofcarroll" in site):
            raise mr.ReaderError("403")
        return 500 if "toyota" in site else 900
    return run


def crm_stub(value=7):
    def run(start, end):
        if value is None:
            raise mr.ReaderError("CRM capture is older than 48 hours")
        return value
    return run


class MonthMath(unittest.TestCase):
    def test_normal_monday_is_this_month(self):
        self.assertEqual(mr.month_text(mr.reporting_month(dt.date(2026, 11, 30))), "2026-11")
        self.assertEqual(mr.leads_window(dt.date(2026, 11, 30)), (dt.date(2026, 11, 1), dt.date(2026, 11, 29)))

    def test_december_seventh_builds_december(self):
        self.assertEqual(mr.month_text(mr.reporting_month(dt.date(2026, 12, 7))), "2026-12")
        self.assertEqual(mr.leads_window(dt.date(2026, 12, 7)), (dt.date(2026, 12, 1), dt.date(2026, 12, 6)))

    def test_first_of_month_monday_refreshes_last_month(self):
        for today, month, end in ((dt.date(2027, 2, 1), "2027-01", dt.date(2027, 1, 31)),
                                  (dt.date(2027, 3, 1), "2027-02", dt.date(2027, 2, 28)),
                                  (dt.date(2027, 1, 1), "2026-12", dt.date(2026, 12, 31))):
            self.assertEqual(mr.month_text(mr.reporting_month(today)), month)
            self.assertEqual(mr.leads_window(today)[1], end)

    def test_previous_month_wraps_the_year(self):
        self.assertEqual(mr.previous_month((2027, 1)), (2026, 12))

    def test_search_console_window_is_28_days_ending_three_days_back(self):
        start, end = mr.gsc_window(dt.date(2026, 11, 30))
        self.assertEqual(end, dt.date(2026, 11, 27))
        self.assertEqual((end - start).days, 27)


class RefreshRun(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.root = self.tmp
        os.makedirs(os.path.join(self.root, "findings", "baselines"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def go(self, today, ga4=None, gsc=None, crm=None):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code, problems = mr.run_refresh(self.root, today, ga4 or ga4_stub(), gsc or gsc_stub(),
                                            crm or crm_stub(), "unused")
        return code, problems

    def baseline(self, month):
        with open(os.path.join(self.root, "findings", "baselines", "%s.json" % month)) as fh:
            return json.load(fh)

    def test_good_run_builds_numbers_and_ai_blocks(self):
        code, problems = self.go(dt.date(2026, 12, 7))
        b = self.baseline("2026-12")
        self.assertEqual(b["organic_leads_total"]["value"], 9)  # direct traffic is not counted
        self.assertEqual(b["crm_website_leads"]["value"], 7)
        self.assertEqual(b["sites"]["group"]["gsc_clicks_28d"]["value"], 900)
        self.assertEqual(b["sites"]["toyota"]["gsc_clicks_28d"]["value"], 500)
        self.assertEqual(b["sites"]["chevy"]["gsc_clicks_28d"], NV)
        self.assertEqual(sorted(b["ai_referrals"]), ["2026-11", "2026-12"])  # this month and last month
        self.assertEqual(b["ai_referrals"]["2026-12"]["sessions"]["value"], 4)
        self.assertTrue(any("chevy" in p for p in problems))  # the 403 is logged
        self.assertEqual(code, 1)

    def test_rollover_does_not_touch_the_old_month_file(self):
        self.go(dt.date(2026, 11, 30))
        before = json.dumps(self.baseline("2026-11"), sort_keys=True)
        self.go(dt.date(2026, 12, 7))
        self.assertEqual(json.dumps(self.baseline("2026-11"), sort_keys=True), before)
        self.assertTrue(os.path.exists(os.path.join(self.root, "findings", "baselines", "2026-12.json")))

    def test_first_of_month_skips_the_new_month(self):
        self.go(dt.date(2027, 2, 1))
        names = sorted(n for n in os.listdir(os.path.join(self.root, "findings", "baselines")) if n.endswith(".json"))
        self.assertEqual(names, ["2027-01.json"])
        self.assertEqual(sorted(self.baseline("2027-01")["ai_referrals"]), ["2026-12", "2027-01"])

    def test_google_analytics_failure_is_not_verified_never_zero(self):
        code, problems = self.go(dt.date(2026, 12, 7), ga4=ga4_stub(fail=True))
        b = self.baseline("2026-12")
        self.assertEqual(b["organic_leads_total"], NV)
        self.assertEqual(b["sites"]["group"]["organic_leads"], NV)
        self.assertEqual(b["ai_referrals"]["2026-12"]["sessions"], NV)
        self.assertEqual(b["crm_website_leads"]["value"], 7)  # the CRM number is independent
        self.assertEqual(code, 1)
        self.assertTrue(problems)

    def test_empty_google_analytics_pull_is_not_a_zero(self):
        self.go(dt.date(2026, 12, 7), ga4=ga4_stub(empty=True))
        self.assertEqual(self.baseline("2026-12")["organic_leads_total"], NV)

    def test_stale_input_is_never_reused_after_a_failure(self):
        self.go(dt.date(2026, 12, 7))
        self.go(dt.date(2026, 12, 7), ga4=ga4_stub(fail=True), gsc=gsc_stub(all_fail=True), crm=crm_stub(None))
        b = self.baseline("2026-12")
        self.assertEqual(b["organic_leads_total"], NV)
        self.assertEqual(b["crm_website_leads"], NV)
        self.assertEqual(b["sites"]["group"]["gsc_clicks_28d"], NV)
        self.assertEqual(b["sites"]["toyota"]["gsc_clicks_28d"], NV)

    def test_dry_run_writes_nothing(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code, problems = mr.run_refresh(self.root, dt.date(2026, 12, 7), None, None, None, "x", dry_run=True)
        self.assertEqual((code, problems), (0, []))
        self.assertEqual(os.listdir(os.path.join(self.root, "findings", "baselines")), [])

    def test_real_run_refuses_today_override(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(mr.main(["--root", self.root, "--today", "2026-12-07"]), 2)


class CrmCount(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.db = os.path.join(self.tmp, "leads.db")
        con = sqlite3.connect(self.db)
        con.execute("create table crm_opportunity (opportunity_id text, created_date text)")
        con.execute("create table lead_source (opportunity_id text, channel_class text, fetched_at text)")
        rows = [
            ("a", "2026-11-03T15:00:00.1234567+00:00", "owned_web"),
            ("b", "2026-11-30T02:30:00.0000000+00:00", "owned_web"),   # 8:30 pm Central on Nov 29: inside
            ("c", "2026-12-01T04:00:00.0000000+00:00", "owned_web"),   # Nov 30 10 pm Central: outside Nov 1..29
            ("d", "2026-11-04T10:00:00+00:00", "walk_in"),
            ("e", "2026-11-05T09:00:00", "owned_web"),                 # no offset: Central
            ("f", "2026-11-06T15:00:00.12+00:00", "owned_web"),        # two-digit fraction
            ("g", "2026-11-07T15:00:00.5+00:00", "owned_web"),         # one-digit fraction
        ]
        for oid, created, cls in rows:
            con.execute("insert into crm_opportunity values (?, ?)", (oid, created))
            con.execute("insert into lead_source values (?, ?, ?)", (oid, cls, "2026-11-30T12:00:00Z"))
        con.commit()
        con.close()
        self.now = dt.datetime(2026, 11, 30, 13, 0, tzinfo=dt.timezone.utc)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_counts_by_central_date(self):
        run = mr.crm_count_reader(self.db, now=self.now)
        self.assertEqual(run(dt.date(2026, 11, 1), dt.date(2026, 11, 29)), 5)  # a, b, e, f, g

    def test_stale_capture_is_refused(self):
        run = mr.crm_count_reader(self.db, now=self.now + dt.timedelta(days=5))
        with self.assertRaises(mr.ReaderError):
            run(dt.date(2026, 11, 1), dt.date(2026, 11, 29))

    def test_unplaceable_date_is_refused_not_undercounted(self):
        con = sqlite3.connect(self.db)
        con.execute("insert into crm_opportunity values ('z', '11/05/2026 3:00 PM')")
        con.execute("insert into lead_source values ('z', 'owned_web', '2026-11-30T12:00:00Z')")
        con.commit()
        con.close()
        with self.assertRaises(mr.ReaderError):
            mr.crm_count_reader(self.db, now=self.now)(dt.date(2026, 11, 1), dt.date(2026, 11, 29))

    def test_missing_database_is_refused(self):
        with self.assertRaises(mr.ReaderError):
            mr.crm_count_reader(os.path.join(self.tmp, "nope.db"))(dt.date(2026, 11, 1), dt.date(2026, 11, 2))

    def test_database_is_opened_read_only(self):
        before = os.path.getmtime(self.db)
        mr.crm_count_reader(self.db, now=self.now)(dt.date(2026, 11, 1), dt.date(2026, 11, 29))
        self.assertEqual(os.path.getmtime(self.db), before)


SENDER = '''
import json, os
def resolve_token():
    open(os.environ["STUB_LOG"], "a").write("TOKEN LOOKED UP\\n")
    return "stub-token"
def post_dm(text, user=None, token=None, call=None):
    if os.environ.get("STUB_FAIL"):
        raise RuntimeError("SLACK_API_ERROR: nope")
    open(os.environ["STUB_LOG"], "a").write("DM to %s: %s\\n" % (user, text))
    return {"channel": "D1", "ts": "1.2"}
'''


class Delivery(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        f = os.path.join(self.tmp, "findings")
        for d in ("baselines", "logs", "summaries"):
            os.makedirs(os.path.join(f, d))
        shutil.copy(os.path.join(FIX, "register.jsonl"), os.path.join(f, "register.jsonl"))
        shutil.copy(os.path.join(FIX, "b.json"), os.path.join(f, "baselines", "2026-11.json"))
        self.sender = os.path.join(self.tmp, "sender.py")
        with open(self.sender, "w") as fh:
            fh.write(SENDER)
        self.cfg = os.path.join(self.tmp, "cfg.json")
        with open(self.cfg, "w") as fh:
            json.dump({"slack_user_id": "UTEST", "slack_sender_path": self.sender}, fh)
        self.stublog = os.path.join(self.tmp, "stub.log")
        os.environ["STUB_LOG"] = self.stublog
        os.environ.pop("STUB_FAIL", None)

    def tearDown(self):
        os.environ.pop("STUB_FAIL", None)
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_main(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = sm.main(["--root", self.tmp, "--config", self.cfg] + list(args))
        return code, out.getvalue(), err.getvalue()

    def stub_calls(self):
        return open(self.stublog).read() if os.path.exists(self.stublog) else ""

    def test_dry_run_prints_and_never_touches_the_sender(self):
        code, out, _ = self.run_main("--dry-run", "--today", "2026-11-30")
        self.assertEqual(code, 0)
        self.assertIn("Motor Inn search", out)
        self.assertEqual(self.stub_calls(), "")
        self.assertEqual(os.listdir(os.path.join(self.tmp, "findings", "summaries")), [])

    def test_dry_run_can_copy_its_text_out(self):
        target = os.path.join(self.tmp, "preview.md")
        self.run_main("--dry-run", "--today", "2026-11-30", "--dry-run-out", target)
        self.assertIn("Motor Inn search", open(target).read())

    def test_rollover_dry_run_falls_back_with_a_note(self):
        code, out, _ = self.run_main("--dry-run", "--today", "2026-12-07")
        self.assertEqual(code, 0)
        self.assertIn("file has not been built yet", out)
        self.assertFalse(os.path.exists(os.path.join(self.tmp, "findings", "baselines", "2026-12.json")))

    def on(self, year, month, day, *args):
        """Run main with the wall clock pinned to a date."""
        real = sm.dt.date

        class Pinned(real):
            @classmethod
            def today(cls):
                return real(year, month, day)
        sm.dt.date = Pinned
        try:
            return self.run_main(*args)
        finally:
            sm.dt.date = real

    def test_refuses_to_send_when_it_is_not_monday(self):
        code, _, err = self.on(2026, 11, 24)
        self.assertEqual(code, 3)
        self.assertIn("not Monday", err)
        self.assertEqual(self.stub_calls(), "")

    def test_force_sends_on_any_day_and_saves_the_file(self):
        code, out, _ = self.run_main("--force")
        self.assertEqual(code, 0)
        self.assertIn("DM to UTEST", self.stub_calls())
        day = dt.date.today().isoformat()
        self.assertTrue(os.path.exists(os.path.join(self.tmp, "findings", "summaries", "summary-%s.txt" % day)))

    def test_today_without_dry_run_needs_force(self):
        code, _, err = self.run_main("--today", "2026-11-30")
        self.assertEqual(code, 2)
        self.assertEqual(self.stub_calls(), "")

    def test_second_send_same_day_is_refused(self):
        self.assertEqual(self.on(2026, 11, 30)[0], 0)  # a real Monday send, no --force
        code, _, err = self.on(2026, 11, 30)
        self.assertEqual(code, 3)
        self.assertIn("already sent", err)
        self.assertEqual(self.stub_calls().count("DM to UTEST"), 1)

    def test_render_failure_sends_the_one_line_notice(self):
        os.remove(os.path.join(self.tmp, "findings", "register.jsonl"))
        code, _, err = self.run_main("--force")
        self.assertEqual(code, 1)
        self.assertIn(sm.FAILED_LINE, self.stub_calls())
        self.assertIn("could not be made", err)

    def test_dm_failure_is_loud_and_logged(self):
        os.environ["STUB_FAIL"] = "1"
        code, _, err = self.run_main("--force")
        self.assertEqual(code, 1)
        self.assertIn("DM NOT SENT", err)
        self.assertIn("did not reach Spencer", open(os.path.join(self.tmp, "findings", "logs", "summary.log")).read())

    def test_missing_config_is_loud_not_silent(self):
        os.remove(self.cfg)
        code, _, err = self.run_main("--force")
        self.assertEqual(code, 1)
        self.assertIn("DM NOT SENT", err)

    def test_stale_numbers_get_a_note_on_a_real_run(self):
        base = os.path.join(self.tmp, "findings", "baselines", "%s.json" % sm.reporting_month(dt.date.today()))
        shutil.copy(os.path.join(FIX, "b.json"), base)
        old = dt.datetime(2026, 1, 5).timestamp()
        os.utime(base, (old, old))
        code, _, _ = self.run_main("--force")
        self.assertIn("were not refreshed this morning (last refreshed 1/5)", self.stub_calls())


if __name__ == "__main__":
    unittest.main()
