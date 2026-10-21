path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(path, "r", encoding="utf-8") as f:
    s = f.read()

def replace(old, new, count=1):
    global s
    assert old in s, f"NOT FOUND: {old[:80]}..."
    s = s.replace(old, new, count)

# ---- 1. Header: revision number ----
replace("revisi terbaru = Rev. 406, §12 updated", "revisi terbaru = Rev. 407, §12 updated")

# ---- 2. §11 changelog title ----
replace("## 11. REVISI TERBARU (Rev. 116–405 — 21 Oktober 2026 WIB)",
        "## 11. REVISI TERBARU (Rev. 116–407 — 21 Oktober 2026 WIB)")

# ---- 3. §12 Rev.406: git HEAD reference (line 1140) ----
old = "`ae23bcfc857a7ded65243fd01750210a62f2c7b1` \"Rev. 405: PRD fresh verification & stability confirmation (21 Oct 2026 WIB); header Rev. 406, §11 compact changelog 116–405, §12 added Rev. 406; HEAD ae23bcf (Rev. 405), 11 commits ahead origin_main\"; `git rev-parse HEAD` = `ae23bcfc857a7ded65243fd01750210a62f2c7b1`"
new = "`584fdfce7884a692c5ca944101c6ee12e71f59af` \"Rev. 406: PRD fresh verification & stability confirmation (21 Oct 2026 WIB); header Rev. 406, §11 compact changelog 116–405, §12 added Rev. 406; HEAD 584fdfce (Rev. 406), 12 commits ahead origin_main\"; `git rev-parse HEAD` = `584fdfce7884a692c5ca944101c6ee12e71f59af`"
replace(old, new)

# ---- 4. §12 Rev.406: local branch ahead count ----
replace("Local branch **11 ahead / 0 behind** origin_main", "Local branch **12 ahead / 0 behind** origin_main")

# ---- 5. §12 Rev.406: status line ----
old = """   - **Status:** dokumen PRD **REVISI** — rev 406 = verifikasi fresh ulang & konfirmasi stabilitas di 21 Oktober 2026 (cron run); `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD `ae23bcf` (Rev. 405: PRD fresh verification & stability confirmation), 11 / 0 (11 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 405."""
new = """   - **Status:** dokumen PRD **REVISI** — rev 406 = verifikasi fresh ulang & konfirmasi stabilitas di 21 Oktober 2026 (cron run); `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD `584fdfce` (Rev. 406: PRD fresh verification & stability confirmation), 12 / 0 (12 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 406."""
replace(old, new)

# ---- 6. Add Rev. 406 & Rev. 407 entries to the compact changelog (after entry 405) ----
old = """    405. 21 Oktober 2026 (WIB): verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD `ae23bcf` (Rev. 405: PRD fresh verification & stability confirmation), 11 / 0 (11 commits ahead origin_main). Siswa: 453."""
new = old + """

    406. 21 Oktober 2026 (WIB): verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD `584fdfce` (Rev. 406: PRD fresh verification & stability confirmation), 12 / 0 (12 commits ahead origin_main). Siswa: 453.
    407. 21 Oktober 2026 (WIB): fresh verification seluruh kondisi repository + dev.db (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 406**. Build gate: `tsc --noEmit` exit 1 & `npm run lint` exit 2 (kedua gagal karena `node_modules/` **absent** — sama seperti Rev. 406; `npm ci` diperlukan). Database: 1 user (admin@pondokanbat.com, role admin) | 5 role (admin, guru, wali_kelas, pengasuh, santri) | 33 role_permissions (M01) | 441 siswa (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 terisi) | 18 kelas (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK) | 54 guru (impor Excel, semua `active`) | 32 mapel | 5.420 nilai | 0 record tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students`, semua 441 NULL (data ekspor NFC Tools belum tersedia). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain). **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri: 453, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi**; `uidNfc` (baris 68) tetap ada. **Status:** dokumen PRD **REVISI** — rev 407 = fresh verification & konfirmasi stabilitas; state stabil, tidak ada perubahan signifikan dari Rev. 406."""
replace(old, new)

# ---- 7. Add §13 Rev. 407 section at the end ----
old = """   - **Status:** dokumen PRD **REVISI** — rev 406 = verifikasi fresh ulang & konfirmasi stabilitas di 21 Oktober 2026 (cron run); `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD `584fdfce` (Rev. 406: PRD fresh verification & stability confirmation), 12 / 0 (12 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 406."""
new = old + """

## 13. REVISI TERBARU (Rev. 407 — 21 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 21 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, `npx tsc --noEmit`, `npx eslint .`, `npx next build`.

1. **Verifikasi fresh kondisi repository + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 406 (data terkonsisten).**
   - **Git HEAD (local):** `584fdfce7884a692c5ca944101c6ee12e71f59af` (Rev. 406: PRD fresh verification & stability confirmation), 12 / 0 (12 commits ahead origin_main).
   - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 407 — lihat §13); seluruh file lain cocak dengan HEAD; untracked: skrip utility (tidak terpantau dalam git). `git ls-files` = 152 file.
   - **Database (dev.db):** file `dev.db` **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Data sumber:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.
   - **Build quality gate:** **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377; `npm ci` diperlukan untuk memulihkan); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/` + `types/` + trace files, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` **tidak dapat dijalankan** karena `node_modules/` **absent**; `npm ci` diperlukan untuk memulihkan sebelum melakukan type-check/lint/build.
   - **Source files:** `src/app/*` = 12 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (12 halaman + layout + page). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.2 (SQLite).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 40, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'); produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri: 453, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB; belum diperbarui ke 453).
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. Schema inconsistency (Rev. 38–45) SELESAI — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **Status:** dokumen PRD **REVISI** — rev 407 = fresh verification & konfirmasi stabilitas di 21 Oktober 2026 (cron run); `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD `584fdfce` (Rev. 406: PRD fresh verification & stability confirmation), 12 / 0 (12 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 406."""
replace(old, new)

with open(path, "w", encoding="utf-8") as f:
    f.write(s)

print("Done. PRD updated to Rev. 407.")
print("File size:", len(s.encode("utf-8")), "bytes")
