#!/usr/bin/env python3
# Update PRD: fix Rev. 163 status line + add Rev. 164 section
path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    # Fix Rev. 163 status line
    if '3. **Status:** dokumen PRD **REVISI** — rev 163' in line:
        line = line.replace(
            'Seluruh perubahan akan dicomit setelah revisi ini.',
            'Seluruh perubahan telah dicomit ke HEAD.'
        )
    new_lines.append(line)

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('Updated Rev. 163 status line')
