# 6. Dealership topical map

## Purpose
Give each meaningful buyer task one owning page and a useful route to inventory or service.

## Inputs
Current three-host crawl; GSC query clusters if available; job 1 questions; current model/stock/service lists; prior drafts. Paths below are candidates, not assertions of live routes.

## Starting map
| Cluster | Owning host proposal | Hub -> children | Conversion |
|---|---|---|---|
| Used vehicles | group | `/used-inventory` -> `/used-trucks`, `/used-suvs`, used model categories | matching live inventory |
| New Toyota | Toyota | new Toyota hub -> Tundra, Tacoma, RAV4, Camry, Highlander | filtered Toyota inventory |
| New Chevrolet | Chevrolet | new Chevrolet hub -> Silverado, Equinox, Traverse, Tahoe | filtered Chevrolet inventory |
| Trade-in | group | trade-in hub -> appraisal process, documents, payoff questions | verified appraisal form |
| Financing | group; brand-specific offers only on relevant host | financing hub -> process, documents, lease vs finance | secure application |
| Service/tires | relevant Toyota or Chevrolet host | service hub -> oil change, brakes, tires, scheduled maintenance | verified scheduler, hours/contact |
| Sell to us | group | sell-my-car hub -> appraisal without purchase, process, documents | purchase/appraisal inquiry |

## Exact steps
1. Build a URL inventory from the current crawl. Record status, canonical, indexability, intent, host and inbound links. Retain aliases but choose a canonical candidate only with evidence.
2. Attach each keyword/question to one primary cluster. Separate buying used from buying new, trade-in with a purchase from selling outright, and general financing from specific current offers.
3. Map model pages to the correct franchise. Confirm a model/year is current and offered before proposing it. Used non-franchise models belong in used inventory, not a new-car franchise hub.
4. Match existing pages first. If `/searchused.aspx` and `/used-inventory` serve the same task, flag job 9 and hold a second page until canonical ownership is reviewed.
5. Add a new page only for a distinct buyer need with useful original evidence. Address the six core towns naturally within helpful regional content; do not clone every model × city combination. Fort Dodge/50501 and Okoboji remain expansion candidates requiring independent evidence.
6. For each node, specify parent, primary question, unique content/proof, two relevant internal links, conversion target, priority and status: keep/improve/propose/merge-review/hold.
7. Feed candidates to job 5 and approved topology to jobs 7 and 8. Do not change live routing.

## Output artifact path
`/Users/spencerheywood/motor-inn-seo/agents/runs/RUN_DATE/topical-map.csv`
Columns: `cluster,node_id,owner_host,existing_url,proposed_url,parent_id,primary_intent,questions,market_segment,unique_evidence,conversion_url,status,dependency`.
Also `topical-map.md` for the hierarchy and unresolved ownership decisions.

## Verification checklist
- [ ] Tundra, Silverado, RAV4, Equinox and all requested transaction/service clusters represented.
- [ ] New-model franchise ownership correct.
- [ ] Every node has unique intent and a useful next action.
- [ ] No mass-generated city duplicates or proxy URLs.
- [ ] Existing canonical conflicts remain review items.
