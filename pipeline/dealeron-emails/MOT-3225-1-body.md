Hello DealerOn team,

One change request for our site https://www.motorinnautogroup.com :

ADD exactly one <h1> to the vehicle details page (VDP) template, containing the vehicle year/make/model/trim title text.

Evidence (checked 2026-09-22, static HTML):
- True VDPs (e.g. /used-Carroll-2009-Chevrolet-Silverado+1500-LTZ-3GCEK33359G145292, /used-Carroll-2009-Ford-Escape-Hybrid-1FMCU49379KB61755, /used-Carroll-2024-Chevrolet-Trax-1KL27LPB6RB215789) contain ZERO <h1> tags. The vehicle title renders as <h2 class="vehicle-title__text">.

Why it matters: SEO/GEO best practice is exactly one H1 per page carrying the page's primary heading. Crawlers and AI answer engines (ChatGPT, Claude, Perplexity) use it to identify the page topic.

Verification step: after the change, curl any VDP and confirm exactly one <h1> element whose text is the vehicle title.

Please confirm when this template change is live. Thank you!

Spencer Heywood
Motor Inn Auto Group — Carroll, Iowa
