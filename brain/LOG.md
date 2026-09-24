# Motor Inn — agent decision log (append-only)
Format: date | page/scope | change | search-side result | business-side result | verdict
Never delete entries. Wobble <2 weeks is ignored when judging.


## AI-Mode citation check 2026-09-23 (DFS $0.004, gap closed)
Query: 'best used truck dealer near carroll iowa' — Google AI Mode cites 12 dealer refs:
Choice Auto (1st), Wittrock, Pro Auto, Motor Inn Chevrolet Carroll (4th), Car Stop, Thiel,
Toms Trucks, Ascendance, Champion Ford, Motor Inn Toyota+Chevrolet (10th), New Way Ford, Farmer.
=> Motor Inn cited 2x/12 in AI answer. Choice Auto leads. Also: our GSC top-10 for
'car dealerships carroll iowa' does NOT include choiceauto/billionauto but AI Mode does.
Next: consistency hunt on the exact business details AI reads (hours/address/phone).


## NAP consistency check 2026-09-23 (DFS my_business_info, gap closed)
GBP (what AI Mode reads): 'Motor Inn Toyota and Chevrolet of Carroll' | +1712-792-5000 |
1526 Le Clark Rd, Carroll, IA 51401 | 4.6 stars / 225 reviews | category: Toyota dealer
Website footer: 1526 Le Clark Rd / 712-792-5000 -> MATCH.
Open item: 'Motor Inn Chevrolet Carroll' and 'Motor Inn of Carroll Iowa' queries return
NONE -> the Chevy store has no distinct GBP listing surfaced by name; hours null on GBP.
Action queued: verify Chevy-store GBP existence + add hours to GBP.

## Chevy GBP check 2026-09-23 (DFS my_business_info/live, item 3)
Observed requests: `Motor Inn Chevrolet Carroll` and `Motor Inn of Carroll Iowa`; both
returned no GBP items. The Toyota query surfaced `Motor Inn Toyota and Chevrolet of Carroll`
with phone +1712-792-5000, address 1526 Le Clark Rd, Carroll, IA 51401, category Toyota
dealer, 4.6 stars / 225 reviews, `work_hours: null`, and place ID
`ChIJlyzqdds57YcRbJmePnyLFYM`. The user-confirmed Chevy GBP exists, but these queries did
not surface it; hours remain not captured. Source: DataForSEO
`/v3/business_data/google/my_business_info/live` responses run via /tmp/nap_full.py.


## GAP CLOSURE 2026-09-23 (all EXM7777 gaps addressed)
1. GA4xGSC killer-page join: DONE (brain/killer_pages.py, first run in STATE.md)
2. brief/state/log trio: DONE (brain/BRIEF.md, STATE.md, LOG.md)
3. Competitor full-text scrape: DONE — free scraper + Firecrawl fallback, reusable
   brain/competitor_scrape.py; first read: brain/competitor-read-2026-09-23.md (7/7 pages)
4. AI-Mode citation check: DONE ($0.004) — Motor Inn cited 2 of 12 refs on
   'best used truck dealer near carroll iowa'; Choice Auto leads
5. NAP consistency: DONE — GBP matches site footer (1526 Le Clark Rd / 712-792-5000);
   OPEN: no distinct Chevy-store GBP surfaced; GBP hours null
6. One-change-per-tick + 2-week wobble rule + search+business judging: encoded in goal function STEP 0
REMAINING OPERATOR DECISIONS:
- Strongest-model pinning for weekly judgment runs (GLM-Flash now; his rule says judgment
  deserves the strongest model) — needs Spencer's model choice
- Free Google API key for PageSpeed (or accept Lighthouse CLI locally)
- Chevy-store GBP listing verification (may need Spencer's Google login)

## C6 CLOSED 2026-09-23 13:20 CT
Codex computer-control confirmed in GSC UI (Settings -> Ownership verification):
'You are a verified owner' — HTML tag successfully verified for
https://www.motorinnofcarroll.com/. Spencer's 09-22 click did it. C6 = DONE.
All 3 dealerships in GSC. Remaining SA access: share Chevy property with
ga4-service-account (siteUnverifiedUser -> siteFullUser) — one click in
Settings -> Property access management, add jeeves SA email as Full user.


## GOAL COMPLETE 2026-09-23 (tick 10)
C1-C6 all verified live; C6 Chevy GSC confirmed by automated probe (GSC "You are a
verified owner / HTML tag — Successfully verified", codex CC, commit fded226).
MOT-3222 + MOT-3223..3227 all moved to Done. Loop closed; cron job to be removed.
Follow-ups parked (not part of this goal): SA delegated-owner invite for Chevy GSC;
Chevy-store GBP listing verification + GBP hours (open item from NAP check).

## Case 01921765 (single H1 vehicle title on used VDP template) — VERIFIED 2026-09-24
Requested: exactly one <h1> per used-VDP, containing the vehicle year/make/model/trim.
Verified via Firecrawl-rendered DOM on 3 LIVE VDPs (URL pattern /used-Carroll-<y-m-m-t>-<VIN>):
- 2009 Ford Escape Hybrid -> h1 count 1, h1 '2009 Ford Escape Hybrid'
- 2018 Chevrolet Silverado 1500 LT (x2 VINs) -> h1 count 1, h1 = vehicle title
NOTE: earlier confusion was from DEAD VIN-URL pattern (/used/<VIN> 301s to /used-inventory
after vehicle rotation) — old URLs are not the template's live state.
VERDICT: fix is correct and complete. Safe for Spencer to click Confirmed.

## Case 01921720 (301 redirects, 4 legacy paths) — VERIFIED 2026-09-24
Requested (MOT-3224): 301 each legacy 404 to its live successor.
Live results (curl + http.client, both methods agree):
- /inventory          -> 301 -> /used-inventory      [200, self-canonical confirmed]
- /used-vehicles      -> 301 -> /used-cars           [200]
- /specials           -> 301 -> /newspecials.html    [200]
- /service-department -> 301 -> /service-locations.html [200]
All permanent 301s, single hop (no chains), targets live 200s, /used-inventory carries
self-referencing canonical (no soft-404 template). VERDICT: correct — safe to Confirm.
Matches goal-loop C2 PASS evidence from 2026-09-23 tick.
