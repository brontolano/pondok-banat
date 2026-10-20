#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Clean up all '4b24651 Rev. 324: PRD ...' messy embeddings in section 110."""
import os
REPO = "/opt/data/home/workspace/dev/pondok-banat"
PRD = os.path.join(REPO, "PRD-PONDOK-BANAT.md")

with open(PRD, encoding="utf-8") as f:
    c = f.read()

needle = "4b24651 Rev. 324: PRD fresh verification & stability confirmation (20 Oct 2026 WIB); updated header to Rev. 324 + added section 109)"
count = c.count(needle)
print(f"needle occurrences: {count}")
assert count == 3, f"expected 3, got {count}"
c = c.replace(needle, "4b24651")

with open(PRD, "w", encoding="utf-8") as f:
    f.write(c)
print("Replaced. Showing affected lines:")
for i, line in enumerate(c.splitlines(), 1):
    if "4b24651 Rev. 324: PRD" in line or "4b246510265ea3b38962d400cba6426a68105458" in line and i >= 7300:
        print(i, "|", line)
