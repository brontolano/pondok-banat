#!/usr/bin/env python3
# Fix PRD: replace string at specific position (L2516)
path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the line with "Seluruh perubahan akan dicomit setelah revisi ini."
# This is the Rev. 163 status line at L2516
for i, line in enumerate(lines):
    if 'Seluruh perubahan akan dicomit setelah revisi ini' in line and 'rev 163' in lines[i-1]:
        print(f'Found at line {i+1}: {line.strip()}')
        # Replace the string
        lines[i] = line.replace(
            'Seluruh perubahan akan dicomit setelah revisi ini.',
            'Seluruh perubahan telah dicomit ke HEAD.'
        )
        print(f'Replaced: {lines[i].strip()}')
        break

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('Done')
