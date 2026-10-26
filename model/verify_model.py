#!/usr/bin/env python3
"""Check the copied URDF, every referenced mesh, and the source manifest."""
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET


def main():
    root = Path(__file__).resolve().parent / 'esrobo_waist_with_head'
    manifest = json.loads((root / 'SOURCE.json').read_text())
    for item in [manifest['urdf'], *manifest['files']]:
        path = root / item['path']
        data = path.read_bytes()
        if len(data) != item['size'] or hashlib.sha256(data).hexdigest() != item['sha256']:
            raise ValueError(f"model file differs or LFS content missing: {path}")
    model = ET.parse(root / manifest['urdf']['path']).getroot()
    prefix = 'package://esrobo_waist_with_head/'
    listed = {x['path'] for x in manifest['files']}
    refs = {x.get('filename') for x in model.findall('.//mesh')}
    for name in refs:
        if not name.startswith(prefix) or name[len(prefix):] not in listed:
            raise ValueError(f'unresolved model resource: {name}')
    links = [x.get('name') for x in model.findall('link')]
    joints = model.findall('joint')
    if len(set(links)) != len(links) or len({x.get('name') for x in joints}) != len(joints):
        raise ValueError('duplicate link or joint')
    for joint in joints:
        if any(joint.find(x).get('link') not in links for x in ('parent', 'child')):
            raise ValueError('joint references an unknown link')
    print(f"Verified {len(links)} links, {len(joints)} joints, {len(refs)} mesh resources")


if __name__ == '__main__':
    main()
