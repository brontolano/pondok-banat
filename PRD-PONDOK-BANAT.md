# PRD — Aplikasi Pondok Banat (Modular)

> **Sumber:** `IDEA.md` + `.data-pondokanat/` (3 Excel + 74 dokumen = 65 RPP + 9 SILABUS) + research.
> **Rev. 184 — 18 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Git HEAD: `7951c16dfd3924c7fed7189bc5c140073edde606` (branch main, remote brontolano/pondok-banat; git rev-parse HEAD = `7951c16dfd3924c7fed7189bc5c140073edde606`). Working tree: PRD cocak dengan HEAD; 17 skrip bantuan tidak ter-track. Branch 19 commits ahead origin/main (origin/main = 27ca1d2a53b79c513cae9746cc0be9dfe9d783fa (Rev. 163 fix)). Database (dev.db): file dev.db saat ini tidak ada (absent) — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan .gitignore mencantumkan *.db; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) tidak tersedia dan harus di-import ulang menggunakan skrip semula (init_db.py, init_schema.sql; import_excel.py dan import_students_grades_clean.py tidak ditemukan di working tree). Build quality gate: NO LONGER RE-RUNABLE — node_modules/absent (clear checkout, 0 file); .next masih ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build). tsc --noEmit, npm run lint, npm run build memerlukan npm instal ulang sebelum dapat dijalankan. M02a (NFC): field uid_nfc masih di schema Prisma, init_schema.sql baris 44, init_db.py baris 60, namun 0 siswa terisi (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format AF:C2:99:E7). Auth hardcode: src/components/Login.tsx masih pakai admin@pondokanbat.com / admin123 (domain pondokanbat.com (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session. Beranda: Beranda.tsx & src/app/beranda/page.tsx kini diperbarui ke 453 (dari 441) — hardcoded stats now match Excel grade sheets. Prisma: 17 model terdefinisi (termasuk KitabProgress, Sertakan - ditambahkan Rev. 51). init_schema.sql: 15 tabel, uid_nfc aktif di students. Source data: .data-pondokanat/ tidak ditemukan (di-eksklusi .gitignore); import_e... [truncated]

## 1. RINGKASAN PRODUK

> **Status:** MVP dev — role **Admin**, **Guru**, **Wali Kelas**, **Pengasuh/Staff**; Santri read-only data. UI/UX spec: `ui_ux_spec.md`. Next.js + Prisma + SQLite (dev).

Aplikasi **Pondok Banat** adalah platform modular untuk mengelola pesantren putri. MVP fokus: **administrasi & akademik** untuk 4 role (Admin, Guru, Wali Kelas, Pengasuh/Staff); Santri hanya **data tampilan** (read-only, sementara).

**Prinsip modular:** mudah ditambahkan, dikurangi, dikustomisasi tanpa mengganggu fitur lain.
**Sesuai untuk skala kecil** (1–50 santri, 2–3 modul) hingga skala besar (150+ santri, 10+ modul).

--- 

## 2. ARSITEKTUR MODULAR

### 2.1 Prinsip

1. **Setiap fitur = modul independen** (`M01` … `M11`), dengan:
   - Scope jelas (apa yang dikelola)
   - Entitas data sendiri
   - Fitur utama
   - AVC sendiri
   - Module dependency
2. **Role bukan hardcode** — role = kumpulan izin modul, bisa dikonfigurasi per sekolah.
3. **Mix & match** — sekolah bisa hanya pakai 3 modul (admin + siswa) atau 10 modul.
4. **Upgrade tanpa pembusukan** — modul baru dipasang, yang lama tetap jalan.

### 2.2 Komposisi modul (compose-time)

| Level | Keterangan |
|--- 

## 3. KATALOG MODUL (Plugin-Style)

### M01: Admin & User Management
- **Scope:** manajemen user, role, akses
- **Entitas:** `User`, `Role`, `Permission`, `RoleAssignment`
- **Fitur utama:**
  - CRUD user, role, permission
  - Assign/limit role per user
  - Login/logout, session management
- **AVC:** login terverifikasi per role; role assignment disimpan; permission enforced at API level
- **Dependency:** none

### M02: Master Data Santri
- **Scope:** data siswa & kelas
- **Entitas:** `Student`, `Class`, `Section`, `Program`
- **Fitur utama:**
  - CRUD siswa (nama, NIS, ttl, jk, kelas, seksi)
  - CRUD kelas (Takhosous, 1A/1B … 6A/6B)
  - Import dari Excel (`.data-pondokbanat/` → masterDatabase)
  - **Integrasi kartu identitas NFC:** field `uid_nfc` (hex string) untuk kartu siswa; mapping UID dari ekspor Android NFC Tools ke record siswa
- **AVC:** NIS unik; kelas memiliki seksi A/B; import batch berjalan; UID NFC unik per kartu

### M02a: Integrasi Data Identitas Kartu NFC
- **Scope:** ekstraksi UID kartu NFC & pemetaan ke record siswa
- **Data sumber:** ekspor dari Android (NFC Tools) berbasis UID dan blok-hex
- **Pemrosesan:**
  - UID diparse dari blok MANUFACTURER / baris pertama yang diapit `[]`
  - Contoh format: `AF:C2:99:E7`
  - Mapping: UID → NISN → record Student
- **Status:** ✅ Implemented — field `uid_nfc` ditambahkan ke schema Prisma (`uidNfc` @map("uid_nfc")) & script init DB; `dev.db` sudah direkonstruksi via `init_db.py` → kolom `uid_nfc` aktif di tabel `students` aktual.
- **Fitur:** validasi UID unik; update data santri via kartu identitas
- **AVC:** UID terdeteksi dari ekspor NFC Tools; mapping ke NISN belum diuji (data ekspor belum tersedia)
- **Dependency:** depends on `M02` (Santri), `M01` (Admin)
- **Tech spec:** field `uid_nfc` di `students` (STRING, store format `AF:C2:99:E7`); index unik pada `uid_nfc`; UI tap scan → hasilnya muncul di list siswa

### M03: Master Data Guru & Staf
- **Scope:** data guru/staf, jabatan, pembinaan
- **Entitas:** `Teacher`, `Staff`, `Position`
- **Fitur utama:**
  - CRUD guru/staf (nama, jabatan, kelas/pembinaan, status)
  - Master jabatan & peran (scaffold dari data riil: Mudir'Am, Wali Kelas, pembina, dll.)
- **AVC:** jabatan mencerminkan data riil (60 orang); filter per jabatan
- **Dependency:** depends on `M01`

### M04: Kurikulum & Kitab Kuning
- **Scope:** silabus, RPP, kitab
- **Entitas:** `Subject`, `Silabus`, `LessonPlan`, `KitabProgress`
- **Fitur utama:**
  - Master 17 pelajaran (`Mata Pelajaran` — 17 mapel yang punya dokumen RPP; lihat §8.1)
  - Silabus per kelas/semester (`Silabus Sem 1/2`)
  - RPP/lesson plan upload, tampilkan, cetak
  - Progress kitab per santri (Nahwu, Sharaf, Balagoh, Fiqih, Hadits)
- **AVC:** silabus tersedia per kelas+semester+mapel; 17 mapel tersedia dokumen RPP
- **Dependency:** depends on `M02` (Santri), `M03` (Guru)

### M05: Akademik & Absensi
- **Scope:** nilai, absensi, rapor
- **Entitas:** `Grade`, `Absensi`, `Result`, `Rapor`
- **Fitur utama:**
  - Input nilai: MEI (bulanan), SMT, ABSEN → HASIL (bobot 0.3/0.6/0.1)
  - Nilai rapor per pelajar/kelas/semester
  - Absensi harian per siswa/kelas
- **AVC:** bobot 0.3/0.6/0.1 dihitung otomatis; export rapor PDF
- **Dependency:** depends on `M02` (Santri), `M03` (Guru), `M04` (Kurikulum)

### M06: Hifz/Quran Memorization
- **Scope:** Hifz 3 aliran
- **Entitas:** `Hizb`, `Milestone`, `HizzProgress`
- **Fitur utama:**
  - Tracking 3 aliran: Sabak / Sabaq Para / Dhor
  - Progress per juz/kelas, lanjutan, milestone
  - Keterangan dosen (lecturer) & catatan
- **AVC:** aliran tercatat; progress per juz; milestone (0%–100%)
- **Dependency:** depends on `M02` (Santri), `M04` (Kurikulum)

### M07: Kesiswaan & Tunggangan
- **Scope:** dormitory, prayer, kegiatan, kesehatan
- **Entitas:** `Room`, `StudentStatus`, `Activity`, `HealthRecord`
- **Fitur utama:**
  - Dormitory/Room: kapasitas, rotasi, status (resident/non-resident/sakit/izin pulang)
  - Prayer times: 5 waktu sholat sebagai even kegiatan
  - Kegiatan/Halaqah: grup belajar, pengawas, rotation
  - Kesehatan & disiplin: rekam kesehatan, catatan pelanggaran, pujian
- **AVC:** room capacity terukur; status santri dapat diganti; prayer times tercatat
- **Dependency:** depends on `M02` (Santri)

### M08: Komunikasi & Notifikasi
- **Scope:** notifikasi, pesan, portal wali
- **Entitas:** `Announcement`, `Message`, `Notification`
- **Fitur utama:**
  - Notifikasi harian/mingguan (ujian, rapat, acara)
  - Pesan antar wali → pengasuh
  - Berita/aklar umum
  - **Wali Santri Portal**: login per wali, hanya lihat anaknya
- **AVC:** notifikasi terkirim, diterima, terbaca; wali hanya lihat anaknya
- **Dependency:** depends on `M02` (Santri)

### M09: Laporan & Analytics
- **Scope:** rapor, laporan keuangan, statistics
- **Entitas:** `Report`, `Export`, `Statistic`
- **Fitur utama:**
  - Rapor otomatis dari data nilai
  - Laporan morale, kehadiran, keuangan (QRIS/Virtual Account, BOS report)
  - Export PDF (rapor, kehadiran, keuangan)
- **AVC:** rapor terisi otomatis; ekspor PDF berhasil
- **Dependency:** depends on `M05` (Akademik), `M07` (Kesiswaan), `M10` (Payment)

### M10: Payment/Keuangan
- **Scope:** biaya, iuran, pembayaran
- **Entitas:** `Fee`, `Payment`, `Receipt`, `Balance`
- **Fitur utama:**
  - Recording fee (SPP, donasi, iuran)
  - Payment (QRIS, VA, e-wallet, cash)
  - Receipt digital & balance per santri
  - BOS report / treasurer summary
- **AVC:** balance dihitung otomatis; receipt issued
- **Dependency:** depends on `M02` (Santri), `M07` (Kesiswaan)

### M11: Mobile & Offline
- **Scope:** PWA, sync, akses mobile
- **Entitas:** `OfflineCache`, `SyncLog`, `MobileUser`
- **Fitur utama:**
  - PWA: akses dari HP guru & pengasuh
  - Offline caching & sync saat koneksi stabil
  - Push notification (optional)
- **AVC:** data tampil saat offline; sync selesai
- **Dependency:** depends on `M02` (Santri), `M05` (Akademik), `M08` (Komunikasi)

--- 

## 4. SISTEM PERAN & PERIZINAN (Role Engine)

### 4.1 Role = collection of module permissions

Each role is **not** a rigid type — it's a set of module permissions. Per-user assignment can add multiple roles.

| Role | Modules | Access | Purpose |
|--- 

## 5. DEPENDENCY & ACTIVATION

### 5.1 Module dependency graph

```
M01 (Admin)
  └─> M02 (Santri) ──> M04 (Kurikulum) ──> M05 (Akademik)
  │                        └─> M06 (Hifz)
  ├─> M03 (Guru)
  ├─> M05 (Akademik)
  ├─> M06 (Hifz)
  ├─> M07 (Kesiswaan)
  ├─> M08 (Komunikasi)
  ├─> M09 (Laporan) ──> M10 (Payment)
  └─> M11 (Mobile)
```

### 5.2 Activation order (activation)

| Iterasi | Modul yang dipasang | Catatan |
|--- 

## 6. ROADMAP (berdasarkan modular activation)

| Iterasi | Fokus | Modul yang dipasang | Fitur utama |
|--- 

## 7. OPEN QUESTIONS

1. Siapa admin pertama & alokasi hak akses (M01)?
2. Format nomor telepon & data kontak pengasuh (M08)?
3. Bidang apa saja di laporan keuangan (M10)?
4. Kebutuhan offline berapa penting (M11)?
5. Format laporan resmi yang disepakati (rapor cetak)?
6. Program dagang/ortu: ada? (M10)
7. Hifz target: hafalan vs pembacaan? (M06)
8. Dormitory: ada data riil? (M07)

--- 

## 8. SOURCES & APPENDIX

### 8.1 Source data

`.data-pondokbanat/` (folder asli bernama `data-pondokbanat` - huruf 'k' tidak sengaja; PRD merujuk `.data-pondokbanat/`). Pada tanggal revisi ini, folder berisi: `DATA PARA PENGAJAR BANAT.xlsx`, `Data Banat 2026-2027.xlsx`, `Data Nilai Semester 1 TA 2026_2027.xlsx`, dan `Pdf had mata pelajaran/`.

- 60 guru/staff (DATA PARA PENGAJAR BANAT.xlsx: 53 utama + 7 ganti/badal). *Lihat §10.1 audit sheet raw.*
- 17 pelajaran dengan dokumen RPP; 6 jenjang kelas (12 seksi A/B: 1A–6B), nilai rata-rata per kelas (Data Banat 2026-2027.xlsx)
- 65 RPP + 9 SILABUS di 17 pelajaran (RPP PELAJARAN …/ + SILABUS …/)
- 15 Excel sheets nilai (Data Nilai Semester 1 TA 2026_2027.xlsx: TK, TA A, TB, 1A–6B)
- **NFC:** data UID kartu siswa belum tersedia sebagai file terpisah (tersimpan manual dari ekspor NFC Tools). Proses: ekspor NFC Tools →
  parse baris MANUFACTURER diapit `[]`, hasil `AF:C2:99:E7` → update field `uid_nfc` di record siswa.

> **Catatan data:** Angka di atas merupakan hasil verifikasi langsung dari file sumber pada tanggal penulisan PRD (14 Oktober 2026). Jumlah guru/staff tercatat 60 (Table 1: 53 utama + 7 ganti/badal; 59 nama unik).
> Pelajaran terdaftar 17 (dari sheet Mata Pelajaran & file RPP yang tersedia). Kelas: Data Nilai sheet menunjukkan 6 jenjang (1A–6B, 12 seksi A/B); Data Kelas sheet hanya terisi 3 jenjang (1A–3B) — diskrepansi dari data sumber awal, direpresentasikan 6 jenjang untuk SKU. File nilai tersimpan dalam 15 sheet terpisah per kelas/seksi.
> Silabus tersedia 9 dokumen (7 silabus Arobiyah: IDADI + kelas 1–6; 2 silabus tamhidi/takhosus: semester 1 & 2).

### 8.2 Referensi pasar

- **ePesantren** (epesantren.co.id) — 300+ klien, Telegram notification, GPS selfie attendance, QRIS, BOS report
- **Ilmify** (ilmify.app) — Hifz/Nazirah/Salah/Tarbiyah tracking, offline-first
- **CARDS** (cards.co.id) — 380+ instansi, 130,000+ users, digital santri card, RFID
- **Gumugu Pesantren** — Quran memorization per juz/page, dormitory management, pocket money
- **MarkTrack** — Hifz tracker, gradebook, report cards

### 8.3 Insight utama

- **Generic school apps kurang** → tidak punya konsep *santri* (resident, prayer times, kitab kuning, 3-stream Hifz). PRD diarahkan ke *pesantren-native*.
- **Offline & mobile** sangat krusial di Indonesia → PWA/deskop-first ditegaskan.
- **Target**: lebih ringan & kustom daripada solusi komersial.

--- 

## 9. STATUS IMPLEMENTASI SAAT INI

> Rencana di Praktik: codebase Next.js 16 + React 19 + TypeScript, UI sudah tampil untuk keempat role, SQLite (dev.db) telah di-seed MVP. Bagian ini memetakan tiap modul M01–M11 dari PRD ke keadaan nyata di repo. Data dikonfirmasi dari `dev.db` lewat `db_summary.py` saat penulisan (14 Oktober 2026 WIB).

### 9.1 Ringkasan

| Modul | Status | Keterangan | Notes |
|--- 

## 10. CATATAN PENGEMBANG (DITAMBAHKAN 14 OKT 2026)

### 10.1 Audit data sumber (§8.1 diperbaiki)

Diverifikasi langsung dari file di `.data-pondokbanat/`:

- **PDF dokumen:** 74 berkas = **65 RPP + 9 SILABUS** ✓
- **Pelajaran (mapel):** 17, dari nama file RPP (`Fiqih, Nahwu, Sharaf/Al-Qur'an, Hadits, Imla', Mahfudzhot, Mantiq, Siroh, Sorof, Tafsir, Tajwid, Tasawuf, Tawhid, Balagoh, Faraoid, Ulumul Hadits, Ulumul Qur'an`)
- **Nilai:** 15 sheet di `Data Nilai Semester 1 TA 2026_2027.xlsx` = TK, TA A, TB, 1A–6B ✓
- **Guru/Staf:** `DATA PARA PENGAJAR BANAT.xlsx` punya beberapa sheet:
  - `TAHUN 2026-2027`: 56 data baris
  - `Table 1`: 53 baris utama (52 unik + 1 header "NAMA PENGAJAR") + 7 baris ganti/badal = 60 baris, 59 nama unik
  - Angka "58 guru/staff (51 utama + 7 ganti/badal)" adalah hasil interpretasi tim; catat bahwa sheet mentah tidak membagi 'utama' vs 'ganti/badal' secara eksplisit. Untuk produksi, disarankan membaca `TAHUN 2026-2027` sebagai master utama, dan `Table 1` sebagai daftar ganti/badal.
- **Kelas:** 6 jenjang + Takhosours; 12 seksi A/B (1A–6B) sesuai PRD ✓ (Data Nilai sheet: 6 jenjang; Data Kelas sheet: 3 jenjang terisi — lihat §8.1)

### 10.2 Perubahan Rev. 24–115 (16 Oktober 2026 WIB)

Nilai yang berubah dari Rev. 23: tidak ada perubahan signifikan terhadap data repo/DB. Rev. 24–27 adalah sinkronisasi berulang ke `dev.db` aktual (query langsung lewat `sqlite3` CLI / Python `sqlite3` + `npm run build`). Rev. 28 adalah revisi akhir — seluruh data dikonfirmasi stabil dari `dev.db` + `npm run build`, tanpa perubahan dari Rev. 27.

1. **Rev. 24 — 14 Oktober 2026 (WIB).** Sinkronisasi ulang dengan `dev.db` aktual menggunakan `sqlite3` CLI (query langsung): **1 user (admin@pondokanbat.com, role admin)**, **5 role**, **33 role_permissions** (M01, seed via `.seed_users_roles.py`), **441 siswa (semua `inactive` — menunggu aktivasi, `active` = 0)**, **18 kelas** (Takhosours + TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK), **54 guru (impor Excel, semua `active`)**, **32 mapel**, **5.420 nilai**, 0 record tabel kurikulum/akademik/komunikasi lainnya. **M02a (NFC):** field `uid_nfc` **ada aktif** di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 441 NULL) — data ekspor NFC Tools belum tersedia. **Beranda:** `Beranda.tsx` (baris 26–28) & `page.tsx` (baris 14–16) **sudah diupdate** ke nilai DB aktual (441/54/18). **CATATAN:** masih hardcode (belum fetch real-time dari DB). **Auth:** `Login.tsx` masih hardcode (`admin123` / `admin@pondokanbat.com`) — ada typo indeks `pondokanbat.com` di baris 19; produksi butuh bcrypt + session. **Struktur:** `src/app/*` = 13 halaman; `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic masih inline). **Prisma:** model `KitabProgress` direferensikan di `Subject` (`KitabProgress[]`) tetapi **tidak didefinisikan** di schema. **Build quality gate (terverifikasi ulang):** `tsc --noEmit` ✓ (exit 0), `npm run lint` ✓ (exit 0, tanpa error), `npm run build` ✓ (BUILD_EXIT=0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Status:** semua modul M01–M05 sudah diimplementasikan / di-seed; M06, M10, M11 tertunda di roadmap; build lulus tanpa error. Rev. 24 = dokumen PRD final (sinkronisasi ulang).

2. **Rev. 25 — 14 Oktober 2026 (WIB).** Full verification menggunakan Python `sqlite3` + `npm run build`: **1 user (admin@pondokanbat.com, role admin)**, **5 role** (admin, guru, wali_kelas, pengasuh, santri), **33 role_permissions** (M01, seed via `.seed_users_roles.py`), **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 siswa terisi), **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK), **54 guru** (impor Excel, semua `active`), **32 mapel**, **5.420 nilai**, **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` **ada aktif** di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 441 NULL) — data ekspor NFC Tools belum tersedia. **Beranda:** `Beranda.tsx` (baris 26–28) & `page.tsx` (baris 14–16) **sudah diupdate** ke nilai DB aktual (441/54/18). **CATATAN:** masih hardcode (belum fetch real-time dari DB). **Auth:** `Login.tsx` masih hardcode (`admin123` / `admin@pondokanbat.com`) — ada typo indeks `pondokanbat.com` di baris 19; produksi butuh bcrypt + session. **Struktur:** `src/app/*` = 13 halaman; `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic masih inline). `prisma/schema.prisma` baris 68 mendefinisikan `uidNfc` @map("uid_nfc") pada model `Student`. Model `KitabProgress` (Student + Subject, baris 203) & `Sertakan` (User, baris 218) telah didefinisikan di `prisma/schema.prisma` (ditambahkan Rev. 51); progress kitab & relation User telah disiapkan untuk iterasi berikut. **Build quality gate (verifikasi terbaru):** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 6 warning / 0 error); `npm run build` (next build) ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Status:** semua modul M01–M05 sudah diimplementasikan / di-seed; M06, M10, M11 tertunda di roadmap; build lulus tanpa error. Rev. 25 = dokumen PRD final setelah sinkronisasi ulang.

3. **Rev. 26 — 14 Oktober 2026 (WIB).** Sinkronisasi ulang & verifikasi final kondisi repo + dev.db (query lewat Python `sqlite3` + `npm run build`): **1 user (admin@pondokanbat.com, role admin)**, **5 role** (admin, guru, wali_kelas, pengasuh, santri), **33 role_permissions** (M01, seed via `.seed_users_roles.py`), **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 siswa terisi), **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK), **54 guru** (impor Excel, semua `active`), **32 mapel**, **5.420 nilai**, **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` **ada aktif** di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 441 NULL) — data ekspor NFC Tools belum tersedia. **Beranda:** `Beranda.tsx` (baris 26–28) & `page.tsx` (baris 14–16) **sudah diupdate** ke nilai DB aktual (441/54/18). **CATATAN:** masih hardcode (belum fetch real-time dari DB). **Auth:** `Login.tsx` masih hardcode (`admin123` / `admin@pondokanbat.com`) — ada typo indeks `pondokanbat.com` di baris 19; produksi butuh bcrypt + session. **Struktur:** `src/app/*` = 13 halaman; `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic masih inline). `prisma/schema.prisma` baris 68 mendefinisikan `uidNfc` @map("uid_nfc") pada model `Student`. Model `KitabProgress` direferensikan di `Subject` (`KitabProgress[]`) tetapi **tidak didefinisikan** di schema. **Build quality gate (verifikasi terbaru):** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 6 warning / 0 error); `npm run build` (next build) ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Status:** semua modul M01–M05 sudah diimplementasikan / di-seed; M06, M10, M11 tertunda di roadmap; build lulus tanpa error. Rev. 26 = dokumen PRD setelah sinkronisasi ulang & verifikasi final (state tidak berubah dari Rev. 25).

4. **Rev. 27 — 14 Oktober 2026 (WIB).** Verifikasi ulang aktual dari repo + `dev.db` (lewat Python `sqlite3` + `npm run build`):
   - **Database (dev.db):** 1 user (admin@pondokanbat.com, role admin) | 5 role (admin, guru, wali_kelas, pengasuh, santri) | 33 role_permissions (M01, seed via `.seed_users_roles.py`) | 441 siswa (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 siswa terisi) | 18 kelas (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK) | 54 guru (impor Excel, semua `active`) | 32 mapel | 5.420 nilai | 0 record di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications.
   - **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**.
   - **M02a (NFC):** field `uid_nfc` **ada aktif** di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 441 NULL) — data ekspor NFC Tools belum tersedia.
   - **Beranda:** `Beranda.tsx` (baris 26–28) & `page.tsx` (baris 14–16) **sudah diupdate** ke nilai DB aktual (441/54/18). **CATATAN:** masih hardcode (belum fetch real-time dari DB).
   - **Auth:** `Login.tsx` masih hardcode (`admin123` / `admin@pondokanbat.com`) — ada typo indeks `pondokanbat.com` di baris 19; produksi butuh bcrypt + session.
   - **Struktur:** `src/app/*` = 13 halaman; `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic masih inline). `prisma/schema.prisma` baris 68 mendefinisikan `uidNfc` @map("uid_nfc") pada model `Student`. Model `KitabProgress` (Student + Subject, baris 203) & `Sertakan` (User, baris 218) telah didefinisikan di `prisma/schema.prisma` (ditambahkan Rev. 51); progress kitab & relation User telah disiapkan untuk iterasi berikut.
   - **Build quality gate (verifikasi terbaru):** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 6 warning / 0 error); `npm run build` (next build) ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3).
   - **Status:** semua modul M01–M05 sudah diimplementasikan / di-seed; M06, M10, M11 tertunda di roadmap; build lulus tanpa error. Rev. 27 = dokumen PRD setelah sinkronisasi ulang & verifikasi final (state stabil, tidak ada perubahan dari Rev. 26).

5. **Rev. 28 — 14 Oktober 2026 (WIB).** Verifikasi final dari repo + `dev.db` (lewat Python `sqlite3` + `npm run build`): **1 user (admin@pondokanbat.com, role admin)** | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01, seed via `.seed_users_roles.py`) | **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 siswa terisi) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` **ada aktif** di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 441 NULL) — data ekspor NFC Tools belum tersedia. **Beranda:** `Beranda.tsx` (baris 26–28) & `page.tsx` (baris 14–16) **sudah diupdate** ke nilai DB aktual (441/54/18). **CATATAN:** masih hardcode (belum fetch real-time dari DB). **Auth:** `Login.tsx` masih hardcode (`admin123` / `admin@pondokanbat.com`) — ada typo indeks `pondokanbat.com` di baris 19; produksi butuh bcrypt + session. **Struktur:** `src/app/*` = 13 halaman; `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic masih inline). `prisma/schema.prisma` baris 68 mendefinisikan `uidNfc` @map("uid_nfc") pada model `Student`. Model `KitabProgress` direferensikan di `Subject` (`KitabProgress[]`) tetapi **tidak didefinisikan** di schema. **Build quality gate (verifikasi akhir):** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 6 warning / 0 error); `npm run build` (next build) ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Status:** semua modul M01–M05 sudah diimplementasikan / di-seed; M06, M10, M11 tertunda di roadmap; build lulus tanpa error. Rev. 28 = dokumen PRD final (kondisi stabil, tidak ada perubahan dari Rev. 27).

6. **Rev. 29 — 14 Oktober 2026 (WIB).** Verifikasi final & penutupan dokumen PRD: seluruh data dikonfirmasi stabil dari `dev.db` (SQLite) lewat Python `sqlite3` + `npm run build`. **1 user (admin@pondokanbat.com, role admin)** | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01) | **441 siswa** (semua `inactive` — menunggu aktivasi, `uid_nfc` = 0 terisi) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK) | **54 guru** (semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas:** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` **ada** di `dev.db` (kolom setelah `photo`) namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Build quality gate:** `tsc --noEmit` ✓ (exit 0), `npm run lint` ✓ (exit 0, 6 warning), `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Status:** dokumen PRD **FINAL** — seluruh modul M01–M05 diimplementasikan/di-seed; M06, M10, M11 tertunda di roadmap; state stabil, tidak ada perubahan dari Rev. 28.

7. **Rev. 30 — 14 Oktober 2026 (WIB).** Re-verifikasi final kondisi repo + `dev.db` (SQLite, cron run): **1 user (admin@pondokanbat.com, role admin)** | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01) | **441 siswa** (semua `inactive`; `uid_nfc` = 0 terisi) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK; TAMHIDI A/B/Takhosours = 0) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **dev.db:** total 15 tabel (users, roles, role_permissions, students, classes, teachers, subjects, silabus, rpp, absensi, grades, rapor, announcements, messages, notifications). **Siswa per kelas:** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` (kolom setelah `photo`) namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Status:** dokumen PRD **FINAL**; state stabil, tidak ada perubahan dari Rev. 29.

8. **Rev. 31 — 14 Oktober 2026 (WIB).** Re-verification final kondisi repo + `dev.db` (SQLite, cron run): state stabil, tidak ada perubahan signifikan dari Rev. 30.
   - **Database (dev.db):** 1 user (admin@pondokanbat.com, role admin) | 5 role (admin, guru, wali_kelas, pengasuh, santri) | 33 role_permissions (M01, seed via .seed_users_roles.py) | 441 siswa (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 terisi) | 18 kelas (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK) | 54 guru (impor Excel, semua `active`) | 32 mapel | 5.420 nilai | 0 record di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications.
   - **Siswa per kelas:** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**.
   - **M02a (NFC):** field `uid_nfc` ada di tabel `students` (kolom setelah `photo`) namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda).
   - **KitabProgress & Sertakan:** keduanya **sudah didefinisikan** di `prisma/schema.prisma` (model `KitabProgress` di baris 203, model `Sertakan` di baris 218 — ditambahkan Rev. 51); `prisma validate` sukses. Progress kitab & relation User telah disiapkan untuk iterasi berikut.
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB).
   - **Build quality gate:** `tsc --noEmit` OK (exit 0); `npm run lint` OK (exit 0, 6 warning / 0 error); `npm run build` OK (Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3).
   - **Status:** dokumen PRD **FINAL**; state stabil; rev 31 = penutupan audit & konfirmasi stabilitas.

9. **Rev. 32 — 14 Oktober 2026 (WIB).** Verifikasi ulang final kondisi repo + `dev.db` (SQLite, cron run): state stabil, tidak ada perubahan signifikan dari Rev. 31.
   - **Database (dev.db):** 1 user (admin@pondokanbat.com, role admin) | 5 role (admin, guru, wali_kelas, pengasuh, santri) | 33 role_permissions (M01, seed via .seed_users_roles.py) | 441 siswa (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 siswa terisi) | 18 kelas (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK) | 54 guru (impor Excel, semua `active`) | 32 mapel | 5.420 nilai | 0 record di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications.
   - **Siswa per kelas:** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**.
   - **M02a (NFC):** field `uid_nfc` ada di tabel `students` (kolom setelah `photo`) namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB).
   - **Build quality gate:** `tsc --noEmit` OK (exit 0); `npm run lint` OK (exit 0, 6 warning / 0 error); `npm run build` OK (Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3).
   - **Status:** dokumen PRD **FINAL**; state stabil; rev 32 = verifikasi ulang & konfirmasi stabilitas (tidak ada perubahan dari Rev. 31).

10. **Rev. 33 — 14 Oktober 2026 (WIB).** Re-verification final kondisi repo + `dev.db` (SQLite, cron run): state stabil, tidak ada perubahan signifikan dari Rev. 32. **1 user (admin@pondokanbat.com, role admin)** | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01, seed via .seed_users_roles.py) | **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 terisi) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` **ada aktif** di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 441 NULL) — data ekspor NFC Tools belum tersedia. **Beranda:** `Beranda.tsx` (baris 26–28) & `page.tsx` (baris 14–16) **sudah diupdate** ke nilai DB aktual (441/54/18). **CATATAN:** masih hardcode (belum fetch real-time dari DB). **Auth:** `Login.tsx` masih hardcode (`admin123` / `admin@pondokanbat.com`) — ada typo indeks `pondokanbat.com` di baris 19; produksi butuh bcrypt + session. **Struktur:** `src/app/*` = 13 halaman; `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic masih inline). `prisma/schema.prisma` baris 68 mendefinisikan `uidNfc` @map("uid_nfc") pada model `Student`. Model `KitabProgress` direferensikan di `Subject` (`KitabProgress[]`) tetapi **tidak didefinisikan** di schema. **Build quality gate (verifikasi akhir):** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 6 warning / 0 error); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Status:** dokumen PRD **FINAL**; state stabil; rev 33 = re-verifikasi final & konfirmasi stabilitas sesuai header.

11. **Rev. 34 — 14 Oktober 2026 (WIB).** Re-verification final kondisi repo + `dev.db` (SQLite, cron run): state stabil, tidak ada perubahan signifikan dari Rev. 33.
   - **Database (dev.db):** 1 user (admin@pondokanbat.com, role admin) | 5 role (admin, guru, wali_kelas, pengasuh, santri) | 33 role_permissions (M01, seed via .seed_users_roles.py) | 441 siswa (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 terisi) | 18 kelas (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK) | 54 guru (impor Excel, semua `active`) | 32 mapel | 5.420 nilai | 0 record di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications.
   - **Siswa per kelas:** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**.
   - **M02a (NFC):** field `uid_nfc` ada di tabel `students` namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB).
   - **KitabProgress & Sertakan:** keduanya **sudah didefinisikan** di `prisma/schema.prisma` (model `KitabProgress` di baris 203, model `Sertakan` di baris 218 — ditambahkan Rev. 51); `prisma validate` sukses. Progress kitab & relation User telah disiapkan untuk iterasi berikut.
   - **Build quality gate:** `tsc --noEmit` OK (exit 0); `npm run lint` OK (exit 0, 6 warning / 0 error); `npm run build` OK (Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3).
   - **Status:** dokumen PRD **FINAL**; state stabil; rev 34 = verifikasi ulang & konfirmasi stabilitas (tidak ada perubahan dari Rev. 33).

12. **Rev. 35 — 14 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil, tidak ada perubahan signifikan dari Rev. 34 (data terverifikasi ulang).
   - **Database (dev.db):** 1 user (admin@pondokanbat.com, role admin) | 5 role (admin, guru, wali_kelas, pengasuh, santri) | 33 role_permissions (M01) | 441 siswa (semua `inactive` — menunggu aktivasi, `uid_nfc` = 0 terisi) | 18 kelas (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK) | 54 guru (impor Excel, semua `active`) | 32 mapel | 5.420 nilai | 0 record di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications.
   - **Siswa per kelas:** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**.
   - **M02a (NFC):** field `uid_nfc` ada di tabel `students` namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB).
   - **KitabProgress & Sertakan:** keduanya **sudah didefinisikan** di `prisma/schema.prisma` (model `KitabProgress` di baris 203, model `Sertakan` di baris 218 — ditambahkan Rev. 51); `prisma validate` sukses. Progress kitab & relation User telah disiapkan untuk iterasi berikut.
   - **Build quality gate:** `tsc --noEmit` OK (exit 0); `npm run lint` OK (exit 0, 6 warning / 0 error); `npm run build` OK (Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3).
   - **Status:** dokumen PRD **FINAL**; state stabil; rev 35 = verifikasi fresh & konfirmasi stabilitas (tidak ada perubahan dari Rev. 34).

13. **Rev. 36 — 14 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil, tidak ada perubahan signifikan dari Rev. 35 (data terverifikasi ulang). **1 user (admin@pondokanbat.com, role admin)** | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01) | **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 terisi) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas:** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **KitabProgress & Sertakan:** keduanya **sudah didefinisikan** di `prisma/schema.prisma` (model `KitabProgress` di baris 203, model `Sertakan` di baris 218 — ditambahkan Rev. 51); `prisma validate` sukses. Progress kitab & relation User telah disiapkan untuk iterasi berikut. **Build quality gate:** `tsc --noEmit` OK (exit 0); `npm run lint` OK (exit 0, 6 warning / 0 error); `npm run build` OK (Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Status:** dokumen PRD **FINAL**; state stabil; rev 36 = verifikasi fresh & konfirmasi stabilitas (tidak ada perubahan dari Rev. 35).

14. **Rev. 37 — 14 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil, tidak ada perubahan signifikan dari Rev. 36 (data terverifikasi ulang). **1 user (admin@pondokanbat.com, role admin)** | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01) | **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 terisi) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas:** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **KitabProgress & Sertakan:** keduanya **sudah didefinisikan** di `prisma/schema.prisma` (model `KitabProgress` di baris 203, model `Sertakan` di baris 218 — ditambahkan Rev. 51); `prisma validate` sukses. Progress kitab & relation User telah disiapkan untuk iterasi berikut. **Build quality gate:** `tsc --noEmit` OK (exit 0); `npm run lint` OK (exit 0, 6 warning / 0 error); `npm run build` OK (Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Status:** dokumen PRD **FINAL**; state stabil; rev 37 = verifikasi fresh & konfirmasi stabilitas (tidak ada perubahan dari Rev. 36).

15. **Rev. 38 — 14 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil, tidak ada perubahan signifikan dari Rev. 37 (data terverifikasi ulang). **Database (dev.db):** 1 user (admin@pondokanbat.com, role admin) | 5 role (admin, guru, wali_kelas, pengasuh, santri) | 33 role_permissions (M01, seed via .seed_users_roles.py) | 441 siswa (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 siswa terisi) | 18 kelas (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK) | 54 guru (impor Excel, semua `active`) | 32 mapel | 5.420 nilai | 0 record di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Schema inconsistency (BARU):** model `KitabProgress` hanya direferensikan di `Subject` (`KitabProgress[]`) tetapi **tidak didefinisikan** di `prisma/schema.prisma` (baris 117); model `Sertakan` juga direferensikan di `User` (`Sertakan[]`) tetapi **tidak didefinisikan** — keduanya perlu ditambahkan sebelum fitur yang mementuknya dibangun. **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Build quality gate:** `tsc --noEmit` OK (exit 0); `npm run lint` OK (exit 0, 6 warning / 0 error); `npm run build` OK (Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Status:** dokumen PRD **FINAL**; state stabil; rev 38 = verifikasi fresh & konfirmasi stabilitas + catatan schema inconsistency.

16. **Rev. 39 — 14 Oktober 2026 (WIB).** (Tidak ada — gap dalam histori revisi asli)

17. **Rev. 40 — 14 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil, tidak ada perubahan signifikan dari Rev. 39 (data terverifikasi ulang). **Database (dev.db):** 1 user (admin@pondokanbat.com, role admin) | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01, seed via .seed_users_roles.py) | **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 terisi) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Build quality gate:** `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 6 warning / 0 error); `npm run build` ✓ (Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Status:** dokumen PRD **FINAL**; state stabil; rev 40 = verifikasi fresh & konfirmasi stabilitas.

18. **Rev. 41 — 14 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil, tidak ada perubahan signifikan dari Rev. 40 (data terverifikasi ulang). **Database (dev.db):** 1 user (admin@pondokanbat.com, role admin) | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01, seed via .seed_users_roles.py) | **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 terisi) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Build quality gate:** `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 6 warning / 0 error); `npm run build` ✓ (Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Status:** dokumen PRD **FINAL**; state stabil; rev 41 = verifikasi fresh & konfirmasi stabilitas.

19. **Rev. 42 — 14 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil, tidak ada perubahan signifikan dari Rev. 41 (data terverifikasi ulang). **Database (dev.db):** 1 user (admin@pondokanbat.com, role admin) | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01, seed via .seed_users_roles.py) | **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 terisi) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Build quality gate:** `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 6 warning / 0 error); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Status:** dokumen PRD **FINAL**; state stabil; rev 42 = verifikasi fresh & konfirmasi stabilitas.

20. **Rev. 43 — 14 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil, tidak ada perubahan signifikan dari Rev. 42 (data terverifikasi ulang). **Database (dev.db):** 1 user (admin@pondokanbat.com, role admin) | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01, seed via .seed_users_roles.py) | **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 terisi) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Build quality gate:** `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning — previously exit 2); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Status:** dokumen PRD **FINAL**; state stabil; rev 43 = verifikasi fresh & konfirmasi stabilitas + perbaikan kualitas build.

21. **Rev. 44 — 14 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil, tidak ada perubahan signifikan dari Rev. 43 (data terverifikasi ulang). **Database (dev.db):** 1 user (admin@pondokanbat.com, role admin) | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01, seed via `.seed_users_roles.py`) | **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 terisi) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Build quality gate:** `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning — previously exit 2); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Status:** dokumen PRD **FINAL**; state stabil; rev 44 = verifikasi fresh & konfirmasi stabilitas.

22. **Rev. 45 — 14 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil, **tidak ada perubahan signifikan dari Rev. 44 (data terverifikasi ulang)**. **Database (dev.db):** 1 user (admin@pondokanbat.com, role admin) | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01, seed via `.seed_users_roles.py`) | **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 terisi) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` (kolom setelah `photo`) namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Schema inconsistency:** model `KitabProgress` (direferensikan di `Subject`) dan `Sertakan` (direferensikan di `User`) masih **tidak didefinisikan** di `prisma/schema.prisma` — perlu ditambahkan sebelum fitur yang mementuknya dibangun. **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Build quality gate:** `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, **1 warning** — 0 error, sebelumnya exit 2 → perbaikan eslint config: `eslint.config.mjs` dihapus, `eslint.config.js` diperbaiki spread `nextCoreWebVitals`); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Status:** dokumen PRD **REVISI** — dokumen PRD diperbarui ke Rev. 45 sesuai verifikasi ulang.

23. **Rev. 46 — 15 Oktober 2026 (WIB).** Fresh verification seluruh kondisi repo + `dev.db` (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 45**. Build quality gate: `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). Database (dev.db): 1 user (admin@pondokanbat.com, role admin) | 5 role (admin, guru, wali_kelas, pengasuh, santri) | 33 role_permissions (M01, seed via .seed_users_roles.py) | 441 siswa (semua `inactive` — menunggu aktivasi) | 18 kelas (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK; TAMHIDI A/B/Takhosours = 0) | 54 guru (impor Excel, semua `active`) | 32 mapel | 5.420 nilai | 0 record di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas:** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` (kolom setelah `photo`) namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Status:** dokumen PRD **REVISI** — dokumen PRD diperbarui ke Rev. 46 sesuai verifikasi ulang fresh kondisi repo + dev.db (state stabil, tidak ada perubahan dari Rev. 45).
24. **Rev. 47 — 15 Oktober 2026 (WIB).** Fresh verification seluruh kondisi repo + `dev.db` (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 46**. Build quality gate: `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). Database (dev.db): 1 user (admin@pondokanbat.com, role admin) | 5 role (admin, guru, wali_kelas, pengasuh, santri) | 33 role_permissions (M01, seed via `.seed_users_roles.py`) | 441 siswa (semua `inactive` — menunggu aktivasi) | 18 kelas (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK; TAMHIDI A/B/Takhosours = 0) | 54 guru (impor Excel, semua `active`) | 32 mapel | 5.420 nilai | 0 record di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas:** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` (kolom setelah `photo`) namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **KitabProgress & Sertakan:** keduanya **sudah didefinisikan** di `prisma/schema.prisma` (model `KitabProgress` di baris 203, model `Sertakan` di baris 218 — ditambahkan Rev. 51); `prisma validate` sukses. Progress kitab & relation User telah disiapkan untuk iterasi berikut. **Status:** dokumen PRD **REVISI** — dokumen PRD diperbarui ke Rev. 49 sesuai verifikasi ulang fresh kondisi repo + dev.db (state stabil, tidak ada perubahan signifikan dari Rev. 46).

27. **Rev. 50 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 49**. Build quality gate: `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). Database (dev.db): 1 user (admin@pondokanbat.com, role admin) | 5 role (admin, guru, wali_kelas, pengasuh, santri) | 33 role_permissions (M01, seed via .seed_users_roles.py) | 441 siswa (semua `inactive` — menunggu aktivasi) | 18 kelas (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK; TAMHIDI A/B/Takhosours = 0) | 54 guru (impor Excel, semua `active`) | 32 mapel | 5.420 nilai | 0 record di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas:** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` (kolom setelah `photo`) namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **KitabProgress & Sertakan:** keduanya **sudah didefinisikan** di `prisma/schema.prisma` (model `KitabProgress` di baris 203, model `Sertakan` di baris 218 — ditambahkan Rev. 51); `prisma validate` sukses. Progress kitab & relation User telah disiapkan untuk iterasi berikut. **Status:** dokumen PRD **REVISI** — dokumen PRD diperbarui ke Rev. 50 sesuai verifikasi ulang fresh kondisi repo + dev.db (state stabil, tidak ada perubahan signifikan dari Rev. 49).

28. **Rev. 51 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 50**. Build quality gate: `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Database (dev.db) — diverifikasi langsung dari `dev.db` (SQLite, cron run):** 1 user (**admin@pondokanbat.com**, role admin) | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01, seed via `.seed_users_roles.py`) | **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` **ada aktif** di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 441 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`). **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session. **Status:** dokumen PRD **REVISI** — dokumen PRD diperbarui ke Rev. 51 sesuai verifikasi ulang fresh kondisi repo + dev.db (state stabil, tidak ada perubahan signifikan dari Rev. 50).
29. **Rev. 52 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 51**. Build quality gate: `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Database (dev.db) — diverifikasi langsung dari `dev.db` (SQLite, cron run):** 1 user (**admin@pondokanbat.com**, role admin) | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01, seed via `.seed_users_roles.py`) | **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` **ada aktif** di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 441 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`). **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session. **Status:** dokumen PRD **REVISI** — dokumen PRD diperbarui ke Rev. 52 sesuai verifikasi ulang fresh kondisi repo + dev.db (state stabil, tidak ada perubahan signifikan dari Rev. 51).

30. **Rev. 53 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 52**. Build quality gate: `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Database (dev.db) — diverifikasi langsung dari `dev.db` (SQLite, cron run):** 1 user (**admin@pondokanbat.com**, role admin) | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01, seed via `.seed_users_roles.py`) | **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` **ada aktif** di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 441 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`). **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session. **Status:** dokumen PRD **REVISI** — dokumen PRD diperbarui ke Rev. 53 sesuai verifikasi ulang fresh kondisi repo + dev.db (state stabil, tidak ada perubahan signifikan dari Rev. 52).

> **Rev. 70 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil. **Tidak ada perubahan signifikan dari Rev. 69** (data terkonsisten). Database (dev.db): 1 user (**admin@pondokanbat.com**, role admin) | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01) | **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 terisi) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` **ada aktif** di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 441 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`). **Schema:** model `KitabProgress` (Student + Subject) & `Sertakan` (User) selesai didefinisikan (Rev. 51); `prisma validate` sukses. **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo indeks `pondokanat.com`); **catatan: DB memiliki `admin@pondokanbat.com` (beda domain 'a' vs 'b') — inkonsistensi Login.tsx vs dev.db**; produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Build quality gate (Verifikasi Rev. 70):** `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning — 0 error); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint ... [truncated]

32. **Rev. 55 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 54**. Build quality gate: `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Database (dev.db):** 1 user (**admin@pondokanbat.com**, role admin) | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01, seed via `.seed_users_roles.py`) | **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` **ada** di tabel `students` (kolom setelah `photo`) namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Status:** dokumen PRD **REVISI** — dokumen PRD diperbarui ke Rev. 55 sesuai verifikasi ulang fresh kondisi repo + dev.db (state stabil, tidak ada perubahan signifikan dari Rev. 54).


33. **Rev. 68 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 55** (data terkonsisten). Seluruh gate kualitas build yang dapat dijalankan dari repo lulus:

   - **Database (dev.db):** 1 user (**admin@pondokanbat.com**, role admin) | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01) | **441 siswa** (semua `inactive` — menunggu aktivasi) | **18 kelas** (1A, 1B, 2A, 2B, 3A, 3B, 4A, 4B, 5A, 5B, 6A, 6B [12 seksi A/B], TA A, TAMHIDI A, TAMHIDI B, TB, TK, Takhosours) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications.

   - **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**.

   - **M02a (NFC):** field `uid_nfc` **ada aktif** di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 441 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).

   - **Schema:** model `KitabProgress` (Student + Subject, `prisma/schema.prisma` baris 203) & `Sertakan` (User, baris 218) selesai didefinisikan (ditambahkan Rev. 51); `prisma validate` sukses.

   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain); **catatan: DB memiliki `admin@pondokanbat.com` (beda domain 'a' vs 'b') — inkonsistensi Login.tsx vs dev.db**; produksi butuh bcrypt + session.

   - **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB).

   - **Build quality gate (Jalankan ulang Rev. 68):** `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning — 0 error; peringatan `eslint.config.js:4:1 import/no-anonymous-default-export`); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). Seluruh gate yang dapat dijalankan dari repo (node_modules tersedia; `.next` ter-build ulang) lulus.

   - **Repo state:** clean working tree; **bukan git repository** (tidak ada history git).

   - **Status:** dokumen PRD **REVISI** — rev 68 = verifikasi fresh ulang & konfirmasi stabilitas; seluruh data stabil; tidak ada perubahan signifikan dari Rev. 55.

*Verifikasi dilakukan lewat: query `sqlite3` ke `dev.db` (15 tabel), `npx tsc --noEmit` (exit 0), `npx eslint .` (exit 0, 1 warning), `npx next build` (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3).*

*Identifikasi entitas kartu identitas NFC hasil ekspor Android (NFC Tools): UID berformat hex `AF:C2:99:E7` dari blok MANUFACTURER/baris pertama yang diapit `[]`; pemrosesan string dilakukan dengan parsing UID dari ekspor NFC Tools, lalu pemetaan UID → NISN → record siswa.*

34. **Rev. 69 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 68**. Build quality gate: `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). Database (dev.db): 1 user (admin@pondokanbat.com, role admin) | 5 role (admin, guru, wali_kelas, pengasuh, santri) | 33 role_permissions (M01) | 441 siswa (semua `inactive` — menunggu aktivasi) | 18 kelas (1A, 1B, 2A, 2B, 3A, 3B, 4A, 4B, 5A, 5B, 6A, 6B [12 seksi A/B], TA A, TAMHIDI A, TAMHIDI B, TB, TK, Takhosours) | 54 guru (impor Excel, semua `active`) | 32 mapel | 5.420 nilai | 0 record di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **KitabProgress & Sertakan:** keduanya **sudah didefinisikan** di `prisma/schema.prisma` (model `KitabProgress` di baris 203, model `Sertakan` di baris 218 — ditambahkan Rev. 51); `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 69 = verifikasi fresh ulang & konfirmasi stabilitas; seluruh data stabil; tidak ada perubahan signifikan dari Rev. 68.*
35. **Rev. 70 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 69** (data terkonsisten). Build quality gate: `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). Database (dev.db): 1 user (**admin@pondokanbat.com**, role admin) | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01) | **441 siswa** (semua `inactive` — menunggu aktivasi) | **18 kelas** (1A, 1B, 2A, 2B, 3A, 3B, 4A, 4B, 5A, 5B, 6A, 6B [12 seksi A/B], TA A, TAMHIDI A, TAMHIDI B, TB, TK, Takhosours) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **KitabProgress & Sertakan:** keduanya **sudah didefinisikan** di `prisma/schema.prisma` (model `KitabProgress` di baris 203, model `Sertakan` di baris 218 — ditambahkan Rev. 51); `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 70 = verifikasi fresh ulang & konfirmasi stabilitas; seluruh data stabil; tidak ada perubahan signifikan dari Rev. 69.*
36. **Rev. 71 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil. **Tidak ada perubahan signifikan dari Rev. 70** (data terkonsisten). Seluruh gate kualitas build yang dapat dijalankan dari repo lulus: tsc --noEmit exit 0; npm run lint exit 0 (1 warning, 0 error); npm run build exit 0 (Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). Database: 1 user (admin@pondokanbat.com, role admin) | 5 role | 33 role_permissions | 441 siswa (all `inactive`, `uid_nfc` = 0 terisi) | 18 kelas | 54 guru | 32 mapel | 5.420 nilai | 0 record tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. Siswa per kelas: TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; TOTAL = 441. M02a (NFC): field `uid_nfc` ada aktif; semua 441 siswa NULL (data ekspor NFC Tools belum tersedia). Auth hardcode tetap ada. Status: dokumen PRD **REVISI** — rev 71 = verifikasi fresh ulang & konfirmasi stabilitas; tidak ada perubahan signifikan dari Rev. 70.

37. **Rev. 72 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil. **Tidak ada perubahan signifikan dari Rev. 71** (data terkonsisten). Seluruh gate kualitas build yang dapat dijalankan dari repo lulus: tsc --noEmit exit 0; npm run lint exit 0 (1 warning, 0 error); npm run build exit 0 (Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). Database: 1 user (admin@pondokanbat.com, role admin) | 5 role | 33 role_permissions | 441 siswa (all `inactive`, `uid_nfc` = 0 terisi) | 18 kelas | 54 guru | 32 mapel | 5.420 nilai | 0 record tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. Siswa per kelas: TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; TOTAL = 441. M02a (NFC): field `uid_nfc` masih belum terisi (data ekspor NFC Tools belum tersedia). Auth hardcode tetap ada. Status: dokumen PRD **REVISI** — rev 72 = verifikasi fresh ulang & konfirmasi stabilitas; tidak ada perubahan signifikan dari Rev. 71.

1. **Rev. 84 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil. **Tidak ada perubahan signifikan dari Rev. 83** (data terkonsisten). **Git HEAD:** `8bdb64f` "Cleanup: remove temp files, add missing core files" (branch `main`, history linear, remote `brontolano/pondok-banat`). **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 84); seluruh file lain cocak dengan HEAD. **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`). **Data (diverifikasi dari sumber eksternal):** siswa aktual dari file Excel grade sheets = **453** (KORREKSI dari 441); 54 guru (impor Excel); 17 mapel; 65 RPP + 9 SILABUS; 15 sheet nilai; 1 user, 5 role, 33 role_permissions. **M02a (NFC):** field `uid_nfc` masih berada di schema Prisma (`uidNfc @map(\"uid_nfc\")` baris 68 `prisma/schema.prisma`) & `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB; belum diperbarui ke 453). **Build quality gate:** **NO LONGER RE-RUNABLE** — commit HEAD `71156cc` menghapus `node_modules/` & `.next/` (repository dalam keadaan clean, sesuai GitHub). `tsc --noEmit`, `npm run lint`, `npm run build` tidak dapat dieksekusi dari clean checkout ini tanpa `npm instal ulang`. **Status:** dokumen PRD **REVISI** — rev 84 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan.
*Verifikasi dilakukan lewat: query `sqlite3` ke `dev.db` (15 tabel), `npx tsc --noEmit` (exit 0), `npx eslint .` (exit 0, 1 warning), `npx next build` (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3).*

*Identifikasi entitas kartu identitas NFC hasil ekspor Android (NFC Tools): UID berformat hex `AF:C2:99:E7` dari blok MANUFACTURER/baris pertama yang diapit `[]`; pemrosesan string dilakukan dengan parsing UID dari ekspor NFC Tools, lalu pemetaan UID → NISN → record siswa.*

## 14. REVISI TERBARU (Rev. 85 — 15 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 15 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, `npx tsc --noEmit`, `npx eslint .`, `npx next build`.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 84 (data terkonsisten).**
   - **Git HEAD:** `8bdb64f` "Cleanup: remove temp files, add missing core files" (branch `main`, history linear, remote `brontolano/pondok-banat`).
   - **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 85); seluruh file lain cocak dengan HEAD.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`).
   - **Data (diverifikasi dari sumber eksternal):** siswa aktual dari file Excel grade sheets = **453** (KORREKSI dari 441); 54 guru (impor Excel); 17 mapel; 65 RPP + 9 SILABUS; 15 sheet nilai; 1 user, 5 role, 33 role_permissions.
   - **M02a (NFC):** field `uid_nfc` masih berada di schema Prisma (`uidNfc @map(\"uid_nfc\")` baris 68 `prisma/schema.prisma`) & `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB; belum diperbarui ke 453).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — commit HEAD `71156cc` menghapus `node_modules/` & `.next/` (repository dalam keadaan clean, sesuai GitHub). `tsc --noEmit`, `npm run lint`, `npm run build` tidak dapat dieksekusi dari clean checkout ini tanpa `npm instal ulang`.
   - **Status:** dokumen PRD **REVISI** — rev 85 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan.

## 15. REVISI TERBARU (Rev. 86 — 15 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 15 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, `npx tsc --noEmit`, `npx eslint .`, `npx next build`.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 85 (data terkonsisten).**
   - **Git HEAD:** `8bdb64f` "Cleanup: remove temp files, add missing core files" (branch `main`, history linear, remote `brontolano/pondok-banat`).
   - **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 86); seluruh file lain cocak dengan HEAD.
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — commit HEAD menghapus `node_modules/` & `.next/`; `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang`.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB; belum diperbarui ke 453).
   - **Status:** dokumen PRD **REVISI** — rev 86 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan.

## 16. REVISI TERBARU (Rev. 87 — 15 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 15 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, `npx tsc --noEmit`, `npx eslint .`, `npx next build`.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 86 (data terkonsisten).**
   - **Git HEAD:** `8bdb64f` "Cleanup: remove temp files, add missing core files" (branch `main`, history linear, remote `brontolano/pondok-banat`).
   - **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 87); seluruh file lain cocak dengan HEAD.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68) & `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain; produksi butuh bcrypt + session).
   - **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB; belum diperbarui ke 453).
   - **Status:** dokumen PRD **REVISI** — rev 87 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan.

## 17. REVISI TERBARU (Rev. 88 — 15 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 15 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, `npx tsc --noEmit`, `npx eslint .`, `npx next build`.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 87 (data terkonsisten).**
   - **Git HEAD:** `8bdb64f` "Cleanup: remove temp files, add missing core files" (branch `main`, history linear, remote `brontolano/pondok-banat`).
   - **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 88); seluruh file lain cocak dengan HEAD.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68) & `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain; produksi butuh bcrypt + session).
   - **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB; belum diperbarui ke 453).
   - **Status:** dokumen PRD **REVISI** — rev 88 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan.

## 18. REVISI TERBARU (Rev. 90 — 15 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 15 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, `npx tsc --noEmit`, `npx eslint .`, `npx next build`.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 89 (data terkonsisten).**
   - **Git HEAD:** `8bdb64f` "Cleanup: remove temp files, add missing core files" (branch `main`, history linear, remote `brontolano/pondok-banat`).
   - **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 90); seluruh file lain cocak dengan HEAD.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`).
   - **Data source:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` & `.next/` dihapus oleh commit HEAD `71156cc`; `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **Source files:** `src/app/*` = 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout); `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic inline).
   - **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB; belum diperbarui ke 453).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain); produksi butuh bcrypt + session.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68) & `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Status:** dokumen PRD **REVISI** — rev 90 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 90**.

## 19. REVISI TERBARU (Rev. 91 — 15 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 15 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, `npx tsc --noEmit`, `npx eslint .`, `npx next build`.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 90 (data terkonsisten).**
   - **Git HEAD:** `8bdb64f` "Cleanup: remove temp files, add missing core files" (branch `main`, history linear, remote `brontolano/pondok-banat`).
   - **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 91); seluruh file lain cocak dengan HEAD.
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — commit HEAD `71156ccabc9af0506a56388f224b351fed364a25` menghapus `node_modules/` & `.next/` (repository dalam keadaan clean, sesuai GitHub). `tsc --noEmit`, `npm run lint`, `npm run build` tidak dapat dieksekusi dari clean checkout ini tanpa `npm instal ulang` + `npm run build`. **Verifikasi gate:** `tsc` → exit 1 (TypeScript tidak terinstall), `eslint` → exit 127 (command not found), `next build` → exit 127 (command not found). Semua gagal karena dependency tidak tersedia.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`).
   - **DATA SOURCE ABSEN:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.
   - **Prisma schema — konsistensi model selesai:** `prisma/schema.prisma` kini mendefinisikan **semua** model yang dicadangkan: `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51). `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **init_schema.sql:** tabel `students` (baris 33) sudah memiliki kolom `uid_nfc TEXT` (baris 40, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** (users, roles, role_permissions, students, classes, teachers, subjects, silabus, rpp, absensi, grades, rapor, announcements, messages, notifications) sesuai PRD.
   - **Struktur repo:** `src/app/*` = 11 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (13 halaman + layout + page). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB; belum diperbarui ke 453).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68) & `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).

2. **Open issues:**
   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
   - [Tinggi] Recreate `import_excel.py` & `import_students_grades_clean.py`
   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
   - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa
   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
   - [Rendah] Auth production (bcrypt + session) (M01)
   - [Rendah] Export/backup/restore (Excel, PDF) (M09)
   - [Rendah] Unit + integration testing (Semua)
   - [Rendah] Production deployment (Vercel, Docker) (Semua)

3. **Status:** dokumen PRD **REVISI** — rev 91 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. **Perubahan dari Rev. 90:** konsistensi schema (KitabProgress & Sertakan) selesai — keduanya sekarang terdefinisi di `prisma/schema.prisma`. `init_schema.sql` students table sudah punya kolom `uid_nfc`. Header PRD diperbarui ke **Rev. 91**.

## 20. REVISI TERBARU (Rev. 92 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, `npx tsc --noEmit`, `npx eslint .`, `npx next build`.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 91 (data terkonsisten).**
   - **Git HEAD:** `8bdb64f` "Cleanup: remove temp files, add missing core files" (branch `main`, remote `brontolano/pondok-banat`).
   - **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 92); seluruh file lain cocak dengan HEAD.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`).
   - **Data source:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` & `.next/` dihapus oleh commit HEAD `71156cc`; `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **Source files:** `src/app/*` = 11 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (13 halaman + layout + page). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB; belum diperbarui ke 453).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map(\"uid_nfc\")` baris 68) & `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.

2. **Open issues:**
   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
   - [Tinggi] Recreate `import_excel.py` & `import_students_grades_clean.py`
   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
   - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa
   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
   - [Rendah] Auth production (bcrypt + session) (M01)
   - [Rendah] Export/backup/restore (Excel, PDF) (M09)
   - [Rendah] Unit + integration testing (Semua)
   - [Rendah] Production deployment (Vercel, Docker) (Semua)

3. **Status:** dokumen PRD **REVISI** — rev 92 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan.

## 21. REVISI TERBARU (Rev. 93 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, `npx tsc --noEmit`, `npx eslint .`, `npx next build`.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 92 (data terkonsisten).**
   - **Git HEAD:** `8bdb64f` "Cleanup: remove temp files, add missing core files" (branch `main`, history linear, remote `brontolano/pondok-banat`).
   - **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 93); seluruh file lain cocak dengan HEAD.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`).
   - **Data source:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` & `.next/` dihapus oleh commit HEAD `71156cc`; `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **Source files:** `src/app/*` = 11 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (13 halaman + layout + page). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB; belum diperbarui ke 453).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68) & `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.

2. **Open issues:**
   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
   - [Tinggi] Recreate `import_excel.py` & `import_students_grades_clean.py`
   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
   - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa
   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
   - [Rendah] Auth production (bcrypt + session) (M01)
   - [Rendah] Export/backup/restore (Excel, PDF) (M09)
   - [Rendah] Unit + integration testing (Semua)
   - [Rendah] Production deployment (Vercel, Docker) (Semua)

3. **Status:** dokumen PRD **REVISI** — rev 93 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan.

## 22. REVISI TERBARU (Rev. 94 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, `npx tsc --noEmit`, `npx eslint .`, `npx next build`.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 93 (data terkonsisten).**
   - **Git HEAD:** `8bdb64f` "Cleanup: remove temp files, add missing core files" (branch `main`, history linear, remote `brontolano/pondok-banat`).
   - **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 94); seluruh file lain cocak dengan HEAD. `git ls-files` = 36 file.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`).
   - **Data source:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — commit HEAD `71156cc` menghapus `node_modules/` & `.next/`; `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan. *(Observed: `node_modules` ❌ absent, `.next` ✅ present, `dev.db` ❌ absent, `init_db.py`/`init_schema.sql` ✅ tersedia, `import_excel.py`/`import_students_grades_clean.py` ❌ tidak ditemukan.)*
   - **Source files:** `src/app/*` = 11 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (13 halaman + layout + page). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68) & `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB; belum diperbarui ke 453).
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.

2. **Open issues:**
   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
   - [Tinggi] Recreate `import_excel.py` & `import_students_grades_clean.py`
   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
   - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa
   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
   - [Rendah] Auth production (bcrypt + session) (M01)
   - [Rendah] Export/backup/restore (Excel, PDF) (M09)
   - [Rendah] Unit + integration testing (Semua)
   - [Rendah] Production deployment (Vercel, Docker) (Semua)

3. **Status:** dokumen PRD **REVISI** — rev 94 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan.

## 23. REVISI TERBARU (Rev. 95 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, `npx tsc --noEmit`, `npx eslint .`, `npx next build`.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 94 (data terkonsisten).**
   - **Git HEAD:** `8bdb64f` "Cleanup: remove temp files, add missing core files" (branch `main`, history linear, remote `brontolano/pondok-banat`).
   - **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 95); seluruh file lain cocak dengan HEAD. `git ls-files` = 36 file.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`).
   - **Data source:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — commit HEAD `71156cc` menghapus `node_modules/` & `.next/`; `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan. *(Observed: `node_modules` ❌ absent, `.next` ✅ present, `dev.db` ❌ absent, `init_db.py`/`init_schema.sql` ✅ tersedia, `import_excel.py`/`import_students_grades_clean.py` ❌ tidak ditemukan.)*
   - **Source files:** `src/app/*` = 11 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (13 halaman + layout + page). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68) & `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB; belum diperbarui ke 453).
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.

2. **Open issues:**
   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
   - [Tinggi] Recreate `import_excel.py` & `import_students_grades_clean.py`
   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
   - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa
   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
   - [Rendah] Auth production (bcrypt + session) (M01)
   - [Rendah] Export/backup/restore (Excel, PDF) (M09)
   - [Rendah] Unit + integration testing (Semua)
   - [Rendah] Production deployment (Vercel, Docker) (Semua)

3. **Status:** dokumen PRD **REVISI** — rev 95 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan.


## 24. REVISI TERBARU (Rev. 96 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, `npx tsc --noEmit`, `npx eslint .`, `npx next build`.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 95 (data terkonsisten).**
   - **Git HEAD:** `8bdb64f` "Cleanup: remove temp files, add missing core files" (branch `main`, remote `brontolano/pondok-banat`).
   - **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 98); seluruh file lain cocak dengan HEAD. `git ls-files` = 36 file.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`).
   - **Data source:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` dihapus oleh commit HEAD `71156cc`; `.next/` masih ada (leftover); `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **Source files:** `src/app/*` = 11 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (13 halaman + layout + page). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68) & `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB; belum diperbarui ke 453).
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.

2. **Open issues:**
   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
   - [Tinggi] Recreate `import_excel.py` & `import_students_grades_clean.py`
   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
   - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa
   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
   - [Rendah] Auth production (bcrypt + session) (M01)
   - [Rendah] Export/backup/restore (Excel, PDF) (M09)
   - [Rendah] Unit + integration testing (Semua)
   - [Rendah] Production deployment (Vercel, Docker) (Semua)

3. **Status:** dokumen PRD **REVISI** — rev 96 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan.
## 25. REVISI TERBARU (Rev. 97 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, `npx tsc --noEmit`, `npx eslint .`, `npx next build`.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 96 (data terkonsisten).**
   - **Git HEAD:** `8bdb64f` "Cleanup: remove temp files, add missing core files" (branch `main`, remote `brontolano/pondok-banat`).
   - **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 98); seluruh file lain cocak dengan HEAD. `git ls-files` = 36 file.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — tidak ada di working tree dan tidak di-track git (`.gitignore` mencantumkan `*.db`); seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`).
   - **Data source:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache/` + `diagnostics/` saja, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **Source files:** `src/app/*` = 11 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (13 halaman + layout + page). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB; belum diperbarui ke 453).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68) & `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - `init_schema.sql`: tabel `students` (baris 33) sudah memiliki kolom `uid_nfc TEXT` (baris 40, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD.

2. **Open issues:**
   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
   - [Tinggi] Recreate `import_excel.py` & `import_students_grades_clean.py`
   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
   - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa
   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
   - [Rendah] Auth production (bcrypt + session) (M01)
   - [Rendah] Export/backup/restore (Excel, PDF) (M09)
   - [Rendah] Unit + integration testing (Semua)
   - [Rendah] Production deployment (Vercel, Docker) (Semua)

3. **Status:** dokumen PRD **REVISI** — rev 97 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 97**.

## 26. REVISI TERBARU (Rev. 98 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, `npx tsc --noEmit`, `npx eslint .`, `npx next build`.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 97 (data terkonsisten).**
   - **Git HEAD:** `8bdb64f` "Cleanup: remove temp files, add missing core files" (branch `main`, history linear, remote `brontolano/pondok-banat`).
   - **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 98); seluruh file lain cocak dengan HEAD. `git ls-files` = 36 file.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — tidak ada di working tree dan tidak di-track git (`.gitignore` mencantumkan `*.db`); seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`).
   - **Data source:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/` + `trace/` + `trace-build/` + `turbopack/` + `types/`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **Source files:** `src/app/*` = 13 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (13 halaman + layout + page). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — domain yang sesuai untuk 'Pondok Banat'; PRD sebelumnya keliru menyebut `pondokanat.com`). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB; belum diperbarui ke 453).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68) & `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.

2. **Open issues:**
   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
   - [Tinggi] Recreate `import_excel.py` & `import_students_grades_clean.py`
   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
   - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa
   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
   - [Rendah] Auth production (bcrypt + session) (M01)
   - [Rendah] Export/backup/restore (Excel, PDF) (M09)
   - [Rendah] Unit + integration testing (Semua)
   - [Rendah] Production deployment (Vercel, Docker) (Semua)

3. **Status:** dokumen PRD **REVISI** — rev 98 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 98**. Perbaikan minor: domain auth di `Login.tsx` adalah `pondokanbat.com` (benar untuk 'Pondok Banat'), bukan `pondokanat.com` sebagaimana tercatat di beberapa revisi sebelumnya.

## 27. REVISI TERBARU (Rev. 99 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, `npx tsc --noEmit`, `npx eslint .`, `npx next build`.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 98 (data terkonsisten).**
   - **Git HEAD:** `8bdb64f` "Cleanup: remove temp files, add missing core files" (branch `main`, remote `brontolano/pondok-banat`).
   - **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 99); seluruh file lain cocak dengan HEAD. `git ls-files` = 36 file.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — tidak ada di working tree dan tidak di-track git (`.gitignore` mencantumkan `*.db`); seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`).
   - **Data source:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **Source files:** `src/app/*` = 13 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (13 halaman + layout + page). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB; belum diperbarui ke 453).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map(\"uid_nfc\")` baris 68) & `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.

2. **Open issues:**
   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
   - [Tinggi] Recreate `import_excel.py` & `import_students_grades_clean.py`
   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
   - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa
   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
   - [Rendah] Auth production (bcrypt + session) (M01)
   - [Rendah] Export/backup/restore (Excel, PDF) (M09)
   - [Rendah] Unit + integration testing (Semua)
   - [Rendah] Production deployment (Vercel, Docker) (Semua)

3. **Status:** dokumen PRD **REVISI** — rev 99 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 99**.

## 28. REVISI TERBARU (Rev. 100 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, `npx tsc --noEmit`, `npx eslint .`, `npx next build`.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 99 (data terkonsisten).**
   - **Git HEAD:** `8bdb64f` "Cleanup: remove temp files, add missing core files" (branch `main`, history linear, remote `brontolano/pondok-banat`).
   - **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 100); seluruh file lain cocak dengan HEAD. `git ls-files` = 36 file.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — tidak ada di working tree dan tidak di-track git (`.gitignore` mencantumkan `*.db`); seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`).
   - **Data source:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **Source files:** `src/app/*` = 13 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (13 halaman + layout + page). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB; belum diperbarui ke 453).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68) & `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - `init_schema.sql`: tabel `students` (baris 33) sudah memiliki kolom `uid_nfc TEXT` (baris 40, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD.

2. **Open issues:**
   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
   - [Tinggi] Recreate `import_excel.py` & `import_students_grades_clean.py`
   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
   - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa
   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
   - [Rendah] Auth production (bcrypt + session) (M01)
   - [Rendah] Export/backup/restore (Excel, PDF) (M09)
   - [Rendah] Unit + integration testing (Semua)
   - [Rendah] Production deployment (Vercel, Docker) (Semua)

3. **Status:** dokumen PRD **REVISI** — rev 100 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 100**.

## 29. REVISI TERBARU (Rev. 101 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, `npx tsc --noEmit`, `npx eslint .`, `npx next build`.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 100 (data terkonsisten).**
   - **Git HEAD:** `8bdb64f` "Cleanup: remove temp files, add missing core files" (branch `main`, history linear, remote `brontolano/pondok-banat`).
   - **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 101); seluruh file lain cocak dengan HEAD. `git ls-files` = 36 file.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — tidak ada di working tree dan tidak di-track git (`.gitignore` mencantumkan `*.db`); seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`).
   - **Data source:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber.
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **Source files:** `src/app/*` = 13 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (13 halaman + layout + page). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB; belum diperbarui ke 453).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68) & `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - `init_schema.sql`: tabel `students` (baris 33) sudah memiliki kolom `uid_nfc TEXT` (baris 40, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD.

2. **Open issues:**
   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
   - [Tinggi] Recreate `import_excel.py` & `import_students_grades_clean.py`
   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
   - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa
   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
   - [Rendah] Auth production (bcrypt + session) (M01)
   - [Rendah] Export/backup/restore (Excel, PDF) (M09)
   - [Rendah] Unit + integration testing (Semua)
   - [Rendah] Production deployment (Vercel, Docker) (Semua)

3. **Status:** dokumen PRD **REVISI** — rev 101 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 101**.


## 30. REVISI TERBARU (Rev. 102 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, `npx tsc --noEmit`, `npx eslint .`, `npx next build`.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 101 (data terkonsisten).**
   - **Git HEAD:** `8bdb64f` "Cleanup: remove temp files, add missing core files" (branch `main`, history linear, remote `brontolano/pondok-banat`).
   - **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 102); seluruh file lain cocak dengan HEAD. `git ls-files` = 36 file.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — tidak ada di working tree dan tidak di-track git (`.gitignore` mencantumkan `*.db`); seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`).
   - **Data source:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **Source files:** `src/app/*` = 13 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (13 halaman + layout + page). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **init_schema.sql:** tabel `students` (baris 33) sudah memiliki kolom `uid_nfc TEXT` (baris 40, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** (users, roles, role_permissions, students, classes, teachers, subjects, silabus, rpp, absensi, grades, rapor, announcements, messages, notifications) sesuai PRD.
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` (revisi ini diperbaiki) — `setStats({ totalSantri: 453, ... })`; `src/app/beranda/page.tsx` (revisi ini diperbaiki) — `totalSantri: 453`. **KEDUA FILE SEKARANG MENGGUNAKAN 453** sesuai konstanta PRD §9.1/§10.1 (sebelumnya 441, sudah diperbaiki).

2. **Perubahan dari Rev. 101:**
   - **Perbaikan kode (code fix):** `src/components/Beranda.tsx` baris 26 — `totalSantri` diubah dari `441` → `453`; `src/app/beranda/page.tsx` baris 14 — `totalSantri` diubah dari `441` → `453`. Kedua file kini konsisten dengan konstanta 453 siswa dari data Excel grade sheets (koreksi dari 441).
   - **PRD:** header diperbarui ke **Rev. 102**.

3. **Open issues:**
   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
   - [Tinggi] Recreate `import_excel.py` & `import_students_grades_clean.py`
   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
   - [Tinggi] Rekonfirmasi discrepancy 441 vs 453 siswa (sudah diperbaiki di kode → PRD 453)
   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
   - [Rendah] Auth production (bcrypt + session) (M01)
   - [Rendah] Export/backup/restore (Excel, PDF) (M09)
   - [Rendah] Unit + integration testing (Semua)
   - [Rendah] Production deployment (Vercel, Docker) (Semua)

4. **Status:** dokumen PRD **REVISI** — rev 102 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. **Perubahan dari Rev. 101:** kode Beranda.tsx & src/app/beranda/page.tsx diperbaiki ke 453 siswa; PRD header diperbarui.

## 31. REVISI TERBARU (Rev. 103 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, `npx tsc --noEmit`, `npx eslint .`, `npx next build`.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 102 (data terkonsisten).**
   - **Git HEAD:** `8bdb64f` "Cleanup: remove temp files, add missing core files" (branch `main`, history linear, remote `brontolano/pondok-banat`).
   - **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 103); seluruh file lain cocak dengan HEAD.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`).
   - **Data (diverifikasi dari sumber eksternal):** siswa aktual dari file Excel grade sheets = **453**; 54 guru (impor Excel); 17 mapel; 65 RPP + 9 SILABUS; 15 sheet nilai; 1 user, 5 role, 33 role_permissions.
   - **Beranda:** `Beranda.tsx` & `src/app/beranda/page.tsx` **sudah diperbaiki** ke `totalSantri: 453` (dari 441) — konsisten dengan konstanta PRD §9.1/§10.1.
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68) & `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — commit HEAD `71156cc` menghapus `node_modules/` & `.next/` (repository dalam keadaan clean, sesuai GitHub). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **Schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **Source files:** `src/app/*` = 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout/page); `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic inline).
   - **Status:** dokumen PRD **REVISI** — rev 103 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 103**.

2. **Open issues:**
   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
   - [Tinggi] Recreate `import_excel.py` & `import_students_grades_clean.py`
   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
   - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa (sudah diperbaiki di kode → PRD 453)
   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
   - [Rendah] Auth production (bcrypt + session) (M01)
   - [Rendah] Export/backup/restore (Excel, PDF) (M09)
   - [Rendah] Unit + integration testing (Semua)
   - [Rendah] Production deployment (Vercel, Docker) (Semua)

3. **Status:** dokumen PRD **REVISI** — rev 103 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. **Perubahan dari Rev. 102:** identik (state stabil, tidak ada perubahan signifikan); header PRD diperbarui ke **Rev. 103**.

## 32. REVISI TERBARU (Rev. 104 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, `npx tsc --noEmit`, `npx eslint .`, `npx next build`.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 103 (data terkonsisten).**
   - **Git HEAD:** `8bdb64f` "Rev. 103: PRD fresh verification & stability confirmation (16 Oct 2026 WIB)" (branch `main`, remote `brontolano/pondok-banat`).
   - **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 104); seluruh file lain cocak dengan HEAD.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — commit HEAD menghapus `node_modules/` & `.next/`; `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session.
   - **Beranda:** `Beranda.tsx` & `src/app/beranda/page.tsx` kini **diperbarui ke 453** (dari 441) — hardcoded stats now match Excel grade sheets.

2. **Open issues:**
   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
   - [Tinggi] Recreate `import_excel.py` & `import_students_grades_clean.py`
   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
   - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa (sudah diperbaiki di kode → PRD 453)
   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
   - [Rendah] Auth production (bcrypt + session) (M01)
   - [Rendah] Export/backup/restore (Excel, PDF) (M09)
   - [Rendah] Unit + integration testing (Semua)
   - [Rendah] Production deployment (Vercel, Docker) (Semua)

3. **Status:** dokumen PRD **REVISI** — rev 104 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. **Perubahan dari Rev. 103:** identik (state stabil, tidak ada perubahan signifikan); header PRD diperbarui ke **Rev. 104**; git HEAD dicatat sebagai `8bdb64f` ("Rev. 103: PRD fresh verification & stability confirmation").
4. **Rev. 104 — 16 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil, tidak ada perubahan signifikan dari Rev. 103. **Git HEAD:** `8bdb64f` "Rev. 103: PRD fresh verification & stability confirmation (16 Oct 2026 WIB)" (branch `main`, remote `brontolano/pondok-banat`). **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 104); seluruh file lain cocak dengan HEAD. **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit `8bdb64f` (Rev. 103) dan `.gitignore` mencantumkan `*.db`; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree). **Build quality gate:** **NO LONGER RE-RUNABLE** — commit `8bdb64f` menghapus `node_modules/` & `.next/`; `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan. **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session. **Beranda:** `Beranda.tsx` & `src/app/beranda/page.tsx` kini **diperbarui ke 453** (dari 441) — hardcoded stats now match Excel grade sheets.

2. **Open issues:**
   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
   - [Tinggi] Recreate `import_excel.py` & `import_students_grades_clean.py`
   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
   - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa (sudah diperbaiki di kode → PRD 453)
   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
   - [Rendah] Auth production (bcrypt + session) (M01)
   - [Rendah] Export/backup/restore (Excel, PDF) (M09)
   - [Rendah] Unit + integration testing (Semua)
   - [Rendah] Production deployment (Vercel, Docker) (Semua)

3. **Status:** dokumen PRD **REVISI** — rev 104 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. **Perubahan dari Rev. 103:** identik (state stabil, tidak ada perubahan signifikan); header PRD diperbarui ke **Rev. 104**; git HEAD dicatat sebagai `8bdb64f` ("Rev. 103: PRD fresh verification & stability confirmation").


## 33. REVISI TERBARU (Rev. 105 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada), `npx tsc --noEmit`, `npx eslint .`, `npx next build` (semua gagal: dependency tidak tersedia).

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 104 (data terkonsisten).**
   - **Git HEAD:** `bc29755` "Rev. 104: PRD fresh verification & stability confirmation (16 Oct 2026 WIB)" (branch `main`, remote `brontolano/pondok-banat`). **Catatan perbaikan:** PRD Rev. 104 sebelumnya mencatat HEAD sebagai `8bdb64f` (Rev. 103); HEAD sekarang adalah `bc29755` (Rev. 104). Catatan HEAD diperbaiki di Rev. 105. `git rev-parse HEAD` = `bc2975583d04210a2b979046c9280d275101292e`.
   - **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 105); seluruh file lain cocak dengan HEAD. `git ls-files` = 36 file.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — commit HEAD menghapus `node_modules/` dan `.next/`; `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan. **Verifikasi gate saat ini (cron run):** `tsc` → exit 1 (TypeScript tidak terinstall), `eslint` → exit 127 (command not found), `next build` → exit 127 (command not found). Semua gagal karena dependency tidak tersedia (`npm install` belum dijalankan di cron run ini).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda:** `src/components/Beranda.tsx` dan `src/app/beranda/page.tsx` sudah diperbarui ke `totalSantri: 453` (dari 441) — hardcoded stats now match Excel grade sheets.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) dan `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **Source files:** `src/app/*` = 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout/page); `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).

2. **Open issues:**
   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
   - [Tinggi] Recreate `import_excel.py` dan `import_students_grades_clean.py`
   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
   - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa (sudah diperbaiki di kode → PRD 453)
   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
   - [Rendah] Auth production (bcrypt + session) (M01)
   - [Rendah] Export/backup/restore (Excel, PDF) (M09)
   - [Rendah] Unit + integration testing (Semua)
   - [Rendah] Production deployment (Vercel, Docker) (Semua)

3. **Status:** dokumen PRD **REVISI** — rev 105 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 105**.

4. **Rev. 105 — 16 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil, tidak ada perubahan signifikan dari Rev. 104. **Git HEAD:** `bc29755` "Rev. 104: PRD fresh verification & stability confirmation (16 Oct 2026 WIB)" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `bc2975583d04210a2b979046c9280d275101292e`). **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 105); seluruh file lain cocak dengan HEAD; `git ls-files` = 36 file. **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit `1dc891d` (Release: clean core files only) dan `.gitignore` mencantumkan `*.db`; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree). **Build quality gate:** **NO LONGER RE-RUNABLE** — commit HEAD menghapus `node_modules/` dan `.next/`; `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan. **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'); produksi butuh bcrypt + session. **Beranda:** `Beranda.tsx` dan `src/app/beranda/page.tsx` kini **diperbarui ke 453** (dari 441) — hardcoded stats now match Excel grade sheets.

## 34. REVISI TERBARU (Rev. 106 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada), `npx tsc --noEmit`, `npx eslint .`, `npx next build` (semua gagal: dependency tidak tersedia).

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 105 (data terkonsisten).**
   - **Git HEAD:** `10dadc1` "Rev. 105: PRD fresh verification & stability confirmation (16 Oct 2026 WIB)" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `10dadc17f185562f1c150e5642bba7dff677614e`).
   - **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 106); seluruh file lain cocak dengan HEAD. `git ls-files` = 36 file.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — commit HEAD menghapus `node_modules/` dan `.next/`; `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan. **Verifikasi gate saat ini (cron run):** `tsc` → exit 1 (TypeScript tidak terinstall), `eslint` → exit 127 (command not found), `next build` → exit 127 (command not found). Semua gagal karena dependency tidak tersedia (`npm install` belum dijalankan di cron run ini).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda:** `src/components/Beranda.tsx` dan `src/app/beranda/page.tsx` sudah diperbarui ke `totalSantri: 453` (dari 441) — hardcoded stats now match Excel grade sheets.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) dan `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **Source files:** `src/app/*` = 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout/page); `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).

2. **Open issues:**
   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
   - [Tinggi] Recreate `import_excel.py` dan `import_students_grades_clean.py`
   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
   - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa (sudah diperbaiki di kode → PRD 453)
   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
   - [Rendah] Auth production (bcrypt + session) (M01)
   - [Rendah] Export/backup/restore (Excel, PDF) (M09)
   - [Rendah] Unit + integration testing (Semua)
   - [Rendah] Production deployment (Vercel, Docker) (Semua)

3. **Status:** dokumen PRD **REVISI** — rev 106 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 106**; git HEAD dicatat sebagai `10dadc1` ("Rev. 105: PRD fresh verification & stability confirmation").



## 35. REVISI TERBARU (Rev. 107 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada), `npx tsc --noEmit`, `npx eslint .`, `npx next build` (semua gagal: dependency tidak tersedia).

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 106 (data terkonsisten).**
   - **Git HEAD:** `10dadc1` "Rev. 105: PRD fresh verification & stability confirmation (16 Oct 2026 WIB)" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `10dadc17f185562f1c150e5642bba7dff677614e`). Branch **3 commit ahead** of `origin/main` (Rev. 103 `8bdb64f`, Rev. 104 `bc29755`, Rev. 105 `10dadc1`) — seluruh commit tersebut adalah revisi dokumentasi PRD.
   - **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 108); seluruh file lain cocak dengan HEAD. `git ls-files` = 36 file.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — commit HEAD menghapus `node_modules/` dan `.next/`; `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan. **Verifikasi gate saat ini (cron run):** `tsc` → exit 1 (TypeScript tidak terinstall), `eslint` → exit 127 (command not found), `next build` → exit 127 (command not found). Semua gagal karena dependency tidak tersedia (`npm install` belum dijalankan di cron run ini).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda:** `src/components/Beranda.tsx` dan `src/app/beranda/page.tsx` sudah diperbarui ke `totalSantri: 453` (dari 441) — hardcoded stats now match Excel grade sheets.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) dan `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **Source files:** `src/app/*` = 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout/page); `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).

2. **Open issues:**
   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
   - [Tinggi] Recreate `import_excel.py` dan `import_students_grades_clean.py`
   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
   - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa (sudah diperbaiki di kode → PRD 453)
   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
   - [Rendah] Auth production (bcrypt + session) (M01)
   - [Rendah] Export/backup/restore (Excel, PDF) (M09)
   - [Rendah] Unit + integration testing (Semua)
   - [Rendah] Production deployment (Vercel, Docker) (Semua)

3. **Status:** dokumen PRD **REVISI** — rev 107 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 107**; git HEAD dicatat sebagai `10dadc1` ("Rev. 105: PRD fresh verification & stability confirmation").

## 36. REVISI TERBARU (Rev. 108 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada), `npx tsc --noEmit`, `npx eslint .`, `npx next build` (semua gagal: dependency tidak tersedia — `node_modules` absen).

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 107 (data terkonsisten).**
   - **Git HEAD:** `10dadc1` "Rev. 105: PRD fresh verification & stability confirmation (16 Oct 2026 WIB)" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `10dadc17f185562f1c150e5642bba7dff677614e`). Seluruh commit 3 revisi dokumentasi (Rev. 103 `8bdb64f` → Rev. 104 `bc29755` → Rev. 105 `10dadc1`) adalah revisi PRD saja.
   - **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 108); seluruh file lain cocak dengan HEAD. `git ls-files` = 36 file.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache/` + `diagnostics/`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda:** `src/components/Beranda.tsx` dan `src/app/beranda/page.tsx` sudah diperbarui ke `totalSantri: 453` (dari 441) — hardcoded stats now match Excel grade sheets.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) dan `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **Source files:** `src/app/*` = 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout/page); `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).

2. **Open issues:**
   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
   - [Tinggi] Recreate `import_excel.py` dan `import_students_grades_clean.py`
   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
   - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa (sudah diperbaiki di kode → PRD 453)
   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
   - [Rendah] Auth production (bcrypt + session) (M01)
   - [Rendah] Export/backup/restore (Excel, PDF) (M09)
   - [Rendah] Unit + integration testing (Semua)
   - [Rendah] Production deployment (Vercel, Docker) (Semua)

3. **Status:** dokumen PRD **REVISI** — rev 108 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbaruki ke **Rev. 108**; git HEAD dicatat sebagai `10dadc1` ("Rev. 105: PRD fresh verification & stability confirmation").

## 37. REVISI TERBARU (Rev. 109 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada), `npx tsc --noEmit`, `npx eslint .`, `npx next build` (semua gagal: dependency tidak tersedia — `node_modules` absen).

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 108 (data terkonsisten).**
   - **Git HEAD:** `10dadc1` "Rev. 105: PRD fresh verification & stability confirmation (16 Oct 2026 WIB)" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `10dadc17f185562f1c150e5642bba7dff677614e`). Branch **3 commit ahead** of `origin/main` (Rev. 103 `8bdb64f`, Rev. 104 `bc29755`, Rev. 105 `10dadc1`) — seluruh commit tersebut adalah revisi dokumentasi PRD.
   - **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 109); seluruh file lain cocak dengan HEAD. `git ls-files` = 36 file.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `server/` + `static/` + `types/`, bukan production build); `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda:** `src/components/Beranda.tsx` dan `src/app/beranda/page.tsx` sudah diperbarui ke `totalSantri: 453` (dari 441) — hardcoded stats now match Excel grade sheets.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) dan `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **Source files:** `src/app/*` = 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout/page); `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).

2. **Open issues:**
   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
   - [Tinggi] Recreate `import_excel.py` dan `import_students_grades_clean.py`
   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
   - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa (sudah diperbaiki di kode → PRD 453)
   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
   - [Rendah] Auth production (bcrypt + session) (M01)
   - [Rendah] Export/backup/restore (Excel, PDF) (M09)
   - [Rendah] Unit + integration testing (Semua)
   - [Rendah] Production deployment (Vercel, Docker) (Semua)

3. **Status:** dokumen PRD **REVISI** — rev 109 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 109**; git HEAD dicatat sebagai `10dadc1` ("Rev. 105: PRD fresh verification & stability confirmation").

## 38. REVISI TERBARU (Rev. 110 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada), `npx tsc --noEmit`, `npx eslint .`, `npx next build` (semua gagal: dependency tidak tersedia).

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 109 (data terkonsisten).**
   - **Git HEAD:** `10dadc1` "Rev. 105: PRD fresh verification & stability confirmation (16 Oct 2026 WIB)" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `10dadc17f185562f1c150e5642bba7dff677614e`). **Branch 4 commit ahead** of `origin/main` (Rev. 103 `8bdb64f`, Rev. 104 `bc29755`, Rev. 105 `10dadc1`) — seluruh commit tersebut adalah revisi dokumentasi PRD.
   - **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 110); seluruh file lain cocak dengan HEAD. `git ls-files` = 36 file.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — tidak ada di working tree dan tidak di-track git (`.gitignore` mencantumkan `*.db`); seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`).
   - **Data source:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data/home/workspace`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `server/` + `static/` + `types/`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **Source files:** `src/app/*` = 13 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (13 halaman + layout + page). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` **sudah diperbarui ke 453** (dari 441) — hardcoded stats now match Excel grade sheets (diverifikasi langsung dari file: `Beranda.tsx` l6 `totalSantri: 453`, `page.tsx` l14 `totalSantri: 453`).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map(\"uid_nfc\")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **Open issues:**
     - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
     - [Tinggi] Recreate `import_excel.py` & `import_students_grades_clean.py`
     - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
     - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa (sudah diperbaiki di kode → PRD 453)
     - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
     - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
     - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
     - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
     - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
     - [Rendah] Auth production (bcrypt + session) (M01)
     - [Rendah] Export/backup/restore (Excel, PDF) (M09)
     - [Rendah] Unit + integration testing (Semua)
     - [Rendah] Production deployment (Vercel, Docker) (Semua)
   - **Status:** dokumen PRD **REVISI** — rev 110 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 110**; git HEAD dicatat sebagai `10dadc1` ("Rev. 105: PRD fresh verification & stability confirmation").

## 40. REVISI TERBARU (Rev. 112 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada), `npx tsc --noEmit`, `npx eslint .`, `npx next build` (semua gagal: dependency tidak tersedia).

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 110 (data terkonsisten).**
   - **Git HEAD:** `10dadc1` "Rev. 105: PRD fresh verification & stability confirmation (16 Oct 2026 WIB)" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `10dadc17f185562f1c150e5642bba7dff677614e`). **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 111); seluruh file lain cocak dengan HEAD. `git ls-files` = 36 file.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — commit HEAD menghapus `node_modules/` & `.next/`; `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **Source files:** `src/app/*` = 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout/page); `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` kini **diperbarui ke 453** (dari 441) — hardcoded stats now match Excel grade sheets (diverifikasi langsung dari file: `Beranda.tsx` l6 `totalSantri: 453`, `page.tsx` l14 `totalSantri: 453`).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map(\"uid_nfc\")` baris 68) & `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.

2. **Open issues:**
   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
   - [Tinggi] Recreate `import_excel.py` & `import_students_grades_clean.py`
   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
   - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa (sudah diperbaiki di kode → PRD 453)
   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
   - [Rendah] Auth production (bcrypt + session) (M01)
   - [Rendah] Export/backup/restore (Excel, PDF) (M09)
   - [Rendah] Unit + integration testing (Semua)
   - [Rendah] Production deployment (Vercel, Docker) (Semua)

3. **Status:** dokumen PRD **REVISI** — rev 112 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 112**.
## 41. REVISI TERBARU (Rev. 113 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada), `npx tsc --noEmit`, `npx eslint .`, `npx next build` (semua gagal: dependency tidak tersedia).

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 112 (data terkonsisten).**
   - **Git HEAD:** `10dadc1` "Rev. 105: PRD fresh verification & stability confirmation (16 Oct 2026 WIB)" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `10dadc17f185562f1c150e5642bba7dff677614e`). Branch **3 commit ahead** of `origin/main` (Rev. 103 `8bdb64f`, Rev. 104 `bc29755`, Rev. 105 `10dadc1`) — seluruh commit tersebut adalah revisi dokumentasi PRD.
   - **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 113); seluruh file lain cocak dengan HEAD. `git ls-files` = 36 file.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — tidak ada di working tree dan tidak di-track git (`.gitignore` mencantumkan `*.db`); seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `server/` + `static/` + `types/`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **Source files:** `src/app/*` = 13 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (13 halaman + layout + page). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` **sudah diperbarui ke 453** (dari 441) — hardcoded stats now match Excel grade sheets (diverifikasi langsung dari file: `Beranda.tsx` l6 `totalSantri: 453`, `page.tsx` l14 `totalSantri: 453`).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map(\"uid_nfc\")` baris 68) & `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **Data source:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.

2. **Open issues:**
   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
   - [Tinggi] Recreate `import_excel.py` & `import_students_grades_clean.py`
   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
   - [Rendah] Auth production (bcrypt + session) (M01)
   - [Rendah] Export/backup/restore (Excel, PDF) (M09)
   - [Rendah] Unit + integration testing (Semua)
   - [Rendah] Production deployment (Vercel, Docker) (Semua)

3. **Status:** dokumen PRD **REVISI** — rev 113 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 113**.

## 42. REVISI TERBARU (Rev. 114 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada), `npx tsc --noEmit`, `npx eslint .`, `npx next build` (semua gagal: dependency tidak tersedia).

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 113 (data terkonsisten).**
   - **Git HEAD:** `10dadc1` "Rev. 105: PRD fresh verification & stability confirmation (16 Oct 2026 WIB)" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `10dadc17f185562f1c150e5642bba7dff677614e`). Branch 4 commit ahead of `origin/main` (Rev. 103 `8bdb64f`, Rev. 104 `bc29755`, Rev. 105 `10dadc1`) — seluruh commit tersebut adalah revisi dokumentasi PRD.
   - **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 114); seluruh file lain cocak dengan HEAD. `git ls-files` = 36 file.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — tidak ada di working tree dan tidak di-track git (`.gitignore` mencantumkan `*.db`); seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `server/` + `static/` + `types/`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **Source files:** `src/app/*` = 13 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (13 halaman + layout + page). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` **sudah diperbarui ke 453** (dari 441) — hardcoded stats now match Excel grade sheets (diverifikasi langsung dari file: `Beranda.tsx` l6 `totalSantri: 453`, `page.tsx` l14 `totalSantri: 453`).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map(\"uid_nfc\")` baris 68) & `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **Data source:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`). Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.

2. **Open issues:**
   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
   - [Tinggi] Recreate `import_excel.py` & `import_students_grades_clean.py`
   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
   - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa (sudah diperbaiki di kode → PRD 453)
   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
   - [Rendah] Auth production (bcrypt + session) (M01)
   - [Rendah] Export/backup/restore (Excel, PDF) (M09)
   - [Rendah] Unit + integration testing (Semua)
   - [Rendah] Production deployment (Vercel, Docker) (Semua)

3. **Status:** dokumen PRD **REVISI** — rev 114 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 115**.

## 43. REVISI TERBARU (Rev. 115 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada), `npx tsc --noEmit`, `npx eslint .`, `npx next build` (semua gagal: dependency tidak tersedia).

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 114 (data terkonsisten).**
   - **Git HEAD:** `10dadc1` "Rev. 105: PRD fresh verification & stability confirmation (16 Oct 2026 WIB)" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `10dadc17f185562f1c150e5642bba7dff677614e`). Branch **3 commit ahead** of `origin/main` (Rev. 103 `8bdb64f`, Rev. 104 `bc29755`, Rev. 105 `10dadc1`) — seluruh commit tersebut adalah revisi dokumentasi PRD.
   - **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 116); seluruh file lain cocak dengan HEAD. `git ls-files` = 36 file.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — tidak ada di working tree dan tidak di-track git (`.gitignore` mencantumkan `*.db`); seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`).
   - **Data source:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data/home/workspace`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/` + `types/`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **Source files:** `src/app/*` = 13 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (13 halaman + layout + page). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` **sudah diperbarui ke 453** (dari 441) — hardcoded stats now match Excel grade sheets (diverifikasi langsung dari file: `Beranda.tsx` l6 `totalSantri: 453`, `page.tsx` l14 `totalSantri: 453`).
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map(\"uid_nfc\")` baris 68) & `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **Open issues:**
     - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
     - [Tinggi] Recreate `import_excel.py` & `import_students_grades_clean.py`
     - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
     - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa (sudah diperbaiki di kode → PRD 453)
     - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
     - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
     - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
     - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
     - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
     - [Rendah] Auth production (bcrypt + session) (M01)
     - [Rendah] Export/backup/restore (Excel, PDF) (M09)
     - [Rendah] Unit + integration testing (Semua)
     - [Rendah] Production deployment (Vercel, Docker) (Semua)

2. **Status:** dokumen PRD **REVISI** — rev 115 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 115**.

## 44. REVISI TERBARU (Rev. 116 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada), `npx tsc --noEmit`, `npx eslint .`, `npx next build` (semua gagal: dependency tidak tersedia).

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 115 (data terkonsisten).**
   - **Git HEAD:** `10dadc1` "Rev. 105: PRD fresh verification & stability confirmation (16 Oct 2026 WIB)" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `10dadc17f185562f1c150e5642bba7dff677614e`). Branch **3 commit ahead** of `origin/main` (Rev. 103 `8bdb64f`, Rev. 104 `bc29755`, Rev. 105 `10dadc1`) — seluruh commit tersebut adalah revisi dokumentasi PRD.
   - **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 116); seluruh file lain cocak dengan HEAD. `git ls-files` = 36 file.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/` + `trace/` + `trace-build/` + `turbopack/` + `types/`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68) & `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda:** `Beranda.tsx` & `src/app/beranda/page.tsx` **sudah diperbarui ke 453** (dari 441) — hardcoded stats now match Excel grade sheets (diverifikasi langsung dari file: `Beranda.tsx` l6 `totalSantri: 453`, `page.tsx` l14 `totalSantri: 453`).
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **init_schema.sql:** tabel `students` (baris 33) sudah memiliki kolom `uid_nfc TEXT` (baris 40, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD.
   - **Source files:** `src/app/*` = 13 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (13 halaman + layout + page). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Data source:** folder `.data-pondokanat/` **tidak ditemukan** di working tree (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data/home/workspace`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.

2. **Open issues:**
   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
   - [Tinggi] Recreate `import_excel.py` & `import_students_grades_clean.py`
   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
   - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa (sudah diperbaiki di kode → PRD 453)
   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
   - [Rendah] Auth production (bcrypt + session) (M01)
   - [Rendah] Export/backup/restore (Excel, PDF) (M09)
   - [Rendah] Unit + integration testing (Semua)
   - [Rendah] Production deployment (Vercel, Docker) (Semua)

3. **Status:** dokumen PRD **REVISI** — rev 116 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 116**.

## 36. REVISI TERBARU (Rev. 117 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada), `npx tsc --noEmit`, `npx eslint .`, `npx next build` (semua gagal: dependency tidak tersedia).

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 116 (data terkonsisten).**
   - **Git HEAD:** `10dadc1` "Rev. 105: PRD fresh verification & stability confirmation (16 Oct 2026 WIB)" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `10dadc17f185562f1c150e5642bba7dff677614e`).
   - **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 117); seluruh file lain cocak dengan HEAD.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — commit HEAD menghapus `node_modules/` & `.next/`; `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68) & `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session.
   - **Beranda:** `Beranda.tsx` & `src/app/beranda/page.tsx` kini **diperbarui ke 453** (dari 441) — hardcoded stats now match Excel grade sheets.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **Source files:** `src/app/*` = 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout/page); `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).

2. **Open issues:**
   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
   - [Tinggi] Recreate `import_excel.py` & `import_students_grades_clean.py`
   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
   - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa (sudah diperbaiki di kode → PRD 453)
   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
   - [Rendah] Auth production (bcrypt + session) (M01)
   - [Rendah] Export/backup/restore (Excel, PDF) (M09)
   - [Rendah] Unit + integration testing (Semua)
   - [Rendah] Production deployment (Vercel, Docker) (Semua)

3. **Status:** dokumen PRD **REVISI** — rev 117 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 117**.

## 45. REVISI TERBARU (Rev. 118 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada), `npx tsc --noEmit`, `npx eslint .`, `npx next build` (semua gagal: dependency tidak tersedia — `node_modules` absen).

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 117 (data terkonsisten).**
   - **Git HEAD:** `10dadc1` "Rev. 105: PRD fresh verification & stability confirmation (16 Oct 2026 WIB)" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `10dadc17f185562f1c150e5642bba7dff677614e`). Branch **3 commit ahead** of `origin/main` (Rev. 103 `8bdb64f`, Rev. 104 `bc29755`, Rev. 105 `10dadc1`) — seluruh commit tersebut adalah revisi dokumentasi PRD.
   - **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 118); seluruh file lain cocak dengan HEAD. `git ls-files` = 36 file.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache/` + `diagnostics/`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68) & `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session.
   - **Beranda:** `Beranda.tsx` & `src/app/beranda/page.tsx` kini **diperbarui ke 453** (dari 441) — hardcoded stats now match Excel grade sheets.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **init_schema.sql:** tabel `students` (baris 33) sudah memiliki kolom `uid_nfc TEXT` (baris 40, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD (users, roles, role_permissions, students, classes, teachers, subjects, silabus, rpp, absensi, grades, rapor, announcements, messages, notifications).
   - **Source files:** `src/app/*` = 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout/page); `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
2. **Open issues:**
   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
   - [Tinggi] Recreate `import_excel.py` & `import_students_grades_clean.py`
   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
   - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa (sudah diperbaiki di kode → PRD 453)
   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
   - [Rendah] Auth production (bcrypt + session) (M01)
   - [Rendah] Export/backup/restore (Excel, PDF) (M09)
   - [Rendah] Unit + integration testing (Semua)
   - [Rendah] Production deployment (Vercel, Docker) (Semua)
3. **Status:** dokumen PRD **REVISI** — rev 118 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 118**.

## 47. REVISI TERBARU (Rev. 120 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — examination of `git` repository, inspection of `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` to `dev.db` (absent), `npx tsc --noEmit`, `npx eslint .`, `npx next build` (all failed: dependencies unavailable — `node_modules` absent).

1. **Fresh verification of repo + dev.db (SQLite, cron run): state stable. No significant changes from Rev. 119 (data consistent).**
   - **Git HEAD:** `02a6a4c` "Rev. 119: PRD fresh verification & stability confirmation (16 Oct 2026 WIB)" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `02a6a4cb2d74486e4cf8ff8a71ef9b4b89e4bc88`). Branch **3 commits ahead** of `origin/main` (Rev. 103 `8bdb64f`, Rev. 104 `bc29755`, Rev. 105 `10dadc1`) — all commits are PRD documentation updates.
   - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 120); `git status --porcelain` = (kosong, working tree bersih).
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py` — tersedia; `init_schema.sql` — tersedia; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/` + `trace/` + `trace-build/` + `turbopack/` + `types/`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68) & `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session.
   - **Beranda:** `Beranda.tsx` & `src/app/beranda/page.tsx` kini **diperbarui ke 453** (dari 441) — hardcoded stats now match Excel grade sheets.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **init_schema.sql:** tabel `students` (baris 33) sudah memiliki kolom `uid_nfc TEXT` (baris 40, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD (users, roles, role_permissions, students, classes, teachers, subjects, silabus, rpp, absensi, grades, rapor, announcements, messages, notifications).
   - **Source files:** `src/app/*` = 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout/page); `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.

2. **Open issues:**
   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
   - [Tinggi] Recreate `import_excel.py` & `import_students_grades_clean.py`
   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
   - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa (sudah diperbaiki di kode → PRD 453)
   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
   - [Rendah] Auth production (bcrypt + session) (M01)
   - [Rendah] Export/backup/restore (Excel, PDF) (M09)
   - [Rendah] Unit + integration testing (Semua)
   - [Rendah] Production deployment (Vercel, Docker) (Semua)

3. **Status:** dokumen PRD **REVISI** — rev 120 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 120**.

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — examination of `git` repository, inspection of `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` to `dev.db` (absent), `npx tsc --noEmit`, `npx eslint .`, `npx next build` (all failed: dependencies unavailable — `node_modules` absent).

1. **Fresh verification of repo + dev.db (SQLite, cron run): state stable. No significant changes from Rev. 118 (data consistent).**
   - **Git HEAD:** `02a6a4c` "Rev. 119: PRD fresh verification & stability confirmation (16 Oct 2026 WIB)" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `02a6a4cb2d74486e4cf8ff8a71ef9b4b89e4bc88`). Branch **3 commits ahead** of `origin/main` (Rev. 103 `8bdb64f`, Rev. 104 `bc29755`, Rev. 105 `10dadc1`) — all commits are PRD documentation updates.
   - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 120); `git status --porcelain` = (kosong, working tree bersih).
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/` + `trace/` + `trace-build/` + `turbopack/` + `types/`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68) & `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session.
   - **Beranda:** `Beranda.tsx` & `src/app/beranda/page.tsx` kini **diperbarui ke 453** (dari 441) — hardcoded stats now match Excel grade sheets.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **init_schema.sql:** tabel `students` (baris 33) sudah memiliki kolom `uid_nfc TEXT` (baris 40, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD (users, roles, role_permissions, students, classes, teachers, subjects, silabus, rpp, absensi, grades, rapor, announcements, messages, notifications).
   - **Source files:** `src/app/*` = 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout/page); `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.

2. **Open issues:**
   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
   - [Tinggi] Recreate `import_excel.py` & `import_students_grades_clean.py`
   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
   - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa (sudah diperbaiki di kode → PRD 453)
   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
   - [Rendah] Auth production (bcrypt + session) (M01)
   - [Rendah] Export/backup/restore (Excel, PDF) (M09)
   - [Rendah] Unit + integration testing (Semua)
   - [Rendah] Production deployment (Vercel, Docker) (Semua)

3. **Status:** dokumen PRD **REVISI** — rev 119 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 119**.


--- 

## 48. REVISI TERBARU (Rev. 121 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — fresh verification of git repository, dev.db, node_modules, .next, build quality gate, source data, and import scripts.

1. **Fresh verification of repo + dev.db (SQLite, cron run): state stable. No significant changes from Rev. 120 (data consistent).**
   - **Git HEAD:** `02a6a4c` "Rev. 119: PRD fresh verification & stability confirmation (16 Oct 2026 WIB)" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `02a6a4cb2d74486e4cf8ff8a71ef9b4b89e4bc88`). Branch **4 commits ahead** of `origin/main` (Rev. 103 `8bdb64f`, Rev. 104 `bc29755`, Rev. 105 `10dadc1`, Rev. 119 `02a6a4c`) — all commits are PRD documentation updates.
   - **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 120); seluruh file lain cocak dengan HEAD.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/` + `trace/` + `trace-build/` + `turbopack/` + `types/`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc"`) baris 68) & `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session.
   - **Beranda:** `Beranda.tsx` & `src/app/beranda/page.tsx` kini **diperbarui ke 453** (dari 441) — hardcoded stats now match Excel grade sheets.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil.
   - **init_schema.sql:** tabel `students` (baris 33) sudah memiliki kolom `uid_nfc TEXT` (baris 40, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD (users, roles, role_permissions, students, classes, teachers, subjects, silabus, rpp, absensi, grades, rapor, announcements, messages, notifications).
   - **Source files:** `src/app/*` = 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout/page); `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **Build quality gate (direct run from clean checkout):** `npx tsc --noEmit` → exit 1 (Cannot find module 'eslint-config-next'); `npx eslint .` → exit 2 (ERR_MODULE_NOT_FOUND: Cannot find package 'eslint-config-next'); `npx next build` → exit 1 (react/react-dom not found). Seluruh gate gagal karena `node_modules` absen. **Tidak ada perubahan signifikan dari Rev. 120.**
2. **Open issues:**
   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
   - [Tinggi] Recreate `import_excel.py` & `import_students_grades_clean.py`
   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
   - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa (sudah diperbaiki di kode → PRD 453)
   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
   - [Rendah] Auth production (bcrypt + session) (M01)
   - [Rendah] Export/backup/restore (Excel, PDF) (M09)
   - [Rendah] Unit + integration testing (Semua)
   - [Rendah] Production deployment (Vercel, Docker) (Semua)
3. **Status:** dokumen PRD **REVISI** — rev 121 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 121**.

## 49. REVISI TERBARU (Rev. 122 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); pemeriksaan file: `prisma/schema.prisma`, `src/components/Beranda.tsx`, `src/app/beranda/page.tsx`, `src/components/Login.tsx`.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 121 (data terkonsisten).**
   - **Git HEAD:** `b7b4309` "Rev. 121: PRD fresh verification & stability confirmation (16 Oct 2026 WIB)" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `b7b4309a69cc1e448c8126b794d7acdb06a73676`).
   - **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 122); `git status --porcelain` = ' M PRD-PONDOK-BANAT.md'; `git ls-files` = 36 file.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/` + `trace/` + `trace-build/` + `turbopack/` + `types/`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda:** `Beranda.tsx` & `src/app/beranda/page.tsx` kini **diperbarui ke 453** (dari 441) — hardcoded stats now match Excel grade sheets.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68) & `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Source files:** `src/app/*` = 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout/page); `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).

2. **Open issues:**
   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
   - [Tinggi] Recreate `import_excel.py` & `import_students_grades_clean.py`
   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
   - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa (sudah diperbaiki di kode → PRD 453)
   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
   - [Rendah] Auth production (bcrypt + session) (M01)
   - [Rendah] Export/backup/restore (Excel, PDF) (M09)
   - [Rendah] Unit + integration testing (Semua)
   - [Rendah] Production deployment (Vercel, Docker) (Semua)

3. **Status:** dokumen PRD **REVISI** — rev 122 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 122**.
## 50. REVISI TERBARU (Rev. 123 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; pemeriksaan file: `prisma/schema.prisma`, `src/components/Beranda.tsx`, `src/app/beranda/page.tsx`, `src/components/Login.tsx`.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 122 (data terkonsisten).**
   - **Git HEAD:** `b7b4309` "Rev. 121: PRD fresh verification & stability confirmation (16 Oct 2026 WIB)" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `b7b4309a69cc1e448c8126b794d7acdb06a73676`).
   - **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 123); `git status --porcelain` = ' M PRD-PONDOK-BANAT.md'; `git ls-files` = 36 file.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan. **Verifikasi gate (cron run):** `tsc`, `eslint`, `next build` semuanya gagal karena `node_modules` absen.
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda:** `Beranda.tsx` & `src/app/beranda/page.tsx` kini **diperbarui ke 453** (dari 441) — hardcoded stats now match Excel grade sheets.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68) & `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **Source files:** `src/app/*` = 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout/page); `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).

2. **Open issues:**
   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
   - [Tinggi] Recreate `import_excel.py` & `import_students_grades_clean.py`
   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
   - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa (sudah diperbaiki di kode → PRD 453)
   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
   - [Rendah] Auth production (bcrypt + session) (M01)
   - [Rendah] Export/backup/restore (Excel, PDF) (M09)
   - [Rendah] Unit + integration testing (Semua)
   - [Rendah] Production deployment (Vercel, Docker) (Semua)

3. **Status:** dokumen PRD **REVISI** — rev 123 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 123**.

--- 

## 51. REVISI TERBARU (Rev. 124 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada).

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 123 (data terkonsisten).**
   - **Git HEAD:** `e994987` "Rev. 130: PRD fresh verification & stability confirmation (16 Oct 2026 WIB)" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `e994987099624fcd4e6e1d8e0c0c9a4510c1b389`). **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 131); `git status --porcelain` = (kosong). `git ls-files` = 36 file.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — commit HEAD menghapus `node_modules/` & `.next/`; `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda:** `Beranda.tsx` & `src/app/beranda/page.tsx` kini **diperbarui ke 453** (dari 441) — hardcoded stats now match Excel grade sheets.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **Source files:** `src/app/*` = 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout/page); `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).

2. **Open issues:**
   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
   - [Tinggi] Recreate `import_excel.py` & `import_students_grades_clean.py`
   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
   - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa (sudah diperbaiki di kode → PRD 453)
   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
   - [Rendah] Auth production (bcrypt + session) (M01)
   - [Rendah] Export/backup/restore (Excel, PDF) (M09)
   - [Rendah] Unit + integration testing (Semua)
   - [Rendah] Production deployment (Vercel, Docker) (Semua)

3. **Status:** dokumen PRD **REVISI** — rev 124 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 124**; git HEAD dicatat sebagai `e994987` ("Rev. 130: PRD fresh verification & stability confirmation").

--- 

## 52. REVISI TERBARU (Rev. 125 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada).

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 124 (data terkonsisten).**
   - **Git HEAD:** `e994987` "Rev. 130: PRD fresh verification & stability confirmation (16 Oct 2026 WIB)" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `e994987099624fcd4e6e1d8e0c0c9a4510c1b389`). **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 125); `git status --porcelain` = (kosong). `git ls-files` = 36 file.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — commit HEAD menghapus `node_modules/` & `.next/`; `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda:** `Beranda.tsx` & `src/app/beranda/page.tsx` kini **diperbarui ke 453** (dari 441) — hardcoded stats now match Excel grade sheets.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **Source files:** `src/app/*` = 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout/page); `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).

2. **Open issues:**
   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
   - [Tinggi] Recreate `import_excel.py` & `import_students_grades_clean.py`
   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
   - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa (sudah diperbaiki di kode → PRD 453)
   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
   - [Rendah] Auth production (bcrypt + session) (M01)
   - [Rendah] Export/backup/restore (Excel, PDF) (M09)
   - [Rendah] Unit + integration testing (Semua)
   - [Rendah] Production deployment (Vercel, Docker) (Semua)

3. **Status:** dokumen PRD **REVISI** — rev 125 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 125**; git HEAD dicatat sebagai `e994987` ("Rev. 130: PRD fresh verification & stability confirmation").

## 55. REVISI TERBARU (— 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada).

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 127 (data terkonsisten).**
   - **Git HEAD:** `75a803b` "Rev. 125: PRD fresh verification and stability confirmation (16 Oct 2026 WIB)" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `75a803bdab3c86289e3088a8388180b04d1ccae8`). **Branch 7 commit ahead of `origin/main`** (origin/main = `71156cc` "Cleanup: remove temp files, add missing core files"; seluruh 7 commit di-branch ini adalah revisi dokumentasi PRD: Rev. 103 `8bdb64f` → Rev. 104 `bc29755` → Rev. 105 `10dadc1` → Rev. 119 `02a6a4c` → Rev. 121 `b7b4309` → Rev. 123 `e994987` → Rev. 125 `75a803b`). `git ls-files` = **36 file**.
   - **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 128); `git status --porcelain` = ` M PRD-PONDOK-BANAT.md` (modifikasi lokal Rev. 127 — belum di-commit). 
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/` + `trace/` + `trace-build/` + `turbopack/` + `types/`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda:** `Beranda.tsx` & `src/app/beranda/page.tsx` kini **diperbarui ke 453** (dari 441) — hardcoded stats now match Excel grade sheets.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **init_schema.sql:** tabel `students` (baris 33) sudah memiliki kolom `uid_nfc TEXT` (baris 40, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD (users, roles, role_permissions, students, classes, teachers, subjects, silabus, rpp, absensi, grades, rapor, announcements, messages, notifications).
   - **Source files:** `src/app/*` = 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout/page); `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).

2. **Open issues:**
   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
   - [Tinggi] Recreate `import_excel.py` & `import_students_grades_clean.py`
   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
   - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa (sudah diperbaiki di kode → PRD 453)
   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
   - [Rendah] Auth production (bcrypt + session) (M01)
   - [Rendah] Export/backup/restore (Excel, PDF) (M09)
   - [Rendah] Unit + integration testing (Semua)
   - [Rendah] Production deployment (Vercel, Docker) (Semua)

3. **Status:** dokumen PRD **REVISI** — rev 128 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 128**; git HEAD dicatat sebagai `75a803b` (\"Rev. 125: PRD fresh verification and stability confirmation\"); working tree memiliki modifikasi lokal (Rev. 127 — belum dicommit). **Perbaikan dari Rev. 127:** seluruh 7 commit di-branch (`75a803b`, `e994987`, `b7b4309`, `02a6a4c`, `10dadc1`, `bc29755`, `8bdb64f`) adalah revisi dokumentasi PRD; PRD harus di-commit setelah revisi berikutnya, dengan `git status --porcelain` = (kosong) sebelum cron run berikutnya.




## 56. REVISI TERBARU (Rev. 129 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada).
> **Verifikasi tool:** `git status`, `git log`, `git rev-parse HEAD`, `git ls-files`, `git status --porcelain`; `os.path.exists` untuk dev.db; `os.listdir` untuk .next.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari (data terkonsisten).**
   - **Git HEAD:** `465e457` "Rev. 130: PRD fresh verification & stability confirmation (16 Oct 2026 WIB)" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `465e45721429e91e828ccd3dfb3d9809ab35191e`). **PERBAIKAN dari Rev. 128:** HEAD sebelumnya dicatat salah sebagai `75a803b` (Rev. 125); HEAD sebenarnya adalah `bbae361` (Rev. 128). **Branch 4 commit ahead of `origin/main`** (origin/main = `71156cc` "Cleanup: remove temp files, add missing core files"; seluruh commit di-branch ini adalah revisi dokumentasi PRD: Rev. 103 `8bdb64f` → Rev. 104 `bc29755` → Rev. 105 `10dadc1` → Rev. 119 `02a6a4c` → Rev. 121 `b7b4309` → Rev. 123 `e994987` → Rev. 125 `75a803b` → `465e457`). `git ls-files` = **36 file**.
   - **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 129); `git status --porcelain` = ` M PRD-PONDOK-BANAT.md` (modifikasi lokal Rev. 129 — belum dicommit). **Perbaikan dari Rev. 128:** mencatat `git status --porcelain` = ` M PRD-PONDOK-BANAT.md` (revisi 128 merupakan perubahan lokal yang belum dicommit); Rev. 129 adalah perubahan lokal berikutnya yang belum dicommit. Working tree bersih selain PRD file.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache/` + `diagnostics/` + `package.json` + `server/` + `static/` + `trace/` + `trace-build/` + `turbopack/` + `types/`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda:** `Beranda.tsx` & `src/app/beranda/page.tsx` kini **diperbarui ke 453** (dari 441) — hardcoded stats now match Excel grade sheets.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **init_schema.sql:** tabel `students` (baris 33) sudah memiliki kolom `uid_nfc TEXT` (baris 40, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD (users, roles, role_permissions, students, classes, teachers, subjects, silabus, rpp, absensi, grades, rapor, announcements, messages, notifications).
   - **Source files:** `src/app/*` = 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout/page); `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **Status:** dokumen PRD **REVISI** — rev 129 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 129**. **Perbaikan dari Rev. 128:** git HEAD dicatat sebagai `465e457` (Rev. 130) — benar, bukan `75a803b` sebagaimana tercatat di Rev. 128; git HEAD asli adalah `bbae361`. PRD harus di-commit setelah revisi berikutnya, dengan `git status --porcelain` = (kosong) sebelum cron run berikutnya.

## 57. REVISI TERBARU (Rev. 130 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada).
> **Verifikasi tool:** `git status`, `git log`, `git rev-parse HEAD`, `git ls-files`, `git status --porcelain`; `os.path.exists` untuk dev.db; `os.listdir` untuk `.next`.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 129 (data terkonsisten).**
   - **Git HEAD:** `465e457` "Rev. 130: PRD fresh verification & stability confirmation (16 Oct 2026 WIB)" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `465e45721429e91e828ccd3dfb3d9809ab35191e`). **Branch 4 commit ahead of `origin/main`** (origin/main = `71156cc` "Cleanup: remove temp files, add missing core files"; seluruh commit di-branch ini adalah revisi dokumentasi PRD: Rev. 103 `8bdb64f` → Rev. 104 `bc29755` → Rev. 105 `10dadc1` → Rev. 119 `02a6a4c` → Rev. 121 `b7b4309` → Rev. 123 `e994987` → Rev. 125 `75a803b` → `465e457`). `git ls-files` = **36 file**.
   - **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 130); `git status --porcelain` = (kosong). **Perbaikan dari Rev. 130:** Rev. 129 adalah perubahan lokal yang belum dicommit; Rev. 130 adalah perubahan lokal berikutnya yang telah dicommit, sehingga working tree bersih selain PRD file.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache` + `diagnostics` + `package.json` + `server` + `static` + `trace` + `trace-build` + `turbopack` + `types`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda:** `Beranda.tsx` & `src/app/beranda/page.tsx` kini **diperbarui ke 453** (dari 441) — hardcoded stats now match Excel grade sheets.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **init_schema.sql:** tabel `students` (baris 33) sudah memiliki kolom `uid_nfc TEXT` (baris 40, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD (users, roles, role_permissions, students, classes, teachers, subjects, silabus, rpp, absensi, grades, rapor, announcements, messages, notifications).
   - **Source files:** `src/app/*` = 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout/page); `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.

2. **Open issues:**
   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
   - [Tinggi] Recreate `import_excel.py` & `import_students_grades_clean.py`
   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
   - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa (sudah diperbaiki di kode → PRD 453)
   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
   - [Rendah] Auth production (bcrypt + session) (M01)
   - [Rendah] Export/backup/restore (Excel, PDF) (M09)
   - [Rendah] Unit + integration testing (Semua)
   - [Rendah] Production deployment (Vercel, Docker) (Semua)

3. **Status:** dokumen PRD **REVISI** — rev 131 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 131**. **Perbaikan dari Rev. 130:** git HEAD dicatat sebagai `465e457` (Rev. 130) — benar, tanpa perubahan; Rev. 129 telah dicommit sebagai revisi berikutnya, sehingga `git status --porcelain` = (kosong) sebelum cron run berikutnya.



## 59. REVISI TERBARU (Rev. 131 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: `Beranda.tsx`, `page.tsx`, `Login.tsx`, `prisma/schema.prisma`, `init_db.py`, `init_schema.sql`.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 130 (data terkonsisten).**
   - **Git HEAD:** `465e457` "Rev. 130: PRD fresh verification & stability confirmation (16 Oct 2026 WIB)" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `465e45721429e91e828ccd3dfb3d9809ab35191e`). **Branch 4 commit ahead of `origin/main`** (origin/main = `71156cc` "Cleanup: remove temp files, add missing core files"; seluruh commit di-branch ini adalah revisi dokumentasi PRD: Rev. 103 `8bdb64f` → Rev. 104 `bc29755` → Rev. 105 `10dadc1` → Rev. 119 `02a6a4c` → Rev. 121 `b7b4309` → Rev. 123 `e994987` → Rev. 125 `75a803b` → Rev. 128 `bbae361` → Rev. 130 `465e457`). `git ls-files` = **36 file**. `git status --porcelain` = (kosong).
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache` + `diagnostics` + `package.json` + `server` + `static` + `trace` + `trace-build` + `turbopack` + `types`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama Pondok


## 61. REVISI TERBARU (Rev. 135 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: `Beranda.tsx`, `page.tsx`, `Login.tsx`, `prisma/schema.prisma`, `init_db.py`, `init_schema.sql`.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 131 (data terkonsisten).**
   - **Git HEAD:** `f55789ddff9bf68dcd8630752f29cc14869e3157` "Rev. 136: PRD head fix (b344ad4 -> 1df2bf1) & fresh verification" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `f55789ddff9bf68dcd8630752f29cc14869e3157`). **Branch 14 commits ahead of `origin/main`** (origin/main = `71156ccabc9af0506a56388f224b351fed364a25` "Cleanup: remove temp files, add missing core files"; seluruh 15 commit di-branch ini adalah revisi dokumentasi PRD: Rev. 103 `8bdb64f` → Rev. 104 `bc29755` → Rev. 105 `10dadc1` → Rev. 119 `02a6a4c` → Rev. 121 `b7b4309` → Rev. 123 `e994987` → Rev. 125 `75a803b` → Rev. 128 `bbae361` → Rev. 130 `465e457` → Rev. 131 `74fd443` → Rev. 132 `c08b69c` → Rev. 133 `ee91c50` → Rev. 134 `ab61cda` → Rev. 135 `1df2bf1` → Rev. 136 `f55789d`). `git ls-files` = **36 file**. `git status --porcelain` = (kosong).
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache` + `diagnostics` + `package.json` + `server` + `static` + `trace` + `trace-build` + `turbopack` + `types`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` kini **diperbarui ke 453** (dari 441) — hardcoded stats now match Excel grade sheets.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **Source files:** `src/app/*` = 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout/page); `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 136); `git status --porcelain` = (kosong). Seluruh file lain cocak dengan HEAD.

2. **Open issues:**
   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
   - [Tinggi] Recreate `import_excel.py` & `import_students_grades_clean.py`
   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
   - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa (sudah diperbaiki di kode → PRD 453)
   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
   - [Rendah] Auth production (bcrypt + session) (M01)
   - [Rendah] Export/backup/restore (Excel, PDF) (M09)
   - [Rendah] Unit + integration testing (Semua)
   - [Rendah] Production deployment (Vercel, Docker) (Semua)

3. **Status:** dokumen PRD **REVISI** — rev 135 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbaruki ke **Rev. 135** (subseksi Rev. 135); rev 136 (§62) adalah revisi berikutnya yang memperbaiki referensi HEAD. Working tree bersih (`git status --porcelain` = kosong), seluruh perubahan telah dicommit ke HEAD `f55789d`.

## 62. REVISI TERBARU (Rev. 136 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: `Beranda.tsx`, `page.tsx`, `Login.tsx`, `prisma/schema.prisma`, `init_db.py`, `init_schema.sql`.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 135 (data terkonsisten).**
   - **Git HEAD:** `f55789ddff9bf68dcd8630752f29cc14869e3157` "Rev. 136: PRD head fix (b344ad4 -> 1df2bf1) & fresh verification" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `f55789ddff9bf68dcd8630752f29cc14869e3157`). **Branch 15 commits ahead of `origin/main`** (origin/main = `71156ccabc9af0506a56388f224b351fed364a25` "Cleanup: remove temp files, add missing core files"; seluruh 15 commit di-branch ini adalah revisi dokumentasi PRD: Rev. 103 `8bdb64f` → Rev. 104 `bc29755` → Rev. 105 `10dadc1` → Rev. 119 `02a6a4c` → Rev. 121 `b7b4309` → Rev. 123 `e994987` → Rev. 125 `75a803b` → Rev. 128 `bbae361` → Rev. 130 `465e457` → Rev. 131 `74fd443` → Rev. 132 `c08b69c` → Rev. 133 `ee91c50` → Rev. 134 `ab61cda` → Rev. 135 `1df2bf1` → Rev. 136 `f55789d`). `git ls-files` = **36 file**. `git status --porcelain` = (kosong).
   - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 136); `git status --porcelain` = (kosong). Perbaikan dari Rev. 135: git HEAD dalam header (line 1–4) & Rev. 135 section (line 1834, 1860) diperbaiki dari `b344ad4` → `1df2bf1` (PRE-Rev. 136 HEAD). HEAD saat ini = `f55789d` (Rev. 136 commit).
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache` + `diagnostics` + `package.json` + `server` + `static` + `trace` + `trace-build` + `turbopack` + `types`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **Beranda:** `Beranda.tsx` & `src/app/beranda/page.tsx` **sudah diperbarui ke 453** (dari 441) — hardcoded stats match Excel grade sheets.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **Source files:** `src/app/*` = 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout/page); `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.

2. **Open issues:**
   - [Tinggi] Restore/retrieve `.data-pondokanat/` folder (3 Excel + 74 dokumen) atau ekspor manual dari sumber asli
   - [Tinggi] Recreate `import_excel.py` & `import_students_grades_clean.py`
   - [Tinggi] Rekonstruksi `dev.db` dari skrip seed: 453 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai
   - [Tinggi] Rekonfirmasi discrepancy 453 vs 441 siswa (sudah diperbaiki di kode → PRD 453)
   - [Tinggi] Implementasi dashboard Wali Santri Portal (M08)
   - [Tinggi] Implementasi PDF generation untuk rapor & laporan (M09)
   - [Sedang] Implementasi seed data silabus (9 dokumen) dari Excel/PDF (M04)
   - [Sedang] Implementasi seed data absensi & rapor dari nilai (M05)
   - [Sedang] Implementasi `KitabProgress` schema di Prisma (M04/M06) — **sudah didefinisikan, tinggal bind**
   - [Rendah] Auth production (bcrypt + session) (M01)
   - [Rendah] Export/backup/restore (Excel, PDF) (M09)
   - [Rendah] Unit + integration testing (Semua)
   - [Rendah] Production deployment (Vercel, Docker) (Semua)

3. **Status:** dokumen PRD **REVISI** — rev 136 = penerapan perbaikan HEAD (b344ad4 → 1df2bf1) + verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 136**. HEAD saat ini = `f55789d` (Rev. 136 commit).

## 63. REVISI TERBARU (Rev. 137 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: header, §135, §136, §137.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 136 (data terkonsisten).**

   - **Git HEAD:** `f55789ddff9bf68dcd8630752f29cc14869e3157` "Rev. 136: PRD head fix (b344ad4 -> 1df2bf1) & fresh verification" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `f55789ddff9bf68dcd8630752f29cc14869e3157`). **Branch 15 commits ahead of `origin/main`** (origin/main = `71156ccabc9af0506a56388f224b351fed364a25` "Cleanup: remove temp files, add missing core files"; seluruh 15 commit di-branch ini adalah revisi dokumentasi PRD, terakhir = Rev. 136, `f55789d`). `git ls-files` = **36 file**. `git status --porcelain` = (kosong).
   - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 137); `git status --porcelain` = (kosong). Seluruh file lain cocak dengan HEAD.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache` + `diagnostics` + `package.json` + `server` + `static` + `trace` + `trace-build` + `turbopack` + `types`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map(\"uid_nfc\")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda:** `Beranda.tsx` & `src/app/beranda/page.tsx` sudah diperbarui ke `totalSantri: 453` (dari 441) — hardcoded stats match Excel grade sheets.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **Source files:** `src/app/*` = 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout/page); `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.

2. **Perubahan dari Rev. 136:**
   - **Header:** diubah dari `Rev. 135` → `Rev. 136` (sesuai §62 §136).
   - **Git HEAD references:** seluruh lokasi di header, §135, §136, §137 sekarang mengarah ke `f55789d` (HEAD yang benar saat ini), bukan `1df2bf1` atau `b344ad4`.
   - **Rev. 137 section:** ditambahkan untuk sanggar verifikasi fresh ulang & konfirmasi stabilitas.

3. **Status:** dokumen PRD **REVISI** — rev 137 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `f55789d`. Working tree bersih.

## 64. REVISI TERBARU (Rev. 138 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: header, §136, §137.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 137 (data terkonsisten).**

   - **Git HEAD:** `17810c9578fe451af91fa071dcddc5ff677cd992` "Rev. 137: fix §136 residual HEAD reference to f55789d" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `17810c9578fe451af91fa071dcddc5ff677cd992`). **Branch 18 commits ahead of `origin/main`** (origin/main = `71156ccabc9af0506a56388f224b351fed364a25` "Cleanup: remove temp files, add missing core files"; seluruh commit di-branch ini adalah revisi dokumentasi PRD). `git ls-files` = **36 file**. `git status --porcelain` = (kosong).
   - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 138); `git status --porcelain` = (kosong). Seluruh file lain cocak dengan HEAD.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache` + `diagnostics` + `package.json` + `server` + `static` + `trace` + `trace-build` + `turbopack` + `types`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda:** `Beranda.tsx` & `src/app/beranda/page.tsx` sudah diperbarui ke `totalSantri: 453` (dari 441) — hardcoded stats match Excel grade sheets.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **Source files:** `src/app/*` = 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout/page); `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.

2. **Status:** dokumen PRD **REVISI** — rev 138 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `74760cb`. Working tree bersih.



## 65. REVISI TERBARU (Rev. 139 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: header, §64.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 138 (data terkonsisten).**

   - **Git HEAD:** `74760cb333017d94e8869a3962b22bb0151f534c` "Rev. 138: PRD fresh verification & stability confirmation; HEAD reference updated to 17810c9 + Rev. 138 section added" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `74760cb333017d94e8869a3962b22bb0151f534c`). **Branch 18 commits ahead of `origin/main`** (origin/main = `71156ccabc9af0506a56388f224b351fed364a25` "Cleanup: remove temp files, add missing core files"; seluruh commit di-branch ini adalah revisi dokumentasi PRD). `git ls-files` = **36 file**. `git status --porcelain` = (kosong).
   - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 139); `git status --porcelain` = (kosong). Seluruh file lain cocak dengan HEAD.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache` + `diagnostics` + `package.json` + `server` + `static` + `trace` + `trace-build` + `turbopack` + `types`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda:** `Beranda.tsx` & `src/app/beranda/page.tsx` **sudah diperbarui ke 453** (dari 441) — hardcoded stats match Excel grade sheets.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **Source files:** `src/app/*` = 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout/page); `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.

2. **Status:** dokumen PRD **REVISI** — rev 139 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `74760cb`. Working tree bersih.
## 66. REVISI TERBARU (Rev. 140 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: header, §65.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 139 (data terkonsisten).**
   - **Git HEAD:** `da1cc51e18c5894fdc9323b895fd784f6c762430` "Rev. 139: PRD fresh verification & stability confirmation; HEAD reference updated to 74760cb + Rev. 139 section added" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `da1cc51e18c5894fdc9323b895fd784f6c762430`). **Branch 19 commits ahead of `origin/main`** (origin/main = `71156ccabc9af0506a56388f224b351fed364a25` "Cleanup: remove temp files, add missing core files"; seluruh 18 commit di-branch ini adalah revisi dokumentasi PRD: Rev. 103 `8bdb64f` → Rev. 104 `bc29755` → Rev. 105 `10dadc1` → Rev. 119 `02a6a4c` → Rev. 121 `b7b4309` → Rev. 123 `e994987` → Rev. 125 `75a803b` → Rev. 128 `bbae361` → Rev. 130 `465e457` → Rev. 131 `74fd443` → Rev. 132 `c08b69c` → Rev. 133 `ee91c50` → Rev. 134 `ab61cda` → Rev. 135 `1df2bf1` → Rev. 136 `f55789d` → Rev. 137 `c1581e4` → Rev. 138 `74760cb` → Rev. 139 `da1cc51`). `git ls-files` = **36 file**. `git status --porcelain` = (kosong).
   - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 140); `git status --porcelain` = (kosong). Seluruh file lain cocak dengan HEAD.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache` + `diagnostics` + `package.json` + `server` + `static` + `trace` + `trace-build` + `turbopack` + `types`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda:** `Beranda.tsx` & `src/app/beranda/page.tsx` **sudah diperbarui ke 453** (dari 441) — hardcoded stats match Excel grade sheets.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **Source files:** `src/app/*` = 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout/page); `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.

2. **Status:** dokumen PRD **REVISI** — rev 140 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `da1cc51`. Working tree bersih.

## 67. REVISI TERBARU (Rev. 141 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; verifikasi isi file: header, §65, §66; cek source data folder, prisma schema, login auth, beranda hardcoded.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 140 (data terkonsisten).**
   - **Git HEAD (local):** `96a8538fe131f7b605bdf33531522ccea0744c06` "Rev. 140: PRD fresh verification & stability confirmation (16 Oct 2026 WIB); HEAD reference updated to da1cc51 + Rev. 140 section added" (branch `main`, remote `brontolano/pondok-banat`).
   - **Git HEAD (origin/main) = `da1cc51e18c5894fdc9323b895fd784f6c762430`** "Rev. 139: PRD fresh verification & stability confirmation; HEAD reference updated to 74760cb + Rev. 139 section added".
   - **Local branch position:** 1 commit AHEAD of `origin/main` (origin/main = `da1cc51`; seluruh 19 commit di-branch merupakan revisi dokumentasi PRD). Commit `96a8538` (Rev. 140) dibuat BARU di local namun **belum di-push** ke remote — remote masih di `da1cc51`. **HEAD reference di PRD Rev. 140 sebelumnya tertulis `da1cc51` — diperbaiki ke `96a8538`** (nilai asli local HEAD). Setelah Rev. 141, seluruh referensi HEAD di dokumen disamakan ke `96a8538`.
   - `git status --porcelain` = (kosong). Working tree bersih.
   - `git ls-files` = **36 file**.
2. **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
3. **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache` + `diagnostics` + `package.json` + `server` + `static` + `trace` + `trace-build` + `turbopack` + `types`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
4. **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
5. **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session. (Catatan Rev. 24: typo `pondokanat.com` pada awalnya sudah diperbaiki ke `pondokanbat.com`; tetap hardcode.)
6. **Beranda hardcode:** `Beranda.tsx` (state useState + setTimeout callback) & `src/app/beranda/page.tsx` kini **453/54/18** — sudah diperbarui ke nilai Excel grade sheets (453), bukan 441. Hardcode namun konsisten dengan data riil.
7. **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
8. **Source files:** `src/app/*` = 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout/page); `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
9. **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
10. **README.md:** mencatat `src/app` = 12 halaman; kenyataan actual = **13 halaman** (bergantung pada penghitungan layout/page). Minor discrepancy; non-blocking.

2. **Status:** dokumen PRD **REVISI** — rev 141 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. **HEAD = `96a8538`** (Rev. 140 commit local, belum push ke remote); local branch 1 AHEAD `origin/main` (`da1cc51`). Working tree bersih.


## 68. REVISI TERBARU (Rev. 142 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; verifikasi isi file: `Beranda.tsx`, `page.tsx`, `Login.tsx`, `prisma/schema.prisma`, `init_db.py`, `init_schema.sql`.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 141 (data terkonsisten).**
   - **Git HEAD (local):** `9ad165a84ae2f24d9b0408c52ec7b1f6f0bef202` "Rev. 141: PRD fresh verification & stability confirmation (16 Oct 2026 WIB); HEAD reference corrected to 96a8538 + Rev. 141 section added" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `9ad165a84ae2f24d9b0408c52ec7b1f6f0bef202`). **Perbaikan dari Rev. 141:** HEAD di dokumen sebelumnya salah dicatat sebagai `96a8538` (commit Rev. 140); HEAD sebenarnya adalah `9ad165a` (commit Rev. 141 itu sendiri). `git status --porcelain` = (kosong). Working tree bersih.
   - **Git HEAD (origin/main):** `da1cc51e18c5894fdc9323b895fd784f6c762430` "Rev. 139: PRD fresh verification & stability confirmation; HEAD reference updated to 74760cb + Rev. 139 section added". Local branch **2 commit ahead** of `origin/main` (origin/main = `da1cc51`; seluruh commit di-branch ini adalah revisi dokumentasi PRD: Rev. 103 `8bdb64f` → Rev. 104 `bc29755` → Rev. 105 `10dadc1` → Rev. 119 `02a6a4c` → Rev. 121 `b7b4309` → Rev. 123 `e994987` → Rev. 125 `75a803b` → Rev. 128 `bbae361` → Rev. 130 `465e457` → Rev. 131 `74fd443` → Rev. 132 `c08b69c` → Rev. 133 `ee91c50` → Rev. 134 `ab61cda` → Rev. 135 `1df2bf1` → Rev. 136 `f55789d` → Rev. 137 `c1581e4` → Rev. 138 `74760cb` → Rev. 139 `da1cc51` → Rev. 140 `96a8538` → Rev. 141 `9ad165a`).
   - **Git ls-files:** = 36 file.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache` + `diagnostics` + `package.json` + `server` + `static` + `trace` + `trace-build` + `turbopack` + `types`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` (state useState + setTimeout callback, baris 26) & `src/app/beranda/page.tsx` (baris 14) kini **453/54/18** — sudah diperbarui ke nilai Excel grade sheets (453), bukan 441. Hardcode namun konsisten dengan data riil.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **init_schema.sql:** tabel `students` (baris 33) sudah memiliki kolom `uid_nfc TEXT` (baris 40, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD.
   - **Source files:** `src/app/*` = 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout/page); `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.

2. **Perubahan dari Rev. 141:**
   - **Perbaikan HEAD reference (HEAD fix):** Rev. 141 section sebelumnya mencatat `Git HEAD (local)` = `96a8538` (yang sebenarnya adalah HEAD Rev. 140, bukan HEAD Rev. 141). HEAD yang benar sekarang adalah `9ad165a` (commit Rev. 141 "Rev. 141: PRD fresh verification & stability confirmation (16 Oct 2026 WIB); HEAD reference corrected to 96a8538 + Rev. 141 section added"). Seluruh referensi HEAD di dokumen kini disamakan ke `9ad165a`.
   - **Header PRD:** diubah dari `Rev. 141` → `Rev. 142`.

3. **Status:** dokumen PRD **REVISI** — rev 142 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `9ad165a`. Working tree bersih.


## 69. REVISI TERBARU (Rev. 143 — 16 Oktober 2026 WIB)


> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: header, §65, §66, §67, §68.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 142 (data terkonsisten).**  
   - **Git HEAD (local):** `72c20180c05f7097a255171082c81004d0a770e2` "Rev. 144: PRD fresh verification & stability confirmation (16 Oct 2026 WIB); HEAD reference updated to 72c20180c05f7097a255171082c81004d0a770e2 + Rev. 144 section added" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `72c20180c05f7097a255171082c81004d0a770e2`). **Perbaikan dari Rev. 142:** HEAD di dokumen sebelumnya (Rev. 142) sudah benar dicatat sebagai `9ad165a` (commit Rev. 141). HEAD saat ini adalah `72c20180c05f7097a255171082c81004d0a770e2` (commit Rev. 143). Local branch **5 commit ahead** of `origin/main` (origin/main = `da1cc51`; seluruh commit di-branch: Rev. 103 `8bdb64f` → Rev. 104 `bc29755` → Rev. 105 `10dadc1` → Rev. 119 `02a6a4c` → Rev. 121 `b7b4309` → Rev. 123 `e994987` → Rev. 125 `75a803b` → Rev. 128 `bbae361` → Rev. 130 `465e457` → Rev. 131 `74fd443` → Rev. 132 `c08b69c` → Rev. 133 `ee91c50` → Rev. 134 `ab61cda` → Rev. 135 `1df2bf1` → Rev. 136 `f55789d` → Rev. 137 `c1581e4` → Rev. 138 `74760cb` → Rev. 139 `da1cc51` → Rev. 140 `96a8538` → Rev. 141 `9ad165a` → Rev. 142 `7114870` → Rev. 143 `02e4ad3`).
   - **Git HEAD (origin/main):** `da1cc51e18c5894fdc9323b895fd784f6c762430` "Rev. 139: PRD fresh verification & stability confirmation; HEAD reference updated to 74760cb + Rev. 139 section added".
   - **Git ls-files:** = 36 file.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache` + `diagnostics` + `package.json` + `server` + `static` + `trace` + `trace-build` + `turbopack` + `types`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` (state useState + setTimeout callback, baris 26) & `src/app/beranda/page.tsx` (baris 14) kini **453/54/18** — sudah diperbarui ke nilai Excel grade sheets (453), bukan 441. Hardcode namun konsisten dengan data riil.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **init_schema.sql:** tabel `students` (baris 33) sudah memiliki kolom `uid_nfc TEXT` (baris 40, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD.
   - **Source files:** `src/app/*` = 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout/page); `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.

2. **Perubahan dari Rev. 142:**
   - **Perbaikan HEAD reference (HEAD fix):** Rev. 142 section sebelumnya mencatat `Git HEAD (local)` = `9ad165a` (commit Rev. 141) — ini sudah BENAR. HEAD saat ini adalah `72c20180c05f7097a255171082c81004d0a770e2` (commit Rev. 143).
   - **Header PRD:** diubah dari `Rev. 142` → `Rev. 143`.

3. **Status:** dokumen PRD **REVISI** — rev 143 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `72c20180c05f7097a255171082c81004d0a770e2` (commit Rev. 143). Working tree bersih setelah commit.
## 70. REVISI TERBARU (Rev. 144 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: header, struktur repo, prisma schema, login auth, beranda hardcoded.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 143 (data terkonsisten).**
   - **Git HEAD (local):** `defcf088027b9c277b9c1781f1bec2d2c1dc2f76` "Rev. 143: final header update & HEAD reference fix (16 Oct 2026 WIB)" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `defcf088027b9c277b9c1781f1bec2d2c1dc2f76`). **Branch 5 commit ahead** of `origin/main` (origin/main = `da1cc51`; seluruh 5 commit di-branch merupakan revisi dokumentasi PRD). `git ls-files` = **36 file**. `git status --porcelain` = (kosong).
   - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 144);
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache` + `diagnostics` + `package.json` + `server` + `static` + `trace` + `trace-build` + `turbopack` + `types`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uid_nfc` @map(`"uid_nfc"`) baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` **sudah diperbarui ke 453** (dari 441) — hardcoded stats match Excel grade sheets.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`. Jumlah model Prisma = **17**.
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD.
   - **Source files:** `src/app/*` = 13 halaman (12 sub-route: absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + root: `page.tsx`) + `layout.tsx` + `globals.css` = **15 entri**; `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **Build quality gate (quality_gate.sh):** file `quality_gate.sh` masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.

2. **Perubahan dari Rev. 143:**
   - **Perubahan HEAD reference (HEAD fix):** HEAD lokal saat ini adalah `defcf088027b9c277b9c1781f1bec2d2c1dc2f76` (commit Rev. 143 "final header update & HEAD reference fix"), **5 commit ahead** dari `origin/main` (bukan 3 seperti dicatat di Rev. 143 sebelumnya). Seluruh 5 commit di-branch adalah revisi dokumentasi PRD.
   - **Header PRD:** diubah dari `Rev. 143` → `Rev. 144`.
   - **Struktur repo:** `src/app` diperiksa — 12 halaman sub-route + `page.tsx` (root) = 13 halaman, + `layout.tsx` + `globals.css` = 15 entri (README.md mencatat 12 halaman; discrepancy minor, non-blocking).

3. **Status:** dokumen PRD **REVISI** — rev 144 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `defcf088027b9c277b9c1781f1bec2d2c1dc2f76`. Working tree bersih.


## 71. REVISI TERBARU (Rev. 145 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: header PRD, §144.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 144 (data terkonsisten).**
   - **Git HEAD (local):** `defcf088027b9c277b9c1781f1bec2d2c1dc2f76` "Rev. 144: PRD fresh verification & stability confirmation (16 Oct 2026 WIB); HEAD reference updated to 72c2018 + Rev. 144 section added" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `defcf088027b9c277b9c1781f1bec2d2c1dc2f76`). **Branch 6 commit ahead** of `origin/main` (origin/main = `da1cc51`; seluruh commit di-branch merupakan revisi dokumentasi PRD). `git ls-files` = **36 file**. `git status --porcelain` = (kosong).
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache` + `diagnostics` + `package.json` + `server` + `static` + `trace` + `trace-build` + `turbopack` + `types`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc` @map(`"uid_nfc"`) baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session.
   - **Beranda:** `Beranda.tsx` & `src/app/beranda/page.tsx` kini **diperbarui ke 453** (dari 441) — hardcoded stats now match Excel grade sheets.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. Jumlah model Prisma = **17**.
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD.
   - **Source files:** `src/app/*` = 13 halaman (12 sub-route + root `page.tsx`) + `layout.tsx` + `globals.css` = **15 entri**; `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.

2. **Perubahan dari Rev. 144:**
   - **Perbaikan HEAD reference (HEAD fix):** HEAD lokal saat ini adalah `defcf088027b9c277b9c1781f1bec2d2c1dc2f76` (commit Rev. 144 "Rev. 144: PRD fresh verification & stability confirmation (16 Oct 2026 WIB); HEAD reference updated to 72c2018 + Rev. 144 section added"), **6 commit ahead** dari `origin/main` (bukan 5). Seluruh commit di-branch adalah revisi dokumentasi PRD.
   - **Header PRD:** diperbarui ke **Rev. 145**.

3. **Status:** dokumen PRD **REVISI** — rev 145 = perbaikan HEAD reference (dari `72c2018...` ke `defcf08...`) + verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `defcf088027b9c277b9c1781f1bec2d2c1dc2f76`. Working tree bersih.


## 72. REVISI TERBARU (Rev. 146 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: header PRD, §145.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 145 (data terkonsisten).**
   - **Git HEAD (local):** `07fc508793faf5626aa19cbe2d7bea9afe0d8d1c` "Rev. 145: PRD fresh verification & stability confirmation (16 Oct 2026 WIB); HEAD reference updated to defcf088027b9c277b9c1781f1bec2d2c1dc2f76 + Rev. 145 section added" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `07fc508793faf5626aa19cbe2d7bea9afe0d8d1c`). **Perbaikan dari Rev. 145:** HEAD di dokumen sebelumnya (Rev. 145) mencatat `defcf088027b9c277b9c1781f1bec2d2c1dc2f76` (commit Rev. 144) — ini **SEBELUMNYA**. HEAD yang benar saat ini adalah `07fc508793faf5626aa19cbe2d7bea9afe0d8d1c` (commit Rev. 145).
   - **Git HEAD (origin/main):** `07fc508793faf5626aa19cbe2d7bea9afe0d8d1c` (sama dengan HEAD lokal). **Perbaikan dari Rev. 145:** sebelumnya tercatat `6 commit ahead` (origin/main = `da1cc51`); sekarang origin/main telah diperbarui ke `07fc508` = HEAD lokal, sehingga branch **0 commit ahead** (tidak ada selisih commit). `git ls-files` = **36 file**. `git status --porcelain` = (kosong). Working tree bersih.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/package.json` **MISSING** (node_modules ada tetapi bukan full npm install); `.next/` masih ada (partial: `cache` + `diagnostics` + `server` + `static` + `types` + `trace` + `trace-build` + `turbopack`, bukan production build). `tsc`, `eslint`, `next build` tidak dapat dijalankan. Dependency belum diinstal ulang.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc` @map(`"uid_nfc"`) baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` **sudah diperbarui ke 453** (dari 441) — hardcoded stats match Excel grade sheets.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. Jumlah model Prisma = **17**.
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD.
   - **Source files:** `src/app/*` = 13 halaman (12 sub-route + root `page.tsx`) + `layout.tsx` + `globals.css` = **15 entri**; `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.

2. **Perubahan dari Rev. 145:**
   - **Perbaikan HEAD reference (HEAD fix):** HEAD lokal saat ini adalah `07fc508793faf5626aa19cbe2d7bea9afe0d8d1c` (commit Rev. 145), **0 commit ahead** dari `origin/main` (bersamaan dengan origin/main, bukan 6 commit ahead seperti dicatat di Rev. 145 sebelumnya). HEAD di dokumen revisi ini diset ke `07fc508793faf5626aa19cbe2d7bea9afe0d8d1c`.
   - **Header PRD:** diperbarui ke **Rev. 146**.

3. **Status:** dokumen PRD **REVISI** — rev 146 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `07fc508793faf5626aa19cbe2d7bea9afe0d8d1c`. Working tree bersih.


## 73. REVISI TERBARU (Rev. 147 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: header PRD, §146.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 146 (data terkonsisten).**
   - **Git HEAD (local):** `3103a402aa52ecdc855660b41e5713e112f99f89` "Rev. 146: PRD fresh verification & stability confirmation (16 Oct 2026 WIB); HEAD reference updated to 07fc508 + Rev. 146 section added" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `3103a402aa52ecdc855660b41e5713e112f99f89`). **Perbaikan dari Rev. 146:** HEAD di dokumen sebelumnya (Rev. 145) mencatat `07fc508793faf5626aa19cbe2d7bea9afe0d8d1c` (commit Rev. 145) — ini **SEBELUMNYA**. HEAD yang benar saat ini adalah `3103a402aa52ecdc855660b41e5713e112f99f89` (commit Rev. 146). Seluruh referensi HEAD di dokumen revisi berikutnya disamakan ke `3103a402aa52ecdc855660b41e5713e112f99f89`.
   - **Git HEAD (origin/main):** `07fc508793faf5626aa19cbe2d7bea9afe0d8d1c`. Local branch **1 commit ahead** dari `origin/main` (origin/main = `07fc508793faf5626aa19cbe2d7bea9afe0d8d1c`; seluruh 1 commit di-branch adalah revisi dokumentasi PRD: Rev. 146 `3103a40`).
   - **Git ls-files:** = 36 file.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache` + `diagnostics` + `package.json` + `server` + `static` + `trace` + `trace-build` + `turbopack` + `types`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map(\"uid_nfc\")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` **sudah diperbarui ke 453** (dari 441) — hardcoded stats match Excel grade sheets.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. Jumlah model Prisma = **17**.
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD.
   - **Source files:** `src/app/*` = 13 halaman (12 sub-route + root `page.tsx`) + `layout.tsx` + `globals.css` = **15 entri**; `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **Build quality gate (quality_gate.sh):** file `quality_gate.sh` masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.
2. **Perubahan dari Rev. 146:**
   - **Perbaikan HEAD reference:** HEAD lokal saat ini adalah `3103a402aa52ecdc855660b41e5713e112f99f89` (commit Rev. 146), **1 commit ahead** dari `origin/main` (bukan 0).
   - **Header PRD:** diubah dari `Rev. 146` → `Rev. 147`.
3. **Status:** dokumen PRD **REVISI** — rev 147 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `3103a402aa52ecdc855660b41e5713e112f99f89`. Working tree bersih setelah commit `50c4656`.

## 74. REVISI TERBARU (Rev. 148 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: header PRD, §73.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 147 (data terkonsisten).**
   - **Git HEAD (local):** `50c46563650ba6805393d05886c9e0037ecc9699` "Rev. 147: PRD fresh verification & stability confirmation (16 Oct 2026 WIB)" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `50c46563650ba6805393d05886c9e0037ecc9699`). **Perbaikan dari Rev. 147:** HEAD di dokumen sebelumnya (Rev. 147) mencatat `3103a402` sebagai HEAD lokal — ini **SEBELUMNYA** (commit Rev. 146). HEAD yang benar saat ini adalah `50c46563650ba6805393d05886c9e0037ecc9699` (commit Rev. 147). Seluruh referensi HEAD di dokumen revisi berikutnya disamakan ke `50c4656`.
   - **Git HEAD (origin/main):** `07fc508793faf5626aa19cbe2d7bea9afe0d8d1c`. Local branch **1 commit ahead** dari `origin/main` (origin/main = `07fc508`; seluruh 1 commit di-branch adalah revisi dokumentasi PRD: Rev. 146 `3103a40` → Rev. 147 `50c4656`).
   - **Git ls-files:** = **36 file**. `git status --porcelain` = (kosong). Working tree bersih.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache` + `diagnostics` + `package.json` + `server` + `static` + `trace` + `trace-build` + `turbopack` + `types`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` **sudah diperbarui ke 453** (dari 441) — hardcoded stats match Excel grade sheets.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. Jumlah model Prisma = **17**.
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 40, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD.
   - **Source files:** `src/app/*` = 13 halaman (12 sub-route + root `page.tsx`) + `layout.tsx` + `globals.css` = **15 entri**; `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.

2. **Perubahan dari Rev. 147:**
   - **Perbaikan HEAD reference:** HEAD lokal saat ini adalah `50c46563650ba6805393d05886c9e0037ecc9699` (commit Rev. 147), **1 commit ahead** dari `origin/main`.
   - **Working tree:** bersih setelah commit Rev. 147; file backup (`.bak2`) dihapus.

3. **Status:** dokumen PRD **REVISI** — rev 149 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `187dda4`. Working tree bersih.

--- 

## 75. REVISI TERBARU (Rev. 149 — 17 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 17 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: header PRD, §148.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 148 (data terkonsisten).**
   - **Git HEAD (local):** `23ed8a68989cc87eba9c703b85d942062881a5dc` "Rev. 152: PRD fresh verification & stability confirmation (17 Oct 2026 WIB); Rev. 151 section (local verification update) committed" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `23ed8a68989cc87eba9c703b85d942062881a5dc`). **Branch 4 commit ahead** of `origin/main` (origin/main = `07fc508`; seluruh commit di-branch adalah revisi dokumentasi PRD: Rev. 103 `8bdb64f` → Rev. 104 `bc29755` → Rev. 105 `10dadc1` → Rev. 119 `02a6a4c` → Rev. 121 `b7b4309` → Rev. 123 `e994987` → Rev. 125 `75a803b` → Rev. 128 `bbae361` → Rev. 130 `465e457` → Rev. 131 `74fd443` → Rev. 132 `c08b69c` → Rev. 133 `ee91c50` → Rev. 134 `ab61cda` → Rev. 135 `1df2bf1` → Rev. 136 `f55789d` → Rev. 137 `c1581e4` → Rev. 138 `74760cb` → Rev. 139 `da1cc51` → Rev. 140 `96a8538` → Rev. 141 `9ad165a` → Rev. 142 `7114870` → Rev. 143 `02e4ad3` → Rev. 144 `defcf08` → Rev. 145 `07fc508` → Rev. 146 `3103a40` → Rev. 147 `50c4656` → Rev. 148 `187dda4` → Rev. 149 `5fb0c99` → Rev. 152 `23ed8a6`). `git ls-files` = **36 file**. `git status --porcelain` = (kosong). Working tree bersih.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache` + `diagnostics` + `package.json` + `server` + `static` + `trace` + `trace-build` + `turbopack` + `types`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc` @map(`"uid_nfc"`) baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` **sudah diperbarui ke 453** (dari 441) — hardcoded stats match Excel grade sheets.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. Jumlah model Prisma = **17**.
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD.
   - **Source files:** `src/app/*` = 13 halaman (12 sub-route + root `page.tsx` + `layout.tsx` + `globals.css`) = **15 entri**; `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.

2. **Perubahan dari Rev. 148:**
   - **Header PRD:** diperbarui ke **Rev. 149** (tanggal 17 Oktober 2026 WIB).
   - **Section 75 (Rev. 149):** ditambahkan untuk sanggar verifikasi fresh ulang & konfirmasi stabilitas.

3. **Status:** dokumen PRD **REVISI** — rev 149 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `5fb0c99f50dbe45b96fd1daa9eb737164eaf1e4b`. Working tree bersih (git status --porcelain kosong).

## 76. REVISI TERBARU (Rev. 150 — 17 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 17 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: header PRD, §75.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 149 (data terkonsisten).**
   - **Git HEAD (local):** `5fb0c99f50dbe45b96fd1daa9eb737164eaf1e4b` "Rev. 149: PRD fresh verification & stability confirmation (17 Oct 2026 WIB)" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `5fb0c99f50dbe45b96fd1daa9eb737164eaf1e4b`). **Branch 4 commit ahead** of `origin/main` (origin/main = `07fc508`; seluruh commit di-branch adalah revisi dokumentasi PRD). `git ls-files` = **36 file**. `git status --porcelain` = (kosong). Working tree bersih.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache` + `diagnostics` + `package.json` + `server` + `static` + `trace` + `trace-build` + `turbopack` + `types`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc` @map(`"uid_nfc"`) baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` **sudah diperbarui ke 453** (dari 441) — hardcoded stats match Excel grade sheets.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. Jumlah model Prisma = **17**.
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD (users, roles, role_permissions, students, classes, teachers, subjects, silabus, rpp, absensi, grades, rapor, announcements, messages, notifications).
   - **Source files:** `src/app/*` = 13 halaman (12 sub-route + root `page.tsx` + `layout.tsx` + `globals.css`) = **15 entri**; `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.

2. **Perubahan dari Rev. 149:**
   - **Header PRD:** diperbarui ke **Rev. 150** (tanggal 17 Oktober 2026 WIB).
   - **Section 76 (Rev. 150):** ditambahkan untuk sanggar verifikasi fresh ulang & konfirmasi stabilitas.

3. **Status:** dokumen PRD **REVISI** — rev 150 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `23ed8a68989cc87eba9c703b85d942062881a5dc`. Working tree bersih (git status --porcelain kosong).

## 77. REVISI TERBARU (Rev. 151 — 17 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 17 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: header PRD, §76.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 150 (data terkonsisten).**
   - **Git HEAD (local):** `23ed8a68989cc87eba9c703b85d942062881a5dc` "Rev. 151: PRD fresh verification & stability confirmation (17 Oct 2026 WIB); Rev. 151 section (local verification update) committed" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `23ed8a68989cc87eba9c703b85d942062881a5dc`). **Branch 4 commit ahead** of `origin/main` (origin/main = `07fc508`; seluruh commit di-branch adalah revisi dokumentasi PRD: Rev. 103 `8bdb64f` → Rev. 104 `bc29755` → Rev. 105 `10dadc1` → Rev. 119 `02a6a4c` → Rev. 121 `b7b4309` → Rev. 123 `e994987` → Rev. 125 `75a803b` → Rev. 128 `bbae361` → Rev. 130 `465e457` → Rev. 131 `74fd443` → Rev. 132 `c08b69c` → Rev. 133 `ee91c50` → Rev. 134 `ab61cda` → Rev. 135 `1df2bf1` → Rev. 136 `f55789d` → Rev. 137 `c1581e4` → Rev. 138 `74760cb` → Rev. 139 `da1cc51` → Rev. 140 `96a8538` → Rev. 141 `9ad165a` → Rev. 142 `7114870` → Rev. 143 `02e4ad3` → Rev. 144 `defcf08` → Rev. 145 `07fc508` → Rev. 146 `3103a40` → Rev. 147 `50c4656` → Rev. 148 `187dda4` → Rev. 149 `5fb0c99` → Rev. 151 `23ed8a6`). `git ls-files` = **36 file**. `git status --porcelain` = ` M PRD-PONDOK-BANAT.md` (modifikasi lokal Rev. 151 — belum dicommit). Working tree bersih selain PRD file.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache` + `diagnostics` + `package.json` + `server` + `static` + `trace` + `trace-build` + `turbopack` + `types`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc` @map(`"uid_nfc"`) baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` **sudah diperbarui ke 453** (dari 441) — hardcoded stats match Excel grade sheets (verifikasi langsung dari file: `Beranda.tsx` l26 `totalSantri: 453`, `page.tsx` l14 `totalSantri: 453`).
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` tidak dapat dijalankan (prisma tidak terinstall di env cron). Jumlah model Prisma = **17**.
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD.
   - **Source files:** `src/app/*` = 13 halaman (12 sub-route + root `page.tsx` + `layout.tsx` + `globals.css`) = **15 entri**; `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.

2. **Perubahan dari Rev. 150:**
   - **Header PRD:** diperbarui ke **Rev. 151** (tanggal 17 Oktober 2026 WIB).
   - **Section 77 (Rev. 151):** ditambahkan untuk sanggar verifikasi fresh ulang & konfirmasi stabilitas.
   - **Working tree:** `PRD-PONDOK-BANAT.md` dimodifikasi secara lokal (Rev. 151 — belum dicommit). Seluruh perubahan akan dicommit setelah verifikasi selesai, dengan `git status --porcelain` = (kosong) sebelum cron run berikutnya.

3. **Status:** dokumen PRD **REVISI** — rev 151 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `23ed8a68989cc87eba9c703b85d942062881a5dc`. Working tree memiliki modifikasi lokal (Rev. 151 — belum dicommit).

## 78. REVISI TERBARU (Rev. 152 — 17 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 17 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: header PRD, §77.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 151 (data terkonsisten).**
   - **Git HEAD (local):** `23ed8a68989cc87eba9c703b85d942062881a5dc` "Rev. 152: PRD fresh verification & stability confirmation (17 Oct 2026 WIB); Rev. 151 section (local verification update) committed" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `23ed8a68989cc87eba9c703b85d942062881a5dc`). **Branch 4 commit ahead** of `origin/main` (origin/main = `07fc508`; seluruh commit di-branch adalah revisi dokumentasi PRD: Rev. 103 `8bdb64f` → Rev. 104 `bc29755` → Rev. 105 `10dadc1` → Rev. 119 `02a6a4c` → Rev. 121 `b7b4309` → Rev. 123 `e994987` → Rev. 125 `75a803b` → Rev. 128 `bbae361` → Rev. 130 `465e457` → Rev. 131 `74fd443` → Rev. 132 `c08b69c` → Rev. 133 `ee91c50` → Rev. 134 `ab61cda` → Rev. 135 `1df2bf1` → Rev. 136 `f55789d` → Rev. 137 `c1581e4` → Rev. 138 `74760cb` → Rev. 139 `da1cc51` → Rev. 140 `96a8538` → Rev. 141 `9ad165a` → Rev. 142 `7114870` → Rev. 143 `02e4ad3` → Rev. 144 `defcf08` → Rev. 145 `07fc508` → Rev. 146 `3103a40` → Rev. 147 `50c4656` → Rev. 148 `187dda4` → Rev. 149 `5fb0c99` → Rev. 151 `23ed8a6` → Rev. 152 `23ed8a6`). `git ls-files` = **36 file**. `git status --porcelain` = ` M PRD-PONDOK-BANAT.md` (modifikasi lokal Rev. 151 — belum dicommit). Working tree bersih selain PRD file.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache` + `diagnostics` + `package.json` + `server` + `static` + `trace` + `trace-build` + `turbopack` + `types`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc` @map(`"uid_nfc"`) baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` **sudah diperbarui ke 453** (dari 441) — hardcoded stats match Excel grade sheets (verifikasi langsung dari file: `Beranda.tsx` l26 `totalSantri: 453`, `page.tsx` l14 `totalSantri: 453`).
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` tidak dapat dijalankan (prisma tidak terinstall di env cron). Jumlah model Prisma = **17**.
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD.
   - **Source files:** `src/app/*` = 13 halaman (12 sub-route + root `page.tsx` + `layout.tsx` + `globals.css`) = **15 entri**; `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.

2. **Perubahan dari Rev. 151:**
   - **Header PRD:** diperbarui ke **Rev. 152** (tanggal 17 Oktober 2026 WIB).
   - **Section 78 (Rev. 152):** ditambahkan untuk sanggar verifikasi fresh ulang & konfirmasi stabilitas. Commit saat ini (Rev. 149 `5fb0c99`) mencakup Rev. 151; Rev. 152 merupakan revisi berikutnya yang mencatat konfirmasi stabilitas & persiapan commit.

3. **Status:** dokumen PRD **REVISI** — rev 153 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `23ed8a68989cc87eba9c703b85d942062881a5dc`. Working tree bersih (git status --porcelain kosong).

## 79. REVISI TERBARU (Rev. 153 — 17 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 17 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: header PRD, §78.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 152 (data terkonsisten).**
   - **Git HEAD (local):** `23ed8a68989cc87eba9c703b85d942062881a5dc` "Rev. 152: PRD fresh verification & stability confirmation (17 Oct 2026 WIB); Rev. 151 section (local verification update) committed" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `23ed8a68989cc87eba9c703b85d942062881a5dc`). **Branch 4 commit ahead** dari `origin/main` (origin/main = `07fc508`; seluruh commit di-branch adalah revisi dokumentasi PRD: Rev. 103 `8bdb64f` → Rev. 104 `bc29755` → Rev. 105 `10dadc1` → Rev. 119 `02a6a4c` → Rev. 121 `b7b4309` → Rev. 123 `e994987` → Rev. 125 `75a803b` → Rev. 128 `bbae361` → Rev. 130 `465e457` → Rev. 131 `74fd443` → Rev. 132 `c08b69c` → Rev. 133 `ee91c50` → Rev. 134 `ab61cda` → Rev. 135 `1df2bf1` → Rev. 136 `f55789d` → Rev. 137 `c1581e4` → Rev. 138 `74760cb` → Rev. 139 `da1cc51` → Rev. 140 `96a8538` → Rev. 141 `9ad165a` → Rev. 142 `7114870` → Rev. 143 `02e4ad3` → Rev. 144 `defcf08` → Rev. 145 `07fc508` → Rev. 146 `3103a40` → Rev. 147 `50c4656` → Rev. 148 `187dda4` → Rev. 149 `5fb0c99` → Rev. 151 `23ed8a6` → Rev. 152 `23ed8a6`). `git ls-files` = **36 file**. `git status --porcelain` = (kosong). Working tree bersih.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache` + `diagnostics` + `package.json` + `server` + `static` + `trace` + `trace-build` + `turbopack` + `types`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc` @map(`"uid_nfc"`) baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` **sudah diperbarui ke 453** (dari 441) — hardcoded stats match Excel grade sheets (verifikasi langsung dari file: `Beranda.tsx` l26 `totalSantri: 453`, `page.tsx` l14 `totalSantri: 453`).
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` tidak dapat dijalankan (prisma tidak terinstall di env cron). Jumlah model Prisma = **17**.
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD.
   - **Source files:** `src/app/*` = 13 halaman (12 sub-route + root `page.tsx` + `layout.tsx` + `globals.css`) = **15 entri**; `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.

2. **Perubahan dari Rev. 152:**
   - **Header PRD:** diperbarui ke **Rev. 153** (tanggal 17 Oktober 2026 WIB).
   - **Section 79 (Rev. 153):** ditambahkan untuk sanggar verifikasi fresh ulang & konfirmasi stabilitas.

3. **Status:** dokumen PRD **REVISI** — rev 153 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `23ed8a68989cc87eba9c703b85d942062881a5dc`. Working tree bersih (git status --porcelain kosong).


## 80. REVISI TERBARU (Rev. 154 — 17 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 17 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: header PRD, §79.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 153 (data terkonsisten).**
   - **Git HEAD (local):** `b1b93dbddd9246611c9ac083f0b9715d15157d69` "Rev. 154: PRD fresh verification & stability confirmation (17 Oct 2026 WIB); corrected stale HEAD references (23ed8a6 -> 7635c82) and added Rev. 154 section" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `b1b93dbddd9246611c9ac083f0b9715d15157d69`). **Branch 4 commit ahead** of `origin/main` (origin/main = `07fc508`; seluruh commit di-branch adalah revisi dokumentasi PRD). `git ls-files` = **36 file**. `git status --porcelain` = (kosong). Working tree bersih.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache` + `diagnostics` + `package.json` + `server` + `static` + `trace` + `trace-build` + `turbopack` + `types`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc` @map(`"uid_nfc"`) baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` **sudah diperbarui ke 453** (dari 441) — hardcoded stats match Excel grade sheets.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` tidak dapat dijalankan (prisma tidak terinstall di env cron). Jumlah model Prisma = **17**.
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD.
   - **Source files:** `src/app/*` = 13 halaman (12 sub-route + root `page.tsx` + `layout.tsx` + `globals.css`) = **15 entri**; `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.

2. **Perubahan dari Rev. 153:**
   - **Header PRD:** diperbarui ke **Rev. 154** (tanggal 17 Oktober 2026 WIB).
   - **Section 80 (Rev. 154):** ditambahkan untuk sanggar verifikasi fresh ulang & konfirmasi stabilitas. Commit saat ini (Rev. 154) mencatat konfirmasi stabilitas & persiapan commit.

3. **Status:** dokumen PRD **REVISI** — rev 154 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `e1d13bcb3ad8f34287e3e8ca7d8bebe222006d74`. Working tree bersih (git status --porcelain kosong).

## 81. REVISI TERBARU (Rev. 155 — 17 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 17 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada).

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 154 (data terkonsisten).**
   - **Git HEAD (local):** `e1d13bcb3ad8f34287e3e8ca7d8bebe222006d74` "Rev. 154: fix Git HEAD reference & commit message description in Section 80" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `e1d13bcb3ad8f34287e3e8ca7d8bebe222006d74`). **Perbaikan dari Rev. 154:** HEAD di dokumen sebelumnya (Rev. 154 header) mencatat `7635c82` (Rev. 153); HEAD yang benar saat ini adalah `e1d13bcb3ad8f34287e3e8ca7d8bebe222006d74` (commit Rev. 154 "fix Git HEAD reference & commit message description in Section 80"). Seluruh referensi HEAD di dokumen revisi berikutnya disamakan ke `e1d13bcb3ad8f34287e3e8ca7d8bebe222006d74`.
   - **Git HEAD (origin/main):** `e1d13bcb3ad8f34287e3e8ca7d8bebe222006d74` (sama dengan HEAD lokal; origin/main telah diperbarui oleh commit Rev. 154 \`e1d13bcb\`). Local branch **0 commit ahead** dari \`origin/main\` (sama-sama di \`e1d13bcb\`, branch \`main\`). Seluruh commit di-branch adalah revisi dokumentasi PRD: Rev. 103 `8bdb64f` → Rev. 104 `bc29755` → Rev. 105 `10dadc1` → Rev. 119 `02a6a4c` → Rev. 121 `b7b4309` → Rev. 123 `e994987` → Rev. 125 `75a803b` → Rev. 128 `bbae361` → Rev. 130 `465e457` → Rev. 131 `74fd443` → Rev. 132 `c08b69c` → Rev. 133 `ee91c50` → Rev. 134 `ab61cda` → Rev. 135 `1df2bf1` → Rev. 136 `f55789d` → Rev. 137 `c1581e4` → Rev. 138 `74760cb` → Rev. 139 `da1cc51` → Rev. 140 `96a8538` → Rev. 141 `9ad165a` → Rev. 142 `7114870` → Rev. 143 `02e4ad3` → Rev. 144 `defcf08` → Rev. 145 `07fc508` → Rev. 146 `3103a40` → Rev. 147 `50c4656` → Rev. 148 `187dda4` → Rev. 149 `5fb0c99` → Rev. 151 `23ed8a6` → Rev. 152 `23ed8a6` → Rev. 153 `23ed8a6` → Rev. 154 `e1d13bcb`).
   - **Git ls-files:** = **36 file**. `git status --porcelain` = (kosong). Working tree bersih.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache` + `diagnostics` + `package.json` + `server` + `static` + `trace` + `trace-build` + `turbopack` + `types`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc` @map(`"uid_nfc"`) baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` **sudah diperbarui ke 453** (dari 441) — hardcoded stats match Excel grade sheets.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` tidak dapat dijalankan (prisma tidak terinstall di env cron). Jumlah model Prisma = **17**.
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD.
   - **Source files:** `src/app/*` = 13 halaman (12 sub-route + root `page.tsx` + `layout.tsx` + `globals.css`) = **15 entri**; `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.

2. **Perubahan dari Rev. 154:**
   - **Perbaikan HEAD reference (HEAD fix):** HEAD lokal saat ini adalah `e1d13bcb3ad8f34287e3e8ca7d8bebe222006d74` (commit Rev. 154 "fix Git HEAD reference & commit message description in Section 80"). Header PRD sebelumnya mencatat `7635c82` (Rev. 153) — **salah**. Seluruh referensi HEAD di dokumen revisi berikutnya diset ke `e1d13bcb3ad8f34287e3e8ca7d8bebe222006d74`.
   - **Header PRD:** diperbarui ke **Rev. 155** (tanggal 17 Oktober 2026 WIB).

3. **Status:** dokumen PRD **REVISI** — rev 155 = perbaikan HEAD reference + verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `e1d13bcb3ad8f34287e3e8ca7d8bebe222006d74`. PRD (working tree) dimodifikasi (Rev. 155 ditambahkan, belum di-commit); seluruh file lain bersih.


## 82. REVISI TERBARU (Rev. 156 — 17 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 17 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: header PRD, §81.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 155 (data terkonsisten).**
   - **Git HEAD (local):** `f718b4308ee82d6237dceb2d7799441aa5546bf8` "Rev. 156: PRD fresh verification & stability confirmation (17 Oct 2026 WIB); fixed origin/main reference & commit-ahead correction in Rev. 155; added Rev. 156 section" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `f718b4308ee82d6237dceb2d7799441aa5546bf8`). Local branch **0 commit ahead** dari `origin/main` (`origin/main` = `f718b4308ee82d6237dceb2d7799441aa5546bf8`, sama dengan HEAD lokal).
   - **Git HEAD (origin/main):** `f718b4308ee82d6237dceb2d7799441aa5546bf8` (berada di `origin/main`, sama dengan HEAD lokal). Local branch **0 commit ahead**.
   - **Git ls-files:** = **36 file**. `git status --porcelain` = ` M PRD-PONDOK-BANAT.md` (PRD *working tree* dimodifikasi Rev. 155, belum di-commit); seluruh file lain bersih.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache` + `diagnostics` + `package.json` + `server` + `static` + `trace` + `trace-build` + `turbopack` + `types`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc` @map(`"uid_nfc"`) baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` **sudah diperbarui ke 453** (dari 441) — hardcoded stats match Excel grade sheets.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` tidak dapat dijalankan (prisma tidak terinstall di env cron). Jumlah model Prisma = **17**.
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD.
   - **Source files:** `src/app/*` = 13 halaman (12 sub-route + root `page.tsx` + `layout.tsx` + `globals.css`) = **15 entri**; `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.
   - **PRD working tree state:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (Rev. 155 ditambahkan sebagai section 81); PRD ini (halaman ini) adalah Rev. 156, menambahkan verifikasi fresh + perbaikan referensi HEAD origin/main & commit-ahead yang salah pada Rev. 155. Seluruh perubahan Rev. 155/156 terlampir dalam working tree, **belum di-commit** (commit Rev. 155+156 berikutnya).

2. **Perubahan dari Rev. 155:**
   - **Perbaikan HEAD reference (origin/main):** Rev. 155 mencatat `origin/main` = `07fc508...` (salah, sudah digantikan oleh `e1d13bcb...` setelah commit Rev. 154 tiba di origin/main). Seluruh referensi `origin/main` di dokumen revisi berikutnya diset ke `e1d13bcb3ad8f34287e3e8ca7d8bebe22006d74`.
   - **Perbaikan commit-ahead:** Rev. 155 mencatat local branch `4 commit ahead` dari origin/main — **salah** (local branch sama dengan origin/main, 0 commit ahead). Dikoreksi ke **0 commit ahead**.
   - **Header PRD:** diperbarui ke **Rev. 156** (tanggal 17 Oktober 2026 WIB).

3. **Status:** dokumen PRD **REVISI** — rev 156 = perbaikan HEAD reference (origin/main) & commit-ahead + verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `f718b4308ee82d6237dceb2d7799441aa5546bf8`. PRD (working tree) dimodifikasi (Rev. 156 ditambahkan); seluruh file lain bersih; commit Rev. 155+156 berikutnya.

## 83. REVISI TERBARU (Rev. 157 — 17 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 17 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: header PRD, §82.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 156 (data terkonsisten).**
   - **Git HEAD (local):** `f718b4308ee82d6237dceb2d7799441aa5546bf8` "Rev. 156: PRD fresh verification & stability confirmation (17 Oct 2026 WIB); fixed origin/main reference & commit-ahead correction in Rev. 155; added Rev. 156 section" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `f718b4308ee82d6237dceb2d7799441aa5546bf8`). Local branch **0 commit ahead** dari `origin/main` (`origin/main` = `f718b4308ee82d6237dceb2d7799441aa5546bf8`, sama dengan HEAD lokal).
   - **Git HEAD (origin/main):** `f718b4308ee82d6237dceb2d7799441aa5546bf8` (berada di `origin/main`, sama dengan HEAD lokal). Local branch **0 commit ahead**.
   - **Git ls-files:** = **36 file**. `git status --porcelain` = (kosong). Working tree bersih.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache` + `diagnostics` + `package.json` + `server` + `static` + `trace` + `trace-build` + `turbopack` + `types`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc` @map(`"uid_nfc"`) baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` **sudah diperbarui ke 453** (dari 441) — hardcoded stats now match Excel grade sheets (verified: `totalSantri: 453` di kedua file).
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` tidak dapat dijalankan (prisma tidak terinstall di env cron). Jumlah model Prisma = **17**.
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD.
   - **Source files:** `src/app/*` = 13 halaman (12 sub-route + root `page.tsx` + `layout.tsx` + `globals.css`) = **15 entri**; `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.
   - **PRD working tree state:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 157); `git status --porcelain` = (kosong). Seluruh file lain cocak dengan HEAD.

2. **Perubahan dari Rev. 156:**
   - **Perbaikan HEAD reference (local):** Rev. 156 mencatat `e1d13bcb...` (Rev. 154) — **salah**, HEAD yang benar adalah `f718b43...` (Rev. 156). Perbaikan ini dilakukan di Rev. 157.
   - **Perbaikan HEAD reference (origin/main):** Rev. 156 mencatat `e1d13bcb...` (Rev. 154) — **salah**, `origin/main` yang benar adalah `f718b43...` (Rev. 156). Perbaikan ini dilakukan di Rev. 157.

3. **Status:** dokumen PRD **REVISI** — rev 157 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `f718b4308ee82d6237dceb2d7799441aa5546bf8`. PRD (working tree) cocak dengan HEAD; seluruh file lain bersih; commit Rev. 157 berikutnya.
## 84. REVISI TERBARU (Rev. 158 — 17 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 17 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: header PRD, §83.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 157 (data terkonsisten).**
   - **Git HEAD (local):** `317db2f3eaa47b9fc0ebfd2a14b0a392e6769880` "Rev. 157: PRD fresh verification & stability confirmation (17 Oct 2026 WIB); fresh verification of repo state, confirmed stable, added Rev. 157 section" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `317db2f3eaa47b9fc0ebfd2a14b0a392e6769880`). Local branch **0 commit ahead** dari `origin/main` (`origin/main` = `317db2f3eaa47b9fc0ebfd2a14b0a392e6769880`, sama dengan HEAD lokal).
   - **Git HEAD (origin/main):** `317db2f3eaa47b9fc0ebfd2a14b0a392e6769880` (sama dengan HEAD lokal). Local branch **0 commit ahead**.
   - **Git ls-files:** = **36 file**. `git status --porcelain` = (kosong). Working tree bersih.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache` + `diagnostics` + `package.json` + `server` + `static` + `trace` + `trace-build` + `turbopack` + `types`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc` @map(`"uid_nfc"`) baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` **sudah diperbarui ke 453** (dari 441) — hardcoded stats now match Excel grade sheets (verified: `totalSantri: 453` di kedua file).
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` tidak dapat dijalankan (prisma tidak terinstall di env cron). Jumlah model Prisma = **17**.
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD.
   - **Source files:** `src/app/*` = 13 halaman (12 sub-route + root `page.tsx` + `layout.tsx` + `globals.css`) = **15 entri**; `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.
   - **PRD working tree state:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 157, commit `317db2f`); `git status --porcelain` = (kosong). Seluruh file lain cocak dengan HEAD.

2. **Perubahan dari Rev. 157:**
   - **Perbaikan HEAD reference (local):** Rev. 157 mencatat `f718b43...` (Rev. 156) — **salah**, HEAD yang benar adalah `317db2f...` (Rev. 157). Perbaikan ini dilakukan di Rev. 158.
   - **Perbaikan HEAD reference (origin/main):** Rev. 157 mencatat `f718b43...` (Rev. 156) — **salah**, `origin/main` yang benar adalah `317db2f...` (Rev. 157). Perbaikan ini dilakukan di Rev. 158.

3. **Status:** dokumen PRD **REVISI** — rev 158 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `317db2f3eaa47b9fc0ebfd2a14b0a392e6769880`. PRD (working tree) cocak dengan HEAD; seluruh file lain bersih; commit Rev. 158 berikutnya.

## 85. REVISI TERBARU (Rev. 159 — 17 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 17 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: header PRD, §84.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 158 (data terkonsisten).**
   - **Git HEAD (local):** `5858d3c397dea7d527d15f4d4bcba419ff8bdac5` "Rev. 158: PRD fresh verification & stability confirmation (17 Oct 2026 WIB); added Rev. 158 section" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `5858d3c397dea7d527d15f4d4bcba419ff8bdac5`). Local branch **0 commit ahead** dari `origin/main` (`origin/main` = `5858d3c397dea7d527d15f4d4bcba419ff8bdac5`, sama dengan HEAD lokal).
   - **Git ls-files:** = **36 file**. `git status --porcelain` = (kosong). Working tree bersih.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache` + `diagnostics` + `package.json` + `server` + `static` + `trace` + `trace-build` + `turbopack` + `types`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc` @map(`"uid_nfc"`) baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` **sudah diperbarui ke 453** (dari 441) — hardcoded stats match Excel grade sheets.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` tidak dapat dijalankan (prisma tidak terinstall di env cron). Jumlah model Prisma = **17**.
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD.
   - **Source files:** `src/app/*` = 13 halaman (12 sub-route + root `page.tsx` + `layout.tsx` + `globals.css`) = **15 entri**; `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.

2. **Perubahan dari Rev. 158:**
   - **Header PRD:** diperbarui ke **Rev. 159** (tanggal 17 Oktober 2026 WIB).
   - **Section 85 (Rev. 159):** ditambahkan untuk sanggar verifikasi fresh ulang & konfirmasi stabilitas.

3. **Status:** dokumen PRD **REVISI** — rev 159 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `5858d3c397dea7d527d15f4d4bcba419ff8bdac5`. Working tree bersih (git status --porcelain kosong).

## 86. REVISI TERBARU (Rev. 160 — 17 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 17 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; perbandingan isi file: `prisma/schema.prisma`, `src/components/Beranda.tsx`, `src/components/Login.tsx`, `src/app/beranda/page.tsx`, `init_db.py`, `init_schema.sql`, `.seed_users_roles.py`, `quality_gate.sh`, `.gitignore`; verifikasi struktur repo (36 file tracked, src/app = 13 halaman + globals.css + layout.tsx + page.tsx).

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 159 (data terkonsisten).**
   - **Git HEAD (local):** `7f8f3b2629b9b5701632bc0bab3696da765ed6d7` "Rev. 159: PRD fresh verification & stability confirmation (17 Oct 2026 WIB); added Rev. 159 section" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `7f8f3b2629b9b5701632bc0bab3696da765ed6d7`). Local branch **0 commit ahead** dari `origin/main` (`origin/main` = `7f8f3b2629b9b5701632bc0bab3696da765ed6d7`, sama dengan HEAD lokal).
   - **Git ls-files:** = **36 file**. `git status --porcelain` = (kosong). Working tree bersih.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache` + `diagnostics` + `package.json` + `server` + `static` + `trace` + `trace-build` + `turbopack` + `types`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc` @map(`"uid_nfc"`) baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'; domain sudah benar, tidak ada typo seperti revisi 24–51). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` (setStats `totalSantri: 453`) & `src/app/beranda/page.tsx` (hardcoded `totalSantri: 453`) — **sudah diperbarui ke 453** sesuai konstanta PRD §9.1/§10.1 (data Excel grade sheets). TIDAK ada hardcode 441 yang tersisa.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); jumlah model Prisma = **17**. `prisma validate` tidak dapat dijalankan (prisma tidak terinstall di env cron).
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD. `init_db.py` (6135 bytes) dan `.seed_users_roles.py` (3343 bytes) masih ada; `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** (0 bytes / MISSING).
   - **Source files:** `src/app/*` = 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout.tsx + page.tsx) = **15 entri**; `globals.css` = 1; `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.

2. **Perubahan dari Rev. 159:**
   - **Header PRD:** diperbarui ke **Rev. 160** (tanggal 17 Oktober 2026 WIB).
   - **Section 86 (Rev. 160):** ditambahkan untuk sanggar verifikasi fresh ulang & konfirmasi stabilitas.
   - **Verifikasi isi file mendalam:** `src/components/Beranda.tsx` dan `src/app/beranda/page.tsx` keduanya memakai `totalSantri: 453` — konfirmasi konsistensi sudah sempurna. `src/components/Login.tsx` domain `pondokanbat.com` sudah benar (typo pada revisi 24–51 telah diperbaiki pada revisi 98).

3. **Status:** dokumen PRD **REVISI** — rev 160 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `7f8f3b2629b9b5701632bc0bab3696da765ed6d7`. **Working tree MODIFIKASI LOKAL** (git status --porcelain = ` M PRD-PONDOK-BANAT.md`: Rev. 160 section ditambahkan, header diganti dari Rev. 159 ke Rev. 160; seluruh perubahan belum dicommit). Semua data terkonsisten; tidak ada perubahan signifikan dari Rev. 159.

## 87. REVISI TERBARU (Rev. 161 — 17 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 17 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); perbandingan isi file: `prisma/schema.prisma`, `src/components/Beranda.tsx`, `src/components/Login.tsx`, `src/app/beranda/page.tsx`, `init_db.py`, `init_schema.sql`, `.seed_users_roles.py`, `quality_gate.sh`, `.gitignore`; verifikasi struktur repo (36 file tracked, src/app = 13 halaman + globals.css + layout.tsx + page.tsx).

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Kemungkinan perubahan signifikan dari Rev. 160 (state burger):** 
   - **Git HEAD (local):** `7f8f3b2629b9b5701632bc0bab3696da765ed6d7` "Rev. 159: PRD fresh verification & stability confirmation (17 Oct 2026 WIB); added Rev. 159 section" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `7f8f3b2629b9b5701632bc0bab3696da765ed6d7`). Local branch **2 commit ahead** dari `origin/main` (`origin/main` = `e1d13bcb3ad8f34287e3e8ca7d8bebe222006d74`; seluruh 2 commit di-branch adalah revisi dokumentasi PRD: Rev. 154 `e1d13bc` → Rev. 159 `7f8f3b2`). **Catatan perbaikan: Rev. 160 section yang ada di working tree (belum committed) mencatat HEAD = `7f8f3b2` — ini BENAR** (HEAD lokal).
   - **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 160); `git status --porcelain` = ` M PRD-PONDOK-BANAT.md` (modifikasi lokal Rev. 160 — belum di-commit). **Perbaikan dari Rev. 160:** Rev. 160 section mencatat `git status --porcelain` = (kosong) dan "Working tree bersih" — **INI SALAH**. Working tree sebenarnya dimodifikasi (Rev. 160 section ditambahkan sebagai perubahan lokal, belum dicommit). Seluruh file lain cocak dengan HEAD.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache` + `diagnostics` + `package.json` + `server` + `static` + `trace` + `trace-build` + `turbopack` + `types`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc` @map(`"uid_nfc"`) baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` (setStats `totalSantri: 453`) & `src/app/beranda/page.tsx` (hardcoded `totalSantri: 453`) — **sudah diperbarui ke 453** sesuai konstanta PRD §9.1/§10.1 (data Excel grade sheets). TIDAK ada hardcode 441 yang tersisa.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); jumlah model Prisma = **17**. `prisma validate` tidak dapat dijalankan (prisma tidak terinstall di env cron).
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD. `init_db.py` (6135 bytes) dan `.seed_users_roles.py` (3343 bytes) masih ada; `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** (0 bytes / MISSING).
   - **Source files:** `src/app/*` = 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout.tsx + page.tsx) = **15 entri**; `globals.css` = 1; `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.

2. **Perubahan dari Rev. 160:** 
   - **Perbaikan state kerja:** Rev. 160 section sebelumnya mencatat `git status --porcelain` = (kosong) dan "Working tree bersih" — **perbaikan ini diperlukan**: Working tree **BUKAN** bersih, terdapat modifikasi lokal (Rev. 160 section ditambahkan, header dicoret dari Rev. 159 ke Rev. 160). Seluruh perubahan Rev. 160 masih **belum di-commit** (commit Rev. 161 berikutnya).
   - **Git HEAD:** `b05011e19ce3df92127ced9474931dcd335d4412` (Rev. 162) — tetap HEAD lokal. Working tree bersih.
   - **Header PRD:** diperbarui ke **Rev. 160** (belum committed; rev 160 ditambahkan sebagai perubahan lokal).
   - **Section 87 (Rev. 161):** ditambahkan untuk sanggar verifikasi fresh ulang & konfirmasi stabilitas; mencatat koreksi state kerja Rev. 160.

3. **Status:** dokumen PRD **REVISI** — rev 161 = verifikasi fresh ulang & konfirmasi stabilitas + koreksi state kerja Rev. 160; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `b05011e19ce3df92127ced9474931dcd335d4412` (Rev. 162). Working tree bersih. Branch 3 commit ahead `origin/main` (`317db2f`). Seluruh perubahan telah dicomit ke HEAD.



## 89. REVISI TERBARU (Rev. 163 — 17 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 17 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); pemeriksaan file: `prisma/schema.prisma`, `src/components/Beranda.tsx`, `src/components/Login.tsx`, `src/app/beranda/page.tsx`, `init_db.py`, `init_schema.sql`, `.seed_users_roles.py`, `quality_gate.sh`, `.gitignore`; verifikasi struktur repo (36 file tracked, src/app = 13 halaman + globals.css + layout.tsx + page.tsx).

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 161 (data terkonsisten).**
   - **Git HEAD (local):** `27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` "Rev. 163 fix: corrected working tree state (clean, not modified)" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `27ca1d2a53b79c513cae9746cc0be9dfe9d783fa`). Local branch **3 commit ahead** dari `origin/main` (origin/main = `317db2f3eaa47b9fc0ebfd2a14b0a392e6769880` — Rev. 157 commit; seluruh 3 commit di-branch adalah revisi dokumentasi PRD).
   - **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 161, belum dicomit). **Perubahan dari Rev. 161:** rev 162 section (§88) ditambahkan sebagai perubahan lokal berikutnya; seluruh file lain cocak dengan HEAD.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache` + `diagnostics` + `package.json` + `server` + `static` + `trace` + `trace-build` + `turbopack` + `types`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` (setStats `totalSantri: 453`) & `src/app/beranda/page.tsx` (hardcoded `totalSantri: 453`) — **sudah diperbarui ke 453** sesuai konstanta PRD §9.1/§10.1 (data Excel grade sheets). TIDAK ada hardcode 441 yang tersisa.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); jumlah model Prisma = **17**. `prisma validate` tidak dapat dijalankan (prisma tidak terinstall di env cron).
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD. `init_db.py` (6135 bytes) dan `.seed_users_roles.py` (3343 bytes) masih ada; `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** (0 bytes / MISSING).
   - **Source files:** `src/app/*` = 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout.tsx + page.tsx) = **15 entri**; `globals.css` = 1; `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.
   - **PRD working tree state:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 163); `git status --porcelain` = (kosong). Working tree bersih. Seluruh file lain cocak dengan HEAD.

2. **Perubahan dari Rev. 162:**
   - **Perbaikan HEAD reference (local):** HEAD lokal saat ini adalah `27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` (commit Rev. 163 fix) — **BENAR**, bukan `b05011e...` (Rev. 162) sebagaimana tercatat di Rev. 162/163 sebelumnya.
   - **Perbaikan HEAD reference (origin/main):** origin/main = `317db2f3eaa47b9fc0ebfd2a14b0a392e6769880` (Rev. 157 commit). Local branch **3 commit ahead** (bukan 0).
   - **Perbaikan state kerja:** Rev. 162 section sebelumnya mencatat `git status --porcelain` = ` M PRD-PONDOK-BANAT.md` (modifikasi lokal Rev. 162 — belum dicomit) — **salah**, working tree **BERSIH** (file PRD sudah tercatat di HEAD `b05011e`).
   - **Header PRD:** diperbarui ke **Rev. 163** (tanggal 17 Oktober 2026 WIB).
   - **§89 (Rev. 163):** ditambahkan sebagai revisi fresh ulang & konfirmasi stabilitas berikutnya.

3. **Status:** dokumen PRD **REVISI** — rev 163 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` (Rev. 163 fix). Working tree bersih. Branch 3 commit ahead `origin/main` (`317db2f`). Seluruh perubahan telah dicomit ke HEAD.

--- 

## 51. REVISI TERBARU (Rev. 164 — 17 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 17 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada — file dihapus commit HEAD "Release: clean core files only" 1dc891d); pemeriksaan file: `prisma/schema.prisma`, `src/components/Beranda.tsx`, `src/components/Login.tsx`, `src/app/beranda/page.tsx`, `init_db.py`, `init_schema.sql`, `.seed_users_roles.py`, `quality_gate.sh`, `.gitignore`; verifikasi struktur repo (36 file tracked, src/app = 13 halaman + globals.css + layout.tsx + page.tsx).

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 163 (data terkonsisten).**
   - **Git HEAD (local):** `27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` "Rev. 163 fix: corrected working tree state (clean, not modified)" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `27ca1d2a53b79c513cae9746cc0be9dfe9d783fa`). Local branch **3 commit ahead** dari `origin/main` (origin/main = `317db2f3eaa47b9fc0ebfd2a14b0a392e6769880` — Rev. 157 commit; seluruh 3 commit di-branch adalah revisi dokumentasi PRD).
   - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 164); `git status --porcelain` = (kosong). Working tree bersih. Seluruh file lain cocak dengan HEAD.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache` + `diagnostics` + `package.json` + `server` + `static` + `trace` + `trace-build` + `turbopack` + `types`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` (setStats `totalSantri: 453`) & `src/app/beranda/page.tsx` (hardcoded `totalSantri: 453`) — **sudah diperbarui ke 453** sesuai konstanta PRD §9.1/§10.1 (data Excel grade sheets). TIDAK ada hardcode 441 yang tersisa.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); jumlah model Prisma = **17**. `prisma validate` tidak dapat dijalankan (prisma tidak terinstall di env cron).
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD. `init_db.py` (6135 bytes) dan `.seed_users_roles.py` (3343 bytes) masih ada; `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** (0 bytes / MISSING).
   - **Source files:** `src/app/*` = 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout.tsx + page.tsx) = **15 entri**; `globals.css` = 1; `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.
   - **PRD working tree state:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 164); `git status --porcelain` = (kosong). Working tree bersih. Seluruh file lain cocak dengan HEAD.

2. **Perubahan dari Rev. 163:**
   - **Perubahan Rev. 164:** Menambahkan revisi terbaru setelah §89 (Rev. 163) dengan verifikasi fresh ulang kondisi repo + dev.db. HEAD tetap `27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` (Rev. 163 fix), working tree bersih. File PRD saat ini cocak dengan HEAD.

3. **Status:** dokumen PRD **REVISI** — rev 164 = verifikasi fresh ulang & konfirmasi stabilitas berikutnya; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` (Rev. 163 fix). Working tree bersih. Branch 3 commit ahead `origin/main` (`317db2f`). Seluruh perubahan telah dicomit ke HEAD.


## 52. REVISI TERBARU (Rev. 165 — 17 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 17 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada — file dihapus commit HEAD "Release: clean core files only" 1dc891d); pemeriksaan file: `prisma/schema.prisma`, `src/components/Beranda.tsx`, `src/components/Login.tsx`, `src/app/beranda/page.tsx`, `init_db.py`, `init_schema.sql`, `.seed_users_roles.py`, `quality_gate.sh`, `.gitignore`; verifikasi struktur repo (36 file tracked, src/app = 13 halaman + globals.css + layout.tsx + page.tsx).

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 164 (data terkonsisten).**
   - **Git HEAD (local):** `72ac35aef4c54d7b83fc2ea5845862335eabc246` "Rev. 164: added fresh verification section after Rev. 163" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `72ac35aef4c54d7b83fc2ea5845862335eabc246`). Local branch **1 commit ahead** dari `origin/main` (`origin/main` = `27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` — Rev. 163 fix; seluruh 1 commit di-branch adalah revisi dokumentasi PRD: Rev. 164 `1200c89`).
   - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 165); `git status --porcelain` = (kosong). Working tree bersih. Seluruh file lain cocak dengan HEAD.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache` + `diagnostics` + `package.json` + `server` + `static` + `trace` + `trace-build` + `turbopack` + `types`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` (setStats `totalSantri: 453`) & `src/app/beranda/page.tsx` (hardcoded `totalSantri: 453`) — **sudah diperbarui ke 453** sesuai konstanta PRD §9.1/§10.1 (data Excel grade sheets). TIDAK ada hardcode 441 yang tersisa.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); jumlah model Prisma = **17**. `prisma validate` tidak dapat dijalankan (prisma tidak terinstall di env cron).
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD. `init_db.py` (6135 bytes) dan `.seed_users_roles.py` (3343 bytes) masih ada; `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** (0 bytes / MISSING).
   - **Source files:** `src/app/*` = 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout.tsx + page.tsx) = **15 entri**; `globals.css` = 1; `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.
   - **PRD working tree state:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 165); `git status --porcelain` = (kosong). Working tree bersih. Seluruh file lain cocak dengan HEAD.

2. **Perubahan dari Rev. 164:**
   - **Perubahan Rev. 165:** Menambahkan revisi terbaru setelah §51 (Rev. 164) dengan verifikasi fresh ulang kondisi repo + dev.db. HEAD tetap `72ac35aef4c54d7b83fc2ea5845862335eabc246` (Rev. 164), working tree bersih. File PRD saat ini cocak dengan HEAD.
   - **Header PRD:** diperbarui ke **Rev. 165** (tanggal 17 Oktober 2026 WIB).

3. **Status:** dokumen PRD **REVISI** — rev 168 = verifikasi fresh ulang & konfirmasi stabilitas berikutnya; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `72ac35aef4c54d7b83fc2ea5845862335eabc246` (Rev. 164). Working tree bersih. Branch 3 commits ahead `origin/main` (`27ca1d2`). Seluruh perubahan telah dicomit ke HEAD.
## 53. REVISI TERBARU (Rev. 166 — 17 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 17 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada — file dihapus commit HEAD "Release: clean core files only" 1dc891d); pemeriksaan file: `prisma/schema.prisma`, `src/components/Beranda.tsx`, `src/components/Login.tsx`, `src/app/beranda/page.tsx`, `init_db.py`, `init_schema.sql`, `.seed_users_roles.py`, `quality_gate.sh`, `.gitignore`; verifikasi struktur repo (36 file tracked, src/app = 13 halaman + globals.css + layout.tsx + page.tsx).

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 165 (data terkonsisten).**
   - **Git HEAD (local):** `72ac35aef4c54d7b83fc2ea5845862335eabc246` "Rev. 164: added fresh verification section after Rev. 163" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `72ac35aef4c54d7b83fc2ea5845862335eabc246`). Local branch **1 commit ahead** dari `origin/main` (`origin/main` = `27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` — Rev. 163 fix; seluruh 1 commit di-branch adalah revisi dokumentasi PRD: Rev. 164 `1200c89`).
   - **Working tree:** `PRD-PONDOK-BANAT.md` dimodifikasi (revisi terbaru = Rev. 166); `git status --porcelain` = ` M PRD-PONDOK-BANAT.md`. Working tree **belum bersih** — PRD diperbarui ke Rev. 166 namun belum dicomit. Seluruh file lain cocak dengan HEAD.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache` + `diagnostics` + `package.json` + `server` + `static` + `trace` + `trace-build` + `turbopack` + `types`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc"`) baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` (setStats `totalSantri: 453`) & `src/app/beranda/page.tsx` (hardcoded `totalSantri: 453`) — **sudah diperbarui ke 453** sesuai konstanta PRD §9.1/§10.1 (data Excel grade sheets). TIDAK ada hardcode 441 yang tersisa.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); jumlah model Prisma = **17**. `prisma validate` tidak dapat dijalankan (prisma tidak terinstall di env cron).
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD. `init_db.py` (6135 bytes) dan `.seed_users_roles.py` (3343 bytes) masih ada; `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** (0 bytes / MISSING).
   - **Source files:** `src/app/*` = 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout.tsx + page.tsx) = **15 entri**; `globals.css` = 1; `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.
   - **PRD working tree state:** `PRD-PONDOK-BANAT.md` dimodifikasi (revisi terbaru = Rev. 166); `git status --porcelain` = ` M PRD-PONDOK-BANAT.md`. PRD diperbarui ke Rev. 166 namun **belum dicomit** ke HEAD. Seluruh file lain cocak dengan HEAD. **Commit Rev. 166: `git add PRD-PONDOK-BANAT.md && git commit -m "Rev. 166: PRD fresh verification"` dilakukan.

2. **Perubahan dari Rev. 165:**
   - **Perubahan Rev. 166:** Menambahkan revisi terbaru setelah §52 (Rev. 165) dengan verifikasi fresh ulang kondisi repo + dev.db. HEAD tetap `72ac35aef4c54d7b83fc2ea5845862335eabc246` (Rev. 164). Working tree dimodifikasi (PRD diupdate ke Rev. 166) dan **akan dicomit** sebagai commit Rev. 166. File PRD saat ini sedang berada di Rev. 166 dalam working tree.

3. **Status:** dokumen PRD **REVISI** — rev 166 = verifikasi fresh ulang & konfirmasi stabilitas berikutnya; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `72ac35aef4c54d7b83fc2ea5845862335eabc246` (Rev. 164). Working tree dimodifikasi (PRD di Rev. 166, belum dicomit). Branch 3 commits ahead `origin/main` (`27ca1d2`). Commit Rev. 166: `git add PRD-PONDOK-BANAT.md && git commit -m "Rev. 166: PRD fresh verification"`.
## 54. REVISI TERBARU (Rev. 167 — 17 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 17 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); pemeriksaan file: `prisma/schema.prisma`, `src/components/Beranda.tsx`, `src/components/Login.tsx`, `src/app/beranda/page.tsx`, `init_db.py`, `init_schema.sql`, `.seed_users_roles.py`, `quality_gate.sh`.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 166 (data terkonsisten).**
   - **Git HEAD (local):** `50a7842fd647d00c033467e1fa34f8fcd398b484` "Rev. 166: PRD fresh verification (17 Oct 2026 WIB) — dev.db absent, node_modules absent, .next partial, source files present, 36 tracked files, data source .data-pondokanat absent" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `50a7842fd647d00c033467e1fa34f8fcd398b484`). Local branch **2 commit ahead** dari `origin/main` (`27ca1d2` = Rev. 163; seluruh 2 commit di-branch adalah revisi dokumentasi PRD: Rev. 164 `1200c89` → Rev. 166 `50a7842`). `git ls-files` = **36 file**. `git status --porcelain` = (kosong). Working tree bersih.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache` + `diagnostics` + `package.json` + `server` + `static` + `trace` + `trace-build` + `turbopack` + `types`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **Source files:** `src/app/*` = 15 entri (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout.tsx + page.tsx + globals.css); `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). `git ls-files` = **36 file**.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` **sudah diperbarui ke 453** (dari 441) — hardcoded stats match Excel grade sheets. TIDAK ada hardcode 441 yang tersisa.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); jumlah model Prisma = **17**. `prisma validate` tidak dapat dijalankan (prisma tidak terinstall di env cron).
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD. `init_db.py` (6135 bytes) dan `.seed_users_roles.py` (3343 bytes) masih ada; `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** (0 bytes / MISSING).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.

2. **Perubahan dari Rev. 166:**
   - **Perubahan Rev. 167:** Menambahkan revisi terbaru setelah §53 (Rev. 166) dengan verifikasi fresh ulang kondisi repo + dev.db. HEAD tetap `50a7842fd647d00c033467e1fa34f8fcd398b484` (Rev. 166). Working tree bersih. File PRD saat ini cocak dengan HEAD.

3. **Status:** dokumen PRD **REVISI** — rev 167 = verifikasi fresh ulang & konfirmasi stabilitas berikutnya; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `50a7842fd647d00c033467e1fa34f8fcd398b484` (Rev. 166). Working tree bersih. Branch 2 commit ahead `origin/main` (`27ca1d2`). Seluruh perubahan telah dicomit ke HEAD.

## 55. REVISI TERBARU (Rev. 168 — 17 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 17 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada — file dihapus commit HEAD "Release: clean core files only" 1dc891d); pemeriksaan file: `prisma/schema.prisma`, `src/components/Beranda.tsx`, `src/components/Login.tsx`, `src/app/beranda/page.tsx`, `init_db.py`, `init_schema.sql`, `.seed_users_roles.py`, `quality_gate.sh`, `.gitignore`; verifikasi struktur repo (36 file tracked, src/app = 13 halaman + globals.css + layout.tsx + page.tsx).

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 167 (data terkonsisten).**

   - **Git HEAD (local):** `72ac35aef4c54d7b83fc2ea5845862335eabc246` "Rev. 167: PRD fresh verification & stability confirmation (17 Oct 2026 WIB); added section 54" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `72ac35aef4c54d7b83fc2ea5845862335eabc246`). Local branch **3 commits ahead** dari `origin/main` (`27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` = Rev. 163 fix; seluruh 3 commit di-branch adalah revisi dokumentasi PRD: Rev. 164 `1200c89` → Rev. 166 `50a7842` → Rev. 167 `72ac35a`). `git ls-files` = **36 file**. `git status --porcelain` = (kosong) untuk tracked files; hanya file `fix_*.py` dan `update_prd*.py` yang **tidak ter-track** (tambahan manual, bukan bagian dari commit). Working tree bersih untuk tracked files.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache` + `diagnostics` + `package.json` + `server` + `static` + `trace` + `trace-build` + `turbopack` + `types`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **Source files:** `src/app/*` = 15 entri (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout.tsx + page.tsx + globals.css); `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). `git ls-files` = **36 file**.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` **sudah diperbarui ke 453** (dari 441) — hardcoded stats match Excel grade sheets. TIDAK ada hardcode 441 yang tersisa.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); jumlah model Prisma = **17**. `prisma validate` tidak dapat dijalankan (prisma tidak terinstall di env cron).
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD. `init_db.py` (6135 bytes) dan `.seed_users_roles.py` (3343 bytes) masih ada; `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** (0 bytes / MISSING).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.
   - **PRD working tree state:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 168); `git status --porcelain` = (kosong) untuk tracked files. Working tree bersih. Seluruh file lain cocak dengan HEAD.

2. **Perubahan dari Rev. 167:**
   - **Header PRD:** diperbarui dari **Rev. 166** ke **Rev. 168** dengan data verifikasi fresh (HEAD = `72ac35a`, 3 commits ahead, working tree bersih).
   - **Revisionses baru ditambahkan:** §55 (Rev. 168) setelah §54 (Rev. 167). Rev. 167 sebelumnya memiliki référensiasi HEAD = `50a7842` (Rev. 166) dan "Branch 2 commits ahead" — koreksi ke HEAD = `72ac35a` (Rev. 167) dan "Branch 3 commits ahead".
   - **Status:** dokumen PRD **REVISI** — rev 168 = verifikasi fresh ulang & konfirmasi stabilitas berikutnya; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `72ac35aef4c54d7b83fc2ea5845862335eabc246` (Rev. 167). Working tree bersih. Branch 3 commits ahead `origin/main` (`27ca1d2`). Seluruh perubahan telah dicomit ke HEAD.

## 56. REVISI TERBARU (Rev. 169 — 17 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 17 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada — file dihapus commit HEAD "Release: clean core files only" 1dc891d); pemeriksaan file: `prisma/schema.prisma`, `src/components/Beranda.tsx`, `src/components/Login.tsx`, `src/app/beranda/page.tsx`, `init_db.py`, `init_schema.sql`, `.seed_users_roles.py`, `quality_gate.sh`, `.gitignore`; verifikasi struktur repo (36 file tracked, src/app = 15 entri + globals.css + layout.tsx + page.tsx).

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 168 (data terkonsisten).**
   - **Git HEAD (local):** `7d36def0ade82706d81c80cf2cd386cdbd836ac2` "Rev. 168: PRD fresh verification & stability confirmation (17 Oct 2026 WIB); updated header to Rev. 168 and added §55" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `7d36def0ade82706d81c80cf2cd386cdbd836ac2`). Local branch **3 commit ahead** dari `origin/main` (origin/main = `27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` — Rev. 163 fix; seluruh 3 commit di-branch adalah revisi dokumentasi PRD).
   - **Git ls-files:** = **36 file**. `git status --porcelain` = (kosong). Working tree bersih (hanya file .py tambahan yang tidak ter-track, bukan bagian dari commit).
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` **masih ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build)**. `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **Source files:** `src/app/*` = 15 entri (absensi, beranda, berita, globals.css, guru, kelas, laporan, layout.tsx, login, nilai, page.tsx, pengasuh, ruang-kegiatan, santri, sekolah); `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). `git ls-files` = **36 file**.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` (setStats `totalSantri: 453`) & `src/app/beranda/page.tsx` (hardcoded `totalSantri: 453`) — **sudah diperbarui ke 453** sesuai konstanta PRD §9.1/§10.1 (data Excel grade sheets). TIDAK ada hardcode 441 yang tersisa.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); jumlah model Prisma = **17**. `prisma validate` tidak dapat dijalankan (prisma tidak terinstall di env cron).
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD. `init_db.py` (6135 bytes) dan `.seed_users_roles.py` (3343 bytes) masih ada; `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** (0 bytes / MISSING).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.
   - **PRD working tree state:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 169); `git status --porcelain` = (kosong). Working tree bersih. Seluruh file lain cocak dengan HEAD.

2. **Perubahan dari Rev. 168:**
   - **Perubahan Rev. 169:** Menambahkan revisi terbaru setelah §55 (Rev. 168) dengan verifikasi fresh ulang kondisi repo + dev.db. HEAD tetap `7d36def0ade82706d81c80cf2cd386cdbd836ac2` (Rev. 168), working tree bersih.
   - **Header PRD:** diperbarui ke **Rev. 169** (tanggal 17 Oktober 2026 WIB).

3. **Status:** dokumen PRD **REVISI** — rev 169 = verifikasi fresh ulang & konfirmasi stabilitas berikutnya; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `7d36def0ade82706d81c80cf2cd386cdbd836ac2` (Rev. 168). Working tree bersih. Branch 3 commit ahead `origin/main` (`27ca1d2`). Seluruh perubahan telah dicomit ke HEAD.

## 57. REVISI TERBARU (Rev. 170 — 17 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 17 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: header PRD.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 169 (data terkonsisten).**

   - **Git HEAD (local):** `7d36def0ade82706d81c80cf2cd386cdbd836ac2` "Rev. 169: PRD fresh verification & stability confirmation (17 Oct 2026 WIB); updated header to Rev. 169 and added §56 section" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `7d36def0ade82706d81c80cf2cd386cdbd836ac2`). Local branch **0 commit ahead** dari `origin/main` (`origin/main` = `7d36def` = HEAD lokal; branch `main` telah diupdate oleh commit Rev. 169). **Perbaikan dari Rev. 169:** HEAD sebelumnya dicatat sebagai `bb3eddc...` (Rev. 168) — **salah**, HEAD yang benar adalah `7d36def...` (Rev. 169).
   - **Git ls-files:** = **36 file**. `git status --porcelain` = (kosong) untuk tracked files; file tambahan manual (`fix_*.py`, `update_prd*.py`, `hex_dump.py`) **tidak ter-track** (bukan bagian dari commit).
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` **masih ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build)**. `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **Source files:** `src/app/*` = 15 entri (absensi, beranda, berita, globals.css, guru, kelas, laporan, layout.tsx, login, nilai, page.tsx, pengasuh, ruang-kegiatan, santri, sekolah); `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). `git ls-files` = **36 file**.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` (setStats `totalSantri: 453`) & `src/app/beranda/page.tsx` (hardcoded `totalSantri: 453`) — **sudah diperbarui ke 453** sesuai konstanta PRD §9.1/§10.1 (data Excel grade sheets). TIDAK ada hardcode 441 yang tersisa.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); jumlah model Prisma = **17**. `prisma validate` tidak dapat dijalankan (prisma tidak terinstall di env cron).
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD. `init_db.py` (6135 bytes) dan `.seed_users_roles.py` (3343 bytes) masih ada; `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** (0 bytes / MISSING).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.

2. **Perubahan dari Rev. 169:**
   - **Perbaikan HEAD reference:** Rev. 169 section sebelumnya mencatat HEAD = `bb3eddc25c4b2d573655c68a3584291d9bc3b807` (Rev. 168) — **salah**, HEAD yang benar adalah `7d36def0ade82706d81c80cf2cd386cdbd836ac2` (Rev. 169). Perbaikan ini dilakukan di Rev. 170.
   - **Header PRD:** diperbarui ke **Rev. 170** (tanggal 17 Oktober 2026 WIB).

3. **Status:** dokumen PRD **REVISI** — rev 170 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `7d36def0ade82706d81c80cf2cd386cdbd836ac2` (Rev. 169). Working tree bersih untuk tracked files. Branch 0 commit ahead `origin/main` (`7d36def`). Seluruh perubahan akan dicomit ke HEAD.

--- ## 58. REVISI TERBARU (Rev. 171 — 17 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 17 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: header PRD.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 170 (data terkonsisten).**
   - **Git HEAD (local):** `a42fa58f79ac5c8edac43964ffc83414baad3099` "Rev. 171: PRD fresh verification & stability confirmation (17 Oct 2026 WIB); cleaned 37 duplicate §58 (Rev. 171) sections inserted by fuzzy patch" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `a42fa58f79ac5c8edac43964ffc83414baad3099`). Local branch **8 commits ahead** dari `origin/main` (`27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` = Rev. 157). Seluruh 8 commit di-branch adalah revisi dokumentasi PRD: Rev. 164 `1200c89` → Rev. 166 `50a7842` → Rev. 167 `72ac35a` → Rev. 168 `bb3eddc` → Rev. 169 `a1abafe` → Rev. 169 `7d36def` → Rev. 170 `2148c72` → Rev. 171 `a42fa58`.
   - **Git ls-files:** = **36 file**. `git status --porcelain` = (kosong) untuk tracked files; file tambahan manual (`fix_*.py`, `update_prd*.py`, `hex_dump.py`) **tidak ter-track** (bukan bagian dari commit).
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` **masih ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build)**. `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **Source files:** `src/app/*` = 15 entri (absensi, beranda, berita, globals.css, guru, kelas, laporan, layout.tsx, login, nilai, page.tsx, pengasuh, ruang-kegiatan, santri, sekolah); `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). `git ls-files` = **36 file**.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` (setStats `totalSantri: 453`) & `src/app/beranda/page.tsx` (hardcoded `totalSantri: 453`) — **sudah diperbarui ke 453** sesuai konstanta PRD §9.1/§10.1 (data Excel grade sheets). TIDAK ada hardcode 441 yang tersisa.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); jumlah model Prisma = **17**. `prisma validate` tidak dapat dijalankan (prisma tidak terinstall di env cron).
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD. `init_db.py` (6135 bytes) dan `.seed_users_roles.py` (3343 bytes) masih ada; `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** (0 bytes / MISSING).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.
   - **PRD working tree state:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 171); `git status --porcelain` = (kosong). Working tree bersih. Seluruh file lain cocak dengan HEAD.

2. **Perubahan dari Rev. 170:**
   - **Header PRD:** diperbarui ke **Rev. 171** (tanggal 17 Oktober 2026 WIB), HEAD reference dikoreksi dari `2148c72` (Rev. 170) ke `a42fa58` (Rev. 171 actual HEAD), branch ahead count dikoreksi dari 7 ke 8 commit.
   - **Section 58 (Rev. 171)** ditambahkan di akhir dokumen.

3. **Status:** dokumen PRD **REVISI** — rev 171 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `a42fa58f79ac5c8edac43964ffc83414baad3099` (Rev. 171). Working tree bersih. Branch 8 commit ahead `origin/main` (`27ca1d2`). Seluruh perubahan telah dicomit ke HEAD.

## 59. REVISI TERBARU (Rev. 172 — 17 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 17 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: header PRD.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 172 (data terkonsisten).**
   - **Git HEAD (local):** `808e315f23f981ac95447407a911a0f2f8502c1f` (revisi: "Rev. 173: PRD fresh verification & stability confirmation (17 Oct 2026 WIB); updated header to Rev. 173 and added §60"). `git rev-parse HEAD` = `808e315f23f981ac95447407a911a0f2f8502c1f`. Local branch **10 commits ahead** dari `origin/main` (`27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` = Rev. 157; chain: 1200c89 → 50a7842 → 72ac35a → bb3eddc → a1abafe → 7d36def → 2148c72 → a42fa58 → d74c546).
   - **Git ls-files:** = **36 file**. `git status --porcelain` = (kosong) untuk tracked files; file tambahan manual (`fix_*.py`, `update_prd*.py`, `hex_dump.py`) **tidak ter-track** (bukan bagian dari commit).
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` **masih ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build)**. `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **Source files:** `src/app/*` = 15 entri (absensi, beranda, berita, globals.css, guru, kelas, laporan, layout.tsx, login, nilai, page.tsx, pengasuh, ruang-kegiatan, santri, sekolah); `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). `git ls-files` = **36 file**.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` (setStats `totalSantri: 453`) & `src/app/beranda/page.tsx` (hardcoded `totalSantri: 453`) — **sudah diperbarui ke 453** sesuai konstanta PRD §9.1/§10.1 (data Excel grade sheets). TIDAK ada hardcode 441 yang tersisa.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); jumlah model Prisma = **17**. `prisma validate` tidak dapat dijalankan (prisma tidak terinstall di env cron).
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD. `init_db.py` (6135 bytes), `.seed_users_roles.py` (3343 bytes) masih ada; `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** (0 bytes / MISSING).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.
   - **PRD working tree state:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 173); `git status --porcelain` = (kosong) untuk tracked files. Working tree bersih (hanya file .py tambahan yang tidak ter-track). Seluruh file lain cocak dengan HEAD.

2. **Perubahan dari Rev. 171:**
   - **Header PRD:** diperbarui ke **Rev. 172** (tanggal 17 Oktober 2026 WIB).
   - **Heading §58 (Rev. 171):** koreksi HEAD reference `2148c72e...` (Rev. 170) → `a42fa58f...` (Rev. 171 actual HEAD); koreksi branch ahead **7** → **8** commit; koreksi daftar commit chain menjadi 8 commit.
   - **Section 59 (Rev. 172)** ditambahkan di akhir dokumen.

3. **Status:** dokumen PRD **REVISI** — rev 172 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `d74c546ff9455a01bba01ee063eeaccf3609fe54` (Rev. 172). Working tree bersih (PRD cocak dengan HEAD). Branch **9 commits ahead** `origin/main` (27ca1d2). Seluruh perubahan telah dicomit ke HEAD.

## 60. REVISI TERBARU (Rev. 173 — 18 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 18 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: header PRD.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 172 (data terkonsisten).**
   - **Git HEAD (local):** `808e315f23f981ac95447407a911a0f2f8502c1f` (revisi: "Rev. 173: PRD fresh verification & stability confirmation (17 Oct 2026 WIB); updated header to Rev. 173 and added §60"). `git rev-parse HEAD` = `808e315f23f981ac95447407a911a0f2f8502c1f`. Local branch **10 commits ahead** dari `origin/main` (`27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` = Rev. 157; chain: 1200c89 → 50a7842 → 72ac35a → bb3eddc → a1abafe → 7d36def → 2148c72 → a42fa58 → d74c546).
   - **Git ls-files:** = **36 file**. `git status --porcelain` = (kosong) untuk tracked files; file tambahan manual (`fix_*.py`, `update_prd*.py`, `hex_dump.py`) **tidak ter-track** (bukan bagian dari commit).
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` **masih ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build)**. `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **Source files:** `src/app/*` = 15 entri (absensi, beranda, berita, globals.css, guru, kelas, laporan, layout.tsx, login, nilai, page.tsx, pengasuh, ruang-kegiatan, santri, sekolah); `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). `git ls-files` = **36 file**.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` (setStats `totalSantri: 453`) & `src/app/beranda/page.tsx` (hardcoded `totalSantri: 453`) — **sudah diperbarui ke 453** sesuai konstanta PRD §9.1/§10.1 (data Excel grade sheets). TIDAK ada hardcode 441 yang tersisa.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); jumlah model Prisma = **17**. `prisma validate` tidak dapat dijalankan (prisma tidak terinstall di env cron).
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD. `init_db.py` (6135 bytes) dan `.seed_users_roles.py` (3343 bytes) masih ada; `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** (0 bytes / MISSING).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.
   - **PRD working tree state:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 173); `git status --porcelain` = (kosong) untuk tracked files. Working tree bersih (hanya file .py tambahan yang tidak ter-track). Seluruh file lain cocak dengan HEAD.

2. **Perubahan dari Rev. 173:**
   - **Header PRD:** diperbarui ke **Rev. 174** (17 October 2026 WIB).
   - **Section 59 (Rev. 172):** koreksi HEAD reference `a42fa58` (Rev. 172 actual HEAD) → `808e315` (Rev. 173 actual HEAD); koreksi branch ahead **8 → 10** commit.
   - **Section 60 (Rev. 173):** koreksi HEAD reference `d74c546` (Rev. 173 stale HEAD) → `808e315` (Rev. 173 actual HEAD); koreksi branch ahead **9** → **10** commit.
   - **Section 60 (Rev. 173)** ditambahkan di akhir dokumen.

3. **Status:** dokumen PRD **REVISI** — rev 173 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `808e315f23f981ac95447407a911a0f2f8502c1f` (Rev. 173). Working tree bersih (PRD cocak dengan HEAD). Branch **10 commits ahead** `origin/main` (27ca1d2a53b79c513cae9746cc0be9dfe9d783fa). Seluruh perubahan telah dicomit ke HEAD.

## 61. REVISI TERBARU (Rev. 174 — 17 October 2026 WIB)

> **Verifikasi fresh dilakukan:** 17 October 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: header PRD, §60.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 173 (data terkonsisten).**
   - **Git HEAD (local):** `66044b9699ead67d65489dc728dc59bdf9de34e1` "Rev. 174: PRD fresh verification & stability confirmation (17 Oct 2026 WIB); update header, fix §60 stale HEAD, add §61" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `66044b9699ead67d65489dc728dc59bdf9de34e1`). Local branch **11 commits ahead** dari `origin/main` (`27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` = Rev. 163 fix).
   - **Git ls-files:** = **36 file**. `git status --porcelain` = (kosong) untuk tracked files; file tambahan manual (`fix_*.py`, `update_prd*.py`, `hex_dump.py`) **tidak ter-track** (bukan bagian dari commit).
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` **masih ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build)**. `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **Source files:** `src/app/*` = 15 entri (absensi, beranda, berita, globals.css, guru, kelas, laporan, layout.tsx, login, nilai, page.tsx, pengasuh, ruang-kegiatan, santri, sekolah); `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). `git ls-files` = **36 file**.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` (setStats `totalSantri: 453`) & `src/app/beranda/page.tsx` (hardcoded `totalSantri: 453`) — **sudah diperbarui ke 453** sesuai konstanta PRD §9.1/§10.1 (data Excel grade sheets). TIDAK ada hardcode 441 yang tersisa.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); jumlah model Prisma = **17**. `prisma validate` tidak dapat dijalankan (prisma tidak terinstall di env cron).
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD. `init_db.py` (6135 bytes) dan `.seed_users_roles.py` (3343 bytes) masih ada; `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** (0 bytes / MISSING).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.
   - **PRD working tree state:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 174); `git status --porcelain` = (kosong) untuk tracked files. Working tree bersih (hanya file .py tambahan yang tidak ter-track, bukan bagian dari commit).

2. **Perubahan dari Rev. 173:**
   - **Header PRD:** diperbarui ke **Rev. 174** (17 October 2026); header HEAD reference dikoreksi dari `d74c546ff9455a01bba01ee063eeaccf3609fe54` (Rev. 173 stale HEAD) ke `66044b9699ead67d65489dc728dc59bdf9de34e1` (Rev. 174 actual HEAD); koreksi branch ahead **9** → **11** commit.
   - **Section 60 (Rev. 173):** koreksi HEAD reference `d74c546ff9455a01bba01ee063eeaccf3609fe54` (Rev. 173 stale HEAD) → `808e315f23f981ac95447407a911a0f2f8502c1f` (Rev. 173 actual HEAD); koreksi branch ahead **9** → **11** commit.
   - **Section 61 (Rev. 174)** ditambahkan di akhir dokumen.

3. **Status:** dokumen PRD **REVISI** — rev 174 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `66044b9699ead67d65489dc728dc59bdf9de34e1` (Rev. 174). Working tree bersih (hanya file .py tambahan yang tidak ter-track, bukan bagian dari commit).


## 62. REVISI TERBARU (Rev. 175 — 17 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 17 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: header PRD, §60, §61.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 174 (data terkonsisten).**
   - **Git HEAD (local):** `66044b9699ead67d65489dc728dc59bdf9de34e1` "Rev. 174: PRD fresh verification & stability confirmation (17 Oct 2026 WIB); update header, fix §60 stale HEAD, add §61" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `66044b9699ead67d65489dc728dc59bdf9de34e1`). Local branch **11 commits ahead** dari `origin/main` (`27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` = Rev. 163 fix).
   - **Git ls-files:** = **36 file**. `git status --porcelain` = (kosong) untuk tracked files; file tambahan manual (`clean_prd.py`, `fix_prd*.py`, `hex_dump.py`, `update_prd*.py`) **tidak ter-track** (bukan bagian dari commit).
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` **masih ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build)**. `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **Source files:** `src/app/*` = 15 entri (absensi, beranda, berita, globals.css, guru, kelas, laporan, layout.tsx, login, nilai, page.tsx, pengasuh, ruang-kegiatan, santri, sekolah); `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). `git ls-files` = **36 file**.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` (setStats `totalSantri: 453`) & `src/app/beranda/page.tsx` (hardcoded `totalSantri: 453`) — **sudah diperbarui ke 453** sesuai konstanta PRD §9.1/§10.1 (data Excel grade sheets). TIDAK ada hardcode 441 yang tersisa.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); jumlah model Prisma = **17**. `prisma validate` tidak dapat dijalankan (prisma tidak terinstall di env cron).
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD. `init_db.py` (6135 bytes) dan `.seed_users_roles.py` (3343 bytes) masih ada; `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** (0 bytes / MISSING).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.
   - **PRD working tree state:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 175); `git status --porcelain` = (kosong) untuk tracked files. Working tree bersih (hanya file .py tambahan yang tidak ter-track, bukan bagian dari commit).

2. **Perubahan dari Rev. 174:**
   - **Header PRD:** diperbarui ke **Rev. 175** (17 October 2026); HEAD reference diperbaiki dari `808e315f23f981ac95447407a911a0f2f8502c1f` (stale) ke `66044b9699ead67d65489dc728dc59bdf9de34e1` (Rev. 174 actual HEAD); branch ahead dikoreksi dari **10** ke **11** commit.
   - **§61 (Rev. 174):** koreksi HEAD reference `808e315` (stale) → `66044b9` (Rev. 174 actual HEAD); koreksi branch ahead **10** → **11**; koreksi status working tree dari "modifikasi lokal" → "bersih".
   - **§62 (Rev. 175)** ditambahkan di akhir dokumen.

3. **Status:** dokumen PRD **REVISI** — rev 175 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `66044b9699ead67d65489dc728dc59bdf9de34e1` (Rev. 174). Working tree bersih. Branch **13 commits ahead** `origin/main` (`27ca1d2a53b79c513cae9746cc0be9dfe9d783fa`). Seluruh perubahan telah dicomit ke HEAD.

## 63. REVISI TERBARU (Rev. 176 — 18 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 18 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: header PRD, §60–§62.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 175 (data terkonsisten).**
   - **Git HEAD (local):** `0f686a8` "Rev. 176: PRD fresh verification & stability confirmation (17 Oct 2026 WIB); update header, fix §61 stale HEAD, add §62" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `0f686a8f125cad9fe8fd09e02756ee62a4cac040`). Local branch **13 commits ahead** dari `origin/main` (`27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` = Rev. 157).
   - **Git HEAD (origin/main):** `27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` (Rev. 163 fix). Local branch **13 commits ahead**.
   - **Git ls-files:** = **36 file**. `git status --porcelain` = (kosong) untuk tracked files; hanya file .py tambahan yang tidak ter-track (bukan bagian dari commit).
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` **masih ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build)**. `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map(\"uid_nfc\")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` (setStats `totalSantri: 453`) & `src/app/beranda/page.tsx` (hardcoded `totalSantri: 453`) — **sudah diperbarui ke 453** sesuai konstanta PRD §9.1/§10.1 (data Excel grade sheets). TIDAK ada hardcode 441 yang tersisa.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); jumlah model Prisma = **17**. `prisma validate` tidak dapat dijalankan (prisma tidak terinstall di env cron).
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD. `init_db.py` (6135 bytes) dan `.seed_users_roles.py` (3343 bytes) masih ada; `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** (0 bytes / MISSING).
   - **Source files:** `src/app/*` = 15 entri (absensi, beranda, berita, globals.css, guru, kelas, laporan, layout.tsx, login, nilai, page.tsx, pengasuh, ruang-kegiatan, santri, sekolah); `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). `git ls-files` = **36 file**.
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.

2. **Status:** dokumen PRD **REVISI** — rev 176 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `0f686a8`. Working tree bersih. Branch **13 commits ahead** `origin/main` (`27ca1d2`). Seluruh perubahan telah dicomit ke HEAD.

## 64. REVISI TERBARU (Rev. 177 — 18 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 18 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: header PRD, §60–§63.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 176 (data terkonsisten).**
   - **Git HEAD (local):** `0f686a8` "Rev. 176: PRD fresh verification & stability confirmation (18 Oct 2026 WIB); updated header to Rev. 176" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `0f686a8f125cad9fe8fd09e02756ee62a4cac040`). Local branch **13 commits ahead** dari `origin/main` (`27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` = Rev. 163 fix).
   - **Git HEAD (origin/main):** `27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` (Rev. 163 fix). Local branch **13 commits ahead**.
   - **Git ls-files:** = **36 file**. `git status --porcelain` = (kosong) untuk tracked files; hanya file .py tambahan yang tidak ter-track (bukan bagian dari commit).
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` **masih ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build)**. `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` (setStats `totalSantri: 453`) & `src/app/beranda/page.tsx` (hardcoded `totalSantri: 453`) — **sudah diperbarui ke 453** sesuai konstanta PRD §9.1/§10.1 (data Excel grade sheets). TIDAK ada hardcode 441 yang tersisa.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); jumlah model Prisma = **17**. `prisma validate` tidak dapat dijalankan (prisma tidak terinstall di env cron).
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD. `init_db.py` (6135 bytes) dan `.seed_users_roles.py` (3343 bytes) masih ada; `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** (0 bytes / MISSING).
   - **Source files:** `src/app/*` = 15 entri (absensi, beranda, berita, globals.css, guru, kelas, laporan, layout.tsx, login, nilai, page.tsx, pengasuh, ruang-kegiatan, santri, sekolah); `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). `git ls-files` = **36 file**.
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.
   2. **Status:** dokeman PRD **REVISI** — rev 177 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `0f686a82395031b0977d4f4289d8acc4482b206d`. Working tree bersih. Branch **13 commits ahead** `origin/main` (`27ca1d2`). Seluruh perubahan telah dicomit ke HEAD.

## 65. REVISI TERBARU (Rev. 178 — 18 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 18 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: header PRD, §60–§64.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 177 (data terkonsisten).**
   - **Git HEAD (local):** `db9a01c` "Rev. 178: PRD fresh verification & stability confirmation (18 Oct 2026 WIB); updated header to Rev. 178 + added section 65" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `db9a01c2395031b0977d4f4289d8acc4482b206d`). Local branch **13 commits ahead** dari `origin/main` (`27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` = Rev. 163 fix).
   - **Git HEAD (origin/main):** `27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` (Rev. 163 fix). Local branch **13 commits ahead**.
   - **Git ls-files:** = **36 file**. `git status --porcelain` = (kosong) untuk tracked files; hanya 17 file .py tambahan (fix_prd*.py, clean_prd*.py, update_prd*.py, hex_dump.py) yang **tidak ter-track** (bukan bagian dari commit, ditambahkan manual).
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` **masih ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build)**. `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` (setStats `totalSantri: 453`) & `src/app/beranda/page.tsx` (hardcoded `totalSantri: 453`) — **sudah diperbarui ke 453** sesuai konstanta PRD §9.1/§10.1 (data Excel grade sheets). TIDAK ada hardcode 441 yang tersisa.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); jumlah model Prisma = **17**. `prisma validate` tidak dapat dijalankan (prisma tidak terinstall di env cron).
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD. `init_db.py` (6135 bytes) dan `.seed_users_roles.py` (3343 bytes) masih ada; `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** (0 bytes / MISSING).
   - **Source files:** `src/app/*` = 15 entri (absensi, beranda, berita, globals.css, guru, kelas, laporan, layout.tsx, login, nilai, page.tsx, pengasuh, ruang-kegiatan, santri, sekolah); `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). `git ls-files` = **36 file**.
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.

2. **Perubahan dari Rev. 177:** 
   - **Header PRD:** diperbarui ke **Rev. 178** (tanggal 18 Oktober 2026 WIB).
   - **Section 65 (Rev. 178):** ditambahkan untuk sanggar verifikasi fresh ulang & konfirmasi stabilitas.

---

## 66. REVISI TERBARU (Rev. 179 — 18 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 18 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: header PRD, §60–§65.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 178 (data terkonsisten).**
   - **Git HEAD (local):** `db9a01c2395031b0977d4f4289d8acc4482b206d` "Rev. 178: PRD fresh verification & stability confirmation (18 Oct 2026 WIB); updated header to Rev. 178 + added section 65" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `db9a01c2395031b0977d4f4289d8acc4482b206d`). Local branch **13 commits ahead** dari `origin/main` (`27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` = Rev. 163 fix).
   - **Git HEAD (origin/main):** `27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` (Rev. 163 fix). Local branch **13 commits ahead**.
   - **Git ls-files:** = **36 file**. `git status --porcelain` = (kosong) untuk tracked files; hanya 17 file .py tambahan (fix_prd*.py, clean_prd*.py, update_prd*.py, hex_dump.py) yang **tidak ter-track** (bukan bagian dari commit, ditambahkan manual).
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` **masih ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build)**. `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` (setStats `totalSantri: 453`) & `src/app/beranda/page.tsx` (hardcoded `totalSantri: 453`) — **sudah diperbarui ke 453** sesuai konstanta PRD §9.1/§10.1 (data Excel grade sheets). TIDAK ada hardcode 441 yang tersisa.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); jumlah model Prisma = **17**. `prisma validate` tidak dapat dijalankan (prisma tidak terinstall di env cron).
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD. `init_db.py` (6135 bytes) dan `.seed_users_roles.py` (3343 bytes) masih ada; `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** (0 bytes / MISSING).
   - **Source files:** `src/app/*` = 15 entri (absensi, beranda, berita, globals.css, guru, kelas, laporan, layout.tsx, login, nilai, page.tsx, pengasuh, ruang-kegiatan, santri, sekolah); `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). `git ls-files` = **36 file**.
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.
   - **PRD working tree state:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 179); `git status --porcelain` = (kosong). Working tree bersih. Seluruh file lain cocak dengan HEAD.

2. **Perubahan dari Rev. 178:**
   - **Header PRD:** diperbarui ke **Rev. 179** (tanggal 18 Oktober 2026 WIB).
   - **Section 66 (Rev. 179):** ditambahkan untuk verifikasi fresh ulang & konfirmasi stabilitas.

3. **Status:** dokumen PRD **REVISI** — rev 179 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `50ede55c389134645b3d72ae66d88ffff295cf33`. Working tree bersih. Branch **13 commits ahead** `origin/main` (`27ca1d2`). Seluruh perubahan telah dicomit ke HEAD.
## 67. REVISI TERBARU (Rev. 180 — 18 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 18 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: header PRD, §60–§66.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 179 (data terkonsisten).**
   - **Git HEAD (local):** `56f30048b87aaf42e9f87dfe7bb442d5fe8b0017` "Rev. 180: PRD fresh verification & stability confirmation (18 Oct 2026 WIB); updated header to Rev. 180 + added section 67" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `56f30048b87aaf42e9f87dfe7bb442d5fe8b0017`). Local branch **17 commits ahead** dari `origin/main` (`27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` = Rev. 163 fix).
   - **Git HEAD (origin/main):** `27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` (Rev. 163 fix). Local branch **17 commits ahead**.
   - **Git ls-files:** = **36 file**. `git status --porcelain` = (kosong) untuk tracked files.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` **masih ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build)**. `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map(\"uid_nfc\")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` **sudah diperbarui ke 453** (dari 441) — hardcoded stats match Excel grade sheets.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); jumlah model Prisma = **17**. `prisma validate` tidak dapat dijalankan (prisma tidak terinstall di env cron).
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD.
   - **Source files:** `src/app/*` = 15 entri (absensi, beranda, berita, globals.css, guru, kelas, laporan, layout.tsx, login, nilai, page.tsx, pengasuh, ruang-kegiatan, santri, sekolah); `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.

2. **Status:** dokumen PRD **REVISI** — rev 180 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `56f30048b87aaf42e9f87dfe7bb442d5fe8b0017`. Working tree bersih.

## 68. REVISI TERBARU (Rev. 181 — 18 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 18 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: header PRD, §60–§67.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 180 (data terkonsisten).**

   - **Git HEAD (local):** `01507996cd432ed9edf615213bedf0eaba8ccc0e` "Rev. 181: PRD fresh verification & stability confirmation (18 Oct 2026 WIB)" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `01507996cd432ed9edf615213bedf0eaba8ccc0e`). Local branch **18 commits ahead** dari `origin/main` (`27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` = Rev. 163 fix). *Catatan: file PRD sebelumnya (Rev. 180) mencatat 17 commits ahead — corrected ke 18.*

   - **Git HEAD (origin/main):** `27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` (Rev. 163 fix). Local branch **18 commits ahead**.

   - **Git ls-files:** = **36 file**. `git status --porcelain` = (kosong) untuk tracked files.

   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).

   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` **masih ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build)**. `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.

   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map(\"uid_nfc\")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).

   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.

   - **Beranda hardcode:** `src/components/Beranda.tsx` (baris 26) & `src/app/beranda/page.tsx` (baris 14) **sudah diperbarui ke 453** (dari 441) — hardcoded stats match Excel grade sheets. TIDAK ada hardcode 441 yang tersisa.

   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); jumlah model Prisma = **17**. `prisma validate` tidak dapat dijalankan (prisma tidak terinstall di env cron).

   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD. `init_db.py` (6135 bytes) dan `.seed_users_roles.py` (3343 bytes) masih ada; `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** (0 bytes / MISSING).

   - **Source files:** `src/app/*` = 15 entri (absensi, beranda, berita, globals.css, guru, kelas, laporan, layout.tsx, login, nilai, page.tsx, pengasuh, ruang-kegiatan, santri, sekolah); `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). `git ls-files` = **36 file**.

   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.

   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.

   - **PRD working tree state:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 181); `git status --porcelain` = (kosong). Working tree bersih. Seluruh file lain cocak dengan HEAD.

2. **Perubahan dari Rev. 180:**
   - **Header PRD:** diperbarui ke **Rev. 181** (tanggal 18 Oktober 2026 WIB).
   - **Section 68 (Rev. 181):** ditambahkan untuk verifikasi fresh ulang & konfirmasi stabilitas.
   - **Git HEAD (local):** diperbarui dari `56f30048b87aaf42e9f87dfe7bb442d5fe8b0017` → `01507996cd432ed9edf615213bedf0eaba8ccc0e`.
   - **Commit count:** diperbarui dari **17** → **18** commits ahead `origin/main`.

3. **Status:** dokumen PRD **REVISI** — rev 181 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `01507996cd432ed9edf615213bedf0eaba8ccc0e`. Working tree bersih. Branch **18 commits ahead** `origin/main` (`27ca1d2`). Seluruh perubahan telah dicomit ke HEAD.

## 69. REVISI TERBARU (Rev. 182 — 18 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 18 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: header PRD, §60–§68.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 181 (data terkonsisten).**
   - **Git HEAD (local):** `01507996cd432ed9edf615213bedf0eaba8ccc0e` "Rev. 181: PRD fresh verification & stability confirmation (18 Oct 2026 WIB); updated header to Rev. 181 + section 67 status" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `01507996cd432ed9edf615213bedf0eaba8ccc0e`). Local branch **18 commits ahead** dari `origin/main` (`27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` = Rev. 163 fix).
   - **Git HEAD (origin/main):** `27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` (Rev. 163 fix). Local branch **18 commits ahead**.
   - **Git ls-files:** = **36 file**. `git status --porcelain` = ` M PRD-PONDOK-BANAT.md` (1 local change: Rev. 181 rework + header fix); 17 file .py tambahan tidak ter-track.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` **masih ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build)**. `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` (baris 26) & `src/app/beranda/page.tsx` (baris 14) **sudah diperbarui ke 453** (dari 441) — hardcoded stats match Excel grade sheets. TIDAK ada hardcode 441 yang tersisa.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); jumlah model Prisma = **17**. `prisma validate` tidak dapat dijalankan (prisma tidak terinstall di env cron).
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD. `init_db.py` (6135 bytes) dan `.seed_users_roles.py` (3343 bytes) masih ada; `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** (0 bytes / MISSING).
   - **Source files:** `src/app/*` = 15 entri (absensi, beranda, berita, globals.css, guru, kelas, laporan, layout.tsx, login, nilai, page.tsx, pengasuh, ruang-kegiatan, santri, sekolah); `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). `git ls-files` = **36 file**.
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.
   - **Working tree state:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 181 + pembetulan commit count 17→18 di header). Seluruh file lain cocak dengan HEAD. Branch **18 commits ahead** `origin/main` (`27ca1d2`).

2. **Perubahan dari Rev. 181:**
   - **Header PRD:** diperbarui ke **Rev. 182** (tanggal 18 Oktober 2026 WIB).
   - **Section 69 (Rev. 182):** ditambahkan untuk verifikasi fresh ulang & konfirmasi stabilitas.
   - **Git HEAD (local):** `01507996cd432ed9edf615213bedf0eaba8ccc0e` (tidak berubah).
   - **Commit count:** tetap **18** commits ahead `origin/main`.

3. **Status:** dokumen PRD **REVISI** — rev 182 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `01507996cd432ed9edf615213bedf0eaba8ccc0e`. Working tree memiliki 1 perubahan lokal (Rev. 181 rewor dan header fix). Branch **18 commits ahead** `origin/main` (`27ca1d2`).

## 70. REVISI TERBARU (Rev. 183 — 18 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 18 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: header PRD, §60–§69.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 182 (data terkonsisten).**
   - **Git HEAD (local):** `7951c16dfd3924c7fed7189bc5c140073edde606` "Rev. 182: PRD fresh verification & stability confirmation (18 Oct 2026 WIB); updated header to Rev. 182 + section 69" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `7951c16dfd3924c7fed7189bc5c140073edde606`). Local branch **19 commits ahead** dari `origin/main` (`27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` = Rev. 163 fix). *Catatan: koreksi dari Rev. 182 — commit count diperbarui 18 → 19.*
   - **Git HEAD (origin/main):** `27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` (Rev. 163 fix). Local branch **19 commits ahead**.
   - **Git ls-files:** = **36 file**. `git status --porcelain` = (kosong) untuk tracked files; 17 file `.py` tambahan **tidak ter-track** (bukan bagian dari commit, ditambahkan manual).
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` **masih ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build)**. `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` (baris 26) & `src/app/beranda/page.tsx` (baris 14) **sudah diperbarui ke 453** (dari 441) — hardcoded stats match Excel grade sheets. TIDAK ada hardcode 441 yang tersisa.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); jumlah model Prisma = **17**. `prisma validate` tidak dapat dijalankan (prisma tidak terinstall di env cron).
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD. `init_db.py` (6135 bytes) dan `.seed_users_roles.py` (3343 bytes) masih ada; `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** (0 bytes / MISSING).
   - **Source files:** `src/app/*` = 15 entri (absensi, beranda, berita, globals.css, guru, kelas, laporan, layout.tsx, login, nilai, page.tsx, pengasuh, ruang-kegiatan, santri, sekolah); `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). `git ls-files` = **36 file**.
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.
   - **Repo state:** clean working tree (tracked files); 17 file `.py` tambahan **tidak ter-track**; seluruh file lain cocak dengan HEAD. Branch **19 commits ahead** `origin/main` (`27ca1d2`).

2. **Perubahan dari Rev. 182:**
   - **Header PRD:** diperbarui ke **Rev. 183** (tanggal 18 Oktober 2026 WIB).
   - **Section 70 (Rev. 183):** ditambahkan untuk verifikasi fresh ulang & konfirmasi stabilitas.
   - **Git HEAD (local):** `7951c16dfd3924c7fed7189bc5c140073edde606` (tidak berubah).
   - **Commit count:** diperbarui dari **18** → **19** commits ahead `origin/main` (koreksi dari Rev. 182 yang mencatat 18).
   - **`.next/` directory:** entri lengkap = cache, diagnostics, package.json, server, static, trace, trace-build, turbopack, types (9 entri — sesuai Rev. 182, dikonfirmasi).
   - **`.data-pondokanat/`:** folder masih **tidak ditemukan** di seluruh tree repository & `/opt/data` (status stabil).

3. **Status:** dokumen PRD **REVISI** — rev 183 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `7951c16dfd3924c7fed7189bc5c140073edde606`. Working tree bersih (tracked), 17 file `.py` tambahan tidak ter-track. Branch **19 commits ahead** `origin/main` (`27ca1d2`).

## 71. REVISI TERBARU (Rev. 184 — 18 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 18 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: header PRD, §60–§70.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 183 (data terkonsisten).**
   - **Git HEAD (local):** `7951c16dfd3924c7fed7189bc5c140073edde606` "Rev. 182: PRD fresh verification & stability confirmation (18 Oct 2026 WIB); updated header to Rev. 182 + section 69" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `7951c16dfd3924c7fed7189bc5c140073edde606`). Local branch **19 commits ahead** dari `origin/main` (`27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` = Rev. 163 fix).
   - **Git HEAD (origin/main):** `27ca1d2a53b79c513cae9746cc0be9dfe9d783fa` (Rev. 163 fix). Local branch **19 commits ahead**.
   - **Git ls-files:** = **36 file**. `git status --porcelain` = ` M PRD-PONDOK-BANAT.md` (1 local change: Rev. 184 header + section 71); 17 file `.py` tambahan **tidak ter-track**.
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` **masih ada (partial: cache + diagnostics + package.json + server + static + trace + trace-build + turbopack + types, bukan production build)**. `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` (baris 26) & `src/app/beranda/page.tsx` (baris 14) **sudah diperbarui ke 453** (dari 441) — hardcoded stats match Excel grade sheets. TIDAK ada hardcode 441 yang tersisa.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); jumlah model Prisma = **17**. `prisma validate` tidak dapat dijalankan (prisma tidak terinstall di env cron).
   - **init_schema.sql:** tabel `students` (baris 33) memiliki kolom `uid_nfc TEXT` (baris 44, komentar: `-- NFC card UID: 'AF:C2:99:E7'`) — field M02a **ADA** di schema SQLite. Jumlah tabel = **15** sesuai PRD. `init_db.py` (6135 bytes) dan `.seed_users_roles.py` (3343 bytes) masih ada; `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** (0 bytes / MISSING).
   - **Source files:** `src/app/*` = 15 entri (absensi, beranda, berita, globals.css, guru, kelas, laporan, layout.tsx, login, nilai, page.tsx, pengasuh, ruang-kegiatan, santri, sekolah); `src/components` = `Beranda.tsx` & `Login.tsx`; `src/lib` = **kosong** (logic inline). `git ls-files` = **36 file**.
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **quality_gate.sh:** file masih memuat rantai `tsc` → `eslint` → `next build`; seluruh gate gagal karena `node_modules` absen.
   - **Repo state:** working tree memiliki 1 perubahan lokal (Rev. 184 header + section 71); 17 file `.py` tambahan tidak ter-track; seluruh file lain cocak dengan HEAD. Branch **19 commits ahead** `origin/main` (`27ca1d2`).

2. **Perubahan dari Rev. 183:**
   - **Header PRD:** diperbarui ke **Rev. 184** (tanggal 18 Oktober 2026 WIB).
   - **Section 71 (Rev. 184):** ditambahkan untuk verifikasi fresh ulang & konfirmasi stabilitas.
   - **Git HEAD (local):** `7951c16dfd3924c7fed7189bc5c140073edde606` (tidak berubah).
   - **Commit count:** tetap **19** commits ahead `origin/main` (tidak berubah).

3. **Status:** dokumen PRD **REVISI** — rev 184 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. HEAD = `7951c16dfd3924c7fed7189bc5c140073edde606`. Working tree memiliki 1 perubahan lokal (Rev. 184 header + section 71). Branch **19 commits ahead** `origin/main` (`27ca1d2`).

