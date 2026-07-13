# GBP Post Publisher — status & unblock runbook (MOT-2428)

`scripts/publish-gbp-posts.mjs` publishes Rory's weekly drafts
(`content/drafts/gbp-posts/posts-week-of-*.md`) as Google Business Profile
"What's New" posts. It is **staged but BLOCKED**: no credential on the Mini
can reach the GBP APIs. It is wired (gated) into
`~/clawd/scripts/no-model/weekly-seo-audit.sh` and activates automatically
once `~/.config/google-business-profile/credentials.json` exists.

## Verified access state (probed 2026-07-13 from the Mini, read-only)

| Credential | Result | Meaning |
|---|---|---|
| `~/.config/gcloud/application_default_credentials.json` (Workspace) | `400 invalid_grant / invalid_rapt` | refresh token dead — Workspace reauth expired |
| `legacy_credentials/spencer.heywood@motorinnmail.com/adc.json` | `400 invalid_grant / invalid_rapt` | same — dead |
| `legacy_credentials/spenchey@gmail.com/adc.json` | token OK, GBP → `403 ACCESS_TOKEN_SCOPE_INSUFFICIENT` | token alive but scoped to cloud-platform only; no `business.manage` |
| `~/.config/gcloud/ga4-service-account.json` (`ga4-reader@jeeves-485623`) | token OK w/ `business.manage`; new GBP APIs → `429 quota_limit_value=0`; legacy v4 → `403 SERVICE_DISABLED` | project **jeeves-485623** has the two new GBP APIs *enabled* but **zero quota = GBP API access never approved by Google**; legacy My Business API (v4, needed for localPosts) not enabled |

Notes on prior "GBP data": `audits/gbp-structural/gbp-research-*.json` are EXA
web-search article dumps (weekly-seo-audit.sh), **not** GBP API data. The
`~/clawd/scripts/no-model/google-reviews/*` pipeline is mock/simulated end to
end (hardcoded fake reviews, "Simulating approval"). Nothing has ever talked
to a real GBP API from this machine.

## Unblock path (Spencer, ~15 min of clicks + a Google approval wait)

Use GCP project **jeeves-485623** (project number 53355027587) — it already
has `mybusinessaccountmanagement` and `mybusinessbusinessinformation`
enabled, and it is visible to **spenchey@gmail.com**.

1. **Request GBP API access** (the per-project approval gate):
   while signed in as the Google account that manages the Motor Inn Business
   Profile, fill Google's access-request form at
   <https://support.google.com/business/contact/api_default>
   with project ID `jeeves-485623`. Approval arrives by email (typically days,
   not weeks). Until approved, quota stays 0 and every call 429s.
   - Which account manages the profile is NOT provable from files on the
     Mini; check <https://business.google.com> — candidates are
     `spencer.heywood@motorinnmail.com` and `spenchey@gmail.com`.
2. **Enable the legacy Google My Business API (v4)** — posts (localPosts)
   were never migrated to the new split APIs:
   <https://console.developers.google.com/apis/api/mybusiness.googleapis.com/overview?project=53355027587>
   (this API is only visible/enabled after step 1 approval).
3. **Pick the credential** (either works):
   - *Service account (recommended, no token rot):* at
     <https://business.google.com> → Business Profile settings → People &
     access → add `ga4-reader@jeeves-485623.iam.gserviceaccount.com` as
     **Manager**. Then `credentials.json` (below) uses the existing key file.
   - *OAuth user:* create an OAuth client (Desktop) in jeeves-485623, run a
     consent flow as the profile-owner account with scope
     `https://www.googleapis.com/auth/business.manage`, and store the
     refresh-token JSON. (Workspace reauth policy killed the previous user
     tokens — service account avoids repeats.)
4. **Create the config file** `~/.config/google-business-profile/credentials.json`
   (`chmod 600`):
   ```json
   {
     "credentials": { /* paste of ga4-service-account.json, or authorized_user JSON */ },
     "account_id": "accounts/<id>",
     "location_ids": ["locations/<carroll-id>", "locations/<okoboji-id>"]
   }
   ```
   Don't know the IDs? Leave `location_ids` out and run
   `node scripts/publish-gbp-posts.mjs` — it does a read-only discovery,
   prints every account/location the credential can see, and exits.
5. **Smoke-test one real post, then let the cron take over:**
   ```bash
   node ~/motor-inn-seo/scripts/publish-gbp-posts.mjs --dry-run    # preview
   node ~/motor-inn-seo/scripts/publish-gbp-posts.mjs --limit 1    # ONE live post; prints the live URL
   ```
   The Monday weekly-seo-audit cron then publishes due posts automatically.

## Behavior

- Reads the **newest** `posts-week-of-*.md`; publishes posts whose
  `**Publish date:**` is <= today (America/Chicago). `--all` overrides.
- All post types publish as `topicType: STANDARD` ("What's New").
  CTA mapping: Call Now→CALL (uses location phone), Learn More→LEARN_MORE,
  Book Now→BOOK, Browse Inventory→SHOP, Sign Up→SIGN_UP.
- Images in drafts are prose descriptions of photos that don't exist as
  files, so posts publish text+CTA only (GBP media upload is a follow-up).
- Idempotent via `content/drafts/gbp-posts/published-state.json`, keyed
  `<week-file>::<post title>::<location>`. Delete a key to force a repost.
- Fail-loud: nonzero exit and a precise diagnosis for dead refresh tokens
  (`invalid_rapt`), missing scope (403), API disabled (403), unapproved
  project (429 quota=0), and anything else. No silent fallback.
- Cadence note: drafts schedule posts Tue/Thu; the Monday cron publishes
  them up to 5 days late. Once live, consider a dedicated
  `0 9 * * 2,4` crontab entry running the same command.
