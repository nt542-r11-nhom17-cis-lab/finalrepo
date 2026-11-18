#!/usr/bin/env python3
"""Inventory selected pinned third-party inputs and explicitly record absent supplier SBOMs."""
import argparse
import json
from pathlib import Path
import audit_dependencies

ROOT = Path(__file__).resolve().parents[1]


def inventory():
    rows = []
    for item in json.loads((ROOT / 'config/python-scanner-lock.json').read_text())['packages']:
        rows.append({'ecosystem': 'pypi', 'name': item['name'], 'version': item['version'],
                     'artifact_sha256': item['sha256'], 'supplier_sbom': 'MISSING'})
    unique = set()
    for path in sorted((ROOT / '.github/workflows').glob('*')):
        if path.suffix in ('.yml', '.yaml'):
            for item in audit_dependencies.parse_action_uses(path.read_text()):
                key = item['repository'], item['ref']
                if key not in unique:
                    unique.add(key)
                    rows.append({'ecosystem': 'githubactions', 'name': key[0], 'version': key[1],
                                 'artifact_sha256': None, 'supplier_sbom': 'MISSING'})
    for filename, ecosystem in [('container-image.json', 'oci'), ('registry-integration.lock.json', 'native-go')]:
        data = json.loads((ROOT / 'config' / filename).read_text())
        rows.append({'ecosystem': ecosystem, 'name': data.get('repository', 'distribution/distribution'),
                     'version': data.get('tag', data.get('version')),
                     'artifact_sha256': data.get('binary_sha256', data.get('digest')),
                     'supplier_sbom': 'MISSING'})
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('reports/supplier-intake/results.json'))
    args = parser.parse_args()
    rows = inventory()
    report = {'scope': 'Selected pinned direct inputs only; not a complete transitive supplier inventory',
              'inputs': rows, 'supplier_sboms_verified': 0, 'missing_supplier_sboms': len(rows),
              'overall_cis': 'MANUAL_REVIEW',
              'limits': ['GitHub dependency export and locally generated SBOM are not supplier-issued evidence',
                         'Upstream Distribution release offers provenance but no named SBOM asset; custom build differs',
                         'Metadata/checksum/source availability does not establish supplier SBOM authenticity',
                         'Owner must approve supplier intake requirement and handle missing evidence explicitly']}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'inputs': len(rows), 'missing_supplier_sboms': len(rows), 'compliance_pass': 0}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
