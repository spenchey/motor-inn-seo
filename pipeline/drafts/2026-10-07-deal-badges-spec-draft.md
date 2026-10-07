Hi Josh,

Feeding you the data via the vehicle feed is easiest for us. Spec:

DELIVERY
- One new custom field on the vehicle feed, e.g. `badge_code` (plain text).
- Values are exactly one of: GREAT_DEAL, GOOD_DEAL, FAIR_DEAL, PRICE_ANALYSIS (blank = no badge).

IMAGE MAPPING (DealerOn hosts; we'll upload the artwork)
- GREAT_DEAL -> green 'Great Deal' ribbon (top-left of the vehicle card photo)
- GOOD_DEAL -> blue 'Good Deal' ribbon, same placement
- FAIR_DEAL -> gray 'Fair Deal' ribbon, same placement
- PRICE_ANALYSIS -> no ribbon; shows 'Free Price Analysis' text pill under the price

WHEN IT SHOWS
- Badge renders whenever `badge_code` is non-empty; blank renders nothing.
- Placement: overlay on the vehicle-card photo + same badge on the VDP gallery hero.

SOURCE
Values come from our vAuto market rating nightly; we'll populate `badge_code` in the feed
we already send. If feed fields are configured on your side, send me the exact field-name
requirements and I'll match them.

Once the mapping is in, send me a staging URL with one vehicle per value and I'll verify
before we go live.

Thanks,
Spencer Heywood
Motor Inn Auto Group - Carroll, IA
