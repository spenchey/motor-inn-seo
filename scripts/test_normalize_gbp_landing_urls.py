import unittest

from normalize_gbp_landing_urls import canonical_gbp_url


class NormalizeGbpLandingUrlsTest(unittest.TestCase):
    def test_toyota_contact_url_maps_to_clean_new_toyota_page(self) -> None:
        url = "https://www.motorinnautogroup.com/Contactus/Carroll?utm_source=organic&utm_medium=web&utm_campaign=toyota&utm_id=gmb"

        self.assertEqual(canonical_gbp_url(url), "https://www.motorinnautogroup.com/new-toyota")

    def test_chevrolet_contact_url_maps_to_clean_used_inventory_page(self) -> None:
        url = "https://www.motorinnautogroup.com/Contactus/Carroll?utm_source=organic&utm_medium=web&utm_campaign=chevrolet&utm_id=gmb"

        self.assertEqual(canonical_gbp_url(url), "https://www.motorinnautogroup.com/used-inventory")

    def test_existing_canonical_url_loses_utm_parameters(self) -> None:
        url = "https://www.motorinnautogroup.com/used-inventory?utm_source=organic&utm_medium=web&utm_id=gmb"

        self.assertEqual(canonical_gbp_url(url), "https://www.motorinnautogroup.com/used-inventory")


if __name__ == "__main__":
    unittest.main()
