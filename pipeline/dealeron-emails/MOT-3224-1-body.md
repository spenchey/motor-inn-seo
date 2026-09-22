# DealerOn change request: 301 redirects for 4 legacy 404 paths (Motor Inn Auto Group)

Hello DealerOn team,

One change request (single issue, per your preferred workflow):

**Add 301 redirects for 4 legacy paths on https://www.motorinnautogroup.com/ that currently return 404 "Page Not Found".**

Current live state (verified 2026-09-21 ~18:00 CT):
- `/inventory` → 404
- `/used-vehicles` → 404
- `/specials` → 404
- `/service-department` → 404

Requested 301 redirect mapping (targets are live pages returning 200):
- `/inventory` → `https://www.motorinnautogroup.com/used-inventory`
- `/used-vehicles` → `https://www.motorinnautogroup.com/used-cars`
- `/specials` → `https://www.motorinnautogroup.com/newspecials.html`
- `/service-department` → `https://www.motorinnautogroup.com/service-locations.html`

Why: these legacy URLs accumulated backlinks and are cited in older marketing materials; 404s waste crawl equity and link authority. 301s preserve it.

Verify step: `curl -I https://www.motorinnautogroup.com/inventory` (and the other three) should return `301` with the `Location` header pointing at the target above.

Please confirm once deployed, or let us know if a different target mapping is correct on your side.

Thank you,
Spencer Heywood
Motor Inn Auto Group — Carroll, IA
