#!/usr/bin/env python3
"""Fix header: change 'Verifikasi Rev. 66' to 'Verifikasi Rev. 67' anywhere."""
PATH = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(PATH, 'r', encoding='utf-8') as f:
    content = f.read()

old = 'Verifikasi Rev. 66'
new = 'Verifikasi Rev. 67'
count = content.count(old)
content = content.replace(old, new, 1)
print(f'Revised: {count} occurrence(s) found, 1 replaced')

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print('Total size:', len(content), 'bytes')
