# SEO WAVE 2 DIRECTIVE — 6 longtail answer pages (Spencer order 2026-11-15)

You are building the deliverable for kanban task t_0fa2999c. Repo: this directory
(/Users/spencerheywood/motor-inn-seo, work-macbook, clean on origin/main @ de5e69b).

ABSOLUTE RULES (never violate, never ask to violate):
- Every page status: draft-needs-owner-approval. NEVER publish, NEVER email DealerOn,
  never use the word "live" for live site. Packages only.
- Real facts only: every number sourced (OEM spec pages — toyota.com, ford.com, gm.com,
  ramtrucks.com tow guides — with source URLs recorded). No invented prices, dates, awards.
  Flag anything unverifiable as [NEEDS-VERIFY] and list every flag in that page's REVIEW.md.
- NEVER mention days on lot.
- Max-2-drafts/week rule is superseded this week by explicit owner order (6 pages).
- Commit per phase with clear messages.

PIPELINE (mandatory, read first): agents/ARTICLE-10X-METHOD.md,
agents/CHATGPT-RECOMMENDED-PIPELINE.md, agents/draft-writer.md, brain/VOICE-DNA.md.
Per page: 10x gap vs live SERP top 3 (fetch the top-3 ranking pages for the primary
query; if SERP fetch fails, use the flagged-query table below + existing site content as
gap base and note the fallback); question-mined H2/H3; TLDR-first (first sentence answers);
metadata; humanize per VOICE-DNA; internal links FROM 2-3 already-ranking pages with
chosen anchor text — verify every target href resolves http 200 with curl before the
REVIEW packet is final.

PAGE LIST — flagged queries (GSC, 6mo, from brain/reports/longtail-answers-2026-11-14.md):
1. trim-levels-explained — REWRITE existing package (keep URL /vehicle-trim-levels-explained).
   Existing: deliveries/site-packages/2026-11-04/motorinnautogroup/trim-levels-explained
   and content/drafts/seo/trim-levels-explained-draft.html. Queries ~1,818 impr/6mo combined:
   "some car manufacturers use this to describe certain trims of a car" (954 impr, pos 1),
   synthetic upholstery variants (166+143+33+32), "what is a trim level on a car" (116),
   "what does trim level mean on a truck" (59), etc. Softbody = SofTex (Toyota synthetic
   upholstery) — verify against toyota.com before naming. Answer "what is a trim level on
   a car/truck" in the first screenful. A quick-answer box was staged in r1 (commit 93b01c9)
   — keep it and expand. Keep FAQPage schema; re-derive after rewrite.
2. heavy-duty-vs-light-duty-trucks — build a PAGE version for the existing blog topic
   (live blog /blog/heavy-duty-vs-light-duty-trucks, 200). ~161 impr: "how does a light
   duty full size truck compare to a heavy duty model for everyday use?" (88),
   "how do heavy duty trucks differ from light duty trucks in real world capability?" (73).
   Must answer: everyday-use comparison, real-world capability delta, towing/payload numbers
   with sources (Ford/GM/Ram tow guides). DECISION FOR SPENCER: page-vs-blog — build the
   page package (slug heavy-duty-vs-light-duty-trucks) and state in the REVIEW.md the 10x-gap
   rationale for page vs augmenting the blog post.
3. highlander-vs-grand-highlander — REWRITE (keep URL /highlander-vs-grand-highlander;
   existing package deliveries/site-packages/2026-11-04/motorinnautogroup/highlander-vs-grand-highlander).
   ~129 impr: "how much bigger is the grand highlander than the highlander" (69), "is the
   grand highlander bigger than the highlander" (60). Lead with the size delta: length,
   wheelbase, cargo, third-row numbers sourced from toyota.com specs. "Is the Grand
   Highlander bigger" answered in sentence 1.
4. toyota-rav4-carroll-iowa — NEW model page. ~330 impr: "what factors explain the toyota
   rav4's market dominance?" (256), "why toyota rav4s are suddenly the most coveted used
   cars in america" (74). Angle: why RAV4s hold value / used availability in Carroll.
   Real specs only. Link live inventory pattern the same way sibling model pages do
   (see 2026-11-06 model pages e.g. chevy-silverado-1500-carroll-iowa).
5. used-car-maintenance-mileage — NEW page. ~97 impr: "how many miles can a car last
   before it breaks down" (42), "what does motorhappy recommend for maintaining a
   high-mileage vehicle?" (55). Angle: our inspection/reconditioning process — only
   claims ops can stand behind; [NEEDS-VERIFY] anything process-specific.
6. about/motorinn-spirit-lake-inventory — NEW; 557 impr: "motor inn of spirit lake inc
   used cars". First check whether /aboutus.aspx-style about content is editable in our
   DealerOn handoff lane. Build the package for slug about/motorinn-spirit-lake-inventory
   (or the closest owned URL) and DECISION FOR SPENCER: state in REVIEW.md whether aboutus
   augmentation is possible or the new page is the right target.

CHROME + PACKAGE RULES:
- INNER-page chrome lifted from a LIVE INNER PAGE of motorinnautogroup.com (never homepage
  chrome; duplicate IDs kill nav JS). Reuse the exact chrome pattern from the 2026-11-04
  packages (header/nav/footer + inline design system + typekit/Roboto + dealerOnTrack script).
  Verify dealerOnTrack script present in every final page.
- FAQPage JSON-LD on every page derived from question-H2s.
- Package dir per page: deliveries/site-packages/2026-11-15/motorinnautogroup/<slug>/
  index.html + metadata.json + entry appended to deliveries/site-packages/2026-11-15/
  README-HANDOFF.md.
- Drafts also saved as content/drafts/seo/<slug>-draft.html (with DRAFT-META block) +
  content/drafts/seo/<slug>-REVIEW.md (competitor gap, metadata, internal-link plan with
  anchors, sources, NEEDS-VERIFY list, 3 approval questions for Spencer).

QA + HYGIENE (phase 4):
- Playwright QA at 390px AND 1280px per page: 0px horizontal overflow, header renders,
  nav links clickable, 0 console errors. Use the repo venv (~/.venv -> actually
  /Users/spencerheywood/motor-inn-seo/.venv/bin/python3 has playwright; browsers cached at
  ~/Library/Caches/ms-playwright). Screenshots + qa-results.md + qa-results.json into
  deliveries/site-packages/2026-11-15/_qa/.
- Hygiene audit per page: title 50-60 chars, meta description 120-158, canonical self,
  exactly 1 H1, correct heading order (no skips), JSON-LD parses, >=3 sibling internal
  links + >=1 money-page link, NAP present (Motor Inn Auto Group, 712-792-5000),
  no AI-tells (VOICE-DNA checklist). Audit table to
  brain/reports/seo-hygiene-audit-2026-11-15.md.
- Do NOT touch the preview server or nada-mini — the parent agent handles restaging.

LOG: append a brain/LOG.md entry for the run after all phases.

PHASE PLAN (commit after each phase):
- phase1: adversarial audit of the 3 rewrite targets (what's wrong live vs the 10x bar)
  -> brain/reports/wave2-audit-2026-11-15.md
- phase2: draft all 6 (drafts + REVIEW packets)
- phase3: chrome + site-packages + README-HANDOFF
- phase4: QA 390/1280 + hygiene audit + brain/LOG.md entry
