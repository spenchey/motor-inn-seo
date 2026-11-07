# Vinindex.ai teardown -> Motor Inn AI-visibility status (2026-11-05, jeeves)
## How vinindex gets dealers into AI answers (their how-it-works, verified)
1. Feed in -> validated VIN pages, server-rendered, sitemap'd (per-VIN pages w/ price/miles/VIN/status)
2. Track buyer questions per market; run on ChatGPT/Copilot/Perplexity/Gemini; record who's named (repeatable panel)
3. Read the pages the engines actually cite; measure facts (price/vin/mileage in HTML, no-JS)
4. Build two page tracks: per-vehicle pages + answer pages for no-VIN questions (bad credit, trade-in w/ loan)
5. Lead routed to CRM stamped w/ AI source
## Our status vs that bar (all verified 2026-11-05)
- 3 ai-mirrors live+healthy (autogroup/toyota/carroll), robots allow OAI-SearchBot/Claude-SearchBot/PerplexityBot, sitemaps 200
- ai-mirrors have llms.txt, dealership.md, contact-hours.md, per-make inventory.md (65 units, VIN+price+mileage) = vinindex track 1 ALREADY EXISTS
- DealerOn VDPs: server-rendered, price+VIN+schema.org present (checked Equinox 3GNAXPEG1SL228732, 732KB HTML)
- DealerOn listing pages (searchused.aspx): NO prices/VINs in server HTML (JS-loaded) = the gap vinindex's analyzer would flag
- ai-mirrors: NO per-VIN unique URL (one big .md per condition), only 1 page w/ GSC data, NO sitemap submitted to GSC
- Main-site robots.txt groups: all AI bots allowed, only ajax/rss disallowed - good
## Live AI-answer baseline (treg/cloro, 11-5, ~$.02)
- ChatGPT AWD<\$30k Q: named Choice Auto+Pro Auto w/ 8 VIN-level rows; Motor Inn only in 'also call' list
- Perplexity dealer Q: Motor Inn #2 named (blog posts cited); RAV4 Q: Motor Inn Toyota #1
- Perplexity AWD Q: rivals w/ specific VINs; Motor Inn 'no specific qualifying vehicles visible'
## Gap = what to fix (the vinindex product, self-serve)
1. Per-VIN pages on ai-mirrors (vinindex's core asset) - /v/<vin>.md or .html from feed.json, in sitemap
2. Submit ai-mirror sitemaps to GSC (needs verification write - Spencer 30s or treg owner route)
3. DealerOn listing-page server-render fix via vendor ticket (rss-newinventory.aspx disallowed but is the data source)
4. Answer pages: bad-credit/trade-with-loan from finance-trade.md content
5. Weekly same-question panel via treg cloro (~4c/run) = vinindex's monitoring, free tier


## DEPLOYED 2026-11-05 (jeeves)
- Repo: github.com/spenchey/ai-markdown-proxy. Commits 43b5a24 (vin+answer pages), 9cf2057 (Dockerfile), 4caa86e (price fallback). Merged to main 9ac5870. Suite 111+22 subtests green; 12 new tests in tests/test_vehicle_pages.py.
- Live: /v/<vin>[.md|.html] on all 3 mirrors (price/mileage/condition/canonical link, doc-fee itemized); /answers index + 4 pages (bad-credit-car-financing-carroll, trade-in-with-loan-payoff-carroll, first-car-buying-carroll, car-payment-calculator-carroll) gemma3:12b-written then human-edited, per-store scoped via dealer_keys; sitemap.xml lists all 4; .html variants indexable w/ md alternate.
- Writer: gemma3:12b via ollama on workMac (100.69.77.97:11434, ssh tunnel localhost:11434), temp 0.4, house-style prompt w/ facts-only constraint + disclosure line.
- GSC sitemaps submitted+verified by readback: sc-domain(motorinnautogroup) now carries www + ai.motorinnautogroup; www.motorinntoyotaofcarroll carries its sitemap. BLOCKER for Spencer: www.motorinnofcarroll.com is siteUnverifiedUser - needs his 30-s verification (Search Console -> Add property or verify existing), then submit ai.motorinnofcarroll.com/sitemap.xml the same way.
- Weekly panel: mini cron Mondays 08:00 Central, ~/Library/Application Support/MotorInn/AiVisibility/panel.sh; 3 questions x engines via treg (perplexity x2, chatgpt x1), summary-<date>.json w/ motorinn_cited trend; cost ~1.5c/wk, promo credit $0.6875 left.


## GSC Carroll verification - STAGED 2026-11-06 (jeeves)
- Blocker: password challenge for spencer.heywood@motorinnmail in workMac relay Chrome (headless, CDP 19222), tab D76B1CA567338C8892D7486B2086EDD2. Google session cookies for BOTH his accounts are Signed out in that profile; vault has no work-Google password (only jimfrank413 google item). gog keyring tokens = gmail/drive/sheets scopes only, NO webmasters - refresh token cannot grant new scopes.
- Site already carries 3 google-site-verification metas (pZSUgoq..., n-yUnBZ..., 6Pu_nZW...) = 3 existing verified owners; the www.motorinnofcarroll.com GSC property exists but is unverified for our SA.
- WHEN SPENCER TYPES THE PASSWORD in that tab (or any Chrome signed in as work acct): run `nohup /opt/homebrew/bin/python3.13 /tmp/finish_gsc.py` on workMac - it waits for sign-in, adds sc-domain:motorinnofcarroll.com, picks GoDaddy verification. Then jeeves: mint full-scope SA JWT, PUT sites/sc-domain%3Amotorinnofcarroll.com/sitemaps/https%3A%2F%2Fai.motorinnofcarroll.com%2Fsitemap.xml + www variant, readback list.
- FALLBACK (no password): email draft prepared - support@dealeron.com, ONE issue (add google-site-verification meta to head), per DealerOn case rules; route via approvals Slack C0AC3BP5XPF prepared_not_sent. Token TBD from GSC UI at property-add time.
- NOTE: xtime direct scheduler (webKey xtm20260814115234xx1 shared by all 3 stores) can be added to service.md on the mirrors - agent-doable follow-up for in-chat booking links.
