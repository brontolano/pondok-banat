#!/usr/bin/env python3
"""Fix §12.387 content (HEAD count) and reorder: 386 → 387 → 388."""
import os

REPO = "/opt/data/home/workspace/dev/pondok-banat"
PRD_PATH = os.path.join(REPO, "PRD-PONDOK-BANAT.md")

with open(PRD_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# ---- 1. Fix §12.387 Git HEAD bullet: 21 -> 22 commits ahead ----
old_387_head = """1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 386 (data terkonsisten).**
   - **Git HEAD (local):** `93d755f00d9756ab07fc0b27dba539f6152501c6` \"Rev. 387: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 387, §11 compact changelog 116–386, §12 updated Rev. 386/387; HEAD 991a4d0 (Rev. 385), 22 commits ahead origin/main\"; content commit `93d755f00d9756ab07fc0b27dba539f6152501c6` (Rev. 386: PRD fresh verification & stability confirmation; HEAD 991a4d0 (Rev. 385), 20 commits ahead origin/main). Local branch **21 commits ahead** of `origin/main` (fresh verification, 23 Oct 2026 WIB)."""
new_387_head = """1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 386 (data terkonsisten).**
   - **Git HEAD (local):** `93d755f00d9756ab07fc0b27dba539f6152501c6` \"Rev. 387: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 387, §11 compact changelog 116–386, §12 updated Rev. 386/387; HEAD 991a4d0 (Rev. 385), 22 commits ahead origin/main\"; content commit `93d755f00d9756ab07fc0b27dba539f6152501c6` (Rev. 386: PRD fresh verification & stability confirmation; HEAD 991a4d0 (Rev. 385), 20 commits ahead origin/main). Local branch **22 commits ahead** of `origin/main` (fresh verification, 21 Oct 2026 WIB)."""
if old_387_head in content:
    content = content.replace(old_387_head, new_387_head, 1)
    print("§12.387 Git HEAD bullet: '21' -> '22' commits ahead")
else:
    print("WARNING: §12.387 Git HEAD bullet not found")

# ---- 2. Reorder: move Rev. 387 section before Rev. 388 ----
# Find the §12.387 heading position
idx_387 = content.find("## 12. REVISI TERBARU (Rev. 387 — 23 Oktober 2026 WIB)")
idx_388 = content.find("## 12. REVISI TERBARU (Rev. 388 — 21 Oktober 2026 WIB)")

if idx_387 != -1 and idx_388 != -1:
    if idx_387 > idx_388:
        # 387 is after 388 — need to swap
        # Extract the full 387 section (until the next "## 12." after it)
        start_387 = idx_387
        end_387 = content.find("\n## 12. REVISI TERBARU", idx_387 + 1)
        if end_387 == -1:
            end_387 = len(content)
        
        # Extract 387 section
        section_387 = content[start_387:end_387]
        
        # Remove it from current position
        content = content[:start_387] + content[end_387:]
        
        # Insert before Rev. 388
        insert_pos = idx_388  # idx_388 is still valid (points to original 388 position)
        content = content[:insert_pos] + section_387 + content[insert_pos:]
        print("§12.387 moved before §12.388")
    else:
        print("§12.387 already before §12.388")
else:
    print("WARNING: Could not find §12.387 or §12.388 headings")

# ---- 3. Write back ----
with open(PRD_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("SUCCESS: PRD fixed")
print(f"PRD size: {os.path.getsize(PRD_PATH)} bytes")
