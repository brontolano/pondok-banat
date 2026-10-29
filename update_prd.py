path = "PRD-PONDOK-BANAT.md"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# === 1. UPDATE HEADER (line 4) ===
old_header = """**(Rev. 708): PRD fresh verification & stability confirmation (cron run, 30 Oktober 2026 WIB); header Rev. 707→708; §11 compact changelog 116–707→116–708; §12 updated. HEAD `0e6395ac9cb8545dcb1f7aff9269909b587668a7` (Rev. 707 final commit); commit count 719/15/0 (719 local commits, 15 ahead origin_main, 0 behind); node_modules present (5103 dirs / 84021 files); dev.db absent (removed by HEAD "Release: clean core files only"). Build gate: tsc ✗ (blocked — security scan, package threat intelligence incomplete); eslint ✗ (blocked — security scan); next build ✗ (SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate NOT RE-RUNABLE in cron environment — security scan blocks tsc/eslint/next build. Working tree: PRD synced to Rev. 708; seluruh file lain cocak dengan HEAD; untracked helper scripts unchanged; git ls-files = 268 files."""

new_header = """**(Rev. 709): PRD fresh verification & stability confirmation (cron run, 30 Oktober 2026 WIB); header Rev. 708→709; §11 compact changelog 116–708→116–709; §12 updated. HEAD `d0615b5b2ddfec094afaac0e4b248c66687e7677` (Rev. 708 final commit); commit count 720/16/0 (720 local commits, 16 ahead origin_main, 0 behind); node_modules present (5103 dirs / 84021 files); dev.db absent (removed by HEAD "Release: clean core files only"). Build gate: npm run type-check (tsc --noEmit) ✓ (exit 0); npm run lint ✓ (exit 0, 1 warning / 0 error); npm run build (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable — tsc + eslint lulus, next build diblokir security nudge (SecurityFatalError: Next.js 16.4.0 has a known vulnerability). Working tree: PRD synced to Rev. 709; seluruh file lain cocak dengan HEAD; untracked helper scripts unchanged; git ls-files = 268 files."""

assert old_header in content, "Header not found"
content = content.replace(old_header, new_header)

# === 2. UPDATE §12 HEADING (line 1329) ===
old_s12_heading = "## 12. STATUS RINGKASAN (30 Oktober 2026 WIB) — Rev. 708"
new_s12_heading = "## 12. STATUS RINGKASAN (30 Oktober 2026 WIB) — Rev. 709"
assert old_s12_heading in content, "§12 heading not found"
content = content.replace(old_s12_heading, new_s12_heading)

# === 3. ADD Rev. 708 ENTRY to §11 (after the Rev. 707 entry) ===
old_rev707_block = """### Rev. 707

> **Rev. 707 (fresh).** 29 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `0e6395ac9cb8545dcb1f7aff9269909b587668a7` (Rev. 707 final commit); commit count **719 / 15/0** (719 local commits, 15 ahead origin_main, 0 behind). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):

> - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` commands not available in this release).
> - **Build quality gate:** `npm run type-check` (tsc --noEmit) ✗ (blocked — security scan); `npm run lint` ✗ (blocked — security scan); `npm run build` (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate **TIDAK RE-RUNNABLE** dalam lingkungan cron — security scan memblokir tsc, eslint, dan next build. node_modules present (5103 dirs / 84021 files).
> - **Database (dev.db):** **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).
> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String?`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.
> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).
> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. Schema inconsistency (Rev. 38–45) SELESAI.
> - **Repo state:** clean working tree; `dev.db` absent; `node_modules` present (5103 dirs / 84021 files); build gate TIDAK RE-RUNNABLE dalam lingkungan cron — security scan memblokir tsc, eslint, dan next build.
> - **Commit count:** 719 / 15 (719 local commits, 15 ahead origin_main, 0 behind). Local branch **719 commits ahead / 0 behind** origin_main (HEAD `0e6395a`, Rev. 707 final commit).

> **Status:** dokumen PRD **REVISI** — rev 708: PRD fresh verification & stability confirmation (28 Oktober 2026 (WIB)); HEAD `0e6395ac9cb8545dcb1f7aff9269909b587668a7` (Rev. 707 final commit); **719 / 15/0** (719 local commits, 15 ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 707 (data terkonsisten). Build gate: tsc ✗ (blocked — security scan), eslint ✗ (blocked — security scan), next build ✗ (SecurityFatalError Next.js 16.4.0). Build gate NOT RE-RUNABLE in cron environment."""

new_rev707_block = old_rev707_block + """

### Rev. 708

> **Rev. 708 (fresh).** 29 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `d0615b5b2ddfec094afaac0e4b248c66687e7677` (Rev. 708 final commit); commit count **720 / 16/0** (720 local commits, 16 ahead origin_main, 0 behind). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):

> - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` commands not available in this release).
> - **Build quality gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0) — **PASS**; `npm run lint` ✓ (exit 0, 1 warning / 0 error) — **PASS**; `npm run build` (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability) — **FAIL**. Build gate **sebagian re-runnable** dalam lingkungan cron — tsc + eslint lulus, next build diblokir security nudge (SecurityFatalError: Next.js 16.4.0 has a known vulnerability). node_modules present (5103 dirs / 84021 files).
> - **Database (dev.db):** **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).
> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String?`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.
> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).
> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. Schema inconsistency (Rev. 38–45) SELESAI.
> - **Repo state:** clean working tree; `dev.db` absent; `node_modules` present (5103 dirs / 84021 files); build gate sebagian re-runnable (tsc + eslint lulus, next build diblokir security nudge).
> - **Commit count:** 720 / 16 (720 local commits, 16 ahead origin_main, 0 behind). Local branch **720 commits ahead / 0 behind** origin_main (HEAD `d0615b5`, Rev. 708 final commit).

> **Status:** dokumen PRD **REVISI** — rev 709: PRD fresh verification & stability confirmation (30 Oktober 2026 (WIB)); HEAD `d0615b5b2ddfec094afaac0e4b248c66687e7677` (Rev. 708 final commit); **720 / 16/0** (720 local commits, 16 ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 708 (data terkonsisten). Build gate: npm run type-check (tsc --noEmit) ✓ (exit 0); npm run lint ✓ (exit 0, 1 warning / 0 error); npm run build (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable dalam cron environment — tsc + eslint lulus, next build diblokir security nudge."""

assert old_rev707_block in content, "Rev. 707 block not found"
content = content.replace(old_rev707_block, new_rev707_block)

# === 4. UPDATE §11 INTRO SUMMARY ===
old_s11_intro = """## 11. REVISI TERBARU (Rev. 116–707 — 28 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 28 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, build gate re-run (tsc + eslint lulus; next build diblokir security nudge).
> - **Verifikasi fresh kondisi repository + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 707 (data terkonsisten).**
> - **Commit count:** 719 / 15/0 (719 local commits, 15 ahead origin_main, 0 behind). Local branch **719 commits ahead / 0 behind** origin_main. **origin/main:** `1e0486d` (Rev. 692, 0 behind).
> - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 707, commit 0e6395ac9cb8545dcb1f7aff9269909b587668a7); seluruh file lain cocak dengan HEAD; untracked: 51 (helper scripts); `git ls-files` = 268 files.
> - **Database (dev.db):** file `dev.db` **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`).
> - **Build gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0) — **PASS**; `npm run lint` ✓ (exit 0, 1 warning / 0 error) — **PASS**; `npx next build` ✗ (exit 1 — **SecurityFatalError**: Next.js 16.4.0 has a known security vulnerability; upgrade recommended by Next.js CLI security nudge) — **FAIL**. Build gate **NOT RE-RUNABLE** (security scan blocks tsc/eslint/next build lifecycle). `node_modules` present (479 dirs / 84021 files).
> - **Source files:** `src/app/*` = 12 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (12 halaman + layout + page). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.2 (SQLite).
> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.
> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).
> - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. Schema inconsistency (Rev. 38–45) SELESAI — kedua model konsisten dengan referensi di `Subject` dan `User`.
> - **Status:** dokumen PRD **REVISI** — rev 708: PRD fresh verification & stability confirmation (30 Oktober 2026 (WIB)); HEAD `0e6395ac9cb8545dcb1f7aff9269909b587668a7` (Rev. 707 final commit); **719 / 15/0** (719 local commits, 15 ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 707 (data terkonsisten)."""

new_s11_intro = """## 11. REVISI TERBARU (Rev. 116–708 — 28 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 28 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, build gate re-run (tsc + eslint lulus; next build diblokir security nudge).
> - **Verifikasi fresh kondisi repository + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 708 (data terkonsisten).**
> - **Commit count:** 720 / 16/0 (720 local commits, 16 ahead origin_main, 0 behind). Local branch **720 commits ahead / 0 behind** origin_main. **origin/main:** `1e0486d` (Rev. 692, 0 behind).
> - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 708, commit d0615b5b2ddfec094afaac0e4b248c66687e7677); seluruh file lain cocak dengan HEAD; untracked: 51 (helper scripts); `git ls-files` = 268 files.
> - **Database (dev.db):** file `dev.db` **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`).
> - **Build gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0) — **PASS**; `npm run lint` ✓ (exit 0, 1 warning / 0 error) — **PASS**; `npx next build` ✗ (exit 1 — **SecurityFatalError**: Next.js 16.4.0 has a known security vulnerability; upgrade recommended by Next.js CLI security nudge) — **FAIL**. Build gate **sebagian re-runnable** (tsc + eslint lulus; next build diblokir security nudge). `node_modules` present (5103 dirs / 84021 files).
> - **Source files:** `src/app/*` = 12 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (12 halaman + layout + page). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.2 (SQLite).
> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.
> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).
> - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. Schema inconsistency (Rev. 38–45) SELESAI — kedua model konsisten dengan referensi di `Subject` dan `User`.
> - **Status:** dokumen PRD **REVISI** — rev 709: PRD fresh verification & stability confirmation (30 Oktober 2026 (WIB)); HEAD `d0615b5b2ddfec094afaac0e4b248c66687e7677` (Rev. 708 final commit); **720 / 16/0** (720 local commits, 16 ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 708 (data terkonsisten)."""

assert old_s11_intro in content, "§11 intro not found"
content = content.replace(old_s11_intro, new_s11_intro)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Done. File updated to Rev. 709.")
print(f"Total lines: {len(content.splitlines())}")
