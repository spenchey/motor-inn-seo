#!/usr/bin/env python3
"""Weekly research-to-pending driver. No approval, publication, messaging or git writes."""
import argparse
import csv
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo

from common import DEFAULT_ROOT, atomic_json, fresh, lock, read_json, utcnow, validate_slug
from providers import DataForSEO, gsc_snapshot, successful

DEFAULT_CONFIG = Path(__file__).with_name('config.json')
STATES = ('pending', 'drafts', 'approved', 'hold', 'rejected', 'ready')


def initialize(root):
    for name in [*(f'queue/{s}' for s in STATES), 'drafts', 'ready-for-dealeron',
                 'ready-for-content', 'cache', 'inputs', 'logs', 'runs', 'handoffs',
                 'approvals/inbox', 'approvals/processed', 'approvals/events', 'email-drafts', 'ai-prs']:
        (Path(root) / name).mkdir(parents=True, exist_ok=True)


def runbooks(directory):
    directory = Path(directory)
    names = ('topical-map', 'opportunity-scoring', 'ai-mentions', 'internal-links', 'cannibalization')
    texts = {name: (directory / f'{name}.md').read_text() for name in names}
    clusters = [line.split('|')[1].strip() for line in texts['topical-map'].splitlines()
                if line.startswith('| ') and not line.startswith('| Cluster')]
    questions = []
    for line in texts['ai-mentions'].splitlines():
        if re.match(r'\| Q\d+ \|', line):
            _, qid, question, segment, *_ = line.split('|')
            questions.append({'id': qid.strip(), 'question': question.strip(), 'segment': segment.strip()})
    if not clusters or len(questions) != 20:
        raise ValueError('Runbooks lack cluster table or stable 20-question set')
    if 'priority_score = base_score × R' not in texts['opportunity-scoring']:
        raise ValueError('Scoring runbook changed; reconcile scoring implementation')
    return clusters, questions, {name: hashlib.sha256(text.encode()).hexdigest() for name, text in texts.items()}


def normalize(query):
    return ' '.join(re.findall(r'[a-z0-9]+', query.lower()))


def owner_key(host):
    return host.lower().removeprefix('www.')


def traffic_bin(value):
    return next((score for bound, score in ((1000, 5), (500, 4), (200, 3), (50, 2), (1, 1)) if value >= bound), 0)


def read_clusters(path):
    return [line.split('|')[1].strip() for line in Path(path).read_text().splitlines()
            if line.startswith('| ') and not line.startswith('| Cluster')]


def read_questions(path):
    return [{'id': cells[1].strip(), 'question': cells[2].strip(), 'segment': cells[3].strip()}
            for line in Path(path).read_text().splitlines() if re.match(r'\| Q\d+ \|', line)
            for cells in [line.split('|')]]


def opportunity(demand, hours, relevance):
    if hours <= 0 or relevance not in (0, .5, 1):
        raise ValueError('Invalid hours or relevance')
    ease = next((e for bound, e in ((2, 5), (4, 4), (8, 3), (16, 2)) if hours <= bound), 1)
    traffic = traffic_bin(demand) if demand is not None else None
    return {'T': traffic, 'E': ease, 'R': relevance,
            'priority_score': traffic * ease * relevance if traffic is not None else None}


def query_evidence(candidate, snapshot):
    overlap = cannibalization(candidate, snapshot)
    prop = snapshot.get('properties', {}).get(candidate['gsc_property'], {})
    queries = {normalize(q) for q in candidate.get('query_variants', []) + [candidate['target_query']]}
    rows = {normalize(r['keys'][0]): r['impressions'] for r in prop.get('query_rows', [])
            if normalize(r['keys'][0]) in queries}
    return {**overlap, 'demand': sum(rows.values()) if prop.get('status') == 'ok' else None,
            'status': 'HOLD-CANNIBALIZATION' if overlap['matches'] else ('checked' if prop.get('status') == 'ok' else 'BLOCKED-GSC')}


def ai_observation(question, items, observed_at):
    overviews = [i for i in items if i.get('type') == 'ai_overview']
    urls = [r['url'] for i in overviews for r in i.get('references', []) if r.get('url')]
    owned = {'motorinnautogroup.com', 'motorinntoyotaofcarroll.com', 'motorinnofcarroll.com'}
    cited = any((urlsplit(url).hostname or '').removeprefix('www.') in owned for url in urls)
    return {**question, 'surface': 'DataForSEO Google SERP AI Overview', 'observed_at': observed_at,
            'status': 'COMPLETE' if overviews else 'NO_OVERVIEW', 'cited_urls': urls,
            'citation_gap': not cited if overviews else None}


def score(candidate, snapshot, volume):
    prop = snapshot.get('properties', {}).get(candidate['gsc_property'], {})
    queries = {normalize(x) for x in candidate.get('query_variants', [candidate['target_query']])}
    queries.add(normalize(candidate['target_query']))
    rows = [r for r in prop.get('query_rows', []) if normalize(r['keys'][0]) in queries
            and not re.search(r'motor\s*inn', r['keys'][0], re.I)]
    if prop.get('status') == 'ok':
        # Query-only rows, never page-row sums; retain max for accidental duplicate queries.
        demand = {}
        for row in rows:
            key = normalize(row['keys'][0])
            demand[key] = max(demand.get(key, 0), row['impressions'])
        total, source, confidence = sum(demand.values()), 'GSC-query-only', 'HIGH'
    else:
        total, source, confidence = volume, 'volume-proxy', 'MEDIUM' if volume is not None else 'LOW'
    hours, relevance = float(candidate['estimated_hours']), float(candidate.get('relevance', .5))
    if hours <= 0 or relevance not in (0, .5, 1):
        raise ValueError('Invalid hours or relevance')
    return {'demand_source': source, 'eligible_demand': total, **opportunity(total, hours, relevance),
            'hours': hours,
            'confidence': confidence, 'window': snapshot.get('request', {})}


def cannibalization(candidate, snapshot):
    prop = snapshot.get('properties', {}).get(candidate['gsc_property'], {})
    if prop.get('status') != 'ok':
        return {'status': 'BLOCKED-GSC', 'property': candidate['gsc_property'], 'matches': []}
    queries = {normalize(q) for q in candidate.get('query_variants', []) + [candidate['target_query']]}
    grouped = {}
    for row in prop.get('page_rows', []):
        query, url = row['keys']
        if normalize(query) in queries:
            grouped.setdefault(query, []).append(row)
    matches = []
    for query, rows in grouped.items():
        total = sum(r['impressions'] for r in rows)
        for row in rows:
            if row['impressions'] >= 20 and total and row['impressions'] / total >= .2:
                matches.append({'query': query, 'url': row['keys'][1], 'impressions': row['impressions'],
                                'page_row_share': row['impressions'] / total})
    # Existing owner takes priority even if there is only one ranking page.
    return {'status': 'HOLD-EXISTING-OWNER' if matches else 'clear-in-observed-window',
            'property': candidate['gsc_property'], 'matches': matches,
            'limitation': 'Observed query/page overlap only; zero rows do not prove no existing page or traffic loss.'}


def citation_gaps(root, questions, candidate):
    chosen = [q for q in questions if q['id'] in candidate.get('ai_question_ids', [])]
    source = Path(root) / 'inputs' / 'ai-mentions.csv'
    observations = list(csv.DictReader(source.open())) if source.exists() else []
    result = []
    for question in chosen:
        for surface in ('ChatGPT', 'Perplexity', 'Google Search AI Overviews'):
            rows = [r for r in observations if r.get('question_id') == question['id'] and r.get('surface') == surface
                    and fresh(r.get('observed_at'))]
            row = max(rows, key=lambda r: r['observed_at']) if rows else None
            item = {**question, 'surface': surface, 'status': 'UNOBSERVED', 'citation_gap': None}
            if row:
                evidence = Path(row.get('evidence_path', ''))
                if not evidence.is_absolute():
                    evidence = source.parent / evidence
                if evidence.is_file() and row.get('status') in ('COMPLETE', 'COMPLETED', 'OK'):
                    cited = row.get('cites_dealer_site', '').lower()
                    item.update(status=row['status'], citation_gap=(cited == 'no') if cited in ('yes', 'no') else None,
                                evidence_path=str(evidence), observed_at=row['observed_at'])
                else:
                    item['status'] = row.get('status', 'BLOCKED-EVIDENCE')
            result.append(item)
    return result


def research(client, candidate, questions=()):
    locale = {'location_name': client.config['location_name'], 'language_code': client.config['language_code']}
    serp = client.call('serp', {**locale, 'keyword': candidate['target_query'], 'depth': 10})
    tasks = successful(serp)
    items = [i for task in tasks for result in task.get('result') or [] for i in result.get('items') or []
             if i.get('type') == 'organic']
    competitors = [{k: i.get(k) for k in ('url', 'domain', 'title', 'rank_group', 'description')}
                   for i in items if urlsplit(i.get('url', '')).hostname != candidate['owner_host']]
    own_results = [{k: i.get(k) for k in ('url', 'domain', 'title', 'rank_group', 'description')}
                   for i in items if urlsplit(i.get('url', '')).hostname == candidate['owner_host']]
    screenshot = client.call('screenshot', {'task_id': tasks[0]['id']})
    successful(screenshot)
    image = client.save_screenshot(screenshot)
    observations = []
    for question in questions[:1]:
        entry = client.call('serp', {**locale, 'keyword': question['question'], 'depth': 10,
                                    'load_async_ai_overview': True})
        observed = [i for task in successful(entry) for result in task.get('result') or [] for i in result.get('items') or []]
        observation = ai_observation(question, observed, entry.get('retrieved_at', utcnow()))
        observation['cache_key'] = entry['cache_key']
        observation['limitation'] = 'API observation; not a logged-in ChatGPT, Perplexity or consumer Google session.'
        observations.append(observation)
    return {'serp_cache_key': serp['cache_key'], 'screenshot_cache_key': screenshot['cache_key'],
            'screenshot_path': str(image), 'competitor_results': competitors,
            'own_results': own_results,
            'ai_observations': observations,
            'owner_in_top_10': any(urlsplit(i.get('url', '')).hostname == candidate['owner_host'] for i in items),
            'limitation': 'SERP competitor visibility gap, not a full competitor-domain keyword gap crawl.'}


def refresh_pending(root, config, pending, snapshot, client, questions, limit):
    """Repair research for bounded pending jobs, preserving facts and all reviewed work."""
    results = []
    for original in pending[:limit]:
        slug = validate_slug(original['slug'])
        path = root / 'queue/pending' / (slug + '.json')
        update = {}
        try:
            check = query_evidence(original, snapshot)
            overlap = cannibalization(original, snapshot)
            update.update(gsc_check=check, cannibalization=overlap)
            if check['status'] != 'checked':
                raise RuntimeError(check['status'])
            volume_entry = client.call('volume', {'keywords': [original['target_query']],
                'location_name': config['dataforseo']['location_name'], 'language_code': config['dataforseo']['language_code']})
            values = [r.get('search_volume') for task in successful(volume_entry) for r in task.get('result') or []
                      if normalize(r['keyword']) == normalize(original['target_query'])]
            volume = values[0] if values else None
            ids = original.get('ai_question_ids', [original.get('ai_question_id')])
            search = research(client, original, [q for q in questions if q['id'] in ids])
            update.update(search_evidence=search, estimated_volume=volume,
                          opportunity=score(original, snapshot, volume), research_refreshed_at=utcnow())
            error = None
        except (ValueError, RuntimeError, OSError, KeyError) as exc:
            error = str(exc)
        with lock(root, 'queue'):
            if not path.exists() or any((root / 'queue' / state / path.name).exists() for state in STATES if state != 'pending'):
                continue
            current = read_json(path)
            if any(current.get(k) != original.get(k) for k in ('target_query', 'owner_host', 'target_url')):
                continue
            # Preserve a concurrent source-builder update; merge only research-owned fields.
            blockers = current.get('blockers', [])
            if not error:
                prefixes = ('DATAFORSEO-', 'RESEARCH-REFRESH:', 'BLOCKED-GSC', 'HOLD-CANNIBALIZATION', 'HOLD-EXISTING-OWNER')
                blockers = [b for b in blockers if not str(b).startswith(prefixes)]
            else:
                blockers = [b for b in blockers if not str(b).startswith('RESEARCH-REFRESH:')]
                blockers.append('RESEARCH-REFRESH: ' + error)
            current.update(update, blockers=blockers, updated_at=utcnow())
            atomic_json(path, current)
        results.append({'slug': slug, 'status': 'blocked' if error else 'refreshed', 'error': error})
    return results


def orchestrate(root, config, limit=None, client=None, snapshot=None):
    root = Path(root)
    initialize(root)
    with lock(root, 'orchestrator'):
        clusters, questions, hashes = runbooks(config['runbook_directory'])
        candidate_data = read_json(config['candidate_path'])
        candidates = candidate_data['candidates'] if isinstance(candidate_data, dict) else candidate_data
        content_path = Path(config['verified_content_path'])
        content = read_json(content_path) if content_path.exists() else {}
        week = datetime.now(ZoneInfo('America/Chicago')).strftime('%G-W%V')
        report = {'week': week, 'ran_at': utcnow(), 'queued': [], 'held': [], 'errors': [], 'runbooks': hashes}
        jobs = [read_json(p) for state in STATES for p in (root / 'queue' / state).glob('*.json')]
        existing = {j['slug'] for j in jobs}
        existing_intents = {(owner_key(j.get('owner_host', '')), normalize(j.get('target_query', ''))) for j in jobs}
        def job_week(job):
            if job.get('orchestrator_week'):
                return job['orchestrator_week']
            try:
                return datetime.fromisoformat(job['created_at']).astimezone(ZoneInfo('America/Chicago')).strftime('%G-W%V')
            except (ValueError, KeyError):
                return None
        count = sum(job_week(j) == week and j.get('kind', 'seo_page') == 'seo_page' for j in jobs)
        cap = int(config['jobs_per_week'])
        if cap < 1 or (limit is not None and limit < 1):
            raise ValueError('Weekly job count must be positive')
        remaining = max(0, min(cap - count, limit if limit is not None else cap))
        report['weekly_remaining'] = remaining
        pending = [j for j in jobs if j.get('gsc_property') and j.get('kind', 'seo_page') == 'seo_page'
                   and (root / 'queue/pending' / (j['slug'] + '.json')).exists()]
        if pending:
            snapshot = snapshot if snapshot is not None else gsc_snapshot(root, config['gsc'])
            client = client or DataForSEO(root, config['dataforseo'])
            report['refreshed'] = refresh_pending(root, config, pending, snapshot, client, questions,
                                                  min(cap, limit if limit is not None else cap))
            report['errors'].extend(r for r in report['refreshed'] if r['error'])
        eligible = []
        for candidate in candidates:
            validate_slug(candidate['slug'])
            if candidate['slug'] in existing or (owner_key(candidate['owner_host']), normalize(candidate['target_query'])) in existing_intents:
                continue
            if candidate['cluster'] not in clusters:
                raise ValueError('Candidate cluster absent from topical-map.md: ' + candidate['cluster'])
            if urlsplit(candidate['target_url']).hostname != candidate['owner_host']:
                raise ValueError('Candidate URL owner mismatch')
            if candidate.get('relevance', .5) == 0:
                report['held'].append({'slug': candidate['slug'], 'reason': 'unsupported-offering'})
                continue
            eligible.append(candidate)
        if remaining and eligible:
            snapshot = snapshot if snapshot is not None else gsc_snapshot(root, config['gsc'])
            report['gsc'] = {k: {'status': v['status'], 'query_rows': len(v.get('query_rows', [])),
                                 'page_rows': len(v.get('page_rows', []))} for k, v in snapshot['properties'].items()}
            client = client or DataForSEO(root, config['dataforseo'])
            volumes = {}
            try:
                entry = client.call('volume', {'keywords': sorted({c['target_query'] for c in eligible}),
                    'location_name': config['dataforseo']['location_name'], 'language_code': config['dataforseo']['language_code']})
                for task in successful(entry):
                    for item in task.get('result') or []:
                        volumes[normalize(item['keyword'])] = item.get('search_volume')
                report['volume_cache_key'] = entry['cache_key']
            except (ValueError, RuntimeError, OSError, KeyError) as exc:
                report['errors'].append(str(exc))
            ranked = [(c, score(c, snapshot, volumes.get(normalize(c['target_query'])))) for c in eligible]
            ranked.sort(key=lambda pair: (-(pair[1]['priority_score'] if pair[1]['priority_score'] is not None else -1),
                        {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}[pair[1]['confidence']], pair[1]['hours'], pair[0]['target_url']))
            for candidate, scoring in ranked:
                overlap = cannibalization(candidate, snapshot)
                if overlap['status'] != 'clear-in-observed-window':
                    report['held'].append({'slug': candidate['slug'], 'reason': overlap['status'], 'cannibalization': overlap})
                    continue
                if len(report['queued']) >= remaining:
                    break
                try:
                    search = research(client, candidate, [q for q in questions if q['id'] in candidate.get('ai_question_ids', [])])
                    job = dict(candidate)
                    # Only content fields may be supplied by the verified source producer.
                    evidence = content.get(candidate['slug'], {})
                    for key in ('title', 'outline', 'meta_description', 'sections', 'faq', 'business', 'source_evidence',
                                'internal_links', 'staging_read_status', 'topology_status', 'topology_evidence',
                                'builder', 'built_at', 'builder_blockers', 'content_limitations'):
                        if key in evidence:
                            job[key] = evidence[key]
                    job.setdefault('source_evidence', [])
                    job.setdefault('internal_links', [])
                    job.update(status='pending', kind='seo_page', orchestrator_week=week, created_at=utcnow(),
                        approval_required=True, publication_authorized=False,
                        estimated_volume=volumes.get(normalize(candidate['target_query'])), opportunity=scoring,
                        cannibalization=overlap, search_evidence=search,
                        gsc_check=query_evidence(candidate, snapshot),
                        ai_citation_evidence=citation_gaps(root, questions, candidate), runbook_hashes=hashes)
                    job['blockers'] = list(job.get('builder_blockers', []))
                    if not job['source_evidence']:
                        job['blockers'].append('VERIFIED-CONTENT-MISSING: source producer must supply dated claims and checked links; generator will hold.')
                    with lock(root, 'queue'):
                        if any((root / 'queue' / state / f"{job['slug']}.json").exists() for state in STATES):
                            continue
                        atomic_json(root / 'queue' / 'pending' / f"{job['slug']}.json", job)
                    report['queued'].append(job['slug'])
                except (ValueError, RuntimeError, OSError, KeyError) as exc:
                    report['errors'].append({'slug': candidate['slug'], 'error': str(exc)})
        atomic_json(root / 'runs' / f'orchestrator-{week}.json', report)
        atomic_json(root / 'orchestrator-last-run.json', report)
        return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=DEFAULT_ROOT)
    parser.add_argument('--config', type=Path, default=DEFAULT_CONFIG)
    parser.add_argument('--limit', type=int)
    parser.add_argument('--init-only', action='store_true', help='Create directory structure without provider calls')
    args = parser.parse_args()
    try:
        if args.init_only:
            initialize(args.root)
            return 0
        result = orchestrate(args.root, read_json(args.config), args.limit)
        print(json.dumps(result, indent=2))
        return int(bool(result['errors']))
    except (ValueError, RuntimeError, OSError, KeyError, TypeError) as exc:
        print(json.dumps({'error': str(exc)}))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
