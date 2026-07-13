#!/usr/bin/env node
/**
 * publish-gbp-posts.mjs
 *
 * Publishes Rory's weekly GBP post drafts
 * (content/drafts/gbp-posts/posts-week-of-YYYY-MM-DD.md) as Google Business
 * Profile "What's New" posts via the Google My Business v4 localPosts API.
 *
 * Usage:
 *   node scripts/publish-gbp-posts.mjs [--dry-run] [--all] [--limit N]
 *
 *   --dry-run   Parse the newest drafts file and print the publish plan
 *               without calling Google. Exits 0 even without credentials.
 *   --all       Ignore the publish-date filter (default: only posts whose
 *               publish date is <= today America/Chicago are due).
 *   --limit N   Publish at most N posts this run (use --limit 1 for the
 *               first live smoke test).
 *
 * Deterministic, node stdlib only, no LLM calls.
 *
 * Idempotent: a ledger at content/drafts/gbp-posts/published-state.json is
 * keyed by "<week-marker>::<post title>::<location>". Already-published
 * posts are skipped.
 *
 * Fails loud (nonzero exit, clear message) if credentials are missing or
 * any request fails — no silent fallback. Error classes are reported
 * precisely (dead refresh token vs missing scope vs API disabled vs
 * unapproved-project quota=0).
 *
 * Credentials: ~/.config/google-business-profile/credentials.json
 * (override with GBP_CREDS_FILE):
 *   {
 *     "credentials": { ...authorized_user or service_account JSON... },
 *     "account_id": "accounts/1234567890",            // optional, discovered
 *     "location_ids": ["locations/9876543210"]        // required to publish
 *   }
 *   credentials must carry the https://www.googleapis.com/auth/business.manage
 *   scope (authorized_user: consented at auth time; service_account: the SA
 *   email must be added as a manager of the Business Profile).
 *
 * BLOCKED as of 2026-07-13 (MOT-2428): GCP project jeeves-485623 has no GBP
 * API approval (quota=0) and the legacy Google My Business API is not
 * enabled. See scripts/README-gbp-publisher.md for the exact unblock path.
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const REPO_ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const DRAFTS_DIR = path.join(REPO_ROOT, 'content', 'drafts', 'gbp-posts');
const LEDGER_FILE = path.join(DRAFTS_DIR, 'published-state.json');
const CREDS_FILE =
  process.env.GBP_CREDS_FILE ||
  path.join(os.homedir(), '.config', 'google-business-profile', 'credentials.json');
const TIMEOUT_MS = 30000;
const SUMMARY_MAX = 1500; // GBP localPost summary hard limit

const V4_BASE = 'https://mybusiness.googleapis.com/v4';
const ACCT_MGMT_BASE = 'https://mybusinessaccountmanagement.googleapis.com/v1';
const BIZ_INFO_BASE = 'https://mybusinessbusinessinformation.googleapis.com/v1';
const SCOPE = 'https://www.googleapis.com/auth/business.manage';

// Draft "CTA button" text -> v4 localPost callToAction.actionType.
// CALL uses the location's phone number; the others require an http(s) url.
const CTA_MAP = {
  'call now': { actionType: 'CALL', needsUrl: false },
  'learn more': { actionType: 'LEARN_MORE', needsUrl: true },
  'book now': { actionType: 'BOOK', needsUrl: true },
  'browse inventory': { actionType: 'SHOP', needsUrl: true },
  'shop now': { actionType: 'SHOP', needsUrl: true },
  'sign up': { actionType: 'SIGN_UP', needsUrl: true },
  'order now': { actionType: 'ORDER', needsUrl: true },
};

function die(msg, code = 1) {
  console.error(`fatal: ${msg}`);
  process.exit(code);
}

function parseArgs() {
  const args = { dryRun: false, all: false, limit: Infinity };
  const argv = process.argv.slice(2);
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--dry-run') args.dryRun = true;
    else if (a === '--all') args.all = true;
    else if (a === '--limit') {
      const n = Number(argv[++i]);
      if (!Number.isInteger(n) || n < 1) die('--limit requires a positive integer');
      args.limit = n;
    } else die(`unknown argument: ${a}`);
  }
  return args;
}

function todayCentral() {
  // YYYY-MM-DD in America/Chicago, matching the weekly SEO pipeline.
  return new Date().toLocaleDateString('en-CA', { timeZone: 'America/Chicago' });
}

// ---------------------------------------------------------------------------
// Draft parsing
// ---------------------------------------------------------------------------

function newestDraftFile() {
  if (!fs.existsSync(DRAFTS_DIR)) die(`drafts directory not found: ${DRAFTS_DIR}`);
  const files = fs
    .readdirSync(DRAFTS_DIR)
    .filter((f) => /^posts-week-of-\d{4}-\d{2}-\d{2}\.md$/.test(f))
    .sort();
  if (files.length === 0) die(`no posts-week-of-*.md files under ${DRAFTS_DIR}`);
  return path.join(DRAFTS_DIR, files[files.length - 1]);
}

function field(block, name) {
  const m = block.match(new RegExp(`^\\*\\*${name}:\\*\\*\\s*(.+)$`, 'mi'));
  return m ? m[1].trim() : null;
}

function parseDrafts(file) {
  const text = fs.readFileSync(file, 'utf8');
  const weekMarker = path.basename(file, '.md'); // posts-week-of-YYYY-MM-DD
  const chunks = text.split(/^### /m).slice(1);
  const posts = [];
  for (const chunk of chunks) {
    const headerLine = chunk.split('\n', 1)[0].trim();
    const titleMatch = headerLine.match(/^Post\s+\d+:\s*(.+)$/);
    if (!titleMatch) continue;
    const title = titleMatch[1].trim();
    const publishDate = field(chunk, 'Publish date');
    const ctaButton = field(chunk, 'CTA button');
    const ctaLink = field(chunk, 'CTA link');
    const copyMatch = chunk.match(/\*\*Copy:\*\*\s*\n([\s\S]*?)\n\s*\*\*CTA button:\*\*/);
    const copy = copyMatch ? copyMatch[1].trim() : null;

    if (!publishDate || !/^\d{4}-\d{2}-\d{2}$/.test(publishDate)) {
      die(`post "${title}" in ${file} has a missing/malformed **Publish date:** field`);
    }
    if (!copy) die(`post "${title}" in ${file} has no **Copy:** section`);
    if (copy.length > SUMMARY_MAX) {
      die(`post "${title}" copy is ${copy.length} chars (GBP limit ${SUMMARY_MAX})`);
    }
    if (!ctaButton) die(`post "${title}" in ${file} has no **CTA button:** field`);
    const cta = CTA_MAP[ctaButton.toLowerCase()];
    if (!cta) {
      die(`post "${title}" has unmapped CTA button "${ctaButton}" — add it to CTA_MAP in ${path.basename(fileURLToPath(import.meta.url))}`);
    }
    if (cta.needsUrl && !/^https?:\/\//.test(ctaLink || '')) {
      die(`post "${title}" CTA "${ctaButton}" requires an http(s) **CTA link:**, got: ${ctaLink}`);
    }
    posts.push({ weekMarker, title, publishDate, copy, ctaButton, ctaLink, cta });
  }
  if (posts.length === 0) die(`no "### Post N: title" blocks parsed from ${file}`);
  return posts;
}

// ---------------------------------------------------------------------------
// Ledger
// ---------------------------------------------------------------------------

function loadLedger() {
  if (!fs.existsSync(LEDGER_FILE)) return {};
  try {
    return JSON.parse(fs.readFileSync(LEDGER_FILE, 'utf8'));
  } catch (err) {
    die(`ledger is not valid JSON: ${LEDGER_FILE} (${err.message}) — fix or remove it before publishing`);
  }
}

function saveLedger(ledger) {
  fs.writeFileSync(LEDGER_FILE, JSON.stringify(ledger, null, 2) + '\n');
}

function ledgerKey(post, locationId) {
  return `${post.weekMarker}::${post.title}::${locationId}`;
}

// ---------------------------------------------------------------------------
// Google auth (stdlib only)
// ---------------------------------------------------------------------------

function loadConfig() {
  if (!fs.existsSync(CREDS_FILE)) {
    die(
      `GBP credentials not configured: ${CREDS_FILE} does not exist. ` +
        `Publishing requires approved GBP API access on a GCP project plus a ` +
        `business.manage credential. See scripts/README-gbp-publisher.md (MOT-2428). ` +
        `No fallback; nothing was published.`
    );
  }
  let cfg;
  try {
    cfg = JSON.parse(fs.readFileSync(CREDS_FILE, 'utf8'));
  } catch (err) {
    die(`GBP credentials file is not valid JSON: ${CREDS_FILE} (${err.message})`);
  }
  if (!cfg.credentials || typeof cfg.credentials !== 'object') {
    die(`GBP credentials file ${CREDS_FILE} is missing the "credentials" object`);
  }
  return cfg;
}

async function fetchJson(url, init = {}) {
  const res = await fetch(url, { ...init, signal: AbortSignal.timeout(TIMEOUT_MS) });
  const text = await res.text();
  let json = null;
  try {
    json = JSON.parse(text);
  } catch {
    /* non-JSON body — handled by callers via status */
  }
  return { res, json, text };
}

function b64url(buf) {
  return Buffer.from(buf).toString('base64url');
}

async function getAccessToken(creds) {
  if (creds.type === 'authorized_user') {
    const body = new URLSearchParams({
      client_id: creds.client_id,
      client_secret: creds.client_secret,
      refresh_token: creds.refresh_token,
      grant_type: 'refresh_token',
    });
    const { res, json, text } = await fetchJson('https://oauth2.googleapis.com/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body,
    });
    if (!res.ok) {
      const sub = json?.error_subtype || json?.error || '';
      if (String(sub).includes('rapt') || json?.error === 'invalid_grant') {
        die(
          `OAuth refresh token is dead (${json?.error}/${json?.error_subtype ?? 'n/a'}): ` +
            `re-consent is required (this is the same invalid_rapt failure the gcloud ADC hit on 2026-07-13). ` +
            `Re-run the OAuth consent for scope ${SCOPE} and update ${CREDS_FILE}.`
        );
      }
      die(`token refresh failed: HTTP ${res.status} ${text.slice(0, 300)}`);
    }
    return json.access_token;
  }
  if (creds.type === 'service_account') {
    const now = Math.floor(Date.now() / 1000);
    const header = b64url(JSON.stringify({ alg: 'RS256', typ: 'JWT' }));
    const claims = b64url(
      JSON.stringify({
        iss: creds.client_email,
        scope: SCOPE,
        aud: creds.token_uri,
        iat: now,
        exp: now + 3600,
      })
    );
    const signingInput = `${header}.${claims}`;
    const signature = crypto
      .sign('RSA-SHA256', Buffer.from(signingInput), creds.private_key)
      .toString('base64url');
    const body = new URLSearchParams({
      grant_type: 'urn:ietf:params:oauth:grant-type:jwt-bearer',
      assertion: `${signingInput}.${signature}`,
    });
    const { res, json, text } = await fetchJson(creds.token_uri, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body,
    });
    if (!res.ok) die(`service-account token grant failed: HTTP ${res.status} ${text.slice(0, 300)}`);
    return json.access_token;
  }
  die(`unsupported credentials.type "${creds.type}" — expected authorized_user or service_account`);
}

// Turn a Google API error into a precise, loud diagnosis.
function explainGoogleError(status, json, text, context) {
  const reason = json?.error?.details?.find((d) => d.reason)?.reason || '';
  const message = json?.error?.message || text.slice(0, 300);
  if (status === 401) {
    return `${context}: HTTP 401 UNAUTHENTICATED — the access token was rejected. ${message}`;
  }
  if (status === 403 && reason === 'ACCESS_TOKEN_SCOPE_INSUFFICIENT') {
    return (
      `${context}: HTTP 403 ACCESS_TOKEN_SCOPE_INSUFFICIENT — the credential lacks the ` +
      `${SCOPE} scope. Re-consent with that scope; do not reuse gcloud CLI tokens.`
    );
  }
  if (status === 403 && /has not been used in project|it is disabled/i.test(message)) {
    return (
      `${context}: HTTP 403 SERVICE_DISABLED — the API is not enabled on the GCP project. ` +
      `${message}`
    );
  }
  if (status === 429 && /quota/i.test(message)) {
    const zeroQuota = json?.error?.details?.some(
      (d) => d.metadata?.quota_limit_value === '0'
    );
    if (zeroQuota) {
      return (
        `${context}: HTTP 429 with quota_limit_value=0 — the GCP project has NOT been approved ` +
        `for Google Business Profile API access (Google grants 0 quota until the access-request ` +
        `form is approved). Submit https://support.google.com/business/contact/api_default — ` +
        `see scripts/README-gbp-publisher.md.`
      );
    }
    return `${context}: HTTP 429 rate-limited — ${message}`;
  }
  return `${context}: HTTP ${status} — ${message}`;
}

async function gbpGet(token, url, context) {
  const { res, json, text } = await fetchJson(url, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) die(explainGoogleError(res.status, json, text, context));
  return json;
}

// ---------------------------------------------------------------------------
// Location resolution / bootstrap discovery
// ---------------------------------------------------------------------------

async function discoverAndDie(token) {
  console.error('No location_ids configured — running read-only discovery instead of publishing.');
  const accounts = await gbpGet(token, `${ACCT_MGMT_BASE}/accounts`, 'list accounts');
  const accts = accounts.accounts || [];
  if (accts.length === 0) {
    die(
      'credential is valid but sees zero Business Profile accounts. If this is a service ' +
        'account, its email must first be added as a Manager of the Motor Inn Business ' +
        'Profile at https://business.google.com (People & access).'
    );
  }
  for (const a of accts) {
    console.error(`account: ${a.name}  (${a.accountName || ''} ${a.type || ''})`);
    const locs = await gbpGet(
      token,
      `${BIZ_INFO_BASE}/${a.name}/locations?readMask=name,title,storefrontAddress&pageSize=100`,
      `list locations for ${a.name}`
    );
    for (const l of locs.locations || []) {
      const addr = l.storefrontAddress
        ? `${(l.storefrontAddress.addressLines || []).join(' ')}, ${l.storefrontAddress.locality || ''}`
        : '';
      console.error(`  location: ${l.name}  "${l.title}"  ${addr}`);
    }
  }
  die(
    `discovery complete — copy the wanted account "name" into account_id and location ` +
      `"name"(s) into location_ids in ${CREDS_FILE}, then re-run.`,
    2
  );
}

function normalizeParent(accountId, locationId) {
  // Accept "accounts/X/locations/Y" or bare "locations/Y" (+ account_id).
  if (/^accounts\/[^/]+\/locations\/[^/]+$/.test(locationId)) return locationId;
  if (/^locations\/[^/]+$/.test(locationId)) {
    if (!/^accounts\/[^/]+$/.test(accountId || '')) {
      die(`location_ids entry "${locationId}" needs account_id ("accounts/<id>") set in ${CREDS_FILE}`);
    }
    return `${accountId}/${locationId}`;
  }
  die(`malformed location_ids entry "${locationId}" — expected "locations/<id>" or "accounts/<id>/locations/<id>"`);
}

// ---------------------------------------------------------------------------
// Publish
// ---------------------------------------------------------------------------

function buildLocalPost(post) {
  const body = {
    languageCode: 'en-US',
    topicType: 'STANDARD', // all drafts publish as "What's New" per MOT-2428
    summary: post.copy,
    callToAction: { actionType: post.cta.actionType },
  };
  if (post.cta.needsUrl) body.callToAction.url = post.ctaLink;
  return body;
}

async function createLocalPost(token, parent, post) {
  const url = `${V4_BASE}/${parent}/localPosts`;
  const { res, json, text } = await fetchJson(url, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify(buildLocalPost(post)),
  });
  if (!res.ok) {
    die(explainGoogleError(res.status, json, text, `create localPost "${post.title}" on ${parent}`));
  }
  return json;
}

function buildPlan(posts, ledger, locations, args, today) {
  const due = posts.filter((p) => args.all || p.publishDate <= today);
  const plan = [];
  for (const post of due) {
    for (const loc of locations) {
      const key = ledgerKey(post, loc);
      if (ledger[key]) continue;
      plan.push({ post, loc, key });
    }
  }
  const capped = plan.slice(0, args.limit === Infinity ? plan.length : args.limit);
  return { due, plan, capped };
}

function printPlan(posts, due, plan, capped, args) {
  console.log(
    `parsed ${posts.length} posts; ${due.length} due${args.all ? ' (--all)' : ''}; ` +
      `${plan.length} unpublished; publishing ${capped.length} this run`
  );
  for (const item of capped) {
    console.log(
      `  -> [${item.post.publishDate}] "${item.post.title}" (${item.post.cta.actionType}) @ ${item.loc}`
    );
  }
}

async function main() {
  const args = parseArgs();
  const draftFile = newestDraftFile();
  const posts = parseDrafts(draftFile);
  const ledger = loadLedger();
  const today = todayCentral();

  console.log(`drafts file: ${draftFile}`);
  console.log(`today (America/Chicago): ${today}`);

  if (args.dryRun) {
    const cfgSafe = loadConfigSafe();
    const locations =
      Array.isArray(cfgSafe?.location_ids) && cfgSafe.location_ids.length > 0
        ? cfgSafe.location_ids
        : ['<unconfigured>'];
    const { due, plan, capped } = buildPlan(posts, ledger, locations, args, today);
    printPlan(posts, due, plan, capped, args);
    if (!fs.existsSync(CREDS_FILE)) {
      console.log(
        `dry-run note: GBP credentials not configured at ${CREDS_FILE} — a real run would fail loud here.`
      );
    }
    console.log('dry-run complete — nothing published.');
    return;
  }

  // Real run: credentials are validated up front so a broken/missing setup
  // always fails loud, even on weeks where nothing is due.
  const cfg = loadConfig(); // dies loud with "GBP credentials not configured" if absent
  const token = await getAccessToken(cfg.credentials);
  if (!Array.isArray(cfg.location_ids) || cfg.location_ids.length === 0) {
    await discoverAndDie(token);
  }

  const { due, plan, capped } = buildPlan(posts, ledger, cfg.location_ids, args, today);
  printPlan(posts, due, plan, capped, args);

  if (capped.length === 0) {
    console.log('nothing to publish (no due posts outside the ledger) — done.');
    return;
  }

  let published = 0;
  for (const item of capped) {
    const parent = normalizeParent(cfg.account_id, item.loc);
    const created = await createLocalPost(token, parent, item.post);
    ledger[item.key] = {
      publishedAt: new Date().toISOString(),
      name: created.name || null,
      searchUrl: created.searchUrl || null,
      state: created.state || null,
      publishDate: item.post.publishDate,
    };
    saveLedger(ledger); // save after every post: crash-safe idempotency
    published++;
    console.log(`published "${item.post.title}" -> ${created.name || '?'}`);
    if (created.searchUrl) console.log(`  live URL: ${created.searchUrl}`);
  }
  console.log(`done — published ${published} post(s); ledger: ${LEDGER_FILE}`);
}

// Non-fatal config peek for dry-run planning only.
function loadConfigSafe() {
  try {
    return JSON.parse(fs.readFileSync(CREDS_FILE, 'utf8'));
  } catch {
    return null;
  }
}

main().catch((err) => die(err?.stack || String(err)));
