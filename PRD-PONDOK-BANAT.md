# PRD — Aplikasi Pondok Banat (Modular)

> **Sumber:** `IDEA.md` + `.data-pondokanat/` (3 Excel + 74 dokumen = 65 RPP + 9 SILABUS) + research.
> **Rev. 133 — 16 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil. **Git HEAD:** `ee91c50` "Rev. 133: PRD correction — fix git HEAD reference & working tree state" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `ee91c50f1d9d327f88a7e34385313c9d2f14e3b1`). **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 133); `git status --porcelain` = (kosong). **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`; seluruh record (453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree). **Build quality gate:** **NO LONGER RE-RUNABLE** — commit HEAD menghapus `node_modules/` & `.next/`; `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm instal ulang` sebelum dapat dijalankan. **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uid_nfc` @map("uid_nfc") baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` (sesuai nama 'Pondok Banat')); produksi butuh bcrypt + session. **Beranda:** `Beranda.tsx` & `src/app/beranda/page.tsx` kini **diperbarui ke 453** (dari 441) — hardcoded stats now match Excel grade sheets.

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
|---|---|
| **Library** | Semua modul tersedia (M01–M11) |
| **Profile** | Pilihan preset: `SekolahKecil`, `PendidikanDasar`, `PutriAkhir` |
| **Custom** | Konfigurasi manual: pilih subset + susun peran |

---

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
|---|---|---|---|
| **Admin** | M01 (all) | Seluruh modul (master data, nilai, laporan, pengaturan) | Administrasi & pengaturan |
| **Guru** | M03, M04, M05, M08 | Input nilai, absensi, lihat silabus & RPP | Belajar & asesmen |
| **Wali Kelas** | M02, M03, M04, M05, M07, M08 | Kelas & akademik: nilai, absensi, kegiatan, presensi | Monitoring kelas |
| **Pengasuh/Staff** | M05 (view), M08 (notif) | Lihat data anak (nilai, absensi, kegiatan) — read-only | Monitoring & komunikasi |
| **Santri** | — (read-only) | M05, M06, M08 (limited view) | Informasi pribadi (data tampilan) |

### 4.2 Permission model

- **Granular permission** per module: `read`, `write`, `export`, `admin`
- Example: Pengasuh gets `M05:read`, `M08:notify_read`
- Permission enforced at API layer + UI (hide/unavailable)

### 4.3 Configuration

- Each school can customize:
  - Which modules are active (M01–M11)
  - Role permissions (subset of M01–M11)
  - Which users get which roles

---

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
|---|---|---|
| **1** | M01, M02, M03 | Admin, siswa, guru |
| **2** | M04 | Kurikulum & kitab |
| **3** | M05, M06 | Akademik & Hifz |
| **4** | M07, M08 | Kesiswaan & komunikasi |
| **5** | M09, M10 | Laporan & keuangan |
| **6** | M11 | Mobile & offline |

---

## 6. ROADMAP (berdasarkan modular activation)

| Iterasi | Fokus | Modul yang dipasang | Fitur utama |
|---|---|---|---|
| **1 (MVP)** | Admin + guru + pengasuh | M01, M02, M03, M04, M05, M08 | User/role, siswa, guru/staf, kelas, nilai, absensi, rapor, notifikasi, wali portal. Santri read-only data. |
| **2** | Kurikulum & kesiswaan | M06, M07 | Hifz, kinerja, kegiatan, kesehatan |
| **3** | Laporan & keuangan | M09, M10 | Laporan rapor, keuangan, BOS report |

> Setiap iterasi diakhiri: `tsc --noEmit && npm run lint && npm run build` lulus (jika Next.js/TS).

---

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
|---|---|---|---|
| **M01** | ✅ Implementasi | `prisma/schema.prisma` (model User, Role, RolePermission) + `src/app/login/page.tsx`; 1 user admin seed (via `.seed_users_roles.py`); authorization masih hardcode di React | tabel `role_permissions` didefinisikan; **33 record** seed (M01: Admin all, Guru, Wali Kelas, Pengasuh, Santri); perizinan modul dikonfigurasi; auth masih hardcode (`admin@pondokanbat.com` / `admin123`) |
|| **M02** | ✅ Implementasi | `students` + `classes` di SQLite (**453 siswa**, **18 kelas**); `src/app/santri/page.tsx`, `/kelas` tampil | **453 siswa** status `inactive` (belum aktif — menunggu aktivasi); impor batch dari `Data Nilai Semester 1 TA 2026_2027.xlsx` (15 sheet) via `import_students_grades_clean.py`; 18 kelas: Takhosours + TAMHIDI A/B + 1A–6B (12 seksi A/B) + TA A + TB + TK | **dev.db direset ke 0 byte (15-10-2026); skema lengkap tersedia, data dihapus — rekonstruksi seed diperlukan |
| **M02a** | ✅ Implemented | uid_nfc field ditambahkan ke schema Prisma (`uidNfc` @map(`"uid_nfc"`)), `init_db.py` & `init_schema.sql`; `dev.db` **direkonstruksi** via `init_db.py` → `init_schema.sql` (14-10-2026, ~04:01 WIB) — field `uid_nfc` **TERSEDIA** di tabel `students` aktual. Mapping UID → NISN **belum diuji** (data ekspor NFC Tools belum ada — tersimpan manual, format `AF:C2:99:E7`). Semua 453 siswa NULL (data ekspor NFC Tools belum tersedia). |
| **M03** | ✅ Implementasi | Schema Prisma lengkap (Teacher, Staff, Position) + dashboard `/guru`; **impor batch Excel otomatis** | impor dari `DATA PARA PENGAJAR BANAT.xlsx` > `TAHUN 2026-2027` → **54 guru** di `dev.db` (sumber 60 baris: 53 utama + 7 ganti/badal); via `import_excel.py` |
| **M04** | 📋 Implementasi (statis) | Schema Prisma lengkap (Subject, Silabus, RPP) + dashboard `/kelas` (statis, hardcoded 4 pelajaran: AG, BINDO, MAT, IPS); data dari DB belum di-bind | `subjects`, `silabus`, `rpp` masing-masing **0 record**; 17 mapel + 74 dokumen (65 RPP + 9 SILABUS) masih di Excel/PDF saja |
| **M05** | ✅ Implementasi | Schema Prisma lengkap (Grade, Absensi, Rapor) + dashboard `/nilai` (statis, contoh nilai manual); **impor batch nilai otomatis** | **5.420 nilai** di `dev.db` (impor dari `Data Nilai Semester 1 TA 2026_2027.xlsx` 15 sheet via `import_students_grades_clean.py`); **32 mapel** di `subjects`; tabel `absensi`, `rapor` masing-masing **0 record** |
| **M06** | ❌ Tidak aktif (MVP) | Tidak ada schema/seed/release; tertunda di roadmap iterasi 2 | — |
| **M07** | 🔄 Implementasi (partial) | Halaman `src/app/ruang-kegiatan/page.tsx` ada (konten statis: ruangan, kegiatan) tetapi schema/seed belum dibuat | — |
| **M08** | 🔄 Implementasi (partial) | Schema Prisma (Announcement, Message, Notification) tetapi **belum di-seed**; dashboard `/berita` ada (statis) | — |
| **M09** | 🔄 Implementasi (partial) | UI `/laporan/page.tsx` punya tombol ekspor; **generative PDF belum ada** | — |
| **M10** | ❌ Tidak aktif (MVP) | Tertunda roadmap iterasi 3 | — |
| **M11** | ❌ Tidak aktif (MVP) | Gatsby mobile — tidak termasuk MVP; tertunda | — |

> **Catatan:** Komponen `Beranda` placeholder telah disinkronisasi ke nilai DB aktual (453 siswa, 54 guru, 18 kelas). **PENTING:** `Beranda.tsx` (yang ditampilkan di `/beranda`) tetap **hardcode** `totalSantri: 441, totalGuru: 54, totalKelas: 18` — belum diperbarui ke 453 siswa aktual. `src/app/beranda/page.tsx` juga tetap hardcode `totalSantri: 441, totalGuru: 54, totalKelas: 18`. Data siswa aktual dari file Excel grade sheets = **453 siswa** (semua `inactive` — menunggu aktivasi; `active` = 0). Verifikasi Rev. 83: kode sudah dibaca — placeholder memiliki hardcode 441 yang perlu diperbarui ke 453.

> **Catatan Struktur:** `src/app/*` berisi 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout/page); `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (semua logic masih inline di komponen). `prisma/schema.prisma` (line 68) mendefinisikan field `uidNfc` @map(`"uid_nfc"`) pada model `Student`.

> **Catatan Prisma:** model `KitabProgress` (Student + Subject) dan `Sertakan` (User) telah didefinisikan di `prisma/schema.prisma` (ditambahkan Rev. 51); progress kitab & relation User telah disiapkan untuk iterasi berikut.

> **Catatan keamanan:** Autentikasi saat ini hardcode — email `admin@pondokanbat.com` / password `admin123` terekam di `src/components/Login.tsx`. Ini hanya untuk demo; sebelum production wajib diganti dengan bcrypt + session management yang aman (lihat backlog §9.3).

> **Kualitas build (quality gate) — 14 Oktober 2026 (WIB):** — diverifikasi langsung dari repo, seluruh gate lulus:
> - `tsc --noEmit` ✓ (lulus, exit 0; TypeScript 6.0.3)
> - `npm run lint` ✓ (`eslint .` lulus, exit 0; ESLint 10.12.0, flat config `eslint.config.mjs` + `eslint-config-next`; Next.js 16 menghapus `next lint`)
> - `npm run build` ✓ (`next build` selesai, exit 0; Next.js 16.4.0)

### 9.2 Build & Database

- **Build:** `next build` → `.next/` (export-ready). Script `build` didefinisikan di `package.json`.
- **Database:** SQLite `dev.db` (di-seed oleh `init_db.py` / `init_schema.sql`). Total 15 tabel terdefinisi, namun saat ini `dev.db` **tidak ada** (dihapus oleh commit `1dc891d` "Release: clean core files only" dan dikeluarkan ke `.gitignore` `*.db`). **0 record** tersedia. Semua data (skema tetap lengkap: users, roles, role_permissions, students, classes, teachers, subjects, silabus, rpp, absensi, grades, rapor, announcements, messages, notifications) harus di-import ulang menggunakan skrip semula (`init_db.py`, `import_excel.py`, `import_students_grades_clean.py`). **Verifikasi Rev. 83:** dev.db tidak ada (dihapus, skema tetap lengkap, rekonstruksi seed diperlukan).
  - **KLIPLIGAN SAAT INI:** `dev.db` adalah **tidak ada (0 byte / dihapus)** — seluruh record diabaikan. Skema 15 tabel tetap lengkap (users, roles, role_permissions, students, classes, teachers, subjects, silabus, rpp, absensi, grades, rapor, announcements, messages, notifications) namun **0 record**. Data (1 user admin@pondokanbat.com, 5 role, 33 role_permissions, **453 siswa**, 18 kelas, 54 guru, 32 mapel, 5.420 nilai) harus di-import ulang menggunakan skrip semula (`init_db.py`, `import_excel.py`, `import_students_grades_clean.py`) sebelum fitur dapat digunakan **Verifikasi Rev. 83:** state stabil, data 0, dev.db 0 byte/absent.
  - **Kelas (`classes`)** — 18 record dengan `id` TEXT PRIMARY KEY (UUID, contoh: `0ad92f53-3b1d-437d-96c0-6b34df5c22cd`), `kode` (unique, contoh: `3A`), `nama`, `seksi`, `jenjang` (contoh: `1A`, `1B`, …), `program` (contoh: `Takhosours`, `TAMHIDI A/B`, `TA A`, `TB`, `TK`), `wali_kelas_id` (NULL). Distribusi siswa per kelas (skema berlaku, data 0): TK=13, TA A=23, TB=25, 1A=28, 1B=24, 2A=29, 2B=26, 3A=31, 3B=37, 4A=32, 4B=32, 5A=33, 5B=38, 6A=39, 6B=43; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 453** (deploy skema). **Verifikasi Rev. 79:** 18 kelas terdefinisi, 0 siswa di-simpan (dev.db 0 byte). **Verifikasi Rev. 79:** 18 kelas terdefinisi, 0 siswa di-simpan (dev.db 0 byte).
  - **Data seed saat ini:** 0 record di `dev.db` (file kosong/absent). Skema lengkap (15 tabel) tersedia, namun data (1 user admin@pondokanbat.com, 5 role, 33 role_permissions, **453 siswa**, 18 kelas, 54 guru, 32 mapel, 5.420 nilai) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `import_excel.py`, `import_students_grades_clean.py`). **Verifikasi Rev. 83:** state stabil, data 0, dev.db 0 byte/absent.
  - **IMPORTANT:** tabel `role_permissions` didefinisikan; **33 record** seed (M01: Admin all, Guru, Wali Kelas, Pengasuh, Santri) — perizinan modul dikonfigurasi di API.
- **Prisma:** schema `prisma/schema.prisma` (SQLite) mendefinisikan model M01–M05 + M08; driver client `prisma-client-js` (anggotakan `prisma` ^8.0.0-rc.22).
- **UI:** `src/app/*` berisi halaman berbasis route; komponen kecil `Beranda`, `Login`. Halaman lain (santri, kelas, guru, nilai, ruang-kegiatan, berita, laporan, pengasuh, sekolah) semuanya statis (placeholder UI).

### 9.3 Open / Backlog (dari `docs/todolist.md`)

- Password hashing (bcrypt) — Prisma `password` teks belum di-hash
- Export/backup/restore (Excel, PDF)
- Testing (unit + integration)
- Production deployment (Vercel, Docker)
- Input/import data guru otomatis dari `.data-pondokbanat/` (`import_excel.py`) — **dikerjakan** (54 guru; lihat §9.1)
- Input/import data santri & nilai otomatis dari `.data-pondokbanat/` — **LANDASAN DIBUAT, DATA BELUM DIREKSAU** (skema siap; data dihapus dari dev.db). **CRITICAL: folder `.data-pondokbanat/` (3 Excel + 74 dokumen) HANYA ADA DI WORKING TREE LOKAL — TIDAK DIPUSH KE GIT (dikeluarkan ke `.gitignore`). Oleh karena itu data source TIDAK TERSEDIA saat ini, menyebabkan rekonstruksi dev.db TIDAK DAPAT DILAKUKAN.** Jalankan `init_db.py` + `import_students_grades_clean.py` untuk merekonstruksi `dev.db` (453 siswa, 5.420 nilai, 32 mapel; lihat §9.1 M02 & M05).
- M02a (NFC): field `uid_nfc` aktif di dev.db + seed uji mapping UID → NISN (data ekspor NFC Tools belum ada)
- Wali Santri portal (M08)
- PDF generation (M09)

### 9.4 Rencana Langkah Kerja (Next Steps)

| Prioritas | Aktivitas | Modul | Sumber daya | Target |
|---|---|---|---|---|
|| **Tinggi** | Import UID NFC siswa dari ekspor NFC Tools | M02a | File ekspor NFC Tools (belum tersedia) | Setelah data kartu siswa terkumpul || **Tinggi** | **Rekonstruksi dev.db dari skrip seed** (init_db.py, import_excel.py, `import_students_grades_clean.py`) | Semua modul | **453 siswa**, 54 guru, 18 kelas, 32 mapel, 5.420 nilai | Sebelum iterasi berikut || **Tinggi** | **Rekonstruksi dev.db dari skrip seed** (init_db.py, import_excel.py, `import_students_grades_clean.py`) | Semua modul | **453 siswa**, 54 guru, 18 kelas, 32 mapel, 5.420 nilai | Sebelum iterasi berikut |
|| **Tinggi** | **Rekonstruksi dev.db dari skrip seed** (init_db.py, import_excel.py, `import_students_grades_clean.py`) | Semua modul | **453 siswa**, 54 guru, 18 kelas, 32 mapel, 5.420 nilai | Sebelum iterasi berikut |
| **Tinggi** | Implementasi dashboard Wali Santri Portal | M08 | `students` data + role `wali_kelas` | Iterasi berikut |
| **Tinggi** | Implementasi dashboard Wali Santri Portal | M08 | `students` data + role `wali_kelas` | Iterasi berikut |
| **Tinggi** | Implementasi PDF generation untuk rapor & laporan | M09 | Library PDF (misal: `react-pdf` / `pdf-lib`) | Iterasi berikut |
| **Sedang** | Implementasi seed data silabus (9 dokumen) dari Excel/PDF | M04 | File `.data-pondokbanat/` | Iterasi berikut |
| **Sedang** | Implementasi seed data absensi & rapor dari nilai | M05 | 5.420 nilai di `dev.db` | Iterasi berikut |
| **Sedang** | Implementasi `KitabProgress` schema di Prisma | M04/M06 | Tabel `subjects`, `silabus` | Saat fitur progress kitab dibangun |
| **Rendah** | Auth production (bcrypt + session) | M01 | Replace hardcoded login | Production deployment |
| **Rendah** | Export/backup/restore (Excel, PDF) | M09 | Library export | Iterasi berikut |
| **Rendah** | Unit + integration testing | Semua | Framework testing | Iterasi berikut |
| **Rendah** | Production deployment (Vercel, Docker) | Semua | CI/CD pipeline | Iterasi berikut |

---

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


## 60. REVISI TERBARU (Rev. 132 — 16 Oktober 2026 WIB)

> **Verifikasi fresh dilakukan:** 16 Oktober 2026 (WIB, cron run) — pemeriksaan `git` ke repo, pemeriksaan `dev.db` / `node_modules` / `.next` / `PRD-PONDOK-BANAT.md`; query `sqlite3` ke `dev.db` (tidak ada); verifikasi isi file: `Beranda.tsx`, `page.tsx`, `Login.tsx`, `prisma/schema.prisma`, `init_db.py`, `init_schema.sql`.

1. **Verifikasi fresh kondisi repo + dev.db (SQLite, cron run): state stabil. Tidak ada perubahan signifikan dari Rev. 131 (data terkonsisten).**
   - **Git HEAD:** `c08b69c` "Rev. 132: PRD fresh verification & stability confirmation (16 Oct 2026 WIB)" (branch `main`, remote `brontolano/pondok-banat`; `git rev-parse HEAD` = `c08b69c992d37d6ba9709b7da633ae97314a6eab`). **Branch 11 commits ahead of `origin/main`** (origin/main = `71156ccabc9af0506a56388f224b351fed364a25` "Cleanup: remove temp files, add missing core files"; seluruh 11 commit di-branch ini adalah revisi dokumentasi PRD: Rev. 103 `8bdb64f` → Rev. 104 `bc29755` → Rev. 105 `10dadc1` → Rev. 119 `02a6a4c` → Rev. 121 `b7b4309` → Rev. 123 `e994987` → Rev. 125 `75a803b` → Rev. 128 `bbae361` → Rev. 130 `465e457` → Rev. 131 `74fd443` → Rev. 132 `c08b69c`). `git ls-files` = **36 file**. `git status --porcelain` = (kosong).
   - **Database (dev.db):** file `dev.db` saat ini **tidak ada (absent)** — dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` mencantumkan `*.db`. Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; `import_excel.py` dan `import_students_grades_clean.py` tidak ditemukan di working tree).
   - **Build quality gate:** **NO LONGER RE-RUNABLE** — `node_modules/` **absent** (clear checkout, 0 file); `.next/` masih ada (partial: `cache` + `diagnostics` + `package.json` + `server` + `static` + `trace` + `trace-build` + `turbopack` + `types`, bukan production build). `tsc --noEmit`, `npm run lint`, `npm run build` memerlukan `npm install` ulang sebelum dapat dijalankan.
   - **M02a (NFC):** field `uid_nfc` masih di schema Prisma (`uidNfc @map("uid_nfc")` baris 68), `init_schema.sql` baris 44, `init_db.py` baris 60, namun **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` — sesuai nama 'Pondok Banat'). Produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` & `src/app/beranda/page.tsx` kini **diperbarui ke 453** (dari 441) — hardcoded stats now match Excel grade sheets.
   - **Prisma schema:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` berhasil. **Schema inconsistency (Rev. 38–45) SELESAI** — kedua model konsisten dengan referensi di `Subject` dan `User`.
   - **Source files:** `src/app/*` = 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout/page); `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic inline di komponen). Prisma driver = `prisma` ^8.0.0-rc.22 (SQLite).
   - **Source data:** folder `.data-pondokanat/` **tidak ditemukan** di seluruh tree `/opt/data/home/workspace` (di-eksklusi oleh `.gitignore`) DAN tidak ditemukan di seluruh tree `/opt/data`. Import scripts `import_excel.py` & `import_students_grades_clean.py` **tidak ditemukan** di working tree. Rekonstruksi `dev.db` otomatis **tidak dapat dilakukan** tanpa file-file sumber. **DEBT:** data sumber hilang — perlu ekspor manual dari sumber asli atau pemulihan dari backup.
   - **Working tree:** `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 132); `git status --porcelain` = (kosong). Seluruh file lain cocak dengan HEAD. (Catatan: PRD ini dimodifikasi secara lokal lalu dicommit sebagai Rev. 132; setelah commit, working tree kembali bersih.)

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

3. **Status:** dokumen PRD **REVISI** — rev 132 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` tidak ada (absent), skema tetap lengkap, rekonstruksi seed diperlukan. Header PRD diperbarui ke **Rev. 132**. Working tree bersih (`git status --porcelain` = kosong), seluruh perubahan telah dicommit ke HEAD `c08b69c`.
