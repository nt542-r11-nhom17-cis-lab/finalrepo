#!/usr/bin/env python3
"""Read-only inventory of action SHAs, release references and release age. No install/update."""
import argparse
import datetime
import json
import os
from pathlib import Path
import re
import audit_github

ROOT=Path(__file__).resolve().parents[1]


def parse_action_uses(text):
    """Inventory static remote uses, including subdirectory actions such as CodeQL."""
    pattern = re.compile(
        r'''^[ \t]*(?:-[ \t]+)?uses:[ \t]*(?P<quote>['"]?)(?P<repo>[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)'''
        r'''(?:/(?P<entrypoint>[A-Za-z0-9_./-]+))?@(?P<ref>[A-Za-z0-9_.-]+)(?P=quote)[ \t]*(?:\#[ \t]*(?P<comment>.*))?$''',
        re.M)
    rows = []
    for match in pattern.finditer(text):
        hint = re.match(r'(v[0-9][A-Za-z0-9_.-]*)(?:[ \t]|$)', match['comment'] or '')
        rows.append({'repository': match['repo'], 'entrypoint': match['entrypoint'] or '',
                     'ref': match['ref'], 'tag_hint': hint[1] if hint else None})
    return rows


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',default='reports/dependencies')
    args=parser.parse_args()
    token=os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    refs={}
    for path in sorted((ROOT/'.github/workflows').glob('*.yml')):
        for parsed in parse_action_uses(path.read_text()):
            action,ref,tag=parsed['repository'],parsed['ref'],parsed['tag_hint']
            key=action+'@'+ref
            item=refs.setdefault(key,{'action':action,'ref':ref,'tag_hint':tag,'files':[], 'entrypoints':[]})
            if path.name not in item['files']:
                item['files'].append(path.name)
            if parsed['entrypoint'] not in item['entrypoints']:
                item['entrypoints'].append(parsed['entrypoint'])
    now=datetime.datetime.now(datetime.timezone.utc)
    rows=[]
    for item in refs.values():
        action,ref,tag=item['action'],item['ref'],item['tag_hint']
        pinned=bool(re.fullmatch('[a-f0-9]{40}',ref))
        commit=audit_github.request(action,'/commits/'+ref,token)
        resolved=commit.get('data',{}).get('sha')
        row={**item,'full_sha_pinned':pinned,'commit_http':commit['http'],
             'commit_exists':commit['http']==200 and resolved==ref,
             'trusted_supplier_verification':'MANUAL_REVIEW',
             'release_age_days':None,'over_60_days':'UNKNOWN','tag_matches_sha':'UNKNOWN'}
        if tag:
            tagged=audit_github.request(action,'/commits/'+tag,token)
            if tagged['http']==200:
                row['tag_matches_sha']=tagged.get('data',{}).get('sha')==ref
            release=audit_github.request(action,'/releases/tags/'+tag,token)
            published=release.get('data',{}).get('published_at') if release['http']==200 else None
            row['release_http']=release['http']
            if published:
                age=(now-datetime.datetime.fromisoformat(published.replace('Z','+00:00'))).total_seconds()/86400
                row['release_published_at']=published
                row['release_age_days']=round(age,2)
                row['over_60_days']=age>60
        rows.append(row)
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    report={'scope':'GitHub Actions only; downloaded tools, runner OS and transitive dependencies require additional evidence',
            'checked_at':now.isoformat(),'dependencies':rows,
            'cis_3_1_8':'No blanket compliance claim: unknown release dates or versions <=60 days must be reviewed.',
            'trust':'API existence and tag match are partial evidence, not independent supplier attestation verification.'}
    (out/'results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'action_refs':len(rows),'full_sha_pinned':sum(r['full_sha_pinned'] for r in rows),
                      'commit_exists':sum(r['commit_exists'] for r in rows),'compliance':'MANUAL_REVIEW'}))

if __name__=='__main__':main()
