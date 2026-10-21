#!/usr/bin/env python3
with open('/opt/data/home/workspace/dev/pondok-banat/update_prd_398.py', 'rb') as f:
    content = f.read()
# Find line 26 (old_s11)
idx = content.find(b'old_s11')
if idx != -1:
    line = content[idx:idx+200]
    print('Line 26 bytes:', line)
    print('Line 26 text:', line.decode('utf-8', errors='replace'))
