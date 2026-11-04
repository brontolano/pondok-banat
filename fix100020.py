#!/usr/bin/env python3
"""Fix remaining 1000/2/0 in Rev. 914 entry."""
import os

ws = "/opt/data/home/workspace/dev/pondok-banat"
os.chdir(ws)

with open("PRD-PONDOK-BANAT.md") as f:
    content = f.read()

# Fix Rev. 914 entry's changelog row commit count
old1 = "| 914 | 04 Nov | 12847e8 | 637f1f7ff092d7f89630efec79cf8f741bee7935 | 1000/2/0 |"
new1 = "| 914 | 04 Nov | 12847e8 | 637f1f7ff092d7f89630efec79cf8f741bee7935 | 1001/2/0 |"
if old1 in content:
    content = content.replace(old1, new1)
    print("Fixed changelog row commit count 1000/2/0 -> 1001/2/0")
else:
    print("Changelog row pattern not found")

# Fix Rev. 914 entry's §13 notes commit count
old2 = "Refreshed 04 November 2026 WIB; HEAD `637f1f7ff092d7f89630efec79cf8f741bee7935` (Rev. 914 final sync); commit count 1000/2/0."
new2 = "Refreshed 04 November 2026 WIB; HEAD `637f1f7ff092d7f89630efec79cf8f741bee7935` (Rev. 914 final sync); commit count 1001/2/0."
if old2 in content:
    content = content.replace(old2, new2)
    print("Fixed §13 notes commit count 1000/2/0 -> 1001/2/0")
else:
    print("§13 notes pattern not found")

# Write
with open("PRD-PONDOK-BANAT.md", "w") as f:
    f.write(content)

print("Done. Size:", os.path.getsize("PRD-PONDOK-BANAT.md"))
