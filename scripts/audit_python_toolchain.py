#!/usr/bin/env python3
"""Verify locked wheel hashes against PyPI and inventory licenses/release age without installation."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import datetime
import json
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request

ROOT=Path(__file__).resolve().parents[1]


def inspect(item,allowed):
    row={k:item[k] for k in ['name','version','wheel','sha256']}
    row.update({'pypi_hash_match':'UNKNOWN','license_review':'MANUAL_REVIEW','release_age_days':None,'over_60_days':'UNKNOWN','ownership_monitoring':'NOT_ASSESSED'})
    url='https://pypi.org/pypi/'+urllib.parse.quote(item['name'],safe='')+'/'+urllib.parse.quote(item['version'],safe='')+'/json'
    try:
        with urllib.request.urlopen(url,timeout=30) as response:data=json.load(response)
    except (urllib.error.HTTPError,urllib.error.URLError,TimeoutError,ValueError):
        row['error']='PyPI metadata unavailable; no compliance conclusion.';return row
    matches=[x for x in data.get('urls',[]) if x.get('filename')==item['wheel']]
    row['pypi_hash_match']=len(matches)==1 and matches[0].get('digests',{}).get('sha256')==item['sha256']
    info=data.get('info',{})
    expression=info.get('license_expression')
    row['license_expression']=expression
    row['license_classifiers']=[x for x in info.get('classifiers',[]) if x.startswith('License ::')]
    if expression in allowed:row['license_review']='MATCHES_PROPOSED_POLICY_ONLY'
    if len(matches)==1 and matches[0].get('upload_time_iso_8601'):
        uploaded=datetime.datetime.fromisoformat(matches[0]['upload_time_iso_8601'].replace('Z','+00:00'))
        age=(datetime.datetime.now(datetime.timezone.utc)-uploaded).total_seconds()/86400
        row['release_age_days']=round(age,2);row['over_60_days']=age>60
        row['age_scope']='Selected wheel upload age; verify original package-version release time separately.'
    return row


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',default='reports/python-toolchain');args=p.parse_args()
    items=json.loads((ROOT/'config/python-scanner-lock.json').read_text())['packages']
    policy=json.loads((ROOT/'config/scanner-license-policy.json').read_text())
    with ThreadPoolExecutor(max_workers=4) as pool:
        rows=list(pool.map(lambda i:inspect(i,policy['allowed_exact_spdx_expressions']),items))
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    report={'scope':'Python scanner tools only; no claim of supplier SBOM/provenance, registry ownership or application dependency coverage',
            'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'policy_status':policy['status'],'packages':rows}
    (out/'results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'packages':len(rows),'pypi_hashes_matched':sum(x['pypi_hash_match'] is True for x in rows),'license_manual_review':sum(x['license_review']=='MANUAL_REVIEW' for x in rows)}))
    # A locked binary not matching official metadata is a failing integrity check.
    return 0 if all(x['pypi_hash_match'] is True for x in rows) else 2

if __name__=='__main__':raise SystemExit(main())
