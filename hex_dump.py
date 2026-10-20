#!/usr/bin/env python3
# Print hex dump of the string in the file
path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the string
idx = content.find('Seluruh perubahan')
if idx != -1:
    print(f'Found at index {idx}')
    print(f'Context: {content[idx:idx+80]!r}')
    print(f'Hex: {content[idx:idx+80].encode("utf-8").hex()}')
else:
    print('Not found')
    
    # Search for similar strings
    import re
    for m in re.finditer(r'Seluruh.*?revisi ini', content):
        print(f'Found: {m.group()!r}')
        print(f'Hex: {m.group().encode("utf-8").hex()}')
