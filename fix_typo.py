#!/usr/bin/env python3
"""Fix typo 'tkconsistent' -> 'terkonsisten'."""

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r') as f:
    content = f.read()

old = "data terkconsistent"
new = "data terkonsisten"

if old in content:
    content = content.replace(old, new)
    print("Fixed typo: 'tkconsistent' -> 'terkonsisten'")
else:
    print("Pattern not found!")

with open(path, 'w') as f:
    f.write(content)

print("Saved")
