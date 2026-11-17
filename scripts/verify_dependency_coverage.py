#!/usr/bin/env python3
"""Fail unless the vulnerability report covers every locked package at the exact version."""
import argparse
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]


def canonical(name):return re.sub(r'[-_.]+','-',name).lower()


def verify(packages,report):
    if not packages:raise ValueError('Expected package inventory is empty')
    expected={canonical(p['name']):p['version'] for p in packages}
    actual=report.get('dependencies',[])
    if len(expected)!=len(packages):raise ValueError('Duplicate expected package')
    if any(p.get('skip_reason') for p in actual):raise ValueError('Vulnerability report skipped a package')
    observed={canonical(p['name']):p.get('version') for p in actual}
    if len(observed)!=len(actual):raise ValueError('Duplicate reported package')
    if expected!=observed:raise ValueError('Vulnerability report does not cover the exact locked package set/versions')
    if any(p.get('vulns') for p in actual):raise ValueError('Known package vulnerability requires remediation')
    return {'expected_packages':len(expected),'audited_packages':len(observed),'known_vulnerabilities':0,'coverage':'EXACT'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--report',default='reports/python-package-audit.json')
    p.add_argument('--output',default='reports/dependency-coverage.json')
    args=p.parse_args()
    expected=json.loads((ROOT/'config/python-scanner-lock.json').read_text())['packages']
    result=verify(expected,json.loads(Path(args.report).read_text()))
    out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))

if __name__=='__main__':main()
