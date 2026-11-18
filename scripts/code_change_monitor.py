#!/usr/bin/env python3
"""Record sensitive code/config changes and reject selected dangerous workflow constructs."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PREFIXES = ('.github/', 'scripts/', 'config/', 'deploy/')
PATTERNS = {
    'privileged_pull_request_target': r'^\s*(?:-\s*)?pull_request_target\s*:',
    'write_all_token': r'^\s*permissions\s*:\s*write-all\s*(?:#.*)?$',
    'persist_checkout_credentials': r'^\s*persist-credentials\s*:\s*true\s*(?:#.*)?$',
}


def inspect_workflow(text):
    return [name for name, pattern in PATTERNS.items() if re.search(pattern, text, re.MULTILINE)]


def changed_paths(base, head, git):
    raw = git('diff', '--name-only', '-z', base, head, '--')
    # No path is executed or passed as an option. Preserve unusual filenames as JSON strings.
    return [p for p in raw.split('\0') if p]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', default='HEAD^')
    parser.add_argument('--output', type=Path, default=Path('reports/code-monitor/results.json'))
    args = parser.parse_args()
    def git(*parts):
        return subprocess.check_output(['git', '-C', str(ROOT), *parts], text=True)
    if not re.fullmatch(r'(?:[0-9a-f]{40}|HEAD(?:[~^][0-9]*)?)', args.base):
        parser.error('Base must be a full commit SHA or HEAD-relative revision')
    # Resolve revisions before using them as diff arguments; never accept arbitrary Git options.
    try:
        base = git('rev-parse', '--verify', args.base + '^{commit}').strip()
        head = git('rev-parse', '--verify', 'HEAD^{commit}').strip()
        changes = changed_paths(base, head, git)
    except subprocess.CalledProcessError:
        parser.exit(2, 'Cannot resolve comparison commits; no clean-monitor claim.\n')
    sensitive = [p for p in changes if p.startswith(PREFIXES)]
    findings = []
    workflows = []
    for path in sorted((ROOT / '.github/workflows').glob('*')):
        if path.suffix not in ('.yaml', '.yml'):
            continue
        if path.is_symlink():
            findings.append({'file': str(path.relative_to(ROOT)), 'rule': 'symlink_workflow_requires_review'})
            continue
        text = path.read_text()
        workflows.append({'file': str(path.relative_to(ROOT)), 'sha256': hashlib.sha256(text.encode()).hexdigest()})
        findings.extend({'file': str(path.relative_to(ROOT)), 'rule': rule} for rule in inspect_workflow(text))
    report = {'scope': 'Changes between two Git snapshots plus selected current-workflow patterns',
              'base': base, 'head': head, 'tracked_worktree_dirty': bool(git('status', '--porcelain', '--untracked-files=no').strip()), 'changed_paths': changes, 'sensitive_paths': sensitive,
              'workflows': workflows, 'findings': findings,
              'review_required': bool(sensitive or findings), 'overall_cis': 'PARTIAL',
              'limits': ['Heuristics are not comprehensive behavioral or insider-threat detection',
                         'Artifact/CI result records findings; no human receipt or incident response verified',
                         'Ruleset/protection history and Enterprise audit-log API are not queried']}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'sensitive_paths': len(sensitive), 'findings': len(findings), 'review_required': report['review_required']}))
    return 2 if findings else 0


if __name__ == '__main__':
    raise SystemExit(main())
