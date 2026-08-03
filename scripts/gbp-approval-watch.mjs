#!/usr/bin/env node
/**
 * gbp-approval-watch.mjs
 *
 * Daily watcher: detects the moment Google approves Google Business Profile
 * (GBP) API access for the SEO service account, stages publisher credentials,
 * and notifies #mission-control. Staging access must not enable live posting;
 * live GBP actions require separate Spencer Slack approval evidence.
 *
 * Deterministic, node stdlib only, fail-loud, fire-once (idempotent).
 *
 * Approval probe:
 *   Mint a business.manage RS256-JWT token from the SA at
 *   ~/.config/gcloud/ga4-service-account.json (project jeeves-485623) and GET
 *   https://mybusinessaccountmanagement.googleapis.com/v1/accounts.
 *     HTTP 200                -> APPROVED. Wire + notify + write state, ONCE.
 *     HTTP 429 quota error    -> still pending. Record status and review age.
 *     HTTP 401/403/other 4xx  -> auth/config failure. Fail loud.
 *     Network/5xx             -> retry, then fail loud.
 *   (Google grants quota=0 -> HTTP 429 until the access-request form is
 *   approved; the SA can always mint a token regardless, so a token-grant
 *   failure is a genuine error and fails loud.)
 *
 * On approval it writes a staged credentials file (chmod 600):
 *   ~/.config/google-business-profile/credentials.pending-live-approval.json
 *     {
 *       "credentials":  <full service-account JSON>,
 *       "account_id":   "accounts/<id>",
 *       "location_ids": ["locations/<id>", ...]
 *     }
 * It does NOT write the canonical credentials.json file consumed by the live
 * publisher. It posts to Slack #mission-control and writes a fire-once access
 * state file so it never re-fires:
 *   ~/.config/google-business-profile/.api-approved
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
const STAGED_CREDS_FILE =
  process.env.GBP_STAGED_CREDS_FILE ||
  path.join(GBP_DIR, 'credentials.pending-live-approval.json');
const STATE_FILE = path.join(GBP_DIR, '.approved');
const ACCESS_STATE_FILE = path.join(GBP_DIR, '.api-approved');
const STATUS_FILE = path.join(GBP_DIR, 'approval-status.json');
const OVERDUE_ALERT_FILE = path.join(GBP_DIR, '.approval-overdue-alerted');
const CLAWD_ENV = path.join(HOME, 'clawd', '.env');
const SLACK_CHANNEL = process.env.GBP_WATCH_SLACK_CHANNEL || 'C0AMAMSDCVC'; // #mission-control
const APPLICATION_SUBMITTED_AT = process.env.GBP_APPLICATION_SUBMITTED_AT || '2026-07-27';
const REVIEW_WINDOW_DAYS = Number(process.env.GBP_REVIEW_WINDOW_DAYS || 14);

const SCOPE = 'https://www.googleapis.com/auth/business.manage';
const ACCT_MGMT_BASE = 'https://mybusinessaccountmanagement.googleapis.com/v1';
const BIZ_INFO_BASE = 'https://mybusinessbusinessinformation.googleapis.com/v1';
const TIMEOUT_MS = 30000;
const FETCH_ATTEMPTS = Number(process.env.GBP_WATCH_FETCH_ATTEMPTS || 3);
const FETCH_RETRY_BASE_MS = Number(process.env.GBP_WATCH_RETRY_BASE_MS || 750);

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

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function shouldRetryStatus(status) {
  return status === 408 || status === 500 || status === 502 || status === 503 || status === 504;
}

async function fetchRaw(url, init = {}) {
  let lastError = null;
  for (let attempt = 1; attempt <= FETCH_ATTEMPTS; attempt += 1) {
    try {
      const res = await fetch(url, { ...init, signal: AbortSignal.timeout(TIMEOUT_MS) });
      const text = await res.text();
      let json = null;
      try {
        json = JSON.parse(text);
      } catch {
        /* non-JSON body — callers key off status */
      }
      if (!shouldRetryStatus(res.status) || attempt === FETCH_ATTEMPTS) {
        return { res, json, text };
      }
      lastError = new Error(`HTTP ${res.status}: ${text.slice(0, 160)}`);
    } catch (error) {
      lastError = error;
      if (attempt === FETCH_ATTEMPTS) break;
    }
    await sleep(FETCH_RETRY_BASE_MS * attempt);
  }
  throw new Error(`request failed after ${FETCH_ATTEMPTS} attempts: ${lastError?.message || 'unknown error'}`);
}

function isPendingQuotaResponse(probe) {
  if (probe.res.status !== 429) return false;
  const reason = String(probe.json?.error?.status || '').toUpperCase();
  const message = String(probe.json?.error?.message || probe.text || '').toLowerCase();
  return (
    reason === 'RESOURCE_EXHAUSTED' ||
    message.includes('quota exceeded') ||
    message.includes('quota metric') ||
    message.includes('requests per minute')
  );
}

function reviewAge() {
  const submittedAt = new Date(`${APPLICATION_SUBMITTED_AT}T00:00:00-05:00`);
  if (Number.isNaN(submittedAt.getTime())) {
    die(`invalid GBP_APPLICATION_SUBMITTED_AT: ${APPLICATION_SUBMITTED_AT}`);
  }
  const elapsedDays = Math.max(0, Math.floor((Date.now() - submittedAt.getTime()) / 86400000));
  const deadline = new Date(submittedAt.getTime() + REVIEW_WINDOW_DAYS * 86400000);
  return { elapsedDays, deadline: deadline.toISOString() };
}

function writeStatus(status) {
  fs.mkdirSync(GBP_DIR, { recursive: true, mode: 0o700 });
  const tmp = `${STATUS_FILE}.tmp-${process.pid}`;
  fs.writeFileSync(tmp, JSON.stringify({ checkedAt: ts(), ...status }, null, 2) + '\n', {
    mode: 0o600,
  });
  fs.renameSync(tmp, STATUS_FILE);
  fs.chmodSync(STATUS_FILE, 0o600);
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

function writeCredsFile(sa, accountId, locationIds, destination) {
  fs.mkdirSync(GBP_DIR, { recursive: true, mode: 0o700 });
  try {
    fs.chmodSync(GBP_DIR, 0o700);
  } catch {
    /* best effort */
  }
  const creds = { credentials: sa, account_id: accountId, location_ids: locationIds };
  const tmp = `${destination}.tmp-${process.pid}`;
  fs.writeFileSync(tmp, JSON.stringify(creds, null, 2) + '\n', { mode: 0o600 });
  fs.chmodSync(tmp, 0o600);
  fs.renameSync(tmp, destination); // atomic swap into place
  fs.chmodSync(destination, 0o600);
}

async function main() {
  // 1. Fire-once guards: a legacy/live wire or a completed access staging run
  //    means there is no reason to probe Google again.
  if (fs.existsSync(STATE_FILE)) {
    log(`already wired (state file ${STATE_FILE} exists) — nothing to do.`);
    return;
  }
  if (fs.existsSync(ACCESS_STATE_FILE)) {
    log(
      `API access already approved and credentials staged at ${STAGED_CREDS_FILE}; ` +
        'live publisher remains blocked pending Spencer Slack approval.'
    );
    return;
  }

  const sa = loadServiceAccount();
  const token = await mintToken(sa);

  // 2. Approval probe. Only an explicit quota-exhausted 429 is pending. Other
  //    statuses are auth/config/runtime failures and must not be hidden.
  const probe = await fetchRaw(`${ACCT_MGMT_BASE}/accounts`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (isPendingQuotaResponse(probe)) {
    const reason = String(probe.json?.error?.message || probe.text || 'quota pending').slice(0, 300);
    const age = reviewAge();
    const overdue = age.elapsedDays >= REVIEW_WINDOW_DAYS;
    writeStatus({
      status: overdue ? 'approval_overdue' : 'approval_pending',
      httpStatus: probe.res.status,
      reason,
      projectId: sa.project_id || null,
      projectNumber: '53355027587',
      applicationSubmittedAt: APPLICATION_SUBMITTED_AT,
      reviewWindowDays: REVIEW_WINDOW_DAYS,
      elapsedDays: age.elapsedDays,
      reviewDeadline: age.deadline,
      publisherWired: false,
    });
    log(
      `GBP ${overdue ? 'approval overdue' : 'still pending'} (HTTP 429, ` +
        `${age.elapsedDays}/${REVIEW_WINDOW_DAYS} review days elapsed) — publisher not wired.`
    );
    if (overdue && !fs.existsSync(OVERDUE_ALERT_FILE)) {
      const notice =
        `:warning: GBP API approval is overdue. Project jeeves-485623 / 53355027587 ` +
        `still has zero quota ${age.elapsedDays} days after the ${APPLICATION_SUBMITTED_AT} ` +
        `application. Reopen Google's Basic API Access case using a verified GBP manager ` +
        `business email and confirm the project number.`;
      const slack = await slackNotify(notice);
      if (slack.ok) {
        fs.writeFileSync(OVERDUE_ALERT_FILE, `${ts()}\n`, { mode: 0o600 });
        log('posted one-time overdue approval notice to Slack #mission-control.');
      } else {
        log(`overdue approval notice was not posted (${slack.reason}); will retry next run.`);
      }
    }
    return;
  }
  if (probe.res.status !== 200) {
    const reason = String(probe.json?.error?.message || probe.text || 'unknown response').slice(0, 300);
    writeStatus({
      status: 'auth_or_configuration_failure',
      httpStatus: probe.res.status,
      reason,
      projectId: sa.project_id || null,
      projectNumber: '53355027587',
      publisherWired: false,
    });
    die(`GBP approval probe failed: HTTP ${probe.res.status} ${reason}`);
  }

  // 3. APPROVED. Resolve account + location(s), wire, notify, mark once.
  log('accounts.list returned HTTP 200 — GBP API access is APPROVED. Wiring the publisher.');
  writeStatus({
    status: 'api_approved_resolving_accounts',
    httpStatus: 200,
    projectId: sa.project_id || null,
    projectNumber: '53355027587',
    publisherWired: false,
  });
  const accounts = (probe.json && probe.json.accounts) || [];
  if (accounts.length === 0) {
    // Approved quota, but the SA sees no Business Profile yet (Manager access
    // not propagated). Do NOT wire/alert/mark — re-check next run. Cron-log only.
    log(
      'APPROVED but 0 Business Profile accounts are visible to the service account. ' +
        'The SA email must be a Manager of the Motor Inn profile (or access has not ' +
        'propagated yet). Not wiring; will re-check on the next daily run.'
    );
    writeStatus({
      status: 'api_approved_manager_access_missing',
      httpStatus: 200,
      projectId: sa.project_id || null,
      projectNumber: '53355027587',
      serviceAccount: sa.client_email,
      publisherWired: false,
    });
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

  // 4. Stage credentials in the exact publisher shape, but deliberately do
  //    not create the canonical credentials.json live-action trigger.
  writeCredsFile(sa, accountId, locationIds, STAGED_CREDS_FILE);
  log(
    `staged GBP credentials -> ${STAGED_CREDS_FILE} (mode 600); account ${accountId}, ` +
      `location(s) ${locationIds.join(', ')}. Live publisher remains blocked.`
  );

  // 5. Notify #mission-control (best-effort; access staging already done).
  const msg =
    `:white_check_mark: GBP API APPROVED and access credentials staged. Account ${accountId}, ` +
    `location(s) ${locationIds.join(', ')}. Live GBP publishing is still BLOCKED. ` +
    `Spencer Slack approval and per-post approval enforcement are required before activation.`;
  const slack = await slackNotify(msg);
  if (slack.ok) {
    log('posted approval notice to Slack #mission-control.');
  } else {
    log(
      `Slack notice NOT posted (${slack.reason}). Access is staged and live publishing is still blocked; the ` +
        `access state below records approval and this cron log has the details.`
    );
  }

  // 6. Fire-once access state, written last. This is intentionally distinct
  //    from .approved, which historically meant the live publisher was wired.
  const state = {
    approvedAt: ts(),
    account_id: accountId,
    location_ids: locationIds,
    staged_creds_file: STAGED_CREDS_FILE,
    slack_notified: slack.ok,
    accounts_seen: seen,
    publisher_wired: false,
    approval_needed: 'Spencer Slack live-action approval plus per-post gate',
  };
  fs.writeFileSync(ACCESS_STATE_FILE, JSON.stringify(state, null, 2) + '\n', { mode: 0o600 });
  fs.chmodSync(ACCESS_STATE_FILE, 0o600);
  writeStatus({
    status: 'api_approved_access_staged_live_action_blocked',
    httpStatus: 200,
    projectId: sa.project_id || null,
    projectNumber: '53355027587',
    accountId,
    locationIds,
    stagedCredentialsFile: STAGED_CREDS_FILE,
    publisherWired: false,
    approvalNeeded: true,
  });
  log(`wrote fire-once access state ${ACCESS_STATE_FILE} — watcher will not re-fire.`);
}

main().catch((err) => die(err?.stack || String(err)));
