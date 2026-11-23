# TASK: Interpret GSC research and build the page plan + page packages (AEO/SEO)

You are working in /Users/spencerheywood/motor-inn-seo on the work MacBook.

## Inputs (read these first)
- ads/gsc-ads-package-2026-11-22/summary.md   - query tier counts, top opportunities
- ads/gsc-ads-package-2026-11-22/intent.md    - tier definitions (ready-now 206, researching 210, research-only 502)
- ads/gsc-ads-package-2026-11-22/keywords.csv - 40 exact-match terms w/ position, impressions, landing page
- ads/gsc-ads-package-2026-11-22/ad-groups.md - ad groups (Toyota / Chevrolet / Carroll dealer / model shopping)
- ads/gsc-ads-package-2026-11-22/negatives.txt

## Deliverable 1 - Interpretation (write to docs/page-plans/page-plan-2026-11-23.md)
Interpret the intent data as a PAGE plan (not ads): which real customer questions/intents deserve pages, mapped to the right site.

Site routing rules (Spencer, 2026-11-23):
- Group-level pages (general "car dealerships carroll iowa", used inventory, trade-appraisal, finance, service, multi-brand) -> motorinnautogroup.com
- New-Toyota-specific intents (trim/model/new Toyota shopping) -> motorinntoyotaofcarroll.com
- New-Chevrolet-specific intents -> motorinnofcarroll.com (Chevrolet of Carroll / Motor Inn of Carroll)
- Where a page could sit on both, prefer the brand site for brand-specific intent and the group site for cross-brand/comparison intent; note the choice in the plan.

## Deliverable 2 - Page packages (one folder per page)
For EVERY page in the plan, produce a DealerOn-ready package under content/page-packages/2026-11-23/<page-slug>/:
- brief.md       - target query(s), intent tier, H1, url slug, internal links (real existing pages only), source evidence (the GSC row(s))
- content.md     - full page copy, written for humans first; question-led H2s matching real GSC phrasing; local proof (Carroll IA, addresses, phone (712) 792-5000 for Toyota storefront pages); no invented prices/offers/APR; numbers only from repo facts
- schema.json    - JSON-LD: AutoDealer or Product/Vehicle + FAQPage where the H2s are questions; valid JSON
- faq.md         - 3-6 Q&A pairs pulled from real query phrasing (AEO target: ai.motorinnautogroup.com already publishes llms.txt; keep answers self-contained so an AI answer engine can quote them)
- meta.md        - title <=60 chars, meta description <=155, og title/desc

Quality bar (house rules):
- motorinn-seo rules: canonical Carroll phone (712) 792-5000 on customer-facing Toyota copy; never 522-2526; CarGurus (980) 4810-8309 is a tracking number, do not flag.
- No fabricated claims: every number traceable to the GSC export or existing site pages.
- AEO: each FAQ answer must stand alone in 2-4 sentences, no "click here".
- E-E-A-T: name the dealership, city, and real differentiators only where the repo/site evidences them.
- Do NOT publish anything. Drafts + packages only; Spencer reviews.

## When done
Print a summary: pages created, site routing per page, file counts, and any intent you could NOT match to a page (gaps).

## Model / effort
Run with model opus (claude-opus-5-5), effort high.

## AEO distribution note (Spencer asked for content on the "aibr" sites)
The AI-readable discovery host is ai.motorinnautogroup.com (llms.txt / llms-full.txt / markdown resources). For every page package, ALSO emit:
- ai/<page-slug>.md - a self-contained markdown version of the page (title, summary paragraph, Q&A section, entity facts: name, address, phone, brands, service URL) formatted for llms.txt-style ingestion.
Do not deploy anywhere; leave the files in the repo for review.
