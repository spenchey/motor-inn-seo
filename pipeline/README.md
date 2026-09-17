# Local SEO pipeline

Run from `/Users/spencerheywood/motor-inn-seo` with Python 3.13:

```bash
python3 automation/orchestrator.py --init-only
python3 automation/orchestrator.py --limit 3
python3 automation/page_generator.py
python3 automation/approval_sync.py
python3 automation/publish_handler.py
```

`automation/run_pipeline.sh` sequences inventory evidence collection → content builder → weekly research → pending content refresh → October post import → page generation. The daily approval wrapper refreshes inventory and pending content before generation and approval sync. Scheduling instructions are in `automation/cron_entries.md`. Generated data, source caches and approval receipts are excluded from git. These commands do not install schedules.

The weekly driver validates configured candidates against `agents/topical-map.md`, ranks with the opportunity-scoring rules and checks GSC before creating jobs. `config/candidates.json` supports either a list or an object with a `candidates` list. Candidate fields include `cluster`, `slug`, `title`, `target_query`, `owner_host`, `target_url`, `gsc_property`, `destination`, `outline`, `estimated_hours`, `relevance`, and `ai_question_ids`; optional `query_variants` are exact normalized alternatives. A slug or matching host/query already present in any queue is not duplicated. Weekly counts include ready/held/rejected jobs and legacy jobs dated in the current week.

`automation/content_builder.py` writes `inputs/verified-content.json` as an object keyed by candidate slug. Each value supplies `meta_description`, `sections` (headings plus claims with text/evidence_ids), `source_evidence` (id, allowed source_type, HTTPS source URL, retrieved_at, verified, verbatim supported claims), `internal_links` (URL, descriptive anchor, HTTP status, canonical, checked_at, evidence_ids), and `topology_status: verified` only after crawl review. Optional `faq`, `business`, and `staging_read_status` require the same evidence. Source-built `title` and `outline` are merged with the body; builder blockers are retained. Technical SiteCrawl evidence is allowed for link URL/anchor only. The automatic builder currently covers supported inventory selections only; other domains remain explicitly blocked without authoritative source fields. Missing factual content stays pending. Inventory aggregates alone do not establish a consumer page's complete copy or route topology. Input shape is exercised in `automation/tests/test_end_to_end.py`; its synthetic data must never be copied to production.

`inputs/ai-mentions.csv` can supply the runbook's consumer observations with question_id, surface, observed_at, status, cites_dealer_site and evidence_path. Supported surface labels are ChatGPT, Perplexity and Google Search AI Overviews. Completed observations require a real local evidence file and recent timestamp. Unobserved/no-overview results never imply a missing citation. The driver separately requests a bounded DataForSEO Google AI Overview observation for the candidate's first question; this does not establish consumer ChatGPT or Perplexity coverage.

Directory ownership:

- `queue/pending`, `queue/drafts`, `queue/approved`, `queue/ready`, `queue/hold`, `queue/rejected`: JSON state markers.
- `drafts/<slug>`: HTML, metadata, evidence and QA, bound by one digest.
- `ready-for-dealeron/<slug>`: final HTML plus metadata, evidence, QA, submission text and receipt marker.
- `ready-for-content`: October immutable content handoffs.
- `cache`: seven-day provider JSON/image evidence; GSC refreshes daily.
- `approvals/{inbox,processed,events}`: authenticated receipts and replay markers.
- `handoffs`, `email-drafts`, `ai-prs`, `runs`, `logs`: operator outputs and evidence.

DealerOn email drafts are consolidated by ISO week and are never sent here. AI execution needs the configured proxy checkout/content mapping and `publish_handler.py --execute-ai`; the default mode only prepares PR state. No merge or deployment command exists. See `automation/approval_state.md` for the exact Slack contract.
