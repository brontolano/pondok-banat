#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix messy HEAD references in section 110 (lines 7307, 7321, 7324)."""
import os
REPO = "/opt/data/home/workspace/dev/pondok-banat"
PRD = os.path.join(REPO, "PRD-PONDOK-BANAT.md")

with open(PRD, encoding="utf-8") as f:
    c = f.read()

# 1) Fix line 7307: commit portion
old1 = "(Rev. 324, commit 4b24651 Rev. 324: PRD fresh verification & stability confirmation (20 Oct 2026 WIB); updated header to Rev. 324 + added section 109)"
new1 = "(Rev. 324, commit 4b24651)"
assert c.count(old1) == 1, f"old1 count={c.count(old1)}"
c = c.replace(old1, new1)

# 2) Fix Referensi HEAD bullet (line 7321)
old2 = """   - **Referensi HEAD:** section 109 (Rev. 324) mencatat HEAD sebagai `4b24651 Rev. 324: PRD fresh verification & stability confirmation (20 Oct 2026 WIB); updated header to Rev. 324 + added section 109` (Rev. 323, commit dbf2fe0) sebab state verifikasi dites sebelum commit Rev. 324. State terkini HEAD = `4b246510265ea3b38962d400cba6426a68105458` (Rev. 324, commit 4b24651 Rev. 324: PRD fresh verification & stability confirmation (20 Oct 2026 WIB); updated header to Rev. 324 + added section 109), **18 commits ahead** origin.main."""
new2 = """   - **Referensi HEAD:** section 109 (Rev. 324) mencatat HEAD sebagai `dbf2fe0` (Rev. 323, commit dbf2fe0) sebab state verifikasi dites sebelum commit Rev. 324. State terkini HEAD = `4b24651` (Rev. 324, commit 4b24651), **18 commits ahead** origin.main."""
assert c.count(old2) == 1, f"old2 count={c.count(old2)}"
c = c.replace(old2, new2)

# 3) Fix Status bullet (line 7324)
old3 = """3. **Status:** dokumen PRD **REVISI** \u2014 rev 325 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 325**. Git HEAD = `4b24651 Rev. 324: PRD fresh verification & stability confirmation (20 Oct 2026 WIB); updated header to Rev. 324 + added section 109` (Rev. 324, commit 4b24651 Rev. 324: PRD fresh verification & stability confirmation (20 Oct 2026 WIB); updated header to Rev. 324 + added section 109), **18 commits ahead** origin.main."""
new3 = """3. **Status:** dokumen PRD **REVISI** \u2014 rev 325 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 325**. Git HEAD = `4b24651` (Rev. 324, commit 4b24651), **18 commits ahead** origin.main."""
assert c.count(old3) == 1, f"old3 count={c.count(old3)}"
c = c.replace(old3, new3)

with open(PRD, "w", encoding="utf-8") as f:
    f.write(c)

print("Fixed. Verifying affected lines:")
for i, line in enumerate(c.splitlines(), 1):
    if "4b24651 Rev. 324: PRD" in line or "4b24651 Rev. 324: PRD" in line and i >= 7300:
        print(i, "|", line)
print("Done.")
