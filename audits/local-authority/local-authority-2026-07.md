# Local Authority Audit — November 2026

**Run date:** 2026-11-02 · **Method:** direct fetches + signed-out browser checks (gstack-browse) + Google Maps public data + GBP API pull of 2026-10-29. No paid tools.
**Exa seed research:** the deep-research helper was not runnable inside this cron window; the July 2026 standards snapshot (relevance / distance / prominence; citation consistency > count; entity consistency for AI answers) remains the working standard and was re-confirmed structurally this run. Flagged as a process gap, not a data gap.

## Canonical NAP (source of truth)

- **Name:** Motor Inn Auto Group
- **Address:** 1526 Le Clark Road, Carroll, IA 51401
- **Phone (canonical per runbook):** (712) 522-2526
- **Website:** https://www.motorinnautogroup.com

**Operating-phone note (verified via GBP API 2026-10-15, still current):** Carroll combined line is **(712) 792-5000**; Carroll Chevrolet **(712) 882-7802**; Spirit Lake **(712) 336-2701**. The 522-2526 line does **not appear anywhere on the live site** (0 occurrences, verified 2026-11-02). Until Spencer rules which number is customer-facing truth, every phone delta below is recorded against **both** references, not "fixed" unilaterally.

## Executive summary

- **Citation health:** 3 of 22 platforms fully consistent; 12 carry a phone/name/website mismatch; 3 confirmed missing; 4 unverifiable this run (DataDome/captcha walls).
- **Entity status:** Google surfaces **four** separate local entities at one address; the group brand has no consolidated panel. No Wikidata entry. Homepage schema still says "Motor Inn Auto" / AutomotiveBusiness with a **literal-masked phone** (`+171****5000`) — a real bug shipped to crawlers.
- **Worst finding (P1):** the homepage JSON-LD `telephone` value is the literal string `+171****5000`. Every consumer of that schema — including AI answer engines — reads a masked phone.
- **Second (P1):** live schema name is `Motor Inn Auto` and type `AutomotiveBusiness`; the corrected `AutoDealer` draft has sat in drafts since July, unshipped.

## Section 1 — Citation audit

| # | Platform | Listed | Name | Address | Phone | Website | Notes |
|---|----------|--------|------|---------|-------|---------|-------|
| 1 | Google Business Profile | Yes | ❌ 4 variants | ✅ 1526 Le Clark Rd | ❌ (712) 792-5000 on all | ✅ | 4 entities at one address (see §4). Toyota entity 254 rev / 4.6; Chevy 37 / 4.8 (GBP API 10-29). |
| 2 | Yelp | Yes | ❌ "Motor Inn Toyota of Carroll" | ❌ "Le Clark Rd" abbrev. | ❌ service listing (866) 772-1687 (July; re-verify) | ? | **DataDome captcha blocked re-verification this run** — July findings carried, flagged stale. |
| 3 | Bing Places | Unverified | — | — | — | — | Maps UI requires WebGL (disabled in headless); organic SERP gave no panel. Re-check manually. |
| 4 | Apple Maps | Yes | ❌ "Motor Inn Toyota of Carroll" | ❌ "1526 Le Clark Rd" | ❌ +1 (866) 804-3714 | ❌ motorinntoyotaofcarroll.com | 1 rating. Place-id IAACB9ED6DF52F9A5. |
| 5 | Facebook | Yes | ✅ "Motor Inn Auto Group" | not public w/o login | not public w/o login | ✅ motorinnautogroup.com | 1K followers; 66% recommend (6 reviews). About page hides phone/address from logged-out view. |
| 6 | BBB | Carry | ❌ "Motor Inn Toyota of Carroll" | ✅ | ❌ (866) 804-3714 + (712) 790-1935 | ❌ motorinntoyotaofcarroll.com | July data carried; BBB 403'd curl and served interstitial to headless. |
| 7 | Cars.com | Unverified | — | — | — | — | no indexed result surfaced (July + this run) |
| 8 | CarGurus | Yes | ❌ "Motor Inn of Carroll" | ❌ "1526 Le Clark Rd" | ⚠️ Sales **(980) 480-8309** (out-of-area!); Service (712) 792-5000 | indirect | **88 cars listed.** 2 reviews. Sales line is a North Carolina area code — near-certainly a tracking number. |
| 9 | Autotrader | Unverified | — | — | — | — | no result surfaced |
| 10 | DealerRater | Carry | ❌ sub-brand (July) | ? | ? | ? | not re-verified this run |
| 11 | Edmunds | Carry | ❌ sub-brand (July) | ? | ? | ? | not re-verified |
| 12 | TrueCar | Unverified | — | — | — | — | no result surfaced |
| 13 | Yellow Pages | Carry | ❌ "Motor Inn of Carroll" | ❌ | ❌ (866) 804-3714 | ❌ gmpsdealer.com | Cloudflare blocked re-pull; July data carried. |
| 14 | Manta | Unverified | — | — | — | — | |
| 15 | Foursquare | Unverified | — | — | — | — | |
| 16 | Superpages | Carry | ❌ (July) | ❌ | ? | ? | |
| 17 | Citysearch | Unverified | — | — | — | — | |
| 18 | MapQuest | Carry | ❌ Toyota Rent-A-Car primary (July) | ✅ | ? | ? | weak/indirect |
| 19 | Iowa ADA | Partial | ❌ "Motor Inn of Carroll" (July) | — | — | — | **Changed:** legacy milestone-anniversary URL now redirects to news; member directory moved online-only (IADA news 2025-09-22). Re-claim path changed. |
| 20 | Carroll Chamber | Yes | ❌ **"Motor Inn of Carroll"** | ⚠️ "1526 Le Clark Rd" | ❌ **712.792.5000** | — | Verified live 2026-11-02 on carrolliowa.com dining-and-retail page. |
| 21 | Okoboji Chamber | Yes(dir) | ? | ? | ? | ? | Directory lives at members.okobojichamber.com/directory (CF-gated); Motor Inn presence unconfirmed this run. |
| 22 | Carroll Times Herald | News only | "Motor Inn" (news) | — | — | — | Nov 2026: President's Award coverage names sub-brand `Motor Inn Toyota of Carroll` in headlines. No structured business directory found. |

**Verified-consistent count: 3** (Facebook name+website; Toyota GBP address; homepage schema address/geo). Everything else deviates on at least one field.

### Inconsistencies found: 12 confirmed (plus 6 unverified)

### Priority fix list

**P1 — wrong phone / broken schema (trust-setting surfaces)**
1. **Homepage schema telephone is literally `+171****5000`** — asterisks are in the served JSON-LD. Fix in DealerOn template: set `telephone` to the ruling customer line. *Blocking decision: 792-5000 vs 522-2526 (see note above).*
2. **CarGurus sales phone (980) 480-8309** — out-of-state area code on a Carroll dealer profile. Verify whether it's a call-tracking number Spencer recognizes; if not, correct to the Carroll line.
3. **BBB + Apple Maps + Yelp still publish (866) 804-3714 / (866) 772-1687** and the `motorinntoyotaofcarroll.com` micro-site as primary — three Tier-1 adjacent surfaces disagree with the main site.
4. **Facebook about-page contact fields empty for logged-out viewers** (email + website only). Add the ruling phone + full address in Page info; it is a knowledge-panel input.

**P2 — missing from Tier 1/2**
5. Bing Places — unverified/likely unclaimed; Apple Maps place is claimable ("Claim This Place" shown) and carries wrong phone.
6. Cars.com / Autotrader / TrueCar dealer profiles — none surfaced; inventory syndication likely exists via vendor, but profiles need claiming for NAP control.

**P3 — name variants**
7. Carroll Chamber: "Motor Inn of Carroll" → "Motor Inn Auto Group" (live-verified diff).
8. CarGurus: "Motor Inn of Carroll" → group name; address abbreviation `Rd` → `Road`.
9. IADA: naming normalization request must route through the **new** online member directory, not the dead milestone page.

**P4**
10. MapQuest entity is still "Toyota Rent-A-Car"-adjacent; Manta/Foursquare/Citysearch unclaimed.

## Section 2 — Backlink profile

**Method note:** Bing/DDG/Google SERPs bot-wall-locked this run (Google captcha; DDG anomaly loop; Bing served generic unquoted results to headless UA). Link discovery is **qualitative + carried baselines**; no count claims.

| Domain | Motor Inn? | Champion? | Wittrock? | Coleman? | Type | Status |
|---|---|---|---|---|---|---|
| carrolliowa.com (Chamber) | ✅ listing | ✅ | ✅ | ? | chamber | name+phone need fix (P1-adjacent) |
| iada.com | ⚠️ legacy mention | ? | ✅ (July) | ? | association | directory moved online — re-engage |
| carrollspaper.com | ✅ news (President's Award, Nov 2026) | ✅ | ✅ | ? | news | **fresh earned mention this month — leverage it** |
| facebook.com | ✅ | ✅ | ✅ | ✅ | social | consistent name — good |
| okobojichamber.com | ? unconfirmed | ? | ? | ? | chamber | CF-gated; verify membership listing |
| vinindex.ai | ✅ (badge/MCP links on site) | ? | ? | ? | vendor | new since July — vendor profile page exists |

**New since July:** carrollspaper.com President's Award story (3rd straight year) is live and names the sub-brand. Highest-value ask this month: get the **group name** into the follow-up. Also new: vinindex vendor profile.

### 90-day link plan (unchanged priorities, updated targets)

- **Month 1 (easy):** 1) Carroll Chamber listing correction (name+phone) · 2) IADA online-member-directory re-claim · 3) BBB phone correction · 4) Apple Maps claim + phone fix · 5) Bing Places claim.
- **Month 2 (medium):** 1) Okoboji chamber membership-listing verification via members portal · 2) Pitch a follow-up to the Times Herald President's Award story under the group name · 3) DealerRater claim/cleanup · 4) CarGurus profile normalization (incl. sales-phone fix) · 5) MapQuest entity cleanup.
- **Month 3 (authority):** 1) IADA normalized member profile live · 2) lakes-area news feature · 3) one community-sponsorship mention · 4) Spirit Lake partnership mention · 5) re-audit after fixes.

## Section 3 — Search intent mapping

Keyword universe unchanged from July (13 BoFu + 9 MoFu + 5 alternatives; no new keyword source this run — GSC export not in cron scope).

| Stage | Count | Est. monthly demand | Coverage |
|---|---|---|---|
| 1 problem-unaware | 0 | 0–10 | none targeted |
| 2 problem-aware | 8 | 80–220 | partial (blog/service) |
| 3 solution-aware | 5 | 30–90 | drafts exist, partially live |
| 4 ready-to-hire | 13 | 200–500 | **city pages now LIVE** (verified in sitemap 2026-11-02: `/car-dealerships-carroll-iowa`, `/toyota-dealer-carroll-iowa`, `/used-cars-carroll-iowa`, `/used-trucks-carroll-iowa`, `/auto-service-carroll-iowa`) |

**Delta vs July: the five draft page packages are published.** That closes the July "publish the package" action item. Remaining Stage-4 work is internal-linking + citation reinforcement, not creation.

### Stage-4 priorities (next 90 days)

1. **car dealerships Carroll Iowa** — live; add homepage + used-inventory links; align title/H1 (verify shipped copy).
2. **Toyota dealer Carroll Iowa** — live; link from `/new-toyota` + service; fix Toyota-franchise citations (Apple/BBB/Yelp still sub-brand).
3. **used cars Carroll Iowa** — live; link from `/used-inventory`; CarGurus/YP normalization feeds this.
4. **auto service Carroll Iowa** — live; link from hours/contact; Yelp service-listing cleanup is the off-page blocker.
5. **used trucks Carroll IA** — live; rural-proof-point copy check; chamber/citation normalization.

## Section 4 — Entity optimization

### Knowledge panel / entity state (Google Maps, verified 2026-11-02)

Four co-located entities:
1. **Motor Inn Toyota and Chevrolet of Carroll** — Toyota dealer
2. **Motor Inn Chevrolet of Carroll** — Chevrolet dealer
3. **Motor Inn Auto Group** — *Auto repair shop* category (!), 5.0
4. **Motor Inn Auto Group** — Toyota dealer, **no reviews**, phone **(888) 698-6447**

All four: 1526 Le Clark Rd, (712) 792-5000. **Finding:** the group-name entity is categorized as a repair shop, and a second group-name shell exists with an 888 number and zero reviews — duplication inside the brand itself. This is the fragmentation Spencer was warned about in July, now with a cleaner map.

**Wikidata:** still no entry (`wbsearchentities` = 0 hits, verified 2026-11-02). Defer per July ruling — after citation cleanup.

### Schema audit (live, 2026-11-02)

| Check | Home | City page | /used-inventory | /hours | VDP |
|---|---|---|---|---|---|
| LocalBusiness/AutoDealer | ⚠️ AutomotiveBusiness, name "Motor Inn Auto", tel `+171****5000` | same | same | same | — |
| WebSite + SearchAction | ✅ | ✅ | ✅ | ✅ | — |
| FAQPage | — | ✅ (2 graphs) | — | — | — |
| ItemList (inventory) | — | — | ✅ | — | — |
| Vehicle + offers | — | — | — | — | ✅ but `offers.availability` **empty string** |
| BreadcrumbList | ❌ | ❌ | ❌ | ❌ | ❌ |
| AggregateRating | ❌ everywhere (correct per July ruling: defer) | | | | |

**Schema bugs to ship (all in the corrected draft):**
1. `telephone: "+171****5000"` → real number (literal asterisks in production JSON-LD).
2. `name: "Motor Inn Auto"` → `Motor Inn Auto Group`; `@type` → `AutoDealer`.
3. Description Toyota-only → four-brand (draft copy ready since July).
4. VDP `offers.availability` empty → `InStock`/`InStoreOnly` per live status.
5. No BreadcrumbList anywhere — add on city + inventory templates.
6. `sameAs` still carries the inconsistent Yelp/CarGurus URLs — keep only after those listings are fixed, per July plan (draft already trimmed these).

**Corrected JSON-LD:** `content/drafts/schema/schema-2026-11.json` (unshipped; Spencer/Dev implements).

### Brand consistency (live observations)

- Names in the wild: `Motor Inn Auto Group` ✅ (site, FB, LI) · `Motor Inn Toyota and Chevrolet of Carroll` · `Motor Inn Chevrolet of Carroll` · `Motor Inn of Carroll` (chamber, CarGurus, IADA legacy, Times Herald photo captions) · `Motor Inn Toyota of Carroll` (Apple, BBB, Times Herald headline) · `Motor Inn Auto` (own schema!).
- Phones: 792-5000 (GBP/FB-adjacent/CarGurus-service/chamber) · 522-2526 (canonical per runbook; **absent from live site**) · 882-7802 (Chevrolet line) · 866-804-3714 (BBB/Apple) · 866-772-1687 (Yelp svc, July) · 790-1935 (BBB add'l) · 980-480-8309 (CarGurus sales) · 888-698-6447 (duplicate GBP shell). **Eight phone variants across surfaces.**

### Authoritative profiles

- LinkedIn ✅ (89 followers, name correct). Instagram/Pinterest/YouTube referenced in schema — not audited this run.
- Iowa SOS: JS/CF-gated; entity status unverified (P4).

## Action items (next 30 days)

1. **Decide the customer-facing phone** (792-5000 vs 522-2526) — every fix keys off this. *Spencer decision.*
2. Ship schema-2026-11 (fixes masked phone, name, type, availability; adds nothing risky).
3. Facebook: add phone + address to public About.
4. CarGurus: verify/replace the (980) sales line; normalize name/address.
5. Apple Maps: claim place IAACB9ED6DF52F9A5; correct phone/website.
6. BBB: phone correction request.
7. Carroll Chamber: name/phone correction request (draft in July report §Month-1).
8. Merge/kill the review-less `(888) 698-6447` GBP shell or repurpose it as the canonical group entity — needs a ruling, not an agent edit.
9. Re-run Yelp/Bing/SOS checks from a non-headless session (captcha-limited this run).

## Escalation check (per runbook)

- 3+ Tier-1 wrong-phone surfaces? **Yes** (BBB, Apple, Yelp-carry) → flagged above, not silent.
- Knowledge panel wrong info? **Yes** — group entity filed under "auto repair shop" + duplicate shell.
- Competitor 5+ link gap? No new evidence (SERP tools down); carried July read.

## Method / data-quality notes

- Live-checked this run: motorinnautogroup.com (home/city/inventory/hours/VDP/sitemap), Google Maps entities, Apple Maps place, CarGurus profile, Facebook page+about, carrolliowa.com, carrollspaper.com search, IADA news/milestone, LinkedIn, Wikidata API, GBP review totals (10-29 pull: 254/4.6 + 37/4.8).
- Captcha/bot-wall blocked (recorded, not guessed): Yelp (DataDome), BBB (interstitial), YellowPages (CF), Bing Places (WebGL), Iowa SOS (CF), members.okobojichamber.com (CF). Google SERP captcha; DDG anomaly loop; Bing quoted-query failure on headless UA. **July values for these are carried and marked.**
- No citation was edited; no listing claimed; documentation only, per runbook.

---
Generated 2026-11-02 (cron, Mac Mini 2 path) — direct fetches + signed-out browser; gstack-browse unavailable-as-documented pattern repeated.
