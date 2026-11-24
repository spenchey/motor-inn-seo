"""is_us() in brain/ai_visibility_run.py: "Carroll" alone must never count as us.

The script calls a paid API at import time, so it is never imported or run here.
Only the is_us pieces are lifted out of its source with ast. No network.
"""
import ast
import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "brain", "ai_visibility_run.py")
REPORTS = os.path.join(ROOT, "brain", "ai-visibility")
KEEP_ASSIGN = ("OUR_HOSTS", "NAME_RE")
KEEP_FUNCS = ("_host_ours", "_host_of", "is_us")


def load_is_us():
    with open(SCRIPT, encoding="utf-8") as fh:
        tree = ast.parse(fh.read())
    keep = [n for n in tree.body
            if isinstance(n, (ast.Import, ast.ImportFrom))
            or (isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") in KEEP_ASSIGN)
            or (isinstance(n, ast.FunctionDef) and n.name in KEEP_FUNCS)]
    ns = {}
    exec(compile(ast.Module(body=keep, type_ignores=[]), SCRIPT, "exec"), ns)
    return ns["is_us"]


is_us = load_is_us()

TITLES = [
    ("Rival Auto Carroll", "Rival Auto Carroll | Used Cars & Auto Repair in Carroll, Iowa", False),
    ("Carroll Example Sales", "Carroll Example Sales | Used Cars", False),
    ("www.example-dealer.biz", "Used & Pre-Owned Car, Trucks & SUVs Dealer Carroll, IA - Example Dealer", False),
    ("Google", "Acme Motor Company", False),
    ("Motor Inn Auto Group", "New & Used Toyota & Chevrolet Vehicles in Carroll, IA | Motor Inn Auto", True),
    ("Google", "Motor Inn Toyota and Chevrolet of Carroll", True),
    ("Google", "Toyota Service at Motor Inn of Carroll", True),
    ("Motor Inn Toyota Of Carroll", "Service Service & Parts Department - Carroll Toyota dealer in Carroll", True),
    ("CARFAX", "Motor Inn of Carroll Dealership, IA - CARFAX", True),
    ("Google", "Toyota of Carroll", False),
    ("Google", "Chevrolet of Carroll", False),
    ("Motor Inn Motel", "Motor Inn Motel - Rooms in Omaha", False),
    ("Google", "Carroll Motor Inn Hotel", False),
    ("x", "y", False),
]
URLS = [
    ("https://www.motorinnautogroup.com/x", "", True),
    ("https://ai.motorinntoyotaofcarroll.com/llms.txt", "", True),
    ("https://motorinnofcarroll.com", "", True),
    ("https://motorinnautogroup.com.evil.com/", "motorinnautogroup.com.evil.com", False),
    ("https://notmotorinnofcarroll.com/", "", False),
    ("", "www.motorinnautogroup.com", True),
    ("https://carroll-example.com", "", False),
]


class IsUs(unittest.TestCase):
    def test_titles_and_sources(self):
        for src, title, want in TITLES:
            self.assertEqual(is_us(src, title), want, (src, title))

    def test_urls_and_domains(self):
        for url, domain, want in URLS:
            self.assertEqual(is_us("Google", "t", url, domain), want, (url, domain))

    def test_malformed_url_gives_empty_host_not_an_error(self):
        for bad in ("http://[bad", "https://[::1", "http://a]b/", "http://[x]y/"):
            self.assertFalse(is_us("Google", "t", bad, ""), bad)
        # a malformed URL does not hide a good domain or a good name
        self.assertTrue(is_us("Google", "t", "http://[bad", "www.motorinnautogroup.com"))
        self.assertTrue(is_us("Google", "Motor Inn Auto Group", "http://[bad", ""))

    def test_non_string_inputs_are_coerced(self):
        self.assertFalse(is_us(None, None, None, None))
        self.assertFalse(is_us("Google", "t", 123, 456))
        self.assertFalse(is_us(["x"], {"a": 1}, b"https://carroll-example.com", object()))
        self.assertTrue(is_us("Google", "t", "", "www.motorinnautogroup.com"))

    def test_new_rule_never_counts_more_than_the_old_one_on_saved_reports(self):
        """Old rule: 'motorinn' or 'carroll' anywhere. The new rule only narrows it."""
        old = lambda s, t: any(m in (s + t).lower() for m in ("motorinn", "carroll"))
        if not os.path.isdir(REPORTS):
            self.skipTest("no saved reports")
        for name in sorted(os.listdir(REPORTS)):
            if not (name.startswith("ai-vis-") and name.endswith(".md")):
                continue
            with open(os.path.join(REPORTS, name), encoding="utf-8") as fh:
                for ln in fh.read().splitlines():
                    if ln.startswith("- ") and "Get onto" not in ln:
                        s, _, t = ln[2:].partition(" | ")
                        if is_us(s, t):
                            self.assertTrue(old(s, t), (name, ln))


if __name__ == "__main__":
    unittest.main()
