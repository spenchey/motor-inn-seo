Hi DealerOn team,

One change request for www.motorinnautogroup.com (Motor Inn Auto Group):

ISSUE
The robots.txt file currently blocks AI crawlers GPTBot and ClaudeBot site-wide:

  User-Agent: ClaudeBot
  Disallow: *

  User-Agent: GPTBot
  Disallow: *

Live evidence (2026-09-21): https://www.motorinnautogroup.com/robots.txt

REQUESTED CHANGE
For both the GPTBot and ClaudeBot stanzas, replace `Disallow: *` with `Allow: /` (or simply remove the Disallow line), so the whole site is crawlable. Keep the existing specific disallow rules under `User-Agent: *` unchanged — those are fine and we want them retained.

Note: the other AI bot stanzas (ChatGPT-User, Claude-SearchBot, OAI-SearchBot, PerplexityBot) already correctly use `Allow: *` — we'd like GPTBot and ClaudeBot to match that behavior.

WHY
We want our inventory VDPs visible to OpenAI and Anthropic crawlers for AI search surfaces (GEO). Blocking them site-wide removes the dealership from those answers.

VERIFY STEP (we will run)
  curl -s https://www.motorinnautogroup.com/robots.txt
and confirm the GPTBot and ClaudeBot stanzas no longer contain `Disallow: *`.

Please confirm once deployed. This is one change in isolation — separate emails will cover our other open requests so nothing gets bundled.

Thanks!
Spencer Heywood
Motor Inn Auto Group
Carroll, IA
