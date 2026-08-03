# Google Business Profile API Readiness

Project: `jeeves-485623` (`53355027587`)

The unattended path has three independent gates:

1. Google grants nonzero GBP API quota to the Cloud project.
2. Primary owner `spenchey@gmail.com` grants offline OAuth scope
   `https://www.googleapis.com/auth/business.manage` through the OAuth client
   owned by that same project.
3. Read-only discovery finds exactly one configured Carroll profile at
   `1526 Le Clark Rd, Carroll, IA`. The preferred title is
   `Motor Inn Toyota and Chevrolet of Carroll`; `Motor Inn Auto Group` is the
   fallback alias.

`gbp-approval-watch.mjs` may stage access credentials after all three gates,
but it never creates the canonical live `credentials.json` file. Publishing
remains separately approval-gated.

## Commands

Validate that the correct OAuth client is available without opening a browser:

```bash
node scripts/gbp-owner-oauth-bootstrap.mjs --check
```

Start the one-time owner consent flow:

```bash
node scripts/gbp-owner-oauth-bootstrap.mjs
```

Probe quota and, after approval, perform read-only account/location discovery:

```bash
node scripts/gbp-approval-watch.mjs
```

## Safety

- Raw OAuth and service-account credentials stay outside git with mode `600`.
- Discovery never selects the first returned account or location.
- Missing, duplicate, or wrong-address Carroll profiles block staging.
- Staging does not publish a post, upload a photo, edit a profile, or enable a
  live publisher.
