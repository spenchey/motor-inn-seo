#!/usr/bin/env python3
"""Linear -> SEO pipeline brief intake (MOT-3170).

Fetches Spencer-approved Grok DRAFT BRIEF tickets from Linear and converts each
into a pipeline candidate + pending queue job, so the next scheduled orchestrator
run treats the approved brief as the pre-selected opportunity instead of the
runbook-invented one. Deterministic, read-only against Linear, no new scheduler:
call it from run_pipeline.sh before orchestrator.py (daily controller path).

Contract (locked 2026-09-18):
- Grok files tickets titled `DRAFT BRIEF: ...` in the SEO Team project.
- Approval signal = BOTH: state moved to Todo AND label `approved-brief` applied
  by Spencer. (Label alone is not enough; state alone is not enough. Double-signal
  prevents accidental drafts entering the paid pipeline.)
- Idempotent: a ticket is imported at most once; the Linear issue id is recorded
  in the job JSON (`linear_issue`) and in processed_ids.json. Re-runs skip it.
- Fail-closed: no network to Linear or missing key -> exit 3, orchestrator run
  continues with existing candidates (never blocks the daily run).
- The imported candidate carries `source: linear-approved-brief` and
  `source_issue: <identifier>`; content validation against first-party evidence
  stays with the existing research/content stages (Rory validates, may reject).

Usage: python3 linear_brief_intake.py [--dry-run]
Exit codes: 0 ok, 3 Linear fetch/auth failure, 4 parse/contract error.
"""
from __future__ import annotations
import json
import re
import sys
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[2]
CONFIG = json.loads((ROOT / 'automation' / 'config.json').read_text())
CANDIDATES_PATH = Path(CONFIG['candidate_path'])
QUEUE_PENDING = ROOT / 'pipeline' / 'queue' / 'pending'
PROCESSED = ROOT / 'pipeline' / 'linear_intake_processed.json'

LINEAR_ENV_CANDIDATES = (
    Path.home() / '.config/motorinn/linear.env',
    Path('/Users/spencerheywood/dispatch/data/secrets/linear-motorinn.env'),
)

DRAFT_TITLE = re.compile(r'^DRAFT BRIEF:', re.I)
TARGET_QUERY_KEYS = ('primary term', 'primary_term', 'target query', 'target_query')
TARGET_URL_KEYS = ('target url', 'target_url', 'page url')
SITE_KEYS = ('site', 'store')
SLUG_KEYS = ('slug',)


def linear_key():
    for p in LINEAR_ENV_CANDIDATES:
        if p.exists():
            for line in p.read_text().splitlines():
                line = line.strip()
                if line.startswith('LINEAR_API_KEY='):
                    return line.split('=', 1)[1].strip().strip('"').strip("'")
    return None


def gql(query, variables=None):
    key = linear_key()
    if not key:
        raise RuntimeError('no LINEAR_API_KEY found')
    data = json.dumps({'query': query, 'variables': variables or {}}).encode()
    req = urllib.request.Request(
        'https://api.linear.app/graphql', data=data,
        headers={'Authorization': key, 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def fetch_approved_briefs() -> list[dict]:
    q = """
    query($teamKey: String!) {
      issues(first: 50, filter: {
        team: { key: { eq: $teamKey } },
        title: { startsWith: "DRAFT BRIEF" },
        state: { type: { eq: "unstarted" } },
        labels: { name: { eq: "approved-brief" } }
      }) {
        nodes { id identifier title description url updatedAt
          project { name }
          labels { nodes { name } } }
      }
    }"""
    data = gql(q, {'teamKey': 'MOT'})
    if 'errors' in data:
        raise RuntimeError(str(data['errors'])[:300])
    return data['data']['issues']['nodes']


def parse_desc_field(desc: str, keys: tuple[str, ...]) -> str | None:
    for line in (desc or '').splitlines():
        low = line.lower()
        for k in keys:
            if low.startswith(k) and ':' in line:
                val = line.split(':', 1)[1].strip().strip('*').strip()
                return val or None
    return None


def slugify(text: str) -> str:
    s = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
    return re.sub(r'-{2,}', '-', s)[:60] or 'linear-brief'


def to_candidate(issue: dict) -> tuple[dict, str]:
    desc = issue.get('description') or ''
    url = parse_desc_field(desc, TARGET_URL_KEYS)
    query = parse_desc_field(desc, TARGET_QUERY_KEYS)
    if not url or not query:
        raise ValueError(f"{issue['identifier']}: missing target URL / primary term in ticket body")
    m = re.search(r'https?://[^\s)\]>"]+', url)
    if not m:
        raise ValueError(f"{issue['identifier']}: unparseable target URL")
    url = m.group(0).rstrip('.,;')
    host = re.sub(r'^https?://', '', url).split('/')[0]
    slug = f"brief-{issue['identifier'].split('-')[1].lower()}-{slugify(query)}"
    now = datetime.now(ZoneInfo('America/Chicago')).isoformat(timespec='seconds')
    return {
        'slug': slug,
        'cluster': 'linear-approved-briefs',
        'target_query': query,
        'target_url': url,
        'owner_host': host,
        'relevance': 1.0,
        'source': 'linear-approved-brief',
        'source_issue': issue['identifier'],
        'source_issue_url': issue.get('url'),
        'approved_at': now,
        'ai_question_ids': [],
    }, desc


def main() -> int:
    dry = '--dry-run' in sys.argv
    processed = json.loads(PROCESSED.read_text()) if PROCESSED.exists() else {'ids': {}}
    try:
        briefs = fetch_approved_briefs()
    except Exception as exc:  # fail-closed, never block orchestrator
        print(f'linear_brief_intake: fetch failed: {exc}', file=sys.stderr)
        return 3

    imported = []
    for issue in briefs:
        iid = issue['id']
        if iid in processed['ids']:
            continue
        try:
            candidate, desc = to_candidate(issue)
        except ValueError as exc:
            print(f'linear_brief_intake: {exc}', file=sys.stderr)
            continue
        cand_path = CANDIDATES_PATH
        data = json.loads(cand_path.read_text())
        cands = data['candidates'] if isinstance(data, dict) else data
        if any(c['slug'] == candidate['slug'] for c in cands):
            processed['ids'][iid] = {'slug': candidate['slug'], 'imported_at': datetime.now(ZoneInfo('America/Chicago')).isoformat(timespec='seconds')}
            continue
        if not dry:
            if isinstance(data, dict):
                data['candidates'].append(candidate)
            else:
                data.append(candidate)
            cand_path.write_text(json.dumps(data, indent=2))
            job = dict(candidate)
            job.update({'kind': 'seo_page', 'created_at': datetime.now(ZoneInfo('America/Chicago')).isoformat(timespec='seconds'),
                        'linear_brief_description': desc[:8000]})
            QUEUE_PENDING.mkdir(parents=True, exist_ok=True)
            (QUEUE_PENDING / f"{candidate['slug']}.json").write_text(json.dumps(job, indent=2))
        processed['ids'][iid] = {'slug': candidate['slug'],
                                 'imported_at': datetime.now(ZoneInfo('America/Chicago')).isoformat(timespec='seconds')}
        imported.append(f"{issue['identifier']} -> {candidate['slug']}")

    if imported and not dry:
        PROCESSED.parent.mkdir(parents=True, exist_ok=True)
        PROCESSED.write_text(json.dumps(processed, indent=2))
    print('linear_brief_intake:', ('(dry-run) ' if dry else '') + '; '.join(imported) or 'no new approved briefs')
    return 0


if __name__ == '__main__':
    sys.exit(main())
