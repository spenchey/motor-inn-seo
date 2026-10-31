# 12. Article draft writer (Holmberg steps 3-4)

## Purpose
Turn an approved research file into a rankable draft that can win Google AND get cited by
AI chats — without inventing anything.

## Inputs
brain/research/<slug>/research.md (MUST exist and be committed); brain/VOICE-DNA.md;
BRIEF.md.

## Exact steps
1. Read research.md + VOICE-DNA.md + BRIEF.md in full before writing.
2. Structure: H1 = primary query intent; every H2 = a real query phrasing from the
   research file; FIRST sentence under each H2 answers it directly; evidence after.
3. Each section stands alone. One CTA only (match page type: call / schedule / browse).
4. Every factual claim carries an inline source from research.md, or the flag
   [NEEDS-VERIFY: what's missing]. No invented prices/payments/dates/awards.
5. Run the anti-slop checklist at the end of VOICE-DNA.md; fix violations before saving.
6. Save draft to content/drafts/seo/<slug>-draft.md with a front-matter block:
   target_url, primary_query, research_sha (git hash of research.md), date.
7. Build the REVIEW PACKAGE next to the draft: <slug>-REVIEW.md containing
   - the draft
   - source list w/ URLs
   - every [NEEDS-VERIFY] item
   - 3 questions for Spencer (voice/claims/CTA)
8. Register for approval: append to pipeline approval queue (existing digest flow).
   NEVER publish or email directly.

## Cadence
Max 2 new drafts/week. Update existing pages when research shows changed facts or a
genuinely-better angle; log update in brain/LOG.md with before/after SHA.

## MANDATORY: 10x article method
Before drafting ANY article, run agents/ARTICLE-10X-METHOD.md end to end (reverse-engineer competitor -> gaps -> verified research -> superior draft -> scored audit). Non-negotiable per Spencer 2026-10-31.

## MANDATORY: ChatGPT-recommendation pipeline
For every article: follow agents/CHATGPT-RECOMMENDED-PIPELINE.md (query mining -> SERP headings -> 10x outline -> TLDR-first draft -> metadata -> humanize -> internal links from ranking pages -> GSC indexing).
