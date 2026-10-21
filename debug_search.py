#!/usr/bin/env python3
with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'r') as f:
    lines = f.readlines()

print("Searching for '397. 21 Oktober 2026' (any whitespace):")
for i, line in enumerate(lines):
    if '397. 21 Oktober 2026' in line:
        print(f'  line {i+1}: {line[:120].rstrip()}')
