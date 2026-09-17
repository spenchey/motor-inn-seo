"""Read-only GSC helper streamed to the Mac mini; credentials never leave it."""
import json
import sys
from urllib.parse import quote
import warnings
warnings.filterwarnings('ignore')
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession


def run(request):
    credentials = service_account.Credentials.from_service_account_file(
        request['credential_path'], scopes=['https://www.googleapis.com/auth/webmasters.readonly'])
    session = AuthorizedSession(credentials)
    sites_response = session.get('https://www.googleapis.com/webmasters/v3/sites', timeout=30)
    sites_response.raise_for_status()
    sites = {s['siteUrl']: s['permissionLevel'] for s in sites_response.json().get('siteEntry', [])}
    results = {}
    for prop in request['properties']:
        if sites.get(prop) not in ('siteOwner', 'siteFullUser', 'siteRestrictedUser'):
            results[prop] = {'status': 'BLOCKED-NO-ACCESS', 'permission': sites.get(prop)}
            continue
        result = {'status': 'ok', 'permission': sites[prop], 'query_rows': [], 'page_rows': [],
                  'start_date': request['start_date'], 'end_date': request['end_date']}
        for dimensions, key in ((['query'], 'query_rows'), (['query', 'page'], 'page_rows')):
            start = 0
            while True:
                response = session.post('https://www.googleapis.com/webmasters/v3/sites/' + quote(prop, safe='') + '/searchAnalytics/query',
                    json={'startDate': request['start_date'], 'endDate': request['end_date'], 'dimensions': dimensions,
                          'rowLimit': 25000, 'startRow': start, 'dataState': 'final', 'type': 'web'}, timeout=45)
                if not response.ok:
                    result = {'status': 'BLOCKED-QUERY', 'http_status': response.status_code}
                    break
                rows = response.json().get('rows', [])
                result[key].extend(rows)
                if len(rows) < 25000:
                    break
                start += 25000
                if start >= 100000:
                    result['status'] = 'BLOCKED-TRUNCATED'
                    break
            if result['status'] != 'ok':
                break
        results[prop] = result
    return {'properties': results}


if __name__ == '__main__':
    try:
        print(json.dumps(run(json.loads(sys.argv[1]))))
    except Exception as exc:
        # Never print tokens, credential material, or HTTP request bodies.
        print(json.dumps({'error': type(exc).__name__}))
        sys.exit(1)
