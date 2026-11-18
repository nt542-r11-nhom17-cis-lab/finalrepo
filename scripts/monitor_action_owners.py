#!/usr/bin/env python3
"""Fail closed on pinned action repository/owner identity drift; PyPI ownership excluded."""
import argparse
import datetime
import json
import os
from pathlib import Path
import re
import audit_github
from audit_dependencies import parse_action_uses

ROOT = Path(__file__).resolve().parents[1]


def actions():
    return sorted({row['repository'] for path in (ROOT / '.github/workflows').glob('*.yml')
                   for row in parse_action_uses(path.read_text()) if re.fullmatch('[a-f0-9]{40}', row['ref'])})


def compare(expected, observed):
    rows = []
    for action in sorted(set(expected) | set(observed)):
        before, after = expected.get(action), observed.get(action)
        known = isinstance(after, dict) and type(after.get('repository_id')) is int and type(after.get('owner_id')) is int
        state = 'UNKNOWN' if not known else ('UNCHANGED' if before == after else 'REVIEW_REQUIRED')
        rows.append({'action': action, 'state': state, 'expected': before, 'observed': after})
    return rows


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--baseline', default=str(ROOT / 'config/action-owners.json'))
    p.add_argument('--output', default='reports/action-owners')
    p.add_argument('--initialize', action='store_true', help='One-time candidate baseline; never overwrites existing baseline')
    args = p.parse_args()
    token = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    observed = {}
    for action in actions():
        response = audit_github.request(action, '', token)
        data = response.get('data') or {}
        observed[action] = ({'repository_id': data.get('id'), 'owner_id': data.get('owner', {}).get('id')}
                            if response['http'] == 200 else None)
    baseline = Path(args.baseline)
    if args.initialize:
        if not observed or any(v is None or type(v.get('repository_id')) is not int or type(v.get('owner_id')) is not int for v in observed.values()):
            p.error('Incomplete API evidence; refusing baseline initialization')
        with baseline.open('x') as handle:
            json.dump({'status': 'Observed candidate baseline; owner must review suppliers', 'actions': observed}, handle, indent=2)
            handle.write('\n')
    expected = json.loads(baseline.read_text())['actions']
    rows = compare(expected, observed)
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    report = {'checked_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'scope': 'Pinned GitHub Actions repositories and owner numeric IDs only; not PyPI maintainers, individual commits or supplier trust',
              'results': rows, 'overall_cis': 'PARTIAL'}
    (out / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
    ok = bool(rows) and all(row['state'] == 'UNCHANGED' for row in rows)
    print(json.dumps({'actions': len(rows), 'unchanged': sum(r['state'] == 'UNCHANGED' for r in rows), 'gate_passed': ok}))
    return 0 if ok else 2


if __name__ == '__main__':
    raise SystemExit(main())
