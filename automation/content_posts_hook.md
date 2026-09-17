# One approval queue for SEO pages and October posts

The read-only adapter is `automation/import_content_posts.py`. Its upstream is `/Users/spencerheywood/Worktrees/motorinn-month-ahead-content-holmes-v3/months/2026-10/W40` through `W44`, each with `manifest.json`, `sources.json`, `assets.json`, `pieces/P1/draft.md` through `P3/draft.md`, and weekly adaptations. The observed manifest quota is 15 posts plus five videos. This adapter imports the 15 post pieces; video scripts/masters remain under Emily's established production and final-media gates. Website roundups and email adaptations remain bound supporting inputs, never automatic sends.

| Upstream value | Shared pipeline value |
| --- | --- |
| `package_id`, `iso_week`, `version`, `authorship` | Full immutable `upstream_manifest` plus absolute path and byte SHA-256 in draft metadata |
| `piece_id`, title, channel adaptations, proposed time | `upstream_piece_id`, title, channels, proposal-only schedule |
| Every piece file `path`, `role`, `sha256` | Exact UTF-8 `content_files` stored inside digest-bound `meta.json`; no rewrite |
| `package_files` including source/asset/provenance registries | Exact hash-checked `upstream_package_files` in metadata |
| Piece `source_ids` -> `sources.json.items` | Original claim mappings, URLs, access dates and expiries in `source_evidence` and `evidence.md` |
| Original immutable piece/source/authorship revision | `content-oct26-wXX-pN-<12 digest chars>`; repeated imports are idempotent; changed content requires a new approval |

Run `python3.13 automation/import_content_posts.py --all-october --check-only` for validation only, or omit `--check-only` to import. A single manifest can be selected with `--manifest /absolute/path/manifest.json`. The weekly shell runner imports after orchestration and before page generation. It reads upstream files only and never starts Holmes, Rory, Emily, GPU work, or an upstream scheduler.

The same queue transitions apply: `pipeline/queue/pending/` → `queue/drafts/` → `queue/approved/` → `queue/ready/`. Missing/unverified/expired cited sources stay pending with errors. Hash mismatches fail the manifest import. Exact-text review artifacts reside in `pipeline/drafts/<slug>/`: `index.html` is an escaped human-readable review wrapper explicitly marked **not a publishable SEO page**; `meta.json` contains the original text and provenance; `evidence.md` preserves source claim mappings. `qa-report.json` verifies import integrity only, not factual/creative approval. All three review artifacts are covered by the common approval digest.

`APPROVALS-TODAY.md` includes both job kinds. Estimated SEO volume for a social post is “unknown”, not a fabricated number. Explicit digest-bound Spencer approval recorded by Jeeves moves the record to approved. The publisher recognizes `kind=content_post` / `target_platform=content_post`, verifies the bound content, and exports exact approved files to `pipeline/ready-for-content/`. It must never route this review wrapper to DealerOn or the AI proxy.

This queue's approval authorizes **preparing the content handoff**. Upstream `EXECUTION-PLAN.md` and `WORKFLOW.md` still require a weekly digest-bound preproduction approval and a separate final publication manifest binding media, accounts, captions, schedule and action. An imported copy is not production or publication permission. Missing assets, usage rights, source refreshes and channel/provider readbacks remain explicit blockers; no automatic text-only fallback. The existing upstream review and production owners retain control. One local approval listing is implemented; a live Jeeves Slack bridge and upstream handoff consumer must be verified before calling the combined process operational end to end.
