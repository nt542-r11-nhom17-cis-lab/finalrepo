#!/usr/bin/env python3
"""Sign a committed-source bundle. Ephemeral CI key is lab evidence, not release trust."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PAYLOADS = ('source.zip', 'project.spdx.json', 'provenance.json')


def run(*args):
    return subprocess.run(args, check=True, capture_output=True).stdout


def sha(data):
    return hashlib.sha256(data).hexdigest()


def fingerprint(public_key):
    return sha(run('openssl', 'pkey', '-pubin', '-in', str(public_key), '-outform', 'DER'))


def verify(directory, trusted_fingerprint):
    """The fingerprint must arrive through an independently reviewed run/log channel."""
    out = Path(directory)
    if fingerprint(out / 'public.pem') != trusted_fingerprint:
        raise ValueError('Signing key differs from trusted fingerprint')
    run('openssl', 'dgst', '-sha256', '-verify', str(out / 'public.pem'),
        '-signature', str(out / 'manifest.sig'), str(out / 'manifest.json'))
    manifest = json.loads((out / 'manifest.json').read_text())
    if set(manifest['sha256']) != set(PAYLOADS):
        raise ValueError('Missing or unexpected signed payload')
    for name in PAYLOADS:
        if sha((out / name).read_bytes()) != manifest['sha256'][name]:
            raise ValueError('Payload digest mismatch: ' + name)
    return manifest


def generate(out):
    out.mkdir(parents=True, exist_ok=True)
    commit = run('git', '-C', str(ROOT), 'rev-parse', 'HEAD').decode().strip()
    tree = run('git', '-C', str(ROOT), 'rev-parse', 'HEAD^{tree}').decode().strip()
    source = run('git', '-C', str(ROOT), 'archive', '--format=zip', 'HEAD')
    (out / 'source.zip').write_bytes(source)
    lock = json.loads(run('git', '-C', str(ROOT), 'show', 'HEAD:config/python-scanner-lock.json'))
    packages = []
    relationships = []
    for i, item in enumerate(lock['packages']):
        sid = 'SPDXRef-Scanner-' + str(i)
        packages.append({'SPDXID': sid, 'name': item['name'], 'versionInfo': item['version'],
                         'downloadLocation': 'https://pypi.org/project/' + item['name'] + '/' + item['version'] + '/',
                         'filesAnalyzed': False, 'licenseConcluded': 'NOASSERTION',
                         'licenseDeclared': 'NOASSERTION', 'copyrightText': 'NOASSERTION',
                         'checksums': [{'algorithm': 'SHA256', 'checksumValue': item['sha256']}]})
        relationships.append({'spdxElementId': 'SPDXRef-DOCUMENT', 'relationshipType': 'DESCRIBES', 'relatedSpdxElement': sid})
    now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    sbom = {'spdxVersion': 'SPDX-2.3', 'dataLicense': 'CC0-1.0', 'SPDXID': 'SPDXRef-DOCUMENT',
            'name': 'Committed scanner toolchain inventory',
            'documentNamespace': 'https://github.com/nt542-r11-nhom17-cis-lab/finalrepo/sbom/' + commit,
            'creationInfo': {'created': now, 'creators': ['Tool: cis-project-bundle']},
            'documentComment': '32 locked scanner wheels only. Not supplier-issued SBOM; dependency graph, OS and downloaded tools excluded.',
            'packages': packages, 'relationships': relationships}
    (out / 'project.spdx.json').write_text(json.dumps(sbom, indent=2) + '\n')
    provenance = {'schema': 'cis-lab-provenance-v1', 'commit': commit, 'tree': tree,
                  'source_sha256': sha(source), 'created': now,
                  'repository': os.environ.get('GITHUB_REPOSITORY', 'local'),
                  'run_id': os.environ.get('GITHUB_RUN_ID'), 'run_attempt': os.environ.get('GITHUB_RUN_ATTEMPT'),
                  'trust': 'Ephemeral same-job key. Not SLSA certification or independent supplier attestation.'}
    (out / 'provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
    manifest = {'commit': commit, 'scope': 'Three payloads of this branch run only, not every release',
                'sha256': {name: sha((out / name).read_bytes()) for name in PAYLOADS}}
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    with tempfile.TemporaryDirectory(prefix='cis-signing-') as temp:
        key = Path(temp) / 'private.pem'
        run('openssl', 'genpkey', '-algorithm', 'RSA', '-pkeyopt', 'rsa_keygen_bits:3072', '-out', str(key))
        key.chmod(0o600)
        run('openssl', 'pkey', '-in', str(key), '-pubout', '-out', str(out / 'public.pem'))
        run('openssl', 'dgst', '-sha256', '-sign', str(key), '-out', str(out / 'manifest.sig'), str(out / 'manifest.json'))
    trusted = fingerprint(out / 'public.pem')
    verify(out, trusted)
    # Exercise a rejected payload without leaving modified evidence behind.
    original = (out / 'source.zip').read_bytes()
    try:
        (out / 'source.zip').write_bytes(original + b'tampered')
        try:
            verify(out, trusted)
        except ValueError:
            rejected = True
        else:
            raise RuntimeError('Tampered payload accepted')
    finally:
        (out / 'source.zip').write_bytes(original)
    verify(out, trusted)
    result = {'scope': manifest['scope'], 'commit': commit, 'payloads_verified': len(PAYLOADS),
              'tampered_payload_rejected': rejected, 'public_key_sha256_der': trusted,
              'private_key_exported': False, 'overall_cis': 'PARTIAL'}
    (out / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', default='reports/project-bundle')
    p.add_argument('--verify', action='store_true')
    p.add_argument('--trusted-fingerprint')
    args = p.parse_args()
    if args.verify:
        if not args.trusted_fingerprint:
            p.error('--verify requires an independently trusted --trusted-fingerprint')
        verify(args.output, args.trusted_fingerprint)
        print('Verified signed manifest and all payloads')
    else:
        generate(Path(args.output))


if __name__ == '__main__':
    main()
