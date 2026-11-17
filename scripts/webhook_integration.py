#!/usr/bin/env python3
"""Exercise real loopback HTTPS delivery; does not configure GitHub webhooks."""
import argparse
import datetime
import hashlib
import hmac
import json
import secrets
import ssl
import tempfile
import threading
import urllib.error
import uuid
import integration_support
import webhook_receiver


def exercise():
    checks = []
    secret = secrets.token_bytes(32)
    with tempfile.TemporaryDirectory(prefix='cis-webhook-') as temp:
        _, _, context, client = integration_support.tls_material(temp)
        service = webhook_receiver.server(webhook_receiver.WebhookPolicy(secret), context)
        worker = threading.Thread(target=service.serve_forever, daemon=True)
        worker.start()
        url = 'https://127.0.0.1:' + str(service.server_address[1]) + '/webhook'
        def send(name, expected, body=None, event='push', delivery=None, signature=None, content_type='application/json'):
            body = body if body is not None else json.dumps({'probe': str(uuid.uuid4())}).encode()
            delivery = delivery or str(uuid.uuid4())
            signature = signature or 'sha256=' + hmac.new(secret, body, hashlib.sha256).hexdigest()
            status, _, _ = integration_support.request(url, client, 'POST', body,
                {'Content-Type': content_type, 'X-Hub-Signature-256': signature,
                 'X-GitHub-Event': event, 'X-GitHub-Delivery': delivery})
            if status != expected:
                raise RuntimeError('Webhook check failed: ' + name + ', observed HTTP ' + str(status))
            checks.append({'check': name, 'http': status, 'expected_http': expected, 'result': 'PASS'})
        try:
            body = b'{"probe":"replay-test"}'
            delivery = str(uuid.uuid4())
            send('valid HMAC delivery accepted', 202, body=body, delivery=delivery)
            send('same delivery and body rejected', 409, body=body, delivery=delivery)
            send('same body with changed delivery header rejected', 409, body=body)
            send('wrong HMAC rejected', 401, signature='sha256=' + '0' * 64)
            send('modified body rejected', 401, body=b'{"modified":true}',
                 signature='sha256=' + hmac.new(secret, b'{"original":true}', hashlib.sha256).hexdigest())
            send('disallowed event rejected', 403, event='repository_dispatch')
            send('invalid delivery ID rejected', 400, delivery='not-a-uuid')
            send('invalid JSON rejected after signature verification', 400, body=b'not-json')
            send('oversized body rejected', 413, body=b'x' * 65537)
            send('wrong content type rejected', 415, content_type='text/plain')
            try:
                integration_support.request(url, ssl.create_default_context(), 'POST', b'{}')
            except urllib.error.URLError as error:
                if not isinstance(error.reason, ssl.SSLCertVerificationError):
                    raise
                checks.append({'check': 'untrusted TLS certificate rejected', 'result': 'PASS'})
            else:
                raise RuntimeError('Untrusted certificate accepted')
        finally:
            service.shutdown()
            service.server_close()
            worker.join(timeout=5)
    return {'checked_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'scope': 'Real HTTPS loopback server and synthetic deliveries; no GitHub webhook installation or build trigger',
            'checks': checks, 'credentials_exported': False, 'service_stopped': not worker.is_alive(),
            'overall_cis': 'PARTIAL',
            'limits': ['In-memory replay cache expires after 600 seconds and is lost on restart',
                       'Body deduplication may reject legitimate identical deliveries; deployment policy must account for this',
                       'No actual GitHub delivery, external endpoint, app permission or production rollout verified']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default='reports/webhook-integration')
    args = parser.parse_args()
    report = exercise()
    integration_support.write_report(args.output, report)
    print(json.dumps({'checks': len(report['checks']), 'service_stopped': report['service_stopped'], 'scope': report['scope']}))


if __name__ == '__main__':
    main()
