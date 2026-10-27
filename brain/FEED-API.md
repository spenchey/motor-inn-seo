# `/feed.json` endpoint spec (local-only)

## Purpose
Machine-readable JSON array of every page the AI-readable mirror exposes for a site, sourced
from the same validated `llms.txt` package already served on each `ai.*` host. One endpoint
per hostname; site identity is never mixed.

## Endpoint
```
GET https://ai.<brand>.com/feed.json
```
- Scope: `ai.motorinnautogroup.com`, `ai.motorinntoyotaofcarroll.com`, `ai.motorinnofcarroll.com`
- Site selection: request `Host` header (same as existing proxy); `?site=` override available for direct-to-app testing only
- Cache: `Cache-Control: public, max-age=3600` (same class as OpenAPI)
- Errors: `503 source_unavailable` if the validated package fails; `500 internal_error` otherwise
- Also added to `DISCOVERY_PATHS`, so the root discovery index and sitemap list it

## Response shape
JSON array; each element has exactly:
| Field | Type | Meaning |
|---|---|---|
| `site` | string | Canonical `site.key` (`motorinnautogroup`, `motorinnchevy`, `motorinntoyota`) |
| `url` | string | Absolute URL as published in that site's `llms.txt` |
| `title` | string | Link title from `llms.txt` |
| `updated` | string | ISO 8601 UTC timestamp (page file mtime, else manifest `generatedAt`) |
| `summary` | string | One-line llms.txt description, or first markdown heading when no description exists |

## Source
The endpoint parses markdown links from the site's static `llms.txt` with the pattern
`- [Title](url): summary`. It does not add new inventory rows and does not expose any
source that is not already published in `llms.txt`.

## llms.txt marker
Each `llms.txt` gains the footer:
```
# machine-readable: /feed.json
```
This is discoverable by agents reading the existing `llms.txt` on each host.

## Deployment (not performed)
Local implementation is on branch `feed-json` in repo `spenchey/ai-markdown-proxy`. On EC2:
```
cd /srv/ai-markdown-proxy
git pull origin feed-json
./deploy.sh
systemctl restart ai-markdown-proxy
```
Then smoke-test each `ai.<brand>.com/feed.json` for a 200 and valid JSON array.
