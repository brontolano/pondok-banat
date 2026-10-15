#!/usr/bin/env python3
"""Fix PRD: keep only first Section 26, remove duplicates."""
PATH = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(PATH, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f'Total lines: {len(lines)}')

# Find all Section 26 markers
markers = []
for i, line in enumerate(lines):
    if line.startswith('## 26. REVISI TERBARU'):
        markers.append(i)
print(f'Section 26 markers at lines: {markers}')

if len(markers) < 2:
    print('No duplicates found')
else:
    # Keep everything up to and including the first Section 26
    # The first Section 26 ends at the line before the second Section 26
    first_section_end = markers[1]  # line index of second Section 26
    # Keep lines[0:first_section_end] (everything before second Section 26)
    new_lines = lines[:first_section_end]
    # Ensure trailing newline
    if new_lines and not new_lines[-1].endswith('\n'):
        new_lines[-1] += '\n'
    
    with open(PATH, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f'Fixed: kept {len(new_lines)} lines (removed {len(lines) - len(new_lines)} lines)')
