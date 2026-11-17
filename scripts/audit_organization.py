#!/usr/bin/env python3
"""GET-only organization settings audit. Missing or permission-filtered fields remain UNKNOWN."""
import argparse
import csv
import datetime
import json
import os
from pathlib import Path
import re
import urllib.error
import urllib.request

FIELDS={
 '1.2.2':('members_can_create_repositories',False,'Review exceptions and who may create repositories.'),
 '1.2.3':('members_can_delete_repositories',False,'Review actual admin/deletion roles and audit trail.'),
 '1.2.4':('members_can_delete_issues',False,'Review issue deletion permissions and exceptions.'),
 '1.2.6':('members_can_change_repo_visibility',False,'Restriction is only partial evidence; visibility-change monitoring still required.'),
 '1.3.2':('members_can_create_teams',False,'Review organization-owner exceptions.'),
 '1.3.5':('two_factor_requirement_enabled',True,'Verify enforcement, membership scope and recovery process.'),
 '1.3.8':('default_repository_permission','none','Verify effective per-team grants and exceptions.'),
 '1.3.9':('is_verified',True,'Confirm the verified domain/badge in organization settings.')}


def get(path,token):
    headers={'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'}
    if token:headers['Authorization']='Bearer '+token
    try:
        req=urllib.request.Request('https://api.github.com'+path,headers=headers)
        with urllib.request.urlopen(req,timeout=30) as response:
            return {'http':response.status,'data':json.load(response)}
    except urllib.error.HTTPError as error:return {'http':error.code}
    except (urllib.error.URLError,TimeoutError,ValueError):return {'http':None}


def evaluate(data,http=200):
    rows=[]
    for cid,(field,expected,note) in FIELDS.items():
        actual=data.get(field)
        typed=isinstance(actual,str) if isinstance(expected,str) else type(actual) is bool
        result='UNKNOWN' if http!=200 or not typed else ('PASS' if actual==expected else 'FAIL')
        rows.append({'cis_id':cid,'field':field,'observed':actual,'expected':expected,
                     'configuration_result':result,'overall_status':'MANUAL_REVIEW',
                     'note':note+(' Field unavailable or permission-filtered; never infer false.' if result=='UNKNOWN' else ' Component setting only; not a full-control compliance claim.')})
    return rows


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',default=os.environ.get('GITHUB_REPOSITORY'))
    parser.add_argument('--output',default='reports/organization')
    args=parser.parse_args()
    if not args.repo or not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',args.repo):parser.error('--repo must be owner/name')
    token=os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    org=args.repo.split('/')[0]
    repo=get('/repos/'+args.repo,token)
    owner=repo.get('data',{}).get('owner',{})
    confirmed=repo['http']==200 and owner.get('type')=='Organization' and owner.get('login','').lower()==org.lower()
    metadata=get('/orgs/'+org,token) if confirmed else {'http':None}
    members=get('/orgs/'+org+'/members?per_page=100',token) if confirmed else {'http':None}
    membership=get('/user/memberships/orgs/'+org,token) if confirmed else {'http':None}
    hooks=get('/orgs/'+org+'/hooks?per_page=100',token) if confirmed else {'http':None}
    # Hook URLs, config, secrets, usernames, emails and raw org metadata are not exported.
    sources={'repository_http':repo['http'],'organization_http':metadata['http'],
             'members_http':members['http'],'self_membership_http':membership['http'],
             'webhooks_http':hooks['http'],
             'visible_member_page_count':len(members['data']) if isinstance(members.get('data'),list) else None,
             'member_inventory_scope':'API-visible first page only; not total members/admin count; membership and pagination require further evidence.'}
    rows=evaluate(metadata.get('data',{}),metadata['http'])
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    report={'repository':args.repo,'organization':org,'owner_is_organization':confirmed,
            'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mode':'GET-only',
            'sources':sources,'results':rows,
            'administrative_changes':'NONE','limitation':'Repository admin permission does not prove organization-settings visibility or permission.'}
    (out/'results.json').write_text(json.dumps(report,indent=2)+'\n')
    with (out/'results.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
    print(json.dumps({'owner_is_organization':confirmed,'component_checks':len(rows),
        'unknown':sum(x['configuration_result']=='UNKNOWN' for x in rows),'sources':sources}))
    return 0 if confirmed and metadata['http']==200 else 2

if __name__=='__main__':raise SystemExit(main())
