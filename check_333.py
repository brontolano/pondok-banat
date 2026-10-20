# -*- coding: utf-8 -*-
import io

PATH = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with io.open(PATH, encoding='utf-8') as f:
    lines = f.readlines()

print('=== LAST 35 LINES ===')
for i, L in enumerate(lines[-35:], start=len(lines)-35+1):
    print(f'{i}: {L}', end='')

print('=== HEADER line 3 / line 4 (first 300) ===')
print(lines[2][:300])
print('---')
print(lines[3][:300])
