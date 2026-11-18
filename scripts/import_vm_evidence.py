#!/usr/bin/env python3
"""Validate untrusted user-supplied lab reports without extracting or executing archive content."""
import argparse
import hashlib
import json
from pathlib import Path
import tarfile

EXPECTED = {
    'supply-chain/results.json': ('checks', 'status', 5),
    'registry-lab/results.json': ('tests', 'result', 13),
    'webhook-https/results.json': ('checks', 'result', 11),
}
MAX_REPORT_BYTES = 100_000


def review_archive(path):
    reports = []
    with tarfile.open(path, 'r:gz') as archive:
        seen = set()
        # Stream metadata and reject early; never extract archive paths to disk.
        for member in archive:
            if member.name not in EXPECTED or member.name in seen:
                raise ValueError('Unexpected or duplicate archive member')
            if not member.isfile() or not 0 < member.size <= MAX_REPORT_BYTES:
                raise ValueError('Reports must be bounded regular files')
            seen.add(member.name)
            raw = archive.extractfile(member).read(MAX_REPORT_BYTES + 1)
            data = json.loads(raw)
            key, result_key, expected_count = EXPECTED[member.name]
            checks = data.get(key) if isinstance(data, dict) else None
            if not isinstance(checks, list) or len(checks) != expected_count:
                raise ValueError('Unexpected report check count')
            label = 'test' if key == 'tests' else 'check'
            names = []
            results = []
            for check in checks:
                if not isinstance(check, dict):
                    raise ValueError('Malformed check')
                name, result = check.get(label), check.get(result_key)
                if not isinstance(name, str) or not name or len(name) > 200:
                    raise ValueError('Invalid check name')
                if result not in ('PASS', 'FAIL') or name in names:
                    raise ValueError('Unknown result or duplicate check')
                names.append(name)
                results.append({'check': name, 'result': result})
            if not isinstance(data.get('scope'), str) or len(data['scope']) > 500:
                raise ValueError('Missing or invalid scope')
            reports.append({'file': member.name, 'sha256': hashlib.sha256(raw).hexdigest(),
                            'scope': data['scope'], 'checks': results,
                            'passed': sum(x['result'] == 'PASS' for x in results),
                            'total': len(results)})
        if seen != set(EXPECTED):
            raise ValueError('Missing required report')
    reports.sort(key=lambda x: x['file'])
    digest = hashlib.sha256()
    with Path(path).open('rb') as source:
        for chunk in iter(lambda: source.read(65536), b''):
            digest.update(chunk)
    return {'schema': 'user-vm-evidence-review-v1',
            'archive_sha256': digest.hexdigest(),
            'source': 'User-uploaded reports; no authenticated remote execution attestation',
            'reports': reports, 'passed': sum(x['passed'] for x in reports),
            'total': sum(x['total'] for x in reports), 'overall_cis': 'PARTIAL',
            'limits': ['Report contents are supplied evidence, not independently observed VM execution',
                       'Registry policy fixture does not verify real MFA, IdP or registry deployment',
                       'HTTPS delivery uses loopback and synthetic payloads, not actual GitHub delivery',
                       'No production access, default-password audit or full CIS control is established']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('--output', type=Path, default=Path('reports/vm-evidence/results.json'))
    args = parser.parse_args()
    try:
        report = review_archive(args.archive)
    except (ValueError, OSError, tarfile.TarError) as error:
        parser.exit(2, 'Invalid lab evidence: ' + type(error).__name__ + '\n')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'passed': report['passed'], 'total': report['total'], 'overall_cis': report['overall_cis']}))
    return 0 if report['passed'] == report['total'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
