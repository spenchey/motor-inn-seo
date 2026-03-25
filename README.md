# Motor Inn SEO Monitor/Builder

SEO keyword gap analysis, content generation, and site health monitoring for **Motor Inn Auto Group** (Carroll, IA).

## Overview

This repo is the central hub for Motor Inn's SEO pipeline:

1. **Monitor** - Continuous SEO health checks on the DealerOn-hosted website
2. **Research** - Keyword gap analysis using GA4 + Google Search Console + competitive data
3. **Build** - Generate SEO-optimized page content for human review before handoff to DealerOn/SEO company

Owned by **Rory** (marketing agent) in the OpenClaw agent org.

## Directory Structure

```
motor-inn-seo/
├── research/          # Keyword gap reports, competitor analysis, search data exports
├── content/
│   ├── drafts/        # Rory-generated page content awaiting review
│   ├── approved/      # Human-reviewed and approved, ready for handoff
│   └── published/     # Archive of content that's live on the site
├── audits/            # SEO health audit reports (technical, on-page, schema)
├── config/            # GA4/GSC credentials config, DataForSEO keys, site settings
├── scripts/           # Automation scripts for data pulls, report generation
└── HANDOFF.md         # Instructions for DealerOn/SEO company to publish content
```

## Workflow

### Gap Analysis (scheduled)
1. Pull current ranking data from Google Search Console
2. Pull traffic/engagement data from GA4
3. Run competitive keyword analysis for Carroll, IA market
4. Identify gaps: keywords competitors rank for that we don't cover
5. Identify striking distance: keywords at positions 5-20 where new/improved content helps
6. Output gap report to `research/`

### Content Generation
1. Rory picks highest-priority gaps from research
2. Generates draft pages with: title, meta description, H1/H2 structure, body content, internal link suggestions, schema markup recommendations
3. Drafts land in `content/drafts/` as markdown files with YAML frontmatter
4. Human reviews and moves approved content to `content/approved/`
5. DealerOn/SEO company picks up from `content/approved/` using HANDOFF.md instructions

### SEO Monitoring (scheduled)
1. Crawl site for technical issues (broken links, missing meta, duplicate content)
2. Validate schema markup
3. Check mobile usability
4. Flag keyword cannibalization
5. Audit reports saved to `audits/`
6. Critical issues posted to Slack `#automated-marketing`

## Content File Format

Each draft page in `content/drafts/` follows this format:

```markdown
---
target_keyword: "used trucks Carroll IA"
secondary_keywords: ["pre-owned trucks Carroll Iowa", "used pickup trucks near me"]
search_intent: transactional
page_type: landing_page
priority: high
status: draft
created: 2026-03-25
author: rory
---

# Page Title (H1)

Page content here...

## SEO Notes
- Recommended URL slug: /used-trucks-carroll-ia
- Meta title: ...
- Meta description: ...
- Schema type: AutoDealer + Vehicle listing
- Internal links: [list of pages to link to/from]
```

## Handoff to DealerOn / SEO Company

See [HANDOFF.md](HANDOFF.md) for detailed instructions on how to take approved content and get it published on the DealerOn platform.

## Setup

### Prerequisites
- Google Search Console access for Motor Inn's domain
- GA4 property access
- DataForSEO API key (optional, for competitive data)

### Configuration
1. Copy `config/example.env` to `config/.env`
2. Add your API keys and property IDs
3. See `config/README.md` for details

## Tech Stack / Tools
- [seomachine](https://github.com/TheCraigHewitt/seomachine) - SEO content research & writing
- [claude-seo](https://github.com/AgriciDaniel/claude-seo) - SEO auditing & monitoring
- Google Search Console API
- GA4 Data API
- DataForSEO API (competitive keyword data)
