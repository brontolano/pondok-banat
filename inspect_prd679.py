#!/usr/bin/env python3
"""Inspect PRD file structure around §12 and Rev. 678 section."""

with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md') as f:
    lines = f.readlines()

# Find all ### Rev. headings
print("=== ### headings ===")
for i, line in enumerate(lines, 1):
    if line.startswith('### Rev.'):
        print(f'{i}|{line.rstrip()[:80]}')

# Find all ## headings
print("\n=== ## headings ===")
for i, line in enumerate(lines, 1):
    if line.startswith('## '):
        print(f'{i}|{line.rstrip()[:80]}')

# Show lines 1280-1312
print("\n=== Lines 1280-1312 ===")
for i in range(1280, min(1312, len(lines))):
    print(f'{i+1}|{lines[i].rstrip()}')
