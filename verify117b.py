# -*- coding: utf-8 -*-
import io
PATH = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with io.open(PATH, encoding='utf-8') as f:
    lines = f.readlines()
# Section 117 main verification bullet is at index 7486 (line 7487)
print('S117 L7487:', repr(lines[7486][:260]))
print('---')
# Header line 4 (index 3)
print('HEADER L4:', repr(lines[3][600:900]))
