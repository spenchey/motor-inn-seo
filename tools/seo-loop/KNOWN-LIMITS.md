# Known limits of the staged SEO loop

These are accepted limits, recorded after two independent reviews. Each is either covered by a person reading the output, or blocks a named go-live step.

## Blocks a go-live step
| Limit | What it blocks | What must happen first |
|---|---|---|
| The AI-answer spend guard is not matched to a real ledger. The real DataForSEO record is a daily reconciliation on Mac mini 2, and its latest run logged `provider_account_usage_unavailable`. | Live paid AI-answer capture | Choose one authoritative spend source reachable from the capture host, then rebuild and test the guard against it. |
| Page proof has never been tested against how DealerOn really serves missing, blocked or redirected pages. A not-found page that names itself as the canonical address would still pass. | Trusting the fix checker on live sites | Run the fix checker read-only on a copy of the register against known good and known missing pages, and review the results before any row may be marked fixed. |
| The live GBP publisher still trusts the `**Approval:**` line in the draft file. | Relying on approvals being tied to exact wording | Spencer's decision on locking approvals. |

## Covered by a person reading the output
| Limit | Why it is acceptable |
|---|---|
| Wording gates cannot catch every banned phrase or model name (R7). | They are aids. Spencer reads every public packet in full before approving. |
| Hand-written fix rules can be weak (R6). | Rules from the watch and the catalog are literal. Hand-written rules are reviewed by the coordinator. |
| Watch-made title rows confirm the old town name is gone, but not that Carroll leads (R8). | The wanted title is approved by Spencer, and seed rows use the stronger rule. |
| Personal names and street addresses cannot be detected reliably in agent-written reports (R9). | Reports come from our own jobs, which are told not to include customer data. |
| The Monday note can carry an unusual code or a personal name in rare wording (R10). | It goes only to Spencer, and its text comes from internal findings. |
| The register cannot tell who really spoke an approval quote (R18). | The coordinator reads Spencer's own message before recording it. |
| The GBP approval key joins fields with `|`, so moving words across that separator between the copy and the button keeps the same key. | No new words can be added this way, and the staged packet is not yet used for live approvals. |
| Someone with shell access can hand-edit the register or code. | Outside the threat model. Git history and the validate command make this visible. |
