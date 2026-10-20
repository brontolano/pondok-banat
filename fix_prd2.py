#!/usr/bin/env python3
# Fix PRD: update Rev. 163 status line
path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = 'Seluruh perubahan akan dicomit setelah revisi ini.'
new = 'Seluruh perubahan telah dicomit ke HEAD.'

if old in content:
    content = content.replace(old, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Replaced successfully')
else:
    # Find similar strings
    import re
    for m in re.finditer(r'Seluruh perubahan[^.]*\.', content):
        print('Found:', repr(m.group()))
    print('Not found')
