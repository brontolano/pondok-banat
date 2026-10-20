#!/usr/bin/env python3
# Fix PRD: replace the status line at L2516
# Use regex to match both "dicomit" and "dicommit" spellings
import re

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern: "Seluruh perubahan" followed by any characters, then "revisi ini."
# This matches the string regardless of the spelling of "dicomit"
pattern = r'Seluruh perubahan[^.]*?revisi ini\.'

replacement = 'Seluruh perubahan telah dicomit ke HEAD.'

matches = list(re.finditer(pattern, content))
print(f'Found {len(matches)} matches')
for i, m in enumerate(matches):
    print(f'Match {i}: {m.group()!r}')

if matches:
    # Replace the match at L2516 (the second match)
    # The first match is at L2486 (Rev. 161), the second is at L2516 (Rev. 163)
    content = re.sub(pattern, replacement, content, count=2)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Updated successfully')
else:
    print('No match found')
