#!/usr/bin/env python3
"""Read-only checks; partial configuration evidence is never full CIS compliance."""
import argparse
import csv
import datetime
import json
import os
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request


def request(repo, endpoint, token):
    headers = {'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28'}
    if token:
        headers['Authorization'] = 'Bearer ' + token
    url = 'https://api.github.com/repos/' + repo + endpoint
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as response:
            return {'http': response.status, 'data': json.load(response)}
    except urllib.error.HTTPError as error:
        return {'http': error.code, 'error': 'API access failed; do not interpret as noncompliance.'}
    except (urllib.error.URLError, TimeoutError, ValueError):
        return {'http': None, 'error': 'Network, timeout or response decoding error.'}


def evaluate(info, protection, rules):
    if info['http'] != 200:
        return [{'cis_id': i, 'configuration_result': 'ERROR', 'overall_status': 'ERROR',
                 'observed': None, 'note': 'Repository metadata unavailable.'}
                for i in ('1.1.3', '1.1.4', '1.1.9', '1.1.16', '1.1.17', '1.1.20')]
    if protection['http'] != 200:
        # A 404 may indicate no classic protection OR inaccessible data. Rulesets can
        # supply equivalent protection; this implementation deliberately avoids guessing.
        return [{'cis_id': i, 'configuration_result': 'UNKNOWN', 'overall_status': 'MANUAL_REVIEW',
                 'observed': {'classic_http': protection['http'], 'rules_http': rules['http'],
                              'rule_count': len(rules.get('data', [])) if rules['http'] == 200 else None},
                 'note': 'Review effective Rulesets, classic protection, permissions and bypass actors.'}
                for i in ('1.1.3', '1.1.4', '1.1.9', '1.1.16', '1.1.17', '1.1.20')]
    data = protection['data']
    review = data.get('required_pull_request_reviews') or {}
    checks = data.get('required_status_checks') or {}
    # Only literal false proves denial. Missing fields are unknown.
    force = (data.get('allow_force_pushes') or {}).get('enabled')
    deletion = (data.get('allow_deletions') or {}).get('enabled')
    cases = [
        ('1.1.3', review.get('required_approving_review_count'),
         review.get('required_approving_review_count', 0) >= 2,
         'At least two configured approvals; CIS Audit specifies 2. Verify reviewer identities and strong authentication.'),
        ('1.1.4', review.get('dismiss_stale_reviews'), review.get('dismiss_stale_reviews') is True,
         'Confirm stale approval dismissal with a real PR update.'),
        ('1.1.9', {'contexts': checks.get('contexts'), 'checks': checks.get('checks')},
         bool(checks.get('contexts') or checks.get('checks')),
         'Validate required checks are meaningful and cannot be bypassed.'),
        ('1.1.16', force, None if force is None else force is False, 'Review bypass actors and overlapping rules.'),
        ('1.1.17', deletion, None if deletion is None else deletion is False, 'Test only on a disposable protected branch.'),
        ('1.1.20', True, True, 'Classic protection returned for the actual default branch; verify effective rules.')]
    return [{'cis_id': cid, 'configuration_result': 'UNKNOWN' if ok is None else ('PASS' if ok else 'FAIL'),
             'overall_status': 'MANUAL_REVIEW', 'observed': observed, 'note': note}
            for cid, observed, ok, note in cases]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', default=os.environ.get('GITHUB_REPOSITORY'))
    parser.add_argument('--output', default='reports/github-api')
    args = parser.parse_args()
    if not args.repo or len(args.repo.split('/')) != 2 or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._/' for c in args.repo):
        parser.error('--repo must be owner/name')
    token = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    info = request(args.repo, '', token)
    default = info.get('data', {}).get('default_branch')
    escaped = urllib.parse.quote(default, safe='') if default else None
    unavailable = {'http': None, 'error': 'Default branch unavailable.'}
    protection = request(args.repo, '/branches/' + escaped + '/protection', token) if default else unavailable
    rules = request(args.repo, '/rules/branches/' + escaped, token) if default else unavailable
    results = evaluate(info, protection, rules)
    policy = request(args.repo, '/community/profile', token)
    security = None
    policy_paths = []
    for path in ('SECURITY.md', '.github/SECURITY.md', 'docs/SECURITY.md'):
        found = request(args.repo, '/contents/' + path, token)
        policy_paths.append({'path': path, 'http': found['http']})
        if found['http'] == 200 and isinstance(found.get('data'), dict) and found['data'].get('type') == 'file':
            security = path
            break
    results.append({'cis_id': '1.2.1', 'configuration_result': 'PASS' if security else 'UNKNOWN',
                    'overall_status': 'MANUAL_REVIEW', 'observed': {'policy_path': security, 'lookups': policy_paths},
                    'note': 'Applicable to public repositories. Read policy content and check inherited organization policy; absence is inconclusive.'})
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    report = {'benchmark': 'CIS GitHub Benchmark v1.2.0', 'repository': args.repo,
              'checked_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'default_branch': default, 'api_http': {'repository': info['http'], 'protection': protection['http'],
              'rules': rules['http'], 'community_profile': policy['http']},
              'mode': 'read-only', 'results': results}
    (out / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
    with (out / 'results.csv').open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=['cis_id', 'configuration_result', 'overall_status', 'observed', 'note'], lineterminator='\n')
        writer.writeheader()
        for row in results:
            writer.writerow({**row, 'observed': json.dumps(row['observed'])})
    print(json.dumps({'repository': args.repo, 'checks': len(results), 'api_http': report['api_http']}))
    # Observation tool: reports uncertainty explicitly; no green compliance claim.
    return 2 if info['http'] != 200 else 0


if __name__ == '__main__':
    raise SystemExit(main())
