#!/usr/bin/env python3
"""Collect read-only evidence for 48 Free-oriented controls; never infer full PASS."""
import argparse
import csv
import datetime
import json
import os
from pathlib import Path
import re
import subprocess
import urllib.parse
import audit_all
import audit_github

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = 'nt542-r11-nhom17-cis-lab/finalrepo'


def protection_component(response, field):
    """Only present, typed values are evidence. 403/null must not be false or PASS."""
    value = response.get('data') if response.get('http') == 200 else None
    for key in field.split('.'):
        value = value.get(key) if isinstance(value, dict) else None
    return {'http': response.get('http'), 'value': value,
            'configuration_result': 'UNKNOWN' if value is None else 'OBSERVED',
            'note': 'Classic protection only; effective rulesets, bypass and behavior still need review.'}


def local_inventory():
    def git(*args):
        return subprocess.check_output(['git', '-C', str(ROOT), *args], text=True).strip()
    files = git('ls-files').splitlines()
    tracked_workflows = [x for x in files if x.startswith('.github/workflows/') and x.endswith(('.yml', '.yaml'))]
    return {'available': True, 'commit': git('rev-parse', 'HEAD'), 'ref': git('branch', '--show-current'),
            'tracked_count': len(files), 'untracked_count': len(git('ls-files', '--others', '--exclude-standard').splitlines()),
            'tracked_workflows': tracked_workflows,
            'note': 'Current checkout only. Does not prove all organization code/changes are version-controlled.'}


def build_rows(plans, sources):
    rows = []
    for plan in plans:
        available = [s for s in plan['sources'] if sources.get(s, {}).get('available') is True]
        missing = [s for s in plan['sources'] if s not in available]
        rows.append({'cis_id': plan['id'], 'execution': 'EVIDENCE_COLLECTED' if not missing else 'INCOMPLETE',
                     'overall_cis': 'MANUAL_REVIEW', 'available_sources': ', '.join(available),
                     'missing_sources': ', '.join(missing), 'remaining': plan['remaining'],
                     'manual_guide': 'PROCEDURES.vi.md#cis-' + plan['id'].replace('.', '-')})
    return rows


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo', default=os.environ.get('GITHUB_REPOSITORY', CANONICAL))
    p.add_argument('--output', default='reports/free-controls')
    args = p.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', args.repo):
        p.error('--repo must be owner/name')
    token = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    meta = audit_github.request(args.repo, '', token)
    data = meta.get('data') or {}
    default = data.get('default_branch')
    sources = {'repository': {'available': meta['http'] == 200, 'http': meta['http'],
                              'id': data.get('id'), 'private': data.get('private'), 'default_branch': default},
               'source': local_inventory()}
    for key, endpoint in [('branches', '/branches'), ('forks', '/forks'), ('collaborators', '/collaborators'),
                          ('pulls', '/pulls?state=all'), ('hooks', '/hooks'), ('releases', '/releases'),
                          ('deployments', '/deployments'), ('runners', '/actions/runners')]:
        # Runners has an object schema, handled separately below.
        if key == 'runners':
            reply = audit_github.request(args.repo, endpoint, token)
            count = (reply.get('data') or {}).get('total_count')
            sources[key] = {'available': reply['http'] == 200 and type(count) is int,
                            'http': reply['http'], 'count': count,
                            'note': 'No runner names, labels, addresses or credentials exported.'}
        else:
            summary = audit_all.list_summary(args.repo, endpoint, token)
            sources[key] = {**summary, 'available': summary['http'] == 200 and summary['complete'],
                            'note': 'Counts only; count does not prove a security policy.'}
    for key, endpoint in [('actions_policy', '/actions/permissions'),
                          ('workflow_token_policy', '/actions/permissions/workflow'),
                          ('secrets', '/actions/secrets')]:
        reply = audit_github.request(args.repo, endpoint, token)
        safe = {}
        if reply['http'] == 200:
            observed = reply.get('data') or {}
            fields = ('enabled', 'allowed_actions') if key == 'actions_policy' else (
                ('default_workflow_permissions', 'can_approve_pull_request_reviews') if key == 'workflow_token_policy' else ('total_count',))
            safe = {field: observed.get(field) for field in fields}
        sources[key] = {'available': reply['http'] == 200, 'http': reply['http'], 'observed': safe,
                        'note': 'No secret names/values or application identities exported.'}
    protection = (audit_github.request(args.repo, '/branches/' + urllib.parse.quote(default, safe='') + '/protection', token)
                  if default else {'http': None})
    components = {}
    for cid, field in {'1.1.5': 'required_pull_request_reviews.dismissal_restrictions',
                       '1.1.7': 'required_pull_request_reviews.require_code_owner_reviews',
                       '1.1.10': 'required_status_checks.strict', '1.1.11': 'required_conversation_resolution.enabled',
                       '1.1.12': 'required_signatures.enabled', '1.1.13': 'required_linear_history.enabled',
                       '1.1.14': 'enforce_admins.enabled', '1.1.15': 'restrictions'}.items():
        components[cid] = protection_component(protection, field)
    sources['protection'] = {'available': protection['http'] == 200, 'http': protection['http'], 'components': components}
    for key, relative in [('bundle', 'project-bundle/verification.json'), ('owners', 'action-owners/results.json')]:
        path = ROOT / 'reports' / relative
        sources[key] = {'available': path.is_file(), 'path': relative,
                        'note': 'Read the referenced report; file existence is not a compliance finding.'}
    for key, reason in {
        'organization_admin': 'Need organization owner Settings evidence; integration lacks organization policy scopes.',
        'build_admin': 'Need actual Actions access/runner lifecycle and configuration evidence.',
        'supplier': 'Need independent supplier SBOM, provenance and verification trust roots.',
        'production': 'Need a real authorized deployment target and identities; sandbox is not production.',
        'behavior_test': 'Need approved disposable protected branch and multiple actual users; never test on main.',
        'registry': 'Need real separately secured registry/storage permissions and audit evidence.'
    }.items():
        sources[key] = {'available': False, 'reason': reason}
    plans = json.loads((ROOT / 'docs/audit/free-controls.json').read_text())
    rows = build_rows(plans, sources)
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    report = {'checked_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'repository': args.repo, 'mode': 'GET-only; no settings/permissions/main mutations',
              'sources': sources, 'controls': rows, 'full_control_pass': 0}
    (out / 'results.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    with (out / 'results.csv').open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps({'controls': len(rows), 'evidence_collected': sum(r['execution'] == 'EVIDENCE_COLLECTED' for r in rows),
                      'incomplete': sum(r['execution'] == 'INCOMPLETE' for r in rows), 'full_control_pass': 0}))
    return 0 if meta['http'] == 200 else 2


if __name__ == '__main__':
    raise SystemExit(main())
