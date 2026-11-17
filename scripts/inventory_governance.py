#!/usr/bin/env python3
"""Review-only branch/fork inventories. Never delete, archive, invite or change permissions."""
import argparse
import datetime
import json
import os
from pathlib import Path
import audit_github


def pages(repo, endpoint, token, fetch=audit_github.request):
    items = []
    for page in range(1, 101):
        result = fetch(repo, endpoint + f'?per_page=100&page={page}', token)
        data = result.get('data')
        if result['http'] != 200 or not isinstance(data, list):
            return items, False, result['http']
        items.extend(data)
        if len(data) < 100:
            return items, True, 200
    return items, False, 200


def commit_age(response, now):
    if response.get('http') != 200:
        return None
    date = (response.get('data') or {}).get('commit', {}).get('committer', {}).get('date')
    try:
        value = datetime.datetime.fromisoformat(date.replace('Z', '+00:00'))
        age = (now - value).total_seconds() / 86400
        return round(age, 2) if age >= 0 else None
    except (AttributeError, TypeError, ValueError):
        return None


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo', default=os.environ.get('GITHUB_REPOSITORY', 'nt542-r11-nhom17-cis-lab/finalrepo'))
    p.add_argument('--output', default='reports/governance')
    args = p.parse_args()
    token = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    now = datetime.datetime.now(datetime.timezone.utc)
    branches, complete_branches, branch_http = pages(args.repo, '/branches', token)
    forks, complete_forks, fork_http = pages(args.repo, '/forks', token)
    rows = []
    for branch in branches:
        sha = branch.get('commit', {}).get('sha')
        observed = audit_github.request(args.repo, '/commits/' + sha, token) if sha else {'http': None}
        rows.append({'branch': branch.get('name'), 'commit': sha, 'protected_api_flag': branch.get('protected'),
                     'commit_http': observed['http'], 'last_commit_age_days': commit_age(observed, now),
                     'decision': 'OWNER_REVIEW_REQUIRED; age alone does not mean inactive or safe to delete'})
    report = {'checked_at': now.isoformat(), 'repository': args.repo,
              'scope': 'API-visible branches and forks only; branch age is not user inactivity; no deletion or archive',
              'branches': {'http': branch_http, 'pagination_complete': complete_branches, 'items': rows},
              'forks': {'http': fork_http, 'pagination_complete': complete_forks,
                        'items': [{'repository_id': f.get('id'), 'full_name': f.get('full_name'), 'private': f.get('private')}
                                  for f in forks]},
              'overall_cis': 'PARTIAL', 'mutations': 0}
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    (out / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'branches_observed': len(rows), 'forks_observed': len(forks),
                      'pagination_complete': complete_branches and complete_forks, 'mutations': 0}))
    return 0 if complete_branches and complete_forks and all(r['last_commit_age_days'] is not None for r in rows) else 2


if __name__ == '__main__':
    raise SystemExit(main())
