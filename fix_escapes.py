#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix escaping artifacts in PRD-PONDOK-BANAT.md from Rev. 366 update."""
import io

PATH = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(PATH, "r", encoding="utf-8") as f:
    content = f.read()

fixed = 0

# 1. Fix literal backslash-n in section 150 status line
old1 = "origin.main.).\\n\\n## 151. REVISI TERBARU (Rev. 366"
new1 = "origin.main.).\n\n## 151. REVISI TERBARU (Rev. 366"
n1 = content.count(old1)
if n1 != 1:
    print("WARNING: pattern 1, expected 1, got", n1)
else:
    content = content.replace(old1, new1)
    fixed += 1
print("Pattern 1 fix:", n1)

# 2. Fix double backslash in "commit HEAD \\\"Release" -> "commit HEAD \"Release"
#    File currently has: commit HEAD \\\"Release (two backslashes + quote)
#    Should be: commit HEAD \"Release (one backslash + quote)
old2 = 'commit HEAD \\\\\\"Release: clean core files only\\\\\\"'
# The above is: commit HEAD \\\"Release (in the file: two backslashes + quote)
# But actually the file has: commit HEAD \\\"Release
# Let me check: the file has \\\" which is backslash backslash backslash quote? No.
# In the file: commit HEAD \\\"Release
# Characters: \ \ \ " (three backslashes + quote) or \ \ " (two backslashes + quote)?
# From cat -A: \\\" = two backslashes + quote (cat shows two backslashes as \\, then quote as ")
# Wait, cat -A shows: \\\" -> this is: backslash, backslash, quote (three chars before quote? No.)
# Actually cat -A shows: \\\" which means: \, \, " (two backslashes + quote)
# So the file has: commit HEAD \ \ " Release ... = commit HEAD \\\"Release
old2 = 'commit HEAD \\"Release: clean core files only\\"'
new2 = 'commit HEAD "Release: clean core files only"'
n2 = content.count(old2)
if n2 != 1:
    print("WARNING: pattern 2, expected 1, got", n2)
else:
    content = content.replace(old2, new2)
    fixed += 1
print("Pattern 2 fix:", n2)

# 3. Fix double backslash in "uidNfc @map(\\\"uid_nfc\\\")"
#    File has: uidNfc @map(\\\"uid_nfc\\\") (with escaped quotes)
#    Should be: uidNfc @map("uid_nfc") (just the quotes, no backslashes)
old3 = 'uidNfc @map(\\\\\\"uid_nfc\\\\\\")'
# Actually let me check the exact pattern. From cat -A:
# uidNfc String? @map(\\\"uid_nfc\\\") = uidNfc String? @map(\ \ " uid_nfc " \) 
# Wait, cat -A shows: uidNfc String? @map(\\\"uid_nfc\\\")
# This is: uidNfc String? @map(\ \ " uid_nfc " \) - hmm
# Let me just check: the file shows uidNfc @map(\\\"uid_nfc\\\")
# Which is: uidNfc @map(\ \ " uid_nfc " \) - three backslashes + quote
# Actually I think cat -A shows: \\\" which is: \, \, " (two backslashes + quote)
# So the file has: uidNfc String? @map(\ \ " uid_nfc " \) = uidNfc String? @map(\\"uid_nfc"\)
old3 = 'uidNfc @map(\\\\\\"uid_nfc\\\\\\")'
new3 = 'uidNfc String? @map("uid_nfc")'
n3 = content.count(old3)
if n3 != 1:
    print("WARNING: pattern 3, expected 1, got", n3)
else:
    content = content.replace(old3, new3)
    fixed += 1
print("Pattern 3 fix:", n3)

# 4. Fix double backslash before "uidNfc @map(\\\"uid_nfc\\\"` )"
old4 = 'uidNfc @map(\\\\\\"uid_nfc\\\\\\"` )'
new4 = 'uidNfc @map("uid_nfc") '
n4 = content.count(old4)
if n4 != 1:
    print("WARNING: pattern 4, expected 1, got", n4)
else:
    content = content.replace(old4, new4)
    fixed += 1
print("Pattern 4 fix:", n4)

with open(PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Total fixes applied:", fixed)
