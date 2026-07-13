# sMedia Google Ads Change Audit - 2026-06-30

Window: 2026-06-01..2026-06-30

## Summary

- Total change events: 846
- Grouped change clusters: 14
- Review-worthy clusters: 8
- Paid clicks in window: 28,065
- Paid conversions in window: 9994.7

## Review-Worthy Patterns

| Risk | Day | User | Client | Operation | Resource | Changes | Why / Ask |
| --- | --- | --- | --- | --- | --- | --- | --- |
| approval-needed | 2026-06-02 | erin@smedia.ca | GOOGLE_ADS_API | CREATE | AD_GROUP_CRITERION | 676 | Likely search-term/keyword expansion or cleanup. Reason flags: keyword/criterion churn, API-driven change, large same-day change batch. Ask which query report or negative-keyword logic triggered the batch. |
| ask-sMedia | 2026-06-01 | erin@smedia.ca | GOOGLE_ADS_API | UPDATE | CAMPAIGN_BUDGET | 20 | Likely budget pacing or allocation activity. Nearby window has 28,065 paid clicks and 9994.7 conversions; ask sMedia what pacing rule or performance signal drove this. |
| ask-sMedia | 2026-06-01 | erin@smedia.ca | GOOGLE_ADS_API | UPDATE | AD | 15 | Likely ad-copy or landing-path iteration. Reason flags: ad final URL changed, API-driven change, outside normal business hours. Ask what test, page, or conversion issue this edit was meant to solve. |
| ask-sMedia | 2026-06-02 | erin@smedia.ca | GOOGLE_ADS_API | UPDATE | AD | 9 | Likely ad-copy or landing-path iteration. Reason flags: ad final URL changed, API-driven change. Ask what test, page, or conversion issue this edit was meant to solve. |
| ask-sMedia | 2026-06-02 | erin@smedia.ca | GOOGLE_ADS_API | UPDATE | CAMPAIGN_BUDGET | 9 | Likely budget pacing or allocation activity. Nearby window has 28,065 paid clicks and 9994.7 conversions; ask sMedia what pacing rule or performance signal drove this. |
| review | 2026-06-01 | erin@smedia.ca | GOOGLE_ADS_API | CREATE | ASSET | 4 | Reason flags: API-driven change, outside normal business hours. Ask sMedia for the optimization rationale if this was not tied to a documented test. |
| review | 2026-06-01 | erin@smedia.ca | GOOGLE_ADS_API | UPDATE | CAMPAIGN | 2 | Reason flags: API-driven change, outside normal business hours. Ask sMedia for the optimization rationale if this was not tied to a documented test. |
| review | 2026-06-01 | integrations2@fluencyinc.co | GOOGLE_ADS_WEB_CLIENT | UPDATE | CAMPAIGN | 2 | Reason flags: outside normal business hours. Ask sMedia for the optimization rationale if this was not tied to a documented test. |

## All Top Change Clusters

| Day | User | Client | Operation | Resource | Changes | Reasons |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-06-02 | erin@smedia.ca | GOOGLE_ADS_API | CREATE | AD_GROUP_CRITERION | 676 | keyword/criterion churn; API-driven change; large same-day change batch |
| 2026-06-02 | erin@smedia.ca | GOOGLE_ADS_API | UPDATE | AD_GROUP_CRITERION | 64 | API-driven change |
| 2026-06-01 | erin@smedia.ca | GOOGLE_ADS_API | UPDATE | CAMPAIGN_BUDGET | 20 | budget amount changed; API-driven change; outside normal business hours |
| 2026-06-02 | erin@smedia.ca | GOOGLE_ADS_API | CREATE | ASSET | 18 | API-driven change |
| 2026-06-02 | erin@smedia.ca | GOOGLE_ADS_API | CREATE | AD_GROUP_ASSET | 16 | API-driven change |
| 2026-06-01 | erin@smedia.ca | GOOGLE_ADS_API | UPDATE | AD | 15 | ad final URL changed; API-driven change; outside normal business hours |
| 2026-06-02 | erin@smedia.ca | GOOGLE_ADS_API | UPDATE | AD | 9 | ad final URL changed; API-driven change |
| 2026-06-02 | erin@smedia.ca | GOOGLE_ADS_API | UPDATE | CAMPAIGN_BUDGET | 9 | budget amount changed; API-driven change; outside normal business hours |
| 2026-06-02 | erin@smedia.ca | GOOGLE_ADS_API | CREATE | AD_GROUP_AD | 6 | API-driven change |
| 2026-06-01 | erin@smedia.ca | GOOGLE_ADS_API | CREATE | ASSET | 4 | API-driven change; outside normal business hours |
| 2026-06-02 | erin@smedia.ca | GOOGLE_ADS_API | UPDATE | AD_GROUP | 3 | API-driven change |
| 2026-06-02 | erin@smedia.ca | GOOGLE_ADS_API | CREATE | AD_GROUP | 2 | API-driven change |
| 2026-06-01 | erin@smedia.ca | GOOGLE_ADS_API | UPDATE | CAMPAIGN | 2 | API-driven change; outside normal business hours |
| 2026-06-01 | integrations2@fluencyinc.co | GOOGLE_ADS_WEB_CLIENT | UPDATE | CAMPAIGN | 2 | outside normal business hours |

## Guardrails

- This report observes change history; it does not infer intent beyond nearby evidence.
- Any Ads mutation requires Spencer approval in a separate workflow.
- Ask sMedia for rationale on `ask-sMedia` and `approval-needed` clusters.
