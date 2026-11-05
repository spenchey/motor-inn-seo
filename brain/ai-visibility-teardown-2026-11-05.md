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
