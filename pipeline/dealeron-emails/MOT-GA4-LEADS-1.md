- Subject: Re: Google support team — case 01922137
- messageId: 1a0cabb23ac77215 / thread 1a0caa43adbfd3e4
- date: 2026-09-22 ~17:45 CT
- note: Jamahl asked which GA4/GTM Google should review (Google found multiple installs).
  Answered with ONE issue: scope = GA4 property 364125348 via GTM-WBJPXB7 (dotagging v2212).
  Explained the two extra G- snippets (G-VLVJFG0PF2, G-BYR9W9V99J) as partner/legacy,
  out of scope. Evidence: dotagging.js fetch + GA4 Admin dataStreams (364125348's only
  stream = G-423R5J010M).

## Jamahl reply decoded (case 01922137) — 2026-09-23
DealerOn says: GTM-WBJPXB7 does NOT fire asc_generate_lead_sales/other (not standard ASC);
form_start/form_submit not supported; asc_click_to_text = custom coding. Most flagged issues
= our custom code + portal site's 2 extra containers.

GA4 live (364125348, 28d): asc_form_submission 17, _sales 12, _other 3; form_start 757,
form_submit 3; NO asc_generate_lead_* firing; sms 2.


## RESOLUTION 2026-09-23
- Case 01922137 CLOSED politely (msg 1a0cec7d7cfee4f2): custom events = our side.
- Key events web_lead_received + asc_form_submission trio registered in GA4 09-22.
- NEXT (our build): dealer-owned GTM container with lead-capture tags (web_lead_received
  lid-gate fix catching thankyou.aspx DealerSocket IDs; asc_generate_lead_sales/_other
  mapping) + ONE-issue DealerOn email requesting container install site-wide.
- GTM container creation needs tagmanager.edit consent (fresh grant) - pending Spencer
  consent or gog interactive flow.
