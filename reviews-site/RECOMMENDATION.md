# Reviews-domain recommendation

Prepared 2026-09-16. Draft only; no purchase or publication performed.

Recommend **motorinnautogroupreviews.com** as the exact-match brand-plus-reviews domain for this project, subject to Spencer's purchase approval. It covers the group rather than favoring one franchise. Use it as a transparent, dealer-maintained directory of original review sources. Do not represent it as independent editorial coverage or promise a ranking lift from the domain name.

## Availability evidence
Read-only checks on 2026-09-16 returned:

| Domain | Verisign WHOIS | Verisign .com RDAP | DNS A query | Assessment |
|---|---|---|---|---|
| motorinnautogroupreviews.com | No match | HTTP 404 | NXDOMAIN | Appears unregistered; first choice |
| motorinntoyotaofcarrollreviews.com | No match | HTTP 404 | NXDOMAIN | Appears unregistered; Toyota-only alternate |
| motorinnofcarrollreviews.com | No match | HTTP 404 | NXDOMAIN | Appears unregistered; Carroll/Chevrolet alternate |

Commands: `whois -h whois.verisign-grs.com DOMAIN`, `dig +time=3 +tries=1 DOMAIN A`, and `https://rdap.verisign.com/com/v1/domain/DOMAIN`. WHOIS “No match” plus RDAP 404 is evidence of no registry record at check time. DNS alone cannot establish availability. Registrar checkout, price, premium/reserved status and renewal cost remain unverified. Recheck immediately before an approved purchase. Do not buy alternates automatically.

## SEO and trust decision
The requested Taras Shyn idea was supplied as a concept; no post URL or full post was supplied or verified. This recommendation evaluates the concept, not a claimed result from that post.

The new domain will need its own discovery, maintenance and useful content. Keep it focused on review navigation, source dates and transparent ownership. If upkeep cannot be sustained, the existing official [review page](https://www.motorinnautogroup.com/customer-reviews.aspx) is a lower-maintenance alternative. Do not duplicate all dealership content across the new domain.

Google excludes dealer-controlled Organization/LocalBusiness self-reviews from review rich results and says not to aggregate other sites' reviews or ratings for that feature. Owning a second domain does not make the reviews independent. Therefore this draft includes Organization JSON-LD and implemented but disabled AggregateRating/Review support for a separately verified first-party collection. Third-party platform summaries never enter rating markup. No stars or review-rich-result outcome is promised. [Google review structured-data guidance](https://developers.google.com/search/docs/appearance/structured-data/review-snippet)

## What is ready
- Responsive static page with inline CSS, no framework, fonts, tracking, embeds or external asset requests.
- One local `REVIEWS-DATA.js` holds all editable summary values, profile/review URLs, provenance and permitted review excerpts.
- Google, Facebook, DealerRater, Cars.com and CarGurus are represented. Counts and ratings are null placeholders; the page shows “not yet verified,” never fabricated stars.
- Profile links found: [Facebook](https://www.facebook.com/MotorInnAutoGroup/) from the official review page; [DealerRater](https://www.dealerrater.com/dealer/Motor-Inn-of-Carroll-LLC-review-16644/) from its [Iowa Toyota directory](https://www.dealerrater.com/directory/iowa/Toyota/); [CarGurus](https://www.cargurus.com/Cars/m-Motor-Inn-of-Carroll-sp368029) public profile.
- Existing Facebook/DealerRater/CarGurus “leave a review” links open the relevant profile; users must follow that platform's review flow and eligibility. Submission flows were not exercised. Direct profile retrieval for DealerRater was unavailable, so its destination still needs browser QA before launch.
- Google's exact Carroll GBP profile and review composer link remain unresolved. A clearly labeled Maps lookup is supplied. Cars.com's exact Carroll profile was not found in the bounded search; a clearly labeled dealer-directory lookup is supplied. Their leave-review controls are visibly disabled until real profile/write links are entered.

## Open launch decisions
1. Spencer's explicit domain purchase approval and budget; no purchase now.
2. Exact Google/Cars.com URLs and confirmation that all five profiles refer to the intended Carroll business/franchise.
3. Fresh, sourced native-platform counts/ratings and check dates. Do not convert recommendation percentages into stars or add syndicated reviews into a unique-customer total.
4. Permission to reproduce any review text; otherwise keep only platform links and permitted summaries. No testimonial was copied in this build.
5. Hosting/DNS/deployment approval after the final page and data are reviewed. The preview carries `noindex, nofollow` until then.
