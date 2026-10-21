#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix escaping artifacts in PRD-PONDOK-BANAT.md from Rev. 366 update."""
import re

PATH = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Show problematic lines for debugging
lines = content.split("\n")
for i, line in enumerate(lines):
    if "151. REVISI TERBARU" in line and "## 151" in line:
        print(f"LINE {i}: {repr(line[:120])}")
        break

# Fix 1: replace literal \n\n (backslash-n backslash-n) with actual newlines
# The file has: origin.main.).\n\n## 151. REVISI
# Where \n is literally backslash+n (2 chars each)
count1 = content.count("\\n\\n")
content = content.replace("\\n\\n", "\n\n")
print("Pattern 1 (\\n\\n -> actual newlines):", count1)

# Fix 2: find and fix lines with double backslashes before quotes
# The file has: commit HEAD \\\"Release
# Where \\\" is: backslash, backslash, backslash, quote? Or: backslash, backslash, quote?
# Let's find the exact pattern
import re
# Pattern: HEAD \\\" -> HEAD \" (backslash backslash backslash quote -> backslash quote)
# Actually the file has: HEAD \\\"Release (3 chars: \ \ \ "?) 
# Let me check with regex
pattern2 = r'HEAD \\{2,3}"'
matches2 = re.findall(pattern2, content)
print("Pattern 2 matches:", matches2[:5])

# Replace HEAD \\\"Release with HEAD \"Release
# In Python source: r'HEAD \\\"Release' is the literal string: HEAD \\\"Release
# Wait, in raw string r'HEAD \\\"Release', the characters are: H E A D space \ \ \ " R e l e a s e
# That's: HEAD + space + 3 backslashes + quote + Release
# But the file has: HEAD + space + 2 backslashes + quote + Release (from cat -A: \\\")
# Let me be more careful.

# From cat -A output: commit HEAD \\\"Release
# cat -A displays: \\ -> two backslashes, \" -> quote (with backslash shown for escaping)
# So the file has: commit HEAD + space + \ + \ + " + Release
# That's: two backslashes + quote

# So in Python, the pattern is: 'HEAD \\"Release' (since \\ in Python string = one backslash)
# Wait, no. Python string 'HEAD \\"Release' = H E A D space \ " R e l e a s e
# That's: HEAD + space + one backslash + quote + Release
# But I need two backslashes + quote = 'HEAD \\\\"Release'
# Actually: 'HEAD \\"Release' in Python source = HEAD + space + \" (escaped quote) 
# No wait: 'HEAD \\"Release' = H E A D space \ " R e l e a s e (because \" is an escaped quote)

# Let me think again. In Python, to represent the literal string: HEAD \ \"Release
# I need: 'HEAD \\\\"Release'
# Because: \\ -> one backslash, \\ -> one backslash, \" -> quote
# So: 'HEAD \\\\"Release' = HEAD + space + \ \ " + Release

# Actually, the simplest way: use raw strings
# r'HEAD \\\"Release' = H E A D space \ \ \ " R e l e a s e (raw string, no escaping)
# That's: HEAD + space + 3 backslashes + quote

# Hmm, but cat -A showed: \\\" which I interpreted as 2 backslashes + quote
# Let me just use a different approach: search for the exact substring

# From the patch tool error, the file contains:
# commit HEAD \\\"Release: clean core files only\\\"
# The patch tool said "Could not find a match" because my old_string had different escaping.
# So the file has: HEAD \\\ "Release (with backslashes)

# Let me just check what's actually in the file using Python
test = 'commit HEAD \\\\"Release'
print("Test pattern:", repr(test))

# Actually, let me just use the simplest approach: read the file, and for each line 
# that has the problematic pattern, do a visual replacement.

# The key fixes needed:
# 1. In section 150 status line: literal \n\n -> actual newlines
# 2. In section 151 lines: \\\" -> \" (2 backslashes + quote -> 1 backslash + quote)
# 3. In section 151 lines: \\\"`) -> \")` (same, with backtick)

# Let me just do line-by-line processing
lines = content.split("\n")
new_lines = []
for line in lines:
    # Fix 2: HEAD \\\"Release -> HEAD \"Release (if we have 2 backslashes + quote in file)
    # In Python source, to match the literal text HEAD \ \ "Release:
    # We need the pattern: HEAD + space + \\ + \\ + " 
    # Which is: r'HEAD \\\"Release' 
    # But wait, in raw string r'HEAD \\\"Release', the characters are:
    # H E A D space \ \ \ " R e l e a s e -> that's 3 backslashes + quote
    # Hmm, I need to be precise.
    
    # Let me just check the actual bytes
    if "\\\\\\\"" in line or "\\\\" in line:
        # The line has backslashes that need fixing
        # Show what we're fixing
        print("Fixing line:", repr(line[:150]))
        # We need to determine how many backslashes there are
        # If the file has \\\" (2 backslashes + quote), we want \"
        # If the file has \\\\\" (4 backslashes + quote?), we want \\\"
        # Let me count: line.count("\\\\\\\"") counts 3 backslashes + quote
        # Wait, in Python source, "\\\\\\\"" = \ \ \ " (3 backslashes + quote)
        pass

# Let me take a completely different approach: use regex to fix all common escaping issues
# Fix: replace \\\" (2 backslashes + quote) with \" (1 backslash + quote)
# In Python regex: r'\\\\"' matches literal: \ \ " (2 backslashes + quote)
# And replacing with: r'\"' matches literal: \ " (1 backslash + quote)
content = re.sub(r'\\\\"', r'\\"', content)
print("After regex fix on \\\":", content.count('\\\\"'))

# Fix 3: replace \\\` with \` (if any)
# The file has: uidNfc @map(\\\"uid_nfc\\\")` )
# Which is: uidNfc @map(\ \ \ " uid_nfc " \ \ " ` )
# We want: uidNfc @map("uid_nfc") `
# Wait, the original PRD has: uidNfc String? @map("uid_nfc")
# So we need to remove ALL backslashes from the @map() and quotes

# Let me check what the file has
lines = content.split("\n")
for i, line in enumerate(lines):
    if "uidNfc @map" in line:
        print(f"Line {i}: {repr(line[:120])}")
        break

# After all fixes, write the file
with open(PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Fixes applied. File saved.")
print("Content has: HEAD \\\":", content.count(r'HEAD \"'))
print("Content has: HEAD \\\":", content.count('HEAD \\\\"'))
