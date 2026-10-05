#!/usr/bin/env python3
"""Check an explicit release file inventory, local links and package structure."""
import json
import re
import struct
import zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
IGNORE={'.git','__pycache__','dist','.DS_Store'}
README_IMAGES={
    'assets/readme/your-personal-information.png',
    'assets/readme/how-it-works.png',
    'assets/readme/privacy-boundary.png',
    'assets/readme/what-can-i-ask.png',
    'assets/readme/personal-intelligence-anywhere.png',
}

def check_png(data):
    if len(data)>2_000_000 or data[:8]!=b'\x89PNG\r\n\x1a\n':raise ValueError('invalid README PNG')
    offset=8;first=True;seen_data=False
    while offset<len(data):
        if offset+12>len(data):raise ValueError('invalid README PNG')
        size=struct.unpack('>I',data[offset:offset+4])[0];end=offset+12+size
        if end>len(data):raise ValueError('invalid README PNG')
        kind=data[offset+4:offset+8];payload=data[offset+8:offset+8+size]
        crc=struct.unpack('>I',data[offset+8+size:end])[0]
        if zlib.crc32(kind+payload)!=crc:raise ValueError('invalid README PNG')
        if first:
            if kind!=b'IHDR' or size!=13:raise ValueError('invalid README PNG')
            width,height=struct.unpack('>II',payload[:8])
            if not (0<width<=8192 and 0<height<=8192):raise ValueError('invalid README PNG')
            first=False
        elif kind==b'IHDR':raise ValueError('invalid README PNG')
        if kind==b'IDAT':seen_data=True
        if kind==b'IEND':
            if size or end!=len(data) or not seen_data:raise ValueError('invalid README PNG')
            return
        offset=end
    raise ValueError('invalid README PNG')
PATTERNS=[r'/Users/[A-Za-z0-9._-]+/',r'/home/[A-Za-z0-9._-]+/',r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',r'\bgh[pousr]_[A-Za-z0-9]{20,}',r'\bsk-[A-Za-z0-9_-]{24,}']

def check(root=ROOT):
    inventory=json.loads((root/'release-files.json').read_text())
    wanted=set(inventory['files'])
    if len(wanted)!=len(inventory['files']):raise ValueError('duplicate release entry')
    actual=set()
    for p in root.rglob('*'):
        rel=p.relative_to(root)
        if any(part in IGNORE for part in rel.parts) or '_prev' in p.name:continue
        if p.is_symlink():raise ValueError('symlink in release')
        if p.is_dir():continue
        if p.suffix=='.pyc':continue
        actual.add(rel.as_posix())
    if actual!=wanted:raise ValueError('release inventory mismatch')
    for rel in sorted(wanted):
        p=root/rel
        if rel in README_IMAGES:
            data=p.read_bytes();check_png(data)
            if any(re.search(pattern,data.decode('utf-8',errors='ignore')) for pattern in PATTERNS):raise ValueError('private path or credential-like material detected')
            continue
        if p.suffix not in {'.md','.json','.py','.yml'} and p.name not in {'LICENSE','.gitignore'}:raise ValueError('unapproved file type')
        if p.stat().st_size>300_000:raise ValueError('unexpectedly large release file')
        content=p.read_text()
        if any(re.search(pattern,content) for pattern in PATTERNS):raise ValueError('private path or credential-like material detected')
        if p.suffix=='.json':json.loads(content)
        if p.suffix=='.md':
            for link in re.findall(r'\[[^\]]*\]\(([^\s)]+)\)',content):
                if re.match(r'[a-z]+://',link) or link.startswith('#'):continue
                target=(p.parent/link.split('#')[0]).resolve()
                if not target.is_relative_to(root.resolve()) or not target.exists():raise ValueError('missing or external local reference')
    plugin=root/'plugins/personal-intelligence'
    manifest=json.loads((plugin/'plugin.json').read_text())
    if manifest.get('name')!='personal-intelligence' or manifest.get('version')!='0.1.0':raise ValueError('manifest identity/version')
    if set(manifest)!={'$schema','name','version','description'}:raise ValueError('unexpected bundled capability')
    for name in ['setup-personal-intelligence','personal-intelligence']:
        skill=plugin/'skills'/name/'SKILL.md';content=skill.read_text()
        if not content.startswith('---\nname: '+name+'\ndescription: ') or '\n---\n' not in content:raise ValueError('skill metadata')
        if '[TODO:' in content:raise ValueError('unfinished skill scaffold')
    marketplace=json.loads((root/'.agents/plugins/marketplace.json').read_text())
    if marketplace['plugins'][0]['source']!={'source':'local','path':'./plugins/personal-intelligence'}:raise ValueError('marketplace path')
    return {'status':'PASS','files':len(wanted),'skills':2,'readme_images':len(wanted & README_IMAGES),'bundled_servers':0,'scope':'release_inventory_structure_and_heuristic_content_scan'}

if __name__=='__main__':
    try:print(json.dumps(check(),indent=2))
    except (ValueError,OSError,KeyError) as e:
        print(json.dumps({'status':'FAIL','reason':str(e)}));raise SystemExit(1)
