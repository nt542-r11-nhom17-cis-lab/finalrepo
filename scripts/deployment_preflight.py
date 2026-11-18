#!/usr/bin/env python3
"""Read-only host preflight. Never reads password hashes, attempts login or changes accounts."""
import argparse
import datetime
import grp
import json
import os
from pathlib import Path
import pwd
import shutil
import subprocess


SSH_FIELDS = ('permitrootlogin', 'passwordauthentication', 'pubkeyauthentication',
              'permitemptypasswords', 'usepam')


def ssh_settings(run=subprocess.run, executable=None):
    binary = executable or shutil.which('sshd')
    if not binary and Path('/usr/sbin/sshd').is_file():
        binary = '/usr/sbin/sshd'
    if not binary:
        return {'execution': 'UNAVAILABLE', 'settings': {key: 'UNKNOWN' for key in SSH_FIELDS}}
    try:
        response = run([binary, '-T'], capture_output=True, text=True, timeout=10, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return {'execution': 'UNAVAILABLE', 'settings': {key: 'UNKNOWN' for key in SSH_FIELDS}}
    if response.returncode != 0:
        return {'execution': 'INSUFFICIENT_PRIVILEGE_OR_INVALID_CONFIG',
                'settings': {key: 'UNKNOWN' for key in SSH_FIELDS}}
    values = dict(line.split(None, 1) for line in response.stdout.splitlines() if len(line.split(None, 1)) == 2)
    return {'execution': 'OBSERVED', 'settings': {key: values.get(key, 'UNKNOWN') for key in SSH_FIELDS},
            'limits': 'sshd -T without connection context does not resolve all Match blocks or live daemon flags'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('reports/deployment-preflight/results.json'))
    args = parser.parse_args()
    accounts = pwd.getpwall()
    groups = {g.gr_gid: g.gr_name for g in grp.getgrall()}
    current = {groups.get(gid, 'UNKNOWN') for gid in os.getgroups()}
    report = {'checked_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'scope': 'Host executing this command; declared lab evidence only, no production attestation',
              'running_as_root': os.geteuid() == 0,
              'current_privileged_group_flags': {name: name in current for name in ('sudo', 'wheel', 'docker', 'lxd')},
              'uid_zero_account_count': sum(account.pw_uid == 0 for account in accounts),
              'interactive_account_count': sum(account.pw_shell not in ('', '/usr/sbin/nologin', '/sbin/nologin', '/bin/false') for account in accounts),
              'ssh': ssh_settings(), 'default_password_test': 'NOT_PERFORMED',
              'password_hashes_read': False, 'login_attempts': 0, 'mutations': 0,
              'overall_cis': 'MANUAL_REVIEW',
              'limits': ['Does not establish effective sudo, directory identities, cloud IAM or production ACLs',
                         'Cannot determine default passwords from account names or a password-authentication flag',
                         'Requires authorized target execution and owner review before production conclusions']}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'mutations': 0, 'ssh_execution': report['ssh']['execution'], 'overall_cis': report['overall_cis']}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
