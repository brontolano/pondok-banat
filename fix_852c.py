#!/usr/bin/env python3
import os
os.chdir("/opt/data/home/workspace/dev/pondok-banat")

with open("PRD-PONDOK-BANAT.md", "r") as f:
    content = f.read()

# Fix remaining "887 / 1/0" in §12 commit count line
# Only replace the one in the Commit count line (not the Rev. 851 section)
old = '> - **Commit count:** 887 / 1/0 (fresh verification & stability confirmation'
new = '> - **Commit count:** 887 / 2/0 (fresh verification & stability confirmation'
if old in content:
    content = content.replace(old, new)
    print("Fixed commit count 887/1/0 -> 887/2/0")
else:
    print("Pattern not found")

with open("PRD-PONDOK-BANAT.md", "w") as f:
    f.write(content)
