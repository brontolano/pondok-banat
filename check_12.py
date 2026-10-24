#!/usr/bin/env python3
"""Extract and fix the §12 Rev. 522/523 entries."""

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(path) as f:
    lines = f.read().split("\n")

# Check lines around §12 section (lines 550-555)
for i in range(548, 556):
    line = lines[i]
    if "Rev. 522" in line or "Rev. 523" in line or "Rev. 521" in line:
        print(f"Line {i+1} ({len(line)} chars):")
        print(f"  Start: {line[:60]}")
        print(f"  End:   {line[-80:]}")
        print()

# Check if §12 Rev. 523 entry exists
found_523 = any("Rev. 523" in lines[i] for i in range(550, 555))
print(f"§12 Rev. 523 exists: {found_523}")

# Find the end of §12 Rev. 522 entry
for i in range(550, 554):
    line = lines[i]
    if "Rev. 522" in line:
        print(f"§12 Rev. 522 at line {i+1}")
        print(f"Last 200 chars: {line[-200:]}")
        break
