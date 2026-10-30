NEW BATCH - two reference threads, build all of it. Local+commit+DEPLOY ok (proxy infra
only, no DealerOn emails).

=== THREAD A: Cloudflare agent-readiness (score 20->67 case study) ===
Source: https://x.com/nicklaunches/status/2115466124133585403 - scanner: isitagentready.com
Add to the PROXY (ai.* mirrors, our control) - each is a small static file/route:
1. /api catalog page + Link headers pointing agents to it (Link: <...>; rel="service")
2. /ai.txt - AI catalog file (what this site offers, agent-readable)
3. /.well-known/agents.json - agent directory card
4. skills index /skills.txt (what actions agents can take: search inventory, hours, contact)
5. Content-Signal line in robots.txt on mirrors
6. MCP server card endpoint (/.well-known/mcp.json) - catalog only, no server needed yet
Run the public scanner against all 3 ai.* hosts after deploy; capture before/after if possible.

=== THREAD B: local citations / NAP (https://x.com/seo_bint_ejamil/status/2115671217944326327) ===
1. Audit current NAP consistency: scrape name/address/phone from all 3 dealer sites' contact
   pages + GBP + the top-20 citation sources in the thread list. Report MISMATCHES table.
2. Canonical NAP per store (from our own GBP records - don't guess).
3. Produce a prioritized submission plan: aggregators first (Data Axle, Neustar Localeze,
   Foursquare) then top directories. CSV with columns: source, url, status, priority, notes.
   NO auto-submission - humans create accounts. This is prep-only.
4. Add NAP block (schema LocalBusiness) to every proxy page footer - consistent canonical.

Deliverables: deployed artifacts + scanner scores + NAP audit CSV + citation plan CSV.
Commit all. Report paths + scores + mismatch count.