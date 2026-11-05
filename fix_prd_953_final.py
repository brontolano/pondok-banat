#!/usr/bin/env python3
"""Fix remaining Rev. 953 updates in PRD-PONDOK-BANAT.md."""
import subprocess

REPO = "/opt/data/home/workspace/dev/pondok-banat"
PRD = f"{REPO}/PRD-PONDOK-BANAT.md"

with open(PRD, "r", encoding="utf-8") as f:
    content = f.read()

lines = content.split("\n")

# 1. Update header (line 3)
header_updated = False
for i, line in enumerate(lines):
    if "Rev. 952 (fresh verification & metadata sync — 04 November 2026 WIB); §11 compact changelog" in line:
        lines[i] = line.replace("Rev. 952", "Rev. 953")\
            .replace("116–951→116–952", "116–952→116–953")\
            .replace("HEAD `5d1e12911d62811e94ec3b5b5d8994933a413b82`", "HEAD `71bb8e7b7ccc2b47ba024896641967674a7effa1`")\
            .replace("(Rev. 952 final commit)", "(Rev. 953 final commit)")\
            .replace("commit count 1056/1/0 (1056 local commits, 1 ahead / 0 behind origin_main)", "commit count 1057/2/0 (1057 local commits, 2 ahead / 0 behind origin_main)")\
            .replace("node_modules present (84021 files / 479 top-level dirs)", "node_modules present (84021 files / 477 top-level dirs)")\
            .replace("Working tree: PRD ditulis ke Rev. 952", "Working tree: PRD ditulis ke Rev. 953")
        header_updated = True
        print(f"Header updated at line {i+1}")
        break

assert header_updated, "Header not found!"

# 2. Update Rev 952 §12 (line 4206, idx 4205)
s12_updated = False
for i, line in enumerate(lines):
    if "> - **§12 status summary:** updated to Rev. 952; commit count 1056/1/0." in line and i > 500:
        lines[i] = line.replace("updated to Rev. 952; commit count 1056/1/0", "updated to Rev. 952; commit count 1057/2/0")
        s12_updated = True
        print(f"Rev 952 §12 updated at line {i+1}")
        break

assert s12_updated, "Rev 952 §12 not found!"

# 3. Verify Rev 952 §13
for i, line in enumerate(lines):
    if "Refreshed 04 November 2026 WIB; HEAD `71bb8e7b7ccc2b47ba024896641967674a7effa1`" in line and "Rev. 952 final commit" in line:
        print(f"Rev 952 §13 confirmed at line {i+1}")
        break

# 4. Verify Rev 953 entry exists
found_953 = False
for i, line in enumerate(lines):
    if "### Rev. 953" in line:
        found_953 = True
        print(f"Rev 953 entry found at line {i+1}")
        break
assert found_953, "Rev 953 entry not found!"

with open(PRD, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("Fix complete!")
