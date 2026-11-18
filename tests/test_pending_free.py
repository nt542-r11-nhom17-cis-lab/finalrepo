import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import audit_pending_free
import build_access_guard
import code_change_monitor
import deployment_preflight
import supplier_intake


class PendingFreeTests(unittest.TestCase):
    def context(self):
        return {'GITHUB_ACTIONS': 'true', 'GITHUB_REPOSITORY': 'nt542-r11-nhom17-cis-lab/finalrepo',
                'GITHUB_REPOSITORY_ID': '1461201903', 'GITHUB_REF': 'refs/heads/audit/remaining-free-integration',
                'GITHUB_EVENT_NAME': 'push', 'GITHUB_ACTOR': 'hieune-ui', 'GITHUB_ACTOR_ID': '357749923',
                'GITHUB_TRIGGERING_ACTOR': 'hieune-ui'}

    def policy(self):
        return json.loads((ROOT / 'config/build-access.json').read_text())

    def test_authorized_platform_context_is_accepted_as_component_only(self):
        report = build_access_guard.evaluate(self.context(), self.policy())
        self.assertTrue(report['execution_allowed'])
        self.assertEqual(report['overall_cis'], 'PARTIAL')

    def test_main_fork_read_actor_impersonation_and_unauthorized_rerun_rejected(self):
        for field, value in [('GITHUB_REF', 'refs/heads/main'), ('GITHUB_REPOSITORY_ID', '7'),
                             ('GITHUB_REPOSITORY', 'someone/finalrepo'), ('GITHUB_EVENT_NAME', 'pull_request_target'),
                             ('GITHUB_ACTOR', 'dtk0106'), ('GITHUB_ACTOR_ID', '1'),
                             ('GITHUB_TRIGGERING_ACTOR', 'dtk0106'), ('GITHUB_ACTIONS', 'false')]:
            with self.subTest(field=field):
                context = self.context()
                context[field] = value
                self.assertFalse(build_access_guard.evaluate(context, self.policy())['execution_allowed'])

    def test_missing_platform_context_is_denied(self):
        self.assertFalse(build_access_guard.evaluate({}, self.policy())['execution_allowed'])

    def test_cli_denial_has_nonzero_exit_and_does_not_export_environment(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'report.json'
            process = subprocess.run([sys.executable, str(ROOT / 'scripts/build_access_guard.py'), '--output', str(output)],
                                     env={'UNRELATED_SECRET': 'private-fixture-value'}, capture_output=True, text=True)
            self.assertEqual(process.returncode, 2)
            self.assertNotIn('private-fixture-value', output.read_text() + process.stdout + process.stderr)

    def test_unreadable_policy_is_unknown_not_absent(self):
        for status in (403, 404, None):
            self.assertEqual(audit_pending_free.policy_snapshot({'http': status})['state'], 'UNKNOWN')
        self.assertEqual(audit_pending_free.policy_snapshot({'http': 200, 'data': None})['state'], 'UNKNOWN')

    def test_policy_digest_ignores_key_order_and_detects_change(self):
        a = audit_pending_free.policy_snapshot({'http': 200, 'data': {'a': 1, 'b': 2}})
        b = audit_pending_free.policy_snapshot({'http': 200, 'data': {'b': 2, 'a': 1}})
        c = audit_pending_free.policy_snapshot({'http': 200, 'data': {'b': 2, 'a': 3}})
        self.assertEqual(audit_pending_free.compare_policy(a, b), 'UNCHANGED')
        self.assertEqual(audit_pending_free.compare_policy(a, c), 'CHANGED_REVIEW_REQUIRED')
        self.assertEqual(audit_pending_free.compare_policy(a, {'digest': None}), 'UNKNOWN')

    def test_partial_pagination_does_not_claim_member_total(self):
        self.assertIsNone(audit_pending_free.observed_count([{}], {'http': 200, 'pagination_complete': False}))
        self.assertIsNone(audit_pending_free.observed_count([], {'http': 403, 'pagination_complete': False}))
        self.assertEqual(audit_pending_free.observed_count([], {'http': 200, 'pagination_complete': True}), 0)

    def test_monitor_detects_selected_dangerous_workflow_patterns(self):
        for text in ['on:\n  pull_request_target:\n', 'permissions: write-all\n', 'persist-credentials: true # risky\n']:
            self.assertTrue(code_change_monitor.inspect_workflow(text))

    def test_monitor_does_not_treat_comments_or_read_only_permissions_as_findings(self):
        self.assertEqual(code_change_monitor.inspect_workflow('# permissions: write-all\npermissions:\n  contents: read\n'), [])

    def test_monitor_preserves_unusual_paths_without_shell_execution(self):
        paths = code_change_monitor.changed_paths('a'*40, 'b'*40, lambda *args: 'scripts/odd\nname.py\0config/x\0')
        self.assertEqual(paths, ['scripts/odd\nname.py', 'config/x'])

    def test_unreadable_sshd_configuration_is_unknown(self):
        response = subprocess.CompletedProcess([], 1, stdout='', stderr='private error detail')
        report = deployment_preflight.ssh_settings(run=lambda *a, **k: response, executable='/fake/sshd')
        self.assertEqual(set(report['settings'].values()), {'UNKNOWN'})
        self.assertNotIn('private error detail', json.dumps(report))

    def test_sshd_exports_only_selected_settings(self):
        response = subprocess.CompletedProcess([], 0, stdout='permitrootlogin no\npasswordauthentication no\nhostkey /private/path\n', stderr='')
        report = deployment_preflight.ssh_settings(run=lambda *a, **k: response, executable='/fake/sshd')
        self.assertEqual(report['settings']['permitrootlogin'], 'no')
        self.assertNotIn('/private/path', json.dumps(report))

    def test_supplier_inventory_keeps_missing_sbom_explicit(self):
        rows = supplier_intake.inventory()
        self.assertGreaterEqual(len(rows), 43)
        self.assertTrue(all(row['supplier_sbom'] == 'MISSING' for row in rows))
        self.assertEqual(sum(row['ecosystem'] == 'pypi' for row in rows), 32)
        self.assertEqual(sum(row['ecosystem'] == 'githubactions' for row in rows), 9)
