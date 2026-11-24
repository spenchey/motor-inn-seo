from __future__ import annotations

import copy
import io
import json
import os
import sys
import tempfile
import unittest

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PKG)

import baseline  # noqa: E402
import build_leads_input as bli  # noqa: E402
import monday_summary  # noqa: E402
import register  # noqa: E402

FIX = os.path.join(PKG, "tests", "fixtures")
REG = os.path.join(FIX, "register.jsonl")
TODAY = "2026-11-30"
PULLED = "2026-11-24T13:00:00Z"


def metric(value, window="2026-11-01..2026-11-22"):
    return {"value": value, "window": window, "source": "test", "pulled_at": PULLED}


def run(register_path, baselines_path):
    out, err = io.StringIO(), io.StringIO()
    old, sys.stderr = sys.stderr, err
    try:
        rc = monday_summary.main(["--register", register_path, "--baselines", baselines_path, "--today", TODAY], out)
    finally:
        sys.stderr = old
    return rc, out.getvalue(), err.getvalue()


def write(path, data):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh)


class RolloverTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def _base(self, month_value):
        return {"month": "x", "sites": {}, "listings": {},
                "organic_leads_total": metric(month_value), "crm_website_leads": metric(30)}

    def test_missing_month_uses_newest_earlier_file_and_says_so(self):
        write(os.path.join(self.tmp, "2026-09.json"), self._base(3))
        write(os.path.join(self.tmp, "2026-10.json"), self._base(5))
        rc, out, _ = run(REG, os.path.join(self.tmp, "2026-12.json"))
        self.assertEqual(rc, 0)
        self.assertIn("in Google Analytics: 5 ", out)
        self.assertIn("The numbers above come from the October 2026 file; the December 2026 file has not been built yet.", out)

    def test_never_uses_a_later_month(self):
        write(os.path.join(self.tmp, "2027-01.json"), self._base(99))
        rc, out, err = run(REG, os.path.join(self.tmp, "2026-12.json"))
        self.assertEqual(rc, 1)
        self.assertEqual(out, "")

    def test_year_boundary_picks_december_for_january(self):
        write(os.path.join(self.tmp, "2026-12.json"), self._base(8))
        rc, out, _ = run(REG, os.path.join(self.tmp, "2027-01.json"))
        self.assertEqual(rc, 0)
        self.assertIn("December 2026 file; the January 2027 file", out)

    def test_existing_month_file_has_no_fallback_note(self):
        write(os.path.join(self.tmp, "2026-11.json"), self._base(9))
        write(os.path.join(self.tmp, "2026-10.json"), self._base(5))
        rc, out, _ = run(REG, os.path.join(self.tmp, "2026-11.json"))
        self.assertEqual(rc, 0)
        self.assertNotIn("has not been built yet", out)
        self.assertIn("in Google Analytics: 9 (November 1 to November 22)", out)

    def test_no_earlier_file_still_refuses(self):
        rc, out, err = run(REG, os.path.join(self.tmp, "2026-11.json"))
        self.assertEqual(rc, 1)
        self.assertEqual(out, "")
        self.assertIn("No summary was made", err)

    def test_odd_file_name_is_not_guessed(self):
        write(os.path.join(self.tmp, "2026-10.json"), self._base(5))
        rc, out, _ = run(REG, os.path.join(self.tmp, "latest.json"))
        self.assertEqual(rc, 1)

    def test_corrupt_fallback_file_refuses(self):
        with open(os.path.join(self.tmp, "2026-10.json"), "w") as fh:
            fh.write("{not json")
        rc, out, _ = run(REG, os.path.join(self.tmp, "2026-11.json"))
        self.assertEqual(rc, 1)

    def test_crm_line_present_and_labelled_a_ceiling(self):
        write(os.path.join(self.tmp, "2026-11.json"), self._base(9))
        _, out, _ = run(REG, os.path.join(self.tmp, "2026-11.json"))
        self.assertIn("Check against our CRM: 30 website leads (November 1 to November 22)", out)
        self.assertIn("ceiling for organic leads", out)
        self.assertNotIn("our own lead count", out)

    def test_crm_missing_says_not_verified_and_is_listed(self):
        data = self._base(9)
        del data["crm_website_leads"]
        write(os.path.join(self.tmp, "2026-11.json"), data)
        _, out, _ = run(REG, os.path.join(self.tmp, "2026-11.json"))
        self.assertIn("Check against our CRM: not verified.", out)
        self.assertIn("our CRM website leads", out.splitlines()[-1])

    def test_crm_number_never_becomes_the_headline(self):
        data = self._base(9)
        data["organic_leads_total"] = "not verified"
        write(os.path.join(self.tmp, "2026-11.json"), data)
        _, out, _ = run(REG, os.path.join(self.tmp, "2026-11.json"))
        self.assertIn("in Google Analytics: not verified.", out)

    def test_unmeasured_sites_are_named_not_zero(self):
        data = self._base(9)
        data["sites"] = {"group": {"organic_leads": metric(9)}}
        write(os.path.join(self.tmp, "2026-11.json"), data)
        _, out, _ = run(REG, os.path.join(self.tmp, "2026-11.json"))
        self.assertIn("Toyota and Chevrolet sites: not verified.", out)

    def test_fix_packets_come_first_then_other_asks_and_never_more_than_three(self):
        rows = register.load_rows(REG)
        base = rows[0]
        mk = []
        for i in range(5):
            r = copy.deepcopy(base)
            r.update(id="F-pk-%d" % i, tier=3, status="waiting_spencer", fix_type="dealeron_request",
                     title="Packet number %d" % i, next_action="Spencer to say yes or no to request %d" % i,
                     first_seen="2026-11-2%d" % i)
            mk.append(r)
        d = copy.deepcopy(base)
        d.update(id="F-dec-1", tier=2, status="triaged", fix_type="spencer_decision",
                 title="A decision that is older", next_action="Spencer to decide", first_seen="2026-10-01")
        path = os.path.join(self.tmp, "reg.jsonl")
        with open(path, "w") as fh:
            for r in [d] + mk:
                fh.write(json.dumps(r) + "\n")
        write(os.path.join(self.tmp, "2026-11.json"), self._base(9))
        _, out, _ = run(path, os.path.join(self.tmp, "2026-11.json"))
        asks = [l for l in out.splitlines() if l.startswith("ASK ")]
        self.assertEqual(len(asks), 3)
        self.assertTrue(all("Packet number" in a for a in asks), asks)
        self.assertNotIn("A decision that is older", out)

    def test_decisions_fill_the_asks_when_few_packets(self):
        rows = register.load_rows(REG)
        base = rows[0]
        p = copy.deepcopy(base)
        p.update(id="F-pk-1", tier=3, status="waiting_spencer", fix_type="dealeron_request",
                 title="Only packet", next_action="Spencer to say yes or no", first_seen="2026-11-20")
        d = copy.deepcopy(base)
        d.update(id="F-dec-1", tier=2, status="triaged", fix_type="spencer_decision",
                 title="A decision", next_action="Spencer to decide", first_seen="2026-10-01")
        path = os.path.join(self.tmp, "reg.jsonl")
        with open(path, "w") as fh:
            fh.write(json.dumps(p) + "\n" + json.dumps(d) + "\n")
        write(os.path.join(self.tmp, "2026-11.json"), self._base(9))
        _, out, _ = run(path, os.path.join(self.tmp, "2026-11.json"))
        asks = [l for l in out.splitlines() if l.startswith("ASK ")]
        self.assertEqual(len(asks), 2)
        self.assertIn("Only packet", asks[0])
        self.assertIn("A decision", asks[1])

    def test_question_and_answer_wording_is_kept_not_replaced_by_fallback(self):
        rows = register.load_rows(REG)
        r = copy.deepcopy(rows[0])
        r.update(id="F-qa-1", tier=3, status="waiting_spencer", fix_type="dealeron_request",
                 title="No question-and-answer markup on the page",
                 next_action="Spencer to say yes or no to the drafted request for question-and-answer markup on one page",
                 first_seen="2026-11-20")
        path = os.path.join(self.tmp, "reg.jsonl")
        with open(path, "w") as fh:
            fh.write(json.dumps(r) + "\n")
        write(os.path.join(self.tmp, "2026-11.json"), self._base(9))
        _, out, _ = run(path, os.path.join(self.tmp, "2026-11.json"))
        ask = [l for l in out.splitlines() if l.startswith("ASK 1:")][0]
        self.assertIn("No question and answer markup on the page.", ask)
        self.assertNotIn("Please take a look when you can", ask)

    def test_slug_guard_still_drops_real_slugs(self):
        rows = register.load_rows(REG)
        r = copy.deepcopy(rows[0])
        r.update(id="F-qa-2", status="waiting_spencer", fix_type="dealeron_request",
                 title="See meta-noindex-f41ae2 now", next_action="Spencer to OK title-leads-other-city")
        path = os.path.join(self.tmp, "reg.jsonl")
        with open(path, "w") as fh:
            fh.write(json.dumps(r) + "\n")
        write(os.path.join(self.tmp, "2026-11.json"), self._base(9))
        _, out, _ = run(path, os.path.join(self.tmp, "2026-11.json"))
        self.assertNotIn("meta-noindex", out)
        self.assertNotIn("title-leads", out)

    def test_tier_one_ask_stays_ahead_of_packets(self):
        rows = register.load_rows(REG)
        base = rows[0]
        out_rows = []
        for i in range(4):
            r = copy.deepcopy(base)
            r.update(id="F-pk-%d" % i, tier=3, status="waiting_spencer", fix_type="dealeron_request",
                     title="Packet number %d" % i, next_action="Spencer to say yes or no", first_seen="2026-11-2%d" % i)
            out_rows.append(r)
        t1 = copy.deepcopy(base)
        t1.update(id="F-t1", tier=1, status="triaged", fix_type="spencer_decision",
                  title="A serious decision", next_action="Spencer to decide now", first_seen="2026-11-25")
        path = os.path.join(self.tmp, "reg.jsonl")
        with open(path, "w") as fh:
            for r in out_rows + [t1]:
                fh.write(json.dumps(r) + "\n")
        write(os.path.join(self.tmp, "2026-11.json"), self._base(9))
        _, out, _ = run(path, os.path.join(self.tmp, "2026-11.json"))
        asks = [l for l in out.splitlines() if l.startswith("ASK ")]
        self.assertEqual(len(asks), 3)
        self.assertIn("A serious decision", asks[0])
        self.assertIn("Packet number", asks[1])


def row(event, channel, host, n):
    return {"eventName": event, "sessionDefaultChannelGroup": channel, "hostName": host, "eventCount": n}


class LeadsInputTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.rows = [
            row("asc_form_submission", "Organic Search", "www.motorinnautogroup.com", 4),
            row("asc_click_to_call", "Organic Search", "www.motorinnautogroup.com", 5),
            row("web_lead_received", "Organic Search", "www.motorinnautogroup.com", 6),      # not an approved event
            row("asc_form_submission_sales", "Organic Search", "www.motorinnautogroup.com", 3),  # subset, not added
            row("asc_form_submission", "Paid Search", "www.motorinnautogroup.com", 40),       # wrong channel
            row("asc_pageview", "Organic Search", "www.motorinnautogroup.com", 1000),
        ]

    def test_counts_only_the_approved_events_in_organic_search(self):
        out = bli.build(self.rows, "2026-11-01", "2026-11-22", "364125348", PULLED)
        self.assertEqual(out["all"]["organic_leads_total"]["value"], 9)
        self.assertEqual(out["group"]["organic_leads"]["value"], 9)
        self.assertEqual(out["all"]["organic_leads_total"]["window"], "2026-11-01..2026-11-22")

    def test_site_with_no_events_on_its_host_is_left_out(self):
        out = bli.build(self.rows, "2026-11-01", "2026-11-22", "364125348", PULLED)
        self.assertNotIn("toyota", out)
        self.assertNotIn("chevy", out)

    def test_measured_site_with_zero_leads_is_zero(self):
        rows = self.rows + [row("asc_pageview", "Direct", "www.motorinntoyotaofcarroll.com", 7)]
        out = bli.build(rows, "2026-11-01", "2026-11-22", "364125348", PULLED)
        self.assertEqual(out["toyota"]["organic_leads"]["value"], 0)

    def test_crm_count_is_a_separate_field_never_added(self):
        out = bli.build(self.rows, "2026-11-01", "2026-11-22", "364125348", PULLED, crm_count=30)
        self.assertEqual(out["all"]["crm_website_leads"]["value"], 30)
        self.assertEqual(out["all"]["organic_leads_total"]["value"], 9)

    def test_no_crm_count_means_no_crm_field(self):
        out = bli.build(self.rows, "2026-11-01", "2026-11-22", "364125348", PULLED)
        self.assertNotIn("crm_website_leads", out["all"])

    def test_bad_input_is_refused(self):
        for bad in ([{"eventName": "x"}], "text", [row("asc_click_to_call", "Organic Search", "h", -1)],
                    [row("asc_click_to_call", "Organic Search", "h", "3")]):
            with self.assertRaises(bli.LeadsError):
                bli.build(bad, "2026-11-01", "2026-11-22", "1", PULLED)
        with self.assertRaises(bli.LeadsError):
            bli.build(self.rows, "2026-11-30", "2026-11-01", "1", PULLED)
        with self.assertRaises(bli.LeadsError):
            bli.build(self.rows, "2026-02-30", "2026-03-01", "1", PULLED)
        with self.assertRaises(bli.LeadsError):
            bli.build(self.rows, "2026-11-01", "2026-11-22", "1", PULLED, crm_count=-2)

    def test_end_to_end_into_baseline_file(self):
        inputs = os.path.join(self.tmp, "in")
        os.makedirs(inputs)
        rep = os.path.join(self.tmp, "ga.json")
        write(rep, self.rows)
        leads = os.path.join(inputs, "leads.json")
        self.assertEqual(bli.main(["--ga4-report", rep, "--start", "2026-11-01", "--end", "2026-11-22",
                                   "--pulled-at", PULLED, "--crm-count", "30", "--out", leads]), 0)
        out = os.path.join(self.tmp, "base", "2026-11.json")
        self.assertEqual(baseline.main(["--month", "2026-11", "--inputs", inputs, "--out", out]), 0)
        data = json.load(open(out))
        self.assertEqual(data["organic_leads_total"]["value"], 9)
        self.assertEqual(data["crm_website_leads"]["value"], 30)
        self.assertEqual(data["sites"]["group"]["organic_leads"]["value"], 9)
        self.assertEqual(data["sites"]["toyota"]["organic_leads"], "not verified")
        self.assertEqual(data["ai_answers"], "not verified")

    def test_month_with_no_pull_is_all_not_verified_not_zero(self):
        empty = os.path.join(self.tmp, "empty")
        os.makedirs(empty)
        payload, counts = baseline.build_payload("2026-12", empty)
        self.assertEqual(payload["organic_leads_total"], "not verified")
        self.assertEqual(payload["crm_website_leads"], "not verified")
        self.assertEqual(counts["total"], counts["not_verified"])

    def test_schema_maps_crm_to_leads_file(self):
        schema = baseline.load_schema()
        self.assertEqual(baseline.metric_file_map(schema)["crm_website_leads"], "leads.json")

    def test_converter_has_no_network_code(self):
        src = open(os.path.join(PKG, "build_leads_input.py"), encoding="utf-8").read().lower()
        for word in ("urllib", "socket", "requests", "http.client", "subprocess", "smtplib"):
            self.assertNotIn(word, src)


if __name__ == "__main__":
    unittest.main()
