import importlib.util
import json
from pathlib import Path
import subprocess
import unittest

ROOT=Path(__file__).parents[1]
import sys
sys.path.insert(0,str(ROOT/'scripts'))
import audit_all

class AllControlsTests(unittest.TestCase):
    def test_exact_catalog_coverage(self):
        catalog=json.loads((ROOT/'docs/audit/catalog.json').read_text())
        plans=json.loads((ROOT/'docs/audit/control-plans.json').read_text())
        self.assertEqual(len(plans),120)
        self.assertEqual(len({x['id'] for x in plans}),120)
        self.assertEqual({x['id'] for x in catalog},{x['id'] for x in plans})
        for item in plans:
            for key in ['audit','remediation','re_audit','evidence_sources']:
                self.assertTrue(item[key],(item['id'],key))

    def test_missing_registry_never_passes(self):
        result=audit_all.classify({'registry':{'available':False}},['registry'])
        self.assertEqual(result['execution'],'BLOCKED_PREREQUISITE')
        self.assertEqual(result['compliance'],'MANUAL_REVIEW')

    def test_available_evidence_does_not_imply_compliance(self):
        result=audit_all.classify({'repository_files':{'available':True}},['repository_files'])
        self.assertEqual(result['execution'],'EVIDENCE_COLLECTED')
        self.assertNotEqual(result['compliance'],'PASS')

    def test_local_push_guard(self):
        hook=ROOT/'.githooks/pre-push'
        def push(ref,remote='https://github.com/nt542-r11-nhom17-cis-lab/finalrepo.git'):
            return subprocess.run(['sh',str(hook),'origin',remote],input=f'refs/heads/audit/test {"1"*40} {ref} {"0"*40}\n',text=True,capture_output=True).returncode
        self.assertNotEqual(push('refs/heads/main'),0)
        self.assertEqual(push('refs/heads/audit/test'),0)
        self.assertNotEqual(push('refs/heads/audit/test','https://github.com/dtk01062006/cis-github-actions-lab.git'),0)

if __name__=='__main__':unittest.main()
