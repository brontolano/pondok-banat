#!/usr/bin/env python3
with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'r') as f:
    content = f.read()
target = 'dari Rev. 702 (data terkonsisten)'
if target in content:
    print('FOUND:', repr(target))
else:
    print('NOT FOUND:', repr(target))
    idx = content.find('data terkonsisten')
    if idx >= 0:
        print('Context:', repr(content[idx-30:idx+60]))
