"""Bounded read clients. Reserve spend before network I/O; never retry ambiguous POSTs."""
import base64
from datetime import datetime, timedelta, timezone
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re
import shlex
import subprocess
from urllib.request import Request, urlopen
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo
from common import atomic_json, fresh, lock, read_json, utcnow

ENDPOINTS = {
    'volume': ('keywords_data/google_ads/search_volume/live', 'kw_data_google_ads_search_volume'),
    'serp': ('serp/google/organic/live/advanced', 'serp_organic_live_advanced'),
    'screenshot': ('serp/screenshot', 'serp_screenshot'),
}
TASK_FIELDS = {
    'volume': {'keywords', 'location_name', 'language_code'},
    'serp': {'keyword', 'location_name', 'language_code', 'depth', 'device', 'os',
             'load_async_ai_overview', 'calculate_rectangles'},
    'screenshot': {'task_id', 'browser_screen_scale_factor'},
}


def validate_task(kind, task):
    if not isinstance(task, dict) or set(task) - TASK_FIELDS[kind]:
        raise ValueError('Unknown or unpriced task fields are forbidden')
    for name in ('location_name', 'language_code'):
        if name in task and (not isinstance(task[name], str) or not task[name].strip() or len(task[name]) > 200):
            raise ValueError('Invalid locale field')
    if kind == 'serp':
        if task.get('device', 'desktop') not in ('desktop', 'mobile') or task.get('os', 'windows') not in ('windows', 'macos', 'android', 'ios'):
            raise ValueError('Unsupported SERP device or operating system')
        for name in ('load_async_ai_overview', 'calculate_rectangles'):
            if name in task and type(task[name]) is not bool:
                raise ValueError('Price-sensitive SERP options must be booleans')
    if kind == 'screenshot' and 'browser_screen_scale_factor' in task:
        scale = task['browser_screen_scale_factor']
        if type(scale) not in (float, int) or not .5 <= scale <= 3:
            raise ValueError('Screenshot scale outside bounded range')
    words = task.get('keywords', []) if kind == 'volume' else [task.get('keyword', '')] if kind == 'serp' else []
    if not isinstance(words, list) or any(not isinstance(word, str) or not word.strip() or len(word) > 700 for word in words):
        raise ValueError('Invalid keyword strings')


def env_credentials(path):
    values = {}
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            key, value = line.removeprefix('export ').split('=', 1)
            values[key.strip()] = value.strip().strip('\"\'')
    return values['DATAFORSEO_USERNAME'], values['DATAFORSEO_PASSWORD']


class DataForSEO:
    def __init__(self, root, config, transport=None):
        self.root = Path(root)
        self.config = config
        self.policy = read_json(config['policy_path'])
        self.transport = transport or self._request

    def _request(self, endpoint, payload):
        username, password = env_credentials(self.config['credentials_path'])
        auth = base64.b64encode((username + ':' + password).encode()).decode()
        request = Request('https://api.dataforseo.com/v3/' + endpoint,
            data=json.dumps(payload).encode(), headers={'Authorization': 'Basic ' + auth, 'Content-Type': 'application/json'})
        with urlopen(request, timeout=60) as response:
            return json.load(response)

    def call(self, kind, task):
        if kind not in ENDPOINTS:
            raise ValueError('Endpoint not allowlisted')
        validate_task(kind, task)
        endpoint, price_key = ENDPOINTS[kind]
        if kind == 'volume' and not 1 <= len(task.get('keywords', [])) <= self.policy['rules']['maxKeywordBatchSize']:
            raise ValueError('Keyword batch outside cost policy')
        if kind == 'serp' and task.get('depth') != 10:
            raise ValueError('SERP depth must be 10')
        words = task.get('keywords', []) if kind == 'volume' else [task.get('keyword', '')]
        if any(re.search(r'\b[a-z]+:', word, re.I) for word in words):
            raise ValueError('Search operators forbidden by policy')
        if kind == 'screenshot' and not re.fullmatch(r'[A-Za-z0-9-]+', task.get('task_id', '')):
            raise ValueError('Screenshot requires a provider task ID')
        payload = [task]
        key = hashlib.sha256(json.dumps([endpoint, payload], sort_keys=True).encode()).hexdigest()
        cache = self.root / 'cache' / ('dataforseo-' + key + '.json')
        # Budget lock spans cache lookup and request, preventing duplicate concurrent charges.
        with lock(self.root, 'dataforseo-budget'):
            if cache.exists():
                entry = read_json(cache)
                if fresh(entry['retrieved_at'], min(7, self.policy.get('cacheDays', 7))):
                    return entry
            ledger_path = self.root / 'cost-ledger.json'
            ledger = read_json(ledger_path) if ledger_path.exists() else {'days': {}}
            day = datetime.now(ZoneInfo('America/Chicago')).date().isoformat()
            state = ledger['days'].setdefault(day, {'charged_or_reserved': 0, 'calls': []})
            if state.get('blocked'):
                raise RuntimeError('BUDGET-BLOCKED: provider exceeded reservation; reconcile ledger')
            reservation = Decimal(str(self.policy['endpointEstimatesUsd'][price_key]))
            cap = min(Decimal('2'), Decimal(str(self.policy['dailyHardCapUsd'])), Decimal(str(self.policy['dailyAutoApproveUsd'])))
            spent = Decimal(str(state['charged_or_reserved']))
            if spent + reservation > cap:
                raise RuntimeError('BUDGET-CAP: request would exceed daily budget')
            record = {'key': key, 'kind': kind, 'reserved': float(reservation), 'status': 'uncertain', 'at': utcnow()}
            # Uncertain requests remain reserved. A crash or timeout cannot refund spend.
            if any(row['key'] == key and row['status'] == 'uncertain' for d in ledger['days'].values() for row in d['calls']):
                raise RuntimeError('AMBIGUOUS-PRIOR-REQUEST: reconcile before retry')
            state['calls'].append(record)
            state['charged_or_reserved'] = float(spent + reservation)
            atomic_json(ledger_path, ledger)
            try:
                response = self.transport(endpoint, payload)
            except Exception as exc:
                raise RuntimeError('DATAFORSEO-TRANSPORT-' + type(exc).__name__ + ': reservation retained') from None
            entry = {'retrieved_at': utcnow(), 'endpoint': endpoint, 'request': payload,
                     'response': response, 'cache_key': key}
            # Persist received evidence before interpreting billing. Diagnostic entries
            # are never eligible cache hits and cannot bypass an uncertain reservation.
            diagnostic = self.root / 'cache' / ('uncertain-response-' + key + '.json')
            atomic_json(diagnostic, entry)
            try:
                actual = Decimal(str(response['cost']))
                if not actual.is_finite() or actual < 0:
                    raise ValueError('Invalid cost')
                # Retain conservative reservation even on a reported lower cost.
                charged = max(actual, reservation)
                state['charged_or_reserved'] = float(spent + charged)
                record.update(status='completed', actual=float(actual))
                state['blocked'] = actual > reservation
                atomic_json(ledger_path, ledger)
            except (KeyError, ValueError, ArithmeticError):
                raise RuntimeError('DATAFORSEO-UNKNOWN-COST: reservation retained') from None
            # Preserve every response, including failed provider tasks, for seven-day reuse.
            atomic_json(cache, entry)
            diagnostic.unlink(missing_ok=True)
            return entry

    def save_screenshot(self, entry):
        """Retain the image locally; provider screenshot URLs expire after one day."""
        target = self.root / 'cache' / ('screenshot-' + entry['cache_key'] + '.png')
        if target.exists() and fresh(entry['retrieved_at']):
            return target
        results = [r for task in successful(entry) for r in task.get('result') or []]
        url = next((r.get('items', [{}])[0].get('image') for r in results if r.get('items')), None)
        # The documented endpoint returns screenshot under result[].items[].image.
        if not url:
            raise ValueError('Screenshot response has no image URL')
        parsed = urlsplit(url)
        if parsed.scheme != 'https' or not (parsed.hostname or '').endswith('.dataforseo.com'):
            raise ValueError('Screenshot URL is not a DataForSEO HTTPS host')
        with urlopen(url, timeout=45) as response:
            data = response.read(20 * 1024 * 1024 + 1)
        if len(data) > 20 * 1024 * 1024 or not data.startswith(b'\x89PNG\r\n\x1a\n'):
            raise ValueError('Screenshot is not a bounded PNG image')
        temp = target.with_suffix('.tmp')
        temp.write_bytes(data)
        temp.replace(target)
        return target


def successful(entry):
    response = entry['response']
    tasks = response.get('tasks') or []
    if response.get('status_code') != 20000 or not tasks or any(t.get('status_code') != 20000 for t in tasks):
        codes = [t.get('status_code') for t in tasks]
        raise RuntimeError('DATAFORSEO-TASK-FAILED:' + str(codes))
    return tasks


def gsc_snapshot(root, config, transport=None):
    end = datetime.now(timezone.utc).date() - timedelta(days=3)
    request = {'credential_path': config['credential_path'], 'properties': config['properties'],
               'start_date': (end - timedelta(days=27)).isoformat(), 'end_date': end.isoformat()}
    cache_key = hashlib.sha256(json.dumps(request, sort_keys=True).encode()).hexdigest()
    path = Path(root) / 'cache' / ('gsc-' + cache_key + '.json')
    if path.exists():
        entry = read_json(path)
        if fresh(entry.get('retrieved_at'), 1):
            return entry
    helper = Path(__file__).with_name('gsc_remote.py').read_text()
    if transport:
        result = transport(request)
    else:
        host = config['ssh_host']
        if not re.fullmatch(r'[a-zA-Z0-9_.@-]+', host) or host.startswith('-'):
            raise ValueError('Invalid SSH host')
        remote = shlex.join([config.get('python', 'python3'), '-', json.dumps(request)])
        proc = subprocess.run(['ssh', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=10', host, remote],
                              input=helper, capture_output=True, text=True, timeout=180)
        if proc.returncode:
            raise RuntimeError('GSC-SSH-FAILED (credentials retained on mini)')
        result = json.loads(proc.stdout)
    if 'error' in result:
        raise RuntimeError('GSC-REMOTE-' + result['error'])
    entry = {'retrieved_at': utcnow(), 'request': request, **result}
    atomic_json(path, entry)
    return entry
