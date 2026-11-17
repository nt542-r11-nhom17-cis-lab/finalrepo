import hashlib
import hmac
from pathlib import Path
import sys
import unittest
import uuid
import io
import tarfile
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import inventory_organization
import registry_integration
import webhook_receiver
import verify_registry_scan
import build_registry


class WebhookPolicyTests(unittest.TestCase):
    def setUp(self):
        self.secret = b'x' * 32
        self.policy = webhook_receiver.WebhookPolicy(self.secret)

    def call(self, body=b'{"sample":1}', delivery=None, event='push', signature=None, now=1):
        return self.policy.evaluate(body, signature or 'sha256=' + hmac.new(self.secret, body, hashlib.sha256).hexdigest(),
                                    event, delivery or str(uuid.uuid4()), now=now)

    def test_changed_delivery_header_cannot_replay_signed_body(self):
        self.assertEqual(self.call(), 202)
        self.assertEqual(self.call(delivery=str(uuid.uuid4())), 409)

    def test_rejected_signature_does_not_poison_cache(self):
        self.assertEqual(self.call(signature='sha256=' + '0' * 64), 401)
        self.assertEqual(self.call(), 202)

    def test_cache_exhaustion_is_fail_closed(self):
        self.policy.max_entries = 2
        self.assertEqual(self.call(), 202)
        self.assertEqual(self.call(body=b'{"different":2}'), 503)
        self.assertEqual(self.call(), 409)

    def test_cache_expiry_scope_is_explicit(self):
        self.assertEqual(self.call(now=1), 202)
        self.assertEqual(self.call(now=602), 202)

    def test_valid_signature_does_not_authorize_wrong_event(self):
        self.assertEqual(self.call(event='repository_dispatch'), 403)

    def test_signed_non_object_payload_is_rejected(self):
        self.assertEqual(self.call(body=b'[]'), 400)


class IntegrationBoundaryTests(unittest.TestCase):
    def test_source_archive_cannot_write_outside_extraction_root(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive = root / 'input.tar.gz'
            with tarfile.open(archive, 'w:gz') as tar:
                member = tarfile.TarInfo('../escaped')
                member.size = 1
                tar.addfile(member, io.BytesIO(b'x'))
            with self.assertRaises(tarfile.FilterError):
                build_registry.unpack('https://unused.invalid', build_registry.file_hash(archive), archive, root / 'source')
            self.assertFalse((root / 'escaped').exists())
            self.assertFalse((root / 'source').exists())

    def test_unreviewed_registry_executable_is_rejected_before_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            binary = Path(directory) / 'unreviewed'
            binary.write_bytes(b'not-a-reviewed-binary')
            with self.assertRaises(ValueError):
                registry_integration.load_binary(binary)

    def test_empty_scanner_report_never_passes_binary_coverage(self):
        self.assertFalse(verify_registry_scan.evaluate({'SchemaVersion': 2}, 'a' * 64)['gate_passed'])

    def test_wrong_binary_or_missing_packages_never_passes(self):
        for record in ({'Type': 'gobinary', 'Target': 'registry-' + 'b' * 64, 'Packages': [{'Name': 'stdlib'}]},
                       {'Type': 'gobinary', 'Target': 'registry-' + 'a' * 64}):
            self.assertFalse(verify_registry_scan.evaluate({'Results': [record]}, 'a' * 64)['gate_passed'])

    def test_high_finding_with_inventory_is_not_clean(self):
        row = {'Type': 'gobinary', 'Target': 'registry-' + 'a' * 64, 'Packages': [{'Name': 'stdlib'}],
               'Vulnerabilities': [{'Severity': 'HIGH'}]}
        self.assertFalse(verify_registry_scan.evaluate({'Results': [row]}, 'a' * 64)['gate_passed'])

    def test_registry_redirect_cannot_receive_credentials(self):
        for location in ('https://example.com/v2/cis/lab/blobs/uploads/x',
                         'http://127.0.0.1:5000/v2/cis/lab/blobs/uploads/x',
                         '/unrelated'):
            with self.assertRaises(ValueError):
                registry_integration.upload_location('https://127.0.0.1:5000', location)

    def test_role_subset_never_proves_full_access_or_mfa(self):
        result = inventory_organization.summarize_roles([{'role_name': 'admin'}], {'http': 200, 'pagination_complete': True})
        self.assertFalse(result['full_effective_access_verified'])
        self.assertEqual(result['mfa'], 'UNKNOWN')

    def test_partial_member_pagination_is_preserved(self):
        replies = iter([{'http': 200, 'data': [{}] * 100}, {'http': 403}])
        rows, scope = inventory_organization.list_pages('/test', None, fetch=lambda *args: next(replies))
        self.assertEqual(len(rows), 100)
        self.assertFalse(scope['pagination_complete'])
        self.assertEqual(scope['http'], 403)


if __name__ == '__main__':
    unittest.main()
