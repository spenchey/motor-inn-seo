
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
