# -*- coding: utf-8 -*-
import io
PATH = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with io.open(PATH, encoding='utf-8') as f:
    lines = f.readlines()
print('L7487:', repr(lines[7486][600:850]))
