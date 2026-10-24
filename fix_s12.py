#!/usr/bin/env python3
"""Fix remaining issues in §12."""

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r') as f:
    content = f.read()

# Fix remaining "Rev. 504 (final)" on line 438
# The working tree section has: HEAD `dc9bd27f6be685f176bfed9c08be3674b17cf744` (Rev. 504 (final))
# We need to change it to: HEAD `dc9bd27f6be685f176bfed9c08be3674b17cf744` (Rev. 506 commit)

old = "HEAD `dc9bd27f6be685f176bfed9c08be3674b17cf744` (Rev. 504 (final))"
new = "HEAD `dc9bd27f6be685f176bfed9c08be3674b17cf744` (Rev. 506 commit)"

if old in content:
    content = content.replace(old, new)
    print("Fixed remaining Rev. 504 (final) on line 438")
else:
    print("Pattern not found - checking what's there...")
    idx = content.find("Working tree")
    print(content[idx:idx+300])

with open(path, 'w') as f:
    f.write(content)

print("Saved")
