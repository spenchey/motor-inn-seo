# DealerOn change request — remove Buick & GMC from Motor Inn of Carroll brand references

**To:** support@dealeron.com
**From:** Motor Inn of Carroll (DealerOn dealer ID 29055, dealer code 280610, sincroweb `gmps-motor-carroll`)
**Subject: Remove Buick and GMC logos from franchise logo rotation — Motor Inn of Carroll (29055)**

---

Hi DealerOn team,

Motor Inn of Carroll is no longer a Buick or GMC dealer (Buick franchise closed October 2026; GMC ended earlier). Our Chevrolet site, **motorinnofcarroll.com**, still shows Buick and GMC logos in the header franchise logo rotation on every page. Please remove both brands from the logo rotation and any other brand references listed below. Do **not** make any other changes to the site.

## 1. Header franchise logo rotation (all templates, desktop + mobile) — highest customer visibility

The global header contains a `rotateLogos` block inside `li.manuLogo` with three `<img>` tags. Chevrolet must stay; **Buick and GMC must be removed** so the rotation shows Chevrolet only.

**Desktop header** (template `#leftBlockInfo`, appears once per page):

    <div class="rotateLogos">
      <img class="img-responsive logoChevrolet" src="/assets/logos/transparent/chevrolet-wide.png" alt="Chevrolet">   <!-- KEEP -->
      <img class="img-responsive hideOnLoad logoBuick" src="/assets/logos/transparent/buick.png" alt="Buick">         <!-- REMOVE -->
      <img class="img-responsive hideOnLoad logoGMC"  src="/assets/logos/transparent/gmc.png"  alt="GMC">            <!-- REMOVE -->
    </div>

**Mobile header** (template `#navbar-header`, `div.mobile.container.visible-xs`, `div.manuLogo` — same three-image structure with the square `chevrolet.png` variant):

    <img class="img-responsive hideOnLoad logoBuick" src="/assets/logos/transparent/buick.png" alt="Buick">   <!-- REMOVE -->
    <img class="img-responsive hideOnLoad logoGMC"  src="/assets/logos/transparent/gmc.png"  alt="GMC">       <!-- REMOVE -->

**Affected URLs (verified 2026-10-12):** this header renders on every page of the site, including:

- https://www.motorinnofcarroll.com/ (homepage)
- https://www.motorinnofcarroll.com/searchused.aspx (used inventory SRP)
- https://www.motorinnofcarroll.com/searchnew.aspx (new inventory SRP)
- Vehicle detail pages, e.g. https://www.motorinnofcarroll.com/used-Lake+City-2024-GMC-Terrain-SLT-3GKALVEG6RL193418
- /service.html, /about.html, /contact.html and all other templates

The Buick/GMC `<img>` elements are hidden on load (`hideOnLoad` class + `.rotateLogos img.hideOnLoad { display:none }` in `/assets/styles/859/header/header.css`) and displayed by the rotation logic — they are customer-visible as the header cycles. Note the images also currently render as the logo link's tooltip/alt when the rotation lands on them.

**Requested change:** delete the two `hideOnLoad logoBuick` / `hideOnLoad logoGMC` `<img>` lines from both the desktop and mobile header templates (or, if the rotation is driven by a franchise list in the dealer settings, remove Buick and GMC from that list for dealer 29055). Chevrolet (wide + square variants) and the dealer logo / CarBravo lockup must remain exactly as-is.

## 2. Items we verified as already correct — no action needed

For completeness, these were audited 2026-10-12 and need no change:

- Page `<title>` tags and meta descriptions on home, new, used, service, about, contact: zero Buick/GMC mentions (Chevrolet-branded, correct).
- Footer: contains only the Chevrolet "Together Lets Drive" tagline image and the DealerOn logo — no Buick/GMC brand row. No change.
- schema.org structured data: no Buick/GMC `brand` values on any audited page.
- Body copy on Chevrolet-store pages: no Buick/GMC mentions outside inventory data.

## 3. Inventory data references (informational — please do not remove)

Buick/GMC strings also appear in inventory-derived content on our sites. These are **legitimate** (they describe vehicles we actually have in stock, e.g. used GMC Terrain/Acadia listings and their JSON-LD `"itemListElement"` entries on used SRPs, plus provider-ID maps in inline JS config). Please leave all inventory data, search filters, and structured data for in-stock used Buick/GMC units untouched — only the brand/identity elements in section 1 should change.

## Sites in scope

- **motorinnofcarroll.com (Chevrolet store, dealer 29055)** — the only site requiring changes (header logo rotation, section 1).
- motorinntoyotaofcarroll.com — audited; zero stale brand references in template/identity elements (only used-inventory data). No changes requested.
- motorinnautogroup.com — audited; clean. No changes requested.

Please confirm the turnaround for the header logo-rotation edit, or let us know if you need the change requested through the DealerOn dashboard instead.

Thanks,
Motor Inn of Carroll — Marketing
1526 Le Clark Rd, Carroll, IA 51401

---

### Internal audit appendix (not part of the email)

Audit date 2026-10-12; pages crawled: chevrolet home/used/new/real VDP/service/about/contact, group home/about/used, toyota home/used; counts of `Buick`/`GMC` raw hits, title/meta/h1 checks, header/footer/schema classification all captured in the run workspace `~/.hermes/kanban/workspaces/t_b8b5454d/` (`audit_counts.py`, `final_verify.py`, `pages/*.html`). Chevrolet-store header = 6 Buick refs + 4–5 GMC refs per page, all inside the two `rotateLogos` blocks (desktop + mobile). Every non-header hit across all three domains is inventory data (used-unit listings, provider maps) or already-correct metadata.
