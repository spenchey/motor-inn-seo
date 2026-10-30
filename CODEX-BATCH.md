Big feature batch from the 'AI Builders' dealer thread - 6 items. Repo:
/Users/spencerheywood/motor-inn-seo + proxy repo
'/Users/spencerheywood/Documents/New project/ai-markdown-proxy' (branch feed-json exists w/
/feed.json done: commit ce0ff09, 65 tests green - DO NOT redeploy, Spencer approves deploys).

WHAT THE THREAD DID (dealer results: AI visits 2.5->7.8/day; rank #12->#4 in a week):
1. AI-visits dashboard (per-source: ChatGPT/Gemini/Perplexity/Copilot + trend)
2. vinindex-style inventory syndication for AI answer engines
3. inventory.md at site root, daily-refreshed with offers/market notes
4. 'answer pages' at scale: local events, comparison tables, ownership guides - rank in days
5. ALL inventory in crawlable HTML + sitemap (never JS-only)
6. (skip CarChief/CRM - different product)

BUILD THIS, scoped to our stack:

A) inventory.md endpoint (proxy repo, feed-json branch): /inventory.md per site - plain
   markdown table of live inventory (vin, year/make/model/trim, price, miles, body, photo
   url, dealer-comments snippet) generated from the existing api_inventory_search source.
   Daily-cache, sitemap+llms.txt link it. Tests included.

B) AI-visits dashboard upgrade: extend brain/ai_referrals.py -> weekly per-source table
   (sessions+users+trend) for chatgpt/perplexity/gemini/ copilot/edgeservices, and a
   self-contained HTML artifact brain/reports/ai-visits-latest.html (simple table+sparkline
   css, no JS deps) regenerated each Monday by the existing weekly-intel launchd job
   (edit brain/weekly_intel_mini.sh on nada-mini? NO - job lives on workMac; edit
   brain/weekly_intel.sh and note mini parity in comments).

C) answer-page factory spec -> brain/ANSWER-PAGES.md: templates for the 3 patterns that
   ranked (comparison tables, local-events/hub page, ownership guides) w/ our VOICE-DNA +
   SEO-PANEL gate + internal-link rules; source data = our inventory API + DFS + manual
   events. ALSO generate the FIRST batch: 3 ownership guides
   (Silverado towing guide, Tahoe family hauler, Highland road-trip checks) as drafts in
   content/drafts/seo/ - subject to the usual approval queue, no publish.

D) crawlability audit script brain/html_inventory_audit.py: crawl main+2 store sites,
   list vehicle pages reachable only via JS (no <a href> in static HTML), output
   exceptions list - evidence for a DealerOn case if needed.

Rules: read brain/BRIEF.md + VOICE-DNA.md first; no invented data in drafts (NEEDS-VERIFY
flags); commits per feature; summary at end. Ask nothing - decide sensibly, document.