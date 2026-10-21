#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix escaping artifacts in PRD-PONDOK-BANAT.md from Rev. 366 update."""
import re

PATH = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Fix 1: literal \n\n (backslash-n backslash-n) -> actual newlines
n1 = content.count("\\n\\n")
content = content.replace("\\n\\n", "\n\n")
print("Fix 1 - literal backslash-n pairs:", n1)

# Fix 2: fix HEAD \\\"Release (file has 2 backslashes + quote) -> HEAD "Release
# In file: HEAD \\\"Release means: H E A D space \ \ " R e l e a s e
# Python string to match: 'HEAD \\"Release' means: H E A D space \ " R e l e a s e (1 backslash)
# No wait: Python 'HEAD \\"Release' = H E A D space \ " R e l e a s e
# We need: H E A D space \ \ " R e l e a s e
# So: 'HEAD \\\\"Release' = H E A D space \ \ " R e l e a s e
n2 = content.count('HEAD \\\\"Release')
content = content.replace('HEAD \\\\"Release', 'HEAD "Release')
print("Fix 2 - HEAD double-backslash quote:", n2)

# Fix 3: fix commit HEAD \\\"Release (same as fix 2)
n3 = content.count('commit HEAD \\\\"Release')
content = content.replace('commit HEAD \\\\"Release', 'commit HEAD "Release')
print("Fix 3 - commit HEAD double-backslash quote:", n3)

# Fix 4: fix uidNfc @map(\\\"uid_nfc\\\") -> uidNfc String? @map("uid_nfc")
# File has: uidNfc String? @map(\\\"uid_nfc\\\")
# Python match string: 'uidNfc String? @map(\\\\\\"uid_nfc\\\\\\")'
# Let me check the actual content first
lines = content.split("\n")
for i, line in enumerate(lines):
    if "uidNfc @map" in line:
        print("Line with uidNfc @map:", repr(line))
        break

# After looking at the file, it seems to have:
# uidNfc String? @map(\\\"uid_nfc\\\")
# Which in Python source is: uidNfc String? @map(\ \ \ " uid_nfc " \ \ ")
# I want: uidNfc String? @map("uid_nfc")
# Python source to match: 'uidNfc String? @map(\\\\\\"uid_nfc\\\\\\")'
# This is: uidNfc String? @map(\ \ \ " uid_nfc " \ \ ")
n4 = content.count('uidNfc String? @map(\\\\\\"uid_nfc\\\\\\\\)')
content = content.replace('uidNfc String? @map(\\\\\\"uid_nfc\\\\\\\\)', 'uidNfc String? @map("uid_nfc")')
print("Fix 4 - uidNfc @map pattern:", n4)

# Also fix the second occurrence: uidNfc @map(\\\"uid_nfc\\\"` )
lines2 = content.split("\n")
for i, line in enumerate(lines2):
    if "@map(\\\"uid_nfc" in line:
        print("Second line with @map:", repr(line))
        break

# Fix @map(\\\"uid_nfc\\\")` ) -> @map("uid_nfc") `)
n5 = content.count('@map(\\\\\\"uid_nfc\\\\\\\\)` )')
content = content.replace('@map(\\\\\\"uid_nfc\\\\\\\\)` )', '@map("uid_nfc") `)')
print("Fix 5 - uidNfc @map second pattern:", n5)

with open(PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("File saved.")
