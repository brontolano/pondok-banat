#!/usr/bin/env python3
# -*- coding: utf-8 -*-
with open("/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md", encoding="utf-8") as f:
    lines = f.read().splitlines()
with open("/opt/data/home/workspace/dev/pondok-banat/update_prd491_v2.py", encoding="utf-8") as f:
    script = f.read()

import re
# Extract the predicate from v2 script line 27
m = re.search(r'l\.startswith\("(\|\-_ \*\*Rev\. 489 \(final\)\.\*+)', script)
print("regex match:", bool(m))
if m:
    pred = m.group(1)
    print("predicate repr:", repr(pred))

# Find the line in PRD containing 'Rev. 489 (final)'
for i, l in enumerate(lines):
    if 'Rev. 489 (final)' in l:
        print("PRD line index:", i, "1-based:", i+1)
        print("startswith predicate:", l.startswith('||_- **Rev. 489 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `7adb7ce66c8d9a5ee707215b21339f451592e1` (Rev. 489 (final):'))
        print("len line:", len(l))
        break

# Compare char-by-char for first 80 chars
target = '||_- **Rev. 489 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD `7adb7ce66c8d9a5ee707215b21339f451592e1` (Rev. 489 (final):'
print("target len:", len(target))
for i, l in enumerate(lines):
    if '||_- **Rev. 489 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); HEAD' in l:
        print("line idx:", i, "len:", len(l))
        print("target == line[:len(target)]:", target == l[:len(target)])
        print("repr target:", repr(target))
        print("repr line[:80]:", repr(l[:80]))
        break
