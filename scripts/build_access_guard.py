#!/usr/bin/env python3
"""Restrict audited build steps using GitHub-provided execution identity; never grants access."""
import argparse
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def evaluate(context, policy):
    checks = {
        'github_actions_context': context.get('GITHUB_ACTIONS') == 'true',
        'repository_identity': context.get('GITHUB_REPOSITORY') == policy['repository']
        and context.get('GITHUB_REPOSITORY_ID') == policy['repository_id'],
        'audit_branch_only': context.get('GITHUB_REF') in policy['refs'],
        'event_allowed': context.get('GITHUB_EVENT_NAME') in policy['events'],
        'authenticated_actor': any(context.get('GITHUB_ACTOR', '').casefold() == p['login'].casefold()
                                   and context.get('GITHUB_ACTOR_ID') == p['id'] for p in policy['principals']),
        'rerun_actor_allowed': context.get('GITHUB_TRIGGERING_ACTOR', '').casefold()
        in {p['login'].casefold() for p in policy['principals']},
    }
    return {'scope': 'In-workflow checks of platform context; not independent authentication or MFA',
            'checks': checks, 'execution_allowed': all(checks.values()),
            'overall_cis': 'PARTIAL', 'credentials_exported': False,
            'limits': ['Workflow source can be changed by repository writers; required reviews still needed',
                       'Does not revoke GitHub rights or restrict every platform administration path',
                       'Local environment variables can be forged; only platform-run evidence has context value']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('reports/build-access/results.json'))
    args = parser.parse_args()
    policy = json.loads((ROOT / 'config/build-access.json').read_text())
    report = evaluate(os.environ, policy)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'execution_allowed': report['execution_allowed'], 'checks': report['checks']}))
    return 0 if report['execution_allowed'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
