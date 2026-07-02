# Local Authority Audit — July 2026

## Executive Summary

- **Overall status:** Motor Inn's entity is still fragmented across citations. The canonical NAP is stable on the main site, but major third-party listings continue to use legacy sub-brand names and non-canonical phone numbers.
- **Most urgent issues:** Google Business Profile duplication/fragmentation, Facebook phone/name mismatch, Yelp service listing mismatch, BBB mismatch, Yellow Pages mismatch.
- **Biggest wins this month:** The live site now exposes the correct canonical NAP and geo coordinates, and the homepage already ships JSON-LD. The next lift is normalization, not starting from zero.
- **Method note:** The runbook called for `gstack-browse`, but that surface is not available in this environment. This audit used Firecrawl, direct site fetches, and the provided source-of-truth files instead.

## Current Local SEO Standards Snapshot

Source research run first:

- https://a3brands.com/blog/how-google-ranks-car-dealerships/
- https://cfmgrowth.com/blog/local-seo-auto-businesses-google-map-pack/
- https://xsquareseo.com/automotive-seo/google-business-profile-seo-for-automotive-dealers-in-2026/
- https://a3brands.com/blog/rank-for-dealer-near-me/

Current consensus from the July 2, 2026 research pass:

1. Google still weights **relevance, distance, and prominence** for local automotive rankings.
2. For dealers, **prominence** is the controllable lever: review velocity, citation consistency, backlinks, and GBP completeness.
3. **Citation consistency matters more than raw citation count.** A smaller set of exact-match, high-authority profiles beats a large set of inconsistent listings.
4. **Exact NAP and brand consistency now matter for AI visibility too**, not just map-pack trust.
5. **FAQ / schema / entity consistency** are increasingly part of answer-engine visibility, especially for local dealership queries.

## Canonical NAP

- **Name:** Motor Inn Auto Group
- **Address:** 1526 Le Clark Road, Carroll, IA 51401
- **Phone:** (712) 522-2526
- **Website:** https://www.motorinnautogroup.com

Any deviation from the above is wrong for this audit.

## Section 1: Citation Audit

| Platform | Listed? | Name Match | Address Match | Phone Match | Website Match | Duplicates? | Rating | Reviews |
|---|---|---|---|---|---|---|---|---|
| Google Business Profile | Yes | No | Unknown | No | Yes | Yes | 4.5 | 182 Google reviews on combined profile |
| Yelp | Yes | No | No | No | Unknown | Yes | 5.0 | 1 review on service listing |
| Bing Places | No | Unknown | Unknown | Unknown | Unknown | Unknown | — | — |
| Apple Maps | No | Unknown | Unknown | Unknown | Unknown | Unknown | — | — |
| Facebook Business Page | Yes | No | Unknown | No | Unknown | No | — | 1.3K+ followers |
| BBB | Yes | No | Yes | No | No | No | Not BBB Accredited | — |
| Cars.com | No indexed result found | Unknown | Unknown | Unknown | Unknown | Unknown | — | — |
| CarGurus | Yes | No | No | No | Unknown | No | — | 2 reviews |
| Autotrader | No indexed result found | Unknown | Unknown | Unknown | Unknown | Unknown | — | — |
| DealerRater | Yes | No | Unknown | Unknown | Unknown | No | N/A | Not enough recent reviews for overall rating |
| Edmunds | Yes | No | Unknown | Unknown | Unknown | No | — | Dealer surfaced inside vehicle result |
| TrueCar | No indexed result found | Unknown | Unknown | Unknown | Unknown | Unknown | — | — |
| Yellow Pages | Yes | No | No | No | No | No | — | — |
| Manta | No indexed result found | Unknown | Unknown | Unknown | Unknown | Unknown | — | — |
| Foursquare | No indexed result found | Unknown | Unknown | Unknown | Unknown | Unknown | — | — |
| Superpages | Yes | No | No | Unknown | Unknown | No | — | — |
| Citysearch | No indexed result found | Unknown | Unknown | Unknown | Unknown | Unknown | — | — |
| MapQuest | Yes | No | No | Unknown | Unknown | Yes / indirect | — | — |
| Iowa Auto Dealers Association directory | Mention only | No | Unknown | Unknown | Unknown | No | — | — |
| Carroll Chamber of Commerce | Yes | No | No | No | Unknown | No | — | — |
| Spirit Lake / Okoboji Chamber of Commerce | No indexed result found | Unknown | Unknown | Unknown | Unknown | Unknown | — | — |
| Carroll Times Herald business directory | No structured directory found; news mention only | No | Yes | Unknown | Unknown | No | — | — |

### Evidence Notes by Platform

- **Google Business Profile**
  - Two live Google entities surfaced: `Motor Inn Toyota and Chevrolet of Carroll` and `Motor Inn Chevrolet of Carroll`.
  - Combined Toyota/Chevrolet profile showed `4.5` stars and `182 Google reviews`.
  - Combined profile exposed `Call +1 712-792-5000`, not the canonical `(712) 522-2526`.
  - This is the clearest entity-fragmentation issue in the stack.

- **Yelp**
  - Search surfaced both `Motor Inn Toyota of Carroll` and `Motor Inn of Carroll, Service`.
  - The live service page was unclaimed and used `1526 Le Clark Rd` plus `(866) 772-1687`.
  - That creates both a name mismatch and a phone mismatch, plus duplicate-profile risk.

- **Facebook**
  - Facebook surfaced `Motor Inn of Carroll, LLC`.
  - Public snippet used `(712) 792-5000`, not the canonical line.

- **BBB**
  - BBB profile is for `Motor Inn Toyota of Carroll`.
  - Address matches the canonical address.
  - Primary phone shown: `(866) 804-3714`.
  - Additional phone shown: `(712) 790-1935`.
  - Website shown: `https://www.motorinntoyotaofcarroll.com/`.

- **CarGurus**
  - Listed as `Motor Inn of Carroll`.
  - Address shown as `1526 Le Clark Rd`.
  - Service phone shown as `(712) 792-5000`.

- **Yellow Pages**
  - Listed as `Motor Inn of Carroll`.
  - Website shown as `http://www.motor-carroll.gmpsdealer.com/`.
  - Phone shown as `(866) 804-3714`.

- **MapQuest**
  - Search surfaced `TOYOTA Rent-A-Car` as the primary entity at the dealership address with `Motor Inn Toyota of Carroll` secondary.
  - This is a weak / indirect citation and not a clean brand entity.

### Priority Fix List

#### P1 Critical

1. **Google Business Profile fragmentation**
   - URLs:
     - https://share.google/MYI84x4R5wq2JQYfX
     - https://share.google/olqo8h1hGSi9mepzk
   - What's wrong:
     - Two separate profiles are surfacing under franchise-specific names.
     - Combined profile call CTA uses `(712) 792-5000`, not canonical `(712) 522-2526`.
   - What it should say:
     - Canonical brand + canonical phone must align with the approved NAP source of truth.
   - How to fix:
     - Review GBP strategy for dual-franchise vs group entity.
     - Confirm which profile is primary for map-pack trust.
     - Normalize phone and landing URL rules before any edits go live.

2. **Facebook page mismatch**
   - URL: https://www.facebook.com/MotorInnofCarroll/
   - What's wrong:
     - Page name uses `Motor Inn of Carroll, LLC`.
     - Public snippet uses `(712) 792-5000`.
   - What it should say:
     - `Motor Inn Auto Group`
     - `(712) 522-2526`
   - How to fix:
     - Claim/update the business profile fields inside Meta Business Suite.

3. **Yelp mismatch + duplicate pattern**
   - URL: https://www.yelp.com/biz/motor-inn-of-carroll-service-carroll
   - What's wrong:
     - Unclaimed service listing.
     - Name mismatch.
     - Address uses `Rd`, not `Road`.
     - Phone shows `(866) 772-1687`.
   - What it should say:
     - `Motor Inn Auto Group`
     - `1526 Le Clark Road, Carroll, IA 51401`
     - `(712) 522-2526`
   - How to fix:
     - Claim the profile, merge duplicates if Yelp support confirms both live entities remain indexed.

4. **BBB mismatch**
   - URL: https://www.bbb.org/us/ia/carroll/profile/used-car-dealers/motor-inn-toyota-of-carroll-0664-32053421
   - What's wrong:
     - Name mismatch.
     - Primary and additional phone numbers do not match canonical NAP.
     - Website points to legacy Toyota microsite.
   - What it should say:
     - `Motor Inn Auto Group`
     - `(712) 522-2526`
     - `https://www.motorinnautogroup.com`
   - How to fix:
     - Update the BBB business profile after login / ownership verification.

5. **Yellow Pages mismatch**
   - URL: https://www.yellowpages.com/carroll-ia/mip/motor-inn-of-carroll-481777343
   - What's wrong:
     - Name mismatch.
     - Address abbreviation mismatch.
     - Phone mismatch `(866) 804-3714`.
     - Website mismatch `motor-carroll.gmpsdealer.com`.
   - What it should say:
     - Canonical NAP and main domain.
   - How to fix:
     - Claim/update YP profile or request correction through profile support.

#### P2 High

1. **Missing Bing Places**
2. **Missing Apple Maps**
3. **Missing indexed result for TrueCar**
4. **Missing indexed result for Autotrader**
5. **Missing indexed result for Cars.com**
6. **CarGurus name/phone mismatch**
7. **Carroll Chamber profile mismatch**

#### P3 Medium

1. DealerRater name mismatch.
2. IADA mention uses `Motor Inn of Carroll`, not canonical group name.
3. MapQuest entity is indirect and should be normalized if claimable.
4. Superpages entry appears present but still under the legacy name.

#### P4 Low

1. No indexed Manta listing.
2. No indexed Foursquare listing.
3. No indexed Citysearch listing.
4. No indexed Spirit Lake / Okoboji Chamber listing.

## Section 2: Backlink Profile Analysis

### Observed Local Authority Sources

| Domain | Links / Mentions Motor Inn? | Links / Mentions Champion Ford? | Links / Mentions Wittrock? | Links / Mentions Coleman? | Type |
|---|---|---|---|---|---|
| carrolliowa.com | Yes | Yes | Yes | No evidence found | Chamber / directory |
| iada.com | Yes | No evidence found | Yes | No evidence found | Industry association |
| carrollspaper.com | Yes | Yes | Yes | No evidence found | Local news |
| facebook.com | Yes | Yes | Yes | Yes | Social / entity reference |
| caredge.com | Yes | Not checked | Not checked | Not checked | Dealer profile / marketplace |

### Backlink Read

- Motor Inn is **not invisible** locally. It already appears on the Carroll Chamber, IADA, Carroll paper, and multiple social/entity sites.
- The bigger problem is **brand inconsistency**, not total absence.
- The cleanest remaining local-authority gap is **secondary market coverage** for the Spirit Lake / Okoboji service area. No clean Motor Inn citation or chamber result surfaced there.

### Priority Link / Mention Opportunities

#### Tier 1

1. **Spirit Lake / Okoboji Chamber presence**
   - Site: Spirit Lake / Okoboji chamber ecosystem
   - Type: chamber / community authority
   - Why it matters:
     - Spirit Lake and Okoboji are declared service areas, but no clear Motor Inn chamber citation surfaced.
   - Suggested approach:
     - Request either a member listing or supporting business profile that clearly connects Motor Inn Auto Group to the regional service market.
   - Draft outreach:
     - `Hi there — I’m reaching out for Motor Inn Auto Group in Carroll. We serve customers across Carroll and the Iowa Great Lakes area, and we’d like to confirm whether there’s a member or business listing option that includes our dealership details and website. If so, we can send the exact business information in your preferred format.`

2. **Normalize IADA naming**
   - Site: https://iada.com/milestone-anniversaries/
   - Type: association / industry entity source
   - Why it matters:
     - IADA currently shows `Motor Inn of Carroll`, not the canonical group name.
   - Suggested approach:
     - Request a profile/name normalization wherever IADA publishes dealer member information.
   - Draft outreach:
     - `Hi — we noticed our Iowa dealer mention is published under "Motor Inn of Carroll." Our approved business name for local SEO and directory consistency is "Motor Inn Auto Group." Could you point us to the right contact or workflow for updating that member display name?`

#### Tier 2

3. **Carroll Chamber cleanup**
   - Site: https://www.carrolliowa.com/dining-and-retail-in-carroll
   - Type: chamber / local directory
   - Why it matters:
     - The listing exists, but it still uses `Motor Inn of Carroll` and `(712) 792-5000`.
   - Suggested approach:
     - Keep the chamber link, but normalize the business presentation.
   - Draft outreach:
     - `Hi — we’re updating our business listings for consistency and noticed our chamber listing is still using "Motor Inn of Carroll" with an older phone number. Could we update it to "Motor Inn Auto Group" with (712) 522-2526 and our main site, motorinnautogroup.com?`

4. **Regional lake-market editorial coverage**
   - Site type: Spirit Lake / Okoboji regional news and business publications
   - Why it matters:
     - Competitors in the lakes market naturally accumulate local mentions; Motor Inn has weaker surfaced authority there.
   - Suggested approach:
     - Pitch community sponsorships, customer-service stories, dealership anniversaries, or local event support.
   - Draft outreach:
     - `Hi — Motor Inn Auto Group serves drivers from Carroll through the Iowa Great Lakes region, and we’d love to share any community partnership, event sponsorship, or customer-service milestones that fit your local business coverage. If helpful, we can send a short summary and approved details for review.`

#### Tier 3

5. **Dealer-profile cleanup on marketplaces**
   - Sites: CarGurus, DealerRater, Yellow Pages, MapQuest
   - Type: marketplace / citation / trust layer
   - Why it matters:
     - These are not premium editorial links, but they are still part of the prominence stack Google cross-references.
   - Suggested approach:
     - Treat them as authority hygiene, not vanity directory work.

### 90-Day Link Plan

#### Month 1: Easiest

1. Carroll Chamber listing correction
   - https://www.carrolliowa.com/dining-and-retail-in-carroll
2. IADA member naming correction
   - https://iada.com/
3. Yelp claim / merge workflow
   - https://biz.yelp.com/
4. Yellow Pages claim / correction
   - https://www.yellowpages.com/
5. BBB profile correction
   - https://www.bbb.org/

#### Month 2: Medium

1. Spirit Lake / Okoboji chamber listing request
   - Chamber/contact path to be confirmed during manual outreach
2. Regional lakes-market publication pitch
3. DealerRater profile claim / cleanup
4. CarGurus dealer profile normalization
5. MapQuest / Apple Maps / Bing Places entity cleanup

#### Month 3: Higher Authority

1. Secure a normalized IADA member mention/profile
2. Publish a local-newsworthy milestone story in Carroll or the lakes market
3. Add one community sponsorship page / recap that earns a local mention
4. Build one regional partnership mention in Spirit Lake / Okoboji
5. Re-audit search results after citation normalization to measure carryover

## Section 3: Search Intent Mapping

### Method

- Source keywords: `bofu_keywords` and `mofu_keywords` from `competitors.json`
- Added from prior July SEO planning: `car dealerships Carroll Iowa`, `auto service Carroll Iowa`, `best place to buy a used car in Carroll Iowa`, `should I buy new or used car Carroll Iowa`, `where to service Toyota Carroll Iowa`
- Coverage status based on current live sitemap plus July draft/page-package inventory
- Volume note:
  - No paid keyword tool was used.
  - Demand estimates below are **rough bands** derived from GSC visibility, internal priority tiers, and local commercial intent.

### Stage Summary

| Stage | Description | Keyword Count | Estimated Monthly Demand | Current Motor Inn Coverage |
|---|---|---:|---|---|
| 1 | Problem-unaware | 0 | 0-10 | No active target set in current competitor list |
| 2 | Problem-aware | 8 | 80-220 | Partial via blog/service content; several gaps remain |
| 3 | Solution-aware | 5 | 30-90 | Drafts exist for comparison / decision queries, not all live |
| 4 | Ready to hire | 13 | 200-500 | Strong partial coverage; July city/service packages directly address this cluster |

### Keyword Mapping

#### Stage 2: Problem-aware

- best trucks for farming Iowa
- Toyota Tundra review Iowa
- best family SUV Iowa
- car buying tips Iowa
- auto financing Carroll IA
- trade in value Carroll Iowa
- oil change Carroll IA
- car service Carroll Iowa

Coverage read:

- Live partial coverage exists via inventory, service, financing, and evergreen content.
- Better answer-first pages are already drafted in July packages for service and new-vs-used decision support.

#### Stage 3: Solution-aware

- Silverado vs F-150
- Champion Ford Carroll alternatives
- best car dealer Carroll Iowa
- should I buy new or used car Carroll Iowa
- best place to buy a used car in Carroll Iowa

Coverage read:

- `Silverado vs F-150` has partial live comparison-style support in older site content.
- July draft packages already target the strongest local decision queries.

#### Stage 4: Ready to hire

- car dealership Carroll IA
- car dealerships Carroll Iowa
- used cars Carroll Iowa
- new Chevy Carroll IA
- new Toyota Carroll Iowa
- Toyota dealer Carroll IA
- Chevrolet dealer Carroll IA
- GMC dealer Carroll Iowa
- Buick dealer Carroll IA
- used trucks Carroll IA
- Motor Inn Auto Group
- Motor Inn Carroll Iowa
- auto service Carroll Iowa

Coverage read:

- Live:
  - homepage
  - `/searchnew.aspx`
  - `/new-toyota`
  - `/new-chevrolets.html`
  - `/used-inventory`
  - `/used-trucks`
  - `/hours.aspx`
- Drafted / ready package:
  - `/car-dealerships-carroll-iowa`
  - `/toyota-dealer-carroll-iowa`
  - `/used-cars-carroll-iowa`
  - `/used-trucks-carroll-iowa`
  - `/auto-service-carroll-iowa`

### Top 10 High-Value Keywords by Intent

1. car dealerships Carroll Iowa
2. used cars Carroll Iowa
3. Toyota dealer Carroll Iowa
4. car dealership Carroll IA
5. auto service Carroll Iowa
6. used trucks Carroll IA
7. Chevrolet dealer Carroll IA
8. new Toyota Carroll Iowa
9. new Chevy Carroll IA
10. best place to buy a used car in Carroll Iowa

### Top 5 Stage 4 Keywords for the Next 90 Days

1. **car dealerships Carroll Iowa**
   - Target page: `/car-dealerships-carroll-iowa` (draft/package ready)
   - On-page changes:
     - Publish the July page package
     - Add homepage and used-inventory internal links
     - Align title/H1/meta to exact local-commercial phrasing
   - Off-page actions:
     - Chamber profile normalization
     - GBP name/phone alignment
     - Yellow Pages / BBB cleanup

2. **Toyota dealer Carroll Iowa**
   - Target page: `/toyota-dealer-carroll-iowa` (draft/package ready)
   - On-page changes:
     - Publish the July package
     - Link from `/new-toyota`, homepage, and service pages
     - Add FAQ support tied to Carroll buying/service questions
   - Off-page actions:
     - Fix Toyota-franchise citations now using legacy sub-brand names and non-canonical numbers

3. **used cars Carroll Iowa**
   - Target page: `/used-cars-carroll-iowa` (draft/package ready)
   - On-page changes:
     - Publish the July package
     - Link from `/used-inventory` and homepage
     - Add stronger Carroll-specific proof and CTA language
   - Off-page actions:
     - Normalize CarGurus, Yelp, and YP references

4. **auto service Carroll Iowa**
   - Target page: `/auto-service-carroll-iowa` (draft/package ready)
   - On-page changes:
     - Publish the July package
     - Link from service-area and hours pages
     - Add service FAQ + direct scheduling CTA
   - Off-page actions:
     - Clean Yelp service listing first
     - Normalize MapQuest / Apple Maps / Bing once claimed

5. **used trucks Carroll IA**
   - Target page: `/used-trucks-carroll-iowa` (draft/package ready)
   - On-page changes:
     - Publish the July package
     - Link from `/used-trucks` and high-traffic used inventory paths
     - Add rural-use proof points and Carroll-area relevance
   - Off-page actions:
     - Citation normalization across CarGurus / YP / chamber sources

## Section 4: Entity Optimization

### Knowledge Panel / Google Entity Read

- Google is surfacing local entity cards for:
  - `Motor Inn Toyota and Chevrolet of Carroll`
  - `Motor Inn Chevrolet of Carroll`
- The canonical brand `Motor Inn Auto Group` does **not** appear to own a single, consolidated local entity in Google.
- Current Google-visible signals are still franchise-specific and phone-fragmented.

### Wikidata Check

- No indexed Wikidata result surfaced for `Motor Inn Auto Group`.
- Recommendation: treat Wikidata as a future authority enhancement, not this month’s top priority.

### Homepage Schema Audit

Live site findings from `/tmp/motorinn-home.html`:

- Existing JSON-LD is present.
- Existing types include:
  - `AutomotiveBusiness`
  - `WebSite`
- Existing schema strengths:
  - correct main domain
  - correct canonical phone
  - correct full address
  - geo coordinates present
  - opening hours present
- Existing schema problems:
  1. **Name is `Motor Inn Auto`, not `Motor Inn Auto Group`.**
  2. **Primary type is `AutomotiveBusiness`, not `AutoDealer`.**
  3. **Description is Toyota-only** even though the business is Chevrolet + Toyota + Buick + GMC.
  4. `sameAs` currently includes citation URLs that are themselves inconsistent (`Yelp`, `CarGurus`) and may reinforce the wrong entity naming.

### Brand Consistency Check

Observed live naming variants in search:

- `Motor Inn Auto Group`
- `Motor Inn of Carroll`
- `Motor Inn Toyota of Carroll`
- `Motor Inn Toyota and Chevrolet of Carroll`
- `Motor Inn Chevrolet of Carroll`
- `Motor Inn of Carroll, LLC`
- `Motor Inn Auto`

Observed live phone variants:

- `(712) 522-2526` — canonical site/hours schema
- `(712) 792-5000` — GBP/Facebook/CarGurus snippets
- `(866) 804-3714` — BBB / Yellow Pages
- `(866) 772-1687` — Yelp service listing
- `(712) 790-1935` — BBB additional number

### Entity Optimization Plan

1. **Normalize first-party naming**
   - Keep `Motor Inn Auto Group` as the master brand.
   - Decide which franchise sub-brand names must remain public vs which should be retired from directory surfaces.

2. **Correct existing homepage schema**
   - Change main type to `AutoDealer`
   - Change `name` to `Motor Inn Auto Group`
   - Rewrite description for Toyota + Chevrolet + Buick + GMC
   - Remove inconsistent third-party `sameAs` references until their listings are corrected

3. **Use the corrected JSON-LD draft in**:
   - homepage
   - contact/hours page
   - Carroll city/service landing pages as they publish

4. **Defer aggregateRating markup**
   - Google rating data exists publicly, but it is not clearly stable on-page first-party content.
   - Safer to omit review schema until the implementation source is explicitly approved.

5. **Wikidata**
   - Nice-to-have, not urgent.
   - Only pursue after citation/name cleanup reduces entity ambiguity.

## Recommended Fix Order

1. Google Business Profile naming / phone / duplication review
2. Facebook correction
3. Yelp claim + merge
4. BBB correction
5. Yellow Pages correction
6. Carroll Chamber correction
7. Bing Places + Apple Maps creation/claim
8. CarGurus / DealerRater cleanup
9. Replace homepage schema with corrected `AutoDealer` version

## Outputs Created

- Report: `/Users/spencerheywood/motor-inn-seo/audits/local-authority/local-authority-2026-07.md`
- Schema draft: `/Users/spencerheywood/motor-inn-seo/content/drafts/schema/schema-2026-07.json`

---

Generated July 2, 2026 using Firecrawl + direct fetches in place of unavailable `gstack-browse`.
