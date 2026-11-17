#!/usr/bin/env python3
"""Fail closed if a successful scanner did not inventory the pinned registry binary."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def evaluate(report, expected_hash):
    matching = [r for r in report.get('Results', [])
                if r.get('Type') == 'gobinary' and str(r.get('Target', '')).endswith('registry-' + expected_hash)]
    packages = [p for r in matching for p in r.get('Packages', [])]
    findings = [v for r in matching for v in r.get('Vulnerabilities', []) if v.get('Severity') in {'HIGH', 'CRITICAL'}]
    return {'matched_binary_records': len(matching), 'inventoried_packages': len(packages),
            'high_critical': len(findings), 'gate_passed': len(matching) == 1 and bool(packages) and not findings,
            'scope': 'Pinned Distribution Go binary only; not complete host or production coverage'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', default='reports/registry-binary-vulnerabilities.json')
    parser.add_argument('--output', default='reports/registry-scan-coverage.json')
    args = parser.parse_args()
    lock = json.loads((ROOT / 'config/registry-integration.lock.json').read_text())
    result = evaluate(json.loads(Path(args.input).read_text()), lock['binary_sha256'])
    Path(args.output).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))
    return 0 if result['gate_passed'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
