#!/usr/bin/env python3
import subprocess

with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'r') as f:
    lines = f.readlines()

print('TOTAL LINES:', len(lines))
line4 = lines[3]
print('LINE4 LEN:', len(line4))
print('LINE4 START:', line4[:200])
print('LINE4 END:', line4[-200:])

out = subprocess.run(['git', 'status', '--porcelain'], cwd='/opt/data/home/workspace/dev/pondok-banat', capture_output=True, text=True).stdout
untracked = [l for l in out.splitlines() if l.startswith('??')]
print('\nUNTRACKED COUNT:', len(untracked))
print('UNTRACKED LIST:', len(untracked))
