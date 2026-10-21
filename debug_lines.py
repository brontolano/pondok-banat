#!/usr/bin/env python3
lines = open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md').readlines()
for i in range(415, 425):
    print(f'{i+1}: {repr(lines[i])}')