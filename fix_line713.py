#!/usr/bin/env python3
import io
path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
lines = io.open(path, encoding='utf-8').read().split('\n')
for i, line in enumerate(lines):
    if i == 712 and 'rev 602' in line and '80b8dd9' in line:
        lines[i] = line.replace('HEAD `80b8dd9` (Rev. 601 final commit)', 'HEAD `b7a5fc4` (Rev. 602 final commit)').replace('Rev. 600 (data terkonsisten)', 'Rev. 601 (data terkonsisten)').replace('Revision 602 confirms the completeness update of Rev. 600', 'Revision 602 confirms the completeness update of Rev. 601')
        print('Fixed line', i+1)
io.open(path, 'w', encoding='utf-8').write('\n'.join(lines))
print('Done')
