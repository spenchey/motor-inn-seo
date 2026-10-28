import unittest
from unittest import TestCase
from bs4 import BeautifulSoup

from brain.html_inventory_audit import (
    js_only_pages,
    sitemap_vehicle_urls,
    static_hrefs,
)


def html_with_links(links):
    body = "\n".join(f'<a href="{href}">link</a>' for href in links)
    return f"<!doctype html><html><body>{body}</body></html>"


def sitemap_with_urls(urls):
    entries = "".join(f"<url><loc>{url}</loc></url>" for url in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{entries}</urlset>'


class HtmlInventoryAuditTest(TestCase):
    def test_static_hrefs_from_html(self):
        result = static_hrefs(html_with_links(["/vehicle/a", "/vehicle/b"]))
        self.assertEqual(result, {"/vehicle/a", "/vehicle/b"})

    def test_sitemap_vehicle_urls_filters_nonvehicle_links(self):
        soup = BeautifulSoup(sitemap_with_urls(["https://site.com/vehicle/a", "https://site.com/about"]), "xml")
        self.assertEqual(sitemap_vehicle_urls(soup), ["https://site.com/vehicle/a"])

    def test_js_only_pages_distinguishes_static_links_from_missing_links(self):
        self.assertEqual(
            js_only_pages(
                ["https://site.com/vehicle/a", "https://site.com/vehicle/b"],
                ["https://site.com/vehicle/a"],
            ),
            ["https://site.com/vehicle/b"],
        )


if __name__ == "__main__":
    unittest.main()
