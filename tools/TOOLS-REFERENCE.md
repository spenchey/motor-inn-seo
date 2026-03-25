# SEO Tools Reference — For Rory

All tools live in `~/motor-inn-seo/tools/`. Python venv at `~/motor-inn-seo/.venv/`.

**Activate venv before running any script:**
```bash
source ~/motor-inn-seo/.venv/bin/activate
```

---

## 1. SEO Machine (tools/seomachine/)

### Research Scripts (run from tools/seomachine/)

| Script | What it does |
|--------|-------------|
| `research_competitor_gaps.py` | Compare our keyword coverage vs competitors, find gaps |
| `research_serp_analysis.py` | Analyze SERP results for target keywords |
| `research_quick_wins.py` | Find keywords where small improvements = big gains |
| `research_performance_matrix.py` | Data-driven priority matrix from GA4/GSC |
| `research_priorities_comprehensive.py` | Full priority analysis combining all data |
| `research_topic_clusters.py` | Group keywords into topic clusters |
| `research_trending.py` | Find trending topics in our market |
| `seo_baseline_analysis.py` | Current rankings for our target keywords |
| `seo_bofu_rankings.py` | Bottom-of-funnel keyword rankings |
| `seo_competitor_analysis.py` | Deep competitor SEO analysis |

### Data Source Modules (tools/seomachine/data_sources/modules/)

| Module | Purpose |
|--------|---------|
| `google_analytics.py` | Pull GA4 traffic/engagement data |
| `google_search_console.py` | Pull GSC ranking/impression/click data |
| `dataforseo.py` | Pull competitive keyword data from DataForSEO API |
| `data_aggregator.py` | Combine data from all sources |
| `keyword_analyzer.py` | Keyword density, clustering, LSI analysis |
| `search_intent_analyzer.py` | Classify search intent (informational/transactional/etc) |
| `content_length_comparator.py` | Compare our content length vs SERP competitors |
| `readability_scorer.py` | Flesch readability scores |
| `seo_quality_rater.py` | Comprehensive 0-100 SEO quality score |
| `opportunity_scorer.py` | Score and prioritize content opportunities |
| `content_scorer.py` | 5-dimension content quality scoring |
| `competitor_gap_analyzer.py` | Detailed competitor gap analysis |
| `above_fold_analyzer.py` | Above-the-fold content analysis |
| `cta_analyzer.py` | CTA effectiveness analysis |
| `trust_signal_analyzer.py` | Trust signal detection and scoring |

### Configuration

- `tools/seomachine/config/competitors.json` — Competitor list (update with our competitors)
- `tools/seomachine/context/` — Brand voice, style guide, target keywords, etc.
- `.env` at `~/motor-inn-seo/config/.env` — API credentials

---

## 2. Claude SEO (tools/claude-seo/)

### Scripts (tools/claude-seo/scripts/)

| Script | What it does |
|--------|-------------|
| `fetch_page.py <url>` | Download HTML with proper headers, SSRF protection |
| `parse_html.py <file> --url <url>` | Extract SEO metadata (titles, headings, images, links, schema, word count) → JSON |
| `capture_screenshot.py <url>` | Screenshot via Playwright (desktop/mobile/tablet) |
| `analyze_visual.py` | Visual analysis of page layout |

### Schema Templates

`tools/claude-seo/schema/templates.json` — 9 JSON-LD schema templates:
- LocalBusiness, AutoDealer, Vehicle, FAQPage, etc.
- Use these when recommending schema markup for new pages

### Audit Logic Reference

The skill definitions in `tools/claude-seo/skills/` contain evaluation criteria:
- `seo-audit/SKILL.md` — Full site audit checklist
- `seo-technical/SKILL.md` — Technical SEO (9 categories)
- `seo-content/SKILL.md` — E-E-A-T content quality
- `seo-schema/SKILL.md` — Schema validation
- `seo-local/SKILL.md` — Local SEO (GBP, citations, reviews)
- `seo-programmatic/SKILL.md` — Programmatic SEO page generation

These are reference docs — read them for the evaluation methodology, then apply it.

---

## Typical Workflow

### Weekly Audit
```bash
source ~/motor-inn-seo/.venv/bin/activate
cd ~/motor-inn-seo/tools

# Fetch and parse the site
python claude-seo/scripts/fetch_page.py https://www.motorinncarroll.com --output /tmp/motorinn.html
python claude-seo/scripts/parse_html.py /tmp/motorinn.html --url https://www.motorinncarroll.com --json

# Check SEO quality
cd seomachine
python seo_baseline_analysis.py
```

### Monthly Gap Analysis
```bash
source ~/motor-inn-seo/.venv/bin/activate
cd ~/motor-inn-seo/tools/seomachine

# Pull data and find gaps
python research_competitor_gaps.py
python research_quick_wins.py
python research_topic_clusters.py
python research_performance_matrix.py
```

### Content Generation
After identifying gaps, use the context templates in `tools/seomachine/context/` and the evaluation criteria in `tools/claude-seo/skills/` to generate draft pages that meet SEO best practices. Save drafts to `~/motor-inn-seo/content/drafts/`.
