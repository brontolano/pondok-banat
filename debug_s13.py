#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Find the §13 Rev. 467 entry - use a unique substring
marker = "||- **Rev. 467.** 23 Oktober 2026 (WIB): PRD fresh verification"
idx = content.find(marker)
print("Found marker at:", idx)
if idx < 0:
    # Try alternative
    idx = content.find("Rev. 467." + " 23 Oktober 2026")
    print("Found alternative at:", idx)

if idx >= 0:
    # Find the end of this entry (next line starting with |||- **Rev. or a newline + |||-)
    end_marker = "||- **Rev. 462.**"
    end_idx = content.find(end_marker, idx)
    print("End marker at:", end_idx)
    if end_idx < 0:
        end_idx = len(content)
    
    # Get the full entry
    entry = content[idx:end_idx]
    print("Entry length:", len(entry))
    print("First 200 chars:", repr(entry[:200]))
    print("...")
    print("Last 200 chars:", repr(entry[-200:]))
    
    # Now check for specific patterns
    if "from Rev. 462" in entry:
        print("Entry contains 'dari Rev. 462'")
    if "from Rev. 466" in entry:
        print("Entry contains 'dari Rev. 466'")
    if "dari Rev. 462 (data" in entry:
        print("Entry contains 'dari Rev. 462 (data'")
    if "dari Rev. 466 (data" in entry:
        print("Entry contains 'dari Rev. 466 (data'")
