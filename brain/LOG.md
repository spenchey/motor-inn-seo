
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
