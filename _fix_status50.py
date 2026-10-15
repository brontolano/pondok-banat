#!/usr/bin/env python3
path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = '**Status:** dokumen PRD **REVISI** — rev 49 = verifikasi fresh ulang; seluruh data stabil; tidak ada perubahan signifikan dari Rev. 48.'
new = '**Status:** dokumen PRD **REVISI** — rev 50 = verifikasi fresh ulang; seluruh data stabil; tidak ada perubahan signifikan dari Rev. 49.'

if old in content:
    content = content.replace(old, new, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed Status field to Rev. 50")
else:
    print("NOT FOUND - searching for Status field...")
    import re
    for m in re.finditer(r'\*\*Status:\*\* dokumen PRD \*\*REVISI\*\*.*?\.', content):
        print(repr(m.group(0)))
