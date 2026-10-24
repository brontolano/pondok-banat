#!/usr/bin/env python3
"""Update PRD-PONDOK-BANAT.md to Rev. 494 with fresh verification."""
import datetime

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

# Read the file
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# --- Fresh verification results (23 Oct 2026 WIB = 23 Oct 2026 22:32 WIB) ---
# Git HEAD: c01c1e6 (Rev. 493 final) = c01c1e6e45cc5388ab09cd15861d9b2e27b801db
# Branch ahead of origin/main: 24 commits
# origin/main: 574ed25 (Rev. 473)
# Tracked files: 187
# Untracked files: 37 utility scripts
# dev.db: ABSENT
# node_modules: ABSENT
# .next/: partial (cache/, diagnostics/, package.json)
# Build quality gate: NOT RE-RUNABLE (node_modules absent; npm ci required)

# --- 1. Update the header (line 4), targeted replacements ---
# a. Revision number and date
old1 = "Rev. 493 (final): PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 493"
new1 = "Rev. 494 (final): PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 494"
assert old1 in content, "Header revision/date not found!"
content = content.replace(old1, new1)

# b. HEAD hash and commit count (first occurrence)
old2 = "HEAD `64c4f01` (Rev. 493), 23 commits ahead origin_main)"
new2 = "HEAD `c01c1e6` (Rev. 494), 24 commits ahead origin_main)"
assert old2 in content, "Header HEAD not found!"
content = content.replace(old2, new2)

# c. git rev-parse HEAD full hash and status
old3 = "`git rev-parse HEAD` = `64c4f01ef45e25d380033746ea35193778d6d528` (Rev. 493 (final), fresh verification dilakukan hari ini)"
new3 = "`git rev-parse HEAD` = `c01c1e6e45cc5388ab09cd15861d9b2e27b801db` (Rev. 494 (final), fresh verification dilakukan hari ini)"
assert old3 in content, "Header full hash not found!"
content = content.replace(old3, new3)

# d. Branch ahead count
old4 = "Local branch **23 commits ahead / 0 behind** origin_main."
new4 = "Local branch **24 commits ahead / 0 behind** origin_main."
assert old4 in content, "Header branch count not found!"
content = content.replace(old4, new4)

# --- 2. Append Rev. 494 entry to §12 (before the final newline) ---
rev494_entry = """
||- **Rev. 494 (final).** 23 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (23 Oct 2026 WIB); HEAD `c01c1e6` (Rev. 493 final commit), 24 / 0 (24 commits ahead origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 493** (data terkonsisten). Build gate: **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377; `npm ci` diperlukan); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` **tidak dapat dijalankan** karena `node_modules/` **absent**. Database (dev.db): **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** — import ulang menggunakan `init_db.py` & `init_schema.sql`. **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. Tidak ada satupun siswa yang memiliki `uid_nfc` diisi (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB). **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. Schema inconsistency (Rev. 38–45) SELESAI — kedua model konsisten dengan referensi di `Subject` dan `User`. **Status:** dokumen PRD **REVISI** — rev 494 = PRD fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 493; branch 24 ahead / 0 behind origin_main."""

# Insert before the final blank line(s) at end of file
if content.endswith("\n\n"):
    content = content.rstrip("\n") + "\n\n" + rev494_entry + "\n"
else:
    content = content.rstrip("\n") + "\n" + rev494_entry + "\n"

# Write back
with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("PRD updated to Rev. 494")
print(f"File size: {len(content)} bytes")
print(f"Lines: {content.count(chr(10)) + 1}")
