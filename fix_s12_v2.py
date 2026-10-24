#!/usr/bin/env python3
"""Fix remaining Rev. 503 -> Rev. 505 in §12 status."""

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r') as f:
    content = f.read()

# Replace Rev. 503 -> Rev. 505 in the Status section of §12
# The status section ends with "State stabil, tidak ada perubahan signifikan dari Rev. 503 (data terkonsisten)."

old = "State stabil, tidak ada perubahan signifikan dari Rev. 503 (data terkonsisten)."
new = "State stabil, tidak ada perubahan signifikan dari Rev. 505 (data terkconsistent)."

if old in content:
    content = content.replace(old, new)
    print("Fixed Rev. 503 -> Rev. 505 in Status section")
else:
    print("Pattern not found!")
    # Find what's there
    idx = content.find("State stabil")
    print(content[idx:idx+100])

with open(path, 'w') as f:
    f.write(content)

print("Saved")
