#!/usr/bin/env python3
PATH = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(PATH, encoding="utf-8") as f:
    s = f.read()

old = "## 11. REVISI TERBARU (Rev. 116–392 — 26 Oktober 2026 WIB)"
new = "## 11. REVISI TERBARU (Rev. 116–393 — 28 Oktober 2026 WIB)"
assert old in s, "subtitle not found"
s = s.replace(old, new)
with open(PATH, "w", encoding="utf-8") as f:
    f.write(s)
print("subtitle fixed")
