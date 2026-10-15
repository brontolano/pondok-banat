#!/usr/bin/env python3
"""Fix remaining 'Verifikasi Rev. 66' in header to 'Verifikasi Rev. 67'."""
PATH = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(PATH, 'r', encoding='utf-8') as f:
    content = f.read()

old = 'Verifikasi Rev. 66)**'
new = 'Verifikasi Rev. 67)**'
content, count = content.replace(old, new, 1)
print(f'Revised: {count} replaced')

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print('Total size:', len(content), 'bytes')
