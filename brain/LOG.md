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

## GSC ALERTS 2026-10-07 (both = Chevy motorinnofcarroll.com)
Alert 1: 'Not found (404)' — pages listed IN A SITEMAP.
Alert 2: 'Soft 404' — separate batch, pages returning 200 w/ thin/no-result content.

ROOT CAUSE (verified live): sitemap generator double-escapes spaces in vehicle URLs —
emits literal '&#x2B;' instead of '+', e.g.
/new-Lake&#x2B;City-2027-Chevrolet-Equinox-ACTIV-<VIN> -> Googlebot 404.
51/164 Chevy sitemap URLs affected. SAME BUG on Toyota (97/225) + Auto Group (59/235)
sitemaps — expect identical alerts there.
The un-escaped variants return 200 (pages exist; only the sitemap syntax is broken).
Soft 404s: separate, needs GSC UI export to enumerate (SA lacks delegated access on
Chevy property — Spencer must add ga4-service-account as user, 1 click).

DRAFT EMAIL (one issue: sitemap entity escaping) saved:
pipeline/drafts/2026-10-07-gsc-sitemap-x2b-draft.md
## 2026-10-07 — soft404-chevy
- GSC URL-prefix property motorinnofcarroll.com (spencer.heywood@motorinnmail.com): soft-404 count 1, example URL windowstickernotfound.pdf, first detected 3/25/23.
- Curl: placeholder served HTTP 200 as 65KB PDF; pdftotext yields blank page (no vehicle info).
- Same placeholder 200 on motorinnautogroup.com and motorinntoyotaofcarroll.com.
- Diagnosis: DealerOn window-sticker component serves "not found" placeholder PDF at 200 instead of 404/410.
- Deliverables: brain/soft404-chevy-2026-10-07.md + pipeline/drafts/soft404-fix-draft.md (email to help@dealeron.com — draft only, not sent).

## DEAL BADGES case 01923978 -> new case 01940814 (2026-10-07)
DealerOn (Josh Meyer) asked for: (1) badge images list, (2) tag verbiage per image.
REPLIED with spec (1a117b25de9bb456, acked as case 01940814):
- feed field badge_code: GREAT_DEAL | GOOD_DEAL | FAIR_DEAL | PRICE_ANALYSIS | blank
- ribbon mapping + placement (card overlay + VDP hero), blank = no badge
- source: nightly vAuto market rating; staged verification before go-live
Also note: sitemap x2B case 01940542 = only acks so far (no fix yet).
Pending DealerOn: sitemap generator fix; badge feed field; soft-404 404/410 change
(draft staged, NOT sent - pipeline/drafts/soft404-fix-draft.md).

## CORRECTION 2026-10-07: case 01940542 subject entity issue
Original subject contained literal HTML entity -> DealerOn ticket title rendered escaped
('&amp;#x2B;'). Follow-up sent with clean subject + plain-English bug restatement
(no entities in subject/body), same fix request. 1a117ba4008ea7ac.
Lesson: never put HTML entities in email subjects to ticketing systems.

## BING WEBMASTER SUBMISSION 2026-10-11
Attempted full automation: AppleScript blocked (JS-from-AppleEvents off, GUI toggle flaky),
CDP found hermes-workspace chrome on :19222 (wrong profile), playwright+Default profile works.
BWT login required: Google chooser shows remembered bingwebmaster17@gmail.com but session
stale -> password entry needed (agent must not type passwords per rule).
NEEDS SPENCER (10s): sign in at bing.com/webmasters with Google -> bingwebmaster17@gmail.com
in Chrome. Then rerun /tmp/bing_pwJ successor to submit 3 sitemaps (script ready).
Alternative: BWT API key from that account -> creds to ~/.config/motorinn/bing.env for
repeatable API submissions (preferred long-term; enables ping + submission cron).
## TARGETS 2026-10-22 set; Monday cycle takes #1 contactus


## HOLMBERG SPRINT 2026-10-22: all 5 targets drafted
Writer = our own llama-class server GLM-5.3-Flash-EXL3 @ spark-a664:100.67.25.103:8888
(only live local gen model; Emily's spark down, studio down). Voice DNA + anti-slop +
NEEDS-VERIFY flags enforced via prompt; phone entity post-fixed.
Drafts+reviews: content/drafts/seo/{contactus-money-page,trim-levels-explained,
highlander-vs-grand-highlander,used-trucks-carroll,testdrive-page}-draft.html (+-REVIEW.md).
NEXT: Spencer reviews 5 packages; on approve -> publish path per page ownership
(DealerOn cases for .aspx pages; direct for static if editable).

## 2026-10-22: all 5 drafts emailed to Spencer for review (1a166a12bab9acbb)

REMAINING FACTS I COULD NOT VERIFY (only 3, all optional-to-publish):
1. Trade appraisal walk-in policy (draft says 'no appointment needed' - TRUE?)
2. Financing structure: in-house dept vs lender network only; 'bad credit ok' wording
3. Test drive: license/insurance requirement + is 30 min the honest duration?
(Emily will design around these; final wording can be locked at DealerOn case stage.)

## OWNER ANSWERS APPLIED 2026-10-23 (bbcf03f)
1. Trade walk-in: confirmed -> kept
2. Financing: lender-network only; 'bad credit' references stripped
3. Test drive: no license/insurance mention; 'at your convenience' framing
All NEEDS-VERIFY converted to BUILD-NOTE (Emily resolves OEM specs/inventory at build).
Kanban t_92537575 commented w/ final copy constraints. Copy LOCKED; Emily designing.

## DESIGNS IN 2026-10-23 (Emily t_92537575 complete)
5 self-contained DealerOn-matched pages verified on disk (1 H1 each, 0 flags, CTAs OK).
Patched: phone added to highlander CTA. Installed repo content/ready-design/ commit 2e2e3f9.
Emailed zip+summary to Spencer for visual review (1a16903e23a7b2f6).
NEXT: Spencer go/change per page -> DealerOn cases (aspx) + publish path (static).

## DEALERON PUBLISH REQUESTS SENT 2026-10-23 (3 pages, one issue per email)
- trim-levels-explained: 1a169755d4d452ac
- highlander-vs-grand-highlander: 1a169756282f92c0
- used-trucks-carroll: 1a1697567d479e20
Each: replace body content of existing URL, final HTML attached, verify step included.
Contact + testdrive drafts remain with Spencer (not yet approved for publish).

## PANEL 2026-10-23T12:28 target=/tmp/plan_under_test.md mean=90
- Technical SEO Specialist: 91 | Data-backed, correctly prioritized queue with honest traps and a clear money-page focus; minor verification gaps keep it from 95+.
- Content Strategist: 91 | Rare queue that leads with the money page and cites real GSC numbers per item, but the verification gaps (page ownership, AI-citation play) 
- Conversion Rate Optimizer: 91 | Rare plan that leads with the money page and names exact queries, positions, and event counts — but the conversion path from #2's traffic is
- Revenue Attribution Expert: 91 | Rare queue where every item cites real GSC numbers, ties to a named conversion event, and names its traps — the weakest link is the unverifi
- Competitive Analyst: 88 | Strong data-backed queue with clear lead logic, but the competitive play against Choice Auto's AI-citation lead is asserted, not evidenced, 
- AI/AEO Specialist: 91 | Data-grounded, conversion-tied queue with correct lead-first prioritization; only soft spot is the AI-citation outreach play being named but
- Data Scientist: 84 | Strong data-backed queue with clear lead logic, but several claims lack verification and the statistical windows/n-sizes are unstated.
- Growth Hacker: 91 | Ruthlessly prioritized, data-backed queue with honest traps and a clear money-page focus; only soft spot is unverified page ownership and a 
- Operations Expert: 88 | Strong, data-backed queue with real GSC numbers and correct 51401 focus, but the "VERIFY ownership" on #2 and the Choice Auto outreach are u
- ROI Calculator: 91 | Rare queue where every item cites real GSC counts, names the exact fix, and ties to lead events — the weakest link is the unverified page ow

## WIRE-UP COMPLETE 2026-10-23 (codex audit items 1-3)
1. keyword-gap: brain/gap_run.py v2 (correct DFS element semantics); FIRST RUN = 138 gaps
   (choiceauto 25, wittrock 22, proautosales 13, billionauto 82). Weekly Mon 7am launchd
   com.motorinn.seo.weekly-intel. NOTE: geo-tightening (metro terms) = next iteration.
2. ai-visibility: FIRST RUN baseline saved (brain/ai-visibility/). Key insight: 'best dealer'
   queries = 0% ours (local pack), brand/service = 100%. Fix = outreach/listings play.
3. weekly report #1: brain/reports/week-2026-10-23.md.
All three wired into launchd; goal loop consumes artifacts.

## MIGRATION 2026-10-23: weekly-intel -> Mac Mini 2 (per Spencer)
- workMac: 41 commits pushed (rebase over mini GBP history), launchd job UNLOADED
- mini: repo pulled current; creds copied to ~/.config/motorinn/dataforseo.env;
  launchd com.motorinn.seo.weekly-intel LOADED + kickstart VERIFIED (own run, own commit bf0da85)
- schedule: Mondays 7am CT on mini. Gap+AI-vis artifacts & commits now originate on mini.

## CODEX 3-TASK RUN COMPLETE 2026-10-27 (Brooks thread gaps)
1. feed.json: proxy branch feed-json (commit ce0ff09, 65 tests pass). NOT deployed - awaiting
   Spencer approval. Spec: brain/FEED-API.md. Deploy = merge + EC2 redeploy.
2. datestamp: content/ready-datestamp.html + amendment draft
   pipeline/drafts/datestamp-amendment-draft.md (NOT sent).
3. AI referrals: brain/ai-referrals.md (segment def + API call) + working brain/ai_referrals.py
   -> chatgpt.com 7 sessions/28d BASELINE. Hooked into weekly-report runbook?
   (verify grep above). Weekly report will carry the section.

## AI-BUILDERS BATCH COMPLETE 2026-10-28 (codex, 4 features)
A. /inventory.md per-site endpoint on proxy feed-json branch (bbb1d35) - live inventory as
   markdown, daily cache; sitemap+llms linked. Deploy w/ feed-json (pending Spencer).
B. AI-visits dashboard: brain/reports/ai-visits-latest.html (per-source table+sparkle css),
   generator wired into weekly intel.
C. Answer-page factory: brain/ANSWER-PAGES.md (3 ranked patterns + panel gate + link rules);
   first 3 ownership drafts: silverado-towing, tahoe-family, highland-roadtrip
   (content/drafts/seo/) - approval queue next.
D. Crawlability audit: 0 JS-only vehicle URLs on all 3 sites - no DealerOn case needed;
   artifact brain/reports/inventory-crawlability-audit.md.
Vinindex note: paid syndication service - skipped; our proxy+feed covers the same surface.

## DEPLOYED 2026-10-28 (codex): feed.json + inventory.md LIVE on all 3 ai. mirrors.
Verified: 200s across the matrix. Fixes during deploy: chevy 502 (container), feed route.
Also merged feed-json branch to codex/feed-json-main (40ab716). Email w/ preview links +
zip of 5 final designs sent (1a184101e4bd7c9f). Pending Spencer: contact/testdrive go;
DealerOn 3 publishes in flight; datestamp amendment rides next contact.
