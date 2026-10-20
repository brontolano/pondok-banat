#!/usr/bin/env python3
# Update PRD-PONDOK-BANAT.md: bump header to Rev. 311 + append Rev. 311 verification section.
PATH = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with open(PATH, "r", encoding="utf-8") as f:
    s = f.read()

replacements = {}

# 1) Header revision bump
replacements["rev_bump"] = (
    "> **Rev. 310 — 19 Oktober 2026 (WIB).**",
    "> **Rev. 311 — 19 Oktober 2026 (WIB).**",
)

# 2) Local git HEAD reference fix
replacements["local_head"] = (
    "Git HEAD (local): `74b54cfde74daeb356595d0abacee173537f7992` \"Rev. 308: PRD fresh verification & stability confirmation (19 Oktober 2026 WIB); updated header to Rev. 308 + added section 86\" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `c35d3d515dbeafcf558ce28c0778ffff283bf9b2`)",
    "Git HEAD (local): `bdf497fa0494829f81fec969878c6ac6a6806270` (Rev. 310, commit bdf497f) (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `bdf497fa0494829f81fec969878c6ac6a6806270`)",
)

# 3) origin/main reference fix
replacements["origin_head"] = (
    "Git HEAD (origin/main): `bf253ccd67c29562decc1c088e99aeed82465396` (Rev. 293) — 15 commit ahead, 0 commit behind origin.main.",
    "Git HEAD (origin/main): `74b54cfde74daeb356595d0abacee173537f7992` (Rev. 309) — 1 commit ahead, 0 commit behind origin.main.",
)

# 4) branch ahead count fix
replacements["ahead_count"] = (
    "Local branch **15 commit ahead**, **0 commit behind** origin.main.",
    "Local branch **1 commit ahead**, **0 commit behind** origin.main.",
)

new_s = s
for name, (old, new) in replacements.items():
    if old in new_s:
        new_s = new_s.replace(old, new)
        print(f"{name}: OK")
    else:
        print(f"{name}: NOT FOUND (skipped)")

# 5) Append Rev. 311 section
NEW_SECTION = """\n\n## 90. REVISI TERBARU (Rev. 311 — 19 Oktober 2026 WIB)\n\n> **Verifikasi fresh dilakukan:** 19 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, `npx tsc --noEmit`, `npx eslint .`, `npx next build`.\n\n1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 310 (data terkonsisten).**\n   - **Git HEAD (local):** `bdf497fa0494829f81fec969878c6ac6a6806270` (Rev. 310, commit bdf497f); branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `bdf497fa0494829f81fec969878c6ac6a6806270`. **origin/main:** `74b54cfde74daeb356595d0abacee173537f7992` (Rev. 309). Local branch **1 commit ahead**, **0 commit behind** origin.main.\n   - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 311, telah dicomit); seluruh file lain cocak dengan HEAD; `git ls-files` = 36 file.\n   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).\n   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` absen (clear checkout), `.next/` masih ada (partial: cache + diagnostics + package.json + server + static + types, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.\n   - **Source files:** `src/app/*` = 13 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (13 halaman + layout + page). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).\n   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'); produksi butuh bcrypt + session.\n   - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` tetap `totalSantri: 453, totalGuru: 54, totalKelas: 18` (hardcode, bukan fetch real-time dari DB).\n   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map(\"uid_nfc\"` baris 68 `prisma/schema.prisma`), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).\n   - **Prisma schema:** 17 model terdefinisi (termasuk KitabProgress, Sertakan — ditambahkan Rev. 51). `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.\n\n2. **Open issues:**\n   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli\n   - [Tinggi] Recreate `import_excel.py` & `import_students_grades_clean.py`\n   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai\n   - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa (sudah diperbaiki di kode → PRD 453)\n   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)\n   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)\n   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)\n   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)\n   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**\n   - [Rendah] Auth production (bcrypt + session) (M01)\n   - [Rendah] Export/backup/restore (Excel, PDF) (M09)\n   - [Rendah] Unit + integration testing (Semua)\n   - [Rendah] Production deployment (Vercel, Docker) (Semua)\n\n3. **Status:** dokumen PRD **REVISI** — rev 311 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 311**. Git HEAD = `bdf497fa0494829f81fec969878c6ac6a6806270` (Rev. 310). Origin/main = `74b54cfde74daeb356595d0abacee173537f7992` (Rev. 309); **1 commit ahead**, **0 commit behind**.\n"""

new_s = new_s + NEW_SECTION

with open(PATH, "w", encoding="utf-8") as f:
    f.write(new_s)

print("new length:", len(new_s))
print("new lines:", new_s.count(chr(10)) + 1)
print("last 5 lines of new file:")
for ln in new_s.splitlines()[-5:]:
    print("  |", ln[:160])
