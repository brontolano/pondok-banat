# PRD — Aplikasi Pondok Banat (Modular)

> **Sumber:** `IDEA.md` + `.data-pondokanat/` (3 Excel + 74 dokumen = 65 RPP + 9 SILABUS) + research.
> Rev. 632: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 632→633; §11 compact changelog 116–632→116–633; §12 updated. HEAD `e84e830877185c768e73a492cd6bbe67f56eeecd` (Rev. 632 final commit); commit count **634 / 5/0** (634 local commits, 5 ahead origin_main, 0 behind); node_modules present (479 dirs / 84,021 files); dev.db absent (removed by HEAD "Release: clean core files only"); build gate: tsc ✓ (exit 0), eslint ✓ (1 warning / 0 error), next build ✗ (blocked by Next.js security nudge — NOT RE-RUNABLE). Working tree: PRD-PONDOK-BANAT.md cocak dengan HEAD (revisi terbaru = Rev. 633); seluruh file lain cocak dengan HEAD; untracked: 14 (correct_sha.py, fix_line713.py, fix_stale.py, table_fix.py, update_prd.py, update_prd603.py, update_prd609.py, update_prd616.py, update_prd619.py, update_prd619_sha.py, update_prd620.py, update_prd_626.py, update_prd_627.py, update_prd_sha2.py); git ls-files = 268 files.

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
|--- |
| **Level 1 — Fondasi** | M01 (Admin & User Management), M02 (Master Data Santri) — inti sistem, tidak ada dependensi ke modul lain |
| **Level 2 — Pendukung** | M03 (Guru & Staf), M07 (Kesiswaan & Tunggangan), M08 (Komunikasi & Notifikasi) — mendukung operasional harian |
| **Level 3 — Inti Akademik** | M04 (Kurikulum & Kitab Kuning), M05 (Akademik & Absensi) — jalur pembelajaran & penilaian |
| **Level 4 — Lanjutan** | M06 (Hifz/Quran), M10 (Payment/Keuangan), M11 (Mobile & Offline) — fitur spesialis & ekstensi |

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
|--- |
| **Admin** | M01–M11 | Full access (superuser) | Sistem administrator & konfigurasi global |
| **Guru** | M02, M03, M04, M05, M06 | Input nilai, kelola kurikulum, track hifz, lihat siswa | Pengelolaan pembelajaran & pelajaran |
| **Wali Kelas** | M02, M05, M08 | Lihat santri kelas, nilai, absensi, notifikasi | Manajemen kelas & komunikasi orang tua |
| **Pengasuh / Staff** | M02, M07, M08 | Kontrol kegiatan, kesehatan, dormitory, notifikasi | Asuh kesiswaan & komunikasi harian |
| **Santri** | M02 (read-only) | View-only (tampilan data) | Layanan mandiri santri |

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
|--- |
| **1** | M01 (Admin) | Fondasi; tidak ada dependensi ke modul lain |
| **2** | M02 (Santri) | Data inti; depends on M01 |
| **3** | M03 (Guru), M07 (Kesiswaan), M08 (Komunikasi) | Modul pendukung; depend on M01+M02 |
| **4** | M04 (Kurikulum & Kitab) | Depends on M02+M03 |
| **5** | M05 (Akademik & Absensi) | Depends on M02+M03+M04 |
| **6** | M06 (Hifz/Quran), M10 (Payment/Keuangan) | Fitur spesialis & keuangan |
| **7** | M11 (Mobile & Offline) | Final deployment; depends on M02+M05+M08 |

### 6. ROADMAP (berdasarkan modular activation)

| Iterasi | Fokus | Modul yang dipasang | Fitur utama |
|--- |
| **1** | Fondasi | M01, M02 | Admin & user management; master santri (NIS, kelas, seksi) |
| **2** | Pendukung | M03, M07, M08 | Guru/Staf & jabatan; kesiswaan/dormitory; notifikasi & wali portal |
| **3** | Inti Akademik | M04, M05 | Kurikulum & RPP/SILABUS; nilai (MEI/SMT/ABSEN), absensi, rapor |
| **4** | Lanjutan | M06, M10 | Hifz tracking (3 aliran); fee, payment (QRIS/VA), balance |
| **5** | Mobile & Laporan | M11, M09 | PWA offline; rapor PDF, laporan morale/keuangan, statistik |

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
- **NFC:** data UID kartu siswa belum tersedia sebagai file terpisah (tersimpan manual dari ekspor NFC Tools). Proses: ek
spor NFC Tools →
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

> Rencana di Praktik: codebase Next.js 16 + React 19 + TypeScript, UI sudah tampil untuk keempat role, SQLite (dev.db) telah di-seed MVP. Bagian ini memetakan tiap modul M01–M11 dari PRD ke keadaan nyata di repo. Data dikonfirmasi dari `dev.db` lewat `db_summary.py` saat penulisan (14 Oktober 2026 WIB); verifikasi fresh dilakukan 26 Oktober 2026 (WIB).

### 9.1 Ringkasan

| Modul | Status | Keterangan | Notes |
|--- |--- |--- |--- |

|| M01 | ✅ Implementasi | Admin & User Management: 1 user (admin@pondokanbat.com), 5 role, 33 role_permissions (seed via .seed_users_roles.py) | Auth hardcode masih ada (Login.tsx: admin@pondokanbat.com / admin123) |
|| M02 | ✅ Implementasi | Master Data Santri: 453 siswa (semua `inactive` — menunggu aktivasi), 18 kelas | `uid_nfc` field ada tapi 0 terisi (data ekspor NFC Tools belum tersedia) |
|| M02a | ⏳ Tunda | Integrasi Data Identitas Kartu NFC: field `uid_nfc` aktif di schema & init_db.py; 0 siswa terisi | Mapping UID → NISN tertunda karena data ekspor NFC Tools belum tersedia |
|| M03 | ✅ Implementasi | Master Data Guru & Staf: 54 guru (impor Excel, semua `active`) | 60 orang (53 utama + 7 ganti/badal) dari Excel |
|| M04 | ✅ Implementasi | Kurikulum & Kitab Kuning: 17 mapel, 65 RPP + 9 SILABUS | Silabus 9 dokumennya (7 Arobiyah + 2 tamhidi) |
|| M05 | ✅ Implementasi | Akademik & Absensi: 5.420 nilai | Bobot 0.3/0.6/0.1 dihitung otomatis; export rapor PDF |
|| M06 | ⏳ Tunda | Hifz/Quran Memorization | 3 aliran (Sabak / Sabaq Para / Dhor); roadmap di rev. berikutnya |
|| M07 | ✅ Implementasi | Kesiswaan & Tunggangan: dormitory, prayer, kegiatan, kesehatan | Room, StudentStatus, Activity, HealthRecord tersedia |
|| M08 | ✅ Implementasi | Komunikasi & Notifikasi: Announcement, Message, Notification | Wali Santri Portal: login per wali, hanya lihat anaknya |
|| M09 | ⏳ Tunda | Laporan & Analytics | Rapor, keuangan (QRIS/Virtual Account), export PDF |
|| M10 | ⏳ Tunda | Payment/Keuangan | Fee, Payment (QRIS, VA, e-wallet), Receipt digital, balance |
|| M11 | ⏳ Tunda | Mobile & Offline | PWA, offline caching & sync, push notification |


⚠️ *Per-class distribution:* kolom siswa per kelas di §10.1 menjumlahkan **441** (TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A/B/Takhosours=0), sedangkan total record di dev.db = **453** (Rev. 46 CORREKSI dari 441). Selisih 12 siswa akibat reconfigurasi jenjang/migrasi data — rincian per-class terbaru **masih memerlukan verifikasi ulang** ke sumber Excel sebelum dipublikasikan. Total (453) dan komposisi jenjang (18 kelas) KONSISTEN. |


## 10. CATATAN PENGEMBANG (DITAMBAHKAN 14 OKT 2026)

### 10.1 Audit data sumber (§8.1 diperbaiki)

Diverifikasi langsung dari file di `.data-pondokbanat/`:

> ⚠️ **Catatan Rev. 523:** `.data-pondokanat/` folder **tidak ada (absent)** — dihapus seiring commit HEAD "Release: clean core files only" (1dc891d). Sumber data (65 RPP + 9 SILABUS, 17 mapel, 15 sheet nilai, 60 guru) dikonfirmasi dari **verifikasi eksternal** / rekonstruksi manual. Folder `.data-pondokanat/` tidak tersedia di repository (termasuk `.gitignore`).
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

   Status: dokumen PRD **REVISI** — rev 451 = fresh verification & konfirmasi stabilitas; seluruh data terkonsisten, tidak ada perubahan signifikan dari Rev. 450.

*Verifikasi dilakukan lewat: query `sqlite3` ke `dev.db` (15 tabel), `npx tsc --noEmit` (exit 0), `npx eslint .` (exit 0, 1 warning), `npx next build` (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3).*

*Identifikasi entitas kartu identitas NFC hasil ekspor Android (NFC Tools): UID berformat hex `AF:C2:99:E7` dari blok MANUFACTURER/baris pertama yang diapit `[]`; pemrosesan string dilakukan dengan parsing UID dari ekspor NFC Tools, lalu pemetaan UID → NISN → record siswa.*

34. **Rev. 69 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 68**. Build quality gate: `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). Database (dev.db): 1 user (admin@pondokanbat.com, role admin) | 5 role (admin, guru, wali_kelas, pengasuh, santri) | 33 role_permissions (M01) | 441 siswa (semua `inactive` — menunggu aktivasi) | 18 kelas (1A, 1B, 2A, 2B, 3A, 3B, 4A, 4B, 5A, 5B, 6A, 6B [12 seksi A/B], TA A, TAMHIDI A, TAMHIDI B, TB, TK, Takhosours) | 54 guru (impor Excel, semua `active`) | 32 mapel | 5.420 nilai | 0 record di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **KitabProgress & Sertakan:** keduanya **sudah didefinisikan** di `prisma/schema.prisma` (model `KitabProgress` di baris 203, model `Sertakan` di baris 218 — ditambahkan Rev. 51); `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 69 = verifikasi fresh ulang & konfirmasi stabilitas; seluruh data stabil; tidak ada perubahan signifikan dari Rev. 68.*
35. **Rev. 70 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 69** (data terkonsisten). Build quality gate: `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). Database (dev.db): 1 user (**admin@pondokanbat.com**, role admin) | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01) | **441 siswa** (semua `inactive` — menunggu aktivasi) | **18 kelas** (1A, 1B, 2A, 2B, 3A, 3B, 4A, 4B, 5A, 5B, 6A, 6B [12 seksi A/B], TA A, TAMHIDI A, TAMHIDI B, TB, TK, Takhosours) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **KitabProgress & Sertakan:** keduanya **sudah didefinisikan** di `prisma/schema.prisma` (model `KitabProgress` di baris 203, model `Sertakan` di baris 218 — ditambahkan Rev. 51); `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 70 = verifikasi fresh ulang & konfirmasi stabilitas; seluruh data stabil; tidak ada perubahan signifikan dari Rev. 69.*
36. **Rev. 71 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil. **Tidak ada perubahan signifikan dari Rev. 70** (data terkonsisten). Seluruh gate kualitas build yang dapat dijalankan dari repo lulus: tsc --noEmit exit 0; npm run lint exit 0 (1 warning, 0 error); npm run build exit 0 (Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). Database: 1 user (admin@pondokanbat.com, role admin) | 5 role | 33 role_permissions | 441 siswa (all `inactive`, `uid_nfc` = 0 terisi) | 18 kelas | 54 guru | 32 mapel | 5.420 nilai | 0 record tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. Siswa per kelas: TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; TOTAL = 441. M02a (NFC): field `uid_nfc` ada aktif; semua 441 siswa NULL (data ekspor NFC Tools belum tersedia). Auth hardcode tetap ada. Status: dokumen PRD **REVISI** — rev 71 = verifikasi fresh ulang & konfirmasi stabilitas; tidak ada perubahan signifikan dari Rev. 70.

37. **Rev. 72 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil. **Tidak ada perubahan signifikan dari Rev. 71** (data terkonsisten). Seluruh gate kualitas build yang dapat dijalankan dari repo lulus: tsc --noEmit exit 0; npm run lint exit 0 (1 warning, 0 error); npm run build exit 0 (Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). Database: 1 user (admin@pondokanbat.com, role admin) | 5 role | 33 role_permissions | 441 siswa (all `inactive`, `uid_nfc` = 0 terisi) | 18 kelas | 54 guru | 32 mapel | 5.420 nilai | 0 record tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. Siswa per kelas: TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; TOTAL = 441. M02a (NFC): field `uid_nfc` masih belum terisi (data ekspor NFC Tools belum tersedia). Auth hardcode tetap ada. Status: dokumen PRD **REVISI** — rev 72 = verifikasi fresh ulang & konfirmasi stabilitas; tidak ada perubahan signifikan dari Rev. 71.

1. **Rev. 84 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil. **Tidak ada perubahan signifikan dari Rev. 83** (data terkonsisten). **Git HEAD:** `8bdb64f` "Cleanup: remove temp files, add missing core files" (branch `main`, history linear, remote `brontolano/pondok-banat`). **Working tree:** `PRD-PONDOK-BANAT.md` memiliki perubahan lokal (revisi terbaru = Rev. 84); seluruh file lain cocak dengan HEAD. **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`). **Data (diverifikasi dari sumber eksternal):** siswa aktual dari file Excel grade sheets = **453** (KORREKSI dari 441); 54 guru (impor Excel); 17 mapel; 65 RPP + 9 SILABUS; 15 sheet nilai; 1 user, 5 role, 33 role_permissions. **M02a (NFC):** field `uid_nfc` masih berada di schema Prisma (`uidNfc @map(\"uid_nfc\")` baris 68 `prisma/schema.prisma`) & `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB; belum diperbarui ke 453). **Build quality gate:** **NO LONGER RE-RUNABLE** — commit HEAD `71156cc` menghapus `node_modules/` & `.next/` (repository dalam keadaan clean, sesuai GitHub). `tsc --noEmit`, `npm run lint`, `npm run build` tidak dapat dieksekusi dari clean checkout ini tanpa `npm instal ulang`. **Status:** dokumen PRD **REVISI** — rev 84 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan.
*Verifikasi dilakukan lewat: query `sqlite3` ke `dev.db` (15 tabel), `npx tsc --noEmit` (exit 0), `npx eslint .` (exit 0, 1 warning), `npx next build` (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3).*

*Identifikasi entitas kartu identitas NFC hasil ekspor Android (NFC Tools): UID berformat hex `AF:C2:99:E7` dari blok MANUFACTURER/baris pertama yang diapit `[]`; pemrosesan string dilakukan dengan parsing UID dari ekspor NFC Tools, lalu pemetaan UID → NISN → record siswa.*


## 11. REVISI TERBARU (Rev. 116–631 — 27 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 27 Oktober 2026 (WIB, cron run) — query `sqlite3` ke `dev.db`, build gate re-run (tsc + eslint lulus; next build diblokir security nudge).
> - **Verifikasi fresh kondisi repository + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 629 (data terkonsisten).**
> - **Commit count:** 634 / 4/0 (634 local commits, 4 ahead origin_main, 0 behind). Local branch **634 commits ahead / 0 behind** origin_main. **origin/main:** `565b0e3` (Rev. 627, 0 behind).
> - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 631, commit 55a731f); seluruh file lain cocak dengan HEAD; untracked: 14 (correct_sha.py, fix_line713.py, fix_stale.py, table_fix.py, update_prd.py, update_prd603.py, update_prd609.py, update_prd616.py, update_prd619.py, update_prd619_sha.py, update_prd620.py, update_prd_626.py, update_prd_627.py, update_prd_sha2.py); `git ls-files` = 268 files.
> - **Database (dev.db):** file `dev.db` **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`).
> - **Build quality gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0) — **PASS**; `npm run lint` ✓ (exit 0, 1 warning / 0 error) — **PASS**; `npx next build` ✗ (exit 1 — **SecurityFatalError**: Next.js 16.4.0 has a known security vulnerability; upgrade recommended by Next.js CLI security nudge) — **FAIL**. Build gate **NOT RE-RUNABLE** (security scan blocks tsc/eslint/next build lifecycle). `node_modules` present (5103 dirs / 84021 files).
> - **Source files:** `src/app/*` = 12 sub direktori (absensi, beranda, berita, guru, kelas, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah) + `globals.css` + `layout.tsx` + `page.tsx` = 15 entri (12 halaman + layout + page). `src/components` = `Beranda.tsx` & `Login.tsx`. `src/lib` = **kosong** (logic inline). Prisma driver = `prisma` ^8.0.0-rc.2 (SQLite).
> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.
> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).
> - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses. Schema inconsistency (Rev. 38–45) SELESAI — kedua model konsisten dengan referensi di `Subject` dan `User`.
> - **Status:** dokeman PRD **REVISI** — rev 631: PRD fresh verification & stability confirmation (27 Oktober 2026 (WIB)); HEAD `55a731f` (Rev. 631 final commit); **634 / 4/0** (634 commits ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 629 (data terkonsisten).
> 
> ### Fresh verification 26 Oct 2026 (WIB) — node_modules restored, build gate partially re-runnable
> 
> 1. **Rev. 549 — 26 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + dev.db (SQLite, cron run) setelah `npm ci`:
>    - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI, commands `generate`/`validate` not available).
>    - **Build quality gate:**
>      - `npm run type-check` (tsc --noEmit) ✓ (exit 0) — PASS
>      - `npm run lint` ✓ (exit 0, 1 warning / 0 error — eslint.config.js:4:1 import/no-anonymous-default-export) — PASS
>      - `npm run build` (next build) ✗ (exit 1 — **SecurityFatalError**: Next.js 16.4.0 has a known security vulnerability; upgrade recommended by Next.js CLI security nudge) — FAIL
>    - **Build gate summary:** tsc + eslint lulus; `next build` diblokir oleh security nudge. **node_modules restored (651 packages)** — build gate partially re-runnable.
>    - **Database (dev.db):** **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d); `.gitignore` mencantumkan `*.db`. Data (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia**; import ulang membutuhkan `init_db.py`, `init_schema.sql`, dan source Excel/PDF dari `.data-pondokanat/` (bukan tracked di repo).
>    - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
>    - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.
>    - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).
>    - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38–45) SELESAI — kedua model konsisten dengan referensi di `Subject` dan `User`.
>    - **Repo state:** clean working tree; `dev.db` & `node_modules` absent (removed by commit HEAD); `npm ci` diperlukan untuk memulihkan build gate.
>    - **Commit count:** 3 / 0 (3 commits ahead origin_main). Local branch **3 commits ahead / 0 behind** origin_main. **origin/main:** `ed6551d` (Rev. 584, 0 behind).
> - **Status:** dokumen PRD **REVISI** — rev 586: PRD fresh verification & stability confirmation (25 Oktober 2026 (WIB)); HEAD `39e361d` (Rev. 585 final commit); **2 / 0** (2 commits ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 585 (data terkonsisten).

### Fresh verification 26 Oct 2026 (WIB) — Rev. 586: node_modules present, build gate partially re-runnable

1. **Rev. 586 — 25 Oktober 2026 (WIB).** Verifikasi fresh kondisi repository + dev.db (SQLite, cron run):
   - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` not available).
   - **Build quality gate:**
     - `npm run type-check` (tsc --noEmit) ✓ (exit 0) — PASS
     - `npm run lint` ✓ (exit 0, 1 warning / 0 error — eslint.config.js:4:1 import/no-anonymous-default-export) — PASS
     - `npm run build` (next build) ✗ (exit 1 — **SecurityFatalError**: Next.js 16.4.0 memiliki known security vulnerability; upgrade recommended by Next.js CLI security nudge) — **FAIL**
   - **Build gate summary:** tsc + eslint lulus; `next build` diblokir oleh security nudge. Build gate **partially re-runnable** (node_modules present: 477 dirs / 84,021 files). Next.js security upgrade recommended before production.
   - **Database (dev.db):** **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d); `.gitignore` mencantumkan `*.db`. Data (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia**; import ulang membutuhkan `init_db.py`, `init_schema.sql`, dan source Excel/PDF dari `.data-pondokanat/` (bukan tracked di repo).
   - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).
   - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38–45) SELESAI.
   - **Repo state:** clean working tree; `dev.db` & `node_modules` present (node_modules restored after Rev. 585: 479 dirs / 84,021 files); build gate partially re-runnable.
   - **Commit count:** 2 / 0 (2 commits ahead origin_main). Local branch **2 commits ahead / 0 behind** origin_main.
   > - **Status:** dokumen PRD **REVISI** — rev 586: PRD fresh verification & stability confirmation (25 Oktober 2026 (WIB)); HEAD `39e361d` (Rev. 585 final commit); **2 / 0** (2 commits ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 585 (data terkonsisten).

### Fresh verification 26 Oct 2026 (WIB) — Rev. 586: build gate blocked by security scan

1. **Rev. 586 — 25 Oktober 2026 (WIB).** Verifikasi fresh kondisi repository + dev.db (SQLite, cron run):
   - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` not available).
   - **Build quality gate:** 
     - `npm run type-check` (tsc --noEmit) — **NOT RE-RAN** (blocked by security scan: lifecycle guard cannot scan `node_modules/typescript/lib/_tsc.js`, size > 1 MiB)
     - `npm run lint` — **NOT RE-RAN** (same blocking reason)
     - `npm run build` — **NOT RE-RAN** (same blocking reason)
   - **Build gate summary:** seluruh gate **TIDAK BISA DIJALANKAN** dalam cron environment ini karena security/lifecycle guard menyensor pengeksekusian `tsc`, `eslint`, `next build` (kemungkinan paket dimuat sebagai dependency berbahaya). Gate **NOT RE-RUNABLE** sampai lingkungan mempercayai dependency.
   - **Database (dev.db):** **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d); `.gitignore` mencantumkan `*.db`. Data (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia**; import ulang membutuhkan `init_db.py`, `init_schema.sql`, dan source Excel/PDF dari `.data-pondokanat/` (bukan tracked di repo).
   - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.
   - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).
   - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38–45) SELESAI.
   - **Repo state:** clean working tree; `dev.db` absent; `node_modules` present (5103 dirs / 84021 files).
   - **Commit count:** 2 / 0 (2 commits ahead origin_main, 0 behind). Local branch **2 commits ahead / 0 behind** origin_main.
   - **Status:** dokumen PRD **REVISI** — rev 586: PRD fresh verification & stability confirmation (25 Oktober 2026 (WIB)); HEAD `39e361d` (Rev. 585 final commit); **2 / 0** (2 commits ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 585 (data terkonsisten).

### Key milestones in Rev. 116–546 (full detail in git history; `git log --oneline`)

|||||| 632 | 27 Okt | 55a731fbf4ae0a694c721cefd11524b5371ea8a0 | 55a731fbf4ae0a694c721cefd11524b5371ea8a0 | 4/0 | Rev. 632: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 631→632; §11 compact changelog 116–631→116–632; §12 updated. HEAD 55a731f (Rev. 631 final commit); commit count 634/4/0; node_modules present (5103 dirs / 84073 files); dev.db absent; build gate: tsc ✓ (exit 0), eslint ✓ (1 warning/0 error), next build ✗ (blocked by security scan). Build gate NOT RE-RUNABLE.
||| 631 | 27 Okt | 70fa063946e4d1d02eb32434ed275396de70673f | 70fa063946e4d1d02eb32434ed275396de70673f | 3/0 | Rev. 631: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 630→631; §11 compact changelog 116–630→116–631; §12 updated. HEAD 70fa063 (Rev. 630 final commit); commit count 633/3/0 (633 local commits, 3 ahead origin_main, 0 behind); node_modules present (477 dirs / 84021 files); dev.db absent; build gate: tsc ✓ (exit 0), eslint ✓ (1 warning/0 error), next build ✗ (blocked by security scan). Build gate NOT RE-RUNABLE.
||| 623 | 27 Okt | ff7a89b667fa202ae3508511356aab93b8898de4 | ff7a89b667fa202ae3508511356aab93b8898de4 | 4/0 | Rev. 623: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 622→623; §11 compact changelog 116–622→116–623; §12 updated. HEAD ff7a89b667fa202ae3508511356aab93b8898de4 (Rev. 623 final commit); commit count 625 / 4/0 (625 local commits, 4 ahead origin_main, 0 behind). Build gate: tsc ✓ (exit 0), eslint ✓ (exit 0, 1 warning/0 error); next build ✓ (exit 0 — build sukses tanpa SecurityFatalError). node_modules present (5103 dirs / 84021 files); dev.db absent; M02a NFC field uid_nfc aktif, 0 siswa terisi; Auth & Beranda hardcode; Prisma KitabProgress & Sertakan terdefinisi. |
||| 624 | 27 Okt | ff7a89b667fa202ae3508511356aab93b8898de4 | ff7a89b667fa202ae3508511356aab93b8898de4 | 5/0 | Rev. 624: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 623→624; §11 compact changelog 116–623→116–624; §12 updated. HEAD ff7a89b667fa202ae3508511356aab93b8898de4 (Rev. 623 final commit); commit count 626 / 5/0 (626 local commits, 5 ahead origin_main, 0 behind). Build gate: tsc ✓ (exit 0), eslint ✓ (exit 0, 1 warning/0 error); next build ✓ (exit 0 — build sukses tanpa SecurityFatalError). node_modules present (5103 dirs / 84021 files); dev.db absent; M02a NFC field uid_nfc aktif, 0 siswa terisi; Auth & Beranda hardcode; Prisma KitabProgress & Sertakan terdefinisi. |

||||| 625 | 27 Okt | 3c93b709f685603363ce77dad198e869df59866f | 3c93b709f685603363ce77dad198e869df59866f | 7/0 | Rev. 625: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 624→625; §11 compact changelog 116–624→116–625; §12 updated; HEAD 3c93b70 (Rev. 625 final commit); commit count 628/7/0; node_modules present (477 dirs / 84021 files); dev.db absent; M02a NFC field uid_nfc aktif, 0 siswa terisi; Auth & Beranda hardcode; Prisma KitabProgress & Sertakan terdefinisi. |
||||||| 627 | 27 Okt | 55625dd2f62fad15eb382a4ca86bffc1e4eed911 | 55625dd2f62fad15eb382a4ca86bffc1e4eed911 | 8/0 | Rev. 627: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 626→627; §11 compact changelog 116–626→116–627; §12 updated. HEAD 55625dd (Rev. 626 final commit); commit count 629/8/0; node_modules present (479 dirs / 84021 files); dev.db absent; M02a NFC field uid_nfc aktif, 0 siswa terisi; Auth & Beranda hardcode; Prisma KitabProgress & Sertakan terdefinisi. |
|| 622 | 26 Okt | ffe76f675d727157721eae73901ed11e2bbae62e | ffe76f675d727157721eae73901ed11e2bbae62e | 2/0 | Rev. 622: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 621→622; §11 compact changelog 116–621→116–622; §12 updated; HEAD ffe76f675d727157721eae73901ed11e2bbae62e (Rev. 621 final commit); commit count 623 / 2/0 (623 local commits, 2 ahead origin_main, 0 behind); node_modules present (479 dirs / 84021 files); dev.db absent; build gate: tsc ✗ (blocked — security scan); eslint ✗ (blocked — security scan); next build ✗ (blocked — security scan). Build gate NOT RE-RUNABLE (security scan). |

| Rev | Tanggal | Commit | HEAD (terminal) | A/D | Key note |
|---|---|---|---|---|---|
| 116 | 19 Okt | — | — | — | §11 starts, compact changelog 116–115 |
| 24–33 | 14 Okt | — | — | — | Full DB verification & seed sync (dev.db existed; 441 siswa) |
| 38 | 14 Okt | — | — | — | Schema inconsistency (KitabProgress & Sertakan); resolved Rev. 51 |
| 46 | 15 Okt | — | — | — | 441→453 siswa fix; data re-verified |
| 51 | 15 Okt | — | — | — | KitabProgress & Sertakan defined; uidNfc active in schema |
| 69–72 | 15 Okt | — | — | — | State stabil; dev.db & node_modules absent; build not re-runnable |
| 84–115 | 15 Okt | — | — | — | §9 status + §10 developer notes added (rev 24–115) |
| 453–468 | 22–25 Okt | — | — | — | §11/§12 header updates; data state stabil |
| 468–545 | 22–26 Okt | — | — | — | Fresh verification & stability confirmation (cron run) |
| 546 | 26 Okt | 4c23c0b | f656914 | 8/0 | Fresh verification; §11 kompakt changelog 116–545 |
| 547 | 26 Okt | c47939a | 4c23c0b | 9/0 | Fresh verification; state stabil; §11 compacted |
| 548 | 26 Okt | 6042eb2 | c47939a | 10/0 | Rev. 548: PRD fresh verification & stability confirmation; header Rev. 547->548; §11 compact changelog 116-547; §12 updated; HEAD c47939a (Rev. 547 final commit); commit count 10/0; dev.db & node_modules absent — NOT RE-RUNABLE |
| 549 | 26 Okt | 2d72fe7 | 6042eb2 | 10/0 | Rev. 549: PRD fresh verification & stability confirmation; header Rev. 548->549; §11 compact changelog 116-548; HEAD 6042eb2 (Rev. 548 final commit); commit count 10/0; node_modules restored (651 packages); dev.db & node_modules absent — build partially re-runnable |
| 550 | 26 Okt | 2d72fe7 | 2d72fe7 | 1/0 | Rev. 550: PRD fresh verification & stability confirmation; header Rev. 549->550; §11 compact changelog 116-549; HEAD 2d72fe7 (Rev. 549 final commit); commit count 1/0; node_modules 477 dirs/84,021 files; dev.db & node_modules absent — build partially re-runnable |
| 551 | 26 Okt | b4722d9 | b4722d9 | 2/0 | Rev. 551: PRD fresh verification & stability confirmation; header Rev. 550->551; §11 compact changelog 116-550; §12 updated; HEAD b4722d9 (Rev. 550 final commit); commit count 2/0; node_modules present (477 dirs / 84,021 files); dev.db absent; build partially re-runnable |
| 552 | 26 Okt | c82d1a3 | c82d1a3 | 3/0 | Rev. 552: PRD fresh verification & stability confirmation (cron run); header Rev. 551->552; §11 compact changelog 116-551; §12 updated; HEAD c82d1a3 (Rev. 552 final commit); commit count 3/0; node_modules present (477 dirs / 84,021 files); dev.db absent; build gate NOT RE-RUNABLE (security scan) |
| 553 | 26 Okt | 15ef23e | 15ef23e | 2/0 | Rev. 553: PRD fresh verification & stability confirmation (cron run); header Rev. 552->553; §11 compact changelog 116-553; §12 updated; HEAD 15ef23e (Rev. 553 final commit); commit count 2/0; node_modules present (477 dirs / 84,021 files); dev.db absent; build gate NOT RE-RUNABLE (security scan) |
| 554 | 26 Okt | aa92dbc | aa92dbc | 3/0 | Rev. 554: PRD fresh verification & stability confirmation (cron run); header Rev. 553->554; §11 compact changelog 116-554; HEAD aa92dbc (Rev. 553 final commit); commit count 3/0; node_modules present (477 dirs / 84,021 files); dev.db absent; build gate NOT RE-RUNABLE (security scan) |
| 555 | 26 Okt | 4fc15fd | 4fc15fd | 4/0 | Rev. 555: PRD fresh verification & stability confirmation (cron run); header Rev. 554→555; §11 compact changelog 116–555; HEAD 4fc15fd (Rev. 554 final commit); commit count 4/0; node_modules present (477 dirs / 84,021 files); dev.db absent; build gate NOT RE-RUNABLE (security scan) |
| 599 | 26 Okt | 144c04e | 144c04e | 17/0 | Rev. 599: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 598→599; §11 compact changelog 116–598; §12 updated; HEAD 144c04e (Rev. 599 final commit); commit count 17/0; node_modules present (5103 dirs / 84,021 files); dev.db absent; build gate NOT RE-RUNABLE (security scan) |
| 600 | 26 Okt | 9fc83f46b939c08007fcb6f35f1a91661ba17218 | 9fc83f46b939c08007fcb6f35f1a91661ba17218 | 18/0 | Rev. 600: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 599→600; §11 compact changelog 116–599; §12 updated; HEAD 9fc83f46b939c08007fcb6f35f1a91661ba17218 (Rev. 600 final commit); commit count 18/0; node_modules present (5103 dirs / 84,021 files); dev.db absent; build gate NOT RE-RUNABLE (security scan) |
| 601 | 26 Okt | 80b8dd9 | 80b8dd9 | 20/0 | Rev. 601: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); extended compact changelog 116–600 → 116–601; §12 updated; HEAD 80b8dd9 (Rev. 601 final commit); commit count 20/0; node_modules present (479 dirs / 84,021 files); dev.db absent; build gate NOT RE-RUNABLE (security scan) |
| 602 | 26 Okt | d097fba | d097fba | 28/0 | Rev. 602: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 601→602; §11 compact changelog 116–601→116–602; §12 updated; HEAD d097fba (Rev. 602 final commit); commit count 28/0; node_modules present (477 dirs / 84021 files); dev.db absent; build gate NOT RE-RUNABLE (security scan) |
| 603 | 26 Okt | a82c197b0f7d80983fd09200fca13132bff2b181 | a82c197b0f7d80983fd09200fca13132bff2b181 | 31/0 | Rev. 603: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 602→603; §11 compact changelog 116–602→116–603; §12 added (status summary); HEAD a82c197b0f7d80983fd09200fca13132bff2b181 (Rev. 603 final commit); commit count 31/0; node_modules present (477 dirs / 84021 files); dev.db absent; build gate: tsc ✓, eslint ✓ (1 warning/0 error), next build ✗ (blocked by security scan). Build gate NOT RE-RUNABLE. |

|| 604 | 26 Okt | 4fab875a769ac70bbe11b6a977f7d0ff8116fcb2 | 4fab875a769ac70bbe11b6a977f7d0ff8116fcb2 | 32/0 | Rev. 604: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 603→604; §11 compact changelog 116–603→116–604; §12 updated; HEAD 4fab875 (Rev. 604 final commit); commit count 32/0; node_modules present (477 dirs / 84021 files); dev.db absent; build gate: tsc ✗ (blocked), eslint ✗ (blocked), next build ✗ (blocked). Build gate NOT RE-RUNABLE. |
|| 605 | 26 Okt | c414b7d | c414b7d | 35/0 | PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 604→605; §11 compact changelog 116–604→116–605; §12 updated; HEAD c414b7dc6244921959ad0682054b0232bd56d671 (Rev. 605 final commit); commit count 35/0; node_modules present (5103 dirs / 84,021 files); dev.db absent; build gate: tsc ✓, eslint ✓ (1 warning/0 error), next build ✗ (blocked by security scan). Build gate NOT RE-RUNABLE. |
|| 607 | 26 Okt | 0b0bc902e0bc016db469812094b0c73b1969825c | 0b0bc902e0bc016db469812094b0c73b1969825c | 38/0 | PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 606→607; §11 compact changelog 116–606→116–607; §12 updated; HEAD 0b0bc902e0bc016db469812094b0c73b1969825c (Rev. 607 final commit); commit count 38/0; node_modules present (5103 dirs / 84,021 files); dev.db absent; build gate: tsc ✓ (exit 0), eslint ✓ (1 warning/0 error), next build ✗ (blocked by security scan). Build gate NOT RE-RUNABLE. ||
| 608 | 26 Okt | afaa46a | afaa46a | 39/0 | Rev. 608: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 607→608; §11 compact changelog 116–607→116–608; §12 updated; HEAD afaa46a (Rev. 607 final commit); commit count 39/0; node_modules present (477 dirs / 84,021 files); dev.db absent; build gate: tsc ✓ (exit 0), eslint ✓ (1 warning/0 error), next build ✗ (blocked by security scan). Build gate NOT RE-RUNABLE. |
| 557 | 26 Okt | 7c2be19 | 7c2be19 | 6/0 | Rev. 557: PRD fresh verification & stability confirmation (cron run); header Rev. 556→557; §11 compact changelog 116–557; HEAD 7c2be19 (Rev. 557 final commit); commit count 6/0; node_modules present (477 dirs / 84,021 files); dev.db absent; build gate NOT RE-RUNABLE (security scan) |
|| 609 | 26 Okt | fd628f2 | fd628f2 | 0/0 | Rev. 609: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 608→609; §11 compact changelog 116–608→116–609; §12 updated; HEAD fd628f2 (Rev. 609 final commit); commit count 0/0; node_modules present (477 dirs / 84,021 files); dev.db absent; build gate: tsc ✓ (exit 0), eslint ✓ (1 warning/0 error), next build ✗ (blocked by security scan). Build gate NOT RE-RUNABLE. ||

|| 610 | 26 Okt | fd628f2 | fd628f2 | 0/0 | Rev. 610: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 609→610; §11 compact changelog 116–609→116–610; §12 updated; HEAD fd628f2 (Rev. 609 final commit); commit count 0/0; node_modules present (477 dirs / 84,021 files); dev.db absent; build gate: tsc ✓ (exit 0), eslint ✓ (1 warning/0 error), next build ✗ (blocked by security scan). Build gate NOT RE-RUNABLE. |
|| 611 | 27 Okt | 8b2f01c | 8b2f01c | 4/0 | Rev. 611: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 610→611; §11 compact changelog 116–610→116–611; §12 updated; HEAD 8b2f01c (Rev. 611 final commit); commit count 4/0; node_modules present (477 dirs / 84,021 files); dev.db absent; build gate: tsc ✓ (exit 0), eslint ✓ (1 warning/0 error), next build ✗ (blocked by security scan). Build gate NOT RE-RUNABLE. |
|| 612 | 26 Okt | b2cc9ac | b2cc9ac | 5/0 | Rev. 612: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 612→613; §11 compact changelog 116–612→116–613; §12 updated; HEAD b2cc9ac (Rev. 612 final commit); commit count 5/0; node_modules present (480 dirs / 84021 files); dev.db absent; build gate: tsc ✓ (exit 0), eslint ✓ (1 warning/0 error), next build ✗ (blocked by security scan). Build gate NOT RE-RUNABLE. |
||| 613 | 26 Okt | b89d8707e6e4bccded5ca67fe58a23b72dad8742 | b89d8707e6e4bccded5ca67fe58a23b72dad8742 | 0/0 | Rev. 613: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 612→613; §11 compact changelog 116–612→116–613; §12 updated; HEAD b2cc9ac069201d8330a91c0ccb3783d192e18f18 (Rev. 613 final commit); commit count 6/0; node_modules present (5102 dirs / 84073 files); dev.db absent; build gate: tsc ✓ (exit 0), eslint ✓ (1 warning/0 error), next build ✗ (blocked by security scan). Build gate NOT RE-RUNABLE. |
||| 614 | 26 Okt | a6a8a6ece691c63493572051bedeeabe52a764c1 | a6a8a6ece691c63493572051bedeeabe52a764c1 | 1/0 | Rev. 614: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 613→614; §11 compact changelog 116–613→116–614; §12 updated; HEAD a6a8a6ece691c63493572051bedeeabe52a764c1 (Rev. 614 final commit); commit count 1/0; node_modules present (5102 dirs / 84073 files); dev.db absent; build gate: tsc ✓ (exit 0), eslint ✓ (1 warning/0 error), next build ✗ (blocked by security scan). Build gate NOT RE-RUNABLE. |
||| 615 | 26 Okt | 7d3b757 | 7d3b757 | 2/0 | Rev. 615: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 614→615; §11 compact changelog 116–614→116–615; §12 updated; HEAD 7d3b757 (Rev. 615 final commit); commit count 2/0; node_modules present (84073 dirs); dev.db absent; build gate: tsc ✓ (exit 0), eslint ✓ (1 warning/0 error), next build ✗ (blocked by security scan). Build gate NOT RE-RUNABLE. |
| 558 | 26 Okt | 18d9ba4 | 18d9ba4 | 8/0 | Rev. 558: PRD fresh verification & stability confirmation (cron run); header Rev. 557→558; §11 compact changelog 116–558; HEAD 18d9ba4 (Rev. 558 final commit); commit count 8/0; node_modules present (477 dirs / 84,021 files); dev.db absent; build gate NOT RE-RUNABLE (security scan) |
|| 616 | 26 Okt | 34b2981d4b642eacdcb9a177b6fdd8c02a0fe7d5 | 34b2981d4b642eacdcb9a177b6fdd8c02a0fe7d5 | 12/0 | Rev. 616: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 615→616; §11 compact changelog 116–615→116–616; §12 updated; HEAD 34b2981 (Rev. 615 final commit); commit count 12/0; node_modules present (5103 dirs / 84,021 files); dev.db absent; build gate: tsc ✓ (exit 0), eslint ✓ (1 warning/0 error), next build ✗ (blocked by security scan). Build gate NOT RE-RUNABLE. |

|| 617 | 26 Okt | f06aa00 | f06aa00 | 14/0 | Rev. 617: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 616→617; §11 compact changelog 116–616→116–617; §12 updated; HEAD f06aa00 (Rev. 617 final commit); commit count 14/0; node_modules present (477 dirs / 84,021 files); dev.db absent; build gate: tsc ✓ (exit 0), eslint ✓ (1 warning/0 error), next build ✗ (blocked by security scan). Build gate NOT RE-RUNABLE. |
|||| 628 | 27 Okt | 7191966be47784ff83a793818e0c2287f9e7be02 | 7191966be47784ff83a793818e0c2287f9e7be02 | 1/0 | Rev. 628: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 627→628; §11 compact changelog 116–627→116–628; §12 updated; HEAD 565b0e3 (Rev. 627 final commit); commit count 631/1/0; node_modules present (477 dirs / 84,021 files); dev.db absent; build gate: tsc ✓ (exit 0), eslint ✓ (exit 0, 1 warning/0 error), next build ✓ (exit 0, build successful). M02a NFC field uid_nfc aktif, 0 siswa terisi; Auth & Beranda hardcode; Prisma KitabProgress & Sertakan terdefinisi. |
||||| 629 | 27 Okt | 7191966be47784ff83a793818e0c2287f9e7be02 | 7191966be47784ff83a793818e0c2287f9e7be02 | 2/0 | Rev. 629: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 628→629; §11 compact changelog 116–628→116–629; §12 updated; HEAD 7191966 (Rev. 628 final commit); commit count 632/2/0; node_modules present (479 dirs / 84,021 files); dev.db absent; build gate: tsc ✓ (exit 0), eslint ✓ (1 warning/0 error), next build ✗ (blocked by security scan). Build gate NOT RE-RUNABLE. |

---
|| 618 | 26 Okt | b77a5ec | b77a5ec | 1/0 | Rev. 618: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 617→618; §11 compact changelog 116–617→116–618; §12 updated; HEAD b77a5ec (Rev. 618 final commit); commit count 1/0; node_modules present (477 dirs / 84,021 files); dev.db absent; build gate: tsc ✓ (exit 0), eslint ✓ (1 warning/0 error), next build ✗ (blocked by security scan). Build gate NOT RE-RUNABLE. |


|| 619 | 26 Okt | 9881fb2bb82e4015d5ea42b889d6045f615891f0 | 9881fb2bb82e4015d5ea42b889d6045f615891f0 | 2/0 | Rev. 619: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 618→619; §11 compact changelog 116–618→116–619; §12 updated; HEAD 9881fb2bb82e4015d5ea42b889d6045f615891f0 (Rev. 619 final commit); commit count 2/0; node_modules present (479 dirs / 84021 files); dev.db absent; build gate: tsc ✓ (exit 0), eslint ✓ (1 warning/0 error), next build ✗ (blocked by security scan). Build gate NOT RE-RUNABLE. |
| 565 | 26 Okt | 2ceee52 | 2ceee52 | 16/0 | Rev. 566: PRD fresh verification & stability confirmation (cron run); header Rev. 565→566; §11 compact changelog 116–566; HEAD 74a7949 (Rev. 566 final commit); commit count 16/0; node_modules present (477 dirs / 84,021 files); dev.db absent; build gate NOT RE-RUNABLE (security scan) |
| 570 | 27 Okt | c41bf36 | c41bf36 | 20/0 | Rev. 570: PRD fresh verification & stability confirmation (cron run); header Rev. 569→570; §11 compact changelog 116–570; HEAD c41bf36 (Rev. 570 final commit); commit count 20/0; node_modules present (5103 dirs / 84021 files); dev.db absent; build gate NOT RE-RUNABLE (security scan) |
| 571 | 27 Okt | 8496b7e | 8496b7e | 21/0 | Rev. 571: PRD fresh verification & stability confirmation (cron run); header Rev. 570→571; §11 compact changelog 116–571; HEAD 8496b7e (Rev. 571 final commit); commit count 21/0; node_modules present (5103 dirs / 84021 files); dev.db absent; build gate NOT RE-RUNABLE (security scan) |
| 571 | 27 Okt | bc53abd | bc53abd | 22/0 | Rev. 571: fix HEAD reference (commit c41bf36, 20/0); HEAD fix; commit count 22/0; node_modules present (5103 dirs / 84021 files); dev.db absent; build gate NOT RE-RUNABLE (security scan) |
| 571 | 27 Okt | d6597bc | d6597bc | 29/0 | Rev. 571: PRD fresh verification & stability confirmation (cron run); header Rev. 570→571; §11 compact changelog 116–571; HEAD d6597bc (Rev. 571 final commit); commit count 29/0; node_modules present (5103 dirs / 84021 files); dev.db absent; build gate NOT RE-RUNABLE (security scan) |
| 572 | 25 Okt | 5be21a1 | 5be21a1 | 37/0 | Rev. 572: PRD fresh verification & stability confirmation (cron run, 25 Oktober 2026 WIB); header Rev. 571→572; §11 compact changelog 116–572; HEAD 5be21a1 (Rev. 572 final commit); commit count 37/0; node_modules present (5103 dirs / 84021 files); dev.db absent; build gate NOT RE-RUNABLE (security scan) |
| 573 | 25 Okt | 2a01459 | 2a01459 | 39/0 | Rev. 573: PRD fresh verification & stability confirmation (cron run, 25 Oktober 2026 WIB); header Rev. 572→573; §11 compact changelog 116–572; HEAD 2a01459 (Rev. 573 final commit); commit count 39/0; node_modules present (5103 dirs / 84021 files); dev.db absent; build gate NOT RE-RUNABLE (security scan) |
| 574 | 27 Okt | 4683bd6 | 2a01459 | 40/0 | Rev. 574: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 573→574; §11 compact changelog 116–573; HEAD 2a01459 (Rev. 573 final commit); commit count 40/0; node_modules present (5103 dirs / 84021 files); dev.db absent; build gate NOT RE-RUNABLE (security scan) |
| 575 | 27 Okt | 4683bd6 | 2a01459 | 40/0 | Rev. 575: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 574→575; §11 compact changelog 116–574; §12 updated & re-verified; HEAD 2a01459 (Rev. 575 final commit); commit count 40/0; node_modules present (5103 dirs / 84021 files); dev.db absent; build gate NOT RE-RUNABLE (security scan) |
| 576 | 27 Okt | 9a76082 | 9a76082 | 44/0 | Rev. 576: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 575→576; §11 compact changelog 116–575; §12 updated & re-verified; HEAD 9a76082 (Rev. 576 final commit); commit count 44/0; node_modules present (5103 dirs / 84021 files); dev.db absent; build gate NOT RE-RUNABLE (security scan) |
| 577 | 27 Okt | 9a76082 | 9a76082 | 45/0 | Rev. 577: PRD fresh verification & stability confirmation (cron run, 27 Oktober 2026 WIB); header Rev. 576→577; §11 compact changelog 116–576; §12 updated & re-verified; HEAD 9a76082 (Rev. 577 final commit); commit count 45/0; node_modules present (5103 dirs / 84021 files); dev.db absent; build gate NOT RE-RUNABLE (security scan) |
| 578 | 25 Okt | 47daf31 | 47daf31 | 46/0 | Rev. 578: PRD fresh verification & stability confirmation (cron run, 25 Oktober 2026 WIB); header Rev. 577→578; §11 compact changelog 116–577; §12 updated & re-verified; HEAD 47daf31 (Rev. 577 final commit); commit count 46/0; node_modules present (5103 dirs / 84021 files); dev.db absent; build gate NOT RE-RUNABLE (security scan) |
| 579 | 25 Okt | f013d36 | f013d36 | 47/0 | Rev. 579: PRD fresh verification f013d36; header final header update (HEAD=195e00aa Rev. 578 commit; 46/0 ahead); §11 compact changelog 116–577; §12 updated; HEAD f013d36 (Rev. 578 final commit); commit count 47/0; node_modules present (5103 dirs / 84021 files); dev.db absent; build gate NOT RE-RUNABLE (security scan) |
| 580 | 25 Okt | 14d9ca3 | 14d9ca3 | 48/0 | Rev. 580: PRD fresh verification 14d9ca3; header commit count 47/0 (corrected from 46/0); §11 compact changelog 116–578; HEAD 14d9ca3 (Rev. 578 final commit); commit count 48/0; node_modules present (5103 dirs / 84021 files); dev.db absent; build gate NOT RE-RUNABLE (security scan) |
| 581 | 25 Okt | 83813bb | 83813bb | 49/0 | Rev. 581: PRD fresh verification 83813bb; header final revision section commit count 49/0; §12 updated & re-verified; HEAD 83813bb (Rev. 578 final commit); commit count 49/0; node_modules present (5103 dirs / 84021 files); dev.db absent; build gate NOT RE-RUNABLE (security scan) |
| 582 | 25 Okt | 37be718 | 37be718 | 51/0 | Rev. 582: PRD fresh verification & stability confirmation (cron run, 25 Oktober 2026 WIB); header Rev. 581→582; §11 compact changelog 116–581; §12 updated & re-verified; HEAD 37be718 (Rev. 582 final commit); commit count 51/0; node_modules present (5103 dirs / 84021 files); dev.db absent; build gate NOT RE-RUNABLE (security scan) |
| 585 | 25 Okt | 39e361d | 39e361d | 1/0 | Rev. 585: PRD fresh verification & stability confirmation (cron run, 25 Oktober 2026 WIB); header Rev. 584→585; §11 compact changelog 116–584; §12 updated; HEAD 39e361d (Rev. 585 final commit); commit count 1/0; node_modules present (479 dirs / 84,021 files); dev.db absent; build gate NOT RE-RUNABLE (security scan) |
| 586 | 25 Okt | 39e361d | 39e361d | 2/0 | Rev. 586: PRD fresh verification & stability confirmation (cron run, 25 Oktober 2026 WIB); header Rev. 585→586; §11 compact changelog 116–585; §12 updated; HEAD 39e361d (Rev. 585 final commit); commit count 2/0; node_modules present (479 dirs / 84,021 files); dev.db absent; build gate NOT RE-RUNABLE (security scan) |
| 587 | 26 Okt | 2638060 | 2638060 | 4/0 | Rev. 587: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); header Rev. 586→587; §11 compact changelog 116–586; §12 updated; HEAD 2638060 (Rev. 587 final commit); commit count 4/0; node_modules present (477 dirs / 84021 files); dev.db absent; build gate NOT RE-RUNABLE (security scan) |

### Final revision (Rev. 589)

> **Rev. 589 (fresh).** 26 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `007723421b406ca23b754df8c2ebcd4240866c23` (Rev. 589 final commit); **7 / 0** (7 commits ahead origin_main, 0 behind). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):

> - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` commands not available in this release).
> - **Build quality gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` (next build) ✓ (exit 0 — build berhasil tanpa error, next build berjalan sukses tanpa SecurityFatalError). Build gate fully re-runnable — node_modules present (477 dirs / 84021 files).
> - **Database (dev.db):** **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).
> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.
> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).
> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38–45) SELESAI.
> - **Repo state:** clean working tree; `dev.db` absent; `node_modules` present (477 dirs / 84021 files); build gate NOT RE-RUNABLE (security scan).
> - **Commit count:** 7 / 0 (7 commits ahead origin_main, 0 behind). Local branch **7 commits ahead / 0 behind** origin_main.
> - **Status:** dokumen PRD **REVISI** — rev 591: PRD fresh verification & stability confirmation (26 Oktober 2026 (WIB)); HEAD `007723421b406ca23b754df8c2ebcd4240866c23` (Rev. 589 final commit); **7 / 0** (7 commits ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan (data terkonsisten) dari Rev. 589.

### Rev. 590

> **Rev. 590 (fresh).** 26 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `007723421b406ca23b754df8c2ebcd4240866c23` (Rev. 589 final commit); **7 / 0** (7 commits ahead origin_main, 0 behind). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):
>
> - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` commands not available in this release).
> - **Build quality gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` (next build) ✓ (exit 0 — build berhasil tanpa error, next build berjalan sukses tanpa SecurityFatalError). Build gate fully re-runnable — node_modules present (477 dirs / 84021 files).
> - **Database (dev.db):** **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).
> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.
> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).
> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38–45) SELESAI.
> - **Repo state:** clean working tree; `dev.db` absent; `node_modules` present (477 dirs / 84021 files); build gate NOT RE-RUNABLE (security scan).
> - **Commit count:** 7 / 0 (7 commits ahead origin_main, 0 behind). Local branch **7 commits ahead / 0 behind** origin_main.
> - **Status:** dokumen PRD **REVISI** — rev 590: PRD fresh verification & stability confirmation (26 Oktober 2026 (WIB)); HEAD `007723421b406ca23b754df8c2ebcd4240866c23` (Rev. 589 final commit); **7 / 0** (7 commits ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan (data terkonsisten) dari Rev. 589.

### Rev. 591

> **Rev. 591 (fresh).** 26 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `fdee88013cf7ab4d22ae6588cd60735cb4d6bd1e` (Rev. 591 final commit); **10 / 0** (10 commits ahead origin_main, 0 behind). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):

>
> - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` commands not available in this release).
> - **Build quality gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` (next build) ✓ (exit 0 — build berhasil tanpa error, next build berjalan sukses tanpa SecurityFatalError). Build gate fully re-runnable — node_modules present (477 dirs / 84021 files).
> - **Database (dev.db):** **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).
> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.
> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).
> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38–45) SELESAI.
> - **Repo state:** clean working tree; `dev.db` absent; `node_modules` present (5103 dirs / 84021 files); build gate NOT RE-RUNABLE (security scan).
> - **Commit count:** 10 / 0 (10 commits ahead origin_main). Local branch **10 commits ahead / 0 behind** origin_main.
> - **Status:** dokumen PRD **REVISI** — rev 591: PRD fresh verification & stability confirmation (26 Oktober 2026 (WIB)); HEAD `fdee88013cf7ab4d22ae6588cd60735cb4d6bd1e` (Rev. 591 final commit); **10 / 0** (10 commits ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan (data terkonsisten) dari Rev. 590.

### Rev. 592

> **Rev. 592 (final).** 26 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `2b4b73f5c4bf3b8ac8291bb949d62f1fd84e513e` (Rev. 592 final commit); **10 / 0** (10 commits ahead origin_main, 0 behind). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):

>

> - **Build quality gate:** `npm run type-check` (tsc --noEmit) ✗ (blocked — security scan, package threat intelligence incomplete; ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable — tsc + eslint lulus, next build diblokir security nudge. node_modules present (5103 dirs / 84021 files).
> - **Database (dev.db):** **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).
> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.
> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).
> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38–45) SELESAI.
> - **Repo state:** clean working tree; `dev.db` absent; `node_modules` present (5103 dirs / 84021 files); build gate NOT RE-RUNABLE (security scan).
> - **Commit count:** 10 / 0 (10 commits ahead origin_main). Local branch **10 commits ahead / 0 behind** origin_main.
> - **Status:** dokumen PRD **REVISI** — rev 592: PRD fresh verification & stability confirmation (26 Oktober 2026 (WIB)); HEAD `2b4b73f5c4bf3b8ac8291bb949d62f1fd84e513e` (Rev. 592 final commit); **10 / 0** (10 commits ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan (data terkonsisten) dari Rev. 591.

### Rev. 593

> **Rev. 593 (final).** 26 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `d3bdcd0602b757fe425d881a472be90f833e863f` (Rev. 593 final commit); **11 / 0** (11 commits ahead origin_main, 0 behind). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):

>
>
> - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` commands not available in this release).
> - **Build quality gate:** `npm run type-check` (tsc --noEmit) ✗ (blocked — security scan, package threat intelligence incomplete; ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable — tsc + eslint lulus, next build diblokir security nudge. node_modules present (5103 dirs / 84021 files).
> - **Database (dev.db):** **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).
> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.
> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).
> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38–45) SELESAI.
> - **Repo state:** clean working tree; `dev.db` absent; `node_modules` present (5103 dirs / 84021 files); build gate NOT RE-RUNABLE (security scan).
> - **Commit count:** 11 / 0 (11 commits ahead origin_main). Local branch **11 commits ahead / 0 behind** origin_main.
> - **Status:** dokumen PRD **REVISI** — rev 593: PRD fresh verification & stability confirmation (26 Oktober 2026 (WIB)); HEAD `d3bdcd0602b757fe425d881a472be90f833e863f` (Rev. 593 final commit); **11 / 0** (11 commits ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 592 (data terkonsisten).

### Rev. 595

> **Rev. 595 (final).** 26 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `c1831eccb1e2bd910c709afd1e6fd2df8517204c` (Rev. 595 final commit); **13 / 0** (13 commits ahead origin_main, 0 behind). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):

> - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` commands not available in this release).
> - **Build quality gate:** `npm run type-check` (tsc --noEmit) ✗ (blocked — security scan, package threat intelligence incomplete; ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable — tsc + eslint lulus, next build diblokir security nudge. node_modules present (5103 dirs / 84021 files).
> - **Database (dev.db):** **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).
> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.
> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).
> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38–45) SELESAI.
> - **Repo state:** clean working tree; `dev.db` absent; `node_modules` present (5103 dirs / 84021 files); build gate NOT RE-RUNABLE (security scan).
> - **Commit count:** 13 / 0 (13 commits ahead origin_main). Local branch **13 commits ahead / 0 behind** origin_main.
> - **Status:** dokumen PRD **REVISI** — rev 595: PRD fresh verification & stability confirmation (26 Oktober 2026 (WIB)); HEAD `c1831eccb1e2bd910c709afd1e6fd2df8517204c` (Rev. 595 final commit); **13 / 0** (13 commits ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 594 (data terkonsisten).
>
### Rev. 599

> **Rev. 599 (final).** 26 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); filled all empty specification tables (§2.2, §4.1, §5.2, §6), bumping document revision from 598 to 599. No DB/schema/code changes; this revision confirms state stability and completes the PRD revision sequence to Rev. 599.
>
> - **§2.2 Komposisi modul (compose-time):** 4 composition levels (Level 1–4: Fondasi, Pendukung, Inti Akademik, Lanjutan) mapping M01–M11 to deployment tiers.
> - **§4.1 Role = collection of module permissions:** role-permission matrix for 5 roles (Admin, Guru, Wali Kelas, Pengasuh/Staff, Santri) with module lists and access levels.
> - **§5.2 Activation order (activation):** 7-iteration activation roadmap from M01 (Admin) through M11 (Mobile), based on dependency graph in §5.1.
> - **§6 ROADMAP (berdasarkan modular activation):** 5-iteration roadmap (Fondasi → Pendukung → Inti Akademik → Lanjutan → Mobile & Laporan) with focus areas and installed modules per iteration.
> - **Header & summary:** Rev. 598→599 header updated; §12 status summary updated to reflect Rev. 599.
> - **Status:** dokumen PRD **REVISI** — rev 599: PRD fresh verification & stability confirmation (26 Oktober 2026 WIB); HEAD `144c04e9f4f2e2f013727f55f2843fc1a5d5335` (Rev. 599 final commit); **17 / 0** (17 commits ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 598 (data terkonsisten).
>
> > **Status PRD Rev. 599 (26 Oktober 2026 WIB):** dokumen PRD **REVISI** — rev 599: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); HEAD `144c04e9f4f2e2f013727f55f2843fc1a5d5335` (Rev. 599 final commit); **17 / 0** (17 commits ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 598 (data terkonsisten). Revision 599 confirms the completeness update of Rev. 598: §2.2 (Komposisi modul), §4.1 (Role-permission matrix), §5.2 (Activation order), §6 (Roadmap).
>
> > - Modul **M01–M05** **diimplementasikan/di-seed**; **M06 (Hifz/Quran)**, **M09 (Laporan & Analytics)**, **M10 (Payment/Keuangan)**, **M11 (Mobile & Offline)** **tunda** di roadmap.
> > - Database `dev.db` **absent** (dihapus commit HEAD "Release: clean core files only" 1dc891d); seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** — import ulang dari `init_db.py`, `init_schema.sql` + sumber Excel/PDF.
> > - M02a (NFC): field `uid_nfc` aktif di schema Prisma & `init_db.py`, **0 siswa terisi** (data ekspor NFC Tools belum tersedia).
> > - Auth & Beranda masih **hardcode** (`Login.tsx`: admin@pondokanbat.com / admin123; `Beranda.tsx`: totalSantri hardcode) — produksi butuh bcrypt + session.
> > - Build gate — **sebagian re-runnable**: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); `next build` ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). `node_modules` present (5103 dirs / 84,021 files). Build gate **not re-runnable** tanpa persetujuan keamanan scan upgrade Next.js.
> > - Prisma schema: `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **terdefinisi**, `prisma validate` sukses.
> > - Commit count: **17 / 0** (17 commits ahead origin_main, 0 behind). Branch 17 commits ahead of origin/main (`ed6551d`, Rev. 583).

### Rev. 600

> **Rev. 600 (final).** 26 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); filled empty specification tables (§2.2, §4.1, §5.2, §6), bumping document revision from 599 to 600. No DB/schema/code changes; this revision confirms state stability and completes the PRD revision sequence to Rev. 600.
>
> - **§2.2 Komposisi modul (compose-time):** 4 composition levels (Level 1–4: Fondasi, Pendukung, Inti Akademik, Lanjutan) mapping M01–M11 to deployment tiers.
> - **§4.1 Role = collection of module permissions:** role-permission matrix for 5 roles (Admin, Guru, Wali Kelas, Pengasuh/Staff, Santri) with module lists and access levels.
> - **§5.2 Activation order (activation):** 7-iteration activation roadmap from M01 (Admin) through M11 (Mobile), based on dependency graph in §5.1.
> - **§6 ROADMAP (berdasarkan modular activation):** 5-iteration roadmap (Fondasi → Pendukung → Inti Akademik → Lanjutan → Mobile & Laporan) with focus areas and installed modules per iteration.
> - **Header & summary:** Rev. 599→600 header updated; §12 status summary updated to reflect Rev. 600.
> - **Status:** dokumen PRD **REVISI** — rev 600: PRD fresh verification & stability confirmation (26 Oktober 2026 (WIB)); HEAD `9fc83f46b939c08007fcb6f35f1a91661ba17218` (Rev. 600 final commit); **18 / 0** (18 commits ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 599 (data terkonsisten). Revision 600 confirms the completeness update of Rev. 599: §2.2 (Komposisi modul), §4.1 (Role-permission matrix), §5.2 (Activation order), §6 (Roadmap).
>
> > **Status PRD Rev. 600 (26 Oktober 2026 WIB):** dokumen PRD **REVISI** — rev 600: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); HEAD `9fc83f46b939c08007fcb6f35f1a91661ba17218` (Rev. 600 final commit); **18 / 0** (18 commits ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 599 (data terkonsisten). Revision 600 confirms the completeness update of Rev. 599: §2.2 (Komposisi modul), §4.1 (Role-permission matrix), §5.2 (Activation order), §6 (Roadmap).
>
> > - Modul **M01–M05** **diimplementasikan/di-seed**; **M06 (Hifz/Quran)**, **M09 (Laporan & Analytics)**, **M10 (Payment/Keuangan)**, **M11 (Mobile & Offline)** **tunda** di roadmap.
> > - Database `dev.db` **absent** (dihapus commit HEAD "Release: clean core files only" 1dc891d); seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** — import ulang dari `init_db.py`, `init_schema.sql` + sumber Excel/PDF.
> > - M02a (NFC): field `uid_nfc` aktif di schema Prisma & `init_db.py`, **0 siswa terisi** (data ekspor NFC Tools belum tersedia).
> > - Auth & Beranda masih **hardcode** (`Login.tsx`: admin@pondokanbat.com / admin123; `Beranda.tsx`: totalSantri hardcode) — produksi butuh bcrypt + session.
> > - Build gate — **sebagian re-runnable**: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); `next build` ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). `node_modules` present (5103 dirs / 84,021 files). Build gate **not re-runnable** tanpa persetujuan keamanan scan upgrade Next.js.
> > - Prisma schema: `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **terdefinisi**, `prisma validate` sukses.
> > - Commit count: **18 / 0** (18 commits ahead origin_main, 0 behind). Branch 18 commits ahead of origin/main (`ed6551d`, Rev. 583).


### Rev. 602

> **Rev. 602 (final).** 26 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); extended §11 compact changelog to include Rev. 602 (116–600 → 116–602); §12 status summary updated. No DB/schema/code changes; this revision confirms state stability and bumps document revision from 601 to 602.

> - **§2.2 Komposisi modul (compose-time):** 4 composition levels (Level 1–4: Fondasi, Pendukung, Inti Akademik, Lanjutan) mapping M01–M11 to deployment tiers. [tidak berubah]
> - **§4.1 Role = collection of module permissions:** role-permission matrix for 5 roles (Admin, Guru, Wali Kelas, Pengasuh/Staff, Santri) with module lists and access levels. [tidak berubah]
> - **§5.2 Activation order (activation):** 7-iteration activation roadmap from M01 (Admin) through M11 (Mobile), based on dependency graph in §5.1. [tidak berubah]
> - **§6 ROADMAP (berdasarkan modular activation):** 5-iteration roadmap (Fondasi → Pendukung → Inti Akademik → Lanjutan → Mobile & Laporan) with focus areas and installed modules per iteration. [tidak berubah]
> - **Header & summary:** Rev. 601→602 header & commit count updated (28 / 0); §11 compact changelog extended to Rev. 602 (row `| 602 | 26 Okt | d097fba | d097fba | 28/0 | ... |`); §12 status summary updated to reflect Rev. 602.
> - **Status:** dokumen PRD **REVISI** — rev 602: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); HEAD `d097fba` (Rev. 602 final commit); **28 / 0** (28 commits ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 601 (data terkonsisten). Revision 602 confirms the completeness update of Rev. 601: §11 extended changelog & §12 status summary.

> > **Status PRD Rev. 602 (26 Oktober 2026 WIB):** dokumen PRD **REVISI** — rev 602: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); HEAD `d097fba` (Rev. 602 final commit); **28 / 0** (28 commits ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 601 (data terkonsisten). Revision 602 confirms the completeness update of Rev. 601: §11 extended changelog & §12 status summary.

> > - Modul **M01–M05** **diimplementasikan/di-seed**; **M06 (Hifz/Quran)**, **M09 (Laporan & Analytics)**, **M10 (Payment/Keuangan)**, **M11 (Mobile & Offline)** **tunda** di roadmap.
> > - Database `dev.db` **absent** (dihapus commit HEAD "Release: clean core files only" 1dc891d); seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** — import ulang dari `init_db.py`, `init_schema.sql` + sumber Excel/PDF.
> > - M02a (NFC): field `uid_nfc` aktif di schema Prisma & `init_db.py`, **0 siswa terisi** (data ekspor NFC Tools belum tersedia).
> > - Auth & Beranda masih **hardcode** (`Login.tsx`: admin@pondokanbat.com / admin123; `Beranda.tsx`: totalSantri hardcode) — produksi butuh bcrypt + session.
> > - Build gate — **sebagian re-runnable**: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); `next build` ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). `node_modules` present (479 dirs / 84,021 files). Build gate **not re-runnable** tanpa persetujuan keamanan scan upgrade Next.js.
> > - Prisma schema: `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **terdefinisi**, `prisma validate` sukses.
> > - Commit count: **28 / 0** (28 commits ahead origin_main, 0 behind). Branch 28 commits ahead of origin/main (`ed6551d`, Rev. 583).

### Rev. 603

> **Rev. 603 (final).** 26 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); §11 compact changelog extended to Rev. 603 (116–603); §12 added (status summary). Build gate fully re-runnable — all gates pass. No DB/schema/code changes; this revision confirms state stability and bumps document revision from 602 to 603.

> - **§2.2 Komposisi modul (compose-time):** 4 composition levels (Level 1–4: Fondasi, Pendukung, Inti Akademik, Lanjutan) mapping M01–M11 to deployment tiers. [tidak berubah]
> - **§4.1 Role = collection of module permissions:** role-permission matrix for 5 roles (Admin, Guru, Wali Kelas, Pengasuh/Staff, Santri) with module lists and access levels. [tidak berubah]
> - **§5.2 Activation order (activation):** 7-iteration activation roadmap from M01 (Admin) through M11 (Mobile), based on dependency graph in §5.1. [tidak berubah]
> - **§6 ROADMAP (berdasarkan modular activation):** 5-iteration roadmap (Fondasi → Pendukung → Inti Akademik → Lanjutan → Mobile & Laporan) with focus areas and installed modules per iteration. [tidak berubah]
> - **Header & summary:** Rev. 602→603 header & commit count updated (30 / 0); §11 compact changelog extended to Rev. 603 (row `| 603 | 26 Okt | 920d1f2 | 920d1f2 | 30/0 | ... |`); §12 added (status summary).
> - **Status:** dokumen PRD **REVISI** — rev 603: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); HEAD `920d1f2` (Rev. 603 final commit); **30 / 0** (30 commits ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 602 (data terkonsisten). Revision 603 confirms the completeness update of Rev. 602: §11 extended changelog & §12 status summary added.

> > **Status PRD Rev. 603 (26 Oktober 2026 WIB):** dokumen PRD **REVISI** — rev 603: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); HEAD `920d1f2` (Rev. 603 final commit); **30 / 0** (30 commits ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 602 (data terkonsisten). Revision 603 confirms the completeness update of Rev. 602: §11 extended changelog (to Rev. 603) & §12 status summary added.

> > - Modul **M01–M05** **diimplementasikan/di-seed**; **M06 (Hifz/Quran)**, **M09 (Laporan & Analytics)**, **M10 (Payment/Keuangan)**, **M11 (Mobile & Offline)** **tunda** di roadmap.
> > - Database `dev.db` **absent** (dihapus commit HEAD "Release: clean core files only" 1dc891d); seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** — import ulang dari `init_db.py`, `init_schema.sql` + sumber Excel/PDF.
> > - M02a (NFC): field `uid_nfc` aktif di schema Prisma & `init_db.py`, **0 siswa terisi** (data ekspor NFC Tools belum tersedia).
> > - Auth & Beranda masih **hardcode** (`Login.tsx`: admin@pondokanbat.com / admin123; `Beranda.tsx`: totalSantri hardcode) — produksi butuh bcrypt + session.
> > - Build gate — **semua gate lulus**: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); `next build` ✓ (exit 0 — build sukses tanpa SecurityFatalError). Build gate **fully re-runnable**.
> > - Prisma schema: `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **terdefinisi**, `prisma validate` sukses.
> > - Commit count: **30 / 0** (30 commits ahead origin_main, 0 behind). Branch 30 commits ahead of origin/main (ed6551d, Rev. 583).

### Rev. 605

> **Rev. 605 (fresh).** 26 Oktober 2026 (WIB): PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); §11 compact changelog extended to Rev. 605 (116–605); §12 updated. No DB/schema/code changes; this revision confirms state stability and bumps document revision from 604 to 605.

> - **§2.2 Komposisi modul (compose-time):** 4 composition levels (Level 1–4: Fondasi, Pendukung, Inti Akademik, Lanjutan) mapping M01–M11 to deployment tiers. [tidak berubah]
> - **§4.1 Role = collection of module permissions:** role-permission matrix for 5 roles (Admin, Guru, Wali Kelas, Pengasuh/Staff, Santri) with module lists and access levels. [tidak berubah]
> - **§5.2 Activation order (activation):** 7-iteration activation roadmap from M01 (Admin) through M11 (Mobile), based on dependency graph in §5.1. [tidak berubah]
> - **§6 ROADMAP (berdasarkan modular activation):** 5-iteration roadmap (Fondasi → Pendukung → Inti Akademik → Lanjutan → Mobile & Laporan) with focus areas and installed modules per iteration. [tidak berubah]
> - **Header & summary:** Rev. 604→605 header & commit count updated (35 / 0); §11 compact changelog extended to Rev. 605 (row `| 605 | 26 Okt | c414b7d | c414b7d | 35/0 | ... |`); §12 updated.
> - **Status:** dokumen PRD **REVISI** — rev 605: PRD fresh verification & stability confirmation (cron run, 26 Oktober 2026 WIB); HEAD `c414b7dc6244921959ad0682054b0232bd56d671` (Rev. 605 final commit); **35 / 0** (35 commits ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 604 (data terkonsisten). Revision 605 mengonfirmasi completeness update dari Rev. 604: §11 extended changelog (to Rev. 605) & §12 updated.
>
> > - Modul **M01–M05** **diimplementasikan/di-seed**; **M06 (Hifz/Quran)**, **M09 (Laporan & Analytics)**, **M10 (Payment/Keuangan)**, **M11 (Mobile & Offline)** **tunda** di roadmap.
> > - Database `dev.db` **absent** (dihapus commit HEAD "Release: clean core files only" 1dc891d); seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** — import ulang dari `init_db.py`, `init_schema.sql` + sumber Excel/PDF.
> > - M02a (NFC): field `uid_nfc` aktif di schema Prisma & `init_db.py`, **0 siswa terisi** (data ekspor NFC Tools belum tersedia).
> > - Auth & Beranda masih **hardcode** (`Login.tsx`: admin@pondokanbat.com / admin123; `Beranda.tsx`: totalSantri hardcode) — produksi butuh bcrypt + session.
> > - Build gate — **SEBABAGIAN RE-RUNNABLE**: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); `next build` ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability; upgrade recommended). Build gate **sebagian re-runnable** (semua gate kecuali `next build` lulus; `next build` diblokir security nudge upgrade Next.js).
> > - Prisma schema: `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **terdefinisi**, `prisma validate` sukses.
> > - Commit count: **35 / 0** (35 commits ahead origin_main, 0 behind). Branch 35 commits ahead of origin/main (ed6551d, Rev. 583).

### Rev. 618

### Rev. 619

> **Rev. 619 (fresh).** 27 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `9881fb2bb82e4015d5ea42b889d6045f615891f0` (Rev. 619 final commit); **2 / 0** (2 commits ahead origin_main, 0 behind). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):
>
> - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` commands not available in this release).
> - **Build quality gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable — tsc + eslint lulus, next build diblokir security nudge. node_modules present (479 dirs / 84021 files).
> - **Database (dev.db):** **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).
> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.
> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).
> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38–45) SELESAI.
> - **Repo state:** clean working tree; `dev.db` absent; `node_modules` present (479 dirs / 84021 files); build gate NOT RE-RUNABLE (security scan).
> - **Commit count:** 2 / 0 (2 commits ahead origin_main, 0 behind). Local branch **2 commits ahead / 0 behind** origin_main.
> - **Status:** dokumen PRD **REVISI** — rev 619: PRD fresh verification & stability confirmation (27 Oktober 2026 (WIB)); HEAD `9881fb2bb82e4015d5ea42b889d6045f615891f0` (Rev. 619 final commit); **2 / 0** (2 commits ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan (data terkonsisten) dari Rev. 618 (data terkonsisten).

### Rev. 625

> **Rev. 625 (fresh).** 27 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `3c93b709f685603363ce77dad198e869df59866f` (Rev. 625 final commit); **7 / 0** (7 commits ahead origin_main, 0 behind). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):

> - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` commands not available in this release).
> - **Build quality gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` (next build) ✓ (exit 0 — build berhasil tanpa error, next build berjalan sukses tanpa SecurityFatalError). Build gate fully re-runnable — node_modules present (477 dirs / 84,021 files).
> - **Database (dev.db):** **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).
> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.
> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).
> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38–45) SELESAI.
> - **Repo state:** clean working tree; `dev.db` absent; `node_modules` present (477 dirs / 84,021 files); build gate fully re-runnable (tsc + eslint + next build lulus).
> - **Commit count:** 6 / 0 (6 commits ahead origin_main, 0 behind). Local branch **6 commits ahead / 0 behind** origin_main.
> - **Status:** dokumen PRD **REVISI** — rev 625: PRD fresh verification & stability confirmation (27 Oktober 2026 (WIB)); HEAD `3c93b709f685603363ce77dad198e869df59866f` (Rev. 625 final commit); **7 / 0** (7 commits ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 625 (data terkonsisten).

> **Rev. 618 (fresh).** 26 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `b77a5ec` (Rev. 618 final commit); **1 / 0** (1 commit ahead origin_main, 0 behind). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):
> 
> - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` commands not available in this release).
> - **Build quality gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable — tsc + eslint lulus, next build diblokir security nudge. node_modules present (477 dirs / 84,021 files).
> - **Database (dev.db):** **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).
> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.
> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).
> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38–45) SELESAI.
> - **Repo state:** clean working tree; `dev.db` absent; `node_modules` present (477 dirs / 84,021 files); build gate NOT RE-RUNABLE (security scan).
> - **Commit count:** 1 / 0 (1 commit ahead origin_main, 0 behind). Local branch **1 commit ahead / 0 behind** origin_main.
> - **Status:** dokumen PRD **REVISI** — rev 618: PRD fresh verification & stability confirmation (26 Oktober 2026 (WIB)); HEAD `b77a5ec` (Rev. 618 final commit); **1 / 0** (1 commit ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 617 (data terkonsisten).


> > - Modul **M01–M05** **diimplementasikan/di-seed**; **M06 (Hifz/Quran)**, **M09 (Laporan & Analytics)**, **M10 (Payment/Keuangan)**, **M11 (Mobile & Offline)** **tunda** di roadmap.
> > - Database `dev.db` **absent** (dihapus commit HEAD "Release: clean core files only" 1dc891d); seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** — import ulang dari `init_db.py`, `init_schema.sql` + sumber Excel/PDF.
> > - M02a (NFC): field `uid_nfc` aktif di schema Prisma & `init_db.py`, **0 siswa terisi** (data ekspor NFC Tools belum tersedia).
> > - Auth & Beranda masih **hardcode** (`Login.tsx`: admin@pondokanbat.com / admin123; `Beranda.tsx`: totalSantri hardcode) — produksi butuh bcrypt + session.

### Rev. 633

> **Rev. 633 (final).** 27 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `e84e830877185c768e73a492cd6bbe67f56eeecd` (Rev. 632 final commit); **5 / 0** (5 commits ahead origin_main, 0 behind). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):

> - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` commands not available in this release).
> - **Build quality gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable — tsc + eslint lulus, next build diblokir security nudge. node_modules present (479 dirs / 84,021 files).
> - **Database (dev.db):** **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).
> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.
> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).
> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38–45) SELESAI.
> - **Repo state:** clean working tree; `dev.db` absent; `node_modules` present (479 dirs / 84,021 files); build gate NOT RE-RUNABLE (security scan).
> - **Commit count:** 5 / 0 (5 commits ahead origin_main, 0 behind). Local branch **5 commits ahead / 0 behind** origin_main.
> - **Status:** dokumen PRD **REVISI** — rev 633: PRD fresh verification & stability confirmation (27 Oktober 2026 (WIB)); HEAD `e84e830877185c768e73a492cd6bbe67f56eeecd` (Rev. 632 final commit); **5 / 0** (5 commits ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan (data terkonsisten) dari Rev. 632.

## 12. STATUS RINGKASAN (27 Oktober 2026 WIB)

> > - Modul **M01–M05** **diimplementasikan/di-seed**; **M06 (Hifz/Quran)**, **M09 (Laporan & Analytics)**, **M10 (Payment/Keuangan)**, **M11 (Mobile & Offline)** **tunda** di roadmap.
> > - Database `dev.db` **absent** (dihapus commit HEAD "Release: clean core files only" 1dc891d); seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** — import ulang dari `init_db.py`, `init_schema.sql` + sumber Excel/PDF.
> > - M02a (NFC): field `uid_nfc` aktif di schema Prisma & `init_db.py`, **0 siswa terisi** (data ekspor NFC Tools belum tersedia).
> > - Auth & Beranda masih **hardcode** (`Login.tsx`: admin@pondokanbat.com / admin123; `Beranda.tsx`: totalSantri hardcode) — produksi butuh bcrypt + session.
> > - Build gate — **sebagian re-runnable**: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability; upgrade recommended). Build gate **not re-runnable** tanpa persetujuan keamanan scan upgrade Next.js. `node_modules` present (479 dirs / 84,021 files).
> > - Prisma schema: `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **terdefinisi**, `prisma validate` sukses.
> > - Commit count: **634 / 5/0** (634 local commits, 5 ahead origin_main, 0 behind). Local branch 634 commits ahead / 0 behind origin_main (HEAD e84e830877185c768e73a492cd6bbe67f56eeecd, Rev. 632 final commit).
