# REVIEW: aboutus-augment-spirit-lake

Status: `draft-needs-owner-approval`

## Wave 2 fix pass (2026-11-15)

- Editor/production language ("the page should," "do not copy," "avoid a blanket quality promise") rewritten in shopper voice; all `[NEEDS-VERIFY]` flags retained unchanged.
- On-page "Related guides" links repointed to live equivalents and re-verified curl `200`: `/car-maintenance-by-mileage`, `/2022-toyota-rav4-carroll-ia` (both 2026-11-15).
Draft: `content/drafts/seo/aboutus-augment-spirit-lake-draft.html`

## Competitor gap and augmentation decision

Phase 1 used the approved query/site fallback because no reliable top three could be extracted. The current About Us page ranks for the Spirit Lake query but offers only Carroll NAP and no Spirit Lake entity, inventory, location, or service answer. The augmentation supplies the missing question structure while flagging every location, entity, transfer, service, inventory-filter, and inspection statement that operations must approve.

**Augment `/aboutus.aspx`; do not launch a competing Spirit Lake route.** The existing page has an editable DealerOn content region, returns HTTP 200, and already receives the query signal. The requested slug `aboutus-augment-spirit-lake` identifies the handoff artifact, not a proposed public URL.

## Metadata

- Title: `About Motor Inn Auto Group and Spirit Lake Used Cars`
- Meta description: `Find Motor Inn Auto Group information, current used inventory, and the details shoppers should confirm before visiting from or shopping in Spirit Lake.`
- Slug: `aboutus-augment-spirit-lake`
- Public target: augment `https://www.motorinnautogroup.com/aboutus.aspx`
- Primary query: `motor inn of spirit lake inc used cars`

## Internal-link plan and HTTP proof

| Already-ranking source page | Proposed anchor | Target href | Proof (2026-11-15) |
|---|---|---|---|
| `/vehicle-trim-levels-explained` | `Motor Inn Auto Group locations and inventory` | `https://www.motorinnautogroup.com/aboutus.aspx` | curl `200` |
| `/car-maintenance-by-mileage` | `about Motor Inn Auto Group` | `https://www.motorinnautogroup.com/aboutus.aspx` | curl `200` |
| `/blog/heavy-duty-vs-light-duty-trucks` | `Motor Inn Auto Group location information` | `https://www.motorinnautogroup.com/aboutus.aspx` | curl `200` |

Draft inventory href `https://www.motorinnautogroup.com/searchused.aspx` returned curl `200` and resolved to `/used-inventory`, final HTTP `200`.

## Sources and every-number map

- Production About Us structure and target URL: https://www.motorinnautogroup.com/aboutus.aspx (curl `200` on 2026-11-15)
- General used-inventory destination: https://www.motorinnautogroup.com/searchused.aspx (curl final `200`)
- Query count and position exist only in the internal Phase-1 audit and do not appear in public copy: `brain/reports/wave2-audit-2026-11-15.md`.
- No public-facing numeric Spirit Lake fact is asserted.

## NEEDS-VERIFY

Count from pre-flight grep: **9**.

1. Whether “Motor Inn of Spirit Lake Inc” is the current legal or public-facing entity name.
2. Approved relationship wording among that entity, Motor Inn Auto Group, and Carroll.
3. Spirit Lake street address.
4. Spirit Lake sales phone number.
5. Spirit Lake sales and service hours.
6. Permanent Spirit Lake-only used-inventory filter and proof that the filter persists.
7. Transfer policy, participating locations, exclusions/fees, and lead time.
8. Spirit Lake-specific departments/services.
9. Inspection/reconditioning checklist, universal steps, responsible team, approved wording, and shopper-visible records.

## Approval questions for Spencer

1. What exact entity/ownership wording and Spirit Lake NAP should this augmentation use?
2. Which Spirit Lake services and transfer terms can operations stand behind on every applicable transaction?
3. Do you approve augmenting `/aboutus.aspx` rather than creating a new public route?
