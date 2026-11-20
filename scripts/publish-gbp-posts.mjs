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
 *   node scripts/publish-gbp-posts.mjs --list-pending [--file NAME]
 *   node scripts/publish-gbp-posts.mjs --approve 1,3 --approved-by "Spencer" [--file NAME]
 *
 * APPROVAL GATE (Spencer, 2026-11-17): nothing publishes without his OK.
 * APPROVAL LOCK (Spencer, 2026-11-20): an approval covers the exact wording
 * Spencer saw. A post publishes only if BOTH:
 *   1. its header (above **Copy:**) carries `**Approval:** approved ...`, and
 *   2. the approvals lock holds an entry for that drafts file + post number
 *      whose fingerprint matches what would be sent now (title, publish date,
 *      copy, CTA type and link). Any later edit, even one character, stops it.
 * The lock lives OUTSIDE the repo (default
 * ~/.config/motor-inn-seo/gbp-approvals.json, override GBP_APPROVALS_FILE),
 * so agents editing or committing the drafts folder never touch it. A missing
 * lock means nothing publishes. A malformed lock stops the run.
 *   --list-pending   Print the posts that cannot publish and why; no Google calls.
 *   --approve N,M    Mark post number(s) N,M approved and record their exact
 *                    wording in the lock. Run ONLY after Spencer himself
 *                    approved that wording in chat. Requires --approved-by.
 *   --approved-at "YYYY-MM-DD HH:MM"  With --approve: the Central time the
 *                    approval was given (default: now).
 *   --check-approvals  Report approved posts whose lock is missing or no longer
 *                    matches; exit 3 if any are still unpublished. No Google calls.
 *   --file NAME      With --list-pending or --approve: use this drafts file
 *                    (posts-week-of-YYYY-MM-DD.md) instead of the newest one.
 *
 * Publishing reads the newest drafts file plus every older drafts file that
 * has a lock entry or an approval line. Posts that match publish; a real run
 * then exits 3 (loud) if any approved, unpublished post was held by the lock.
 *
 * Test overrides: GBP_DRAFTS_DIR, GBP_LEDGER_FILE, GBP_APPROVALS_FILE.
 *
 *   --dry-run   Parse the publishable drafts files and print the publish plan
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
const DRAFTS_DIR = process.env.GBP_DRAFTS_DIR || path.join(REPO_ROOT, 'content', 'drafts', 'gbp-posts');
const LEDGER_FILE = process.env.GBP_LEDGER_FILE || path.join(DRAFTS_DIR, 'published-state.json');
const APPROVALS_FILE =
  process.env.GBP_APPROVALS_FILE ||
  path.join(os.homedir(), '.config', 'motor-inn-seo', 'gbp-approvals.json');
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
  'book appointment': { actionType: 'BOOK', needsUrl: true },
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
  const args = {
    dryRun: false, all: false, limit: Infinity, listPending: false, checkApprovals: false,
    approve: null, approvedBy: null, approvedAt: null, file: null,
  };
  const argv = process.argv.slice(2);
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--dry-run') args.dryRun = true;
    else if (a === '--all') args.all = true;
    else if (a === '--list-pending') args.listPending = true;
    else if (a === '--check-approvals') args.checkApprovals = true;
    else if (a === '--approved-at') {
      args.approvedAt = (argv[++i] || '').trim();
      if (!/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$/.test(args.approvedAt)) die('--approved-at must look like "YYYY-MM-DD HH:MM" (Central time)');
    }
    else if (a === '--approve') {
      const raw = argv[++i] || '';
      const nums = raw.split(',').map((x) => Number(x.trim()));
      if (!raw || nums.some((n) => !Number.isInteger(n) || n < 1)) die('--approve requires post numbers like 1,3');
      args.approve = nums;
    } else if (a === '--approved-by') {
      args.approvedBy = (argv[++i] || '').trim();
    } else if (a === '--file') {
      args.file = (argv[++i] || '').trim();
      if (!args.file) die('--file requires a drafts file name');
    }
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

const DRAFT_FILE_RE = /^posts-week-of-\d{4}-\d{2}-\d{2}\.md$/;

function draftFiles() {
  if (!fs.existsSync(DRAFTS_DIR)) die(`drafts directory not found: ${DRAFTS_DIR}`);
  const files = fs.readdirSync(DRAFTS_DIR).filter((f) => DRAFT_FILE_RE.test(f)).sort();
  if (files.length === 0) die(`no posts-week-of-*.md files under ${DRAFTS_DIR}`);
  return files.map((f) => path.join(DRAFTS_DIR, f));
}

function newestDraftFile() {
  const files = draftFiles();
  return files[files.length - 1];
}

// The newest file plus any older file that has a lock entry or an approval
// line. Older files with neither are not parsed, so old drafts cannot stop a
// run. Files with an approval line but no lock are parsed so the mismatch is
// reported, never silently dropped.
function publishableDraftFiles(lock) {
  const files = draftFiles();
  const newest = files[files.length - 1];
  const locked = new Set(Object.values(lock).map((e) => e.file));
  return files.filter(
    (f) =>
      f === newest ||
      locked.has(path.basename(f)) ||
      /^\*\*Approval:\*\*\s*approved\b/im.test(fs.readFileSync(f, 'utf8'))
  );
}

function namedDraftFile(name) {
  if (!DRAFT_FILE_RE.test(name)) die(`--file must look like posts-week-of-YYYY-MM-DD.md, got: ${name}`);
  const file = path.join(DRAFTS_DIR, name);
  if (!fs.existsSync(file)) die(`no such drafts file: ${name}`);
  return file;
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
    const titleMatch = headerLine.match(/^Post\s+(\d+):\s*(.+)$/);
    if (!titleMatch) continue;
    const postNumber = Number(titleMatch[1]);
    const title = titleMatch[2].trim();
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
    // Approval line: read from the header only (above **Copy:**), so an
    // "**Approval:** approved" line pasted into the copy never counts.
    // Only an explicit "approved ..." value counts; absent = pending.
    const head = chunk.split(/^\*\*Copy:\*\*/m, 1)[0];
    const approval = field(head, 'Approval');
    const lineApproved = /^approved\b/i.test(approval || '');
    // `approved` stays false until applyLock() confirms the exact wording.
    posts.push({
      file: path.basename(file), weekMarker, postNumber, title, publishDate, copy, ctaButton, ctaLink, cta,
      approval, lineApproved, approved: false, lockState: 'unchecked',
    });
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
// Approval lock: an approval is bound to the exact wording that was approved
// ---------------------------------------------------------------------------

function lockKey(post) {
  return `${post.file}::post-${post.postNumber}`;
}

// Exactly what reaches Google, plus the title and the schedule.
function approvedContent(post) {
  return { title: post.title, publishDate: post.publishDate, localPost: buildLocalPost(post) };
}

function canonical(v) {
  if (Array.isArray(v)) return `[${v.map(canonical).join(',')}]`;
  if (v && typeof v === 'object') {
    return `{${Object.keys(v).sort().map((k) => `${JSON.stringify(k)}:${canonical(v[k])}`).join(',')}}`;
  }
  return JSON.stringify(v);
}

function fingerprint(post) {
  return crypto.createHash('sha256').update(canonical(approvedContent(post))).digest('hex');
}

// Returns {} when the lock file does not exist (nothing can publish).
// Dies on a malformed lock: a broken lock must never be read as "no changes".
function loadApprovals() {
  if (!fs.existsSync(APPROVALS_FILE)) return {};
  let lock;
  try {
    lock = JSON.parse(fs.readFileSync(APPROVALS_FILE, 'utf8'));
  } catch (err) {
    die(`approvals lock is not valid JSON: ${APPROVALS_FILE} (${err.message}). Nothing published.`);
  }
  if (!lock || typeof lock !== 'object' || Array.isArray(lock)) {
    die(`approvals lock ${APPROVALS_FILE} must be a JSON object. Nothing published.`);
  }
  for (const [k, e] of Object.entries(lock)) {
    if (!e || typeof e !== 'object' || !/^[0-9a-f]{64}$/.test(e.sha256 || '') || !e.file || !e.content) {
      die(`approvals lock entry "${k}" in ${APPROVALS_FILE} is malformed. Nothing published.`);
    }
  }
  return lock;
}

function saveApprovals(lock) {
  fs.mkdirSync(path.dirname(APPROVALS_FILE), { recursive: true });
  const tmp = `${APPROVALS_FILE}.tmp-${process.pid}`;
  fs.writeFileSync(tmp, JSON.stringify(lock, null, 2) + '\n', { mode: 0o600 });
  fs.renameSync(tmp, APPROVALS_FILE);
}

// Sets post.lockState ('match' | 'no-lock' | 'changed') and post.approved.
function applyLock(posts, lock) {
  for (const p of posts) {
    const entry = lock[lockKey(p)];
    if (!entry) p.lockState = 'no-lock';
    else if (entry.sha256 === fingerprint(p)) p.lockState = 'match';
    else p.lockState = 'changed';
    p.approved = p.lineApproved && p.lockState === 'match';
  }
  return posts;
}

// First difference between two strings, with a little context either side.
function firstDiff(a, b) {
  a = String(a ?? '');
  b = String(b ?? '');
  let i = 0;
  while (i < a.length && i < b.length && a[i] === b[i]) i++;
  const from = Math.max(0, i - 40);
  return { approved: a.slice(from, i + 60), now: b.slice(from, i + 60) };
}

function describeChange(post, lock) {
  const entry = lock[lockKey(post)];
  if (!entry) return 'no lock entry: this wording was never recorded as approved';
  const was = entry.content;
  const now = approvedContent(post);
  const pairs = [
    ['title', was.title, now.title],
    ['publish date', was.publishDate, now.publishDate],
    ['copy', was.localPost?.summary, now.localPost.summary],
    ['CTA type', was.localPost?.callToAction?.actionType, now.localPost.callToAction.actionType],
    ['CTA link', was.localPost?.callToAction?.url, now.localPost.callToAction.url],
  ];
  const changed = pairs.filter(([, x, y]) => (x ?? null) !== (y ?? null));
  if (changed.length === 0) return 'wording changed since approval';
  return changed
    .map(([name, x, y]) => {
      const d = firstDiff(x, y);
      return `${name} changed since approval\n       approved: "${d.approved}"\n       now:      "${d.now}"`;
    })
    .join('\n     ');
}

// Approved-line posts the lock is holding back that are not yet published at
// every location. These are the ones a person must look at.
function lockProblems(posts, ledger, locations) {
  return posts.filter(
    (p) => p.lineApproved && !p.approved && locations.some((loc) => !ledger[ledgerKey(p, loc)])
  );
}

function reportLockProblems(problems, lock) {
  if (problems.length === 0) return;
  console.log(`APPROVAL LOCK: ${problems.length} approved post(s) held back because the wording does not match what was approved:`);
  for (const p of problems) {
    console.log(`  - ${p.file} post ${p.postNumber} [${p.publishDate}] "${p.title}"\n     ${describeChange(p, lock)}`);
  }
  console.log('  To publish, Spencer must approve the current wording in chat, then run --approve for it.');
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
  const dueAll = posts.filter((p) => args.all || p.publishDate <= today);
  const due = dueAll.filter((p) => p.approved); // approval gate: line + exact-wording lock
  const unapprovedDue = dueAll.length - due.length;
  const plan = [];
  for (const post of due) {
    for (const loc of locations) {
      const key = ledgerKey(post, loc);
      if (ledger[key]) continue;
      plan.push({ post, loc, key });
    }
  }
  const capped = plan.slice(0, args.limit === Infinity ? plan.length : args.limit);
  return { due, plan, capped, unapprovedDue };
}

function printPlan(posts, due, plan, capped, args, unapprovedDue = 0) {
  console.log(
    `parsed ${posts.length} posts; ${posts.filter((p) => p.approved).length} approved (wording locked); ` +
      `${unapprovedDue} due but NOT approved (skipped); ${due.length} due+approved${args.all ? ' (--all)' : ''}; ` +
      `${plan.length} unpublished; publishing ${capped.length} this run`
  );
  for (const item of capped) {
    console.log(
      `  -> [${item.post.publishDate}] "${item.post.title}" (${item.post.cta.actionType}) @ ${item.loc}`
    );
  }
}

function approvePosts(file, numbers, by, at) {
  const stamp =
    at ||
    new Date().toLocaleString('en-CA', {
      timeZone: 'America/Chicago', hour12: false, year: 'numeric', month: '2-digit', day: '2-digit',
      hour: '2-digit', minute: '2-digit',
    }).replace(',', '');
  const marker = `**Approval:** approved — ${by}, ${stamp} CT`;
  // Check every requested post parses before writing anything.
  const before = parseDrafts(file);
  for (const n of numbers) {
    if (before.filter((p) => p.postNumber === n).length !== 1) {
      die(`expected exactly one "### Post ${n}:" block in ${file}`);
    }
  }
  const parts = fs.readFileSync(file, 'utf8').split(/^(?=### )/m);
  for (const n of numbers) {
    const idx = parts.findIndex((c) => new RegExp(`^### Post\\s+${n}:`).test(c));
    let block = parts[idx];
    // Only touch the header (above **Copy:**), never the copy itself.
    const cut = block.search(/^\*\*Copy:\*\*/m);
    let head = cut < 0 ? block : block.slice(0, cut);
    const rest = cut < 0 ? '' : block.slice(cut);
    if (/^\*\*Approval:\*\*.*$/m.test(head)) {
      head = head.replace(/^\*\*Approval:\*\*.*$/m, marker);
    } else if (/^\*\*Publish date:\*\*.*$/m.test(head)) {
      head = head.replace(/^(\*\*Publish date:\*\*.*)$/m, `$1\n${marker}`);
    } else die(`post ${n} has no **Publish date:** line to anchor the approval`);
    parts[idx] = head + rest;
  }
  fs.writeFileSync(file, parts.join(''));

  // Record the exact wording now in the file. The drafts file is written
  // first, so a failure here leaves the post unpublishable (fail-safe).
  const lock = loadApprovals();
  const posts = parseDrafts(file);
  const recordedAt = new Date().toISOString();
  for (const n of numbers) {
    const p = posts.find((x) => x.postNumber === n);
    const key = lockKey(p);
    const sha256 = fingerprint(p);
    const prior = lock[key];
    lock[key] = {
      file: p.file, postNumber: p.postNumber, sha256, approvedBy: by, approvedAt: `${stamp} CT`, recordedAt,
      content: approvedContent(p),
    };
    const note = prior && prior.sha256 !== sha256 ? ' (replaces an approval of different wording)' : '';
    console.log(`  post ${n} [${p.publishDate}] "${p.title}" locked ${sha256.slice(0, 12)}${note}`);
  }
  saveApprovals(lock);
  console.log(
    `approved post(s) ${numbers.join(',')} in ${path.basename(file)} (${by}); exact wording locked in ${APPROVALS_FILE}. ` +
      'Nothing published; the next publisher run will publish due+approved posts.'
  );
}

async function main() {
  const args = parseArgs();
  if (args.file && !args.listPending && !args.approve) die('--file works only with --list-pending or --approve');
  if (args.approvedAt && !args.approve) die('--approved-at works only with --approve');
  const draftFile = args.file ? namedDraftFile(args.file) : newestDraftFile();
  const lock = loadApprovals(); // dies loud on a malformed lock
  const selectedPosts = applyLock(parseDrafts(draftFile), lock);
  const ledger = loadLedger();
  const today = todayCentral();

  console.log(`drafts file: ${draftFile}`);
  console.log(`today (America/Chicago): ${today}`);
  console.log(
    `approvals lock: ${APPROVALS_FILE} (${Object.keys(lock).length} entr${Object.keys(lock).length === 1 ? 'y' : 'ies'}` +
      `${fs.existsSync(APPROVALS_FILE) ? '' : ', file not found: nothing can publish'})`
  );

  if (args.listPending) {
    const pending = selectedPosts.filter((p) => !p.approved);
    console.log(`PENDING-APPROVAL: ${pending.length} of ${selectedPosts.length} posts in ${path.basename(draftFile)}`);
    for (const p of pending) {
      const snippet = p.copy.replace(/\s+/g, ' ').slice(0, 160);
      const why = p.lineApproved ? ` (held: ${p.lockState === 'changed' ? 'wording changed since approval' : 'approved wording not locked'})` : '';
      console.log(`${p.postNumber}. [${p.publishDate}] ${p.title} (CTA: ${p.ctaButton})${why}\n   "${snippet}..."`);
    }
    console.log('nothing published.');
    return;
  }

  if (args.approve) {
    if (!args.approvedBy) die('--approve requires --approved-by "<who approved>" (audit trail)');
    approvePosts(draftFile, args.approve, args.approvedBy, args.approvedAt);
    return;
  }

  const sourceFiles = publishableDraftFiles(lock);
  const posts = applyLock(
    sourceFiles.flatMap((f) => parseDrafts(f)),
    lock
  ).sort((a, b) => a.publishDate.localeCompare(b.publishDate));
  console.log(`publish sources: ${sourceFiles.map((f) => path.basename(f)).join(', ')}`);

  if (args.dryRun || args.checkApprovals) {
    const cfgSafe = loadConfigSafe();
    const locations =
      Array.isArray(cfgSafe?.location_ids) && cfgSafe.location_ids.length > 0
        ? cfgSafe.location_ids
        : ['<unconfigured>'];
    const problems = lockProblems(posts, ledger, locations);
    if (args.checkApprovals) {
      reportLockProblems(problems, lock);
      if (problems.length > 0) die(`${problems.length} approved post(s) held by the approval lock`, 3);
      console.log(`approval lock OK: every approved, unpublished post matches its approved wording. Nothing published.`);
      return;
    }
    const { due, plan, capped, unapprovedDue } = buildPlan(posts, ledger, locations, args, today);
    printPlan(posts, due, plan, capped, args, unapprovedDue);
    reportLockProblems(problems, lock);
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

  const { due, plan, capped, unapprovedDue } = buildPlan(posts, ledger, cfg.location_ids, args, today);
  printPlan(posts, due, plan, capped, args, unapprovedDue);
  const problems = lockProblems(posts, ledger, cfg.location_ids);
  reportLockProblems(problems, lock);
  const failIfHeld = () => {
    if (problems.length > 0) die(`${problems.length} approved post(s) held by the approval lock (see above)`, 3);
  };

  if (capped.length === 0) {
    console.log('nothing to publish (no due posts outside the ledger).');
    failIfHeld();
    console.log('done.');
    return;
  }

  let published = 0;
  for (const item of capped) {
    // Defense in depth: re-read the lock and re-check the exact wording right
    // before each call to Google.
    if (!item.post.approved) die(`refusing to publish unapproved post "${item.post.title}"`);
    const entry = loadApprovals()[lockKey(item.post)];
    if (!entry || entry.sha256 !== fingerprint(item.post)) {
      die(`refusing to publish "${item.post.title}": wording does not match the approved wording`);
    }
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
  console.log(`published ${published} post(s); ledger: ${LEDGER_FILE}`);
  failIfHeld();
  console.log('done.');
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
