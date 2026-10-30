Three implementation tasks from the James Brooks AI-SEO thread gap analysis. Work in
/Users/spencerheywood/motor-inn-seo. Commit each as its own commit. NO emails, NO deploys to
production, NO DealerOn contacts - local build + evidence only. Spencer approves deploys.

TASK 1 - JSON content feed (gap: feed.json 404)
Our ai.* proxies (EC2 67.202.51.138, Caddy, repo spenchey/ai-markdown-proxy) serve markdown
+ llms.txt per site. Add a /feed.json endpoint to the proxy: JSON array of
{site, url, title, updated, summary} for each page the proxy knows (parse from existing
llms.txt/link data). Add link in each llms.txt: '# machine-readable: /feed.json'. Write the
code + tests in the repo on a branch feed-json, DO NOT deploy - print deploy instructions.
Also write the exact endpoint spec to brain/FEED-API.md.

TASK 2 - dated answer block copy (for DealerOn cases)
Draft the exact one-line HTML snippet for a 'Last updated <Month YYYY> - verified by Motor Inn
Auto Group' stamp, styled to match the ready-design pages (content/ready-design/*.hat are the
final designs - reuse their CSS vars). Save snippet + usage note to
content/ready-datestamp.html and document in the file header where it goes (top of body,
under H1). This goes into the NEXT DealerOn correspondence as an amendment - draft the
amendment text too at pipeline/drafts/datestamp-amendment-draft.md (do not send).

TASK 3 - GA4 AI-referrals segment spec + report hook
Write brain/ai-referrals.md documenting: (a) GA4 exploration segment definition regex
source matching (chatgpt|openai|perplexity|copilot|gemini|perplexity\.ai|edgeservices) on
sessionSource/referrer, (b) the exact GA4 Data API runReport call (property 364125348, using
sa-readonly creds pattern from motorinn-ga4/ga4_common.py on this machine) to pull
sessions by sessionSource filtered to those hosts, last 28d, and (c) a python snippet
brain/ai_referrals.py that prints the count per source - TEST IT LIVE against the API now
(read-only; the service account has access). Wire: append an '## AI referrals' section
generator call into agents/weekly-report.md instructions (edit the runbook to add step).

When done: git commit each separately, print summary of files changed + test outputs.