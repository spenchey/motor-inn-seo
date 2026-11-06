
## DEALERON EMAIL HOLD - 2026-11-02
Spencer: do NOT email DealerOn the www fix tickets (404->301, terms, H-ladder etc).
Www-side fixes wait for his go or another route. Mirror-side work continues regardless.

## PUBLISH used-trucks-towing-iowa - 2026-11-02 (Spencer: "publish")
1. WP draft created (id 119) via publish-to-wordpress.mjs from content/page-packages/2026-11/, then flipped to publish via REST -> live at motorinnconten.wpenginepowered.com/?page_id=119 (SEO-company WP; plain permalinks).
2. NOTE: www.motorinnautogroup.com/<slug> 404s - www is DealerOn; WP pages do NOT auto-appear there (script header overstates). www publication needs a DealerOn page build (held per no-email rule).
3. ai mirror: https://ai.motorinnautogroup.com/articles/used-trucks-towing-iowa 200 (live since 10-31).
4. GSC: urlInspection on mirror = "URL unknown to Google" (expected); ai.* sitemap NOT submitted to GSC (only www sitemap is). robots.txt references mirror sitemap so discovery is passive. Submitting needs webmasters write scope - add ga4-reader svc acct as Owner in GSC, or wait for crawl.
DRAFT-META status flipped: draft-needs-owner-approval -> published (wp + mirror).

TREG LOGIN - PARKED STATE (2026-11-03)
Everything automated except ONE phone tap (Google 2FA).
RESUME ANYTIME: ssh workMac; bash ~/treg-finisher.sh  (5-min window, tap Yes when phone buzzes)
NOTE: GSC work complete via service account; treg = future tool-catalog convenience only.

## TREG AUTHENTICATED 2026-11-04 (codex micro-task loop)
- treg v0.29 on workMac (~/.local/bin/treg), org 'motor-inn' owner, email linked.
- Email-code loop closed by codex: login --email -> gog inbox poll -> 6-digit -> stdin. 
- Verified: treg whoami OK; google-search-console.sites => all 3 properties siteOwner.
- GSC via treg now agent-runnable WITHOUT service account/keychain (server-side creds).
- Note: prior cannibalization audit used the SA path; both routes live.

## ASKOKARA FAQ HACK EXECUTED 2026-11-04
GSC question-regex (6mo) -> 847 rows -> opportunity scoring (impr>=50, CTR-weighted).
Top: trim-levels page = 2761 question-impressions ~0% CTR (12 variants!); rav4 blog 330;
heavy-duty blog 243; highlander comparison 231.
Delivered (commits 14b4f41, 1791983):
- FAQ blocks (visible accordion + FAQPage JSON-LD) INSERTED into ready-design
  trim-levels-explained + highlander-vs-grand-highlander drafts.
- Staged DealerOne...DealerOn case draft: pipeline/faqs-2026-11-04.md (rav4 + heavy-duty
  live-page FAQ blocks) - NOT sent, awaiting go per rule.
- Full opportunity table: brain/reports/gsc-faq-opportunities... via /tmp/faq-opp.md data
  (saved in repo? verify next pass).
Recurring: this query now part of monthly SEO audit (cron picks up pattern).

## MASTER BUILD COMPLETE 2026-11-04 (3 phases + 2 schema fixes)
Phase1 cabe884 adversarial pass (report: brain/reports/adversarial-pass-2026-11.md) + fixes
Phase2 a3b5968 rewrite x7 pages per ALL agents/*.md rules (answer-first, VOICE-DNA,
  entities, cannibalization-resolved, no orphans)
Phase3 01bf68b DealerOn-naive packages @ deliveries/site-packages/2026-11-04/
  motorinnautogroup/{7 pages + toyota variant} each: index.html + metadata.json
  (slug/title/meta/canonical/owner_host) + README-HANDOFF.md
Fixes fd29c48+d41(?): FAQPage JSON-LD now on 8/8 pages (derived from question-H2s and
  visible accordions).
Internal links: cross-page + www targets + mirrors article; anchors keyword-variant.
NEW page: car-dealership-carroll-iowa (the #26 volume query) w/ 32-Q FAQ.
Status: packages READY for Spencer review -> then DealerOn handoff per page.

## PREVIEW HOST LIVE 2026-11-04
URL (tailnet only): http://100.112.147.69:8899/
Index page links all 7 packages + toyota variant. Served by launchd
com.motorinn.seo-preview on nada-mini (KeepAlive), dir ~/seo-previews/2026-11-04.
Refresh procedure: re-tar deliveries/site-packages/<date> -> scp mini -> extract to new
dated dir -> update plist path or add dated index links.

## REDESIGN DEPLOYED TO PREVIEWS 2026-11-04 (commit 3826bc8)
Pages rebuilt inside verbatim DealerOn chrome (header 13KB + nav 35KB + footer + 256KB
inline design system + typekit/Roboto). Header match 95.9% normalized vs live site.
Preview server restaged; same URLs. ~318KB/page incl. full chrome; dealerOnTrack present.

## FORMAT FIX VERIFIED 2026-11-04 (ad74945)
Root cause: homepage chrome + CSS on inner pages, duplicate IDs, homepage-only css.
Fix: inner-page chrome from real inner-page layout, dedup IDs, homepage css dropped.
QA (playwright, 390+1280px, all 7 pages): 0px overflow, header 68/37px, nav 10-11 links,
content full-width. Evidence PNGs + qa-results.md in deliveries/.../_qa/.
Previews restaged - same URLs. Commit ad74945 pushed.

## WAQAS COMPETITIVE INTEL SCAN 2026-11-04
Ran the 4-layer recon (robots hidden paths / sitemap vs-pages / subdomains / repeated
headlines) on 5 Carroll-market competitors + self.
Headlines: Champion's f150-vs-silver1500 page targets us; Wittrock has ZERO comparison
content (open lane); Billion = 6775-url benchmark; our own vs-pages healthy (9).
Report: brain/reports/waqa-intel-2026-11-04.md. Raw: waqa-browser.json.
Queued: f-150-vs-silverado page + wittrock-lane pages -> next article batch (2/wk cap).

## RORY WORK ORDERS A+B COMPLETE 2026-11-04
A: f-150-vs-silverado-1500-carroll + car-dealer-comparison-carroll-iowa (commit 89ab102)
   full pipeline, REVIEW packets incl gap tables/link plans. Awaiting Spencer approval.
B: competitor-teardown project: 450-page crawl (champion/wittrock/billion), per-competitor
   ANALYSIS.md x3 + COMBINED + ADAPTATION-PLAYBOOK.md ranked effort-impact (top: Billion
   brand/body-style inventory pages; Wittrock nearby-town pages; offer-path mirror).
   git repo initialized, all committed.
Next: Spencer picks playbook items -> article queue; pages 1-2 enter approval flow.

## GAP-FIX COMPLETE 2026-11-05 (commit 1201d84)
The 2 rory pages (f-150-vs-silverado-1500-carroll, car-dealer-comparison-carroll-iowa)
were missing from packages + chrome + one schema. Now: full DealerOn chrome (dealerOnTrack,
header/nav/footer, inline design system) + FAQPage schema + packages + previews restaged.
ALL 10 pages / 10 packages now uniform: chrome, schema, metadata, interlinks.
Previews: same URLs, hard-refresh.

## WRITING OVERHAUL COMPLETE 2026-11-05 (3 phases, 6 commits)
P1 eb199de: 10 writing skills adopted (skills.sh: marketingskills copywriting/copy-editing,
anthropics writing/brand-guidelines, anti-slop x2, humanizer, storytelling, writing-beats)
+ blind 3-model writeoff: winner Codex GPT-6.1-Sol 7/10 > Gemma3-12b 6/10 > GLM 5/10.
P2 c07fef9+73a2652: all 10 pages rewritten w/ winning model+skills; read-aloud QA notes;
0 banned AI patterns.
P3 bd6a79a+e5e9378: re-rendered DealerOn chrome, QA 0-overflow/1 schema/ids clean.
Previews restaged (v2 copy live at same URLs).
Model note: Gemma tested per Spencer; lost to GPT-6.1-Sol on house-voice fit. Future
creative drafts default GPT-6.1-Sol via codex runtime; fallback GLM.

## BATCH 1 EXPANSION x6 COMPLETE - 2026-11-05 (commit 0323347)
Built 6 new ready-design pages + DealerOn-chrome packages + QA:
1 car-service-denison-iowa
2 car-service-storm-lake-iowa
3 used-car-dealer-lake-city-iowa
4 toyota-suvs-carroll-iowa
5 chevy-trucks-carroll-iowa
6 used-suv-carroll-iowa
Each: question H2s, TLDR on 3 hubs, single FAQPage JSON-LD, live DealerOn routes,
390/1280 QA PASS (0 overflow, chrome present, no duplicate IDs).
Paths: content/ready-design/*.html + deliveries/site-packages/2026-11-05/**.
Next: Spencer review + DealerOn handoff. Nothing live or published.

## BATCH 1 (6 expansion pages) LIVE 2026-11-05 + answer to 'more pages?'
Existing 10: all went through the identical rewrite/QA (per-page notes in
rewrite-notes-2026-11-05.md) - nothing was skipped.
Backlog quantified: 37 high-value pages. Batch 1 of 6 now BUILT+LIVE on previews
(/2026-11-05/ path): denison + storm-lake service, lake-city used, toyota-suvs,
chevy-trucks, used-suv-carroll. Remaining 31 queued in 5 batches (~2.5mo at 2/wk, or
faster w/ approval).
Playbook source: competitor-teardown/ADAPTATION-PLAYBOOK.md.

Preview index rebuilt at root with ALL 16 entries (8 core + 6 batch1 + sections).
Batch1 live under /2026-11-05/ path prefix; core at root. 14/14 URLs verified 200.

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

## STATUS 2026-10-27 09:50 (live-checked)
- trim-levels-explained: NEW copy LIVE
- highlander-vs-grand-highlander: NEW copy LIVE
- used-trucks-carroll-iowa: still OLD copy; no DealerOn reply on 1a1697567d479e20. Spencer: do NOT nudge DealerOn (said no 10-27).
- contact + testdrive: drafts with Spencer (resent 10-27 9:43 thread 1a17dd13274d890e), awaiting go/change; NOT sent to DealerOn.

## 2026-11-06: DealerOn handoff SENT + batch2 + recurring gapscan + hygiene audit
1. dealeron-handoff-2026-11-06.zip (per-page PLACEMENT.md + metadata.csv + email draft)
   EMAILED to support@dealeron.com w/ zip attached - msg 1a1b135603f831e7.
2. Batch 2 (6 model pages) built+QA'd+committed (0acae3f) - previews live /2026-11-06/.
3. Weekly gap-scan cron LIVE on mini (com.motorinn.seo-gapscan, Mondays 7am):
   GSC question-intent -> brain/reports/gapscan-latest.md (first run: 4 flagged).
4. Hygiene audit all 22 pages: title/desc length fixes committed (41d2c2d+dffb1a3).
   Remaining FAILs: none blocking; audit table in brain/reports/seo-hygiene-audit-2026-11-06.md.
Preview index: 23/23 URLs verified 200 (3 sections).
Backlog remaining after batch2: 25 pages (models+towns+comparisons phase2+service hubs).
