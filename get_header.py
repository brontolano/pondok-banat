#!/usr/bin/env python3
with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'r') as f:
    lines = f.readlines()
line = lines[3]
print('LENGTH:', len(line))
# Print the full line so we can copy it exactly
print(line)
