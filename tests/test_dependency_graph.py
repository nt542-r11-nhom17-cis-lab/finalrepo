import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
try:
    import dependency_graph
except ModuleNotFoundError as error:
    if error.name != 'packaging':
        raise
    dependency_graph = None


@unittest.skipIf(dependency_graph is None, 'Run with hashed scanner environment for graph tests')
class DependencyGraphTests(unittest.TestCase):
    def test_mandatory_missing_dependency_is_error(self):
        result = dependency_graph.graph([{'name': 'a', 'version': '1'}], {'a': {'version': '1', 'requires': ['b>=2']}})
        self.assertTrue(result['errors'])

    def test_optional_dependency_is_retained_without_false_missing_error(self):
        result = dependency_graph.graph([{'name': 'a', 'version': '1'}], {'a': {'version': '1', 'requires': ['b; extra == "test"']}})
        self.assertFalse(result['errors'])
        self.assertFalse(result['edges'][0]['default_environment_active'])
        self.assertFalse(result['edges'][0]['target_in_lock'])

    def test_wrong_installed_version_is_error(self):
        result = dependency_graph.graph([{'name': 'a', 'version': '1'}], {'a': {'version': '2', 'requires': []}})
        self.assertTrue(result['errors'])

    def test_incompatible_locked_version_is_error(self):
        result = dependency_graph.graph([{'name': 'a', 'version': '1'}, {'name': 'b', 'version': '1'}],
                                        {'a': {'version': '1', 'requires': ['b>=2']}, 'b': {'version': '1'}})
        self.assertTrue(result['errors'])


if __name__ == '__main__':
    unittest.main()
