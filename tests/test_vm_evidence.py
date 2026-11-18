import io
import json
from pathlib import Path
import sys
import tarfile
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from import_vm_evidence import EXPECTED, review_archive


class VmEvidenceTests(unittest.TestCase):
    def archive(self, directory, mutate=None, extra=None):
        path = Path(directory) / 'reports.tar.gz'
        with tarfile.open(path, 'w:gz') as archive:
            for name, (key, result, count) in EXPECTED.items():
                label = 'test' if key == 'tests' else 'check'
                data = {'scope': 'Lab only', key: [{label: f'check {i}', result: 'PASS'} for i in range(count)]}
                if mutate:
                    mutate(name, data, key, result)
                raw = json.dumps(data).encode()
                info = tarfile.TarInfo(name)
                info.size = len(raw)
                archive.addfile(info, io.BytesIO(raw))
            if extra:
                archive.addfile(extra, io.BytesIO(b''))
        return path

    def test_complete_evidence_is_partial_and_not_execution_attestation(self):
        with tempfile.TemporaryDirectory() as directory:
            report = review_archive(self.archive(directory))
        self.assertEqual((report['passed'], report['total']), (29, 29))
        self.assertEqual(report['overall_cis'], 'PARTIAL')
        self.assertIn('no authenticated', report['source'])

    def test_failed_check_is_preserved(self):
        def fail(name, data, key, result):
            if name.startswith('supply-chain'):
                data[key][0][result] = 'FAIL'
        with tempfile.TemporaryDirectory() as directory:
            report = review_archive(self.archive(directory, mutate=fail))
        self.assertEqual(report['passed'], 28)

    def test_traversal_symlink_duplicate_and_oversize_are_rejected(self):
        for name, kind in [('../escape', 'path'), ('supply-chain/results.json', 'duplicate'),
                           ('supply-chain/results.json', 'symlink'), ('huge.json', 'oversize')]:
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as directory:
                info = tarfile.TarInfo(name)
                if kind == 'symlink':
                    info.type = tarfile.SYMTYPE
                    info.linkname = '/etc/passwd'
                if kind == 'oversize':
                    # Use a separate all-invalid archive to test the size guard.
                    info.name = 'supply-chain/results.json'
                    info.size = 100001
                    path = Path(directory) / 'large.tar.gz'
                    with tarfile.open(path, 'w:gz') as archive:
                        archive.addfile(info, io.BytesIO(b' ' * info.size))
                else:
                    path = self.archive(directory, extra=info)
                with self.assertRaises(ValueError):
                    review_archive(path)

    def test_missing_report_and_unknown_result_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            empty = Path(directory) / 'empty.tar.gz'
            with tarfile.open(empty, 'w:gz'):
                pass
            with self.assertRaises(ValueError):
                review_archive(empty)
            def unknown(name, data, key, result):
                data[key][0][result] = 'UNKNOWN'
            with self.assertRaises(ValueError):
                review_archive(self.archive(directory, mutate=unknown))
