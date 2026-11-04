# Adversarial pass — 2026-11-04

## Scored page table

| Page | Current status | Key risk | Priority fix |
|---|---|---|---
| contactus-money-page | 4/10 | Local money page has no live NAP proof beyond phone/address; `75+ years` and Chevrolet `certification` claims are unsourced. | Remove/qualify those two claims; add NAP block, map, hours, service and inventory links. |
| testdrive-page | 4/10 | `1741 N. US Highway 71` competes with `1526 Le Clark Rd` in the same paragraph; dealer policy and phone/insurance/licence require owner confirmation; FAQ absent. | Use the GBP-verified `1526 Le Clark Rd`; strip the unverified policy/insurance/licence copy; add NAP + service/inventory links. |
| trim-levels-explained | 5/10 | Has real GSC question demand (2,761 impressions) and FAQ, but the source line is wrong (`hyundaiusa.../santa-cruz` labelled `Ford Escape tech specs`), and the page has no local/brand entity coverage. | Fix source; add Toyota/Chevrolet entity coverage and live inventory links. |
| highlander-vs-grand-highlander | 5/10 | Has solid GSC FAQ demand and spec table, but the CTA and some duplicate Toyota links are weak. | Tidy CTA and duplicate links; add local dealer contact/NAP and inventory routing. |
| used-trucks-carroll | 4/10 | Address and phone match, but no evidence for `Silverado vs F-150/Ram` claims or for "Strong towing numbers"; the page also lacks a live DealerOn route map. | Drop unverified model-specific claims; add inventory/contact/test-drive links; use verified NAP. |
| used-trucks-towing-iowa | 4/10 | Real towing ranges are sourced, but the page has no Iowa winter/used-safety schema and no live DealerOn route map. | Add local contact, used-inventory and related model links; make the towing ranges clearly sourced. |
| car-dealership-carroll-iowa (new) | 4/10 | Highest local demand (#26 volume 169-imp cluster) but currently no dedicated page. | Add dedicated Carroll dealership page, live inventory/contact/test-drive links, GSC-aligned H1/H2s. |

## Non-negotiables
1. Drop every claim that lacks proof: `75+ years`, Chevrolet `certification`, specific `Silverado vs F-150/Ram` performance claims, dealer policy/insurance/licence claims.
2. Use the GBP-verified `1526 Le Clark Rd, Carroll, IA 51401` and `(712) 792-5000`.
3. Fix every broken source anchor and duplicate/inconsistent heading.
4. Add explicit local/internal links to `used-inventory`, `/vehicle-trim-levels-explained`, `/highlander-vs-grand-highlander`, `/used-trucks`, `/used-trucks-towing-iowa`, `/contactus`, `/testdrive`, `/silverado-towing-guide` whenever relevant.
5. Every page gets FAQPage schema only where the GSC question demand is real; otherwise omit.
6. Every page uses DealerOn-exact classes and no external CSS dependencies.
7. Every page has canonical URL and title/meta that match the live page slug.

## Fix list
- `contactus-money-page.html` — remove 75+ years and Chevrolet-certification claims, add NAP + map + inventory/service/test-drive links.
- `testdrive-page.html` — replace `1741 N. US Highway 71` with `1526 Le Clark Rd`; drop the dealer policy/insurance/licence copy and mismatch of phone/insurance/licence; add NAP and service/inventory cross-links.
- `trim-levels-explained.html` — fix the source line to `Hyundai Santa Cruz` (not Ford Escape); add entity-rich H2/H3 coverage.
- `highlander-vs-grand-highlander.html` — clean the CTA and duplicate Toyota links; add the local contact/lot link.
- `used-trucks-carroll.html` — align phone href and text; add inventory/test-drive/service links; label the towing numbers clearly.
- `used-trucks-towing-iowa.html` — add the Iowa winter/used-safety FAQ schema and local dealer routes.
- `car-dealership-carroll-iowa.html` — new page for the highest local-demand query; add the exact local-intent H1/H2s, FAQ schema, and DealerOn route links.
