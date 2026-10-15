#!/usr/bin/env python3
"""Check exact bytes of folder name in line 260."""

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r') as f:
    lines = f.readlines()

# Line 260 (index 259)
line = lines[259]
print("Line 260 bytes:")
for i, b in enumerate(line.encode('utf-8')):
    if b in [46, 47, 99, 107, 97, 110]:  # . / c k a n
        print(f"  pos {i}: byte {b} = {chr(b)}")
print()
print("Line 260:")
print(repr(line[:80]))
print()

# Check for 'c' vs 'k' after 'pondon'
idx = line.find('pondokanat')
if idx != -1:
    print(f"Found 'pondokanat' at index {idx}")
    print(f"  Bytes: {list(line[idx:idx+12].encode('utf-8'))}")
    print(f"  Chars: {line[idx:idx+12]}")
