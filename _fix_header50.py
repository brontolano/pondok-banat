#!/usr/bin/env python3
path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = '**Build quality gate (Verifikasi Rev. 49)**'
new = '**Build quality gate (Verifikasi Rev. 50)**'

if old in content:
    content = content.replace(old, new, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed: Verifikasi Rev. 49 -> Rev. 50 in header")
else:
    print("NOT FOUND: 'Build quality gate (Verifikasi Rev. 49)'")
    # Show context around 'Verifikasi Rev'
    import re
    for m in re.finditer(r'Verifika.{0,50}', content):
        print(repr(m.group(0)))
