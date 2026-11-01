#!/usr/bin/env python3
import os
os.chdir("/opt/data/home/workspace/dev/pondok-banat")

with open("PRD-PONDOK-BANAT.md", "r") as f:
    content = f.read()

# Fix commit count 887/1/0 -> 887/2/0 in header
content = content.replace(
    "commit count 887/1/0 (887 local commits, 2 ahead / 0 behind origin_main)",
    "commit count 887/2/0 (887 local commits, 2 ahead / 0 behind origin_main)"
)

# Fix untracked count in header: 62 -> 66
content = content.replace(
    "340 tracked files; 62 untracked (incl. helper scripts); 0 deleted.",
    "340 tracked files; 66 untracked (incl. helper scripts); 0 deleted."
)

with open("PRD-PONDOK-BANAT.md", "w") as f:
    f.write(content)
print("Done")
