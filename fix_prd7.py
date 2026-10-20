#!/usr/bin/env python3
# Fix PRD: replace string at L2516
path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find and replace the line with "Seluruh perubahan akan dicomit setelah revisi ini."
for i, line in enumerate(lines):
    if 'Seluruh perubahan akan dicomit setelah revisi ini' in line:
        # This is the Rev. 163 status line (line 2516)
        # Check if previous line mentions "rev 163"
        if 'rev 163' in lines[i-1] or (i > 0 and 'rev 163' in lines[i-1]):
            print(f'Found at line {i+1}')
            lines[i] = line.replace(
                'Seluruh perubahan akan dicomit setelah revisi ini.',
                'Seluruh perubahan telah dicomit ke HEAD.'
            )
            print(f'Replaced: {lines[i].strip()}')
            break

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('Done')
