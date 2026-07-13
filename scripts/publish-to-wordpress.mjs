#!/usr/bin/env node
/**
 * publish-to-wordpress.mjs
 *
 * Pushes the monthly SEO page packages (content/page-packages/YYYY-MM/*.html)
 * into the headless WordPress install as DRAFT pages so the SEO company can
 * review + Publish in wp-admin. Any WP PAGE published at a slug appears on the
 * live site at /{slug} (code routes at the same slug win over WP pages).
 *
 * Usage:
 *   node scripts/publish-to-wordpress.mjs [package-dir]
 *
 * package-dir defaults to the newest YYYY-MM directory under
 * content/page-packages/. Deterministic, stdlib only, no LLM calls.
 *
 * Idempotent: if a WP page already exists at the slug (any status), it is
 * skipped. Fails loud (nonzero exit, clear message) if credentials are
 * missing or any request fails — no silent fallback.
 *
 * Credentials: ~/.config/openclaw/credentials/wpengine.json
 *   { install_url, wp_rest_user, wp_rest_app_password }
 * Override with WPENGINE_CREDS_FILE.
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const REPO_ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const PACKAGES_ROOT = path.join(REPO_ROOT, 'content', 'page-packages');
const CREDS_FILE =
  process.env.WPENGINE_CREDS_FILE ||
  path.join(os.homedir(), '.config', 'openclaw', 'credentials', 'wpengine.json');
// Read-only cross-check: slugs that also exist as code routes on the website
// (code wins over WP at the same slug, so drafting duplicates is safe).
const CODE_PAGES_FILE =
  process.env.LOCAL_SEO_PAGES_FILE ||
  path.join(os.homedir(), 'Sites', 'motorinn-website', 'lib', 'local-seo-pages.ts');
const TIMEOUT_MS = 30000;

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

function resolvePackageDir() {
  const arg = process.argv[2];
  if (arg) {
    const dir = path.resolve(arg);
    if (!fs.existsSync(dir) || !fs.statSync(dir).isDirectory()) {
      die(`package directory not found: ${dir}`);
    }
    return dir;
  }
  if (!fs.existsSync(PACKAGES_ROOT)) die(`no package root at ${PACKAGES_ROOT}`);
  const months = fs
    .readdirSync(PACKAGES_ROOT)
    .filter((name) => /^\d{4}-\d{2}$/.test(name))
    .filter((name) => {
      try {
        return fs.statSync(path.join(PACKAGES_ROOT, name)).isDirectory();
      } catch {
        return false;
      }
    })
    .sort();
  if (months.length === 0) die(`no YYYY-MM package directories under ${PACKAGES_ROOT}`);
  return path.join(PACKAGES_ROOT, months[months.length - 1]);
}

function parsePackage(file) {
  const html = fs.readFileSync(file, 'utf8');
  const problems = [];

  const slugMatch = html.match(/Suggested URL slug:\s*\/?([A-Za-z0-9][A-Za-z0-9/_-]*)/);
  let slug = slugMatch ? slugMatch[1].replace(/\/+$/, '') : null;
  if (!slug) {
    slug = path.basename(file, '.html');
    console.log(`warn: ${path.basename(file)}: no "Suggested URL slug" comment header; using filename as slug (${slug})`);
  }

  const titleMatch = html.match(/<title>([\s\S]*?)<\/title>/i);
  if (!titleMatch) problems.push('missing <title>');

  const metaMatch = html.match(/<meta\s+name=["']description["']\s+content=["']([^"']*)["']/i);
  if (!metaMatch) problems.push('missing meta description');

  const mainMatch = html.match(/<main\b[^>]*>([\s\S]*?)<\/main>/i);
  if (!mainMatch) problems.push('missing <main> content');

  if (problems.length > 0) return { slug, error: problems.join(', ') };

  // Inner <main> only; strip the DealerOn comment block and any <script>
  // JSON-LD — the site renders its own schema.
  const content = mainMatch[1]
    .replace(/<script\b[\s\S]*?<\/script>/gi, '')
    .replace(/<!--[\s\S]*?-->/g, '')
    .trim();

  return {
    slug,
    title: titleMatch[1].trim(),
    excerpt: metaMatch[1].trim(),
    content,
  };
}

function loadCodeSlugs() {
  try {
    const src = fs.readFileSync(CODE_PAGES_FILE, 'utf8');
    return new Set([...src.matchAll(/slug:\s*["']([^"']+)["']/g)].map((m) => m[1]));
  } catch {
    console.log(`note: code-page cross-check skipped (${CODE_PAGES_FILE} not readable)`);
    return new Set();
  }
}

async function main() {
  const creds = loadCreds();
  const pkgDir = resolvePackageDir();
  const files = fs
    .readdirSync(pkgDir)
    .filter((name) => name.endsWith('.html'))
    .sort()
    .map((name) => path.join(pkgDir, name));
  if (files.length === 0) die(`no *.html page packages in ${pkgDir}`);

  const codeSlugs = loadCodeSlugs();
  console.log(`publishing ${files.length} page package(s) from ${pkgDir}`);
  console.log(`target: ${creds.installUrl} (user ${creds.user}, status=draft)`);

  let created = 0;
  let skipped = 0;
  const failures = [];

  for (let i = 0; i < files.length; i += 1) {
    const file = files[i];
    const label = `[${i + 1}/${files.length}]`;
    const page = parsePackage(file);
    const codeNote = codeSlugs.has(page.slug)
      ? ' [also exists as code page in app/(local-seo) — code wins at this slug on the live site]'
      : '';

    if (page.error) {
      failures.push(`${path.basename(file)}: ${page.error}`);
      console.error(`${label} ${page.slug}: FAILED — ${page.error}`);
      continue;
    }

    try {
      const lookup = await wpFetch(creds, { slug: page.slug, status: 'any' });
      if (!lookup.res.ok || !Array.isArray(lookup.json)) {
        throw new Error(`slug lookup failed: HTTP ${lookup.res.status} ${lookup.text.slice(0, 200)}`);
      }
      if (lookup.json.length > 0) {
        const existing = lookup.json[0];
        skipped += 1;
        console.log(`${label} ${page.slug}: exists, skipped (WP id ${existing.id}, status ${existing.status})${codeNote}`);
        continue;
      }

      const post = await wpFetch(creds, {}, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: page.title,
          slug: page.slug,
          status: 'draft',
          content: page.content,
          excerpt: page.excerpt,
        }),
      });
      if (!post.res.ok || !post.json || !post.json.id) {
        throw new Error(`create failed: HTTP ${post.res.status} ${post.text.slice(0, 200)}`);
      }
      created += 1;
      console.log(`${label} ${page.slug}: created draft (WP id ${post.json.id})${codeNote}`);
    } catch (err) {
      failures.push(`${page.slug}: ${err.message}`);
      console.error(`${label} ${page.slug}: FAILED — ${err.message}`);
    }
  }

  console.log(`done: ${created} created, ${skipped} skipped, ${failures.length} failed (of ${files.length})`);
  if (failures.length > 0) {
    console.error(`fatal: ${failures.length} page(s) failed:\n  - ${failures.join('\n  - ')}`);
    process.exit(1);
  }
}

main().catch((err) => die(err.message));
