#!/usr/bin/env python3
path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = "(revisi terbaru = Rev. 493 (final), fresh verification dilakukan hari ini)"
new = "(revisi terbaru = Rev. 494 (final), fresh verification dilakukan hari ini)"
assert old in content, "Working tree note not found"
content = content.replace(old, new)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("Fixed working tree note")
