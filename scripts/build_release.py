#!/usr/bin/env python3
"""Build the exact reviewed generic inventory; never package a private workspace."""
import argparse
import hashlib
import json
import zipfile
from pathlib import Path
from check_release import check,ROOT

def build(destination):
    check()
    destination=Path(destination).resolve()
    if destination.is_relative_to(ROOT):raise ValueError('archive destination must be outside source repository')
    destination.mkdir(parents=True,exist_ok=True)
    inventory=json.loads((ROOT/'release-files.json').read_text())['files']
    groups={'personal-intelligence-v0.1.0-repository.zip':[(rel,'personal-intelligence/'+rel) for rel in inventory],
            'personal-intelligence-v0.1.0-plugin.zip':[(rel,'personal-intelligence/'+rel.removeprefix('plugins/personal-intelligence/')) for rel in inventory if rel.startswith('plugins/personal-intelligence/')]}
    groups['personal-intelligence-v0.1.0-plugin.zip'].append(('LICENSE','personal-intelligence/LICENSE'))
    # Refuse collisions before writing either archive or its checksum file.
    outputs=[destination/name for name in groups]+[destination/'SHA256SUMS.txt']
    if any(target.exists() for target in outputs):raise ValueError('existing release output; preserve before replacing')
    for name,entries in groups.items():
        target=destination/name
        if target.exists():raise ValueError('existing release archive; preserve before replacing')
        with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED) as archive:
            for rel,member in sorted(entries):
                info=zipfile.ZipInfo(member,date_time=(2026,10,6,0,0,0))
                info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
                archive.writestr(info,(ROOT/rel).read_bytes())
    checksum=destination/'SHA256SUMS.txt'
    if checksum.exists():raise ValueError('existing checksum file')
    checksum.write_text(''.join(hashlib.sha256((destination/name).read_bytes()).hexdigest()+'  '+name+'\n' for name in sorted(groups)))
    return {'status':'BUILT','archives':sorted(groups),'checksums':'SHA256SUMS.txt'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--destination',required=True)
    try:print(json.dumps(build(p.parse_args().destination),indent=2))
    except (ValueError,OSError) as e:print(json.dumps({'status':'FAIL','reason':str(e)}));raise SystemExit(1)
