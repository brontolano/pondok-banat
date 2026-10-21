#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update PRD-PONDOK-BANAT.md to a clean Rev. 415 state."""
import io
import subprocess

PATH = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with io.open(PATH, encoding="utf-8") as f:
    lines = f.read().splitlines(keepends=True)

def find(sub, start=0):
    for i in range(start, len(lines)):
        if sub in lines[i]:
            return i
    raise ValueError("not found: " + sub)

# Capture ALL section boundaries BEFORE any mutation
s11_head = find("## 11. REVISI TERBARU")
s12_head = find("## 12. REVISI TERBARU (Rev. 380")
s13_head = find("## 13. DAFTAR REVISI (REFERENSI)")

# 1) Header (line 3)
new_header = (
    "> **Sumber:** `IDEA.md` + `.data-pondokanat/` (3 Excel + 74 dokumen = 65 RPP + 9 SILABUS) + research.\n"
    "> **Git HEAD (local):** `a564301aabf15540ffb295557a0f84a68b179b11` \"Rev. 415: PRD fresh verification & stability confirmation (21 Oct 2026 WIB); header Rev. 415, §11 compact changelog 116–414, §12 updated, §13 updated to Rev. 415\". Branch `main`, remote `brontolano/pondok-banat`. `git rev-parse HEAD` = `a564301aabf15540ffb295557a0f84a68b179b11`. **origin/main:** `1c4b8bd122332bfe269419a4a9286bb43ef27e94` (Rev. 396). Local branch **20 ahead / 0 behind** origin_main. Working tree: `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 415, §12 updated); seluruh file lain cocak dengan HEAD; untracked: skrip utility (tidak terpantau dalam git). `git ls-files` = 152 file. Database (dev.db): **tidak ada (absent)** — dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree). Build quality gate: **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/` + `types/` + trace files, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` **tidak dapat dijalankan** karena `node_modules/` **absent**.\n"
)
lines[3] = new_header

# 2) §11 title
lines[s11_head] = "## 11. REVISI TERBARU (Rev. 116–414 — 21 Oktober 2026 WIB)\n"

# 3) §12 region (s12_head .. s13_head-1) -> clean single Rev. 415 section
new_s12 = [
    "## 12. REVISI TERBARU (Rev. 415 — 21 Oktober 2026 WIB)\n",
    "\n",
    "> **Verifikasi fresh dilakukan:** 21 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, `npx tsc --noEmit`, `npx eslint .`, `npx next build`.\n",
    "\n",
    "1. **Verifikasi fresh kondisi repository + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 414 (data terkonsisten).**\n",
    "   - **Git HEAD (local):** `a564301aabf15540ffb295557a0f84a68b179b11` (Rev. 415: PRD fresh verification & stability confirmation (21 Oct 2026 WIB); header Rev. 415, §11 compact changelog 116–414, §12 updated, §13 updated to Rev. 415; HEAD 63facea (Rev. 414), 20 / 0 (20 commits ahead origin_main)).\n",
    "   - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 415 — lihat §13); seluruh file lain cocak dengan HEAD; untracked: skrip utility (tidak terpantau dalam git). `git ls-files` = 152 file.\n",
    "   - **Database (dev.db):** file `dev.db` **tidak ada (absent)** — dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree).\n",
    "   - **Data sumber:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.\n",
    "   - **Build quality gate:** **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377; `npm ci` diperlukan untuk memulihkan); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/` + `types/` + trace files, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` **tidak dapat dijalankan** karena `node_modules/` **absent**; `npm ci` diperlukan untuk memulihkan sebelum melakukan type-check/lint/build.\n",
    "   - **Source files:** `src/app/*` = 13 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah, modul) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (13 halaman + layout + page). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.2 (SQLite).\n",
    "   - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).\n",
    "   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.\n",
    "   - **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri: 453, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB).\n",
    "   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. Schema inconsistency (Rev. 38–45) SELESAI — kedua model konsisten dengan referensi di `Subject` dan `User`.\n",
    "   - **Status:** dokumen PRD **REVISI** — rev 415 = verifikasi fresh ulang & konfirmasi stabilitas di 21 Oktober 2026 (cron run); `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD `a564301` (Rev. 415: PRD fresh verification & stability confirmation), 20 / 0 (20 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 414.\n",
    "\n",
    "> *Identifikasi entitas kartu identitas NFC hasil ekspor Android (NFC Tools): UID berformat hex `AF:C2:99:E7` dari blok MANUFACTURER/baris pertama yang diapit `[]`; pemrosesan string dilakukan dengan parsing UID dari ekspor NFC Tools, lalu pemetaan UID → NISN → record siswa.*\n",
]
# Replace the §12 region (exclusive of §13 heading)
lines[s12_head:s13_head] = new_s12

# 4) §13: prepend Rev. 415 entry (s13_head still valid — §13 not yet modified)
s13_rest = [l for l in lines[s13_head+1:] if l.strip() != ""]
rev415_entry = "- **Rev. 415:** header Rev. 415, §11 compact changelog 116–414, §12 updated, §13 updated to Rev. 415. HEAD `a564301` (Rev. 415: PRD fresh verification & stability confirmation (21 Oct 2026 WIB)), 20 / 0 (20 commits ahead origin_main).\n"
lines[s13_head+1:s13_head+1] = [rev415_entry] + s13_rest

with io.open(PATH, "w", encoding="utf-8") as f:
    f.write("".join(lines))

print("=== CHECKS ===")
assert "Rev. 415" in lines[3] and "116–414" in lines[3] and "20 / 0" in lines[3]
print("header: OK (Rev. 415, changelog 116–414, 20 ahead)")
assert "Rev. 116–414" in lines[s11_head]
print("§11 title: OK (Rev. 116–414)")
assert "## 12. REVISI TERBARU (Rev. 415" in lines[s12_head]
print("§12 heading: OK (single Rev. 415 section)")
cnt = int(subprocess.run(["grep","-c","## 12. REVISI TERBARU",PATH],capture_output=True,text=True).stdout)
print("§12 occurrences: %d (was 29)" % cnt)
assert any("Rev. 415" in l for l in lines[s13_head+1:])
print("§13 Rev. 415 entry: OK")
print("lines: %d" % len(lines))
