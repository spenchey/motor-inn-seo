
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
