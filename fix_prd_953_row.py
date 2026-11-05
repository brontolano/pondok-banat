#!/usr/bin/env python3
"""Fix the Rev 952 §11 row metadata (commit hash and count)."""
import subprocess

REPO = "/opt/data/home/workspace/dev/pondok-banat"
PRD = f"{REPO}/PRD-PONDOK-BANAT.md"

with open(PRD, "r", encoding="utf-8") as f:
    content = f.read()

lines = content.split("\n")

# Fix the Rev 952 §11 row (line 4204, idx 4203)
# The row metadata | 952 | 04 Nov | 5d1e129 | 5d1e12911d62811e94ec3b5b5d8994933a413b82 | 1056/1/0 |
# needs to be updated to | 952 | 04 Nov | 71bb8e7 | 71bb8e7b7ccc2b47ba024896641967674a7effa1 | 1057/2/0 |
rev952_s11_row_updated = False
for i, line in enumerate(lines):
    if "extended 116–951→116–952" in line and "1056/1/0 |" in line and "5d1e12911d62811e94ec3b5b5d8994933a413b82" in line:
        # Replace the commit metadata
        old_meta = "| 952 | 04 Nov | 5d1e129 | 5d1e12911d62811e94ec3b5b5d8994933a413b82 | 1056/1/0 |"
        new_meta = "| 952 | 04 Nov | 71bb8e7 | 71bb8e7b7ccc2b47ba024896641967674a7effa1 | 1057/2/0 |"
        if old_meta in line:
            lines[i] = line.replace(old_meta, new_meta)
            rev952_s11_row_updated = True
            print(f"Rev 952 §11 row metadata updated at line {i+1}")
            break

assert rev952_s11_row_updated, "Rev 952 §11 row metadata not found!"

with open(PRD, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("Fix complete!")
