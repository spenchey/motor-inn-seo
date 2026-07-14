#!/usr/bin/env node
/**
 * gbp-approval-watch.mjs
 *
 * Daily watcher: detects the moment Google approves Google Business Profile
 * (GBP) API access for the SEO service account, then AUTO-WIRES the existing
 * publisher (scripts/publish-gbp-posts.mjs) and notifies #mission-control so
 * nobody has to keep manually re-checking the access-request status.
 *
 * Deterministic, node stdlib only, fail-loud, fire-once (idempotent).
 *
 * Approval probe:
 *   Mint a business.manage RS256-JWT token from the SA at
 *   ~/.config/gcloud/ga4-service-account.json (project jeeves-485623) and GET
 *   https://mybusinessaccountmanagement.googleapis.com/v1/accounts.
 *     HTTP 200                -> APPROVED. Wire + notify + write state, ONCE.
 *     HTTP 429 / any non-200  -> still pending. Log quietly, exit 0. NO alert.
 *   (Google grants quota=0 -> HTTP 429 until the access-request form is
 *   approved; the SA can always mint a token regardless, so a token-grant
 *   failure is a genuine error and fails loud.)
 *
 * On approval it writes the creds file publish-gbp-posts.mjs expects (verified
 * against that script's loadConfig/getAccessToken/normalizeParent):
 *   ~/.config/google-business-profile/credentials.json   (chmod 600)
 *     {
 *       "credentials":  <full service-account JSON>,
 *       "account_id":   "accounts/<id>",
 *       "location_ids": ["locations/<id>", ...]
 *     }
 * posts to Slack #mission-control (chat.postMessage, SLACK_BOT_TOKEN from
 * ~/clawd/.env — the fleet's slack-notify.mjs pattern), and writes a fire-once
 * state file so it never re-fires:
 *   ~/.config/google-business-profile/.approved
 *
 * Scheduled daily 08:05 America/Chicago on the Mac mini. MOT-2445.
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';

const HOME = os.homedir();
const SA_FILE =
  process.env.GBP_SA_FILE ||
  path.join(HOME, '.config', 'gcloud', 'ga4-service-account.json');
const GBP_DIR = path.join(HOME, '.config', 'google-business-profile');
const CREDS_FILE = process.env.GBP_CREDS_FILE || path.join(GBP_DIR, 'credentials.json');
const STATE_FILE = path.join(GBP_DIR, '.approved');
const CLAWD_ENV = path.join(HOME, 'clawd', '.env');
const SLACK_CHANNEL = process.env.GBP_WATCH_SLACK_CHANNEL || 'C0AMAMSDCVC'; // #mission-control

const SCOPE = 'https://www.googleapis.com/auth/business.manage';
const ACCT_MGMT_BASE = 'https://mybusinessaccountmanagement.googleapis.com/v1';
const BIZ_INFO_BASE = 'https://mybusinessbusinessinformation.googleapis.com/v1';
const TIMEOUT_MS = 30000;

function ts() {
  return new Date().toISOString();
}
function log(msg) {
  console.log(`[${ts()}] gbp-approval-watch: ${msg}`);
}
function die(msg, code = 1) {
  console.error(`[${ts()}] gbp-approval-watch FATAL: ${msg}`);
  process.exit(code);
}
function b64url(buf) {
  return Buffer.from(buf).toString('base64url');
}

async function fetchRaw(url, init = {}) {
  const res = await fetch(url, { ...init, signal: AbortSignal.timeout(TIMEOUT_MS) });
  const text = await res.text();
  let json = null;
  try {
    json = JSON.parse(text);
  } catch {
    /* non-JSON body — callers key off status */
  }
  return { res, json, text };
}

function loadServiceAccount() {
  if (!fs.existsSync(SA_FILE)) die(`service account file not found: ${SA_FILE}`);
  let sa;
  try {
    sa = JSON.parse(fs.readFileSync(SA_FILE, 'utf8'));
  } catch (e) {
    die(`service account file is not valid JSON: ${SA_FILE} (${e.message})`);
  }
  if (sa.type !== 'service_account') {
    die(`${SA_FILE} is not a service_account key (type=${sa.type})`);
  }
  for (const k of ['client_email', 'private_key', 'token_uri']) {
    if (!sa[k]) die(`service account file ${SA_FILE} is missing "${k}"`);
  }
  return sa;
}

// Mint a business.manage access token from the SA (RS256 JWT -> token_uri).
// Mirrors publish-gbp-posts.mjs getAccessToken() exactly.
async function mintToken(sa) {
  const now = Math.floor(Date.now() / 1000);
  const header = b64url(JSON.stringify({ alg: 'RS256', typ: 'JWT' }));
  const claims = b64url(
    JSON.stringify({
      iss: sa.client_email,
      scope: SCOPE,
      aud: sa.token_uri,
      iat: now,
      exp: now + 3600,
    })
  );
  const signingInput = `${header}.${claims}`;
  const signature = crypto
    .sign('RSA-SHA256', Buffer.from(signingInput), sa.private_key)
    .toString('base64url');
  const body = new URLSearchParams({
    grant_type: 'urn:ietf:params:oauth:grant-type:jwt-bearer',
    assertion: `${signingInput}.${signature}`,
  });
  const { res, json, text } = await fetchRaw(sa.token_uri, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body,
  });
  // Token minting does NOT depend on GBP approval — a failure here is a real
  // error (bad key / clock skew / network), so fail loud rather than treating
  // it as "pending".
  if (!res.ok || !json?.access_token) {
    die(`service-account token grant failed: HTTP ${res.status} ${text.slice(0, 300)}`);
  }
  return json.access_token;
}

// Read one KEY=value from a .env file (stdlib only; handles export/quotes and
// trailing inline comments on unquoted values). No dependency on a sourced env.
function readEnvVar(file, name) {
  if (!fs.existsSync(file)) return null;
  const txt = fs.readFileSync(file, 'utf8');
  const m = txt.match(new RegExp(`^(?:export\\s+)?${name}\\s*=\\s*(.*)$`, 'm'));
  if (!m) return null;
  let v = m[1].trim();
  if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) {
    return v.slice(1, -1) || null;
  }
  v = v.split(/\s+/)[0]; // drop any trailing inline comment on an unquoted value
  return v || null;
}

// Post to Slack via chat.postMessage (the fleet's slack-notify.mjs mechanism).
// Best-effort: never throws; wiring must not depend on Slack being reachable.
async function slackNotify(text) {
  const token = process.env.SLACK_BOT_TOKEN || readEnvVar(CLAWD_ENV, 'SLACK_BOT_TOKEN');
  if (!token) return { ok: false, reason: `no SLACK_BOT_TOKEN (env or ${CLAWD_ENV})` };
  try {
    const res = await fetch('https://slack.com/api/chat.postMessage', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ channel: SLACK_CHANNEL, text }),
      signal: AbortSignal.timeout(TIMEOUT_MS),
    });
    const json = await res.json();
    if (!json.ok) return { ok: false, reason: `slack api error: ${json.error}` };
    return { ok: true };
  } catch (e) {
    return { ok: false, reason: `network error: ${e.message}` };
  }
}

async function gbpGet(token, url, context) {
  const { res, json, text } = await fetchRaw(url, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) die(`${context}: HTTP ${res.status} ${text.slice(0, 300)}`);
  return json;
}

function writeCredsFile(sa, accountId, locationIds) {
  fs.mkdirSync(GBP_DIR, { recursive: true, mode: 0o700 });
  try {
    fs.chmodSync(GBP_DIR, 0o700);
  } catch {
    /* best effort */
  }
  const creds = { credentials: sa, account_id: accountId, location_ids: locationIds };
  const tmp = `${CREDS_FILE}.tmp-${process.pid}`;
  fs.writeFileSync(tmp, JSON.stringify(creds, null, 2) + '\n', { mode: 0o600 });
  fs.chmodSync(tmp, 0o600);
  fs.renameSync(tmp, CREDS_FILE); // atomic swap into place
  fs.chmodSync(CREDS_FILE, 0o600);
}

async function main() {
  // 1. Fire-once guard: already wired -> exit immediately, no network calls.
  if (fs.existsSync(STATE_FILE)) {
    log(`already wired (state file ${STATE_FILE} exists) — nothing to do.`);
    return;
  }

  const sa = loadServiceAccount();
  const token = await mintToken(sa);

  // 2. Approval probe. Per contract: ONLY HTTP 200 means approved; 429 (quota=0)
  //    and every other non-200 mean "still pending" -> quiet exit 0 (runs daily,
  //    must never spam).
  const probe = await fetchRaw(`${ACCT_MGMT_BASE}/accounts`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (probe.res.status !== 200) {
    const reason = probe.json?.error?.message
      ? ` — ${String(probe.json.error.message).slice(0, 160)}`
      : '';
    log(`GBP still pending (HTTP ${probe.res.status})${reason} — no action, publisher not wired.`);
    return;
  }

  // 3. APPROVED. Resolve account + location(s), wire, notify, mark once.
  log('accounts.list returned HTTP 200 — GBP API access is APPROVED. Wiring the publisher.');
  const accounts = (probe.json && probe.json.accounts) || [];
  if (accounts.length === 0) {
    // Approved quota, but the SA sees no Business Profile yet (Manager access
    // not propagated). Do NOT wire/alert/mark — re-check next run. Cron-log only.
    log(
      'APPROVED but 0 Business Profile accounts are visible to the service account. ' +
        'The SA email must be a Manager of the Motor Inn profile (or access has not ' +
        'propagated yet). Not wiring; will re-check on the next daily run.'
    );
    return;
  }

  // Pick the first account that owns at least one location.
  let chosen = null;
  const seen = [];
  for (const a of accounts) {
    const locsResp = await gbpGet(
      token,
      `${BIZ_INFO_BASE}/${a.name}/locations?readMask=name,title,storefrontAddress&pageSize=100`,
      `list locations for ${a.name}`
    );
    const locs = (locsResp.locations || []).map((l) => l.name).filter(Boolean);
    seen.push(`${a.name} (${a.accountName || a.type || ''}) -> ${locs.length} location(s)`);
    if (!chosen && locs.length > 0) chosen = { account: a.name, locations: locs };
  }

  if (!chosen) {
    log(
      'APPROVED and account(s) visible, but 0 locations were returned [' +
        seen.join('; ') +
        ']. Cannot wire without a location_id; not wiring. Will re-check on the next daily run.'
    );
    return;
  }

  const accountId = chosen.account; // "accounts/<id>"
  const locationIds = chosen.locations; // ["locations/<id>", ...]

  // 4. Write the creds file in the EXACT shape publish-gbp-posts.mjs expects.
  writeCredsFile(sa, accountId, locationIds);
  log(
    `wrote GBP credentials -> ${CREDS_FILE} (mode 600); account ${accountId}, ` +
      `location(s) ${locationIds.join(', ')}.`
  );

  // 5. Notify #mission-control (best-effort; wiring already done).
  const msg =
    `:white_check_mark: GBP API APPROVED + publisher wired. Account ${accountId}, ` +
    `location(s) ${locationIds.join(', ')}. Rory's weekly GBP posts will begin on the Monday cron.`;
  const slack = await slackNotify(msg);
  if (slack.ok) {
    log('posted approval notice to Slack #mission-control.');
  } else {
    log(
      `Slack notice NOT posted (${slack.reason}). Publisher is wired regardless; the ` +
        `state file below records the approval and this cron log has the details.`
    );
  }

  // 6. Fire-once state file, written last (after a successful wire).
  const state = {
    approvedAt: ts(),
    account_id: accountId,
    location_ids: locationIds,
    creds_file: CREDS_FILE,
    slack_notified: slack.ok,
    accounts_seen: seen,
  };
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2) + '\n');
  log(`wrote fire-once state file ${STATE_FILE} — watcher will not re-fire.`);
}

main().catch((err) => die(err?.stack || String(err)));
