# Motor Inn Auto Group — Monthly SEO Report
## September 2026

---

### Read This First (30-Second Summary)

**Calls from organic:** 2 (-80% vs August)
**Organic traffic:** 744 sessions (-23% vs August)
**Organic forms:** 1 (-89%)
**Bottom line:** Organic call volume fell this month — that is the number to fix first; everything else is context until it recovers.

---

### 3 Wins This Month

1. No tracked money metric improved by more than 2% this month.

### 3 Problems That Need Fixing

1. **Form submissions from organic search declined** — 1 forms vs 9 last month (-89%).
2. **Calls from organic search declined** — 2 calls vs 10 last month (-80%).
3. **Organic sessions declined** — 744 sessions vs 968 last month (-23%).

> ⚠️ ESCALATION THRESHOLD: Organic calls dropped -80% MoM (threshold -30%).
> ⚠️ ESCALATION THRESHOLD: Organic form submissions dropped -89% MoM (threshold -30%).

### The One Thing for Next Month

**Publish the ready Carroll local pages and link them from the money pages** — Start with the Carroll dealership, Toyota dealer, and used-cars pages, then link them from `/used-inventory`, `/contactus.aspx`, `/new-toyota`, and the homepage. This is the fastest way to raise non-brand organic traffic without waiting on a full site rebuild.

_(Carried forward from last month's report; this build does not re-derive strategy. If it shipped, replace it — the latest website audit's top recommendation is the candidate.)_

---

### Traffic Scorecard

| Metric | September 2026 | Prior Month | MoM Change |
|--------|----------:|------------:|-----------:|
| Total sessions | 9,074 | 9,589 | -5% |
| Organic sessions | 744 | 968 | -23% |
| Organic % of total | 8% | 10% | -2 pp |
| New users | 5,585 | 5,973 | -6% |

### Key Events (Conversions)

| Event | Total | Prior | MoM | From Organic | Organic Prior |
|-------|------:|------:|----:|-------------:|--------------:|
| asc_vdp_view | 7,146 | 7,826 | -9% | 474 | 584 |
| used_vdp | 24 | 11 | +118% | 4 | 4 |
| new_vdp | 3 | 9 | -67% | 2 | 2 |
| asc_click_to_call | 97 | 130 | -25% | 2 | 10 |
| asc_form_submission | 20 | 31 | -35% | 1 | 9 |

### Traffic Sources (GA4 default channel groups)

| Channel | Sessions | % of Total | MoM Change |
|---------|---------:|-----------:|-----------:|
| Paid Social | 3,326 | 37% | -1% |
| Paid Search | 1,904 | 21% | -7% |
| Unassigned | 1,004 | 11% | -5% |
| Direct | 988 | 11% | -4% |
| Cross-network | 761 | 8% | -6% |
| Organic Search | 495 | 5% | -28% |
| Organic Social | 229 | 3% | -7% |

### Top Organic Pages (sessions from Organic channels)

| Page | Sessions | MoM Change |
|------|---------:|-----------:|
| / | 285 | -20% |
| /used-inventory | 214 | -31% |
| /contactus.aspx | 125 | -28% |
| /searchnew.aspx | 109 | +6% |
| /new-toyota | 55 | -40% |
| /used-trucks | 44 | +19% |
| /searchall.aspx | 35 | +119% |
| /used-Carroll-2009-Ford-Escape-Hybrid-1FMCU49379KB61755 | 26 | — |

### GSC Top Queries (from latest weekly audit)

| Query | Clicks | Impressions | Position |
|-------|-------:|------------:|---------:|
| motor inn carroll | 39 | 113 | 1.1 |
| motor inn carroll iowa | 24 | 65 | 1.8 |
| motor inn | 7 | 48 | 4.3 |
| motor inn carroll ia | 7 | 19 | 1 |
| motor inn toyota of carroll | 6 | 20 | 1.6 |
| toyota carroll iowa | 6 | 30 | 4.5 |
| carroll iowa car dealerships | 5 | 17 | 4 |
| carroll toyota | 4 | 20 | 4.4 |

### GBP & Citation Status (quoted from latest audits, not re-run)

#### structural audit (2026-08-17)

> # GBP Structural Audit — 2026-08-17
> ## Executive Summary
> - **The biggest new signal this week is a phone NAP discrepancy on the live Motor Inn listing.** The public Google Business Profile shows **(712) 792-5000**, but the documented NAP in `product-marketing-context.md` is **(712) 522-2526**. An inconsistent phone number across the web weakens local ranking and confuses shoppers. This must be reconciled in GBP admin before anything else.
> - **Competitor activity is accelerating while Motor Inn is flat.** Okoboji Motor Company (1,011 reviews) now surfaces a **Book online** CTA plus **Delivery** and a **Videos** tab; Macke Motors surfaces **Book online**; Wittrock and Choice Auto both posted photos within the last 1–3 weeks; Spirit Lake Ford CDJR runs a live owner post with a financing offer. Motor Inn showed none of these action or freshness signals today.
> - **Next:** verify the correct phone number, enable/confirm a service-booking action, publish one owner post, and start the photo cadence. These are the highest-leverage moves.
> - **Spencer needs to decide the phone number (792-5000 vs 522-2526)** and whether Motor Inn's GBP should surface a booking/service action and a GMC category signal.
> ## Data Collection Status
> | Source | Status | Notes |

#### velocity audit (2026-10-01)

> # GBP Velocity Audit — 2026-10-01
> ## Method note (migration)
> - Runbook tool `gstack-browse` remains unavailable; this run used the **GBP API directly** (owner OAuth + configured fallback, same credential stack as the daily review-reply job) via a one-off pull script on nada-mini. Data below is from `mybusiness.googleapis.com/v4` + `mybusinessbusinessinformation.googleapis.com/v1` — not screen-scraped, so totals are exact, not panel estimates.
> - Locations covered: **Motor Inn Toyota and Chevrolet of Carroll** (locations/14730652758503817758, the review-bearing primary listing) and **Motor Inn Chevrolet of Carroll** (locations/2099693230539902964). The posts-publisher listing (locations/1983269944339166584, "Motor Inn Auto Group") carries the localPosts and **0 reviews** — that is why the old 08-27 audit's "204 live reviews" figure does not match API counts; the two audits measured different listings.
> - Competitor panels were not re-scraped this cycle (API has no competitor reviews access); 08-27 competitor baselines carried forward and flagged as such.
> ## Executive Summary
> - **Review velocity is real and now precisely measurable: 47 reviews since Jul 1 on the primary listing** (2 in July, 18 in Aug, 26 in Sep, 1 so far in Oct). That is **~23/month across Aug–Sep** on the API surface. The mid-August review-ask re-energization is holding: Sep was the best month measured to date (26).
> - **Reply discipline fixed itself.** Median reply lag on reviews since Jul 1 is **~1.0 day** (was 1–2 months in the 08-27 audit). Slowest recent reply was 6.9 days (Monica Schiltz). 49 of the last 50 primary-listing reviews have replies.

#### website audit (2026-10-01)

> # Monthly Website SEO Audit - Motor Inn Auto Group - 2026-10
> **Generated:** 2026-10-01
> **Purpose:** identify local SEO gaps and feed the monthly page-draft pipeline.
> **Status:** actionable draft set created for Spencer review.
> ## Executive Summary
> - GA4 90-day sessions captured: **27,763**
> - GA4 90-day users captured: **18,182**
> - Sitemap URLs found: **224**

#### authority audit (2026-07-02)

> # Local Authority Audit — July 2026
> ## Executive Summary
> - **Overall status:** Motor Inn's entity is still fragmented across citations. The canonical NAP is stable on the main site, but major third-party listings continue to use legacy sub-brand names and non-canonical phone numbers.
> - **Most urgent issues:** Google Business Profile duplication/fragmentation, Facebook phone/name mismatch, Yelp service listing mismatch, BBB mismatch, Yellow Pages mismatch.
> - **Biggest wins this month:** The live site now exposes the correct canonical NAP and geo coordinates, and the homepage already ships JSON-LD. The next lift is normalization, not starting from zero.
> - **Method note:** The runbook called for `gstack-browse`, but that surface is not available in this environment. This audit used Firecrawl, direct site fetches, and the provided source-of-truth files instead.
> ## Current Local SEO Standards Snapshot
> Source research run first:

---

### Data Notes

- GA4 property: 364125348; windows 2026-09-01..2026-09-30 vs 2026-08-01..2026-08-31
- GSC: via latest weekly audit Top Queries table
- Audit freshness: structural 2026-08-17 (STALE, over 45 days old), velocity 2026-10-01, website 2026-10-01, authority 2026-07-02 (STALE, over 45 days old)
- Build: deterministic no-model lane (monthly-seo-performance-report.js). Narrative lines are templated from computed numbers; nothing here came from a language model. Replaces the retired OpenClaw job `seo-monthly-report`.
- Delivery: repo + Slack only (stakeholder email lane not migrated; the executive report covers email).
