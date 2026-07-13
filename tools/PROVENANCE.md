# tools/ provenance (MOT-2431)

Vendored third-party SEO/GEO tooling. All copies are snapshots (no nested
`.git`); re-vendor by cloning the upstream at a newer commit and replacing the
directory, then re-run the security sweep below.

| Directory | Upstream | Pinned commit | Vendored | License |
|---|---|---|---|---|
| `claude-seo/` | https://github.com/AgriciDaniel/claude-seo | `6cf1ea9` (2026-07-06) | 2026-07-13 (replaced 2026-03-25 snapshot) | MIT |
| `geo-seo-claude/` | https://github.com/zubair-trabzada/geo-seo-claude | `9eec32f` (2026-05-26) | 2026-07-13 | MIT |
| `seomachine/` | https://github.com/TheCraigHewitt/seomachine | vendored 2026-03-25 (configured: `config/competitors.json`, `context/` — do NOT clobber on re-vendor) | 2026-03-25 | see dir |
| `skills-sh/marketingskills-seo-audit/` | https://github.com/coreyhaines31/marketingskills (`skills/seo-audit/` only) | `0ba2a7f` (2026-07-12) | 2026-07-13 | MIT |
| `skills-sh/opc-seo-geo/` | https://github.com/ReScienceLab/opc-skills (`skills/seo-geo/` only) | `8e38aae` (2026-07-13) | 2026-07-13 | MIT |

## Python environments

- `~/motor-inn-seo/.venv/` — seomachine research scripts (pre-existing).
- `tools/.venv-toolkit/` — dedicated venv for the analyzer battery
  (`scripts/run-seo-toolkit.sh`). Rebuild:
  `/opt/homebrew/bin/python3.13 -m venv tools/.venv-toolkit &&
  tools/.venv-toolkit/bin/pip install -r tools/geo-seo-claude/requirements.txt`
  (that requirement set also covers every claude-seo script the toolkit calls).
  Gitignored.

## Security sweep (2026-07-13, on-Mini re-verification)

Swept all four fresh clones for outbound hosts and credential reads before
wiring. The nine analyzers actually wired (`geo-seo-claude/scripts/fetch_page,
llmstxt_generator, citability_scorer, brand_scanner`; `claude-seo/scripts/
fetch_page, parse_html, drift_baseline, drift_compare, content_quality`):

- No reads of `~/.claude`, `~/.ssh`, `~/.aws`, `~/.zshrc`, env API keys.
- `subprocess` only in `drift_baseline.py` — invokes its own sibling scripts.
- Outbound hosts: the audited target, plus (brand scanner only) public
  platform searches: youtube/reddit/wikipedia/wikidata/linkedin/bing/quora/
  trustpilot/g2/producthunt/crunchbase/stackoverflow. No telemetry endpoints.
- NOT installed/executed: repo `install.sh` scripts (they register skills into
  `~/.claude/` — we deliberately use the analyzers directly from this vendored
  tree), `claude-seo/extensions/` (ahrefs/dataforseo/firecrawl API bridges),
  opc-skills dirs other than `seo-geo` (its `logo-creator` greps `~/.zshrc`
  for API keys — excluded), marketingskills dirs other than `seo-audit`,
  `geo-seo-claude/scripts/webapp/` (flask UI) and `crm_dashboard.py`.
- Drift state lives at `~/.cache/claude-seo/drift/baselines.db` (sqlite,
  machine-local).

## Runtime wiring (who calls what)

- `scripts/run-seo-toolkit.sh` — deterministic battery, NO LLM.
  Weekly (light): technical, crawlers, llms.txt, onpage, drift.
  Monthly (full): + citability, content-quality, sitemap, brand.
  Called by `~/clawd/scripts/no-model/weekly-seo-audit.sh` (Mon 11:20) and
  `~/clawd/scripts/no-model/monthly-seo-executive-report.sh` (1st 11:45).
- `scripts/seo-toolkit-findings.py` — deterministic findings templating
  (the default synthesis path; cron paths stay LLM-free).
- `scripts/rory-seo-inspect.sh` — OPTIONAL inspector pass via the `rory-seo`
  hermes profile (local qwen3.6 only, fail-loud). Not in the cron path.
