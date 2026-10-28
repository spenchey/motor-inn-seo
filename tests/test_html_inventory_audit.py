import unittest
from bs4 import BeautifulSoup

from brain.html_inventory_audit import js_only_pages, sitemap_vehicle_urls, static_hrefs


def html_with_links(links):
    body = "\n".join(f'<a href="{href}">link</a>' for href in links)
    return f"<!doctype html><html><body>{body}</body></html>"


class HtmlInventoryAuditTest(unittest.TestCase):
    def test_static_hrefs_from_html(self):
        result = static_hrefs(html_with_links(["/vehicle/a", "/vehicle/b"]))
        self.assertEqual(result, {"/vehicle/a", "/vehicle/b"})

    def test_sitemap_vehicle_urls_filters_nonvehicle_links(self):
        xml = """<?xml version="1.0"?><urlset><url><loc>https://site.com/vehicle/a</loc></url>
<url><loc>https://site.com/about</loc></url></urlset>"""
        soup = BeautifulSoup(xml, "xml")
        self.assertEqual(sitemap_vehicle_urls(soup), ["https://site.com/vehicle/a"])

    def test_js_only_pages_distinguish_static_links_from_missing_links(self):
        sitemap = {"https://site.com/vehicle/a", "https://site.com/vehicle/b"}
        static = {"https://site.com/vehicle/a"}
        self.assertEqual(js_only_pages(sitemap, static), ["https://site.com/vehicle/b"])


if __name__ == "__main__":
    unittest.main()
