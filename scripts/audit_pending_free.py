#!/usr/bin/env python3
"""GET-only evidence for twelve pending Free controls; no emails, credentials or admin writes."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import datetime
import hashlib
import json
import os
from pathlib import Path

import audit_organization
import inventory_organization

REPOSITORY = 'nt542-r11-nhom17-cis-lab/finalrepo'
IDS = ['1.1.19', '1.3.1', '1.3.3', '1.3.4', '1.3.6', '1.3.13',
       '2.1.5', '2.1.6', '2.1.11', '3.1.2', '5.2.3', '5.2.4']
ROOT = Path(__file__).resolve().parents[1]


def observed_count(items, scope):
    return len(items) if scope.get('http') == 200 and scope.get('pagination_complete') is True else None


def policy_snapshot(response):
    # Store only a digest of an actual readable policy, not URLs, identities or raw configuration.
    if response.get('http') != 200 or not isinstance(response.get('data'), (dict, list)):
        return {'http': response.get('http'), 'digest': None, 'state': 'UNKNOWN'}
    raw = json.dumps(response['data'], sort_keys=True, separators=(',', ':')).encode()
    return {'http': 200, 'digest': hashlib.sha256(raw).hexdigest(), 'state': 'OBSERVED'}


def compare_policy(previous, current):
    if not previous or not previous.get('digest') or not current.get('digest'):
        return 'UNKNOWN'
    return 'UNCHANGED' if previous['digest'] == current['digest'] else 'CHANGED_REVIEW_REQUIRED'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('reports/pending-free'))
    parser.add_argument('--previous', type=Path)
    args = parser.parse_args()
    token = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    org = REPOSITORY.split('/')[0]
    repo_path = '/repos/' + REPOSITORY
    endpoints = {
        'org': '/orgs/' + org,
        'actions_permissions': repo_path + '/actions/permissions',
        'workflow_permissions': repo_path + '/actions/permissions/workflow',
        'runners': repo_path + '/actions/runners',
        'protection': repo_path + '/branches/main/protection',
        'rulesets': repo_path + '/rulesets?includes_parents=true',
    }
    with ThreadPoolExecutor(max_workers=6) as pool:
        responses = dict(pool.map(lambda item: (item[0], audit_organization.get(item[1], token)), endpoints.items()))
    collections = {
        'owners': '/orgs/' + org + '/members?role=admin',
        'members': '/orgs/' + org + '/members',
        'mfa_disabled': '/orgs/' + org + '/members?filter=2fa_disabled',
        'collaborators': repo_path + '/collaborators',
        'invitations': '/orgs/' + org + '/invitations',
    }
    with ThreadPoolExecutor(max_workers=5) as pool:
        lists = dict(pool.map(lambda item: (item[0], inventory_organization.list_pages(item[1], token)), collections.items()))
    counts = {key: {'count': observed_count(items, scope), 'scope': 'Caller-visible only; not proof of full organization membership/ownership', **scope} for key, (items, scope) in lists.items()}
    anonymous = audit_organization.get(repo_path + '/actions/runners', None)
    roles = inventory_organization.summarize_roles(*lists['collaborators'])
    policies = {key: policy_snapshot(responses[key]) for key in ('protection', 'rulesets')}
    previous = {}
    if args.previous:
        previous = json.loads(args.previous.read_text())
        if previous.get('repository') != REPOSITORY:
            parser.error('Previous evidence belongs to another repository')
    drift = {key: compare_policy(previous.get('policies', {}).get(key), value) for key, value in policies.items()}
    org_data = responses['org'].get('data', {})
    mfa = org_data.get('two_factor_requirement_enabled')
    org_mfa = mfa if type(mfa) is bool else 'UNKNOWN'
    runner_data = responses['runners'].get('data', {})
    runner_count = runner_data.get('total_count')
    runner_count = runner_count if responses['runners']['http'] == 200 and type(runner_count) is int else None
    workflow = responses['workflow_permissions'].get('data', {})
    sources = {'counts': counts, 'repo_access': roles, 'organization_mfa_required': org_mfa,
               'anonymous_runner_metadata_http': anonymous['http'], 'runner_count': runner_count,
               'actions_permissions_http': responses['actions_permissions']['http'],
               'workflow_permissions_http': responses['workflow_permissions']['http'],
               'default_workflow_permissions': workflow.get('default_workflow_permissions', 'UNKNOWN'),
               'note': 'Anonymous metadata rejection is not proof that every build-management path rejects access'}
    components = {
        '1.1.19': ('Policy snapshots and digest comparison', 'Effective rule event/actor/time log and recurring owner review missing'),
        '1.3.1': ('Paginated visible member inventory', 'Last-login/full activity, periodic review and any authorized removal not established'),
        '1.3.3': ('Paginated organization owner count', 'Owner justification, minimum required and recovery approval still needed'),
        '1.3.4': ('Org MFA field and filtered member count attempted', 'Enforcement and contributor coverage require privileged evidence; no member access changed'),
        '1.3.6': ('Invitation inventory attempted without exporting emails', 'Approved-email policy and actual invitation comparison unavailable; no invitations sent'),
        '1.3.13': ('Code change monitor and CI findings artifact', 'No comprehensive behavioral detection or human incident receipt verified'),
        '2.1.5': ('Platform-context execution guard for existing write/admin contributors', 'Not complete host/platform ACL enforcement; writers can modify workflow policy'),
        '2.1.6': ('Platform actor/id guard, rerun actor check and anonymous metadata GET', 'No independent authentication service or all-path negative authorization test'),
        '2.1.11': ('Repo admin counts and Actions management GETs', 'Hosted platform administrators, justified minimum and owner approval not established'),
        '3.1.2': ('Third-party exact-version/digest intake ledger', 'Supplier-issued SBOM missing for components; own export is not supplier SBOM'),
        '5.2.3': ('Read-only deployment-host preflight prepared', 'No authorized production execution or effective access evidence supplied'),
        '5.2.4': ('Read-only SSH/account configuration preflight prepared', 'No production credential inventory or authorized old/default credential rejection test'),
    }
    report = {'checked_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'repository': REPOSITORY, 'mode': 'GET-only; no Audit Log API, invitations or permission writes',
              'sources': sources, 'policies': policies, 'policy_drift': drift,
              'controls': [{'cis_id': cid, 'component': components[cid][0], 'remaining': components[cid][1],
                            'overall_cis': 'MANUAL_REVIEW'} for cid in IDS], 'compliance_pass': 0}
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'results.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'controls': len(IDS), 'owners': counts['owners']['count'],
                      'members': counts['members']['count'], 'policy_drift': drift, 'compliance_pass': 0}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
