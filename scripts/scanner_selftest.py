#!/usr/bin/env python3
"""Positive/negative secret-scanner tests using synthetic data only; fixture files are temporary."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--gitleaks',required=True)
    parser.add_argument('--output',default='reports/scanner-selftest')
    args=parser.parse_args()
    binary=str(Path(args.gitleaks).resolve())
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    checks=[]
    with tempfile.TemporaryDirectory(prefix='cis-secret-fixtures-') as temp:
        root=Path(temp);sample=root/'fixture'
        sample.mkdir()
        (sample/'settings.txt').write_text('message = harmless lab fixture\n')
        def scan(label):
            report=root/(label+'.json')
            result=subprocess.run([binary,'detect','--no-git','--source',str(sample),'--redact','--report-format','json','--report-path',str(report)],capture_output=True,text=True)
            return result.returncode,json.loads(report.read_text()) if report.exists() else []
        code,findings=scan('benign')
        if code!=0 or findings:raise RuntimeError('Benign fixture rejected or scanner failed')
        checks.append({'test':'benign configuration accepted','status':'PASS'})
        # Deterministically generated fake token. Never an actual credential and never committed as a fixture file.
        fake='gh'+'p_'+'1234567890abcdefghijklmnopqrstuvwxyzABCD'
        (sample/'settings.txt').write_text('GITHUB_PAT_TOKEN = "'+fake+'"\n')
        code,findings=scan('synthetic-secret')
        if code!=1 or not findings:raise RuntimeError('Synthetic secret was not rejected; check scanner health')
        checks.append({'test':'synthetic credential rejected','status':'PASS','finding_count':len(findings),'rules':sorted({x['RuleID'] for x in findings})})
    (out/'results.json').write_text(json.dumps({'scope':'scanner behavior test only; does not prove branch protection or real secret remediation','checks':checks},indent=2)+'\n')
    print(json.dumps({'tests':len(checks),'result':'PASS','scope':'synthetic positive/negative fixtures'}))

if __name__=='__main__':main()
