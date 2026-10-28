# Answer-page factory — spec (draft-only)

## Purpose
Turn buyer questions into rankable, useful pages. Three proven patterns:
1. Comparison tables
2. Local-events / local-hub pages
3. Ownership guides

## Source data
- Live inventory: `https://ai.motorinnautogroup.com/inventory.md` (and per-store `ai.` subdomains)
- Search evidence: GSC exports + DataForSEO keyword research
- Local events: manual collection only; no invented dates
- Any claim that can't be verified stays `[NEEDS-VERIFY]`

## Gate
- Every page goes through the Eric Siu 10-expert gate in `brain/SEO-PANEL.md`
  (mean 90+, no expert under 80, 3-round max).
- Voice check against `brain/VOICE-DNA.md` before submit:
  short declaratives, answer-first H2s, one CTA, zero marketing slop.
- No invented prices, payments, awards, OEM endorsements, or local facts.
- Carroll = 51401 only; Fort Dodge 50501 stays a separate expansion cohort.

## Internal-link rules
- Each page links to the money page it supports, with an exact-phrase anchor.
- Each page links to one sibling page on the same topic.
- Each page links to one category page (`/used-trucks`, `/used-suvs`, `/service-locations.html`).
- No orphan pages: every new page needs at least one inbound link from an existing indexed page.
- Never link a draft page before publish; use the draft file path in review, not in HTML.

## Template 1 — comparison table
Best for model-vs-model, trim-vs-trim, body-style-vs-body-style.

```md
# [A] vs [B]: Which Makes More Sense in Carroll?

## Which one should you buy?
[pick-A-or-B-if condition]. Exact current inventory: [inventory link].

## [A]
| Spec | Value |
|---|---:|
| ... | [NEEDS-VERIFY] |

## [B]
| Spec | Value |
|---|---:|
| ... | [NEEDS-VERIFY] |

## Which one fits how you use it?
[1-2 lines per real use case: towing, family, fuel, cargo]

## Current inventory
[link to inventory or money page]

## CTA
Call the store or schedule a test drive.
```

## Template 2 — local-events / hub page
Best for recurring local demand around events and seasonal activities.

```md
# [Topic] in Carroll, Iowa

## What's happening in [Topic] near Carroll?
[2–4 sentence direct answer; no invented date.]

## Calendar
| Event | Date | Where | Why it matters |
|---|---|---|---|
| [only verified events] | [NEEDS-VERIFY] | ... | ... |

## Before you go
[one practical checklist tied to ownership/service; no invented service details]

## CTA
Call the store or schedule service.
```

## Template 3 — ownership guide
Best for maintenance, towing, road trips, first-time ownership.

```md
# [Vehicle/topic] ownership guide for [real use case]

## What owners should do first
[direct answer]

## When to bring it in
[explicit trigger; no invented service claims]

## Checklist
| Item | Why | Source |
|---|---|---|
| ... | ... | [NEEDS-VERIFY] |

## CTA
Call the store or schedule service.
```

## First batch drafts
- `content/drafts/seo/silverado-towing-guide.md`
- `content/drafts/seo/tahoe-family-hauler.md`
- `content/drafts/seo/highland-road-trip-checks.md`
All three are draft-only and remain in the approval queue. No publish.
