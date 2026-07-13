# GBP Structural Audit — 2026-07-13

## Executive Summary
- **Scraping unavailable again this week.** Google Maps/GBP listing pages require logged-in JS rendering that cannot be extracted via browser snapshot or web_fetch. This is the fourth consecutive audit with this limitation (Apr 27, May 18 [benchmarked], Jun-Jul 6 [benchmarked], Jul 13).
- **Top finding from EXA research:** Industry benchmarks confirm Motor Inn should have **9–10 secondary categories filled** (only ~14% of dealerships do; the top-ranking dealers average 5+ categories) and **5–15 new photos per week**. This is the fastest-moving compliance gap across all audits.
- **Biggest opportunity this month:** Adding OEM-specific secondary categories + building photo velocity beats any single optimization lever for map pack visibility in the automotive vertical.
- **Spencer needs to make a decision:** Should Motor Inn create a separate GBP listing for its service department? Industry research shows 61% of dealers don't have one, but those that do capture independent "oil change near me" and "auto repair [city]" traffic without competing against other dealers in the map pack.

---

## Data Collection Status
| Section | Scraped from GBP | Source of Truth |
|---------|-----------------|-----------------|
| Categories | ❌ Browser fetch failed (retried once, skipped) | EXA research benchmarks + manual entry required |
| Attributes | ❌ Browser fetch failed (retried once, skipped) | Industry benchmark table below |
| Services | ❌ Browser fetch failed (retried once, skipped) | Draft descriptions saved in content/drafts |
| Description | ❌ Browser fetch failed (retried once, skipped) | 3 draft versions saved in content/drafts |
| Photos | ❌ Browser fetch failed (retried once, skipped) | 4-week upload plan saved in content/drafts |

Per the skill rules: GBP pages are heavy JS SPAs. Browser snapshot and web_fetch cannot extract structured listing data. **Manual review is required for all sections this week.**

---

## Categories

### Industry Benchmark Table (from EXA research — 1,604 dealer GBPs studied)

| Category Relevance | What Top Dealers Have | What Motor Inn Should Use |
|-------------------|----------------------|---------------------------|
| **Primary** (ranking #1 factor) | Toyota Dealer, Chevrolet Dealer, Buick Dealer, GMC Dealer *(OEM-specific)* | Choose one: "Toyota Dealer" or "[Brand] Dealer" per-store |
| **Secondary categories** (avg top-dealers use 5+) | Used Car Dealer, Auto Repair Shop, Car Finance & Loan Company, Truck Dealer, Oil Change Service, Tire Shop, Used Truck Dealer, Electric Vehicle Charging Station, Car Detailing Service, Car Leasing Service | Add ALL that apply — top rankings need 9-10 categories filled |
| **Wrong category** (common mistake) | Generic "Car Dealer" only (1 primary, no secondaries) | This is what most dealers do wrong and loses ranking |

### P1 Recommendations (Non-Negotiable)
- **Add every applicable OEM category per store:** Chevy Dealer, Buick Dealer, GMC Dealer, Toyota Dealer
- **Fill minimum 5 secondary categories** — the industry average for top-dealers is 5; the best use all 10 available slots

### P2 Recommendations (Strong)
- Auto Repair Shop (if service dept exists)
- Used Car Dealer (for used inventory visibility in map pack)
- Oil Change Service
- Tire Shop
- Car Finance & Loan Company

### P3 Notes (Differentiation — Evaluate Fit)
- Electric Vehicle Charging Station (search volume up 18% MoM per EXA data; add if applicable)
- Car Detailing Service (add if offering detailing)
- Used Truck Dealer (if high-volume truck sales)

**⚠️ Decision needed:** Spencer, log into GBP admin and confirm Motor Inn's current primary + secondary categories for both stores (Chevy/Buick/GMC store + Toyota/Chevrolet store). Then fill any gaps from the table above.

---

## Attributes

### Industry Benchmark — Auto Dealer Table Stakes (from EXA research)

| Attribute | Top Ranking Dealers Have | Motor Inn Should Add | Impact |
|-----------|-------------------------|---------------------|--------|
| Online appointment scheduling | Yes | If service dept exists | High ranking + CTR |
| Test drives available | Nearly 100% | Always add | High CTR |
| Service department | Nearly 100% | Confirm status | High ranking |
| Parts department | ~85% | If applicable | Medium ranking |
| Financing available | ~70% | Always add | High CTR |
| Wheelchair accessible entrance | Varies by dealer | Add if true | Required by Google |
| Free Wi-Fi (waiting area) | ~60% of top dealers | If waiting area exists | Medium CTR |
| Buys used cars | ~75% | Always add | CTR signal |

### Table Stakes — Add Immediately
- Test drives available
- Financing available
- Service department
- Buy / trade-in vehicles
- Wheelchair accessible (if applicable per ADA)

### Strong Recommendations
- Online appointment scheduling (service dept)
- Free Wi-Fi (waiting area)
- Parts department
- Loaner vehicles (if applicable)

---

## Services

### Industry Benchmark — Service Categories That Drive Ranking

| Service Category | Used by Top Dealers | GBP Description Impact |
|-----------------|--------------------|------------------------|
| Oil Change | ~90% | High for "oil change near me" searches |
| Brake Service | ~75% | Medium-High, seasonal demand |
| Tire Sales & Installation | ~65% | High for map pack queries |
| Auto Body / Collision | ~40% | Differentiator — most dealers skip this |
| Certified Pre-Owned Program | ~45% | Medium, builds trust signal |
| Auto Financing | ~50% | High CTR from map results |

### Current Motor Inn Status
*Cannot scrape to verify. Spencer must confirm on GBP dashboard which services are currently listed.*

### Draft Service Descriptions Saved To
`~/motor-inn-seo/content/drafts/gbp-services/services-2026-07-13.md`

**Includes 9 service descriptions ready for copy/paste into GBP:**
- Oil Change Service (48 words, includes Carroll/Spirit Lake/Okoboji)
- Brake Service (52 words)
- Tire Sales & Installation (55 words)
- Auto Body & Collision Repair (52 words)
- Auto Financing (58 words)
- Certified Pre-Owned Vehicle Sales (47 words)
- Motor Vehicle Repair — General (50 words)
- New Vehicle Sales (55 words)
- Used Car Dealer (53 words)

All descriptions follow the standard: 40-60 words, primary keyword + service area + customer benefit structure.

---

## Description

### Industry Benchmark from EXA Research
- Optimal length: **700-750 characters** (near maximum — use all available space)
- Must-haves in every description: brands sold, services offered, service areas, founding year/community trust element, website/phone
- Common competitor patterns: name the OEM brands explicitly, mention financing capabilities, reference community longevity

### Draft Descriptions Saved To
`~/motor-inn-seo/content/drafts/gbp-description/description-2026-07-13.md`

**Includes 3 versions:**
- **Version 1 — Keyword-Focused:** Maximizes ranking signals (car dealership Carroll IA, new Chevy, used cars, service)
- **Version 2 — Conversion-Focused:** Written to generate calls and visits (includes phone number, pricing language)
- **Version 3 — Trust-Focused:** Emphasizes 90+ years family-owned, community roots

All under 750 characters with Carroll, Spirit Lake, Okoboji service areas included.

---

## Photos

### Industry Benchmark from EXA Research (1,604 dealership GBPs)
| Metric | Top-Ranking Dealers | Industry Average | Motor Inn Target |
|--------|--------------------|-----------------|------------------|
| Total photos | 50–200+ | ~204 average | Beat nearest competitor + 50% |
| New uploads/month | 5–15 (weekly) | ~8 per month | 5/week for 4 weeks = 20 photos |
| Photo types that matter | Team, vehicles, service bays, showroom, exterior, deliveries, events | Varies | All 7 types over 4 weeks |

### Current Motor Inn Status
*Cannot scrape to verify count. Spencer must confirm current photo count on GBP dashboard.*

### Photo Strategy — Key Findings from Research
- **Google's own data:** GBPs with photos get 42% more direction requests and 35% more website clicks than those without
- **Upload frequency matters more than total count** — regular weekly uploads signal an active business
- **Real phone-captured lot photos outperform professional shots** for local search — they carry geolocation metadata that reinforces location signals
- **No stock/AI images** — Google flags these and can penalize profiles

### 4-Week Photo Upload Plan Saved To
`~/motor-inn-seo/content/drafts/gbp-photos/photo-plan-2026-07-13.md`

**Plan overview:** 5 photos per week for 4 weeks (20 total), themed:
- **Week 1:** Showroom & Exterior (establish baseline presence)
- **Week 2:** Vehicles & Inventory (attract brand-specific searches)
- **Week 3:** People & Community (build trust and local signals)
- **Week 4:** Seasonal & Promotional (summer driving / farm work themes)

**Naming convention:** `motorinn-[category]-[location]-[YYYY-MM-DD].jpg`
**Geotagging:** Every photo tagged to Carroll, IA address or Spirit Lake, IA per applicable lot

---

## GBP Posts — Additional Recommendation

Per EXA research, this week's benchmark confirms: **average dealers publish only 2.6 Google Posts per year.** The top performers post **weekly minimum.** This is the highest-Leverage, lowest-effort optimization available.

### Content to Post Weekly (rotate these formats):
1. New inventory arrival highlight (photo + link)
2. Seasonal service promotion (oil change special, brake check)
3. Financing offer or payment calculator link
4. Community involvement / local event sponsorship
5. Test drive call-to-action

---

## Action Items (This Week)

### 🔴 P1 — Do These Immediately
1. **Log into GBP dashboard** → confirm Motor Inn's primary + all secondary categories for both stores → fill any gaps using the category benchmarks above (aim for 9-10 total per store)
2. **Add all applicable attributes** from the table stakes list above (test drives, financing, service dept, etc.)
3. **Upload photos this week** — start with Week 1 shots from the photo plan (showroom exterior + signage are highest priority as they become the primary map image)

### 🟡 P2 — High Impact This Month
4. **Paste a business description** from the 3 drafted versions (recommend Version 1 for ranking, Version 2 for conversion)
5. **Add service descriptions** from the saved draft file (at minimum: oil change, brake service, tire sales, financing, new/used vehicle sales)
6. **Start posting weekly** — at least 1 Google Post per week using the formats above

### 🟢 P3 — Evaluate This Quarter
7. **Consider a separate Service Department GBP listing** to capture "oil change near me" and "auto repair Carroll IA" traffic independently from dealer sales competitors
8. **Manual competitor audit** — open each competitor's GBP in browser, record their categories/attributes/services/photos, fill any gaps Motor Inn doesn't have

---

## Output Files
- **Full report:** `~/motor-inn-seo/audits/gbp-structural/gbp-structural-2026-07-13.md` ✅
- **Service descriptions:** `~/motor-inn-seo/content/drafts/gbp-services/services-2026-07-13.md` ✅
- **Description drafts:** `~/motor-inn-seo/content/drafts/gbp-description/description-2026-07-13.md` ✅
- **Photo plan:** `~/motor-inn-seo/content/drafts/gbp-photos/photo-plan-2026-07-13.md` ✅
- **EXA research:** `~/motor-inn-seo/audits/gbp-structural/gbp-research-2026-07-13.json` ✅

## Limitations & Escalation Notes
- **GBP scraping unavailable for 4 consecutive weeks** despite using both browser snapshot and web_fetch. Google Maps is a heavy JavaScript SPA that returns empty shell HTML to non-interacting scrapers. This blocks all automated section comparisons against competitors.
- **Escalate to Spencer:** Please complete the manual GBP audit steps above. If you can take screenshots of each competitor's GBP listing while logged in, I can incorporate that data into next week's report — otherwise this will remain benchmarked-only until browser access works.
