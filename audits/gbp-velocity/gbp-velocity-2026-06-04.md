# GBP Velocity Audit — 2026-06-04

## Executive Summary
- Review velocity: inconclusive in fresh scrape because Google Maps exposed only limited listing views and blocked review-tab extraction for Motor Inn share URLs.
- Posting cadence: behind plan. Accessible GBP snapshots showed no current visible Motor Inn owner posts, while Champion Ford still showed a visible owner post in the listing shell.
- Top finding: this week's edge is content freshness. Google/EXA signals continue to reward active profiles with weekly posts, real visuals, and specific local utility.

## Data Quality Note
- This run used Firecrawl against Google Maps because `gstack-browse` is not available in the OpenClaw environment.
- Google Maps returned limited-view listing shells for most profiles and blocked some Motor Inn share URLs with CAPTCHA/traffic checks.
- Fresh ratings, hours, phone numbers, and visible owner-post snippets were captured. Review-tab counts, last-50-review text, and last-30-response details were not reliably accessible this run.
- Where review-velocity status is referenced below, the baseline is carried forward from the last complete observed audit on 2026-05-21.

## Review Velocity

| Metric | Motor Inn Toyota/Chevy | Motor Inn Chevy | Champion Ford | Wittrock | Okoboji Motor Co. | Macke Motors |
|---|---|---|---|---|---|---|
| Avg rating | 4.4 | 4.8 | 4.2 | 4.6 | 4.5 | 3.8 |
| Total reviews | N/V | N/V | N/V | N/V | N/V | N/V |
| Last 30d | N/V | N/V | N/V | N/V | N/V | N/V |
| Last 60d | N/V | N/V | N/V | N/V | N/V | N/V |
| Last 90d | N/V | N/V | N/V | N/V | N/V | N/V |
| Velocity/mo | N/V | N/V | N/V | N/V | N/V | N/V |

### Gap Analysis
- Last complete baseline (2026-05-21): Motor Inn combined 213 reviews vs Wittrock 258 reviews.
- Carry-forward velocity baseline: Motor Inn at 82.5% of the top observed competitor.
- Reviews needed/month to catch the prior top competitor in 6 months: about 8.
- Reviews needed/month to catch the prior top competitor in 12 months: about 4.
- **Status:** P3 maintain, with low confidence until full review-tab access is restored.

## Review Response Quality

| Metric | Motor Inn | Champion Ford | Wittrock | Okoboji Motor Co. |
|---|---|---|---|---|
| Fresh response rate | N/V | N/V | N/V | N/V |
| Avg word count | N/V | N/V | N/V | N/V |
| Mentions services | Prior pattern: yes | N/V | N/V | N/V |
| Mentions locations | Prior pattern: occasional | N/V | N/V | N/V |
| Neg handling | Prior pattern: warm/personal | N/V | N/V | N/V |

### Response Rate
- Fresh response-tab extraction was not available in the limited-view Google Maps shells.
- Prior Motor Inn pattern remains the best observed benchmark: personal, specific, and gratitude-forward.
- New templates generated: yes.

## GBP Posts

| Metric | Motor Inn | Champion Ford | Wittrock | Okoboji Motor Co. | Macke Motors |
|---|---|---|---|---|---|
| Visible owner posts in accessible view | 0 | 1 | 0 | 0 | 0 |
| Visible post example | None surfaced | Bronco inventory post dated 2026-02-27 | None surfaced | None surfaced | None surfaced |
| Has images | Limited view | Yes | Limited view | Limited view | Limited view |
| Has CTAs | Limited view | Yes | Limited view | Book online surfaced | Service booking surfaced |
| Types surfaced | None | Inventory/update | None | None | None |

### Motor Inn Posting Status
- 0 current posts surfaced in the accessible limited view this week.
- Target remains 2-3 posts per week on Tuesday/Thursday rotation.

## Posting Patterns

### Competitor Insights
1. Champion Ford's visible post continues the simple inventory-plus-CTA pattern: one featured model, plain-language utility, direct action.
2. EXA trend research points in the same direction across GBP guidance: weekly freshness, real images, clear CTAs, and local-season specificity are the current visibility levers.
3. Google is treating GBP more like a live feed in 2026. Profiles that publish fresh posts, upload current visuals, and keep details aligned are more likely to earn AI-driven local visibility.

### Trend-Led Strategy Update
- Keep Tuesday/Thursday as the core posting cadence, with an optional Sunday slot when inventory or event relevance is strong.
- Use a 40/30/30 topic split for the next two weeks:
  - 40% service/seasonal utility
  - 30% inventory or certified/pre-owned value
  - 30% local lifestyle/community relevance
- Priority June angles from EXA research:
  - summer road-trip readiness
  - lake-season towing and cargo practicality
  - used-value / CPO reassurance
  - FAQ-style posts answering real buyer and service questions

## Action Items (This Week)
1. Publish 5 GBP posts across the next two weeks to reestablish freshness and match the active-profile pattern Google is rewarding.
2. Pair every post with a real Motor Inn image: service bay, lot walk, tow-capable truck, customer-approved delivery, or parts counter.
3. Keep review responses personal and fast while asking sales and service teams to prompt for specific language around transparency, easy process, and helpful staff.

## Keyword Phrases for Review Requests
- easy process
- helpful staff
- great service
- clear communication
- worth the drive

## Sources Used This Run
- Firecrawl Google Maps listing snapshots for Motor Inn, Champion Ford, Wittrock, Okoboji Motor Company, and Macke Motors
- Prior velocity baseline: `gbp-velocity-2026-05-21.md`
- EXA marketing-content research run completed 2026-06-04
