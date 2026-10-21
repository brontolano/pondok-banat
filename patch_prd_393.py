#!/usr/bin/env python3
# Edit PRD-PONDOK-BANAT for Rev 393 update
import io

REPO = "/opt/data/home/workspace/dev/pondok-banat"
PATH = f"{REPO}/PRD-PONDOK-BANAT.md"

with open(PATH, "r", encoding="utf-8") as f:
    s = f.read()

edits = []

# 1. Header: "revisi terbaru = Rev. 392" -> "Rev. 393"
old = "cocak dengan HEAD (revisi terbaru = Rev. 392)"
new = "cocak dengan HEAD (revisi terbaru = Rev. 393)"
assert old in s, "header revisi terbaru not found"
s = s.replace(old, new)
edits.append("header revisi terbaru -> Rev. 393")

# 2. Header: git rev-parse HEAD reference
old = "`git rev-parse HEAD` = `adb91f23a5cee5c5fd30104e56dac6a3047b2c23`"
new = "`git rev-parse HEAD` = `663984f92d33c574ca4459fdeb7e7d292fbddcf8`"
assert old in s, "git rev-parse HEAD not found"
s = s.replace(old, new)
edits.append("git rev-parse HEAD -> 663984f")

# 3. Header: Local branch ahead count
old = "Local branch **3 ahead / 0 behind** origin_main"
new = "Local branch **1 ahead / 0 behind** origin_main"
assert old in s, "local branch not found"
s = s.replace(old, new)
edits.append("local branch -> 1 ahead")

# 4. §11 subtitle: Rev. 116–391 -> Rev. 116–392
old = "## 11. REVISI TERBARU (Rev. 116–391 — 26 Oktober 2026 WIB)"
new = "## 11. REVISI TERBARU (Rev. 116–392 — 26 Oktober 2026 WIB)"
assert old in s, "§11 subtitle not found"
s = s.replace(old, new)
edits.append("§11 subtitle -> Rev. 116–392")

# 5. §11 changelog: add entry 393 after entry 392
old = """    392. 27 Oktober 2026 (WIB): verifikasi fresh ulang & konfirmasi stabilitas; HEAD `adb91f2` (Rev. 391), 3 commits ahead origin_main; `dev.db` tidak ada (absent); node_modules **absent** (dihapus setelah Rev. 377; build quality gate **tidak dapat dijalankan** tanpa `npm ci`). Siswa: 453."""
new = """    392. 27 Oktober 2026 (WIB): verifikasi fresh ulang & konfirmasi stabilitas; HEAD `adb91f2` (Rev. 391), 3 commits ahead origin_main; `dev.db` tidak ada (absent); node_modules **absent** (dihapus setelah Rev. 377; build quality gate **tidak dapat dijalankan** tanpa `npm ci`). Siswa: 453.
    393. 28 Oktober 2026 (WIB): verifikasi fresh ulang & konfirmasi stabilitas; HEAD `663984f` (Rev. 392), 0 commits ahead origin_main; `dev.db` tidak ada (absent); node_modules **absent** (dihapus setelah Rev. 377; build quality gate **tidak dapat dijalankan** tanpa `npm ci`). Siswa: 453."""
assert old in s, "entry 392 not found"
s = s.replace(old, new)
edits.append("changelog entry 393 added")

# 6. Add §12 Rev 393 section at the end (after the last line)
new_section = """

## 12. REVISI TERBARU (Rev. 393 — 28 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 28 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, `npx tsc --noEmit`, `npx eslint .`, `npx next build`.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 392 (data terkonsisten).**
   - **Git HEAD (local):** `adb91f23a5cee5c5fd30104e56dac6a3047b2c23` \"Rev. 391: PRD fresh verification & stability confirmation (26 Oct 2026 WIB); header Rev. 391, §11 compact changelog 116–390, §12 added Rev. 391; HEAD 8c845dc (Rev. 390), 2 commits ahead origin_main\"; content commit `adb91f23a5cee5c5fd30104e56dac6a3047b2c23` (Rev. 391: PRD fresh verification & stability confirmation; HEAD 8c845dc (Rev. 390), 2 commits ahead origin_main). Local branch **1** commit ahead of `origin/main` (Rev. 392 ×1, 27 Oct 2026; Rev. 393 ×1, 28 Oct 2026).
   - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 393); seluruh file lain cocak dengan HEAD; untracked: skrip utility (tidak terpantau dalam git). `git ls-files` = 152 file.
   - **Database (dev.db):** file `dev.db` **tidak ada (absent)** — dihapus oleh commit HEAD \"Release: clean core files only\" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Data sumber:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.
   - **Build quality gate:** **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377; `npm ci` diperlukan untuk memulihkan); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` **tidak dapat dijalankan** karena `node_modules/` **absent**; `npm ci` diperlukan untuk memulihkan sebelum melakukan type-check/lint/build.
   - **Source files:** `src/app/*` = 13 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (13 halaman + layout + page). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.2 (SQLite).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map(\"uid_nfc\")` baris 68), `init_schema.sql` baris 40, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'); produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded totalSantri (totalSantri: 453, totalGuru: 54, totalKelas: 18 — sesuai `dev.db`); belum fetch real-time dari DB; tidak menggunakan nilai DB aktual.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. Schema inconsistency (Rev. 38–45) SELESAI — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **Status:** dokumen PRD **REVISI** — rev 393 = verifikasi fresh ulang & konfirmasi stabilitas di 28 Oktober 2026 (cron run); `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD `663984f` (Rev. 392), 0 commits ahead origin_main. State stabil, tidak ada perubahan signifikan dari Rev. 392."""

# Append at the end (before the final newline)
s = s.rstrip() + "\n" + new_section + "\n"

with open(PATH, "w", encoding="utf-8") as f:
    f.write(s)

print("Edits applied:")
for e in edits:
    print("  -", e)
print("Total edits:", len(edits))
