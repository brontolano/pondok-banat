#!/usr/bin/env python3
"""Fix remaining Rev. 953 issues in PRD-PONDOK-BANAT.md."""
import subprocess

REPO = "/opt/data/home/workspace/dev/pondok-banat"
PRD = f"{REPO}/PRD-PONDOK-BANAT.md"

with open(PRD, "r", encoding="utf-8") as f:
    content = f.read()

lines = content.split("\n")

# Fix 1: Rev 952 §11 row (line 4204, idx 4203)
# Find line containing "extended 116–951→116–952" and "1052| 04 Nov | 5d1e129"
rev952_s11_updated = False
for i, line in enumerate(lines):
    if "extended 116–951→116–952" in line and "5d1e129" in line and "1056/1/0" in line:
        lines[i] = line.replace("HEAD `5d1e12911d62811e94ec3b5b5d8994933a413b82`", "HEAD `71bb8e7b7ccc2b47ba024896641967674a7effa1`")\
            .replace("1056/1/0 (1056 local commits, 1 ahead / 0 behind origin_main)", "1057/2/0 (1057 local commits, 2 ahead / 0 behind origin_main)")\
            .replace("(Rev. 952 final commit)", "(Rev. 953 final commit)")
        rev952_s11_updated = True
        print(f"Rev 952 §11 row updated at line {i+1}")
        break

assert rev952_s11_updated, "Rev 952 §11 row not found!"

# Fix 2: Rev 950 entry's §12 (line 4186, idx 4185) - revert to correct
# Find line containing "updated to Rev. 952; commit count 1057/2/0" and "§12 status summary" before Rev 951 heading
rev950_s12_reverted = False
for i, line in enumerate(lines):
    if "updated to Rev. 952; commit count 1057/2/0" in line and "§12 status summary" in line and "1057/2/0" in line:
        # Check if this is the Rev 950 entry (before Rev 951 heading at line 4190)
        # Find Rev 951 heading
        for j in range(i, len(lines)):
            if "### Rev. 951" in lines[j]:
                if j > i:
                    # This is the Rev 950 entry's §12
                    lines[i] = lines[i].replace("updated to Rev. 952; commit count 1057/2/0", "updated to Rev. 950; commit count 1056/1/0")
                    rev950_s12_reverted = True
                    print(f"Rev 950 §12 reverted at line {i+1}")
                    break
        break

# Actually, let me just search for the Rev 950 entry's §12 more specifically
# The Rev 950 entry's §12 should say "updated to Rev. 950"
# Let me find the correct line number
rev950_s12_line = None
for i, line in enumerate(lines):
    if "> - **§12 status summary:** updated to Rev. 952; commit count 1057/2/0." in line and i < 4200:
        rev950_s12_line = i
        print(f"Found Rev 950 §12 at line {i+1}")
        break

if rev950_s12_line is not None:
    # Revert it to the original Rev 950 values
    lines[rev950_s12_line] = lines[rev950_s12_line].replace("updated to Rev. 952; commit count 1057/2/0", "updated to Rev. 950; commit count 1056/1/0")
    print(f"Rev 950 §12 reverted at line {rev950_s12_line+1}")

with open(PRD, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("Fix complete!")
