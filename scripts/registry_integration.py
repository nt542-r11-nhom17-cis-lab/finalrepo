#!/usr/bin/env python3
"""Real Distribution registry over verified loopback TLS and bcrypt authentication."""
import argparse
import base64
import datetime
import hashlib
import importlib
import io
import json
import os
from pathlib import Path
import secrets
import socket
import ssl
import subprocess
import tarfile
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import integration_support
import build_registry

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = 'application/vnd.oci.image.manifest.v1+json'


def digest(body):
    return 'sha256:' + hashlib.sha256(body).hexdigest()


def load_binary(destination=None):
    lock = json.loads((ROOT / 'config/registry-integration.lock.json').read_text())
    if destination:
        binary = Path(destination)
    else:
        cache = Path(os.environ.get('RUNNER_TEMP', tempfile.gettempdir())) / 'cis-registry-bin'
        cache.mkdir(mode=0o700, exist_ok=True)
        if cache.is_symlink() or cache.stat().st_uid != os.getuid() or cache.stat().st_mode & 0o077:
            raise ValueError('Registry binary cache must be an owned private directory')
        binary = cache / ('registry-' + lock['binary_sha256'])
        if not binary.exists():
            if lock.get('mode') == 'source-build':
                build_registry.build_binary(lock, cache, binary)
                return binary, lock
            with urllib.request.urlopen(lock['url'], timeout=60) as response:
                archive = response.read(32 * 1024 * 1024 + 1)
            if hashlib.sha256(archive).hexdigest() != lock['archive_sha256']:
                raise ValueError('Registry archive does not match pinned SHA256')
            with tarfile.open(fileobj=io.BytesIO(archive), mode='r:gz') as tar:
                entries = [m for m in tar.getmembers() if m.name.lstrip('./') == 'registry' and m.isfile()]
                if len(entries) != 1 or entries[0].size > 64 * 1024 * 1024:
                    raise ValueError('Unexpected registry archive contents')
                data = tar.extractfile(entries[0]).read()
            # Avoid following a pre-existing symlink in a shared temporary directory.
            with binary.open('xb') as handle:
                handle.write(data)
            binary.chmod(0o700)
    if binary.is_symlink() or hashlib.sha256(binary.read_bytes()).hexdigest() != lock['binary_sha256']:
        raise ValueError('Registry executable does not match pinned SHA256')
    return binary, lock


def upload_location(base, location):
    target = urllib.parse.urljoin(base, location)
    parsed, expected = urllib.parse.urlsplit(target), urllib.parse.urlsplit(base)
    if parsed.scheme != 'https' or parsed.netloc != expected.netloc or not parsed.path.startswith('/v2/cis/lab/blobs/uploads/'):
        raise ValueError('Unexpected upload location; credentials will not be forwarded')
    return target


def signature_valid(public, payload, signature):
    result = subprocess.run(['openssl', 'dgst', '-sha256', '-verify', str(public),
                             '-signature', str(signature), str(payload)], capture_output=True,
                            env={'PATH': os.defpath, 'LANG': 'C.UTF-8'})
    return result.returncode == 0


def exercise(binary):
    checks = []
    def record(name, expected, actual):
        if actual != expected:
            raise RuntimeError('Registry check failed: ' + name)
        checks.append({'check': name, 'expected': expected, 'observed': actual, 'result': 'PASS'})
    # This integration targets Python 3.12 on Ubuntu 24.04. crypt is used only
    # for bcrypt htpasswd generation; no weak fallback is accepted.
    crypt = importlib.import_module('crypt')
    if not hasattr(crypt, 'METHOD_BLOWFISH'):
        raise RuntimeError('bcrypt-capable htpasswd generator required')
    with tempfile.TemporaryDirectory(prefix='cis-registry-service-') as directory:
        temp = Path(directory)
        cert, tls_key, _, client = integration_support.tls_material(temp)
        password = secrets.token_urlsafe(32)
        hashed = crypt.crypt(password, crypt.mksalt(crypt.METHOD_BLOWFISH))
        if not hashed.startswith(('$2a$', '$2b$', '$2y$')):
            raise RuntimeError('bcrypt htpasswd generation failed')
        auth_file = temp / 'htpasswd'
        auth_file.write_text('cis-publisher:' + hashed + '\n')
        auth_file.chmod(0o600)
        with socket.socket() as probe:
            probe.bind(('127.0.0.1', 0))
            port = probe.getsockname()[1]
        base = 'https://127.0.0.1:' + str(port)
        config = {'version': 0.1, 'log': {'level': 'error'},
                  'storage': {'filesystem': {'rootdirectory': str(temp / 'data')}},
                  'http': {'addr': '127.0.0.1:' + str(port), 'host': base,
                           'secret': secrets.token_urlsafe(32),
                           'tls': {'certificate': str(cert), 'key': str(tls_key)}},
                  'auth': {'htpasswd': {'realm': 'cis-local-registry', 'path': str(auth_file)}}}
        # JSON is a YAML subset supported by Distribution's configuration parser.
        config_path = temp / 'config.yml'
        config_path.write_text(json.dumps(config))
        config_path.chmod(0o600)
        proc = subprocess.Popen([str(binary), 'serve', str(config_path)], stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL, env={'PATH': os.defpath, 'LANG': 'C.UTF-8'})
        auth = 'Basic ' + base64.b64encode(('cis-publisher:' + password).encode()).decode()
        headers = {'Authorization': auth}
        def call(path, method='GET', body=None, extra=None, authenticated=True):
            return integration_support.request(base + path, client, method, body,
                                               {**(headers if authenticated else {}), **(extra or {})})
        try:
            ready = False
            for _ in range(100):
                if proc.poll() is not None:
                    raise RuntimeError('Registry exited during startup')
                try:
                    if call('/v2/')[0] == 200:
                        ready = True
                        break
                except (urllib.error.URLError, TimeoutError):
                    pass
                time.sleep(0.1)
            if not ready:
                raise RuntimeError('Registry TLS startup timeout')
            record('anonymous registry access denied', 401, call('/v2/', authenticated=False)[0])
            wrong = 'Basic ' + base64.b64encode(b'cis-publisher:invalid-probe').decode()
            record('wrong credentials denied', 401, call('/v2/', extra={'Authorization': wrong})[0])
            record('authenticated registry access accepted', 200, call('/v2/')[0])
            record('anonymous upload denied', 401, call('/v2/cis/lab/blobs/uploads/', 'POST', b'', authenticated=False)[0])
            try:
                integration_support.request(base + '/v2/', ssl.create_default_context())
            except urllib.error.URLError as error:
                if not isinstance(error.reason, ssl.SSLCertVerificationError):
                    raise
                record('untrusted TLS certificate denied', True, True)
            else:
                raise RuntimeError('Untrusted registry certificate accepted')
            private, public = temp / 'signing-private.pem', temp / 'signing-public.pem'
            integration_support.command('openssl', 'genpkey', '-algorithm', 'RSA', '-pkeyopt', 'rsa_keygen_bits:3072', '-out', str(private))
            private.chmod(0o600)
            integration_support.command('openssl', 'pkey', '-in', str(private), '-pubout', '-out', str(public))
            published = []
            def blob(body):
                code, reply, _ = call('/v2/cis/lab/blobs/uploads/', 'POST', b'')
                if code != 202:
                    raise RuntimeError('Registry upload initialization failed')
                location = next((v for k, v in reply.items() if k.lower() == 'location'), None)
                if not location:
                    raise RuntimeError('Registry omitted upload location')
                target = upload_location(base, location)
                sep = '&' if '?' in target else '?'
                target += sep + urllib.parse.urlencode({'digest': digest(body)})
                code, _, _ = integration_support.request(target, client, 'PUT', body,
                                                        {**headers, 'Content-Type': 'application/octet-stream'})
                if code != 201:
                    raise RuntimeError('Registry blob digest upload failed')
                return {'mediaType': 'application/octet-stream', 'digest': digest(body), 'size': len(body)}
            for version in ('0.1.0', '0.1.1'):
                payload = ('CIS isolated artifact ' + version).encode()
                payload_path, signature_path = temp / 'artifact', temp / 'artifact.sig'
                payload_path.write_bytes(payload)
                integration_support.command('openssl', 'dgst', '-sha256', '-sign', str(private), '-out', str(signature_path), str(payload_path))
                record('pipeline verifies signature before upload ' + version, True, signature_valid(public, payload_path, signature_path))
                descriptor = blob(payload)
                signature = blob(signature_path.read_bytes())
                empty = blob(b'{}')
                empty['mediaType'] = 'application/vnd.oci.empty.v1+json'
                manifest = {'schemaVersion': 2, 'mediaType': MANIFEST, 'artifactType': 'application/vnd.cis.lab.v1',
                            'config': empty, 'layers': [descriptor, signature]}
                encoded = json.dumps(manifest, sort_keys=True).encode()
                record('OCI manifest upload accepted ' + version, 201,
                       call('/v2/cis/lab/manifests/' + version, 'PUT', encoded, {'Content-Type': MANIFEST})[0])
                code, _, received_manifest = call('/v2/cis/lab/manifests/' + version, extra={'Accept': MANIFEST})
                record('downloaded manifest digest matches ' + version, (200, digest(encoded)), (code, digest(received_manifest)))
                code, _, received = call('/v2/cis/lab/blobs/' + descriptor['digest'])
                record('downloaded blob digest matches ' + version, (200, descriptor['digest']), (code, digest(received)))
                code, _, received_signature = call('/v2/cis/lab/blobs/' + signature['digest'])
                record('downloaded signature digest matches ' + version, (200, signature['digest']), (code, digest(received_signature)))
                downloaded_signature = temp / 'downloaded.sig'
                downloaded_signature.write_bytes(received_signature)
                downloaded = temp / 'downloaded'
                downloaded.write_bytes(received)
                record('downloaded signature verifies ' + version, True, signature_valid(public, downloaded, downloaded_signature))
                downloaded.write_bytes(received + b'modified')
                record('modified downloaded artifact rejected ' + version, False, signature_valid(public, downloaded, downloaded_signature))
                downloaded.write_bytes(received)
                corrupt = bytes([received_signature[0] ^ 1]) + received_signature[1:]
                downloaded_signature.write_bytes(corrupt)
                record('modified downloaded signature rejected ' + version, False, signature_valid(public, downloaded, downloaded_signature))
                published.append({'version': version, 'artifact_digest': descriptor['digest'], 'manifest_digest': digest(encoded)})
            record('anonymous known-artifact download denied', 401,
                   call('/v2/cis/lab/blobs/' + published[0]['artifact_digest'], authenticated=False)[0])
            code, _, raw_tags = call('/v2/cis/lab/tags/list')
            tags = json.loads(raw_tags).get('tags') if code == 200 else None
            record('all published test versions inventoried', ['0.1.0', '0.1.1'], sorted(tags) if tags else None)
        finally:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=5)
        stopped = proc.poll() is not None
    return {'checked_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'scope': 'Real temporary Distribution registry on HTTPS loopback with one bcrypt publisher; no production or GitHub settings changes',
            'checks': checks, 'published_versions': published, 'service_stopped': stopped,
            'credentials_exported': False, 'overall_cis': 'PARTIAL',
            'limits': ['Basic-auth test account has no MFA or external IdP',
                       'Signature verification is in this pipeline client; registry-side signature admission is not configured',
                       'Registry permissions are not per-user read/write RBAC; no organization-wide access inventory',
                       'Two test versions and ephemeral signing key do not establish production release trust']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--registry', help='Path to executable; must match pinned binary SHA256')
    parser.add_argument('--output', default='reports/registry-integration')
    args = parser.parse_args()
    binary, lock = load_binary(args.registry)
    report = exercise(binary)
    report['registry_version'] = lock['version']
    report['binary_sha256'] = lock['binary_sha256']
    report['archive_sha256'] = lock['archive_sha256']
    if lock.get('mode') == 'source-build':
        report['build'] = {key: lock['build'][key] for key in
                           ('source_commit', 'go_version', 'module_locks', 'patched_dependencies')}
    integration_support.write_report(args.output, report)
    print(json.dumps({'checks': len(report['checks']), 'versions': len(report['published_versions']),
                      'service_stopped': report['service_stopped'], 'overall_cis': report['overall_cis']}))


if __name__ == '__main__':
    main()
