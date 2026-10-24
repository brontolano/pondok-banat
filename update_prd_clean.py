#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Clean update: start from git HEAD (Rev. 466), apply all changes to Rev. 467."""
import io

src = "/tmp/prd_orig_466.md"
dst = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with io.open(src, "r", encoding="utf-8") as f:
    content = f.read()

# ===== 1. HEADER =====
old = "Rev. 466: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 466, §11 kompakt changelog 116–465"
new = "Rev. 467: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 467, §11 kompakt changelog 116–466"
assert old in content, "Header not found"
content = content.replace(old, new)

# ===== 2. §11 header =====
old = "## 11. REVISI TERBARU (Rev. 116–463 — 23 Oktober 2026 WIB)"
new = "## 11. REVISI TERBARU (Rev. 116–467 — 23 Oktober 2026 WIB)"
assert old in content, "§11 header not found"
content = content.replace(old, new)

# ===== 3. §12 header =====
old = "## 12. REVISI TERBARU (Rev. 463 — 23 Oktober 2026 WIB)"
new = "## 12. REVISI TERBARU (Rev. 467 — 23 Oktober 2026 WIB)"
assert old in content, "§12 header not found"
content = content.replace(old, new)

# ===== 4. §12 content =====
# 4a. Line 759: "Tidak ada perubahan signifikan dari Rev. 462 (data terkonsisten)" -> "Rev. 466"
old = "Tidak ada perubahan signifikan dari Rev. 462 (data terkonsisten)"
new = "Tidak ada perubahan signifikan dari Rev. 466 (data terkonsisten)"
assert content.count(old) == 1, f"4a count={content.count(old)}"
content = content.replace(old, new)

# 4b. Line 760: "Local branch **0 commit ahead / 0 behind** origin_main (in sync)" + "updated), 0 / 0 (0 commit ahead origin_main). Local branch"
old = "updated), 0 / 0 (0 commit ahead origin_main). Local branch **0 commit ahead / 0 behind** origin_main (in sync)"
new = "updated), 4 / 0 (4 commits ahead origin_main). Local branch **4 commits ahead / 0 behind** origin_main"
cnt = content.count(old)
assert cnt == 1, f"4b count={cnt}"
content = content.replace(old, new)

# 4c. Line 760: "header Rev. 463, §11 kompakt changelog 116–462, §12 updated" -> "header Rev. 467, §11 kompakt changelog 116–466, §12 updated"
old = "header Rev. 463, §11 kompakt changelog 116–462, §12 updated"
new = "header Rev. 467, §11 kompakt changelog 116–466, §12 updated"
cnt = content.count(old)
# This appears 3 times: line 760 (§12), line 775 (§13), line 776 (§13)
# We want to change only the §12 one (line 760). But the §13 ones also need "Rev. 463" -> "Rev. 467"
# Let's handle them separately in the §13 section.

# 4d. Line 761: "revisi terbaru = Rev. 463" -> "revisi terbaru = Rev. 467"
old = "revisi terbaru = Rev. 463"
new = "revisi terbaru = Rev. 467"
assert content.count(old) == 1, f"4d count={content.count(old)}"
content = content.replace(old, new)

# 4e. Line 761: HEAD hash
old = "HEAD `360cfb1f5864524570e622ed4d94a61c6e5950ef` (Rev. 463); seluruh file lain"
new = "HEAD `3a66337a205155138b85916b47828346e09340bd` (Rev. 467); seluruh file lain"
assert content.count(old) == 1, f"4e count={content.count(old)}"
content = content.replace(old, new)

# 4f. Line 770: "rev 463 = PRD fresh verification & stability confirmation"
old = "rev 463 = PRD fresh verification & stability confirmation"
new = "rev 467 = PRD fresh verification & stability confirmation"
assert content.count(old) == 1, f"4f count={content.count(old)}"
content = content.replace(old, new)

# 4g. Line 770: HEAD hash (in Status line)
old = "HEAD `360cfb1f5864524570e622ed4d94a61c6e5950ef` (Rev. 463), 0 / 0 (0 commit ahead origin_main)"
new = "HEAD `3a66337a205155138b85916b47828346e09340bd` (Rev. 467), 4 / 0 (4 commits ahead origin_main)"
assert content.count(old) == 1, f"4g count={content.count(old)}"
content = content.replace(old, new)

# 4h. Line 770: "dari Rev. 462 (data terkonsisten)" -> "dari Rev. 466 (data terkonsisten)"
old = "dari Rev. 462 (data terkonsisten)"
new = "dari Rev. 466 (data terkonsisten)"
assert content.count(old) == 1, f"4h count={content.count(old)}"
content = content.replace(old, new)

# 4i. §12: "0 / 0 (0 commit ahead origin_main)" -> "4 / 0 (4 commits ahead origin_main)" (in §12 only)
# This appears in line 760 (§12 Git HEAD bullet) and line 770 (§12 Status line)
# We want to change both, since they are both in §12.
old = "0 / 0 (0 commit ahead origin_main)"
new = "4 / 0 (4 commits ahead origin_main)"
# We'll replace all occurrences in the §12 section later, after the §12-specific replacements.

print("All §12 replacements done.")

# ===== 5. §11: add new entry for Rev. 467 =====
old = "## 11. REVISI TERBARU (Rev. 116–467 — 23 Oktober 2026 WIB)"
new = old + "\n\n    467. 23 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (23 Oct 2026 WIB); HEAD `3a66337a205155138b85916b47828346e09340bd` (Rev. 466: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 466, §11 kompakt changelog 116–465, §12 updated), 4 / 0 (4 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 466** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — node_modules absent; npm ci diperlukan. Database: dev.db absent; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia — import ulang menggunakan `init_db.py` & `init_schema.sql`. **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL (data ekspor NFC Tools belum tersedia). **Auth hardcode:** Login.tsx tetap pakai `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** Beranda.tsx & page.tsx masih hardcoded totalSantri 453. **Prisma schema:** KitabProgress & Sertakan sudah terdefinisi; uidNfc (baris 68) tetap ada. **Status:** dokeman PRD **REVISI** — rev 467 = PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 466; branch 4 ahead / 0 behind origin_main."
assert old in content, "§11 header not found for insert"
content = content.replace(old, new)

print("§11 entry added.")

# ===== 6. §13: change "Rev. 463" entry to "Rev. 467" =====
# Find the §13 Rev. 463 entry
old = "||- **Rev. 463.** 23 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (23 Oct 2026 WIB); HEAD `360cfb1f5864524570e622ed4d94a61c6e5950ef` (Rev. 463: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 463, §11 kompakt changelog 116–462, §12 updated), 0 / 0 (0 commit ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 462 (data terkonsisten)."
new = "||- **Rev. 467.** 23 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (23 Oct 2026 WIB); HEAD `3a66337a205155138b85916b47828346e09340bd` (Rev. 467: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 467, §11 kompakt changelog 116–466, §12 updated), 4 / 0 (4 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 466 (data terkonsisten). Build gate: NOT RE-RUNABLE — `node_modules/` absent; `npm ci` diperlukan. Database: dev.db absent; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia — import ulang menggunakan `init_db.py` & `init_schema.sql`. **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students`, semua 453 NULL (data ekspor NFC Tools belum tersedia). **Auth hardcode:** `src/components/Login.tsx` tetap pakai `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB). **Schema:** model `KitabProgress` (baris 203) & `Sertakan` (baris 218) sudah terdefinisi; `uidNfc` (baris 68) tetap ada. **Status:** dokeman PRD **REVISI** — rev 467 = PRD fresh verification & konfirmasi stabilitas; state stabil, tidak ada perubahan signifikan dari Rev. 466; branch 4 ahead / 0 behind origin_main."
assert old in content, "§13 Rev. 463 entry not found"
content = content.replace(old, new)

# ===== 7. §13: add new "Rev. 467" entry before the §13 Rev. 467 entry =====
old = "||- **Rev. 467.** 23 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (23 Oct 2026 WIB); HEAD `3a66337a205155138b85916b47828346e09340bd` (Rev. 467: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 467, §11 kompakt changelog 116–466, §12 updated), 4 / 0 (4 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 466 (data terkonsisten)."
new = old + " Build gate: NOT RE-RUNABLE — `node_modules/` absent; `npm ci` diperlukan. Database: dev.db absent; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia — import ulang menggunakan `init_db.py` & `init_schema.sql`. **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students`, semua 453 NULL (data ekspor NFC Tools belum tersedia). **Auth hardcode:** `src/components/Login.tsx` tetap pakai `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB). **Schema:** model `KitabProgress` (baris 203) & `Sertakan` (baris 218) sudah terdefinisi; `uidNfc` (baris 68) tetap ada. **Status:** dokeman PRD **REVISI** — rev 467 = PRD fresh verification & konfirmasi stabilitas; state stabil, tidak ada perubahan signifikan dari Rev. 466; branch 4 ahead / 0 behind origin_main."

# Find the position of the §13 Rev. 467 entry
pos = content.find(old)
assert pos != -1, "§13 Rev. 467 entry not found"
content = content[:pos] + new + content[pos:]

print("§13 updates done.")

# ===== 8. Write back =====
with io.open(dst, "w", encoding="utf-8") as f:
    f.write(content)

print(f"\nFile updated: {dst}")
print(f"Total lines: {content.count(chr(10)) + 1}")
