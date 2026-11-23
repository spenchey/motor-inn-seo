# GBP Structural Audit — 2026-11-23

## Executive Summary
- **What changed or matters most this week:** Review momentum is the strong suit — the primary listing hit **270 reviews / 4.6**, with the best week since tracking began (**9 new reviews Nov 16–22**, vs 4 the week prior) and 14 in November so far. Owner posts are fresh and local (four new posts Oct 29 + one Oct 22, all service/trade-themed, one linking the used row for Black Friday week). Every structural fix on the list, though, is the same list as last week: photo gallery still stuck in 2020/2021 era, no Book online CTA while Champion Ford shows one, and the Buick listing has now been "Permanently closed" for roughly three months.
- **Biggest risk or opportunity:** Opportunity — reviews and posts prove the account is active and the team responds fast; the profiles look alive. Risk — the two things shoppers actually *click* (recent photos, one-tap booking) are the two things still missing, and Coleman/Spirit Lake Ford keeps widening the photo-recency gap (Sep 2026 vs our ~2020/21 public carousel).
- **What should be done next:** One 30-minute GBP admin session fixes the three standing items at once: upload the first 4-photo batch (plan attached), add the booking link to the service appointment page, and publish description V2. Second: reply to the single unanswered review (Jason Lhotka, Nov 22, 2 stars) — it is the only open one and reply lag has been 0–6 days all year.
- **Spencer decision needed?** Yes, one: the standing Buick listing call — reopen/merge the "Permanently closed" Buick at Motor Inn listing (792-6275) or let it ride. Plus ~15 minutes to approve the photo batch; everything else is execution, not decisions.

---

## Categories
Signed-out Maps, 2026-11-23 (combined listing scrape + Champion scrape):

| Category | Motor Inn (primary) | Champion Ford |
|----------|--------------------|---------------|
| Toyota dealer | **Primary** | — |
| Chevrolet dealer | Secondary (nested Chevrolet listing, "Floor 1") | — |
| Car dealer | Secondary | — |
| Car finance and loan company | Secondary | — |
| Car leasing service | Secondary | — |
| Truck dealer | Secondary | — |
| Used car dealer | Secondary | — |
| Used truck dealer | Secondary | — |
| Ford dealer | — | Primary |
| Lincoln dealer | — | Secondary |

Sub-listings visible under our campus: Chevrolet Service, Chevrolet Parts (Auto parts store), Toyota Service, Toyota Parts. Buick listing separate ("Permanently closed"). Category set unchanged vs last week; no competitor category gains observed in the scrape. Macke/Wittrock/Okoboji listings were not re-scraped this week (browser-run skipped; no category drift reported by the public data we did capture).

### Missing Categories (Prioritized)
- P1: none — all mapped brand/service categories relevant to Motor Inn are present on the pair of listings.
- P2: none new.
- P3: Buick dealer — exists only on the "Permanently closed" Buick at Motor Inn listing. If that listing is reopened/merged (Spencer decision, standing ~12 weeks), the Buick category returns to live search surfaces. No action possible without that decision.

## Attributes
| Attribute | Motor Inn | Champion Ford |
|-----------|-----------|---------------|
| Wheelchair accessible entrance | Yes | Yes |
| Wheelchair accessible parking lot | Yes | Yes |
| Service booking link (Book online / appointment URL) | **No** (site link present; GBP booking CTA not configured) | Yes (deep link to service-appointment page) |

(Okoboji Motor Co. remains the only area listing with Google's native "Book online"; per 11-16 About-tab check — unchanged.)

### Missing Attributes (Prioritized)
- **Table stakes:** none — accessibility attributes match Champion.
- **Strong rec:** booking/appointment CTA. Ranking impact: low-medium; **CTR impact: yes** — Champion's "book service appointment" button is a one-tap path our profile lacks even though `service-locations` resolves 200. Fix is admin config, not a website change.

## Services
| Service area | Motor Inn | Notes |
|---|---|---|
| Sales (new + used, Toyota & Chevrolet) | 8 service items live since 11-16 API push | Read-back verified then; no drift signal this week |
| Service / parts / test drive / financing / trade appraisal | covered by the 8 items | Chevrolet listing carries 7 (same minus test drive) |

### Services Missing from GBP
- None known. Site-to-GBP cross-check clean: every site service surface (`/service`, `/trade-in`, `/used-inventory`, sales) maps to a live GBP service item.

### Services Needing Better Descriptions
- None new. Public Maps again did not render service descriptions (Google limitation, noted every week); the 2026-11-16 API-pushed descriptions are the record and already meet the 40–60 word quality bar. Draft folder: `content/drafts/gbp-services/services-2026-11-23.md` (no-change note).

## Description
| Business | Public desc visible? | Notes |
|----------|---------------------|-------|
| Motor Inn | Not exposed (signed-out) | 3 approved drafts waiting since 08-17; V2 recommended |
| Champion Ford | Not exposed | — |

### Current Motor Inn Description
Not retrievable via public scrape this week (unchanged limitation). Last confirmed state predates the 08-17 drafts.

### Recommendation
**Rewrite — pending the same admin session as the booking link.** Versions live at `content/drafts/gbp-description/description-2026-08-17.md` (V1 keyword / **V2 conversion — recommended** / V3 trust) with a no-change addendum from today (`description-2026-11-23.md`). No new versions written; do not stack duplicates.

## Photos
| Metric | Motor Inn (combined) | Champion Ford | Best area practice |
|--------|---------------------|---------------|--------------------|
| Public count (header) | 67 | 13 | — |
| Dated bylines in carousel | mostly Oct 2020 / 2018; newest visible Sep 2021 | Oct 2018 era | Coleman Sep 2026 |
| Nov 2026 uploads observed | 0 visible | 0 | — |

(The "Jul 2026" date seen in raw data is a viewer metadata stamp, not a photo byline; treated as noise.)

### Upload Plan Summary
**4 photos/week × 4 weeks = 16** — survival cadence, one sitting each. Full shot list: `content/drafts/gbp-photos/photo-plan-2026-11-23.md`. Week 1 due Fri 11-27: entrance, service drive, waiting area, one winter unit. Approval required before upload (standing rule). This is the 8th consecutive week the photo gap is the top item — if the batch lands once, subsequent weeks get easier because the habit exists.

## Review health (context for the week)
- Primary: 270 @ 4.6 (+9 WoW, best week on record); Nov MTD 14; W47 velocity 9 vs W46 4.
- Reply coverage: 19/20 of recent reviews; **one open: Jason Lhotka 2★ Nov 22** (service inspection complaint mentioning Nathan positively — reply drafts itself).
- Chevrolet listing: 37 @ 4.8, drought now ~12 weeks (no new review since Aug 28). Process fix (ask at delivery) still owed — carry.
- Review themes to mine for posts/replies: Kyle G. named 3× in recent 5★s; body shop (Matt) praised; "no pressure" recurs. Nate (service) positive in the Nov 22 2★ text itself.

## Action Items (This Week)
1. **One GBP admin session (~30 min):** upload photo batch week 1 (4 photos) + set booking link to the service appointment page + publish description V2. Highest leverage per minute spent; kills three standing P1/P2s at once.
2. **Reply to the Nov 22 2-star (Jason Lhotka)** — only open review; keep the <1-week reply streak intact.
3. **Spencer decision — Buick listing:** reopen/merge "Buick at MOTOR INN OF CARROLL" (permanently closed ~3 months, phone 792-6275) or formally drop it. Also still open from prior weeks: Chevrolet review-ask process fix (12-week drought) and duplicate-shell cleanup; none block this week's items.

## Sources
- `scrapes-2026-11-23/` (signed-out Maps: combined, Chevrolet tree, Champion Ford)
- `reviews-pull-2026-11-23.json` (GBP API v4, owner_oauth — authoritative counts/replies)
- EXA research: `gbp-research-2026-11-23.json` (local-pack inputs = relevance/distance/prominence; attributes feed AI summaries; category hygiene per SearchLab dealer study — no new mandatory-category findings vs prior weeks)
- Prior audit: `gbp-structural-2026-11-16.md`
