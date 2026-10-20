#!/usr/bin/env python3
# Fix PRD: replace string at L2516 - simple approach
path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all occurrences of the string
old = 'Seluruh perubahan akan dicomit setelah revisi ini.'
new = 'Seluruh perubahan telah dicomit ke HEAD.'

count = content.count(old)
print(f'Found {count} occurrences')

content = content.replace(old, new)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Done')
