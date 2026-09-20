**Toyota indexing sprint — September 20, 2026**

**11 of 14 indexing requests accepted; three remain after Google exhausted the daily quota.** The XML sitemap was successfully resubmitted. These are confirmed crawl-queue submissions, not confirmation that Google has indexed the pages.

Property: https://www.motorinntoyotaofcarroll.com/  
Work performed from the MacBook; read-only GSC API inspection ran on the verified Mac Mini through its configured `codex-mac-mini` SSH alias. The supplied `nada-mini` alias did not resolve here. The service-account key remained on the Mini. One Chrome session was signed out; the other was already signed in with access to the correct property. No password was entered.

**Per-URL results**

Every URL below returned HTTP 200 with `index,follow,noydir,noodp`, no X-Robots-Tag, and a self-referencing canonical, using both desktop-browser and Googlebot smartphone user agents. None of the target paths is disallowed in robots.txt. All 14 are present in the XML sitemap with September 20 lastmod values. The API returned HTTP 200 for all 14 inspections; each still reported **Excluded by noindex** from the historical crawl shown below (UTC).

| URL path | Live HTTP / robots | Google's last crawl (UTC) | GSC UI outcome |
|---|---|---|---|
| [toyota-corolla](https://www.motorinntoyotaofcarroll.com/toyota-corolla) | 200 / index,follow | 2026-09-14 13:44:01 | Requested |
| [toyota-highlander](https://www.motorinntoyotaofcarroll.com/toyota-highlander) | 200 / index,follow | 2026-04-28 18:44:32 | Requested |
| [toyota-tacoma](https://www.motorinntoyotaofcarroll.com/toyota-tacoma) | 200 / index,follow | 2026-04-10 23:03:51 | Requested |
| [toyota-4runner](https://www.motorinntoyotaofcarroll.com/toyota-4runner) | 200 / index,follow | 2026-04-11 04:59:52 | Requested |
| [toyota-sienna](https://www.motorinntoyotaofcarroll.com/toyota-sienna) | 200 / index,follow | 2026-04-30 01:15:38 | Requested |
| [toyota-gr86](https://www.motorinntoyotaofcarroll.com/toyota-gr86) | 200 / index,follow | 2026-09-14 13:10:40 | Requested |
| [toyota-crown-signia](https://www.motorinntoyotaofcarroll.com/toyota-crown-signia) | 200 / index,follow | 2026-05-19 17:20:33 | Requested |
| [2025-toyota-crown-signia](https://www.motorinntoyotaofcarroll.com/2025-toyota-crown-signia) | 200 / index,follow | 2026-04-11 00:44:43 | Requested |
| [toyota-rav4-plug-in-hybrid](https://www.motorinntoyotaofcarroll.com/toyota-rav4-plug-in-hybrid) | 200 / index,follow | 2026-04-11 05:23:20 | Requested |
| [2027-toyota-land-cruiser](https://www.motorinntoyotaofcarroll.com/2027-toyota-land-cruiser) | 200 / index,follow | 2026-04-28 15:44:31 | Requested |
| [toyota-college-rebate-kansas-city](https://www.motorinntoyotaofcarroll.com/toyota-college-rebate-kansas-city) | 200 / index,follow | 2026-04-11 06:33:50 | Requested |
| [toyota-military-rebate-kansas-city](https://www.motorinntoyotaofcarroll.com/toyota-military-rebate-kansas-city) | 200 / index,follow | 2026-06-18 10:03:56 | Rejected: daily quota |
| [testdrive.aspx](https://www.motorinntoyotaofcarroll.com/testdrive.aspx) | 200 / index,follow | 2026-06-15 14:39:39 | Pending: quota exhausted |
| [findmycar.aspx](https://www.motorinntoyotaofcarroll.com/findmycar.aspx) | 200 / index,follow | 2026-04-28 14:59:33 | Pending: quota exhausted |

**Why the homepage appeared to have no model links**

- The main navigation already contains a normal HTML link to `/model-research.html` (“Model Line-Up”). That page has raw HTML links to nine target model pages: Corolla, Highlander, Tacoma, 4Runner, Sienna, GR86, Crown Signia, RAV4 Plug-in Hybrid, and 2027 Land Cruiser. They are reachable in two links from the homepage without JavaScript.
- The homepage also links to `/sitemap.aspx`, whose raw HTML includes all 14 target URLs. Test Drive is directly linked from the homepage navigation. The target pages are therefore not XML-sitemap-only orphans.
- Chrome rendering adds a relative `toyota-crown-signia` href. The inline carousel script explains why: zero-inventory model cards switch their anchor href to the research URL stored in `data-url`; other cards retain inventory-search links. This is a mixture of JavaScript link rewriting and links to inventory URLs, not an entirely JavaScript-only navigation.
- Browser-UA and Googlebot-UA homepage crawls returned 200 and the same relevant raw navigation links. This was UA emulation from a normal client IP, not a verified Googlebot visit or Google's renderer. Google does execute JavaScript and extract rendered links, subject to resource access and rendering limitations, per [Google's JavaScript documentation](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics).

**Actions and remaining work**

Used computer control for every Request Indexing action. Eleven produced the “Indexing requested” confirmation and priority-crawl-queue notice. The military-rebate request returned **Quota Exceeded** with an instruction to try tomorrow. Test Drive and Find My Car were not submitted after that limit appeared. The military-rebate GSC tab is retained for follow-up.

Resubmitted `sitemap.xml` at approximately 3:40 p.m. America/Chicago; GSC confirmed successful submission. Before resubmission, it showed Success, last read September 19, and 215 discovered pages. The current fetched XML contained 214 URLs (126 non-vehicle/non-offer URLs, 82 vehicle URLs, six offers). Other historical sitemap submissions showed errors; those were left unchanged.

On **September 21, after quota availability returns**, request the military rebate, test-drive, and vehicle-finder URLs. Then check for new crawl dates, removal of the noindex exclusion, and Google's chosen canonical. No follow-up job was scheduled. Google controls recrawl timing and indexing; [Google's recrawl guidance](https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl) does not guarantee inclusion. The [URL Inspection API](https://developers.google.com/webmaster-tools/v1/urlInspection.index/inspect) supplies indexed-version status and cannot submit these indexing requests.

DealerOn remained read-only. No public social/GBP posts, purchases, or external messages were made. Optional DealerOn follow-up: strengthen direct contextual links, and review the observed carousel mapping of “Toyota Crown” to Crown Signia and the malformed Prius Plug-in Hybrid href `/2027-Toyota-/toyota-prius-plug-in-hybrid`; neither was changed or separately tested here.

Evidence: [live URL checks](indexing-evidence-2026-09-20/live-urls.json), [GSC API snapshot](indexing-evidence-2026-09-20/gsc-api-inspection.json), [request ledger](indexing-evidence-2026-09-20/gsc-request-ledger.json), [discovery summary](indexing-evidence-2026-09-20/discovery-summary.json), and [carousel link rule](indexing-evidence-2026-09-20/homepage-carousel-link-rule.js). Raw homepage, sitemap, robots.txt, and discovery-page HTML are retained in the same evidence folder.

**Chevrolet GSC verification handoff — September 20, 2026**

Used computer control in Chrome, signed in as `spencer.heywood@motorinnmail.com`. The property selector already listed `https://www.motorinnofcarroll.com/` under **Not verified**, so the existing property was opened. Expanded **HTML tag** and clicked **COPY**; GSC confirmed “Copied to clipboard.” The exact tag is saved in [chevy-gsc-verification-tag.txt](chevy-gsc-verification-tag.txt). No password was entered; no DNS or HTML-file verification method was used.

DealerOn case **01919856**, contact Melanie Stila, recipient `help@dealeron.com`, Gmail thread `1a0b525811343bf6`. The local `/opt/homebrew/bin/gog` exists, but the read-only thread lookup returned `No auth for gmail spencer.heywood@motorinnmail.com.` Saved the authorized fallback [email draft](chevy-gsc-verification-email-draft.md), containing the exact tag and the request to install it in the site `<head>` alongside the existing verification tags, preserve those tags, and confirm when live. **No email was sent.**

**Ownership remains unverified.** DealerOn must install the tag and confirm; then return to the HTML tag verification method in GSC and click Verify. The tag capture and draft are complete; installation and successful ownership verification are not claimed.
