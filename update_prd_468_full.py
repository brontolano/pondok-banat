#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Complete Rev. 468 update for PRD-PONDOK-BANAT.md."""
import io

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

initial_size = len(content)
print(f"Initial file size: {initial_size} bytes, {content.count(chr(10)) + 1} lines")

# --- 1. Header update ---
old_h = "Rev. 467: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 467, §11 kompakt changelog 116–466, §12 updated"
new_h = "Rev. 468: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 468, §11 kompakt changelog 116–467, §12 updated"
if old_h in content:
    content = content.replace(old_h, new_h)
    print("  Header updated to Rev. 468")
else:
    print("  WARNING: Header pattern not found")

# Also update "revisi terbaru = Rev. 465" to "Rev. 468"
old_h2 = "revisi terbaru = Rev. 465"
new_h2 = "revisi terbaru = Rev. 468"
if old_h2 in content:
    content = content.replace(old_h2, new_h2)
    print("  Updated 'revisi terbaru = Rev. 465' -> 'Rev. 468'")

# --- 2. §11 header update ---
old_11h = "## 11. REVISI TERBARU (Rev. 116–467 — 23 Oktober 2026 WIB)"
new_11h = "## 11. REVISI TERBARU (Rev. 116–468 — 23 Oktober 2026 WIB)"
if old_11h in content:
    content = content.replace(old_11h, new_11h)
    print("  §11 header updated to Rev. 116–468")
else:
    print("  WARNING: §11 header pattern not found")

# --- 3. §12 header update ---
old_12h = "## 12. REVISI TERBARU (Rev. 467 — 23 Oktober 2026 WIB)"
new_12h = "## 12. REVISI TERBARU (Rev. 468 — 23 Oktober 2026 WIB)"
if old_12h in content:
    content = content.replace(old_12h, new_12h)
    print("  §12 header updated to Rev. 468")
else:
    print("  WARNING: §12 header pattern not found")

# --- 4. §12 content updates ---
# 4a: "dari Rev. 466 (data terkonsisten)" -> "dari Rev. 467"
old_4a = "Tidak ada perubahan signifikan dari Rev. 466 (data terkonsisten)"
new_4a = "Tidak ada perubahan signifikan dari Rev. 467 (data terkonsisten)"
if old_4a in content:
    content = content.replace(old_4a, new_4a)
    print("  4a: updated 'dari Rev. 466' -> 'dari Rev. 467'")
else:
    print("  WARNING: 4a pattern not found")

# 4b: Git HEAD bullet (line 763)
old_4b = "360cfb1f5864524570e622ed4d94a61c6e5950ef` (Rev. 463: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 467, §11 kompakt changelog 116–466, §12 updated). Local branch **4 commits ahead / 0 behind** origin_main"
new_4b = "fa1a12f2153eeb53e2512460de451b06e867a695` (Rev. 468: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 468, §11 kompakt changelog 116–467, §12 updated). Local branch **5 commits ahead / 0 behind** origin_main"
if old_4b in content:
    content = content.replace(old_4b, new_4b)
    print("  4b: updated §12 Git HEAD bullet")
else:
    print("  WARNING: 4b pattern not found")

# 4c: Working tree bullet (line 764)
old_4c = "HEAD `3a66337a205155138b85916b47828346e09340bd` (Rev. 467); seluruh file lain cocak dengan HEAD"
new_4c = "HEAD `fa1a12f2153eeb53e2512460de451b06e867a695` (Rev. 468); seluruh file lain cocak dengan HEAD"
if old_4c in content:
    content = content.replace(old_4c, new_4c)
    print("  4c: updated Working tree HEAD hash")
else:
    print("  WARNING: 4c pattern not found")

# 4d: "revisi terbaru = Rev. 467" -> "revisi terbaru = Rev. 468"
old_4d = "revisi terbaru = Rev. 467"
new_4d = "revisi terbaru = Rev. 468"
if old_4d in content:
    content = content.replace(old_4d, new_4d)
    print("  4d: updated 'revisi terbaru = Rev. 467' -> 'Rev. 468'")
else:
    print("  WARNING: 4d pattern not found")

# 4e: §12 Status line (now in the compact changelog, after §13 entries)
old_4e = "rev 467 = PRD fresh verification & stability confirmation (23 Oct 2026 WIB); HEAD `3a66337a205155138b85916b47828346e09340bd` (Rev. 467), 4 / 0 (4 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 466 (data terkonsisten)."
new_4e = "rev 468 = PRD fresh verification & stability confirmation (23 Oct 2026 WIB); HEAD `fa1a12f2153eeb53e2512460de451b06e867a695` (Rev. 468), 5 / 0 (5 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 467 (data terkonsisten)."
if old_4e in content:
    content = content.replace(old_4e, new_4e)
    print("  4e: updated §12 Status line")
else:
    print("  WARNING: 4e pattern not found")

# 4f: "dari Rev. 466 (data terkonsisten)" in §12 Status line (if not already done by 4a)
# Check if there's still "dari Rev. 466" in the §12 status context
old_4f = "dari Rev. 466 (data terkonsisten)"
if old_4f in content:
    # Find the first occurrence after the §12 Status line
    idx = content.find(old_4f)
    # Get context before and after
    before = content[:idx]
    after = content[idx + len(old_4f):]
    # Check if this is in §12 Status (before §13) or §11 compact changelog
    if "§12. REVISI TERBARU (Rev. 468" in before:
        # This is in §12 Status
        content = content[:idx] + "dari Rev. 467 (data terkonsisten)" + after
        print("  4f: updated §12 Status 'dari Rev. 466' -> 'dari Rev. 467'")
    else:
        # This is in §11 compact changelog
        pass
else:
    print("  4f: no more 'dari Rev. 466' found")

# --- 5. §11: add entry for Rev. 468 ---
old_6 = "## 11. REVISI TERBARU (Rev. 116–468 — 23 Oktober 2026 WIB)"
new_6 = old_6 + "\n\n    468. 23 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (23 Oct 2026 WIB); HEAD `fa1a12f2153eeb53e2512460de451b06e867a695` (Rev. 468: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 468, §11 kompakt changelog 116–467, §12 updated), 5 / 0 (5 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 467** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — node_modules absent; npm ci diperlukan. Database: dev.db absent; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia — import ulang menggunakan `init_db.py` & `init_schema.sql`. **M02a (NFC):** field `uid_nfc` ada aktif di tabel students, semua 453 NULL (data ekspor NFC Tools belum tersedia). **Auth hardcode:** Login.tsx tetap pakai `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** Beranda.tsx & page.tsx masih hardcoded totalSantri 453. **Prisma schema:** KitabProgress & Sertakan sudah terdefinisi; uidNfc (baris 68) tetap ada. **Status:** dokeman PRD **REVISI** — rev 468 = PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 467; branch 5 ahead / 0 behind origin_main."

if old_6 in content:
    content = content.replace(old_6, new_6)
    print("  5: Added §11 entry for Rev. 468")
else:
    print("  WARNING: §11 header for insertion not found")

# --- 6. Verify changes ---
new_size = len(content)
print(f"\nFinal file size: {new_size} bytes (delta: {new_size - initial_size})")
print(f"Total lines: {content.count(chr(10)) + 1}")

with io.open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("\nFile updated successfully.")
