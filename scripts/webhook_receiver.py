#!/usr/bin/env python3
"""Loopback HTTPS webhook receiver example; no build/deploy commands are executed."""
import argparse
import collections
import hashlib
import hmac
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import re
import threading
import time
import uuid
import ssl


class WebhookPolicy:
    def __init__(self, secret, ttl=600, max_entries=8192):
        if len(secret) < 32:
            raise ValueError('At least 32 bytes of webhook secret are required')
        self.secret = secret
        self.ttl = ttl
        self.max_entries = max_entries
        self.seen = collections.OrderedDict()
        self.lock = threading.Lock()

    def evaluate(self, body, signature, event, delivery, now=None):
        if not re.fullmatch(r'sha256=[a-f0-9]{64}', signature or ''):
            return 401
        expected = 'sha256=' + hmac.new(self.secret, body, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected, signature):
            return 401
        if event not in {'ping', 'push'}:
            return 403
        try:
            if str(uuid.UUID(delivery)) != delivery:
                return 400
            payload = json.loads(body)
        except (ValueError, TypeError, UnicodeDecodeError):
            return 400
        if not isinstance(payload, dict):
            return 400
        # Delivery headers are not covered by GitHub's body HMAC. Retain both
        # delivery IDs and body digests so changing the header cannot replay a body.
        keys = ('delivery:' + delivery, 'body:' + hashlib.sha256(body).hexdigest())
        now = time.monotonic() if now is None else now
        with self.lock:
            while self.seen and next(iter(self.seen.values())) <= now:
                self.seen.popitem(last=False)
            if any(key in self.seen for key in keys):
                return 409
            if len(self.seen) + len(keys) > self.max_entries:
                return 503
            for key in keys:
                self.seen[key] = now + self.ttl
        return 202


def handler(policy):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            pass  # Never log raw payloads, Authorization headers or signatures.

        def reply(self, status):
            self.send_response(status)
            self.send_header('Content-Length', '0')
            self.send_header('Connection', 'close')
            self.end_headers()

        def do_POST(self):
            self.connection.settimeout(3)
            if self.path != '/webhook':
                self.reply(404)
                return
            if self.headers.get('Transfer-Encoding'):
                self.reply(400)
                return
            lengths = self.headers.get_all('Content-Length', [])
            if len(lengths) != 1 or not re.fullmatch(r'[0-9]{1,5}', lengths[0]):
                self.reply(411)
                return
            length = int(lengths[0])
            if length > 65536:
                self.reply(413)
                return
            if self.headers.get_content_type() != 'application/json':
                self.reply(415)
                return
            for key in ('X-Hub-Signature-256', 'X-GitHub-Event', 'X-GitHub-Delivery'):
                if len(self.headers.get_all(key, [])) != 1:
                    self.reply(400)
                    return
            try:
                body = self.rfile.read(length)
            except (TimeoutError, OSError):
                self.reply(408)
                return
            if len(body) != length:
                self.reply(400)
                return
            status = policy.evaluate(body, self.headers.get('X-Hub-Signature-256'),
                                     self.headers.get('X-GitHub-Event'), self.headers.get('X-GitHub-Delivery'))
            self.reply(status)
    return Handler


def server(policy, tls_context):
    service = ThreadingHTTPServer(('127.0.0.1', 0), handler(policy))
    service.daemon_threads = True
    service.socket = tls_context.wrap_socket(service.socket, server_side=True)
    return service


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--secret-file', required=True)
    parser.add_argument('--certificate', required=True)
    parser.add_argument('--private-key', required=True)
    args = parser.parse_args()
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.load_cert_chain(args.certificate, args.private_key)
    service = server(WebhookPolicy(Path(args.secret_file).read_bytes()), context)
    print('HTTPS loopback receiver port:', service.server_address[1], flush=True)
    try:
        service.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        service.server_close()


if __name__ == '__main__':
    main()
