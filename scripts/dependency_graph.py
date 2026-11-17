#!/usr/bin/env python3
"""Inventory installed scanner dependency metadata; preserve optional/marker qualifications."""
import argparse
import importlib.metadata
import json
from pathlib import Path
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

ROOT = Path(__file__).resolve().parents[1]


def graph(items, metadata):
    locked = {canonicalize_name(i['name']): i['version'] for i in items}
    nodes, edges, errors = [], [], []
    for name, expected in sorted(locked.items()):
        installed = metadata.get(name)
        if not installed or installed['version'] != expected:
            errors.append({'package': name, 'problem': 'Missing or mismatched installed version'})
            continue
        nodes.append({'name': name, 'version': expected})
        for raw in installed.get('requires', []):
            req = Requirement(raw)
            target = canonicalize_name(req.name)
            # Evaluate default environment without extras, but retain all declared edges.
            default_active = req.marker is None or req.marker.evaluate({'extra': ''})
            present = target in locked
            version_ok = present and (not req.specifier or req.specifier.contains(locked[target], prereleases=True))
            edges.append({'from': name, 'to': target, 'declared': raw, 'marker': str(req.marker) if req.marker else None,
                          'default_environment_active': default_active, 'target_in_lock': present,
                          'locked_version_satisfies': bool(version_ok),
                          'scope': 'Declared metadata edge; selected extras/actual resolver path not inferred'})
            if default_active and not version_ok:
                errors.append({'package': name, 'dependency': target, 'problem': 'Required dependency absent or version incompatible'})
    return {'scope': '32 locked Python scanner distributions only, current Python/platform default markers; optional declared edges retained, extras resolution not certified',
            'nodes': nodes, 'edges': edges, 'errors': errors, 'overall_cis': 'PARTIAL'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', default='reports/dependency-graph')
    args = p.parse_args()
    items = json.loads((ROOT / 'config/python-scanner-lock.json').read_text())['packages']
    metadata = {}
    for item in items:
        try:
            dist = importlib.metadata.distribution(item['name'])
        except importlib.metadata.PackageNotFoundError:
            continue
        metadata[canonicalize_name(item['name'])] = {'version': dist.version, 'requires': dist.requires or []}
    report = graph(items, metadata)
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    (out / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'nodes': len(report['nodes']), 'declared_edges': len(report['edges']), 'errors': len(report['errors'])}))
    return 2 if report['errors'] or len(report['nodes']) != len(items) else 0


if __name__ == '__main__':
    raise SystemExit(main())
