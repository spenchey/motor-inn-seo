#!/usr/bin/env node
/**
 * publish-paid-search-drafts.mjs
 *
 * Pushes Rory's paid-search landing-page briefs
 * (content/drafts/paid-search/*.md) into the headless WordPress install as
 * DRAFT pages so they can be reviewed + published (or rejected) in wp-admin.
 * Any WP PAGE published at a slug appears on the live site at /{slug}
 * (code routes at the same slug win over WP pages).
 *
 * Usage:
 *   node scripts/publish-paid-search-drafts.mjs [drafts-dir]
 *
 * drafts-dir defaults to content/drafts/paid-search/. Deterministic, node
 * stdlib only, no LLM calls.
 *
 * - Slug: the .md filename (without extension).
 * - Title: the markdown H1 (fallback: title-cased filename).
 * - Body: deterministic markdown->HTML for the subset these files use
 *   (frontmatter, #/##/### headings, paragraphs, "-"/"*" bullet lists,
 *   **bold**, [inline](links)). The first H1 is dropped from the body
 *   because it becomes the WP page title.
 * - Link repointing: any motorinnautogroup.com (DealerOn-era) link is
 *   rewritten to the equivalent new-site route (/inventory/used,
 *   /inventory/new, /finance, /contact, /service, /trade-in).
 * - Safety: slugs that collide with real site routes are skipped, never
 *   drafted (RESERVED_SLUGS below).
 * - Review flags: drafts containing $ prices, year+mileage combos, or
 *   "in stock" claims are logged as needing dated-content review.
 *
 * Idempotent: if a WP page already exists at the slug (any status), it is
 * skipped. Fails loud (nonzero exit, clear message) if credentials are
 * missing or any request fails — no silent fallback.
 *
 * Credentials: ~/.config/openclaw/credentials/wpengine.json
 *   { install_url, wp_rest_user, wp_rest_app_password }
 * Override with WPENGINE_CREDS_FILE.
 *
 * Helper functions (die/loadCreds/restUrl/wpFetch) are mirrored from
 * scripts/publish-to-wordpress.mjs — that script executes main() at import
 * time, so importing it directly is not clean.
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const REPO_ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const DRAFTS_DIR_DEFAULT = path.join(REPO_ROOT, 'content', 'drafts', 'paid-search');
const CREDS_FILE =
  process.env.WPENGINE_CREDS_FILE ||
  path.join(os.homedir(), '.config', 'openclaw', 'credentials', 'wpengine.json');
const TIMEOUT_MS = 30000;

// Slugs that are real routes on the live site (code wins at these slugs, and
// drafting a WP page there invites an accidental shadow publish). Never draft
// these. Includes the 8 local-seo code pages from
// motorinn-website/lib/local-seo-pages.ts.
const RESERVED_SLUGS = new Set([
  'about',
  'finance',
  'service',
  'contact',
  'inventory',
  'blog',
  'specials',
  'trade-in',
  'careers',
  'parts',
  'models',
  'near',
  'reviews',
  'disclosures',
  'privacy-policy',
  'terms',
  'data-deletion',
  'sitemap',
  'accessibility',
  'certified',
  'warranty-questions',
  'financing-questions',
  'service-area',
  'body-shop',
  // local-seo code pages
  'car-dealerships-carroll-iowa',
  'toyota-dealer-carroll-iowa',
  'used-cars-carroll-iowa',
  'used-trucks-carroll-iowa',
  'auto-service-carroll-iowa',
  'best-place-to-buy-used-car-carroll-iowa',
  'new-vs-used-car-carroll-iowa',
  'where-to-service-toyota-carroll-iowa',
]);

function die(msg) {
  console.error(`fatal: ${msg}`);
  process.exit(1);
}

function loadCreds() {
  if (!fs.existsSync(CREDS_FILE)) {
    die(`WordPress credentials file not found: ${CREDS_FILE} — cannot publish drafts. No fallback; fix the credentials file.`);
  }
  let creds;
  try {
    creds = JSON.parse(fs.readFileSync(CREDS_FILE, 'utf8'));
  } catch (err) {
    die(`WordPress credentials file is not valid JSON: ${CREDS_FILE} (${err.message})`);
  }
  const { install_url, wp_rest_user, wp_rest_app_password } = creds;
  if (!install_url || !wp_rest_user || !wp_rest_app_password) {
    die(`WordPress credentials file ${CREDS_FILE} is missing install_url, wp_rest_user, or wp_rest_app_password`);
  }
  return {
    installUrl: String(install_url).replace(/\/+$/, ''),
    user: wp_rest_user,
    authHeader: 'Basic ' + Buffer.from(`${wp_rest_user}:${wp_rest_app_password}`).toString('base64'),
  };
}

function restUrl(installUrl, params) {
  const url = new URL(`${installUrl}/`);
  url.searchParams.set('rest_route', '/wp/v2/pages');
  for (const [key, value] of Object.entries(params)) url.searchParams.set(key, value);
  return url;
}

async function wpFetch(creds, params, init = {}) {
  const url = restUrl(creds.installUrl, params);
  const res = await fetch(url, {
    ...init,
    headers: {
      Authorization: creds.authHeader,
      Accept: 'application/json',
      ...(init.headers || {}),
    },
    signal: AbortSignal.timeout(TIMEOUT_MS),
  });
  const text = await res.text();
  let json = null;
  try {
    json = JSON.parse(text);
  } catch {
    /* non-JSON body handled by caller via status check */
  }
  return { res, json, text };
}

// ---------------------------------------------------------------------------
// DealerOn-era link repointing
// ---------------------------------------------------------------------------

const OLD_HOST_RE = /^https?:\/\/(?:www\.)?motorinnautogroup\.com/i;

// Deterministic path-keyword map, first match wins.
const REPOINT_RULES = [
  { re: /new.*(inventory|vehicles|cars)|(inventory|vehicles|cars).*new/i, to: '/inventory/new' },
  { re: /used|inventory|vehicles|cars|vdp|searchused|searchnew/i, to: '/inventory/used' },
  { re: /financ|credit|loan|payment/i, to: '/finance' },
  { re: /service|maintenance|repair|oil|tire|brake/i, to: '/service' },
  { re: /trade|value|sell.*car|apprais/i, to: '/trade-in' },
  { re: /contact|about|hours|directions|staff|dealership/i, to: '/contact' },
];

function repointUrl(url) {
  if (!OLD_HOST_RE.test(url)) return url;
  const oldPath = url.replace(OLD_HOST_RE, '').split(/[?#]/)[0];
  for (const rule of REPOINT_RULES) {
    if (rule.re.test(oldPath)) return rule.to;
  }
  return '/'; // unknown DealerOn path: send to the new-site homepage
}

// ---------------------------------------------------------------------------
// Deterministic markdown -> HTML (only the subset these briefs use)
// ---------------------------------------------------------------------------

function escapeHtml(text) {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function renderInline(text) {
  // Repoint bare DealerOn URLs in plain text before escaping.
  let out = text.replace(/https?:\/\/(?:www\.)?motorinnautogroup\.com[^\s)\]"']*/gi, (m) => repointUrl(m));
  out = escapeHtml(out);
  // [text](href) — href already escaped (quotes/&), repoint if DealerOn.
  out = out.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, (m, label, href) => {
    const target = repointUrl(href);
    return `<a href="${target}">${label}</a>`;
  });
  // **bold**
  out = out.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  return out;
}

function stripFrontmatter(markdown) {
  const lines = markdown.split(/\r?\n/);
  if (lines[0] !== '---') return { frontmatter: '', body: lines };
  const end = lines.indexOf('---', 1);
  if (end === -1) return { frontmatter: '', body: lines };
  return { frontmatter: lines.slice(1, end).join('\n'), body: lines.slice(end + 1) };
}

function markdownToHtml(bodyLines) {
  const html = [];
  let listItems = null;
  let paragraph = [];
  let firstH1Dropped = false;

  const flushParagraph = () => {
    if (paragraph.length > 0) {
      html.push(`<p>${renderInline(paragraph.join(' '))}</p>`);
      paragraph = [];
    }
  };
  const flushList = () => {
    if (listItems) {
      html.push(`<ul>\n${listItems.map((li) => `  <li>${renderInline(li)}</li>`).join('\n')}\n</ul>`);
      listItems = null;
    }
  };

  for (const rawLine of bodyLines) {
    const line = rawLine.trimEnd();
    const heading = line.match(/^(#{1,4})\s+(.*)$/);
    const bullet = line.match(/^\s*[-*]\s+(.*)$/);

    if (line.trim() === '') {
      flushParagraph();
      flushList();
    } else if (heading) {
      flushParagraph();
      flushList();
      const level = heading[1].length;
      if (level === 1 && !firstH1Dropped) {
        firstH1Dropped = true; // H1 becomes the WP page title; don't duplicate it
        continue;
      }
      html.push(`<h${level}>${renderInline(heading[2].trim())}</h${level}>`);
    } else if (bullet) {
      flushParagraph();
      if (!listItems) listItems = [];
      listItems.push(bullet[1].trim());
    } else {
      flushList();
      paragraph.push(line.trim());
    }
  }
  flushParagraph();
  flushList();
  return html.join('\n');
}

function extractTitle(bodyLines, slug) {
  for (const line of bodyLines) {
    const m = line.match(/^#\s+(.*)$/);
    if (m) return m[1].trim();
  }
  return slug
    .split('-')
    .map((w) => (w ? w[0].toUpperCase() + w.slice(1) : w))
    .join(' ');
}

// ---------------------------------------------------------------------------
// Dated-content review flags
// ---------------------------------------------------------------------------

function reviewFlags(markdownBody) {
  const flags = [];
  if (/\$\s?\d/.test(markdownBody)) flags.push('contains $ price(s)');
  if (/\b(19|20)\d{2}\b/.test(markdownBody) && /\bmil(es|eage)\b/i.test(markdownBody)) {
    flags.push('contains specific year + mileage');
  }
  if (/\bin[\s-]stock\b/i.test(markdownBody)) flags.push('contains "in stock" claim');
  return flags;
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

function resolveDraftsDir() {
  const arg = process.argv[2];
  const dir = arg ? path.resolve(arg) : DRAFTS_DIR_DEFAULT;
  if (!fs.existsSync(dir) || !fs.statSync(dir).isDirectory()) {
    die(`drafts directory not found: ${dir}`);
  }
  return dir;
}

async function main() {
  const creds = loadCreds();
  const draftsDir = resolveDraftsDir();
  const files = fs
    .readdirSync(draftsDir)
    .filter((name) => name.endsWith('.md'))
    .sort()
    .map((name) => path.join(draftsDir, name));
  if (files.length === 0) die(`no *.md drafts in ${draftsDir}`);

  console.log(`publishing ${files.length} paid-search draft(s) from ${draftsDir}`);
  console.log(`target: ${creds.installUrl} (user ${creds.user}, status=draft)`);

  let created = 0;
  let skippedExisting = 0;
  let skippedReserved = 0;
  const flagged = [];
  const failures = [];

  for (let i = 0; i < files.length; i += 1) {
    const file = files[i];
    const label = `[${i + 1}/${files.length}]`;
    const slug = path.basename(file, '.md');

    if (RESERVED_SLUGS.has(slug)) {
      skippedReserved += 1;
      console.log(`${label} ${slug}: SKIPPED — collides with a real site route (reserved slug)`);
      continue;
    }

    const markdown = fs.readFileSync(file, 'utf8');
    const { body } = stripFrontmatter(markdown);
    const bodyText = body.join('\n');
    const title = extractTitle(body, slug);
    const content = markdownToHtml(body);
    if (!content) {
      failures.push(`${slug}: empty body after conversion`);
      console.error(`${label} ${slug}: FAILED — empty body after conversion`);
      continue;
    }

    const flags = reviewFlags(bodyText);
    if (flags.length > 0) flagged.push(`${slug}: ${flags.join('; ')}`);

    try {
      const lookup = await wpFetch(creds, { slug, status: 'any' });
      if (!lookup.res.ok || !Array.isArray(lookup.json)) {
        throw new Error(`slug lookup failed: HTTP ${lookup.res.status} ${lookup.text.slice(0, 200)}`);
      }
      if (lookup.json.length > 0) {
        const existing = lookup.json[0];
        skippedExisting += 1;
        console.log(`${label} ${slug}: exists, skipped (WP id ${existing.id}, status ${existing.status})`);
        continue;
      }

      const post = await wpFetch(creds, {}, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, slug, status: 'draft', content }),
      });
      if (!post.res.ok || !post.json || !post.json.id) {
        throw new Error(`create failed: HTTP ${post.res.status} ${post.text.slice(0, 200)}`);
      }
      created += 1;
      const flagNote = flags.length > 0 ? ` [REVIEW: ${flags.join('; ')}]` : '';
      console.log(`${label} ${slug}: created draft (WP id ${post.json.id})${flagNote}`);
    } catch (err) {
      failures.push(`${slug}: ${err.message}`);
      console.error(`${label} ${slug}: FAILED — ${err.message}`);
    }
  }

  console.log(
    `done: ${created} created, ${skippedExisting} skipped (already in WP), ` +
      `${skippedReserved} skipped (reserved slug), ${failures.length} failed (of ${files.length})`,
  );
  if (flagged.length > 0) {
    console.log(`dated-content review needed for ${flagged.length} draft(s):\n  - ${flagged.join('\n  - ')}`);
  }
  if (failures.length > 0) {
    console.error(`fatal: ${failures.length} draft(s) failed:\n  - ${failures.join('\n  - ')}`);
    process.exit(1);
  }
}

main().catch((err) => die(err.message));
