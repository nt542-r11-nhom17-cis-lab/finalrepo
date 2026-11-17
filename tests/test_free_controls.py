import json
import datetime
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import audit_free_controls
import monitor_action_owners
import project_bundle
import inventory_governance


class FreeEvidenceTests(unittest.TestCase):
    def test_mid_pagination_denial_retains_partial_and_never_claims_complete(self):
        replies = iter([{'http': 200, 'data': [{}] * 100}, {'http': 403}])
        items, complete, http = inventory_governance.pages('a/b', '/branches', None, fetch=lambda *args: next(replies))
        self.assertEqual(len(items), 100)
        self.assertFalse(complete)
        self.assertEqual(http, 403)

    def test_missing_and_future_commit_dates_stay_unknown(self):
        now = datetime.datetime(2026, 1, 1, tzinfo=datetime.timezone.utc)
        self.assertIsNone(inventory_governance.commit_age({'http': 403}, now))
        self.assertIsNone(inventory_governance.commit_age({'http': 200, 'data': {'commit': {'committer': {'date': '2027-01-01T00:00:00Z'}}}}, now))

    def test_exact_scope_excludes_enterprise_controls(self):
        plans = json.loads((ROOT / 'docs/audit/free-controls.json').read_text())
        ids = [p['id'] for p in plans]
        self.assertEqual(len(ids), 48)
        self.assertEqual(len(set(ids)), 48)
        self.assertFalse(set(ids) & {'1.3.10', '1.3.11', '1.3.12'})

    def test_forbidden_protection_never_becomes_false_or_pass(self):
        row = audit_free_controls.protection_component({'http': 403, 'data': {'enforce_admins': {'enabled': True}}}, 'enforce_admins.enabled')
        self.assertEqual(row['configuration_result'], 'UNKNOWN')
        self.assertIsNone(row['value'])

    def test_available_counts_never_imply_control_pass(self):
        rows = audit_free_controls.build_rows([{'id': '1.2.5', 'sources': ['forks'], 'remaining': 'Review fork inventory'}],
                                              {'forks': {'available': True, 'count': 0}})
        self.assertEqual(rows[0]['overall_cis'], 'MANUAL_REVIEW')

    def test_owner_transfer_blocks_without_advancing_baseline(self):
        before = {'a/b': {'repository_id': 1, 'owner_id': 2}}
        after = {'a/b': {'repository_id': 1, 'owner_id': 3}}
        self.assertEqual(monitor_action_owners.compare(before, after)[0]['state'], 'REVIEW_REQUIRED')
        self.assertEqual(before['a/b']['owner_id'], 2)

    def test_removed_or_unknown_owner_is_not_green(self):
        before = {'a/b': {'repository_id': 1, 'owner_id': 2}}
        for after in ({}, {'a/b': None}, {'a/b': {'repository_id': 1, 'owner_id': None}}):
            self.assertEqual(monitor_action_owners.compare(before, after)[0]['state'], 'UNKNOWN')

    def test_added_action_needs_explicit_review(self):
        after = {'a/b': {'repository_id': 1, 'owner_id': 2}}
        self.assertEqual(monitor_action_owners.compare({}, after)[0]['state'], 'REVIEW_REQUIRED')


class BundleIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.original = Path(cls.temp.name) / 'original'
        project_bundle.generate(cls.original)
        cls.trusted = project_bundle.fingerprint(cls.original / 'public.pem')

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def copy(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        copied = Path(temp.name) / 'bundle'
        shutil.copytree(self.original, copied)
        return copied

    def test_original_and_missing_private_key(self):
        manifest = project_bundle.verify(self.original, self.trusted)
        self.assertEqual(set(manifest['sha256']), set(project_bundle.PAYLOADS))
        self.assertFalse(list(self.original.glob('*private*')))

    def test_payload_tampering_rejected(self):
        for name in project_bundle.PAYLOADS:
            copied = self.copy()
            with (copied / name).open('ab') as handle:
                handle.write(b'altered')
            with self.assertRaises(ValueError):
                project_bundle.verify(copied, self.trusted)

    def test_manifest_tampering_rejected(self):
        copied = self.copy()
        with (copied / 'manifest.json').open('ab') as handle:
            handle.write(b'altered')
        with self.assertRaises(subprocess.CalledProcessError):
            project_bundle.verify(copied, self.trusted)

    def test_wrong_trusted_key_rejected(self):
        with self.assertRaises(ValueError):
            project_bundle.verify(self.original, '0' * 64)


if __name__ == '__main__':
    unittest.main()
