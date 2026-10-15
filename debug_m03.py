#!/usr/bin/env python3
with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'r') as f:
    content = f.read()
idx = content.find('| M03 | Master')
if idx >= 0:
    print(content[idx:idx+400])
