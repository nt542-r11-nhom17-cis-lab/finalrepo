#!/usr/bin/env python3
"""Read-only organization repository/access inventory; hidden policies stay unknown."""
import argparse
import collections
import datetime
import json
import os
from pathlib import Path
import re
import audit_organization
import audit_github
import integration_support


def list_pages(path, token, fetch=audit_organization.get):
    items = []
    for page in range(1, 101):
        sep = '&' if '?' in path else '?'
        reply = fetch(path + sep + f'per_page=100&page={page}', token)
        if reply['http'] != 200 or not isinstance(reply.get('data'), list):
            return items, {'http': reply['http'], 'pagination_complete': False}
        items.extend(reply['data'])
        if len(reply['data']) < 100:
            return items, {'http': 200, 'pagination_complete': True}
    return items, {'http': 200, 'pagination_complete': False}


def summarize_roles(items, visibility):
    roles = collections.Counter(x.get('role_name', 'UNKNOWN') for x in items)
    return {'visible_accounts': len(items), 'visible_roles': dict(roles),
            'pagination': visibility, 'full_effective_access_verified': False,
            'mfa': 'UNKNOWN', 'inactive_user_decision': 'OWNER_REVIEW_REQUIRED',
            'note': 'API visibility depends on caller; role counts do not prove full member/admin inventory or MFA.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', default=os.environ.get('GITHUB_REPOSITORY', 'nt542-r11-nhom17-cis-lab/finalrepo'))
    parser.add_argument('--output', default='reports/organization-inventory')
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', args.repo):
        parser.error('--repo must be owner/name')
    org = args.repo.split('/')[0]
    token = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    now = datetime.datetime.now(datetime.timezone.utc)
    repos, repo_scope = list_pages('/orgs/' + org + '/repos?type=all', token)
    inventory = []
    for repo in repos:
        pushed = repo.get('pushed_at')
        age = None
        if pushed:
            try:
                delta = (now - datetime.datetime.fromisoformat(pushed.replace('Z', '+00:00'))).total_seconds() / 86400
                age = round(delta, 2) if delta >= 0 else None
            except ValueError:
                pass
        inventory.append({'id': repo.get('id'), 'name': repo.get('name'), 'archived': repo.get('archived'),
                          'private': repo.get('private'), 'last_push_age_days': age,
                          'decision': 'OWNER_REVIEW_REQUIRED; age alone does not justify archiving'})
    def repo_fetch(path, supplied):
        return audit_github.request(args.repo, path, supplied)
    access, access_scope = list_pages('/collaborators', token, fetch=repo_fetch)
    # Administrative GETs collect status/field presence, never raw members,
    # invitations, webhook configuration, app identities or secret values.
    endpoints = {'organization_owners': '/members?role=admin', 'applications': '/installations',
                 'invitations': '/invitations', 'organization_webhooks': '/hooks'}
    administrative = {}
    for name, suffix in endpoints.items():
        reply = audit_organization.get('/orgs/' + org + suffix, token)
        administrative[name] = {'http': reply['http'], 'overall_cis': 'MANUAL_REVIEW',
                                'note': 'Use owner Settings for effective policy review; API-visible data alone is insufficient.'}
    report = {'checked_at': now.isoformat(), 'repository': args.repo, 'mode': 'GET-only; mutations=0',
              'repositories': {'scope': repo_scope, 'items': inventory},
              'repo_access': summarize_roles(access, access_scope), 'administrative': administrative,
              'overall_cis': 'MANUAL_REVIEW',
              'limits': ['No inactive users removed, repositories archived, members invited or permissions changed',
                         'No member email, MFA recovery data, hook URLs or credential values exported']}
    integration_support.write_report(args.output, report)
    print(json.dumps({'visible_repositories': len(inventory), 'visible_accounts': len(access),
                      'repositories_http': repo_scope['http'], 'mutations': 0}))
    return 0 if repo_scope['http'] == 200 and repo_scope['pagination_complete'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
