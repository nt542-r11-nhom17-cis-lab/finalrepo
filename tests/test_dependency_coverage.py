import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).parents[1]/'scripts'))
from verify_dependency_coverage import verify

class CoverageTests(unittest.TestCase):
    expected=[{'name':'pip','version':'1'},{'name':'packaging','version':'2'}]

    def test_missing_bootstrap_packages_are_rejected(self):
        with self.assertRaises(ValueError):verify(self.expected,{'dependencies':[]})

    def test_normalized_exact_packages_are_accepted(self):
        result=verify([{'name':'example_package','version':'1'}],{'dependencies':[{'name':'example-package','version':'1','vulns':[]}]})
        self.assertEqual(result['coverage'],'EXACT')

    def test_changed_version_is_rejected(self):
        with self.assertRaises(ValueError):verify([{'name':'pip','version':'1'}],{'dependencies':[{'name':'pip','version':'2','vulns':[]}]})

    def test_skipped_package_and_vulnerability_are_rejected(self):
        for payload in [{'name':'pip','version':'1','skip_reason':'unavailable'}, {'name':'pip','version':'1','vulns':[{'id':'test-advisory'}]}]:
            with self.subTest(payload=payload),self.assertRaises(ValueError):verify([{'name':'pip','version':'1'}],{'dependencies':[payload]})

if __name__=='__main__':unittest.main()
