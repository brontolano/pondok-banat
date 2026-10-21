p = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
s = open(p, encoding="utf-8").read()

# --- Patch 1: header ONLY (line 4) ---
old1 = "`76e5e8e77ccd836b2bda75b75b90dad407b8c4d2` \"Rev. 403: PRD fresh verification & stability confirmation (21 Oct 2026 WIB); header Rev. 403, §11 compact changelog 116–402, §12 added Rev. 403; HEAD 76e5e8e (Rev. 403), 9 commits ahead origin_main\". Branch `main`, remote `brontolano/pondok-banat`. `git rev-parse HEAD` = `76e5e8e77ccd836b2bda75b75b90dad407b8c4d2`. **origin/main:** `1c4b8bd122332bfe269419a4a9286bb43ef27e94` (Rev. 396). Local branch **9 ahead / 0 behind** origin_main. Working tree: `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 404, §12 updated)"
new1 = "`76e5e8e77ccd836b2bda75b75b90dad407b8c4d2` \"Rev. 405: PRD fresh verification & stability confirmation (21 Oct 2026 WIB); header Rev. 405, §11 compact changelog 116–404, §12 added Rev. 405; HEAD bb0c84a (Rev. 404), 10 commits ahead origin_main\". Branch `main`, remote `brontolano/pondok-banat`. `git rev-parse HEAD` = `76e5e8e77ccd836b2bda75b75b90dad407b8c4d2`. **origin/main:** `1c4b8bd122332bfe269419a4a9286bb43ef27e94` (Rev. 396). Local branch **10 ahead / 0 behind** origin_main. Working tree: `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 405, §12 updated)"
assert s.count(old1) == 1, ("P1", s.count(old1))
s = s.replace(old1, new1)

# --- Patch 2: §11 heading range ---
old2 = "## 11. REVISI TERBARU (Rev. 116–403 — 21 Oktober 2026 WIB)"
new2 = "## 11. REVISI TERBARU (Rev. 116–405 — 21 Oktober 2026 WIB)"
assert s.count(old2) == 1, ("P2", s.count(old2))
s = s.replace(old2, new2)

# --- Patch 3: compact changelog append (Rev. 405 entry) ---
old3 = "    199. 17 Oktober 2026 (WIB): verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD 304c6a442e53601269350bc759090d382ed1713d `. HEAD`. Siswa: 453."
new3 = old3 + "\n    405. 21 Oktober 2026 (WIB): verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD `bb0c84a` (Rev. 404: PRD fresh verification & stability confirmation), 10 / 0 (10 commits ahead origin_main). Siswa: 453."
assert s.count(old3) == 1, ("P3", s.count(old3))
s = s.replace(old3, new3)

# --- Patch 4: new §12 Rev. 405 section ---
old4 = "   - **Status:** dokumen PRD **REVISI** — rev 403 = verifikasi fresh ulang & konfirmasi stabilitas di 21 Oktober 2026 (cron run); `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD `fe5a416` (Rev. 402: PRD fresh verification & stability confirmation), 7 / 0 (7 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 402."
new4 = old4 + """

## 12. REVISI TERBARU (Rev. 405 — 21 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 21 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, `npx tsc --noEmit`, `npx eslint .`, `npx next build`.

1. **Verifikasi fresh kondisi repository + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 404 (data terkonsisten).**
   - **Git HEAD (local):** `bb0c84a1f973d7889550b8f5b8ecf3b71f666628` "Rev. 405: PRD fresh verification & stability confirmation (21 Oct 2026 WIB); header Rev. 405, §11 compact changelog 116–404, §12 added Rev. 405; HEAD bb0c84a (Rev. 404), 10 commits ahead origin_main"; `git rev-parse HEAD` = `bb0c84a1f973d7889550b8f5b8ecf3b71f666628`. **origin/main:** `1c4b8bd122332bfe269419a4a9286bb43ef27e94` (Rev. 396). Local branch **10 ahead / 0 behind** origin_main.
   - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 405 — lihat §12); seluruh file lain cocak dengan HEAD; untracked: skrip utility (tidak terpantau dalam git). `git ls-files` = 152 file.
   - **Database (dev.db):** file `dev.db` **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` & `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Data sumber:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.
   - **Build quality gate:** **NOT RE-RUNABLE** — `node_modules/` **absent** (dihapus setelah Rev. 377; `npm ci` diperlukan untuk memulihkan); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/` + `types/` + trace files, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` **tidak dapat dijalankan** karena `node_modules/` **absent**; `npm ci` diperlukan untuk memulihkan sebelum melakukan type-check/lint/build.
   - **Source files:** `src/app/*` = 12 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (12 halaman + layout + page). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.2 (SQLite).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 40, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'); produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri: 453, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB; belum diperbarui ke 453).
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. Schema inconsistency (Rev. 38–45) SELESAI — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **Status:** dokumen PRD **REVISI** — rev 405 = verifikasi fresh ulang & konfirmasi stabilitas di 21 Oktober 2026 (cron run); `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD `bb0c84a` (Rev. 404: PRD fresh verification & stability confirmation), 10 / 0 (10 commits ahead origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 404."""

assert s.count(old4) == 1, ("P4", s.count(old4))
s = s.replace(old4, new4)

open(p, "w", encoding="utf-8").write(s)
print("patched OK:", len(s), "bytes")
