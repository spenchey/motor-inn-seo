# GBP Landing URL Canonicalization - 2026-06-29

## Finding

Historical SEO audits show Google Business Profile traffic landing on:

- `https://www.motorinnautogroup.com/Contactus/Carroll?utm_source=organic&utm_medium=web&utm_campaign=toyota&utm_id=gmb`
- `https://www.motorinnautogroup.com/Contactus/Carroll?utm_source=organic&utm_medium=web&utm_campaign=chevrolet&utm_id=gmb`

These URLs route local-intent traffic to a generic contact page and split Google Search Console attribution through UTM variants.

## Canonical Replacement

Use query-free DealerOn landing URLs for GBP profile and GBP campaign destinations:

| Source intent | Replace with |
| --- | --- |
| Toyota/new vehicle intent | `https://www.motorinnautogroup.com/new-toyota` |
| Used inventory, Chevrolet, GM, or unknown inventory intent | `https://www.motorinnautogroup.com/used-inventory` |

Do not add `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, or `utm_id` to GBP landing URLs. Let GSC and GBP attribution remain clean.

## Automation Added

Rory's SEO/GEO workflow can now run:

```bash
python3 scripts/normalize_gbp_landing_urls.py path/to/gbp-export.csv --check
python3 scripts/normalize_gbp_landing_urls.py path/to/gbp-export.csv --output path/to/gbp-export.normalized.csv
```

The same script supports JSON exports.

## Live API Status

Attempted a bounded Google Business Profile API read on 2026-06-29 using ADC and quota project `jeeves-485623`. The request returned `429`, so live `websiteUri` values were not changed from this run.

Rory should retry the read/update step after quota clears, or use this audit as the manual update handoff for Google Business Profile.
