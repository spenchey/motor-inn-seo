# Hosting and data notes

This is a local draft, not a deployment instruction authorized for execution. No cloud project, DNS record, domain purchase, paid API request or customer message was created.

## Local preview
Open `index.html` directly in a browser; it loads the neighboring `REVIEWS-DATA.js` using a normal script tag, so no build step or web server is needed. Both files must remain together. If desired, serve this folder locally with `python3 -m http.server 8765 --bind 127.0.0.1` and visit `http://127.0.0.1:8765/`. Do not bind a preview to a public interface.

## Update one config file
1. Edit `REVIEWS-DATA.js`. Leave unknown values `null`; never use `0` as a missing-value marker.
2. For each platform, confirm the Carroll entity and enter its exact `profileUrl` and review-flow `writeUrl`. Google: get the profile and “Get more reviews” link from the GBP owner. Cars.com: get the actual dealership page and review action from the platform account owner. No guessed dealer ID.
3. Enter `rating`, `count`, native `metric`, `scale`, ISO `checkedAt` date and `verified:true` only after observing the current public profile. `metric` is `stars` or `recommendation-percent`. Check dates must be real dates and not in the future. A verified count may coexist with a null/unavailable rating. Facebook percentages stay percentages. Review counts are displayed per source, not summed as unique customers.
4. Review excerpts are optional. Add only verified, permitted text with public author display name, original date, source URL and platform ID. Retain negative as well as positive feedback; no sentiment gate. Use `origin:'third-party'` for platform quotes. Nothing auto-fetches or auto-refreshes.
5. Refresh source data weekly. Check that source identity, scales, counts and publication permissions remain correct. Archive dated source evidence under this project; do not place raw customer records or API secrets here.
6. Keep `structuredReviews.enabled:false` for this third-party aggregator. Organization markup is always present. The requested AggregateRating and Review implementation is available only for a verified first-party review collection; its aggregate and quoted reviews must also be visible on the page. That still does not make dealer-controlled reviews eligible for Google review stars. Enabling it requires review of data provenance and the complete aggregate collection, not just selected excerpts. [Google's requirements](https://developers.google.com/search/docs/appearance/structured-data/review-snippet)
7. After purchase and deployment approval, set `siteUrl` to the purchased HTTPS URL and `preview:false`. Review source HTML before launch: explicitly remove `noindex, nofollow`, add a static self-canonical matching `siteUrl` for non-JavaScript crawlers, and remove the dynamic canonical insertion if using a static tag. Preview false alone intentionally does not remove indexing protection.
8. Reload at desktop and mobile sizes, verify every link and compare rendered data to JSON-LD. Missing/invalid data must remain visibly unverified; third-party ratings must not enter schema. Validate final JSON-LD after real data is supplied.

## Option A: Cloudflare Pages — simplest static hosting
Use the current free static tier if it covers this two-file site; verify plan limits before approving anything. No Functions or paid worker is needed. Create a Pages project with Direct Upload after approval and upload **only `index.html` and `REVIEWS-DATA.js`**. Do not upload these internal notes, runbooks, evidence, test fixtures or screenshots. Test the generated HTTPS preview before attaching the new domain. [Direct Upload documentation](https://developers.cloudflare.com/pages/get-started/direct-upload/)

For the apex `motorinnautogroupreviews.com`, Cloudflare Pages requires the domain as a Cloudflare zone and its authoritative nameservers at Cloudflare. The registrar can remain Network Solutions or GoDaddy. A subdomain can instead use an external DNS CNAME after association in the Pages dashboard. Do not assume an apex CNAME at the old provider works. Moving nameservers is a separately approved DNS change: copy and validate all existing records for the new domain first. Do not alter any of the three DealerOn domains or their AI subdomains. [Custom-domain requirements](https://developers.cloudflare.com/pages/configuration/custom-domains/)

## Option B: Private S3 + CloudFront
After approval, create a private S3 bucket with public access blocked; upload only the two deploy files. Use the S3 REST endpoint as the CloudFront origin with Origin Access Control and a bucket policy allowing only the distribution. Do not use the public S3 website endpoint for this private-origin design. Set default root object `index.html`, HTTPS redirect and correct MIME types (`text/html`, `application/javascript`). Attach an ACM certificate issued in `us-east-1` for the exact custom hostname(s). [AWS origins guidance](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/DownloadDistS3AndCustomOrigins.html)

At existing external DNS, a `www` hostname can CNAME to the distribution; the apex needs a provider-supported ALIAS/ANAME/flattening feature or an explicitly approved DNS-provider move. Do not invent a fixed CloudFront IP. Keep the canonical hostname consistent and implement the alternate-host redirect only after confirming provider support. Prefer Cloudflare Pages if this complexity is unnecessary. Estimate S3/CloudFront request, transfer and storage costs in the actual account; no fixed monthly cost is asserted. Do not create chargeable resources without approval.

## DNS ownership and live observations
Prior work/user context places DNS administration with **Network Solutions / GoDaddy**. Read-only NS lookups on 2026-09-16 returned:

| Existing domain | Observed nameservers | Provider indication |
|---|---|---|
| motorinnautogroup.com | ns99.worldnic.com, ns100.worldnic.com | Network Solutions-style DNS |
| motorinntoyotaofcarroll.com | ns71.domaincontrol.com, ns72.domaincontrol.com | GoDaddy-style DNS |
| motorinnofcarroll.com | ns17.domaincontrol.com, ns18.domaincontrol.com | GoDaddy-style DNS |

Nameservers indicate DNS service, not verified account ownership or registrar access. Confirm the actual registrar/DNS account and authorized owner before any future change. The recommended new domain is not purchased and has no selected DNS owner yet. Existing DealerOn sites and AI markdown proxies are outside this deployment.

## Release verification and rollback
- Verify purchase ownership, domain spelling, HTTPS, canonical hostname and exact hosting directory.
- Verify five profile links and review flows, all values/dates, franchise identity and reproduction permission.
- Check 320/390/768/1440px widths, keyboard focus, readable contrast and zero automatic third-party network requests.
- Preserve the prior deploy bundle and record release hash/time. Use short cache lifetimes for config and revalidation for HTML; avoid a long-lived data file with stale ratings.
- After an authorized release, check live HTML, config, schema and outgoing links; save proof under this project. Only then mark deployment complete.
- Roll back to the prior static bundle if data or links are wrong. No rollback requires touching DealerOn or AI-proxy infrastructure.
