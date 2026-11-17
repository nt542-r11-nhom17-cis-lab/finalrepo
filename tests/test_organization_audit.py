import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).parents[1]/'scripts'))
import audit_organization

class OrganizationTests(unittest.TestCase):
    def row(self,data,cid,http=200):
        return next(r for r in audit_organization.evaluate(data,http) if r['cis_id']==cid)

    def test_hidden_mfa_field_is_unknown(self):
        self.assertEqual(self.row({},'1.3.5')['configuration_result'],'UNKNOWN')
        self.assertEqual(self.row({'two_factor_requirement_enabled':None},'1.3.5')['configuration_result'],'UNKNOWN')

    def test_mfa_disabled_is_a_configuration_finding(self):
        self.assertEqual(self.row({'two_factor_requirement_enabled':False},'1.3.5')['configuration_result'],'FAIL')

    def test_string_is_not_boolean_policy_evidence(self):
        self.assertEqual(self.row({'two_factor_requirement_enabled':'true'},'1.3.5')['configuration_result'],'UNKNOWN')

    def test_null_permission_is_not_string_none(self):
        self.assertEqual(self.row({'default_repository_permission':None},'1.3.8')['configuration_result'],'UNKNOWN')
        self.assertEqual(self.row({'default_repository_permission':'none'},'1.3.8')['configuration_result'],'PASS')

    def test_component_pass_is_not_full_control_pass(self):
        self.assertEqual(self.row({'two_factor_requirement_enabled':True},'1.3.5')['overall_status'],'MANUAL_REVIEW')

    def test_access_error_never_becomes_policy_pass(self):
        self.assertEqual(self.row({'two_factor_requirement_enabled':True},'1.3.5',403)['configuration_result'],'UNKNOWN')

if __name__=='__main__':unittest.main()
