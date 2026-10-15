#!/usr/bin/env python3
with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'r') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'M03' in line and ('Master' in line or 'Guru' in line or 'Direncanakan' in line):
        print(f"{i+1}: {line.rstrip()}")
