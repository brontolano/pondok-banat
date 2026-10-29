#!/usr/bin/env python3
with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'r') as f:
    lines = f.readlines()

# Find the Rev. 703 status line
for i, line in enumerate(lines, 1):
    if 'rev 703' in line and 'Status' in line:
        print(f'Line {i}: {repr(line)}')
