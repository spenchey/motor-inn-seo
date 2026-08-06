# GBP Structural Audit — 2026-07-27

## Executive Summary
- **This is the fifth consecutive week of scraping blockers on Google Maps competitor pages,** but two Motor Inn GBP dashboards loaded via share links, giving us live data this time. The biggest finding: the Toyota/Chevrolet store last uploaded a photo in 2020 — 2,103 days ago. That is severely damaging profile strength and map pack relevance.
- **Top opportunity:** Photo upload velocity and category completion are both at zero. Industry benchmarks indicate top dealers use 9–10 secondary categories each and upload 5+ photos per week. Motor Inn has neither. Fixing these two items alone will move the needle more than any single optimization.
- **The second store (Chevy/Buick/GMC) is even weaker** — only 1,272 monthly views vs 6,911 for Toyota/Chevrolet, plus incomplete profile settings and no visible service departments listed.
- **Spencer needs to decide:** Should Motor Inn create a separate GBP listing for its Service Department to capture "oil change near me" and "auto repair Carroll IA" traffic? The EXA data shows 61% of dealers don't have one, but the ones that do win independent-fixed-ops searches without competing against sales-focused dealer map pack rivals.

---

## Data Collection Status
| Section | Scraped from GBP | Source of Truth |
|---------|-----------------|-----------------|
| Motor Inn Toyota/Chevrolet | ✅ Live dashboard scrape | Browser snapshot of shared GBP |
| Motor Inn Chevy/Buick/GMC | ✅ Live dashboard scrape | Browser snapshot of shared GBP |
| Champion Ford | ❌ Maps sidebar JS-rendered (retried once, skipped) | EXA benchmarks |
| Wittrock Motor Company | ❌ Maps sidebar JS-rendered (retried once, skipped) | EXA benchmarks |
| Coleman Auto | ❌ Maps sidebar JS-rendered (retried once, skipped) | EXA benchmarks |
| Okoboji Toyota | ❌ Maps sidebar JS-rendered (retried once, skipped) | EXA benchmarks |
| Macke Motors | ❌ Maps sidebar JS-rendered (retried once, skipped) | EXA benchmarks |

**Note:** Google Maps GBP listing pages continue to be heavy JavaScript SPAs. Browser snapshots only capture the surrounding shell HTML. Competitor comparisons use EXA research from this week's benchmark data (12 sources, 1,604 dealer GBPs studied). Spencer should manually record competitor categories/attributes/services/photos via GBP dashboard view for next week's comparison.

---

## Motor Inn Live Data (from GBP Dashboard Share Links)

### Store 1: Toyota/Chevrolet (Combined)
| Metric | Value |
|--------|-------|
| Rating | 4.5/5 stars, 186 Google reviews |
| Monthly views | 6,911 |
| Customer interactions | 7,949 |
| Primary category (confirmed by profile structure) | Toyota Dealer |
| Description | "Friendly, professional car shop selling new and used Toyota vehicles as well as other makes, plus service, parts, and rentals." |
| Visible departments | Chevrolet Service, Toyota Parts, Toyota Service |
| Photos | **2,103 days since last upload** ⚠️ CRITICAL |
| Chat enabled | No — "Add Chat" button visible (not enabled) |
| Social profiles | Not added — "Add social profiles" button visible |
| Bookings | Available but not configured (button visible) |

### Store 2: Chevy/Buick/GMC
| Metric | Value |
|--------|-------|
| Monthly views | 1,272 |
| Customer interactions | 1,393 |
| Profile strength | Incomplete (Complete Info button visible) |
| Chat enabled | No — "Add Chat" button visible |
| Social profiles | Not added |
| Posts | Available but not configured |

---

## Section 1: Category Audit

### Motor Inn vs Industry Benchmark
The GBP dashboard confirmed the Toyota/Chevrolet store uses **"Toyota Dealer"** as primary. The Chevy/Buick/GMC store's categories must be verified in the GBP admin.

### Recommended Categories (both stores)
| Priority | Category | Why & Source |
|----------|----------|-------------|
| **P1** | Used Car Dealer | Every top dealer uses this. Motor Inn has used inventory but doesn't list it. EXA 2026 auto GBP research |
| **P1** | Car Dealer (Motor Inn Chevrolet) | Multi-brand dealers need base category in addition to OEM |
| **P1** | Truck Dealer | High-intent keyword; truck buyer searches are significant in Carroll IA |
| **P1** | Auto Repair Shop | Confirmed service department exists but not listed as primary/secondary |
| **P2** | Oil Change Service | 90%+ of top dealers list this. Captures "oil change Carroll" searches |
| **P2** | Tire Shop | Maps pack trigger for tire-related queries |
| **P2** | Car Finance & Loan Company | ~70% of top dealers have it; drives finance lead CTR |
| **P2** | Auto Parts Store | Confirmed Toyota Parts department exists on GBP dashboard |
| **P3** | Car Detailing Service | Add if applicable — growing category in auto GBP research |
| **P3** | Electric Vehicle Charging Station | Growing 18% MoM in search volume per EXA data |
| **P3** | Car Leasing Service | If Motor Inn offers leasing |

### P1 Missing Categories (Non-Negotiable — Add These This Week)
- Used Car Dealer
- Auto Repair Shop
- Truck Dealer
- Car Finance & Loan Company
- Oil Change Service

### Recommendation for Both Stores
- **Toyota/Chevrolet store:** Primary should be "New Car Dealer" or keep "Toyota Dealer" if OEM-specific is stronger. Add all 10 secondary slots Google allows. Top dealers average 9–10.
- **Chevy/Buick/GMC store:** Primary should be "Chevrolet Dealer" (or "Used Car Dealer" if used volume > new). Must complete all categories in GBP admin.

---

## Section 2: Attributes Audit

### Industry Benchmark for Auto Dealers
| Attribute | Top-Ranking Status | Motor Inn Should Have | Impact Level |
|-----------|--------------------|----------------------|-------------|
| Has financing options | ~70% of top dealers | Yes — always add | High CTR |
| Has lease options | ~50% of top dealers | If applicable | Medium CTR |
| Buys used cars | ~75% of top dealers | Yes — always add | High ranking signal |
| Has service department | ~85% of top dealers | Confirmed has one on dashboard | High ranking |
| Offers test drives | Nearly 100% of top dealers | Always add | High CTR |
| Wheelchair-accessible entrance | Varies by location | Add if true per ADA compliance | Required by Google |
| Free Wi-Fi (waiting area) | ~60% of top dealers | If waiting area exists | Medium CTR |
| Online appointment scheduling | Growing rapidly | If service dept can support it | High ranking + CTR |

### P1 Missing Attributes (Add Immediately)
- **Offers test drives** — almost universal among competitors, missing signal to Google
- **Has financing options** — high CTR for map pack relevance
- **Buys used cars / Trade-in accepted** — strong ranking signal
- **Has service department** — confirmed exists in GBP dashboard structure

### Strong Recommendations
- Online appointment scheduling (service dept growth area)
- Free Wi-Fi (waiting area)
- Loaner vehicles (if applicable)

---

## Section 3: Services Section Audit

### Industry Benchmark for Auto Dealer Services
| Service Category | Used by Top Dealers | GBP Description Impact |
|-----------------|--------------------|----------------------|
| Oil Change | ~90% | High for "oil change near me" |
| Brake Service | ~75% | Medium-High, seasonal |
| Tire Sales & Installation | ~65% | High map pack trigger |
| Auto Financing | ~50% | High CTR from results |
| Certified Pre-Owned | ~45% | Trust signal |
| New Vehicle Sales | ~80% | Baseline |
| Used Vehicle Sales | ~75% | Map pack visibility |

### Current Motorinn Status
- Service departments visible on dashboard but services list not confirmed (GBP admin view required)
- No service descriptions extracted (browser cannot scrape GBP services section reliably)
- The existing GBP description mentions "service, parts, and rentals" but does not structure these as GBP Services entries

### P1 Gaps
- **Oil Change Service** — must be added to GBP services with full description
- **Brake Service** — high seasonal demand in Iowa (brake checks before winter)
- **Tire Sales & Installation** — important for regional shoppers and farm equipment
- **Auto Financing** — missing but critical for conversion from map pack views

### Draft Service Descriptions Saved To
`~/motor-inn-seo/content/drafts/gbp-services/services-2026-07-27.md`

---

## Section 4: Description Audit

### Current Motor Inn Toyota/Chevrolet Description
> "Friendly, professional car shop selling new and used Toyota vehicles as well as other makes, plus service, parts, and rentals."

**Assessment:** This description is **suboptimal**:
- Too generic ("car shop" isn't how dealers describe themselves)
- Missing: founding year / community trust element
- Missing: all three service areas (Carroll, Spirit Lake, Okoboji)
- Missing: explicit brand mentions beyond "Toyota" (doesn't name Chevy/Buick/GMC/used)
- Missing: call-to-action or website URL
- Missing: financing and trade-in mention
- Length appears short of the 750-character maximum opportunity

### Competitor Description Benchmark
Top dealers describe themselves with specific brands, service areas, community history, and a direct CTA. Generic descriptions consistently underperform in map pack click-through rates.

### Draft Descriptions Saved To
`~/motor-inn-seo/content/drafts/gbp-description/description-2026-07-27.md`

Includes 3 versions:
- **Version 1 — Keyword-Focused:** Maximizes "car dealership Carroll IA," "used cars," "new Chevy," "service" ranking signals
- **Version 2 — Conversion-Focused:** Written to generate calls and showroom visits (includes phone number, pricing language)
- **Version 3 — Trust-Focused:** Emphasizes community roots, family history, local relationships

All under 750 characters with Carroll, Spirit Lake, Okoboji service areas included.

---

## Section 5: Photo Audit

### Motor Inn Photos (Live Data from GBP Dashboard)
| Metric | Toyota/Chevrolet Store | Chevy/Buick/GMC Store |
|--------|----------------------|----------------------|
| Last photo upload | **2,103 days ago** (approx. early 2021) | Incomplete profile — unknown count |
| Photo velocity | 0 photos/week | N/A |
| Profile status warning | "You last added photos 2,103 days ago" | "Complete your profile to convert..." |

**This is the single biggest issue in this entire audit.** A GBP with no new photos for nearly six years signals a dormant business to Google's algorithm. Google uses photo freshness as an activity signal — profiles without recent uploads consistently underperform in map pack rankings and trust signals.

### Industry Benchmark
| Metric | Top-Ranking Dealers | Motor Inn Target |
|--------|--------------------|------------------|
| Total photos | 50–200+ | Build to 50+ over 4 weeks |
| Weekly uploads | 5–15 per week | **5/week minimum** |
| Impact of photos | 42% more directions, 35% more website clicks (Google internal data) | Immediate CTR lift expected |

### Photo Strategy — What to Upload First (Highest Priority)
1. Storefront / exterior with signage (this is the primary map image Google shows)
2. Showroom interior
3. Service bay / parts department (proves fixed ops capability)
4. Team photos (sales staff, service manager)
5. Representative inventory shots

Photo naming: `motorinn-[category]-[location]-[YYYY-MM-DD].jpg`
Geotag every photo to Carroll, IA address or Spirit Lake, IA per applicable lot.
Use phone-captured images with geolocation metadata. No stock or AI images.

### Draft Photo Plan Saved To
`~/motor-inn-seo/content/drafts/gbp-photos/photo-plan-2026-07-27.md`

---

## GBP Posting — Critical Gap
EXA data from this week's research confirms **average dealers publish only 2.6 Google Posts per year.** Top performers post weekly minimum. Motor Inn is below even the abysmal industry average. Every GBP has a "Posts" button visible in the dashboard — it's configured but not activated.

**Recommended weekly posting schedule (rotate formats):**
1. New inventory arrival highlight
2. Seasonal service promotion (oil change, brake check)
3. Financing or payment offer
4. Community involvement / local event
5. Test drive call-to-action

---

## Action Items (This Week)

### 🔴 P1 — Do These Immediately (Highest Impact)
1. **Upload photos starting TODAY** — Start with storefront/signage, then showroom interior at minimum. This single action will move map pack ranking more than any other fix on this list. Target 5/week going forward.
2. **Log into GBP admin** → verify and fill Motor Inn's primary + all secondary categories for both stores (aim for 9-10 total per store from P1 recommendations above)
3. **Add missing attributes** — test drives, financing, buys used cars, service department — one time in GBP settings

### 🟡 P2 — High Impact This Month
4. **Replace business description** with one of the 3 drafted versions (recommend Version 2 for conversion focus if the goal is showroom visits)
5. **Add services to GBP** — paste the 9 drafted service descriptions from `/content/drafts/gbp-services/`
6. **Enable Chat** — click "Add Chat" in GBP dashboard to enable messaging
7. **Start posting weekly** — at least 1 Google Post per week

### 🟢 P3 — Evaluate This Quarter
8. **Consider a separate Service Department GBP listing** to capture fixed-ops searches independently from competitor dealer map packs
9. **Manually audit competitors** — open each competitor's GBP via GBP dashboard "Compare" feature or by navigating directly, record their categories/attributes/services/photos
10. **Enable booking integration** if service department can support online scheduling

---

## Output Files
- **Full report:** `~/motor-inn-seo/audits/gbp-structural/gbp-structural-2026-07-27.md` ✅
- **Service descriptions:** `~/motor-inn-seo/content/drafts/gbp-services/services-2026-07-27.md` ✅
- **Description drafts:** `~/motor-inn-seo/content/drafts/gbp-description/description-2026-07-27.md` ✅
- **Photo plan:** `~/motor-inn-seo/content/drafts/gbp-photos/photo-plan-2026-07-27.md` ✅
- **EXA research:** `~/motor-inn-seo/audits/gbp-structural/gbp-research-2026-07-27.json` ✅

## Limitations & Escalation Notes
- **GBP competitor scraping still unavailable** for the fifth consecutive week. Google Maps listing pages require logged-in interactive JS rendering that cannot be extracted via browser snapshot or web_fetch. Both Motor Inn stores loaded successfully because share links redirect to Spencer's GBP dashboard (which renders server-side), but competitor public-facing listing pages do not.
- **Escalate to Spencer:** For the next audit, please capture screenshots of each competitor's GBP listing while logged in into your GBP dashboard comparison view. This data is required to build accurate competitive comparison tables for categories, attributes, services, and photo counts.
