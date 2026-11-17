#!/usr/bin/env python3
"""Evidence readiness audit for all 120 controls. GET only; never asserts full compliance."""
import argparse
import csv
import datetime
import json
import os
from pathlib import Path
import re
import subprocess
import audit_github

ROOT = Path(__file__).resolve().parents[1]


def list_summary(repo, endpoint, token):
    count = 0
    # Pagination is bounded; hitting a bound is explicitly incomplete, not a pass.
    for page in range(1, 101):
        sep = '&' if '?' in endpoint else '?'
        result = audit_github.request(repo, endpoint + sep + f'per_page=100&page={page}', token)
        if result['http'] != 200:
            return {'http': result['http'], 'complete': False, 'count': count}
        items = result.get('data')
        if not isinstance(items, list):
            return {'http': 200, 'complete': False, 'count': count, 'note': 'Unexpected response schema'}
        count += len(items)
        if len(items) < 100:
            return {'http': 200, 'complete': True, 'count': count}
    return {'http': 200, 'complete': False, 'count': count, 'note': 'Pagination limit reached'}


def classify(sources, needed):
    missing = [key for key in needed if sources.get(key, {}).get('available') is not True]
    return {'execution': 'BLOCKED_PREREQUISITE' if missing else 'EVIDENCE_COLLECTED',
            'compliance': 'MANUAL_REVIEW', 'missing': missing}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo', default=os.environ.get('GITHUB_REPOSITORY'))
    p.add_argument('--output', default='reports/all-controls')
    args = p.parse_args()
    if not args.repo or not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', args.repo):
        p.error('--repo must be owner/name')
    token = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    metadata = audit_github.request(args.repo, '', token)
    data = metadata.get('data', {})
    if metadata['http'] != 200:
        data = {}
    sources = {'repository': {'available': metadata['http'] == 200, 'http': metadata['http'],
               'private': data.get('private'), 'default_branch': data.get('default_branch'),
               'owner_type': data.get('owner', {}).get('type')}}
    for name, endpoint in [('collaborators','/collaborators'), ('forks','/forks'), ('branches','/branches'),
                           ('pull_requests','/pulls?state=all'), ('releases','/releases'),
                           ('webhooks','/hooks'), ('deployments','/deployments')]:
        summary = list_summary(args.repo, endpoint, token)
        # Counts only: no hooks URL, credential, deployment payload or collaborator PII is published.
        sources[name] = {**summary, 'available': summary['http'] == 200 and summary['complete']}
    for key, note in {
        'organization_policy': 'Organization settings, MFA, SSO, SSH CA, approved email and audit log require owner evidence; current repo may be personal.',
        'identity_provider': 'Need actual IdP/MFA and role assignment evidence; do not simulate identities as production.',
        'supplier': 'Need supplier-provided SBOM, signatures, provenance, license and ownership baseline.',
        'registry': 'Need actual package registry configuration, permissions, versions and audit log.',
        'production': 'Need actual deployment environment and authorized access evidence.',
        'build_platform_admin': 'Need build platform/runner administrative configuration and trusted lifecycle evidence.',
        'required_check_enforcement': 'Need effective protection/bypass policy and negative PR test; no setting changes allowed.'
    }.items():
        sources[key] = {'available': False, 'reason': note}
    tracked = subprocess.check_output(['git','-C',str(ROOT),'ls-files'],text=True).splitlines()
    workflows = [f for f in tracked if f.startswith('.github/workflows/') and f.endswith(('.yml','.yaml'))]
    sources['repository_files'] = {'available': True, 'tracked_files': len(tracked), 'workflow_count': len(workflows), 'note': 'Source inspection is partial evidence, not runtime enforcement.'}
    sources['sandbox'] = {'available': False, 'reason': 'Run supply_chain_lab.py and review scope-limited evidence.'}
    sandbox = ROOT / 'reports/supply-chain/results.json'
    if sandbox.exists():
        parsed = json.loads(sandbox.read_text())
        sources['sandbox'] = {'available': True, 'scope': parsed.get('scope'), 'checks': len(parsed.get('checks', []))}
    plans = json.loads((ROOT/'docs/audit/control-plans.json').read_text())
    rows=[]
    for plan in plans:
        status=classify(sources, plan['evidence_sources'])
        rows.append({'cis_id':plan['id'], 'title':plan['title'], 'cis_assessment':plan['assessment'],
                     'execution':status['execution'], 'compliance':status['compliance'],
                     'missing_sources':', '.join(status['missing']), 'audit':plan['audit'],
                     'remediation':plan['remediation'], 're_audit':plan['re_audit'],
                     'note':'All 120 runbooks exist; evidence collected does not mean the control is satisfied.'})
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    report={'repository':args.repo,'ref':os.environ.get('GITHUB_REF_NAME','local'),
            'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'mode':'GET-only evidence readiness, no administrative mutations',
            'sources':sources,'controls':rows}
    (out/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    with (out/'results.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]), lineterminator='\n');w.writeheader();w.writerows(rows)
    summary={'controls':len(rows),'evidence_collected':sum(r['execution']=='EVIDENCE_COLLECTED' for r in rows),
             'blocked_prerequisite':sum(r['execution']=='BLOCKED_PREREQUISITE' for r in rows),
             'compliance_pass':0,'mode':report['mode']}
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary))
    return 2 if metadata['http']!=200 else 0

if __name__=='__main__':
    raise SystemExit(main())
