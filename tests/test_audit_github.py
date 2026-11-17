import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('audit', Path(__file__).parents[1] / 'scripts/audit_github.py')
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

class AuditTests(unittest.TestCase):
    def test_access_failure_is_not_noncompliance(self):
        rows = audit.evaluate({'http': 403}, {'http': 404}, {'http': 200, 'data': []})
        self.assertTrue(all(r['overall_status'] == 'ERROR' for r in rows))

    def test_rulesets_without_classic_protection_require_review(self):
        rows = audit.evaluate({'http': 200}, {'http': 404}, {'http': 200, 'data': [{'type': 'pull_request'}]})
        self.assertTrue(all(r['overall_status'] == 'MANUAL_REVIEW' for r in rows))
        self.assertFalse(any(r['configuration_result'] == 'FAIL' for r in rows))

    def test_missing_denial_fields_are_unknown(self):
        rows = audit.evaluate({'http': 200}, {'http': 200, 'data': {}}, {'http': 200, 'data': []})
        by_id = {r['cis_id']: r for r in rows}
        self.assertEqual(by_id['1.1.16']['configuration_result'], 'UNKNOWN')
        self.assertEqual(by_id['1.1.17']['configuration_result'], 'UNKNOWN')

    def test_insufficient_approvals_is_configuration_failure(self):
        rows = audit.evaluate({'http': 200}, {'http': 200, 'data': {'required_pull_request_reviews': {'required_approving_review_count': 1}}}, {'http': 200, 'data': []})
        self.assertEqual(rows[0]['configuration_result'], 'FAIL')

if __name__ == '__main__':
    unittest.main()
