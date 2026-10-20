#!/usr/bin/env python3
# Fix PRD: update Rev. 163 status line with flexible pattern
path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Use regex to find and replace the status line
import re

# Pattern: match "Seluruh perubahan [anything] revisi ini." at the end of the status line
pattern = r'(Seluruh perubahan[^.]*?revisi ini\.)'
replacement = r'Seluruh perubahan telah dicomit ke HEAD.'

# Check if the pattern exists
matches = list(re.finditer(pattern, content))
print(f'Found {len(matches)} matches')

for i, m in enumerate(matches):
    print(f'Match {i}: {repr(m.group())}')

if matches:
    content = re.sub(pattern, replacement, content, count=1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Updated successfully')
else:
    print('No match found')
