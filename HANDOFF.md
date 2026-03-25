# Content Handoff Instructions

## For DealerOn / SEO Company

This document explains how to take approved SEO content from this repo and publish it on the Motor Inn Auto Group website.

## Where to Find Content

Approved content ready for publishing lives in: `content/approved/`

Each file is a markdown document with YAML frontmatter containing all the SEO metadata you need.

## What's in Each File

| Field | Description |
|-------|-------------|
| `target_keyword` | Primary keyword this page targets |
| `secondary_keywords` | Supporting keywords to include naturally |
| `search_intent` | informational, transactional, navigational, or commercial |
| `page_type` | landing_page, blog_post, service_page, etc. |
| `priority` | high, medium, low |

### In the SEO Notes section at the bottom:
- **Recommended URL slug** - suggested URL path
- **Meta title** - for the `<title>` tag
- **Meta description** - for the meta description tag
- **Schema type** - structured data to add (e.g., AutoDealer, Vehicle, FAQPage)
- **Internal links** - pages that should link to/from this new page

## Publishing Checklist

For each page:

- [ ] Create the page in DealerOn CMS
- [ ] Set the URL slug as recommended
- [ ] Add the meta title and description
- [ ] Format the content with proper H1/H2/H3 headings
- [ ] Add any recommended images (with alt text using target keyword)
- [ ] Implement schema markup
- [ ] Add internal links as specified
- [ ] Preview on mobile
- [ ] Publish
- [ ] Move the source file from `content/approved/` to `content/published/` and commit
- [ ] Note the live URL in the file's frontmatter as `live_url:`

## DealerOn-Specific Notes

- DealerOn uses a custom CMS - pages are typically added under the "Custom Pages" or "Landing Pages" section
- Check with your DealerOn rep if you need additional page slots or URL routing
- Schema markup may need to be added via DealerOn's custom HTML/script injection feature
- DealerOn sites have built-in schema for dealer info - make sure new pages don't conflict

## Frequency

Rory generates new content on a regular basis. Check `content/approved/` weekly for new pages, or watch this repo for commits.

## Questions?

Reach out to Spencer or check Slack `#automated-marketing` for context on any content piece.
