#!/usr/bin/env node
'use strict';
/* Read-only GBP review fetch using the fallback_credentials (authorized_user OAuth)
   plus the primary owner_oauth candidate. Dumps normalized reviews JSON.
   2026-09-21: retry across ALL credentials per location; skip empty bodies. */
const path = require('path');
const os = require('os');
const fs = require('fs');
const clientPath = path.join(os.homedir(), 'clawd/scripts/no-model/google-reviews/gbp-client.js');
const { loadConfig, loadCredentialCandidates, mintAccessToken, starRating } = require(clientPath);

const V4_BASE = 'https://mybusiness.googleapis.com/v4';

async function main() {
  const config = loadConfig({});
  const candidates = [];
  for (const candidate of loadCredentialCandidates(config, {})) {
    try {
      const token = await mintAccessToken(candidate.credentials, {});
      candidates.push({ name: candidate.name, token });
      console.error(`auth ok: ${candidate.name}`);
    } catch (e) {
      console.error(`cred ${candidate.name}: ${e.message}`);
    }
  }
  if (!candidates.length) { console.error('ERROR no credential worked'); process.exit(1); }

  const out = { locations: [] };
  for (const locationId of config.location_ids) {
    let reviews = [];
    let total = null;
    let avg = null;
    let authUsed = null;
    for (const cand of candidates) {
      const token = cand.token;
      const pageReviews = [];
      let pageToken = '';
      let pTotal = null;
      let pAvg = null;
      let ok = true;
      do {
        const q = new URLSearchParams({ pageSize: '50', orderBy: 'updateTime desc' });
        if (pageToken) q.set('pageToken', pageToken);
        const url = `${V4_BASE}/${config.account_id}/${locationId}/reviews?${q}`;
        const res = await fetch(url, { headers: { Authorization: `Bearer ${token}` } });
        if (!res.ok) { console.error(`WARN ${locationId} [${cand.name}]: HTTP ${res.status}`); ok = false; break; }
        const page = await res.json();
        if (page.totalReviewCount === undefined && !(Array.isArray(page.reviews) && page.reviews.length)) {
          console.error(`WARN ${locationId} [${cand.name}]: empty reviews body (account/location mismatch for this credential)`);
        }
        pTotal = page.totalReviewCount ?? pTotal;
        pAvg = page.averageRating ?? pAvg;
        pageReviews.push(...(Array.isArray(page.reviews) ? page.reviews : []));
        pageToken = page.nextPageToken || '';
      } while (pageToken);
      if (ok && (pTotal !== null || pageReviews.length)) {
        reviews = pageReviews; total = pTotal; avg = pAvg; authUsed = cand.name;
        break;
      }
    }
    const norm = reviews.map((r) => ({
      author: r.reviewer?.displayName || null,
      rating: starRating(r.starRating),
      text: r.comment || null,
      create_time: r.createTime || null,
      has_reply: Boolean(r.reviewReply?.comment),
      reply_text: r.reviewReply?.comment || null,
      reply_update_time: r.reviewReply?.updateTime || null,
    }));
    out.locations.push({ location: locationId, totalReviewCount: total, averageRating: avg, auth: authUsed, fetched: norm.length, reviews: norm });
  }
  process.stdout.write(JSON.stringify(out, null, 1));
}

main().catch((e) => { console.error('ERROR', e.message); process.exit(1); });
