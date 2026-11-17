#!/usr/bin/env python3
"""Offline sandbox: reproducible artifact, SBOM, signatures, encryption and verified local deployment."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def command(*args, expect_failure=False):
    proc = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if expect_failure:
        if proc.returncode == 0:
            raise RuntimeError('Negative test unexpectedly succeeded')
    elif proc.returncode:
        # Do not include command args or stderr that could contain key material.
        raise RuntimeError('Sandbox operation failed: ' + args[0])


def build():
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', compression=zipfile.ZIP_STORED) as archive:
        info = zipfile.ZipInfo('app.py', date_time=(2026, 1, 1, 0, 0, 0))
        info.external_attr = 0o100644 << 16
        archive.writestr(info, (ROOT / 'examples/demo-app/app.py').read_bytes())
    return buffer.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default='reports/supply-chain')
    args = parser.parse_args()
    out = Path(args.output).resolve()
    out.mkdir(parents=True, exist_ok=True)
    for binary in ('openssl', 'python3'):
        if not shutil.which(binary):
            parser.error('Required executable unavailable: ' + binary)
    checks = []
    def record(name, evidence):
        checks.append({'check': name, 'status': 'PASS', 'evidence': evidence, 'scope': 'local demo only'})

    lock = json.loads((ROOT / 'lab-inputs.lock.json').read_text())
    for relative, expected in lock['sha256'].items():
        if digest(ROOT / relative) != expected:
            raise RuntimeError('Input differs from reviewed lock: ' + relative)
    record('locked_inputs', 'Application source and deployment configuration match committed SHA256 values; Git review is the trust boundary.')
    config = json.loads((ROOT / 'deploy/demo.json').read_text())
    if config['production'] or config['network_listener'] or config['entrypoint'] != 'app.py':
        raise RuntimeError('Only the fixed offline sandbox configuration is supported')
    artifact = out / 'application.zip'
    artifact.write_bytes(build())
    if artifact.read_bytes() != build():
        raise RuntimeError('Artifact is not reproducible')
    record('reproducible_artifact', digest(artifact))
    sbom = {'spdxVersion': 'SPDX-2.3', 'dataLicense': 'CC0-1.0', 'SPDXID': 'SPDXRef-DOCUMENT',
            'name': 'cis-demo-application', 'documentNamespace': 'https://example.invalid/spdx/' + digest(artifact),
            'creationInfo': {'creators': ['Tool: cis-sandbox-lab'], 'created': '2026-01-01T00:00:00Z'},
            'packages': [{'SPDXID': 'SPDXRef-Demo', 'name': 'cis-demo-application', 'versionInfo': '1.0.0',
                          'downloadLocation': 'NOASSERTION', 'filesAnalyzed': False,
                          'licenseConcluded': 'NOASSERTION', 'licenseDeclared': 'NOASSERTION',
                          'copyrightText': 'NOASSERTION',
                          'checksums': [{'algorithm': 'SHA256', 'checksumValue': digest(artifact)}]}],
            'relationships': [{'spdxElementId': 'SPDXRef-DOCUMENT', 'relationshipType': 'DESCRIBES', 'relatedSpdxElement': 'SPDXRef-Demo'}],
            'comment': 'First-party demo package only; Python standard library/runtime ' + platform.python_version() + '. No claim of complete third-party or OS inventory.'}
    sbom_path = out / 'application.spdx.json'
    sbom_path.write_text(json.dumps(sbom, indent=2) + '\n')
    provenance = out / 'provenance.json'
    provenance.write_text(json.dumps({'schema': 'lab-provenance-v1', 'artifact_sha256': digest(artifact),
        'source_revision': os.environ.get('GITHUB_SHA', 'local-unattested'),
        'repository': os.environ.get('GITHUB_REPOSITORY', 'local'),
        'run_id': os.environ.get('GITHUB_RUN_ID', 'local'),
        'deployment_config_sha256': digest(ROOT / 'deploy/demo.json'),
        'trust': 'ephemeral lab key; not a trusted release attestation'}, indent=2) + '\n')

    with tempfile.TemporaryDirectory(prefix='cis-lab-') as temp:
        work = Path(temp)
        key, password = work / 'signing.pem', work / 'encryption.pass'
        # Private material never enters the artifact upload directory.
        password.write_text(os.urandom(32).hex())
        password.chmod(0o600)
        command('openssl', 'genpkey', '-algorithm', 'RSA', '-pkeyopt', 'rsa_keygen_bits:3072', '-out', str(key))
        key.chmod(0o600)
        public = out / 'lab-public-key.pem'
        command('openssl', 'pkey', '-in', str(key), '-pubout', '-out', str(public))
        def sign(path):
            command('openssl', 'dgst', '-sha256', '-sign', str(key), '-out', str(path) + '.sig', str(path))
        def verify(path, signature=None, negative=False):
            command('openssl', 'dgst', '-sha256', '-verify', str(public), '-signature', str(signature or (str(path)+'.sig')), str(path), expect_failure=negative)
        for path in (artifact, sbom_path, provenance):
            sign(path)
            verify(path)
        altered = work / 'altered.zip'
        altered.write_bytes(artifact.read_bytes() + b'tampered')
        verify(altered, str(artifact) + '.sig', negative=True)
        record('signed_artifact_sbom_provenance', 'Original signatures accepted; modified artifact rejected. Ephemeral lab identity only.')

        encrypted = out / 'application.zip.enc'
        command('openssl', 'enc', '-aes-256-cbc', '-pbkdf2', '-iter', '200000', '-salt', '-in', str(artifact), '-out', str(encrypted), '-pass', 'file:' + str(password))
        sign(encrypted)
        verify(encrypted)  # Authenticate the ciphertext before decryption.
        changed = work / 'changed.enc'
        changed.write_bytes(encrypted.read_bytes() + b'tampered')
        verify(changed, str(encrypted) + '.sig', negative=True)
        decoded = work / 'decoded.zip'
        command('openssl', 'enc', '-d', '-aes-256-cbc', '-pbkdf2', '-iter', '200000', '-in', str(encrypted), '-out', str(decoded), '-pass', 'file:' + str(password))
        if digest(decoded) != digest(artifact):
            raise RuntimeError('Decrypted artifact differs')
        record('encrypted_roundtrip', 'Ciphertext signature checked before decrypt; modified ciphertext rejected. Keys removed after job.')
        verify(decoded, str(artifact) + '.sig')
        deployment = work / 'deployment'
        deployment.mkdir(mode=0o700)
        with zipfile.ZipFile(decoded) as archive:
            if archive.namelist() != ['app.py']:
                raise RuntimeError('Unexpected archive members')
            (deployment / 'app.py').write_bytes(archive.read('app.py'))
        proc = subprocess.run(['python3', str(deployment / 'app.py')], check=True, capture_output=True, text=True)
        if proc.stdout.strip() != 'CIS sandbox deployment succeeded':
            raise RuntimeError('Sandbox smoke test failed')
        record('verified_local_deployment', 'Verified artifact extracted to temporary private directory; fixed smoke test succeeded; no network or production changes.')
    (out / 'results.json').write_text(json.dumps({'scope': 'local sandbox, not production CIS compliance', 'checks': checks}, indent=2) + '\n')
    print(json.dumps({'checks': len(checks), 'result': 'PASS', 'scope': 'local sandbox only'}))

if __name__ == '__main__':
    main()
