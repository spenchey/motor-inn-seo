# Motor Inn SEO pack and reviews-site build report

Date: 2026-09-16, America/Chicago.
Status: **Local deliverables complete; operational SEO runs and launch remain blocked by the inputs below.**

All deliverables are under `/Users/spencerheywood/motor-inn-seo/`. No publishing, email, messages, domain purchase, paid API call, DNS mutation or AI-proxy change was performed. No agent scheduler was installed. Existing modified/untracked files in the repository were preserved.

## Files created
Paths are relative to `/Users/spencerheywood/motor-inn-seo/`.

| File | One-line description |
|---|---|
| `agents/README.md` | Scope, three-host ownership, weekly 2/3/5 -> review -> 7 flow, monthly crawl and output contract. |
| `agents/keyword-research.md` | Six exact seeds, local intent research, privacy-safe CRM extraction and specific missing-source retrieval instructions. |
| `agents/gsc-audit.md` | Per-property page/query audit, finalized windows, API canaries and explicit BLOCKED-IF-NO-CREDS procedure. |
| `agents/ai-mentions.md` | Twenty stable seed questions, 60 weekly observations, citation evidence and DataForSEO CREDS-NEEDED section. |
| `agents/citation-gaps.md` | AI-cited source inventory and evidence-based weak/missing profile classifications. |
| `agents/opportunity-scoring.md` | Reproducible traffic-potential × ease score, null-data fallback and distinct 50501 expansion view. |
| `agents/topical-map.md` | Model, used body-style, trade-in, financing, service/tires and sell-to-us ownership map. |
| `agents/content-brief.md` | DealerOn brief template with the exact staging package ID and a missing-package verification gate. |
| `agents/internal-links.md` | Used-SUV/truck reciprocal rules, model-to-inventory and service-to-hours/contact link checks. |
| `agents/cannibalization.md` | GSC-dependent query/page overlap procedure, including used-inventory versus searchused.aspx. |
| `agents/local-citations.md` | Chamber, newspaper, sponsor and Iowa association citation work; link exchanges excluded. |
| `agents/RUN-REPORT.md` | This inventory, verification evidence, discrepancies and complete blocker register. |
| `reviews-site/RECOMMENDATION.md` | Primary/alternate domain recommendation, WHOIS/RDAP/DNS observations and honest SEO limits. |
| `reviews-site/index.html` | Mobile-friendly static review directory with inline CSS, metadata, Organization schema and guarded rating/review schema support. |
| `reviews-site/REVIEWS-DATA.js` | Single editable config for five platforms, null numeric placeholders, URLs, dates and optional permitted review excerpts. |
| `reviews-site/DEPLOY-NOTES.md` | Local preview, data maintenance, Cloudflare Pages or S3/CloudFront hosting and Network Solutions/GoDaddy DNS notes. |
| `reviews-site/PRODUCT.md` | Scoped design context and explicitly inferred design choices for the review page. |
| `reviews-site/qa/check.py` | Repeatable local Chromium verification with synthetic data restricted to browser memory. |
| `reviews-site/qa/results.json` | Machine-readable results: 30 checks passed, no JavaScript errors and no external requests. |
| `reviews-site/qa/preview-390.png` | Visually inspected mobile preview at 390px. |
| `reviews-site/qa/preview-1440.png` | Visually inspected desktop preview at 1440px. |

Total: **21 retained files**. Temporary build helper and isolated QA browser profiles were removed. Only index.html and REVIEWS-DATA.js belong in a future approved hosting bundle.

## Verification performed
- All 10 job runbooks plus README contain purpose, inputs, exact steps, output paths and verification checklists.
- Browser checks passed at 320, 390, 768 and 1440px without horizontal overflow; mobile and desktop screenshots inspected.
- Verified title, five source rows, keyboard skip link, no-JavaScript fallback and preview noindex protection.
- Six text/background combinations measured at >=4.5:1 contrast in browser-converted colors; precise results are in qa/results.json.
- Verified null placeholder behavior, disabled unknown review destinations, valid data display, rejection of out-of-range ratings, escaped review text and no third-party review-schema leakage.
- Verified optional first-party AggregateRating and Review generation against temporary in-memory fixtures and corresponding visible content. Fixtures were not written into REVIEWS-DATA.js. No real reviews or ratings were populated.
- Loaded Organization JSON-LD is valid JSON. No claim of live Google rich-result eligibility or a live Rich Results Test; preview remains noindex and unpublished.
- Initial page and config total approximately 20 KB uncompressed; zero external asset/network requests observed. Outbound links navigate only after a user clicks them.
- Read-only WHOIS found no match for all three proposed domains; Verisign RDAP returned 404; DNS returned NXDOMAIN. Availability remains provisional until registrar checkout.
- Read-only DNS showed group `ns99/ns100.worldnic.com`, Toyota `ns71/ns72.domaincontrol.com`, Chevrolet `ns17/ns18.domaincontrol.com`. These match the stated Network Solutions/GoDaddy DNS setup, but do not prove account ownership.
- No current GSC audit, AI-mention survey, keyword-volume pull, DealerOn staging review or monthly crawl was claimed as executed.

Re-run local QA: `/Users/spencerheywood/motor-inn-seo/.venv/bin/python /Users/spencerheywood/motor-inn-seo/reviews-site/qa/check.py`. Uses the existing installed Playwright/Chromium; no dependency was installed.

## Context discrepancies and open blockers

| Blocker | Evidence and required next action | Owner / impact |
|---|---|---|
| GSC credentials / grants | Task states unavailable. Complete service-account re-invite acceptance/grant verification in each GSC property's UI, then prove sites.get and searchanalytics.query read access. A service account has no ordinary inbox; owner assignment and successful reads are the completion test. | GSC property owner; jobs 2 and 9 blocked, numeric job 5 may be blocked. |
| Historical GSC contradiction | Requested audit was read; it is May 25, 2026 and says `GSC skipped: no` and connected, not skipped. Historical memory also records a Toyota grant. Neither proves access today; current task's unavailable state governs. | Report consumer; do not use old figures as current evidence. |
| DataForSEO credentials | Account signup on 2026-08-17 is user-supplied context. API login/password are unavailable per task; enabled endpoints, balance and explicit paid-call authorization also needed. No credentials were searched or printed. | Account owner; API-based AI/keyword research blocked. |
| Missing llms.txt | `/Users/spencerheywood/.hermes/profiles/jeeves/workspace/llms.txt` does not exist here; the profile has no workspace directory. No substitute llms draft was found in this SEO repository. | Jeeves workspace owner; provide correct read path or draft. No proxy changes required. |
| DealerSocket/service questions | No readable notes/advisor exports found in bounded local search. The read-only local lead-response DB has 0 leads and 0 followups. Job 1 names CRM work notes/inbound inquiry exports and advisor/RO concern logs to obtain. | CRM administrator + service manager; real buyer-language extraction pending. |
| Historical CRM archive pointer | Memory provides a July 31 S3/Glyph archive location; current access and contents were not verified. No archive mounted or ingestion started. | Data owner; supply de-identified local extract if appropriate. |
| Saved 20-question list | No saved question file found. Job 3 supplies a labeled generated seed-v1 list; it is not presented as actual customer wording or past measured results. | SEO owner; reconcile with historical saved set and real notes. |
| DealerOn staged package | Exact ID preserved: `MOTORINN-SEO-STAGING-4a2aaec73b56bb4638eef49a5d6a9b4d`. No matching source package found in repository content, audits or research. | Staging owner; exact export/manifest/preview needed for implementation-ready used-inventory brief. |
| Domain purchase approval | motorinnautogroupreviews.com is recommended and appears unregistered. No checkout price or registrar reservation status verified; do not purchase until Spencer explicitly approves. | Spencer; purchase and registrar choice pending. |
| Exact Google/Cars.com links | Google has a labeled Maps lookup, not a confirmed GBP/review composer URL. Cars.com has a labeled dealer-directory lookup; exact Motor Inn Carroll profile not found. Their leave-review buttons are disabled. | Profile/account owner; exact profile and review URLs required before launch. |
| Profile submission checks | Facebook, DealerRater and CarGurus URLs are sourced; CTAs open profiles rather than submitting anything. DealerRater direct retrieval failed; platform sign-in/eligibility and all review flows require final browser verification. | Profile owner; verify every link before publishing. |
| Real review data / permissions | All counts/ratings remain null and verified flags false. Need dated native-platform numbers, entity matching and permission for any excerpt. Do not merge syndicated counts or turn recommendation percentages into stars. | Review-data owner; content population pending. |
| Review schema limits | Requested AggregateRating/Review code exists but remains disabled for third-party aggregation. Organization JSON-LD is active. Dealer ownership does not become independent on a second domain; no search-star promise. | SEO reviewer; follow Google's current guidelines before any change. |
| Hosting and DNS release | Cloudflare Pages and private S3+CloudFront are documented only. No project created. New-domain account ownership, hosting choice, DNS change and publication need separate explicit approval. | Spencer / DNS owner; no launch attempted. |
| Geography | 50501 is Fort Dodge; Carroll is 51401. Scoring keeps 50501 distinct. Okoboji is an expansion query, not claimed inside the 50-mile Carroll core. Verify actual distances before publishing travel claims. | SEO reviewer; prevent geography conflation. |
| Local authority profiles | Organization sites identified, but Motor Inn membership/sponsorship claims remain unverified. Direct newspaper site retrieval was unavailable; current newspaper URL evidence is noted in job 10. | Local relationship owner; verify target and relationship before any later proposal. |
| Taras Shyn post source | No URL/full post was supplied or verified; recommendation evaluates the described reviews-domain concept only. | Optional research input; not required for the completed local draft. |

Sources informing schema and hosting decisions are linked directly in RECOMMENDATION.md and DEPLOY-NOTES.md. Historical memory was used only for the labeled prior GSC identity/grant and CRM archive pointers; neither was represented as live proof.


## FULLY AUTOMATED PIPELINE - SEPT 16

Build completed and verified locally on 2026-09-16 America/Chicago; final verification `2026-09-17T00:43:40.881740+00:00`. This section updates the earlier credential/access blockers above. **The code and handoff artifacts are built; live end-to-end operation is not yet activated.**

- Weekly driver, bounded pending research refresh, capped/cached DataForSEO research, remote GSC checks, dated inventory content assembly, evidence-bound page generation and one approval queue for SEO/October posts are implemented.
- Approved DealerOn jobs produce exact approved HTML plus metadata/evidence/QA/submission packets and one consolidated weekly Jeeves email draft. Approved AI jobs have an isolated branch/PR path; no email send, main-branch push or merge is performed by this build.
- `106` tests passed; Python compile, shell syntax, all three plist lints and whitespace checks passed. The isolated `test-page-alpha` journey reached a local ready packet with a signed simulated Slack approval and was deleted after QA. No real approval, external send, PR or publication occurred.
- Existing live evidence inspected: group GSC 1,899 query rows / 3,728 query-page rows; Toyota accessible with zero rows; Chevrolet property remains unshared. Credentials stay on the mini via SSH. DataForSEO actual spend $0.10 with $0.32 conservatively reserved; cached screenshot retained. DealerVault source has 72 rows; only derived inventory aggregates and provenance stored.
- Final real builder result: five source-derived inventory briefs, zero fully assembled candidates and 11 blocked by truthful source/topology/staging gates. Local queue: 12 October drafts, three blocked October posts plus one blocked financing research job, zero approved/ready pages.
- Schedules supplied: Monday 06:00 research/preparation, daily 07:30 approval sync, daily 07:45 approved handoffs/AI PR execution. They are not installed or loaded. Slack bridge identity/signing settings, DealerOn recipient and AI-proxy destination provisioning still require operator setup and live canaries. Spencer's intended recurring action remains an exact digest-bound APPROVE/HOLD/REJECT Slack reply.

Full file inventory, reproducible checks, installation commands, source limitations and exact Slack format: [pipeline/BUILD-REPORT.md](../pipeline/BUILD-REPORT.md). Runtime/input contract: [pipeline/README.md](../pipeline/README.md). Authentication contract: [automation/approval_state.md](../automation/approval_state.md). Generated test evidence: `pipeline/runs/build-validation.json`. Existing source runbooks and absolute host paths remain local dependencies.
