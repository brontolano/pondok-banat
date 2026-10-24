#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update PRD-PONDOK-BANAT.md to Rev. 468 — fresh verification & stability confirmation."""
import io

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# --- 1. Header update ---
old_h = "Rev. 467: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 467, §11 kompakt changelog 116–466, §12 updated"
new_h = "Rev. 468: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 468, §11 kompakt changelog 116–467, §12 updated"
assert old_h in content, "Header not found"
content = content.replace(old_h, new_h)
print("  Header updated to Rev. 468")

# --- 2. §11 header update ---
old_11h = "## 11. REVISI TERBARU (Rev. 116–467 — 23 Oktober 2026 WIB)"
new_11h = "## 11. REVISI TERBARU (Rev. 116–468 — 23 Oktober 2026 WIB)"
assert old_11h in content, "§11 header not found"
content = content.replace(old_11h, new_11h)
print("  §11 header updated to Rev. 116–468")

# --- 3. §12 header update ---
old_12h = "## 12. REVISI TERBARU (Rev. 467 — 23 Oktober 2026 WIB)"
new_12h = "## 12. REVISI TERBARU (Rev. 468 — 23 Oktober 2026 WIB)"
assert old_12h in content, "§12 header not found"
content = content.replace(old_12h, new_12h)
print("  §12 header updated to Rev. 468")

# --- 4. §12 content updates ---

# 4a: Line 761: "dari Rev. 466 (data terkonsisten)" -> "dari Rev. 467"
old_4a = "Tidak ada perubahan signifikan dari Rev. 466 (data terkonsisten)"
new_4a = "Tidak ada perubahan signifikan dari Rev. 467 (data terkonsisten)"
assert content.count(old_4a) == 1, f"4a count={content.count(old_4a)}"
content = content.replace(old_4a, new_4a)
print("  4a: updated 'dari Rev. 466' -> 'dari Rev. 467' in §12 intro")

# 4b: Line 763: HEAD hash + prefix
old_4b = "360cfb1f5864524570e622ed4d94a61c6e5950ef` (Rev. 463: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 467, §11 kompakt changelog 116–466, §12 updated). Local branch **4 commits ahead / 0 behind** origin_main"
new_4b = "fa1a12f2153eeb53e2512460de451b06e867a695` (Rev. 468: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 468, §11 kompakt changelog 116–467, §12 updated). Local branch **5 commits ahead / 0 behind** origin_main"
cnt_4b = content.count(old_4b)
print(f"  4b: replacing {cnt_4b} occurrence(s) of §12 Git HEAD bullet pattern")
assert cnt_4b == 1, f"4b count={cnt_4b}"
content = content.replace(old_4b, new_4b)

# 4c: Line 764: HEAD hash (Rev. 467) -> (Rev. 468)
old_4c = "HEAD `3a66337a205155138b85916b47828346e09340bd` (Rev. 467); seluruh file lain cocak dengan HEAD"
new_4c = "HEAD `fa1a12f2153eeb53e2512460de451b06e867a695` (Rev. 468); seluruh file lain cocak dengan HEAD"
cnt_4c = content.count(old_4c)
print(f"  4c: replacing {cnt_4c} occurrence(s) of HEAD hash (Rev. 467) in Working tree bullet")
assert cnt_4c == 1, f"4c count={cnt_4c}"
content = content.replace(old_4c, new_4c)

# 4d: Line 764: "revisi terbaru = Rev. 467" -> "revisi terbaru = Rev. 468"
old_4d = "revisi terbaru = Rev. 467"
new_4d = "revisi terbaru = Rev. 468"
assert content.count(old_4d) == 1, f"4d count={content.count(old_4d)}"
content = content.replace(old_4d, new_4d)
print("  4d: updated 'revisi terbaru = Rev. 467' -> 'Rev. 468'")

# 4e: Line 773: "rev 467 = PRD fresh verification" -> "rev 468"
old_4e = "rev 467 = PRD fresh verification & stability confirmation (23 Oct 2026 WIB); HEAD `3a66337a205155138b85916b47828346e09340bd` (Rev. 467), 4 / 0 (4 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 466 (data terkonsisten)."
new_4e = "rev 468 = PRD fresh verification & stability confirmation (23 Oct 2026 WIB); HEAD `fa1a12f2153eeb53e2512460de451b06e867a695` (Rev. 468), 5 / 0 (5 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 467 (data terkonsisten)."
cnt_4e = content.count(old_4e)
print(f"  4e: replacing {cnt_4e} occurrence(s) of §12 Status line pattern")
assert cnt_4e == 1, f"4e count={cnt_4e}"
content = content.replace(old_4e, new_4e)
print("  4e: updated §12 Status line to Rev. 468")

# --- 5. §13 reference table updates ---
# 5a: Change the "Rev. 467" entry to "Rev. 468" (the whole entry including Build gate)
old_5a = "||- **Rev. 467.** 23 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (23 Oct 2026 WIB); HEAD `3a66337a205155138b85916b47828346e09340bd` (Rev. 467: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 467, §11 kompakt changelog 116–466, §12 updated), 4 / 0 (4 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 462 (data terkonsisten). Build gate: NOT RE-RUNABLE — `node_modules/` absent; `npm ci` diperlukan. Database: dev.db absent; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia — import ulang menggunakan `init_db.py` & `init_schema.sql`. **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students`, semua 453 NULL (data ekspor NFC Tools belum tersedia). **Auth hardcode:** `src/components/Login.tsx` tetap pakai `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB). **Schema:** model `KitabProgress` (baris 203) & `Sertakan` (baris 218) sudah terdefinisi; `uidNfc` (baris 68) tetap ada. **Status:** dokeman PRD **REVISI** — rev 467 = PRD fresh verification & konfirmasi stabilitas; state stabil, tidak ada perubahan signifikan dari Rev. 466; branch 4 ahead / 0 behind origin_main."

new_5a = "||- **Rev. 468.** 23 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (23 Oct 2026 WIB); HEAD `fa1a12f2153eeb53e2512460de451b06e867a695` (Rev. 468: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 468, §11 kompakt changelog 116–467, §12 updated), 5 / 0 (5 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 467 (data terkonsisten). Build gate: NOT RE-RUNABLE — `node_modules/` absent; `npm ci` diperlukan. Database: dev.db absent; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia — import ulang menggunakan `init_db.py` & `init_schema.sql`. **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students`, semua 453 NULL (data ekspor NFC Tools belum tersedia). **Auth hardcode:** `src/components/Login.tsx` tetap pakai `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB). **Schema:** model `KitabProgress` (baris 203) & `Sertakan` (baris 218) sudah terdefinisi; `uidNfc` (baris 68) tetap ada. **Status:** dokeman PRD **REVISI** — rev 468 = PRD fresh verification & konfirmasi stabilitas; state stabil, tidak ada perubahan signifikan dari Rev. 467; branch 5 ahead / 0 behind origin_main."

cnt_5a = content.count(old_5a)
print(f"  5a: replacing {cnt_5a} occurrence(s) of §13 Rev. 467 entry")
assert cnt_5a == 1, f"5a count={cnt_5a}"
content = content.replace(old_5a, new_5a)
print("  5a: §13 Rev. 467 entry updated to Rev. 468")

# 5b: Add new "Rev. 468" entry before the §13 Rev. 468 entry
s13_marker = "||- **Rev. 468.** 23 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (23 Oct 2026 WIB); HEAD `fa1a12f2153eeb53e2512460de451b06e867a695` (Rev. 468: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 468, §11 kompakt changelog 116–467, §12 updated), 5 / 0 (5 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 467 (data terkonsisten)."

assert s13_marker in content, "§13 Rev. 468 marker not found"
insert_pos = content.find(s13_marker)

new_s13_468_dup = s13_marker + " Build gate: NOT RE-RUNABLE — `node_modules/` absent; `npm ci` diperlukan. Database: dev.db absent; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia — import ulang menggunakan `init_db.py` & `init_schema.sql`. **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students`, semua 453 NULL (data ekspor NFC Tools belum tersedia). **Auth hardcode:** `src/components/Login.tsx` tetap pakai `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB). **Schema:** model `KitabProgress` (baris 203) & `Sertakan` (baris 218) sudah terdefinisi; `uidNfc` (baris 68) tetap ada. **Status:** dokeman PRD **REVISI** — rev 468 = PRD fresh verification & konfirmasi stabilitas; state stabil, tidak ada perubahan signifikan dari Rev. 467; branch 5 ahead / 0 behind origin_main."

content = content[:insert_pos] + new_s13_468_dup + content[insert_pos:]
print("  5b: Added new §13 Rev. 468 entry")

# --- 6. §11: add new entry for Rev. 468 ---
old_6 = "## 11. REVISI TERBARU (Rev. 116–468 — 23 Oktober 2026 WIB)"
new_6 = old_6 + "\n\n    468. 23 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (23 Oct 2026 WIB); HEAD `fa1a12f2153eeb53e2512460de451b06e867a695` (Rev. 467: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 467, §11 kompakt changelog 116–466, §12 updated), 5 / 0 (5 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 467** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — node_modules absent; npm ci diperlukan. Database: dev.db absent; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia — import ulang menggunakan `init_db.py` & `init_schema.sql`. **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL (data ekspor NFC Tools belum tersedia). **Auth hardcode:** Login.tsx tetap pakai `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** Beranda.tsx & page.tsx masih hardcoded totalSantri 453. **Prisma schema:** KitabProgress & Sertakan sudah terdefinisi; uidNfc (baris 68) tetap ada. **Status:** dokeman PRD **REVISI** — rev 468 = PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 467; branch 5 ahead / 0 behind origin_main."

assert old_6 in content, "§11 header not found for insert"
content = content.replace(old_6, new_6)
print("  6: Added §11 entry for Rev. 468")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"\nFile updated: {path}")
print(f"Total lines: {content.count(chr(10)) + 1}")
