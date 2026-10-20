#!/usr/bin/env python3
# Fix PRD: update Rev. 163 status line
path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the second occurrence (Rev. 163 section)
old = 'Seluruh perubahan akan dicomit setelah revisi ini.'
new = 'Seluruh perubahan telah dicomit ke HEAD.'

# Find all occurrences
count = content.count(old)
print(f'Found {count} occurrences')

# Replace the second occurrence (index 1)
if count >= 2:
    # Find the position of the second occurrence
    first_pos = content.find(old)
    second_pos = content.find(old, first_pos + 1)
    print(f'First pos: {first_pos}, Second pos: {second_pos}')
    
    # Replace the second occurrence
    content = content[:second_pos] + new + content[second_pos + len(old):]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Updated successfully')
else:
    print(f'Expected 2 occurrences, found {count}')
