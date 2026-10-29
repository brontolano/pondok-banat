#!/usr/bin/env python3
"""Debug: inspect the final status line of the PRD file."""

with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'rb') as f:
    data = f.read()

# Find the final status line
idx = data.rfind(b'dokeman PRD **REVISI**')
print('Found at byte:', idx)
print('Context:')
print(repr(data[idx-50:idx+300]))

# Check for trailing comma
end_bytes = data[idx+250:idx+260]
print('End bytes:', repr(end_bytes))
if end_bytes.endswith(b','):
    print('Trailing comma found!')
else:
    print('No trailing comma.')
