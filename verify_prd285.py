#!/usr/bin/env python3
# -*- coding: utf-8 -*-
PRD = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(PRD, 'r', encoding='utf-8') as f:
    lines = f.readlines()

def subprocess_run(cmd):
    import subprocess
    return subprocess.run(cmd, capture_output=True, text=True).stdout

print('=== GIT STATUS (via python) ===')

print('\n=== SECTION HEADERS (Rev. X) ===')
import re
for l in lines:
    if re.match(r'^## 6\d+\.\s+REVISI', l):
        print(' ', l.rstrip()[:100])

print('\n=== HEADER LINE 4 ===')
print(' ', lines[3].rstrip()[:200])

print('\n=== VERIFY GIT HEAD REFS IN HEADER ===')
header = lines[3]
print('Local HEAD ref:', 'b53a00c4c7a09b4dbbf999487ca471171cd33510' in header)
print('Origin HEAD ref:', '1c67b15280e94489504b518831cfdf674e2bf8d0' in header)
print('Branch 1 ahead:', '**1 commit ahead**' in header)

print('\n=== VERIFY NEW SECTION CONTENT ===')
section63 = ''.join(lines)
print('Section 63 exists:', '## 63. REVISI TERBARU' in section63)
print('Rev. 285 date:', '19 Oktober 2026' in section63)
print('Branch ahead 1:', '1 commit ahead' in section63)
print('Untracked 51:', '51 file tambahan' in section63)
print('Last 5 lines:')
for l in lines[-5:]:
    print('   ', l.rstrip()[:110])

def subprocess_run(cmd):
    import subprocess
    return subprocess.run(cmd, capture_output=True, text=True).stdout

