import importlib.util
import os
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT=Path(__file__).parents[1]

def load():
    spec=importlib.util.spec_from_file_location('config_under_test',ROOT/'database_config.py')
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class ConfigTests(unittest.TestCase):
    def test_missing_credentials_do_not_have_embedded_defaults(self):
        with patch.dict(os.environ,{},clear=True):
            config=load()
        self.assertIsNone(config.AWS_SECRET_ACCESS_KEY)
        self.assertIsNone(config.GITHUB_PAT_TOKEN)
        self.assertEqual(config.DB_PORT,5432)

    def test_only_environment_supplies_credentials(self):
        with patch.dict(os.environ,{'AWS_SECRET_ACCESS_KEY':'unit-fixture','GITHUB_PAT_TOKEN':'unit-fixture','DB_PORT':'6000'},clear=True):
            config=load()
        self.assertEqual(config.DB_PORT,6000)
        self.assertEqual(config.AWS_SECRET_ACCESS_KEY,'unit-fixture')

    def test_invalid_port_is_rejected(self):
        for value in ['0','65536','not-an-integer']:
            with self.subTest(value=value),patch.dict(os.environ,{'DB_PORT':value},clear=True):
                with self.assertRaises(ValueError):load()

if __name__=='__main__':unittest.main()
