#!/usr/bin/env python3
"""Assemble dated source-backed inventory briefs; refresh pending jobs only.

This module cannot create approvals, mutate review artifacts or invent public routes.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone, timedelta
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import urlsplit, urljoin, parse_qs

try:
    from .common import atomic_json, read_json, lock, validate_slug, utcnow
except ImportError:
    from common import atomic_json, read_json, lock, validate_slug, utcnow

REPO = Path(__file__).resolve().parents[1]
INVENTORY_CLUSTERS = {'Used vehicles', 'New Toyota', 'New Chevrolet'}


def _stamp(value):
    result = datetime.fromisoformat(str(value).replace('Z', '+00:00'))
    if result.tzinfo is None:
        raise ValueError('Evidence timestamps require timezone')
    return result


def validate_inventory(data: dict, now: datetime) -> dict:
    if data.get('status') != 'verified':
        raise ValueError('Fresh DealerVault aggregate evidence unavailable')
    feed = data['feed']
    if feed.get('verified') is not True or feed.get('source_type') != 'DealerVault' or not re.fullmatch(r'[0-9a-f]{64}', feed.get('sha256', '')):
        raise ValueError('DealerVault source proof missing')
    if feed.get('dealer_id') != 'DVD56054' or feed.get('location') != '9':
        raise ValueError('Inventory store mapping not verified')
    if not timedelta(0) <= now - _stamp(feed['modified_at']) <= timedelta(hours=48):
        raise ValueError('DealerVault snapshot stale/future-dated')
    if not timedelta(0) <= now - _stamp(feed['retrieved_at']) <= timedelta(hours=48) or _stamp(feed['valid_until']) <= now:
        raise ValueError('DealerVault evidence retrieval or expiry invalid')
    groups = data['aggregates'].get('groups')
    if not isinstance(groups, list) or not groups:
        raise ValueError('Missing type/make/model/style aggregate groups')
    if any(not isinstance(g.get('count'), int) or isinstance(g['count'], bool) or g['count'] <= 0 for g in groups):
        raise ValueError('Invalid aggregate count')
    if sum(g['count'] for g in groups) != feed['row_count']:
        raise ValueError('Aggregate counts do not reconcile to source row count')
    return feed


def choose_groups(candidate: dict, groups: list) -> tuple[list, dict, str]:
    cluster = candidate['cluster']
    scope = (candidate['slug'] + ' ' + candidate.get('target_query', '')).lower()
    if cluster in {'New Toyota', 'New Chevrolet'}:
        make = 'TOYOTA' if cluster == 'New Toyota' else 'CHEVROLET'
        models = ['TUNDRA', 'RAV4'] if make == 'TOYOTA' else ['SILVERADO', 'EQUINOX']
        found = [model for model in models if model.lower() in scope]
        if len(found) != 1:
            raise ValueError('Unsupported/ambiguous model; no inferred model mapping')
        filters = {'type_code': 'N', 'make': make, 'model_prefix': found[0]}
        selected = [g for g in groups if g['type_code'] == 'N' and g['make'] == make and (g['model'] == found[0] or g['model'].startswith(found[0] + ' '))]
        label = make.title() + ' ' + ('RAV4' if found[0] == 'RAV4' else found[0].title())
    elif cluster == 'Used vehicles' and 'truck' in scope:
        filters = {'type_code': 'U', 'style': 'PICKUP'}
        selected = [g for g in groups if g['type_code'] == 'U' and g['style'] == 'PICKUP']
        label = 'pickup'
    else:
        raise ValueError('Unsupported vehicle classification; WAGON labels do not prove SUV classification')
    if not selected:
        raise ValueError('No matching records in the dated inventory snapshot')
    return selected, filters, label


class PageProof(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.canonical, self.robots, self.title, self.h1 = [], [], '', ''
        self.links = []
        self.active = None
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a' and attrs.get('href'):
            self.links.append(attrs['href'])
        if tag == 'link' and 'canonical' in attrs.get('rel', '').lower().split():
            self.canonical.append(attrs.get('href', ''))
        if tag == 'meta' and attrs.get('name', '').lower() in {'robots', 'googlebot'}:
            self.robots.append(attrs.get('content', '').lower())
        if tag in {'title', 'h1'}:
            self.active = tag
    def handle_data(self, data):
        if self.active == 'title': self.title += data
        if self.active == 'h1': self.h1 += data
    def handle_endtag(self, tag):
        if tag == self.active: self.active = None


def verify_link(url: str, candidate: dict, fetch, now: datetime) -> tuple[dict, dict, dict]:
    """Only exact same-owner, indexable, canonical inventory destinations qualify."""
    parsed = urlsplit(url)
    if parsed.scheme != 'https' or parsed.hostname != candidate['owner_host'] or parsed.username or parsed.password or parsed.fragment or parsed.port not in {None,443}:
        raise ValueError('Link outside HTTPS page-owner allowlist')
    if any(k in parsed.query.lower() for k in ['utm_', 'gclid', 'fbclid', 'vin=']) or re.search(r'/vehicle/|[A-HJ-NPR-Z0-9]{17}', parsed.path):
        raise ValueError('Tracking/VDP links are outside permanent inventory topology')
    page = fetch(url)
    final = page['url']
    if page['status'] != 200 or urlsplit(final).hostname != candidate['owner_host'] or urlsplit(final).scheme != 'https':
        raise ValueError('Link does not resolve to HTTP 200 on the page owner')
    parser = PageProof(); parser.feed(page['text'])
    canonicals = [urljoin(final, value) for value in parser.canonical]
    if len(canonicals) != 1:
        raise ValueError('Destination requires exactly one canonical')
    canonical = canonicals[0]
    canonical_proof = {}
    if any('noindex' in value or 'none' in value.split(',') for value in parser.robots + [page.get('x_robots_tag', '').lower()]):
        raise ValueError('Destination is not indexable')
    visible = (parser.title + ' ' + parser.h1).lower()
    scope = (candidate['slug'] + ' ' + candidate.get('target_query', '')).lower()
    expected = ['used', 'truck'] if candidate['cluster'] == 'Used vehicles' else ['new', 'toyota' if candidate['cluster'] == 'New Toyota' else 'chevrolet']
    if candidate['cluster'] != 'Used vehicles':
        expected += [word for word in ['tundra', 'rav4', 'silverado', 'equinox'] if word in scope]
    if candidate['cluster'] == 'Used vehicles' and not re.search(r'\bused\s+trucks?\b', visible):
        raise ValueError('Destination is general used inventory rather than a confirmed truck category')
    if any(word not in visible for word in expected):
        raise ValueError('Visible title/H1 does not confirm intended make/model/type filters')
    if canonical != final:
        c, f = urlsplit(canonical), urlsplit(final)
        if (candidate['cluster'] == 'Used vehicles' or final != url or not f.query or c.query or c.fragment
                or (c.scheme,c.hostname,c.path,c.port) != (f.scheme,f.hostname,f.path,f.port)):
            raise ValueError('Canonical mismatch does not qualify for parent-inventory proof')
        intended_make = 'Toyota' if candidate['cluster'] == 'New Toyota' else 'Chevrolet'
        intended_model = next((word for word in ['Tundra','RAV4','Silverado','Equinox'] if word.lower() in scope), '')
        query = {key.lower():values for key,values in parse_qs(f.query).items()}
        model_values = query.get('model',[])
        if not intended_model or not any(value.lower() == intended_model.lower() for value in model_values):
            raise ValueError('Exact intended model filter is not preserved in final URL')
        if len(query.get('make', [])) != 1 or any(value.lower() != intended_make.lower() for value in query['make']):
            raise ValueError('Final make filter mismatches intended make')
        parent = fetch(canonical)
        if parent['status'] != 200 or parent['url'] != canonical:
            raise ValueError('Parent inventory canonical lacks exact HTTP 200 proof')
        canonical_proof = {'canonical_scope':'parent-inventory','canonical_verified':True,'canonical_http_status':200,
                           'filter_verified':True,'requested_url':url,'final_url':final,'intended_make':intended_make,
                           'intended_model':intended_model,'visible_heading':' '.join((parser.title+' '+parser.h1).split()),
                           'canonical_response_sha256':hashlib.sha256(parent['text'].encode()).hexdigest()}
    anchor = ' '.join((parser.h1 or parser.title).split())[:160]
    if len(anchor.split()) < 2:
        raise ValueError('No descriptive destination heading')
    digest = hashlib.sha256(page['text'].encode()).hexdigest()
    eid = 'sitecrawl-' + digest[:16]
    proof = {'id': eid, 'source_type': 'SiteCrawl', 'verified': True, 'url': final, 'retrieved_at': now.isoformat(), 'checked_at': now.isoformat(),
             'valid_until': (now + timedelta(days=1)).isoformat(), 'response_sha256': digest, 'http_status': 200, 'canonical': canonical, **canonical_proof,
             'claims': [final, anchor], 'scope': 'links'}
    link = {'url': final, 'anchor': anchor, 'http_status': 200, 'canonical': canonical, **canonical_proof, 'checked_at': now.isoformat(), 'evidence_ids': [eid],
            'section': 'Related dealership resources', 'purpose': 'Matching permanent inventory destination', 'link_type': 'same-site'}
    crawl = {'requested_url': url, 'final_url': final, 'http_status': 200, 'canonical': canonical, **canonical_proof, 'indexable': canonical == final,
             'indexability_checks': ['HTTP 200', 'meta robots', 'X-Robots-Tag'], 'robots_txt_checked': False, 'heading': anchor, 'verified_filter_terms': expected, 'checked_at': now.isoformat(), 'response_sha256': digest}
    return link, proof, crawl


def live_fetch(url: str) -> dict:
    import requests
    # Resolve redirects manually to prevent an unexpected host/HTTP transition.
    original_host = urlsplit(url).hostname
    for _ in range(4):
        response = requests.get(url, timeout=(8, 20), allow_redirects=False, stream=True, headers={'User-Agent':'MotorInn-SEO-Review/1.0'})
        if response.is_redirect:
            next_url = urljoin(url, response.headers.get('Location', ''))
            response.close()
            if urlsplit(next_url).scheme != 'https' or urlsplit(next_url).hostname != original_host or urlsplit(next_url).port not in {None,443} or urlsplit(next_url).username or urlsplit(next_url).password:
                raise ValueError('Cross-host or insecure redirect refused')
            url = next_url
            continue
        raw = bytearray()
        for chunk in response.iter_content(65536):
            raw.extend(chunk)
            if len(raw) > 2 * 1024 * 1024:
                response.close(); raise ValueError('Destination exceeds bounded 2 MiB crawl')
        content = {'url':response.url, 'status':response.status_code, 'text':bytes(raw).decode(response.encoding or 'utf-8', errors='replace'), 'x_robots_tag':response.headers.get('X-Robots-Tag','')}
        response.close()
        return content
    raise ValueError('Too many destination redirects')


def _own_result_urls(value, owner):
    # Search only the supplied DataForSEO search_evidence subtree, never arbitrary job fields.
    results = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key in {'url', 'domain_url'} and isinstance(child, str) and urlsplit(child).hostname == owner:
                results.append(child)
            elif isinstance(child, (dict, list)):
                results.extend(_own_result_urls(child, owner))
    elif isinstance(value, list):
        for child in value: results.extend(_own_result_urls(child, owner))
    return results


def assemble(candidate: dict, inventory: dict, pending: dict | None = None, fetch=live_fetch, now: datetime | None = None) -> dict:
    now = now or datetime.now(timezone.utc)
    result = {'slug':candidate['slug'], 'builder':'dealer-vault-snapshot-v1', 'built_at':now.isoformat(), 'builder_blockers':[], 'topology_status':'blocked', 'publication_authorized':False}
    if candidate.get('cluster') not in INVENTORY_CLUSTERS:
        result['builder_blockers'] = ['No verified source for service, financing, trade-in or sell-to-us claims']
        return result
    try:
        feed = validate_inventory(inventory, now)
        groups, filters, label = choose_groups(candidate, inventory['aggregates']['groups'])
    except (ValueError, KeyError, TypeError) as exc:
        result['builder_blockers'] = [str(exc)]
        return result
    count = sum(row['count'] for row in groups)
    code = filters['type_code']
    date = _stamp(feed['modified_at']).strftime('%Y-%m-%d')
    when = _stamp(feed['modified_at']).strftime('%Y-%m-%d at %H:%M UTC')
    label_title = 'Pickup Trucks' if code == 'U' else label
    title = f'{label_title} in Carroll: Inventory Snapshot'
    meta = f'Explore a dated selection of {count} {label} vehicles from the {date} inventory snapshot and check the linked inventory for updates.'
    if not 120 <= len(meta) <= 158:
        result['builder_blockers'] = ['Derived metadata does not fit required length; no padding claim invented']
        return result
    headline = f'This selection from Carroll’s inventory snapshot received on {when} includes {count} {label} vehicles.'
    method = 'This selection reflects the inventory snapshot at that time. See the linked inventory for current details.'
    limit = 'Vehicle availability can change after an inventory snapshot. This selection does not reserve a vehicle or guarantee current availability.'
    groups_text = [f"{row['count']} {row['make'].title()} {row['model']} vehicles appear in this dated selection." for row in groups]
    eid = 'dealervault-derived-' + feed['sha256'][:12] + '-' + candidate['slug']
    claims = [title, meta, headline, method, limit] + groups_text
    source = {key:value for key,value in feed.items() if key not in {'claims','row_count','dealer_id','location'}}
    source.update({'id':eid, 'claims':claims, 'transformation':{'algorithm':'exact-group-filter-and-count-v1', 'input_sha256':feed['sha256'], 'filters':filters, 'matching_groups':groups,
                                                          'group_total':count, 'code_semantics':'Original N/U source codes retained explicitly; no added stock or sale guarantee'}})
    result.update({'title':title, 'meta_description':meta, 'source_evidence':[source], 'outline':['Dated inventory snapshot','Recorded inventory details','How to use this snapshot'],
                   'sections':[{'heading':'Dated inventory snapshot','claims':[{'text':headline,'evidence_ids':[eid]}]},
                               {'heading':'Recorded inventory details','claims':[{'text':s,'evidence_ids':[eid]} for s in groups_text]},
                               {'heading':'How to use this snapshot','claims':[{'text':s,'evidence_ids':[eid]} for s in [method,limit]]}],
                   'faq':[{'question':'What does this inventory count describe?', 'answer':headline,'evidence_ids':[eid]},
                          {'question':'Does this snapshot guarantee availability?', 'answer':limit,'evidence_ids':[eid]}],
                   'internal_links':[], 'topology_evidence':{'scope':'Bounded candidate-to-inventory destination checks only; not a whole-site crawl','checks':[],'failures':[]},
                   'content_limitations':['Inventory snapshot only; no financing, service, pricing, business-name or model-feature assertions.','Used inventory staging comparison remains a separate unresolved gate.']})
    urls = [row.get('url') if isinstance(row,dict) else row for row in candidate.get('internal_links', [])]
    urls += _own_result_urls((pending or {}).get('search_evidence', {}), candidate['owner_host'])
    if not urls:
        # The configured owner homepage is the discovery root; candidate paths are never guessed.
        homepage = 'https://' + candidate['owner_host'] + '/'
        try:
            home = fetch(homepage)
            if home['status'] != 200 or urlsplit(home['url']).hostname != candidate['owner_host']:
                raise ValueError('Owner homepage unavailable for destination discovery')
            parser = PageProof(); parser.feed(home['text'])
            discovered = list(dict.fromkeys(urljoin(home['url'], href) for href in parser.links))
            tokens = ['used', 'truck'] if code == 'U' else ['new', filters['model_prefix'].lower()]
            ranked = sorted((url for url in discovered if urlsplit(url).hostname == candidate['owner_host']),
                            key=lambda url: sum(token in url.lower() for token in tokens), reverse=True)
            urls = [url for url in ranked if any(token in url.lower() for token in tokens)][:3]
            result['topology_evidence']['discovery'] = {'url':home['url'], 'http_status':200, 'checked_at':now.isoformat(),
                'response_sha256':hashlib.sha256(home['text'].encode()).hexdigest(), 'discovered_link_count':len(discovered), 'selected_urls':urls}
        except Exception as exc:
            result['topology_evidence']['failures'].append({'url':homepage,'error':str(exc)[:300]})
    urls = list(dict.fromkeys(url for url in urls if isinstance(url,str)))[:3]
    for url in urls:
        try:
            link, proof, crawl = verify_link(url,candidate,fetch,now)
            result['internal_links'].append(link); result['source_evidence'].append(proof); result['topology_evidence']['checks'].append(crawl)
        except Exception as exc:
            result['topology_evidence']['failures'].append({'url':url, 'error':str(exc)[:300]})
    if result['internal_links']:
        result['topology_status'] = 'verified'
    else:
        result['builder_blockers'].append('No live canonical inventory destination with confirmed matching filters; topology remains unverified')
    if code == 'U' and (pending or {}).get('staging_read_status') != 'verified':
        result['builder_blockers'].append('BLOCKED-STAGING-READ: used-inventory staged package comparison unavailable')
    return result


CONTENT_FIELDS = {'title','meta_description','source_evidence','outline','sections','faq','internal_links','topology_status','topology_evidence','content_limitations','builder','built_at','builder_blockers'}


def build(root: Path, config: dict, fetch=live_fetch) -> dict:
    root = Path(root)
    candidate_data = read_json(config.get('candidate_path', REPO/'automation/config/candidates.json'))
    candidates = candidate_data if isinstance(candidate_data,list) else candidate_data['candidates']
    try: inventory = read_json(root/'inputs/inventory-evidence.json')
    except (OSError, ValueError): inventory = {'status':'blocked'}
    output, results = {}, []
    fetch_cache = {}
    def cached_fetch(url):
        if url not in fetch_cache:
            fetch_cache[url] = fetch(url)
        return fetch_cache[url]
    with lock(root,'queue'):
        for candidate in candidates:
            slug = validate_slug(candidate['slug'])
            path = root/'queue/pending'/f'{slug}.json'
            pending = read_json(path) if path.exists() else None
            brief = assemble(candidate,inventory,pending,cached_fetch)
            output[slug] = brief
            if pending and pending.get('kind') != 'content_post' and not any((root/'queue'/state/f'{slug}.json').exists() for state in ['drafts','approved','hold','ready','rejected']):
                # Remove only this builder's prior blockers; research/GSC/provider gates stay intact.
                old_blockers = set(pending.get('builder_blockers',[]))
                blockers = [x for x in pending.get('blockers',[]) if x not in old_blockers]
                for field in CONTENT_FIELDS - {'title','outline'}:
                    pending.pop(field,None)
                pending.update({key:value for key,value in brief.items() if key in CONTENT_FIELDS})
                pending['blockers'] = list(dict.fromkeys(blockers + brief['builder_blockers']))
                pending['qa_passed'] = False
                pending['status'] = 'pending'
                atomic_json(path,pending)
            results.append({'slug':slug,'status':'blocked' if brief['builder_blockers'] else 'assembled','blockers':brief['builder_blockers']})
        atomic_json(root/'inputs/verified-content.json',output)
    return {'candidates':results,'assembled':sum(r['status']=='assembled' for r in results),'blocked':sum(r['status']=='blocked' for r in results)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=REPO/'pipeline')
    parser.add_argument('--config',type=Path,default=REPO/'automation/config.json')
    args=parser.parse_args()
    result=build(args.root,read_json(args.config))
    print(json.dumps(result,indent=2))
    return int(bool(result['blocked']))


if __name__=='__main__':
    raise SystemExit(main())
