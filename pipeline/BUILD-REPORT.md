# Motor Inn automation build — September 16, 2026

Status: **local build and offline end-to-end verification complete.** Live Slack delivery/intake, scheduler activation and AI-proxy destination setup are not complete.

## Implemented behavior

The weekly orchestrator reads the topical-map cluster table and runbook hashes, validates configured page candidates, ranks using query-only GSC demand (or clearly labeled volume proxy) × ease × relevance, checks existing query/page ownership, and creates bounded JSON jobs in `queue/pending`. It deduplicates slugs and host/query intent, including www aliases and prior queue states. It counts jobs against a weekly cap across all states, including legacy creation timestamps. Provider errors and missing facts are never treated as verification. Weekly runs also refresh research for a bounded number of existing pending jobs, even when the new-job cap is exhausted; failed refreshes preserve old evidence and source fields.

DataForSEO uses the mirrored cost policy with a $2 daily admission cap, conservative reservations before requests, a durable ledger, seven-day JSON caching, local screenshot retention and no retry of uncertain paid requests. Keyword volume uses keywords_data; top-ten SERPs supply competitor visibility evidence. A bounded exact runbook question supplies a separately labeled Google API AI Overview observation. Consumer ChatGPT, Perplexity and Google evidence remains separately sourced; unobserved/NO_OVERVIEW never means missing citation. The screenshot response contract was checked against [DataForSEO documentation](https://docs.dataforseo.com/v3/serp/screenshot/).

The source builder assembles dated inventory content from verified make/model/type/style aggregates and checks real same-host canonical inventory destinations. It refreshes pending jobs only, preserves research blockers and holds unsupported service/finance/trade/sell content and missing route/staging evidence. SiteCrawl records can support link URLs/anchors only, never dealership body/meta/business claims.

The page generator renders supported claims, metadata, links and applicable Article/FAQPage/LocalBusiness schema. Drafts require fresh evidence, source-linked factual strings, verified topology and a checked GSC gate. Failing jobs remain pending with errors. The approval receiver verifies original signed Slack requests and Spencer/channel identity; decisions bind to the exact draft digest. Publication rechecks approval, current source evidence and QA.

The publisher copies the exact approved final-candidate HTML into DealerOn HTML/metadata/evidence/QA/submission packets and one consolidated ISO-week email draft with a Jeeves handoff. It does not email or open support tickets. AI targets use isolated worktrees and `seo/<slug>-<digest>` branches with `gh` PR creation when execution is enabled; no main-branch push or merge exists. Remote PR behavior is implemented but has no live approved-page canary in this build. October posts share the same approval queue and retain their upstream owner and unresolved publication blockers.

## Observed integration evidence

- Existing GSC cache: group property `sc-domain:motorinnautogroup.com`, 1,899 query rows and 3,728 query/page rows; Toyota property accessible with zero rows; `https://www.motorinnofcarroll.com/` remains `BLOCKED-NO-ACCESS`. Window August 18–September 14. Credentials remain on the Mac mini and are read through SSH alias `codex-mac-mini`; requested `nada-mini` is documented as unresolved on this host. No service-account JSON was copied here.
- Existing successful DataForSEO volume and question-SERP/screenshot responses inspected. One financing SERP returned provider error 40101 and remains recorded as blocked. September 16 ledger: **$0.10 actual / $0.32 charged-or-reserved**, under the $2 cap. No ledger reset. Continuation downloaded the already-paid cached screenshot (510,790 bytes) without another paid API call.
- Collector evidence: verified Carroll Store 9 / DVD56054 DealerVault feed, 72 rows, SHA-256 `5a509ec04642bbf5876f467886f016fd48dffe8f557186688db09ae8abc0c8ca`, 48-hour source TTL. Only aggregates/provenance are stored; no VIN/raw-feed export.
- Final read-only builder run: **0 fully assembled / 11 blocked**, with five actual source-derived inventory briefs retained. The discovered `/used-trucks` link passed HTTP/canonical/heading checks, but its page remains blocked by the required staging comparison. Model-filtered Toyota/Chevrolet URLs rendered generic new-inventory headings, so the builder did not claim their model filters were proven. SUV classification and noninventory facts remain unavailable. Exact result: `pipeline/content-builder-last-run.json`. A narrow same-path parent-canonical exception is tested and requires complete filter/heading/canonical proof; it did not bypass these live failures.
- Final local queue snapshot: 12 October content drafts, three blocked October posts and one blocked financing research job; zero approved or ready jobs. These are local imports, not Slack delivery or publication.
- Direct `launchctl print` checks found all three SEO labels not loaded (exit 113). Definitions and install commands are supplied; they have not been activated.

## Test results

**106 tests passed**, Python compilation passed, both shell wrappers passed syntax checks, all three launchd plists passed lint, and `git diff --check` passed. Verified at `2026-09-17T00:43:40.881740+00:00`. Machine-readable results and source hashes: `pipeline/runs/build-validation.json`. No `test-page-alpha` artifacts remain anywhere under the real pipeline.

Coverage includes source freshness/expiry, escaping and schema, fixture rejection, budget/cache/unknown-cost retention, GSC ownership holds, weekly caps and pending refresh, immutable source import, authenticated approval/replay/tampering/rejection chronology, publication revalidation, and the integrated sample journey. Remote GitHub PR execution has not been canaried against the actual proxy repository.

The `test-page-alpha` exercise uses an isolated TemporaryDirectory: fake provider responses → real orchestrator → real HTML generator/QA → digest displayed in approval summary → signed simulated Slack event using temporary keys → real approval sync → real DealerOn packet/email-draft/ready marker. It verifies reruns create neither duplicate jobs nor email drafts. Temporary sample data, keys, receipts and output are deleted on exit. No test approval is represented as Spencer's approval, and no sample was published. Additional tests enforce fixture rejection in the production publisher.

Reproduce:

```bash
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3.13 -m unittest discover -s automation/tests -q
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3.13 -m unittest discover -s automation/tests -p test_end_to_end.py -v
```

## Exact Slack approval format

Jeeves is to display the generated `pipeline/APPROVALS-TODAY.md` entries:

```text
## <actual-slug>
- Target query: <actual query>
- Estimated monthly volume (DataForSEO): <measured volume or unavailable>
- Outline: <one-line outline>
- Draft: drafts/<actual-slug>/index.html

APPROVE <actual-slug> <actual-64-character-draft-digest>
HOLD <actual-slug> <actual-64-character-draft-digest>
REJECT <actual-slug> <actual-64-character-draft-digest>
```

One exact command per Slack message. A changed draft requires a new digest. The full original Slack body/timestamp/signature goes to the Jeeves receipt recorder; self-asserted author IDs and bot messages cannot approve. See `automation/approval_state.md` for the complete bridge contract and configuration.

## Schedules to install

Use either the launchd definitions or cron, never both. Host calendar scheduling must be America/Chicago. LaunchAgent installation commands are in `automation/cron_entries.md`.

```cron
0 6 * * 1 cd /Users/spencerheywood/motor-inn-seo && /bin/bash automation/run_pipeline.sh >> pipeline/logs/orchestrator.out.log 2>> pipeline/logs/orchestrator.err.log
30 7 * * * cd /Users/spencerheywood/motor-inn-seo && /bin/bash automation/approval_sync.sh >> pipeline/logs/approval-sync.out.log 2>> pipeline/logs/approval-sync.err.log
45 7 * * * cd /Users/spencerheywood/motor-inn-seo && /Library/Frameworks/Python.framework/Versions/3.13/bin/python3.13 automation/publish_handler.py --execute-ai >> pipeline/logs/publish-handler.out.log 2>> pipeline/logs/publish-handler.err.log
```

Local execution depends on the existing `agents/` runbooks and the configured host paths. Those source runbooks remain existing untracked project inputs; this is not a clean-clone portability claim.

## Remaining live setup and source gaps

- Slack identity/channel/signing-secret/receipt-key settings are blank. The Jeeves outbound handoff and authenticated inbound receiver are implemented locally; a live delivery/intake bridge has not been connected or proven.
- DealerOn support recipient is blank. The pipeline creates an unsent draft; the existing authorized Jeeves delivery workflow must supply the verified recipient and send proof.
- AI-proxy checkout/content-directory mapping is blank. An approved page must pass a live branch/PR canary before claiming this route operational.
- Chevrolet GSC access is missing. Used-inventory work requires the exact staged-package comparison. Consumer AI observations still have coverage gaps. Unsupported service/finance facts and unverified route topology remain blocked.
- Schedules are supplied but not installed. Spencer's intended recurring action is the Slack decision; bridge/source/scheduler provisioning is operator setup, not another recurring approval request.

## File inventory

| File | Purpose |
|---|---|
| `automation/.gitignore` | Generated artifacts and coordination scratch exclusions. |
| `automation/approval_state.md` | Slack message/receipt contract and live bridge setup requirements. |
| `automation/approval_sync.py` | Slack authentication, digest-bound decisions, chronological receipt reconciliation and approval summary. |
| `automation/approval_sync.sh` | Daily inventory/content refresh, generation and approval synchronization. |
| `automation/collect_inventory_evidence.py` | Verified Carroll DealerVault aggregate collector; raw sensitive fields excluded. |
| `automation/common.py` | Atomic JSON writes, locks, timestamps, slug validation and draft digests. |
| `automation/config/candidates.json` | Candidate intent/host/cluster definitions; not claims of existing routes. |
| `automation/config/dataforseo-cost-policy.json` | Local $2/day capped policy and seven-day cache settings. |
| `automation/config/dataforseo-cost-policy.upstream.json` | Retained upstream policy mirror. |
| `automation/config.json` | Runtime paths, provider settings and explicitly incomplete live integration configuration. |
| `automation/content_builder.py` | Dated inventory claim assembler and bounded live destination verification; pending-only refresh. |
| `automation/content_posts_hook.md` | October worktree mapping and shared approval-queue contract. |
| `automation/cron_entries.md` | LaunchAgent installation, cron equivalents, timezone and verification instructions. |
| `automation/gsc_remote.py` | Read-only service-account GSC query/page export streamed over SSH. |
| `automation/import_content_posts.py` | October manifest imports into the shared immutable approval queue. |
| `automation/launchd/com.motorinn.seo.approval-sync.plist` | Provided launchd schedule; not loaded. |
| `automation/launchd/com.motorinn.seo.orchestrator.plist` | Provided launchd schedule; not loaded. |
| `automation/launchd/com.motorinn.seo.publish-handler.plist` | Provided launchd schedule; not loaded. |
| `automation/orchestrator.py` | Weekly ranking, research admission, pending research refresh and JSON queue writer. |
| `automation/page_generator.py` | Evidence-bound HTML/schema rendering and fail-closed QA. |
| `automation/providers.py` | Allowlisted DataForSEO client with budget/cache/reconciliation and remote GSC wrapper. |
| `automation/publish_handler.py` | Verified approval consumption, exact approved DealerOn packets, consolidated email draft and isolated AI PR path. |
| `automation/run_pipeline.sh` | Weekly stage sequence; continues independent stages while retaining failure exit status. |
| `automation/tests/test_approval_publish.py` | Offline regression tests for approval publish. |
| `automation/tests/test_content_builder.py` | Offline regression tests for content builder. |
| `automation/tests/test_content_import.py` | Offline regression tests for content import. |
| `automation/tests/test_end_to_end.py` | Offline regression tests for end to end. |
| `automation/tests/test_inventory_evidence.py` | Offline regression tests for inventory evidence. |
| `automation/tests/test_orchestrator.py` | Offline regression tests for orchestrator. |
| `automation/tests/test_page_generator.py` | Offline regression tests for page generator. |
| `automation/tests/test_research.py` | Offline regression tests for research. |
| `pipeline/README.md` | Runtime, directories and input contracts. |
| `pipeline/BUILD-REPORT.md` | This inventory, verification, schedules and Slack approval format. |
| `pipeline/.gitignore` | Keeps generated evidence, queues and receipts out of git. |
| `pipeline/runs/build-validation.json` | Machine-readable final test/syntax/sample-cleanup results (local generated evidence). |
| `agents/RUN-REPORT.md` | Requested FULLY AUTOMATED PIPELINE - SEPT 16 update. |

Runtime directories are created by `orchestrator.py --init-only`: `queue/{pending,drafts,approved,ready,hold,rejected}`, `drafts`, `ready-for-dealeron`, `ready-for-content`, `cache`, `inputs`, `logs`, `runs`, `handoffs`, `approvals/{inbox,processed,events}`, `email-drafts`, `ai-prs`; isolated worktrees are created only for approved AI execution.
