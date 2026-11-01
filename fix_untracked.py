#!/usr/bin/env python3
"""Fix untracked count in PRD header."""

PRD_PATH = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(PRD_PATH, 'r') as f:
    content = f.read()

content = content.replace('340 tracked files; 59 untracked', '340 tracked files; 60 untracked')

with open(PRD_PATH, 'w') as f:
    f.write(content)

print("Fixed untracked count in header: 59 -> 60")
