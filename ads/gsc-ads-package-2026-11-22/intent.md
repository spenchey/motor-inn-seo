# Intent tiers for queries with 20+ impressions

Rule: would this person buy a vehicle in 30 days?

| Tier | Count |
|---|---:|
| ready-now | 206 |
| researching | 210 |
| brand | 4 |
| navigational | 0 |
| research-only | 502 |


## Classification logic

- Brand: includes standalone and misspelled brand phrases, including “Motor Inn”.
- Navigational: action-page intent (contact, hours, directions), not shopping intent.
- Research-only: definitions, comparisons, repairs, DIY, maintenance, and questions about vehicle features.
- Ready-now: explicit buying signal such as dealership, dealer, cars “for sale”, buy, lease, pricing, financing, inventory, auto sales, car lots.
- Researching: broad vehicle interest without the stronger buying signal, e.g., “Toyota” or “used cars”.

Counts above use unique query strings from the source GSC export.

