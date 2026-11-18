import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

const SCRIPT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../scripts/publish-gbp-posts.mjs');
const PAST = '2020-01-07';
const FUTURE = '2099-01-07';
const OLD_FILE = 'posts-week-of-2020-01-01.md';
const NEW_FILE = 'posts-week-of-2020-02-01.md';

function post(number, title, date, { approved = false, malformed = false } = {}) {
  return [
    `### Post ${number}: ${title}`,
    '**Type:** update',
    `**Publish date:** ${date}`,
    ...(approved ? ['**Approval:** approved — Spencer, 2020-01-01 09:00 CT'] : []),
    '',
    '**Copy:**',
    'A short test post about winter service.',
    '',
    ...(malformed ? [] : ['**CTA button:** Call Now', '**CTA link:** tel:7127925000']),
    '',
    '---',
    '',
  ].join('\n');
}

function setup(files, ledger = {}) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'gbp-publisher-test-'));
  const drafts = path.join(root, 'content', 'drafts', 'gbp-posts');
  fs.mkdirSync(path.join(root, 'scripts'), { recursive: true });
  fs.mkdirSync(drafts, { recursive: true });
  fs.copyFileSync(SCRIPT, path.join(root, 'scripts', 'publish-gbp-posts.mjs'));
  fs.writeFileSync(path.join(root, 'config.json'), JSON.stringify({ location_ids: ['locations/1'] }));
  fs.writeFileSync(path.join(drafts, 'published-state.json'), JSON.stringify(ledger));
  for (const [name, body] of Object.entries(files)) fs.writeFileSync(path.join(drafts, name), `# Drafts\n\n${body}`);
  return { root, drafts };
}

function run({ root }, ...args) {
  return spawnSync(process.execPath, [path.join(root, 'scripts', 'publish-gbp-posts.mjs'), ...args], {
    encoding: 'utf8',
    env: { ...process.env, GBP_CREDS_FILE: path.join(root, 'config.json') },
  });
}

test('an approved post in an older file still publishes after a newer file appears', () => {
  const ctx = setup({
    [OLD_FILE]: post(1, 'Old Approved', PAST, { approved: true }),
    [NEW_FILE]: post(1, 'New Pending', FUTURE),
  });
  const out = run(ctx, '--dry-run');
  assert.equal(out.status, 0, out.stderr);
  assert.match(out.stdout, /-> \[2020-01-07\] "Old Approved"/);
});

test('an unapproved post never publishes from any file', () => {
  const ctx = setup({
    [OLD_FILE]: post(1, 'Old Approved', PAST, { approved: true }) + post(2, 'Old Pending', PAST),
    [NEW_FILE]: post(1, 'New Pending', PAST),
  });
  const out = run(ctx, '--dry-run');
  assert.equal(out.status, 0, out.stderr);
  assert.doesNotMatch(out.stdout, /-> .*Old Pending/);
  assert.doesNotMatch(out.stdout, /-> .*New Pending/);
  assert.match(out.stdout, /2 due but NOT approved/);
});

test('an older file with no approvals is ignored even if malformed', () => {
  const ctx = setup({
    [OLD_FILE]: post(1, 'Broken Old Draft', PAST, { malformed: true }),
    [NEW_FILE]: post(1, 'New Approved', PAST, { approved: true }),
  });
  const out = run(ctx, '--dry-run');
  assert.equal(out.status, 0, out.stderr);
  assert.match(out.stdout, /-> \[2020-01-07\] "New Approved"/);
  assert.match(out.stdout, new RegExp(`publish sources: ${NEW_FILE}\\n`));
});

test('a malformed older file holding an approval fails loud', () => {
  const ctx = setup({
    [OLD_FILE]: post(1, 'Broken Approved', PAST, { approved: true, malformed: true }),
    [NEW_FILE]: post(1, 'New Pending', FUTURE),
  });
  const out = run(ctx, '--dry-run');
  assert.equal(out.status, 1);
  assert.match(out.stderr, /fatal: /);
});

test('a post already in the ledger is not published again', () => {
  const key = 'posts-week-of-2020-01-01::Old Approved::locations/1';
  const ctx = setup(
    { [OLD_FILE]: post(1, 'Old Approved', PAST, { approved: true }), [NEW_FILE]: post(1, 'New Pending', FUTURE) },
    { [key]: { publishedAt: '2020-01-07T12:00:00Z' } }
  );
  const out = run(ctx, '--dry-run');
  assert.equal(out.status, 0, out.stderr);
  assert.match(out.stdout, /publishing 0 this run/);
});

test('an approved post is held until its publish date', () => {
  const ctx = setup({
    [OLD_FILE]: post(1, 'Future Approved', FUTURE, { approved: true }),
    [NEW_FILE]: post(1, 'New Pending', FUTURE),
  });
  const out = run(ctx, '--dry-run');
  assert.equal(out.status, 0, out.stderr);
  assert.match(out.stdout, /publishing 0 this run/);
});

test('--approve marks the newest file by default', () => {
  const ctx = setup({ [OLD_FILE]: post(1, 'Old Pending', FUTURE), [NEW_FILE]: post(1, 'New Pending', FUTURE) });
  const out = run(ctx, '--approve', '1', '--approved-by', 'Spencer');
  assert.equal(out.status, 0, out.stderr);
  assert.match(out.stdout, /Post 1: New Pending/);
  assert.match(fs.readFileSync(path.join(ctx.drafts, NEW_FILE), 'utf8'), /\*\*Approval:\*\* approved — Spencer/);
  assert.doesNotMatch(fs.readFileSync(path.join(ctx.drafts, OLD_FILE), 'utf8'), /\*\*Approval:\*\*/);
});

test('--approve --file marks only the named older file', () => {
  const ctx = setup({ [OLD_FILE]: post(1, 'Old Pending', FUTURE), [NEW_FILE]: post(1, 'New Pending', FUTURE) });
  const out = run(ctx, '--approve', '1', '--approved-by', 'Spencer', '--file', OLD_FILE);
  assert.equal(out.status, 0, out.stderr);
  assert.match(out.stdout, /Post 1: Old Pending/);
  assert.match(fs.readFileSync(path.join(ctx.drafts, OLD_FILE), 'utf8'), /\*\*Approval:\*\* approved — Spencer/);
  assert.doesNotMatch(fs.readFileSync(path.join(ctx.drafts, NEW_FILE), 'utf8'), /\*\*Approval:\*\*/);
});

test('--list-pending --file lists the named file', () => {
  const ctx = setup({ [OLD_FILE]: post(1, 'Old Pending', FUTURE), [NEW_FILE]: post(1, 'New Pending', FUTURE) });
  const out = run(ctx, '--list-pending', '--file', OLD_FILE);
  assert.equal(out.status, 0, out.stderr);
  assert.match(out.stdout, /Old Pending/);
  assert.doesNotMatch(out.stdout, /New Pending/);
});

test('--file refuses bad names and refuses to steer publishing', () => {
  const ctx = setup({ [NEW_FILE]: post(1, 'New Pending', FUTURE) });
  for (const name of ['../../config.json', 'published-state.json', 'posts-week-of-2031-01-01.md']) {
    assert.equal(run(ctx, '--list-pending', '--file', name).status, 1, name);
  }
  assert.equal(run(ctx, '--dry-run', '--file', NEW_FILE).status, 1);
});
