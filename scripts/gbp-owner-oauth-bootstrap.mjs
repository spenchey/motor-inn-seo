#!/usr/bin/env node

import crypto from 'node:crypto';
import fs from 'node:fs';
import http from 'node:http';
import os from 'node:os';
import path from 'node:path';
import { spawn } from 'node:child_process';

const HOME = os.homedir();
const CLIENT_FILE =
  process.env.GBP_OAUTH_CLIENT_FILE ||
  path.join(HOME, '.config', 'openclaw', 'credentials', 'youtube-client-secret.json');
const OUTPUT_FILE =
  process.env.GBP_OWNER_OAUTH_FILE ||
  path.join(HOME, '.config', 'google-business-profile', 'owner-oauth.json');
const EXPECTED_PROJECT = process.env.GBP_EXPECTED_PROJECT || 'jeeves-485623';
const EXPECTED_ACCOUNT = process.env.GBP_EXPECTED_OWNER_ACCOUNT || 'spenchey@gmail.com';
const SCOPES = [
  'openid',
  'email',
  'https://www.googleapis.com/auth/business.manage',
];
const TIMEOUT_MS = 5 * 60 * 1000;

function die(message) {
  console.error(`fatal: ${message}`);
  process.exit(1);
}

function loadClient() {
  if (!fs.existsSync(CLIENT_FILE)) die(`OAuth client file not found: ${CLIENT_FILE}`);
  let parsed;
  try {
    parsed = JSON.parse(fs.readFileSync(CLIENT_FILE, 'utf8'));
  } catch (error) {
    die(`OAuth client file is invalid JSON: ${error.message}`);
  }
  const client = parsed.installed || parsed.web;
  if (!client) die(`${CLIENT_FILE} has neither an installed nor web OAuth client`);
  if (client.project_id !== EXPECTED_PROJECT) {
    die(`OAuth client belongs to ${client.project_id}, not ${EXPECTED_PROJECT}`);
  }
  for (const key of ['client_id', 'client_secret', 'auth_uri', 'token_uri']) {
    if (!client[key]) die(`OAuth client is missing ${key}`);
  }
  return client;
}

function b64url(buffer) {
  return Buffer.from(buffer).toString('base64url');
}

async function fetchJson(url, init) {
  const response = await fetch(url, { ...init, signal: AbortSignal.timeout(30000) });
  const text = await response.text();
  let json = null;
  try {
    json = JSON.parse(text);
  } catch {
    // The caller includes the bounded body in its error.
  }
  return { response, json, text };
}

function waitForCallback(server, expectedState) {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => {
      server.close();
      reject(new Error('OAuth callback timed out after 5 minutes'));
    }, TIMEOUT_MS);
    server.on('request', (request, response) => {
      const url = new URL(request.url, 'http://127.0.0.1');
      if (url.pathname !== '/oauth2/callback') {
        response.writeHead(404).end('Not found');
        return;
      }
      const error = url.searchParams.get('error');
      const state = url.searchParams.get('state');
      const code = url.searchParams.get('code');
      if (error || state !== expectedState || !code) {
        response.writeHead(400, { 'Content-Type': 'text/plain; charset=utf-8' });
        response.end('Authorization failed. Return to the terminal for details.');
        clearTimeout(timer);
        server.close();
        reject(new Error(error || 'OAuth callback state/code validation failed'));
        return;
      }
      response.writeHead(200, { 'Content-Type': 'text/plain; charset=utf-8' });
      response.end('Google Business Profile authorization completed. You can close this tab.');
      clearTimeout(timer);
      server.close();
      resolve(code);
    });
  });
}

async function main() {
  const client = loadClient();
  if (process.argv.includes('--check')) {
    console.log(
      JSON.stringify(
        {
          status: 'ready_for_owner_consent',
          projectId: client.project_id,
          clientId: client.client_id,
          expectedAccount: EXPECTED_ACCOUNT,
          outputFile: OUTPUT_FILE,
          scopes: SCOPES,
        },
        null,
        2
      )
    );
    return;
  }
  const verifier = b64url(crypto.randomBytes(48));
  const challenge = b64url(crypto.createHash('sha256').update(verifier).digest());
  const state = b64url(crypto.randomBytes(24));
  const server = http.createServer();
  await new Promise((resolve, reject) => {
    server.once('error', reject);
    server.listen(0, '127.0.0.1', resolve);
  });
  const address = server.address();
  const redirectUri = `http://127.0.0.1:${address.port}/oauth2/callback`;
  const authUrl = new URL(client.auth_uri);
  authUrl.search = new URLSearchParams({
    client_id: client.client_id,
    redirect_uri: redirectUri,
    response_type: 'code',
    scope: SCOPES.join(' '),
    access_type: 'offline',
    prompt: 'consent',
    include_granted_scopes: 'true',
    login_hint: EXPECTED_ACCOUNT,
    state,
    code_challenge: challenge,
    code_challenge_method: 'S256',
  }).toString();

  console.log(`Authorize the verified primary owner ${EXPECTED_ACCOUNT}:`);
  console.log(authUrl.toString());
  if (!process.argv.includes('--no-open')) {
    const child = spawn('open', [authUrl.toString()], { detached: true, stdio: 'ignore' });
    child.unref();
  }

  const code = await waitForCallback(server, state);
  const tokenBody = new URLSearchParams({
    client_id: client.client_id,
    client_secret: client.client_secret,
    code,
    code_verifier: verifier,
    grant_type: 'authorization_code',
    redirect_uri: redirectUri,
  });
  const tokenResult = await fetchJson(client.token_uri, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: tokenBody,
  });
  if (!tokenResult.response.ok || !tokenResult.json?.access_token) {
    die(`token exchange failed: HTTP ${tokenResult.response.status} ${tokenResult.text.slice(0, 300)}`);
  }
  if (!tokenResult.json.refresh_token) {
    die('Google did not return a refresh token; revoke prior consent and run again with prompt=consent');
  }

  const userResult = await fetchJson('https://openidconnect.googleapis.com/v1/userinfo', {
    headers: { Authorization: `Bearer ${tokenResult.json.access_token}` },
  });
  if (!userResult.response.ok || !userResult.json?.email) {
    die(`could not verify OAuth account: HTTP ${userResult.response.status}`);
  }
  if (userResult.json.email.toLowerCase() !== EXPECTED_ACCOUNT.toLowerCase()) {
    die(`authorized ${userResult.json.email}, expected primary owner ${EXPECTED_ACCOUNT}; no file written`);
  }

  const credentials = {
    type: 'authorized_user',
    project_id: client.project_id,
    client_id: client.client_id,
    client_secret: client.client_secret,
    refresh_token: tokenResult.json.refresh_token,
    token_uri: client.token_uri,
    scopes: SCOPES,
    account_email: userResult.json.email,
    authorized_at: new Date().toISOString(),
  };
  fs.mkdirSync(path.dirname(OUTPUT_FILE), { recursive: true, mode: 0o700 });
  const temp = `${OUTPUT_FILE}.tmp-${process.pid}`;
  fs.writeFileSync(temp, `${JSON.stringify(credentials, null, 2)}\n`, { mode: 0o600 });
  fs.renameSync(temp, OUTPUT_FILE);
  fs.chmodSync(OUTPUT_FILE, 0o600);
  console.log(`Stored primary-owner OAuth at ${OUTPUT_FILE} (mode 600).`);
  console.log('No Business Profile data was changed.');
}

main().catch((error) => die(error?.stack || String(error)));
