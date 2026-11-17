"""TLS and subprocess helpers for isolated loopback integration tests."""
import json
import os
from pathlib import Path
import ssl
import subprocess
import urllib.error
import urllib.parse
import urllib.request


def command(*args):
    return subprocess.run(args, check=True, capture_output=True,
                          env={'PATH': os.defpath, 'LANG': 'C.UTF-8'}).stdout


def tls_material(directory):
    root = Path(directory)
    key, cert = root / 'tls-private.pem', root / 'tls-cert.pem'
    command('openssl', 'req', '-x509', '-newkey', 'rsa:3072', '-sha256', '-nodes',
            '-keyout', str(key), '-out', str(cert), '-days', '1',
            '-subj', '/CN=CIS local integration', '-addext', 'subjectAltName=IP:127.0.0.1,DNS:localhost')
    key.chmod(0o600)
    server = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    server.minimum_version = ssl.TLSVersion.TLSv1_2
    server.load_cert_chain(cert, key)
    client = ssl.create_default_context(cafile=str(cert))
    client.minimum_version = ssl.TLSVersion.TLSv1_2
    return cert, key, server, client


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError('Unexpected redirect from loopback test service')


def request(url, context, method='GET', body=None, headers=None):
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != 'https' or parsed.hostname != '127.0.0.1' or parsed.username or parsed.password:
        raise ValueError('Integration requests must use HTTPS loopback without URL credentials')
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect(),
                                        urllib.request.HTTPSHandler(context=context))
    req = urllib.request.Request(url, data=body, method=method, headers=headers or {})
    try:
        with opener.open(req, timeout=5) as response:
            return response.status, dict(response.headers), response.read()
    except urllib.error.HTTPError as error:
        return error.code, dict(error.headers), error.read()


def write_report(output, report):
    out = Path(output)
    out.mkdir(parents=True, exist_ok=True)
    (out / 'results.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
