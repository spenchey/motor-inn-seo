#!/usr/bin/env python3
"""Read-only October manifest adapter into the common approval queue.

No producer execution, upstream writes, media production, or publication occurs.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import html
import json
from pathlib import Path
import shutil
import tempfile

try:
    from .common import atomic_json, draft_digest, lock, utcnow, validate_slug
except ImportError:
    from common import atomic_json, draft_digest, lock, utcnow, validate_slug

REPO = Path(__file__).resolve().parents[1]
OCTOBER = Path('/Users/spencerheywood/Worktrees/motorinn-month-ahead-content-holmes-v3')


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _read_bound(base: Path, entry: dict) -> dict:
    relative = Path(entry['path'])
    path = (base / relative).resolve()
    if relative.is_absolute() or '..' in relative.parts or not path.is_relative_to(base.resolve()):
        raise ValueError(f'Unsafe upstream path: {relative}')
    data = path.read_bytes()
    if _sha(data) != entry['sha256']:
        raise ValueError(f'Upstream SHA-256 mismatch: {relative}')
    return {**entry, 'source_path': str(path), 'text': data.decode('utf-8')}


def inspect_manifest(manifest_path: Path, now: datetime | None = None) -> list[dict]:
    """Validate byte-bound files and preserve original text and factual-source pointers."""
    now = now or datetime.now(timezone.utc)
    raw = manifest_path.read_bytes()
    manifest = json.loads(raw)
    if manifest.get('authorship', {}).get('author') != 'Rory':
        raise ValueError('Expected existing Rory-authored October package')
    package_files = [_read_bound(manifest_path.parent, entry) for entry in manifest['package_files']]
    registries = [entry for entry in package_files if entry['role'] == 'source_registry']
    if len(registries) != 1:
        raise ValueError('Expected exactly one hash-bound source registry')
    source_list = json.loads(registries[0]['text'])['items']
    sources = {source['source_id']: source for source in source_list}
    if len(sources) != len(source_list):
        raise ValueError('Duplicate source IDs')
    results = []
    for piece in manifest['pieces']:
        if piece['kind'] != 'post':
            continue  # Video approvals/media remain owned by the established Emily pipeline.
        files = [_read_bound(manifest_path.parent, entry) for entry in piece['files']]
        if not files or not any(entry['role'] == 'draft' and entry['text'].strip() for entry in files):
            raise ValueError(f"Missing exact draft: {piece['piece_id']}")
        selected = []
        errors = []
        if not piece.get('source_ids'):
            errors.append('No claim sources listed')
        for source_id in piece.get('source_ids', []):
            source = sources.get(source_id)
            if not source:
                errors.append(f'Missing source: {source_id}')
                continue
            source = {**source, 'verified': source.get('status') in {'verified', 'verified_secondary'}, 'retrieved_at': source.get('accessed_date', '') + 'T00:00:00Z', 'valid_until': source.get('expires_at_utc'), 'retrieved_at_precision': 'day (UTC start-of-day used conservatively)'}
            selected.append(source)
            if source.get('status') not in {'verified', 'verified_secondary'} or not source.get('claims_supported') or not source.get('url', '').startswith('https://') or not source.get('accessed_date'):
                errors.append(f'Unverified/incomplete source: {source_id}')
            try:
                expiry = datetime.fromisoformat(source['expires_at_utc'].replace('Z', '+00:00'))
                if expiry.tzinfo is None or expiry <= now:
                    errors.append(f'Expired source: {source_id}')
            except (KeyError, ValueError, TypeError):
                errors.append(f'Missing/invalid source expiry: {source_id}')
        # Stable revision identity: unrelated weekly pieces cannot invalidate/requeue this post.
        identity = {'piece': piece, 'files': [{k: v for k, v in f.items() if k != 'source_path'} for f in files], 'sources': selected, 'authorship': manifest['authorship']}
        revision = _sha(json.dumps(identity, sort_keys=True, ensure_ascii=False).encode())
        slug = f"content-{piece['piece_id'].lower()}-{revision[:12]}"
        validate_slug(slug)
        results.append({
            'slug': slug, 'kind': 'content_post', 'target_platform': 'content_post',
            'title': piece['title'], 'cluster': f"October {manifest['iso_week']}",
            'target-query': piece['title'], 'target_query': piece['title'],
            'outline': [f"Review original {', '.join(piece['channel_adaptations'])} copy; no publication authorization"],
            'estimated_volume': None, 'source-evidence': selected, 'source_evidence': selected,
            'content_files': files, 'upstream_manifest': manifest,
            'upstream_manifest_path': str(manifest_path.resolve()), 'upstream_manifest_sha256': _sha(raw),
            'upstream_package_files': package_files, 'upstream_piece_id': piece['piece_id'],
            'upstream_revision_sha256': revision, 'channels': piece['channel_adaptations'],
            'proposed_at_utc': piece.get('proposed_at_utc'), 'schedule_status': 'proposal_only',
            'publish_authorized': False, 'publication_authorized': False, 'source_errors': errors,
            'publication_blockers': ['Approval here prepares an immutable content handoff only; existing production and live-publication gates still apply.',
                                     'Verify assets/rights and volatile facts before production or publication; no automatic text-only fallback.'],
        })
    # Detect concurrent producer writes before accepting the snapshot.
    if manifest_path.read_bytes() != raw:
        raise ValueError('Upstream manifest changed during import')
    for entry in package_files + [entry for result in results for entry in result['content_files']]:
        _read_bound(manifest_path.parent, entry)
    return results


def import_manifest(manifest_path: Path, pipeline: Path, now: datetime | None = None) -> list[dict]:
    records = inspect_manifest(manifest_path, now)
    summaries = []
    for record in records:
        slug = record['slug']
        existing = [p for p in (pipeline / 'queue').glob(f'*/{slug}.json')]
        if any(p.parent.name != 'pending' for p in existing):
            summaries.append({'slug': slug, 'status': 'already_imported'})
            continue
        pending = pipeline / 'queue' / 'pending' / f'{slug}.json'
        job = {**record, 'status': 'pending', 'created_at': utcnow(), 'qa_passed': False}
        atomic_json(pending, job)
        if record['source_errors']:
            job['errors'] = record['source_errors']
            atomic_json(pending, job)
            summaries.append({'slug': slug, 'status': 'pending', 'errors': job['errors']})
            continue
        final = pipeline / 'drafts' / slug
        final.parent.mkdir(parents=True, exist_ok=True)
        if final.exists():
            raise ValueError(f'Orphaned draft exists; review before retry: {slug}')
        stage = Path(tempfile.mkdtemp(prefix=f'.{slug}-', dir=final.parent))
        try:
            title = html.escape(record['title'])
            body = ''.join(f"<h2>{html.escape(f['path'])}</h2><pre>{html.escape(f['text'])}</pre>" for f in record['content_files'])
            (stage / 'index.html').write_text(
                '<!doctype html><html lang="en"><head><meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width,initial-scale=1">'
                f'<title>{title}</title><style>body{{max-width:70rem;margin:2rem auto;padding:1rem;font:18px system-ui}}pre{{white-space:pre-wrap;overflow-wrap:anywhere}}</style>'
                f'</head><body><h1>{title}</h1><p>Content-post review copy. This is not a publishable SEO page. Original text below is unchanged. Approval prepares a content handoff only.</p>{body}</body></html>', encoding='utf-8')
            atomic_json(stage / 'meta.json', record)
            evidence = ['# Original content source evidence', '', f"Upstream manifest: `{record['upstream_manifest_path']}`", f"Manifest SHA-256: `{record['upstream_manifest_sha256']}`", '', 'Claim mappings are preserved from the reviewed source registry; import integrity QA does not replace factual or creative review.', '']
            for source in record['source_evidence']:
                evidence.extend([f"## {source['source_id']}: {source.get('title', '')}", f"URL: {source['url']}", f"Accessed: {source['accessed_date']}; expires: {source['expires_at_utc']}", f"Claims: {json.dumps(source['claims_supported'], ensure_ascii=False)}", ''])
            (stage / 'evidence.md').write_text('\n'.join(evidence), encoding='utf-8')
            atomic_json(stage / 'qa-report.json', {'passed': True, 'scope': 'content_import_integrity', 'checks': ['Upstream file hashes match', 'Cited source registry entries verified and unexpired', 'Exact immutable source text retained in meta.json', 'HTML review wrapper escaped; no executable upstream content'], 'publication_authorized': False})
            stage.rename(final)
            job.update({'status': 'drafts', 'qa_passed': True, 'draft_digest': draft_digest(final), 'draft_path': str(final), 'drafted_at': utcnow()})
            atomic_json(pipeline / 'queue' / 'drafts' / f'{slug}.json', job)
            pending.unlink()
            summaries.append({'slug': slug, 'status': 'drafts'})
        finally:
            if stage.exists():
                shutil.rmtree(stage)
    return summaries


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, action='append', default=[])
    parser.add_argument('--all-october', action='store_true')
    parser.add_argument('--worktree', type=Path, default=OCTOBER)
    parser.add_argument('--pipeline', type=Path, default=REPO / 'pipeline')
    parser.add_argument('--check-only', action='store_true', help='Validate upstream snapshots without writing queue records')
    args = parser.parse_args()
    manifests = args.manifest + ([args.worktree / 'months/2026-10' / f'W{week}' / 'manifest.json' for week in range(40, 45)] if args.all_october else [])
    if not manifests:
        parser.error('Pass --manifest or --all-october')
    results, failures = [], []
    from contextlib import nullcontext
    with (nullcontext() if args.check_only else lock(args.pipeline, 'queue')):
        for path in manifests:
            try:
                if args.check_only:
                    records = inspect_manifest(path)
                    results.extend({'slug': r['slug'], 'errors': r['source_errors']} for r in records)
                else:
                    results.extend(import_manifest(path, args.pipeline))
            except (OSError, ValueError, KeyError, TypeError) as exc:
                failures.append({'manifest': str(path), 'error': str(exc)})
    print(json.dumps({'results': results, 'failures': failures}, indent=2))
    return int(bool(failures) or any(item.get('errors') for item in results))


if __name__ == '__main__':
    raise SystemExit(main())
