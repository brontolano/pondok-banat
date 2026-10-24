#!/usr/bin/env python3
"""Fix remaining duplicate indentation in PRD-PONDOK-BANAT.md."""

PATH = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(PATH) as f:
    content = f.read()

# Fix 1: Line 450 duplicate indentation: "    ||    ||- " -> "    ||- "
old = "    ||    ||- **Rev. 523 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oktober 2026 (WIB); HEAD `8604c3c440d839e5312de173e70e067695006663`"
new = "    ||- **Rev. 523 (final).** 24 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (24 Oktober 2026 (WIB); HEAD `8604c3c440d839e5312de173e70e067695006663`"

if old in content:
    content = content.replace(old, new)
    print("✅ Fixed duplicate indentation at line 450")
else:
    print("⚠️ Expected pattern not found at line 450")

# Fix 2: Check for any remaining duplicate "(WIB)" patterns
import re
remaining = re.findall(r"\([^)]*WIB[^)]*\)", content)
if any("(WIB) (WIB)" in s or "(WIB) WIB)" in s for s in remaining):
    print("⚠️ Still found duplicate WIB patterns")
else:
    print("✅ No duplicate WIB patterns found")

with open(PATH, "w") as f:
    f.write(content)

print(f"\n✅ Done. File size: {len(content)} bytes")
