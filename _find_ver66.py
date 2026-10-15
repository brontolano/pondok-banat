#!/usr/bin/env python3
"""Find exact pattern in header line."""
PATH = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# Find "Verifikasi Rev. 66" 
idx = content.find('Verifikasi Rev. 66')
if idx != -1:
    print(f'Found at position {idx}')
    print('Context:')
    print(repr(content[idx:idx+50]))
else:
    print('Not found')

# Count all occurrences
count = content.count('Verifikasi Rev. 66')
print(f'Count of "Verifikasi Rev. 66": {count}')

# Also check the header line
header = content[:500]
print('--- HEADER FIRST 500 chars ---')
print(repr(header))
