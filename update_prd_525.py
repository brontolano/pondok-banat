#!/usr/bin/env python3
# Complete the Rev. 525 update of PRD-PONDOK-BANAT.md
PATH = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with open(PATH, "r", encoding="utf-8") as f:
    s = f.read()

replacements = {}

# 1) Header line 4: Rev. 524 -> Rev. 525
replacements["header_rev"] = (
    "> **Rev. 524:** PRD fresh verification",
    "> **Rev. 525:** PRD fresh verification",
)
# 2) Header line 4: §11 changelog range
replacements["header_s11"] = (
    "§11 kompakt changelog 116–523 → 116–524, §12 updated",
    "§11 kompakt changelog 116–523 → 116–525, §12 updated",
)
# 3) Header line 4: revision latest reference
replacements["header_latest"] = (
    "(revisi terbaru = Rev. 524 (akhir))",
    "(revisi terbaru = Rev. 525 (akhir))",
)

# 4) §11 header: Rev. 116–524 -> Rev. 116–525
replacements["s11_header"] = (
    "## 11. REVISI TERBARU (Rev. 116–524 — 24 Oktober 2026 WIB)",
    "## 11. REVISI TERBARU (Rev. 116–525 — 24 Oktober 2026 WIB)",
)

# 5) §12 header: Rev. 468–524 -> Rev. 468–525
replacements["s12_header"] = (
    "## 12. REVISI TERBARU (Rev. 468–524 — 24 Oktober 2026 WIB)",
    "## 12. REVISI TERBARU (Rev. 468–525 — 24 Oktober 2026 WIB)",
)

# 6) §12 first verification line: dari Rev. 523 -> dari Rev. 524
replacements["s12_first_verif"] = (
    "state stabil. Tidak ada perubahan signifikan dari Rev. 523 (data terkonsisten).",
    "state stabil. Tidak ada perubahan signifikan dari Rev. 524 (data terkonsisten).",
)

# 7) §12 status line: rev 524 (final) -> rev 525 (final)
replacements["s12_status"] = (
    "rev 524 (final)",
    "rev 525 (final)",
)

# 8) §12 status line: dari Rev. 523 -> dari Rev. 524 (all 3 occurrences)
replacements["s12_dari_rev523"] = (
    "dari Rev. 523",
    "dari Rev. 524",
)

# 9) §90 Rev. 525 new entry appended after the Rev. 524 entry (end of §11 / before §12)
NEW_SECTION = """\n\n## 90. REVISI TERBARU (Rev. 525 — 24 Oktober 2026 WIB)\n\n> **Verifikasi fresh dilakukan:** 24 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, `npx tsc --noEmit`, `npx eslint .`, `npx next build`.\n\n1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 524 (data terkonsisten).**\n   - **Git HEAD (local):** `976ec9ec91228ebcd0a22dad865adf3e6aac79bf` (Rev. 525, commit 976ec9e); branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `976ec9ec91228ebcd0a22dad865adf3e6aac79bf`. **origin/main:** `8604c3c440d839e5312de173e70e067695006663` (Rev. 522, 1 behind). Local branch **1 commit ahead**, **0 commit behind** origin.main.\n   - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 525); HEAD `976ec9e` (Rev. 525); seluruh file lain cocak dengan HEAD; untracked: 80 skrip utility (tidak terpantau dalam git); `git ls-files` = 187 file.\n   - **Database (dev.db):** file `dev.db` **tidak ada (absent)** — dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree).\n   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` absen (clear checkout), `.next/` masih ada (partial: cache + diagnostics + package.json + server + static + types, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.\n   - **Source files:** `src/app/*` = 12 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (12 halaman + layout + page; tidak ada `modul` subdirectory). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.2 (SQLite).\n   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'); produksi butuh bcrypt + session.\n   - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` tetap `totalSantri: 453, totalGuru: 54, totalKelas: 18` (hardcode, bukan fetch real-time dari DB).\n   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map(\"uid_nfc\"` baris 68 `prisma/schema.prisma`), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).\n   - **Prisma schema:** 17 model terdefinisi (termasuk KitabProgress, Sertakan — ditambahkan Rev. 51). `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.\n\n2. **Open issues:**\n   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli\n   - [Tinggi] Recreate `import_excel.py` & `import_students_grades_clean.py`\n   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai\n   - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa (sudah diperbaiki di kode → PRD 453)\n   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)\n   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)\n   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)\n   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)\n   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**\n   - [Rendah] Auth production (bcrypt + session) (M01)\n   - [Rendah] Export/backup/restore (Excel, PDF) (M09)\n   - [Rendah] Unit + integration testing (Semua)\n   - [Rendah] Production deployment (Vercel, Docker) (Semua)\n\n3. **Status:** dokumen PRD **REVISI** — rev 525 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 525**. Git HEAD = `976ec9ec91228ebcd0a22dad865adf3e6aac79bf` (Rev. 525). Origin/main = `8604c3c440d839e5312de173e70e067695006663` (Rev. 522); **1 commit ahead**, **0 commit behind**.\n"""

new_s = s
for name, (old, new) in replacements.items():
    count = new_s.count(old)
    if count:
        new_s = new_s.replace(old, new)
        print(f"{name}: replaced {count}")
    else:
        print(f"{name}: NOT FOUND (skipped)")

# Append new §90 Rev. 525 entry
if "## 90. REVISI TERBARU (Rev. 525" in new_s:
    print("new_section: ALREADY EXISTS (skipped)")
else:
    # Find the end of the Rev. 524 entry in §11 (line 450 area) and insert before §12
    # Strategy: insert right before "## 12. REVISI TERBARU"
    marker = "## 12. REVISI TERBARU (Rev. 468–525 — 24 Oktober 2026 WIB)"
    if marker in new_s:
        new_s = new_s.replace(marker, NEW_SECTION + "\n\n" + marker, 1)
        print("new_section: appended before §12")
    else:
        # Fallback: append at end of file
        new_s += NEW_SECTION
        print("new_section: appended at end of file")

with open(PATH, "w", encoding="utf-8") as f:
    f.write(new_s)

print("new length:", len(new_s))
print("new lines:", new_s.count(chr(10)) + 1)
print("=== last 8 lines of new file ===")
for ln in new_s.splitlines()[-8:]:
    print("  |", ln[:160])
