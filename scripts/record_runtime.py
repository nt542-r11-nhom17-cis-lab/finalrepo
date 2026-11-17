#!/usr/bin/env python3
"""Allowlisted runtime evidence: never dump environment, secrets, paths or user identities."""
import datetime
import json
import os
from pathlib import Path
import platform
import ssl
import subprocess


def main():
    evidence = {'checked_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                'system': platform.system(), 'release': platform.release(), 'machine': platform.machine(),
                'python': platform.python_version(), 'openssl': ssl.OPENSSL_VERSION,
                'commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
                'runner': {k: os.environ.get(k) for k in ('RUNNER_OS', 'RUNNER_ARCH', 'ImageOS', 'ImageVersion')},
                'github': {k: os.environ.get(k) for k in ('GITHUB_REPOSITORY', 'GITHUB_RUN_ID', 'GITHUB_RUN_ATTEMPT', 'GITHUB_REF_NAME')},
                'scope': 'Allowlisted metadata for this job only; no complete host/runtime security attestation.'}
    out = Path('reports')
    out.mkdir(exist_ok=True)
    (out / 'runtime.json').write_text(json.dumps(evidence, indent=2) + '\n')
    print(json.dumps({'runtime_evidence': 'reports/runtime.json', 'commit': evidence['commit']}))


if __name__ == '__main__':
    main()
