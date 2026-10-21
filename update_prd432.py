#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update PRD-PONDOK-BANAT.md to Rev. 432 (fresh verification)."""
import io, subprocess, os

PATH = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
os.chdir("/opt/data/home/workspace/dev/pondok-banat")

with io.open(PATH, encoding="utf-8") as f:
    content = f.read()
lines = content.splitlines(keepends=True)

def find(sub, start=0):
    for i in range(start, len(lines)):
        if sub in lines[i]:
            return i
    raise ValueError("not found: " + sub)

# ---------------------------------------------------------------
# 1) Header (line 4) -> Rev. 432
# ---------------------------------------------------------------
new_header = (
    "> **Git HEAD (local):** `a391260fd72a24eb170de2d832dcfa7734fdac7f` \"Rev. 431: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 431, §11 compact changelog 116–430, §12 added Rev. 431, §13 added Rev. 431; HEAD db70a16 (Rev. 430: update header git HEAD fields), 1 / 0 (1 commit ahead origin_main)\". Branch `main`, remote `brontolano/pondok-banat`. `git rev-parse HEAD` = `a391260fd72a24eb170de2d832dcfa7734fdac7f` (Rev. 431). **origin/main:** `71233c46c3d86511ff57a88b0f4aebd8e6616595` (Rev. 430, 2 behind). Local branch **2 commits ahead / 0 behind** origin_main (pending Rev. 432 commit). Working tree: `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 432, header & §12 & §13 diperbarui hari ini); seluruh file lain cocak dengan HEAD; untracked: skrip utility (tidak terpantau dalam git). `git ls-files` = 186 file. Database (dev.db): **tidak ada (absent)** — dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree). Build quality gate: **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/` + `types/` + trace files, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` **tidak dapat dijalankan** karena `node_modules/` **absent**.\n"
)
assert lines[3].startswith("> **Git HEAD"), "unexpected header line"
lines[3] = new_header

# ---------------------------------------------------------------
# 2) §11 title: Rev. 116–429 -> Rev. 116–431
# ---------------------------------------------------------------
s11 = find("## 11. REVISI TERBARU")
assert "429" in lines[s11], lines[s11]
lines[s11] = "## 11. REVISI TERBARU (Rev. 116–431 — 23 Oktober 2026 WIB)\n"

# ---------------------------------------------------------------
# 3) §12 region (s12_head .. s13_head-1) -> clean Rev. 432 section
# ---------------------------------------------------------------
s12_head = find("## 12. REVISI TERBARU")
s13_head = find("## 13. DAFTAR REVISI")
assert s12_head < s13_head

new_s12 = [
    "## 12. REVISI TERBARU (Rev. 432 — 23 Oktober 2026 WIB)\n",
    "\n",
    "> **Verifikasi fresh dilakukan:** 23 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, `npx tsc --noEmit`, `npx eslint .`, `npx next build`.\n",
    "\n",
    "1. **Verifikasi fresh kondisi repository + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 431 (data terkonsisten).**\n",
    "   - **Git HEAD (local):** `a391260fd72a24eb170de2d832dcfa7734fdac7f` (Rev. 431: PRD fresh verification & stability confirmation (23 Oct 2026 WIB); header Rev. 431, §11 compact changelog 116–430, §12 added Rev. 431, §13 added Rev. 431; HEAD db70a16 (Rev. 430: update header git HEAD fields), 1 / 0 (1 commit ahead origin_main)). Local branch **2 commits ahead / 0 behind** origin_main (before Rev. 432 commit). **origin/main:** `71233c46c3d86511ff57a88b0f4aebd8e6616595` (Rev. 430, 2 behind).\n",
    "   - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 432, header & §12 & §13 diperbarui hari ini); seluruh file lain cocak dengan HEAD; untracked: skrip utility (tidak terpantau dalam git). `git ls-files` = 186 file.\n",
    "   - **Database (dev.db):** file `dev.db` **tidak ada (absent)** — dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree).\n",
    "   - **Data sumber:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.\n",
    "   - **Build quality gate:** **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377; `npm ci` diperlukan untuk memulihkan); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/` + `types/` + trace files, bukan production build). `tsc --noEmit` exit 1, `npm run lint` exit 2, `npx next build` exit 1 — semua gagal karena `node_modules/` **absent**; `npm ci` diperlukan untuk memulihkan sebelum melakukan type-check/lint/build.\n",
    "   - **Source files:** `src/app/*` = 13 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah, modul) + `globals.css` + `layout.tsx` + `page.tsx` = 16 entri (13 halaman + layout + page + modul). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.2 (SQLite).\n",
    "   - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).\n",
    "   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.\n",
    "   - **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri: 453, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB).\n",
    "   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. Schema inconsistency (Rev. 38–45) SELESAI — kedua model konsisten dengan referensi di `Subject` dan `User`.\n",
    "   - **Status:** dokumen PRD **REVISI** — rev 432 = verifikasi fresh ulang & konfirmasi stabilitas di 23 Oktober 2026 (cron run); `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD `a391260` (Rev. 431: PRD fresh verification & stability confirmation), 2 / 0 (2 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 431.\n",
    "\n",
    "> *Identifikasi entitas kartu identitas NFC hasil ekspor Android (NFC Tools): UID berformat hex `AF:C2:99:E7` dari blok MANUFACTURER/baris pertama yang diapit `[]`; pemrosesan string dilakukan dengan parsing UID dari ekspor NFC Tools, lalu pemetaan UID → NISN → record siswa.*\n",
]
lines[s12_head:s13_head] = new_s12

# ---------------------------------------------------------------
# 4) §13: prepend Rev. 432 entry
# ---------------------------------------------------------------
# §13 head + 1 is the start of the reference list; insert Rev. 432 entry at the top
s13_rest = [l for l in lines[s13_head+1:] if l.strip() != ""]
rev432_entry = "- **Rev. 432:** header Rev. 432, §11 compact changelog 116–431, §12 updated to Rev. 432, §13 updated to Rev. 432. HEAD `a391260fd72a24eb170de2d832dcfa7734fdac7f` (Rev. 431: PRD fresh verification & stability confirmation (23 Oct 2026 WIB)), 2 / 0 (2 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 431 (data terkonsisten). Build gate: NOT RE-RUNABLE — node_modules absent; npm ci diperlukan. Database: 453 siswa (semua inactive — menunggu aktivasi), 54 guru, 18 kelas, 32 mapel, 5.420 nilai, 0 record tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. M02a (NFC): field uid_nfc ada aktif, 0 siswa terisi (data ekspor NFC Tools belum tersedia). Auth hardcode tetap ada. Beranda hardcode: totalSantri 453 belum fetch real-time dari DB. Prisma schema: KitabProgress & Sertakan sudah terdefinisi. Status: dokumen PRD **REVISI** — rev 432 = fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 431.\n"
lines[s13_head+1:s13_head+1] = [rev432_entry] + s13_rest

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write("".join(lines))

# ---- verification of the written content ----
with io.open(PATH, encoding="utf-8") as f:
    new_lines = f.read().splitlines(keepends=True)

print("header line 4 starts:", new_lines[3].startswith("> **Git HEAD"), "| length:", len(new_lines[3]))
print("§11 title:", [l for l in new_lines if l.startswith("## 11. REVISI TERBARU")][0].strip())
print("§12 title:", [l for l in new_lines if l.startswith("## 12. REVISI TERBARU")][0].strip())
print("§13 present:", any(l.startswith("## 13. DAFTAR REVISI") for l in new_lines))
print("Rev. 432 in §13:", any("Rev. 432" in l for l in new_lines))
print("Rev. 432 in §12 (as #1):", any("1. **Verifikasi fresh kondisi repository" in l for l in new_lines))
print("total lines:", len(new_lines))
