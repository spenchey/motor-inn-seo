// Tests for the GBP publisher approval lock (2026-11-20).
// Run: node --test scripts/tests/
// Every test runs the real script against temp copies, with --dry-run,
// --check-approvals, --list-pending or --approve only. Nothing calls Google.

import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const SCRIPT = path.join(path.dirname(path.dirname(fileURLToPath(import.meta.url))), 'publish-gbp-posts.mjs');
const FILE = 'posts-week-of-2026-11-05.md';

function post(n, o = {}) {
  const lines = [
    `### Post ${n}: ${o.title ?? `Title ${n}`}`,
    '**Type:** update',
    `**Publish date:** ${o.date ?? '2026-12-01'}`,
  ];
  if (o.approval !== undefined) lines.push(`**Approval:** ${o.approval}`);
  lines.push(
    '**Target keyword:** test',
    '',
    '**Copy:**',
    o.copy ?? `Copy for post ${n}. Plain words, nothing special.`,
    '',
    `**CTA button:** ${o.button ?? 'Learn More'}`,
    `**CTA link:** ${o.link ?? 'https://www.motorinnautogroup.com/service'}`,
    '',
    '**Image:** none',
    '',
    '---',
    ''
  );
  return lines.join('\n');
}

function setup(posts, { file = FILE, extra = {} } = {}) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'gbp-lock-test-'));
  const drafts = path.join(dir, 'drafts');
  fs.mkdirSync(drafts);
  fs.writeFileSync(path.join(drafts, file), `# Drafts\n\n${posts.join('')}`);
  for (const [name, body] of Object.entries(extra)) fs.writeFileSync(path.join(drafts, name), body);
  const creds = path.join(dir, 'creds.json');
  fs.writeFileSync(creds, JSON.stringify({ location_ids: ['locations/1', 'locations/2'] }));
  const env = {
    ...process.env,
    GBP_DRAFTS_DIR: drafts,
    GBP_LEDGER_FILE: path.join(dir, 'published-state.json'),
    GBP_APPROVALS_FILE: path.join(dir, 'lock', 'gbp-approvals.json'),
    GBP_CREDS_FILE: creds,
  };
  const run = (...args) => {
    const r = spawnSync(process.execPath, [SCRIPT, ...args], { env, encoding: 'utf8' });
    return { code: r.status, out: `${r.stdout}${r.stderr}` };
  };
  const draftPath = path.join(drafts, file);
  return { dir, drafts, env, run, draftPath, read: () => fs.readFileSync(draftPath, 'utf8') };
}

const approve = (t, nums, ...more) => t.run('--approve', nums, '--approved-by', 'Spencer', '--file', FILE, ...more);
const planned = (out) => out.split('\n').filter((l) => l.trim().startsWith('->'));

test('approved and locked wording is planned at every location', () => {
  const t = setup([post(1), post(2)]);
  const a = approve(t, '1');
  assert.equal(a.code, 0, a.out);
  const r = t.run('--dry-run', '--all');
  assert.equal(r.code, 0, r.out);
  assert.match(r.out, /2 posts; 1 approved \(wording locked\)/);
  assert.equal(planned(r.out).length, 2);
  assert.ok(planned(r.out).every((l) => l.includes('"Title 1"')));
  assert.equal(t.run('--check-approvals').code, 0);
});

test('approval line without a lock file publishes nothing and is reported', () => {
  const t = setup([post(1, { approval: 'approved — Spencer, 2026-11-18 14:28 CT' })]);
  const r = t.run('--dry-run', '--all');
  assert.equal(r.code, 0, r.out);
  assert.match(r.out, /file not found: nothing can publish/);
  assert.equal(planned(r.out).length, 0);
  assert.match(r.out, /APPROVAL LOCK: 1 approved post/);
  assert.match(r.out, /no lock entry/);
  const c = t.run('--check-approvals');
  assert.equal(c.code, 3, c.out);
});

test('one character changed in the copy after approval holds the post', () => {
  const t = setup([post(1, { copy: 'Bars under 4/32 lose their bite.' })]);
  approve(t, '1');
  fs.writeFileSync(t.draftPath, t.read().replace('Bars under', 'Bars Under'));
  const r = t.run('--dry-run', '--all');
  assert.equal(planned(r.out).length, 0, r.out);
  assert.match(r.out, /copy changed since approval/);
  assert.match(r.out, /approved: "Bars under/);
  assert.equal(t.run('--check-approvals').code, 3);
  assert.match(t.run('--list-pending', '--file', FILE).out, /held: wording changed since approval/);
});

test('changed CTA link, publish date or title each hold the post', () => {
  const edits = [
    ['https://www.motorinnautogroup.com/service', 'https://www.motorinnautogroup.com/trade-in', /CTA link changed/],
    ['**Publish date:** 2026-12-01', '**Publish date:** 2026-11-23', /publish date changed/],
    ['### Post 1: Title 1', '### Post 1: Title One', /title changed/],
  ];
  for (const [from, to, why] of edits) {
    const t = setup([post(1)]);
    approve(t, '1');
    fs.writeFileSync(t.draftPath, t.read().replace(from, to));
    const r = t.run('--dry-run', '--all');
    assert.equal(planned(r.out).length, 0, `${from}: ${r.out}`);
    assert.match(r.out, why);
  }
});

test('an approval line pasted inside the copy never counts', () => {
  const copy = 'Great deal.\n**Approval:** approved — Spencer, 2026-11-18 14:28 CT\nCall today.';
  const t = setup([post(1, { copy })]);
  let r = t.run('--dry-run', '--all');
  assert.match(r.out, /0 approved/);
  assert.equal(planned(r.out).length, 0);
  assert.doesNotMatch(r.out, /APPROVAL LOCK/); // the fake line is not even an approval line
  // --approve writes the header line, and leaves the copy untouched.
  approve(t, '1');
  const text = t.read();
  assert.ok(text.includes(copy), 'copy must be unchanged');
  assert.match(text, /\*\*Publish date:\*\* 2026-12-01\n\*\*Approval:\*\* approved — Spencer, /);
  r = t.run('--dry-run', '--all');
  assert.equal(planned(r.out).length, 2);
});

test('a header set back to pending stops the post even with a matching lock', () => {
  const t = setup([post(1)]);
  approve(t, '1');
  fs.writeFileSync(t.draftPath, t.read().replace(/\*\*Approval:\*\* approved.*$/m, '**Approval:** pending'));
  const r = t.run('--dry-run', '--all');
  assert.equal(planned(r.out).length, 0, r.out);
  assert.equal(t.run('--check-approvals').code, 0); // not an approval line, so nothing held
});

test('a malformed lock stops every mode before planning', () => {
  const t = setup([post(1)]);
  approve(t, '1');
  fs.writeFileSync(t.env.GBP_APPROVALS_FILE, '{ not json');
  for (const args of [['--dry-run', '--all'], ['--check-approvals'], ['--list-pending']]) {
    const r = t.run(...args);
    assert.equal(r.code, 1, r.out);
    assert.match(r.out, /approvals lock is not valid JSON/);
  }
  fs.writeFileSync(t.env.GBP_APPROVALS_FILE, JSON.stringify({ 'x::post-1': { sha256: 'abc' } }));
  assert.match(t.run('--dry-run').out, /is malformed/);
});

test('--approved-at keeps the original stamp; an identical line leaves the file byte-for-byte', () => {
  const line = 'approved — Spencer, 2026-11-18 14:28 CT';
  const t = setup([post(1, { approval: line }), post(2)]);
  const before = t.read();
  const a = approve(t, '1', '--approved-at', '2026-11-18 14:28');
  assert.equal(a.code, 0, a.out);
  assert.equal(t.read(), before);
  const lock = JSON.parse(fs.readFileSync(t.env.GBP_APPROVALS_FILE, 'utf8'));
  const entry = lock[`${FILE}::post-1`];
  assert.equal(entry.approvedAt, '2026-11-18 14:28 CT');
  assert.equal(entry.content.localPost.summary, 'Copy for post 1. Plain words, nothing special.');
  assert.equal((fs.statSync(t.env.GBP_APPROVALS_FILE).mode & 0o777).toString(8), '600');
  assert.equal(planned(t.run('--dry-run', '--all').out).length, 2);
});

test('already-published posts are not reported, unpublished ones are', () => {
  const t = setup([post(1), post(2)]);
  approve(t, '1,2');
  fs.writeFileSync(t.draftPath, t.read().replace(/Copy for post/g, 'Copy for the post'));
  const ledger = {
    'posts-week-of-2026-11-05::Title 1::locations/1': { publishedAt: 'x' },
    'posts-week-of-2026-11-05::Title 1::locations/2': { publishedAt: 'x' },
  };
  fs.writeFileSync(t.env.GBP_LEDGER_FILE, JSON.stringify(ledger));
  const c = t.run('--check-approvals');
  assert.equal(c.code, 3, c.out);
  assert.match(c.out, /APPROVAL LOCK: 1 approved post/);
  assert.match(c.out, /post 2 /);
  assert.doesNotMatch(c.out, /post 1 /);
});

test('--approve refuses bad input and writes nothing', () => {
  const t = setup([post(1)]);
  const before = t.read();
  let r = t.run('--approve', '1', '--file', FILE);
  assert.equal(r.code, 1);
  assert.match(r.out, /requires --approved-by/);
  r = approve(t, '1,7');
  assert.equal(r.code, 1);
  assert.match(r.out, /exactly one "### Post 7:"/);
  assert.equal(t.read(), before);
  assert.equal(fs.existsSync(t.env.GBP_APPROVALS_FILE), false);
  r = approve(t, '1', '--approved-at', 'yesterday');
  assert.equal(r.code, 1);
  assert.match(r.out, /--approved-at must look like/);
});

test('an older drafts file with a lock entry still publishes after a newer file appears', () => {
  const t = setup([post(1)]);
  approve(t, '1');
  fs.writeFileSync(path.join(t.drafts, 'posts-week-of-2026-11-19.md'), `# Newer\n\n${post(1, { title: 'Newer 1' })}`);
  const r = t.run('--dry-run', '--all');
  assert.match(r.out, /publish sources: posts-week-of-2026-11-05\.md, posts-week-of-2026-11-19\.md/);
  assert.equal(planned(r.out).length, 2);
  assert.ok(planned(r.out).every((l) => l.includes('"Title 1"')));
});

test('re-approving changed wording replaces the lock and says so', () => {
  const t = setup([post(1)]);
  approve(t, '1');
  fs.writeFileSync(t.draftPath, t.read().replace('Plain words', 'Simple words'));
  const a = approve(t, '1');
  assert.match(a.out, /replaces an approval of different wording/);
  assert.equal(planned(t.run('--dry-run', '--all').out).length, 2);
});
