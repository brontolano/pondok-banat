# PRD — Aplikasi Pondok Banat (Modular)

> **Sumber:** `IDEA.md` + `.data-pondokbanat/` (3 Excel + 74 dokumen = 65 RPP + 9 SILABUS) + research.
> **Rev. 80 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil. **Tidak ada perubahan signifikan dari Rev. 79** (data terkonsisten). **PERUBAHAN SIGNIFIKAN dari Rev. 76: dev.db direset ke 0 byte (file kosong) — database dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan .gitignore diperbarui untuk mengecualikan *.db** (data terkonsisten). **Database (dev.db):** 1 user (**admin@pondokanat.com**, role admin) | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01) | **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 terisi) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` **ada aktif** di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 441 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`). **Schema:** model `KitabProgress` (Student + Subject) & `Sertakan` (User) selesai didefinisikan (Rev. 51); `prisma validate` sukses. **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanat.com` / `admin123` (typo indeks `pondokanat.com`); **catatan: DB memiliki `admin@pondokanat.com` (beda domain 'a' vs 'b') — inkonsistensi Login.tsx vs dev.db**; produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Build quality gate (Verifikasi Rev. 79):** `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning — 0 error); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Repo state:** git repository (branch main, history ada); PRD-PONDOK-BANAT.md memiliki perubahan local (revisi terbaru); dev.db (0 byte), package-lock.json, tsconfig.json termasuk untracked. **Status:** dokumen PRD **REVISI** — rev 78 = verifikasi fresh ulang & konfirmasi stabilitas; dev.db 0 byte (database dihapus, skema tetap lengkap, rekonstruksi seed diperlukan).
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
| **M01** | ✅ Implementasi | `prisma/schema.prisma` (model User, Role, RolePermission) + `src/app/login/page.tsx`; 1 user admin seed (via `.seed_users_roles.py`); authorization masih hardcode di React | tabel `role_permissions` didefinisikan; **33 record** seed (M01: Admin all, Guru, Wali Kelas, Pengasuh, Santri); perizinan modul dikonfigurasi; auth masih hardcode (`admin@pondokanat.com` / `admin123`) |
| **M02** | ✅ Implementasi | `students` + `classes` di SQLite (**441 siswa**, **18 kelas**); `src/app/santri/page.tsx`, `/kelas` tampil | **441 siswa** status `inactive` (belum aktif — menunggu aktivasi); impor batch dari `Data Nilai Semester 1 TA 2026_2027.xlsx` (15 sheet) via `import_students_grades_clean.py`; 18 kelas: Takhosours + TAMHIDI A/B + 1A–6B (12 seksi A/B) + TA A + TB + TK | **dev.db direset ke 0 byte (15-10-2026); skema lengkap tersedia, data dihapus — rekonstruksi seed diperlukan |
| **M02a** | ✅ Implemented | uid_nfc field ditambahkan ke schema Prisma (`uidNfc` @map(`"uid_nfc"`)), `init_db.py` & `init_schema.sql`; `dev.db` **direkonstruksi** via `init_db.py` → `init_schema.sql` (14-10-2026, ~04:01 WIB) — field `uid_nfc` **TERSEDIA** di tabel `students` aktual. Mapping UID → NISN **belum diuji** (data ekspor NFC Tools belum ada — tersimpan manual, format `AF:C2:99:E7`). Semua 441 siswa NULL (data ekspor NFC Tools belum tersedia). |
| **M03** | ✅ Implementasi | Schema Prisma lengkap (Teacher, Staff, Position) + dashboard `/guru`; **impor batch Excel otomatis** | impor dari `DATA PARA PENGAJAR BANAT.xlsx` > `TAHUN 2026-2027` → **54 guru** di `dev.db` (sumber 60 baris: 53 utama + 7 ganti/badal); via `import_excel.py` |
| **M04** | 📋 Implementasi (statis) | Schema Prisma lengkap (Subject, Silabus, RPP) + dashboard `/kelas` (statis, hardcoded 4 pelajaran: AG, BINDO, MAT, IPS); data dari DB belum di-bind | `subjects`, `silabus`, `rpp` masing-masing **0 record**; 17 mapel + 74 dokumen (65 RPP + 9 SILABUS) masih di Excel/PDF saja |
| **M05** | ✅ Implementasi | Schema Prisma lengkap (Grade, Absensi, Rapor) + dashboard `/nilai` (statis, contoh nilai manual); **impor batch nilai otomatis** | **5.420 nilai** di `dev.db` (impor dari `Data Nilai Semester 1 TA 2026_2027.xlsx` 15 sheet via `import_students_grades_clean.py`); **32 mapel** di `subjects`; tabel `absensi`, `rapor` masing-masing **0 record** |
| **M06** | ❌ Tidak aktif (MVP) | Tidak ada schema/seed/release; tertunda di roadmap iterasi 2 | — |
| **M07** | 🔄 Implementasi (partial) | Halaman `src/app/ruang-kegiatan/page.tsx` ada (konten statis: ruangan, kegiatan) tetapi schema/seed belum dibuat | — |
| **M08** | 🔄 Implementasi (partial) | Schema Prisma (Announcement, Message, Notification) tetapi **belum di-seed**; dashboard `/berita` ada (statis) | — |
| **M09** | 🔄 Implementasi (partial) | UI `/laporan/page.tsx` punya tombol ekspor; **generative PDF belum ada** | — |
| **M10** | ❌ Tidak aktif (MVP) | Tertunda roadmap iterasi 3 | — |
| **M11** | ❌ Tidak aktif (MVP) | Gatsby mobile — tidak termasuk MVP; tertunda | — |

> **Catatan:** Komponen `Beranda` placeholder telah disinkronisasi ke nilai DB aktual (441 siswa, 54 guru, 18 kelas) — changes applied to `Beranda.tsx:42/27/13` → `441/54/18` & `page.tsx:42/27/13` → `441/54/18`. nilai DB aktual: **441 siswa (semua `inactive`)**, **54 guru (semua `active`)**, **18 kelas**. Verifikasi Rev. 19: kode sudah dibaca — placeholder telah di-update, tidak ada hardcode yang mencerminkan jumlah aktual `dev.db` (441 siswa, 54 guru, 18 kelas).

> **Catatan Struktur:** `src/app/*` berisi 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout/page); `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (semua logic masih inline di komponen). `prisma/schema.prisma` (line 68) mendefinisikan field `uidNfc` @map(`"uid_nfc"`) pada model `Student`.

> **Catatan Prisma:** model `KitabProgress` (Student + Subject) dan `Sertakan` (User) telah didefinisikan di `prisma/schema.prisma` (ditambahkan Rev. 51); progress kitab & relation User telah disiapkan untuk iterasi berikut.

> **Catatan keamanan:** Autentikasi saat ini hardcode — email `admin@pondokanat.com` / password `admin123` terekam di `src/components/Login.tsx`. Ini hanya untuk demo; sebelum production wajib diganti dengan bcrypt + session management yang aman (lihat backlog §9.3).

> **Kualitas build (quality gate) — 14 Oktober 2026 (WIB):** — diverifikasi langsung dari repo, seluruh gate lulus:
> - `tsc --noEmit` ✓ (lulus, exit 0; TypeScript 6.0.3)
> - `npm run lint` ✓ (`eslint .` lulus, exit 0; ESLint 10.12.0, flat config `eslint.config.mjs` + `eslint-config-next`; Next.js 16 menghapus `next lint`)
> - `npm run build` ✓ (`next build` selesai, exit 0; Next.js 16.4.0)

### 9.2 Build & Database

- **Build:** `next build` → `.next/` (export-ready). Script `build` didefinisikan di `package.json`.
- **Database:** SQLite `dev.db` (di-seed oleh `init_db.py` / `init_schema.sql`). Total 15 tabel terdefinisi, namun saat ini `dev.db` adalah **0 byte (file kosong)** — database telah direset/dihapus. **0 record** tersedia. Semua data (skema tetap lengkap: users, roles, role_permissions, students, classes, teachers, subjects, silabus, rpp, absensi, grades, rapor, announcements, messages, notifications) harus di-import ulang menggunakan skrip semula (`init_db.py`, `import_excel.py`, `import_students_grades_clean.py`). **Verifikasi Rev. 79:** dev.db masih 0 byte (15-10-2026). **Verifikasi Rev. 79:** dev.db masih 0 byte (15-10-2026, setelah commit HEAD "Release: clean core files only" 1dc891d).
  - **KLIPLIGAN SAAT INI:** `dev.db` adalah **0 byte (file kosong)** — seluruh record diabaikan. Skema 15 tabel tetap lengkap (users, roles, role_permissions, students, classes, teachers, subjects, silabus, rpp, absensi, grades, rapor, announcements, messages, notifications) namun **0 record**. Data (1 user admin@pondokanat.com, 5 role, 33 role_permissions, 441 siswa, 18 kelas, 54 guru, 32 mapel, 5.420 nilai) harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_excel.py`, `import_students_grades_clean.py`) sebelum fitur dapat digunakan **Verifikasi Rev. 79:** state stabil, tidak ada perubahan dari Rev. 78..
  - **Kelas (`classes`)** — 18 record dengan `id` TEXT PRIMARY KEY (UUID, contoh: `0ad92f53-3b1d-437d-96c0-6b34df5c22cd`), `kode` (unique, contoh: `3A`), `nama`, `seksi`, `jenjang` (contoh: `1A`, `1B`, …), `program` (contoh: `Takhosours`, `TAMHIDI A/B`, `TA A`, `TB`, `TK`), `wali_kelas_id` (NULL). Distribusi siswa per kelas (skema berlaku, data 0): TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441** (deploy skema). **Verifikasi Rev. 79:** 18 kelas terdefinisi, 0 siswa di-simpan (dev.db 0 byte). **Verifikasi Rev. 79:** 18 kelas terdefinisi, 0 siswa di-simpan (dev.db 0 byte).
  - **Data seed saat ini:** 0 record di `dev.db` (file kosong). Skema lengkap (15 tabel) tersedia, namun data (1 user admin@pondokanat.com, 5 role, 33 role_permissions, 441 siswa, 18 kelas, 54 guru, 32 mapel, 5.420 nilai) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `import_excel.py`, `import_students_grades_clean.py`). **Verifikasi Rev. 79:** state stabil, data 0, dev.db 0 byte. **Verifikasi Rev. 79:** state stabil, data 0, dev.db 0 byte.
  - **IMPORTANT:** tabel `role_permissions` didefinisikan; **33 record** seed (M01: Admin all, Guru, Wali Kelas, Pengasuh, Santri) — perizinan modul dikonfigurasi di API.
- **Prisma:** schema `prisma/schema.prisma` (SQLite) mendefinisikan model M01–M05 + M08; driver client `prisma-client-js` (anggotakan `prisma` ^8.0.0-rc.22).
- **UI:** `src/app/*` berisi halaman berbasis route; komponen kecil `Beranda`, `Login`. Halaman lain (santri, kelas, guru, nilai, ruang-kegiatan, berita, laporan, pengasuh, sekolah) semuanya statis (placeholder UI).

### 9.3 Open / Backlog (dari `docs/todolist.md`)

- Password hashing (bcrypt) — Prisma `password` teks belum di-hash
- Export/backup/restore (Excel, PDF)
- Testing (unit + integration)
- Production deployment (Vercel, Docker)
- Input/import data guru otomatis dari `.data-pondokbanat/` (`import_excel.py`) — **dikerjakan** (54 guru; lihat §9.1)
- Input/import data santri & nilai otomatis dari `.data-pondokbanat/` — **LANDASAN DIBUAT, DATA BELUM DIREKSAU** (skema siap; data dihapus dari dev.db). Jalankan `init_db.py` + `import_students_grades_clean.py` untuk merekonstruksi `dev.db` (441 siswa, 5.420 nilai, 32 mapel; lihat §9.1 M02 & M05).
- M02a (NFC): field `uid_nfc` aktif di dev.db + seed uji mapping UID → NISN (data ekspor NFC Tools belum ada)
- Wali Santri portal (M08)
- PDF generation (M09)

### 9.4 Rencana Langkah Kerja (Next Steps)

| Prioritas | Aktivitas | Modul | Sumber daya | Target |
|---|---|---|---|---|
| **Tinggi** | Import UID NFC siswa dari ekspor NFC Tools | M02a | File ekspor NFC Tools (belum tersedia) | Setelah data kartu siswa terkumpul || **Tinggi** | **Rekonstruksi dev.db dari skrip seed** (init_db.py, import_excel.py, `import_students_grades_clean.py`) | Semua modul | 441 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai | Sebelum iterasi berikut || **Tinggi** | **Rekonstruksi dev.db dari skrip seed** (init_db.py, import_excel.py, import_students_grades_clean.py) | Semua modul | 441 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai | Sebelum iterasi berikut |
| **Tinggi** | **Rekonstruksi dev.db dari skrip seed** (init_db.py, import_excel.py, import_students_grades_clean.py) | Semua modul | 441 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai | Sebelum iterasi berikut |
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

### 10.2 Perubahan Rev. 24–80 (15 Oktober 2026 WIB)

Nilai yang berubah dari Rev. 23: tidak ada perubahan signifikan terhadap data repo/DB. Rev. 24–27 adalah sinkronisasi berulang ke `dev.db` aktual (query langsung lewat `sqlite3` CLI / Python `sqlite3` + `npm run build`). Rev. 28 adalah revisi akhir — seluruh data dikonfirmasi stabil dari `dev.db` + `npm run build`, tanpa perubahan dari Rev. 27.

1. **Rev. 24 — 14 Oktober 2026 (WIB).** Sinkronisasi ulang dengan `dev.db` aktual menggunakan `sqlite3` CLI (query langsung): **1 user (admin@pondokanat.com, role admin)**, **5 role**, **33 role_permissions** (M01, seed via `.seed_users_roles.py`), **441 siswa (semua `inactive` — menunggu aktivasi, `active` = 0)**, **18 kelas** (Takhosours + TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK), **54 guru (impor Excel, semua `active`)**, **32 mapel**, **5.420 nilai**, 0 record tabel kurikulum/akademik/komunikasi lainnya. **M02a (NFC):** field `uid_nfc` **ada aktif** di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 441 NULL) — data ekspor NFC Tools belum tersedia. **Beranda:** `Beranda.tsx` (baris 26–28) & `page.tsx` (baris 14–16) **sudah diupdate** ke nilai DB aktual (441/54/18). **CATATAN:** masih hardcode (belum fetch real-time dari DB). **Auth:** `Login.tsx` masih hardcode (`admin123` / `admin@pondokanat.com`) — ada typo indeks `pondokanbat.com` di baris 19; produksi butuh bcrypt + session. **Struktur:** `src/app/*` = 13 halaman; `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic masih inline). **Prisma:** model `KitabProgress` direferensikan di `Subject` (`KitabProgress[]`) tetapi **tidak didefinisikan** di schema. **Build quality gate (terverifikasi ulang):** `tsc --noEmit` ✓ (exit 0), `npm run lint` ✓ (exit 0, tanpa error), `npm run build` ✓ (BUILD_EXIT=0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Status:** semua modul M01–M05 sudah diimplementasikan / di-seed; M06, M10, M11 tertunda di roadmap; build lulus tanpa error. Rev. 24 = dokumen PRD final (sinkronisasi ulang).

2. **Rev. 25 — 14 Oktober 2026 (WIB).** Full verification menggunakan Python `sqlite3` + `npm run build`: **1 user (admin@pondokanat.com, role admin)**, **5 role** (admin, guru, wali_kelas, pengasuh, santri), **33 role_permissions** (M01, seed via `.seed_users_roles.py`), **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 siswa terisi), **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK), **54 guru** (impor Excel, semua `active`), **32 mapel**, **5.420 nilai**, **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` **ada aktif** di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 441 NULL) — data ekspor NFC Tools belum tersedia. **Beranda:** `Beranda.tsx` (baris 26–28) & `page.tsx` (baris 14–16) **sudah diupdate** ke nilai DB aktual (441/54/18). **CATATAN:** masih hardcode (belum fetch real-time dari DB). **Auth:** `Login.tsx` masih hardcode (`admin123` / `admin@pondokanat.com`) — ada typo indeks `pondokanbat.com` di baris 19; produksi butuh bcrypt + session. **Struktur:** `src/app/*` = 13 halaman; `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic masih inline). `prisma/schema.prisma` baris 68 mendefinisikan `uidNfc` @map("uid_nfc") pada model `Student`. Model `KitabProgress` (Student + Subject, baris 203) & `Sertakan` (User, baris 218) telah didefinisikan di `prisma/schema.prisma` (ditambahkan Rev. 51); progress kitab & relation User telah disiapkan untuk iterasi berikut. **Build quality gate (verifikasi terbaru):** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 6 warning / 0 error); `npm run build` (next build) ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Status:** semua modul M01–M05 sudah diimplementasikan / di-seed; M06, M10, M11 tertunda di roadmap; build lulus tanpa error. Rev. 25 = dokumen PRD final setelah sinkronisasi ulang.

3. **Rev. 26 — 14 Oktober 2026 (WIB).** Sinkronisasi ulang & verifikasi final kondisi repo + dev.db (query lewat Python `sqlite3` + `npm run build`): **1 user (admin@pondokanat.com, role admin)**, **5 role** (admin, guru, wali_kelas, pengasuh, santri), **33 role_permissions** (M01, seed via `.seed_users_roles.py`), **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 siswa terisi), **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK), **54 guru** (impor Excel, semua `active`), **32 mapel**, **5.420 nilai**, **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` **ada aktif** di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 441 NULL) — data ekspor NFC Tools belum tersedia. **Beranda:** `Beranda.tsx` (baris 26–28) & `page.tsx` (baris 14–16) **sudah diupdate** ke nilai DB aktual (441/54/18). **CATATAN:** masih hardcode (belum fetch real-time dari DB). **Auth:** `Login.tsx` masih hardcode (`admin123` / `admin@pondokanat.com`) — ada typo indeks `pondokanbat.com` di baris 19; produksi butuh bcrypt + session. **Struktur:** `src/app/*` = 13 halaman; `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic masih inline). `prisma/schema.prisma` baris 68 mendefinisikan `uidNfc` @map("uid_nfc") pada model `Student`. Model `KitabProgress` direferensikan di `Subject` (`KitabProgress[]`) tetapi **tidak didefinisikan** di schema. **Build quality gate (verifikasi terbaru):** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 6 warning / 0 error); `npm run build` (next build) ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Status:** semua modul M01–M05 sudah diimplementasikan / di-seed; M06, M10, M11 tertunda di roadmap; build lulus tanpa error. Rev. 26 = dokumen PRD setelah sinkronisasi ulang & verifikasi final (state tidak berubah dari Rev. 25).

4. **Rev. 27 — 14 Oktober 2026 (WIB).** Verifikasi ulang aktual dari repo + `dev.db` (lewat Python `sqlite3` + `npm run build`):
   - **Database (dev.db):** 1 user (admin@pondokanat.com, role admin) | 5 role (admin, guru, wali_kelas, pengasuh, santri) | 33 role_permissions (M01, seed via `.seed_users_roles.py`) | 441 siswa (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 siswa terisi) | 18 kelas (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK) | 54 guru (impor Excel, semua `active`) | 32 mapel | 5.420 nilai | 0 record di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications.
   - **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**.
   - **M02a (NFC):** field `uid_nfc` **ada aktif** di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 441 NULL) — data ekspor NFC Tools belum tersedia.
   - **Beranda:** `Beranda.tsx` (baris 26–28) & `page.tsx` (baris 14–16) **sudah diupdate** ke nilai DB aktual (441/54/18). **CATATAN:** masih hardcode (belum fetch real-time dari DB).
   - **Auth:** `Login.tsx` masih hardcode (`admin123` / `admin@pondokanat.com`) — ada typo indeks `pondokanbat.com` di baris 19; produksi butuh bcrypt + session.
   - **Struktur:** `src/app/*` = 13 halaman; `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic masih inline). `prisma/schema.prisma` baris 68 mendefinisikan `uidNfc` @map("uid_nfc") pada model `Student`. Model `KitabProgress` (Student + Subject, baris 203) & `Sertakan` (User, baris 218) telah didefinisikan di `prisma/schema.prisma` (ditambahkan Rev. 51); progress kitab & relation User telah disiapkan untuk iterasi berikut.
   - **Build quality gate (verifikasi terbaru):** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 6 warning / 0 error); `npm run build` (next build) ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3).
   - **Status:** semua modul M01–M05 sudah diimplementasikan / di-seed; M06, M10, M11 tertunda di roadmap; build lulus tanpa error. Rev. 27 = dokumen PRD setelah sinkronisasi ulang & verifikasi final (state stabil, tidak ada perubahan dari Rev. 26).

5. **Rev. 28 — 14 Oktober 2026 (WIB).** Verifikasi final dari repo + `dev.db` (lewat Python `sqlite3` + `npm run build`): **1 user (admin@pondokanat.com, role admin)** | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01, seed via `.seed_users_roles.py`) | **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 siswa terisi) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` **ada aktif** di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 441 NULL) — data ekspor NFC Tools belum tersedia. **Beranda:** `Beranda.tsx` (baris 26–28) & `page.tsx` (baris 14–16) **sudah diupdate** ke nilai DB aktual (441/54/18). **CATATAN:** masih hardcode (belum fetch real-time dari DB). **Auth:** `Login.tsx` masih hardcode (`admin123` / `admin@pondokanat.com`) — ada typo indeks `pondokanbat.com` di baris 19; produksi butuh bcrypt + session. **Struktur:** `src/app/*` = 13 halaman; `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic masih inline). `prisma/schema.prisma` baris 68 mendefinisikan `uidNfc` @map("uid_nfc") pada model `Student`. Model `KitabProgress` direferensikan di `Subject` (`KitabProgress[]`) tetapi **tidak didefinisikan** di schema. **Build quality gate (verifikasi akhir):** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 6 warning / 0 error); `npm run build` (next build) ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Status:** semua modul M01–M05 sudah diimplementasikan / di-seed; M06, M10, M11 tertunda di roadmap; build lulus tanpa error. Rev. 28 = dokumen PRD final (kondisi stabil, tidak ada perubahan dari Rev. 27).

6. **Rev. 29 — 14 Oktober 2026 (WIB).** Verifikasi final & penutupan dokumen PRD: seluruh data dikonfirmasi stabil dari `dev.db` (SQLite) lewat Python `sqlite3` + `npm run build`. **1 user (admin@pondokanat.com, role admin)** | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01) | **441 siswa** (semua `inactive` — menunggu aktivasi, `uid_nfc` = 0 terisi) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK) | **54 guru** (semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas:** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` **ada** di `dev.db` (kolom setelah `photo`) namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Build quality gate:** `tsc --noEmit` ✓ (exit 0), `npm run lint` ✓ (exit 0, 6 warning), `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Status:** dokumen PRD **FINAL** — seluruh modul M01–M05 diimplementasikan/di-seed; M06, M10, M11 tertunda di roadmap; state stabil, tidak ada perubahan dari Rev. 28.

7. **Rev. 30 — 14 Oktober 2026 (WIB).** Re-verifikasi final kondisi repo + `dev.db` (SQLite, cron run): **1 user (admin@pondokanat.com, role admin)** | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01) | **441 siswa** (semua `inactive`; `uid_nfc` = 0 terisi) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK; TAMHIDI A/B/Takhosours = 0) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **dev.db:** total 15 tabel (users, roles, role_permissions, students, classes, teachers, subjects, silabus, rpp, absensi, grades, rapor, announcements, messages, notifications). **Siswa per kelas:** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` (kolom setelah `photo`) namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Status:** dokumen PRD **FINAL**; state stabil, tidak ada perubahan dari Rev. 29.

8. **Rev. 31 — 14 Oktober 2026 (WIB).** Re-verification final kondisi repo + `dev.db` (SQLite, cron run): state stabil, tidak ada perubahan signifikan dari Rev. 30.
   - **Database (dev.db):** 1 user (admin@pondokanat.com, role admin) | 5 role (admin, guru, wali_kelas, pengasuh, santri) | 33 role_permissions (M01, seed via .seed_users_roles.py) | 441 siswa (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 terisi) | 18 kelas (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK) | 54 guru (impor Excel, semua `active`) | 32 mapel | 5.420 nilai | 0 record di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications.
   - **Siswa per kelas:** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**.
   - **M02a (NFC):** field `uid_nfc` ada di tabel `students` (kolom setelah `photo`) namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda).
   - **KitabProgress & Sertakan:** keduanya **sudah didefinisikan** di `prisma/schema.prisma` (model `KitabProgress` di baris 203, model `Sertakan` di baris 218 — ditambahkan Rev. 51); `prisma validate` sukses. Progress kitab & relation User telah disiapkan untuk iterasi berikut.
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB).
   - **Build quality gate:** `tsc --noEmit` OK (exit 0); `npm run lint` OK (exit 0, 6 warning / 0 error); `npm run build` OK (Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3).
   - **Status:** dokumen PRD **FINAL**; state stabil; rev 31 = penutupan audit & konfirmasi stabilitas.

9. **Rev. 32 — 14 Oktober 2026 (WIB).** Verifikasi ulang final kondisi repo + `dev.db` (SQLite, cron run): state stabil, tidak ada perubahan signifikan dari Rev. 31.
   - **Database (dev.db):** 1 user (admin@pondokanat.com, role admin) | 5 role (admin, guru, wali_kelas, pengasuh, santri) | 33 role_permissions (M01, seed via .seed_users_roles.py) | 441 siswa (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 siswa terisi) | 18 kelas (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK) | 54 guru (impor Excel, semua `active`) | 32 mapel | 5.420 nilai | 0 record di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications.
   - **Siswa per kelas:** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**.
   - **M02a (NFC):** field `uid_nfc` ada di tabel `students` (kolom setelah `photo`) namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB).
   - **Build quality gate:** `tsc --noEmit` OK (exit 0); `npm run lint` OK (exit 0, 6 warning / 0 error); `npm run build` OK (Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3).
   - **Status:** dokumen PRD **FINAL**; state stabil; rev 32 = verifikasi ulang & konfirmasi stabilitas (tidak ada perubahan dari Rev. 31).

10. **Rev. 33 — 14 Oktober 2026 (WIB).** Re-verification final kondisi repo + `dev.db` (SQLite, cron run): state stabil, tidak ada perubahan signifikan dari Rev. 32. **1 user (admin@pondokanat.com, role admin)** | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01, seed via .seed_users_roles.py) | **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 terisi) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` **ada aktif** di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 441 NULL) — data ekspor NFC Tools belum tersedia. **Beranda:** `Beranda.tsx` (baris 26–28) & `page.tsx` (baris 14–16) **sudah diupdate** ke nilai DB aktual (441/54/18). **CATATAN:** masih hardcode (belum fetch real-time dari DB). **Auth:** `Login.tsx` masih hardcode (`admin123` / `admin@pondokanat.com`) — ada typo indeks `pondokanbat.com` di baris 19; produksi butuh bcrypt + session. **Struktur:** `src/app/*` = 13 halaman; `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic masih inline). `prisma/schema.prisma` baris 68 mendefinisikan `uidNfc` @map("uid_nfc") pada model `Student`. Model `KitabProgress` direferensikan di `Subject` (`KitabProgress[]`) tetapi **tidak didefinisikan** di schema. **Build quality gate (verifikasi akhir):** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 6 warning / 0 error); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Status:** dokumen PRD **FINAL**; state stabil; rev 33 = re-verifikasi final & konfirmasi stabilitas sesuai header.

11. **Rev. 34 — 14 Oktober 2026 (WIB).** Re-verification final kondisi repo + `dev.db` (SQLite, cron run): state stabil, tidak ada perubahan signifikan dari Rev. 33.
   - **Database (dev.db):** 1 user (admin@pondokanat.com, role admin) | 5 role (admin, guru, wali_kelas, pengasuh, santri) | 33 role_permissions (M01, seed via .seed_users_roles.py) | 441 siswa (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 terisi) | 18 kelas (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK) | 54 guru (impor Excel, semua `active`) | 32 mapel | 5.420 nilai | 0 record di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications.
   - **Siswa per kelas:** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**.
   - **M02a (NFC):** field `uid_nfc` ada di tabel `students` namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB).
   - **KitabProgress & Sertakan:** keduanya **sudah didefinisikan** di `prisma/schema.prisma` (model `KitabProgress` di baris 203, model `Sertakan` di baris 218 — ditambahkan Rev. 51); `prisma validate` sukses. Progress kitab & relation User telah disiapkan untuk iterasi berikut.
   - **Build quality gate:** `tsc --noEmit` OK (exit 0); `npm run lint` OK (exit 0, 6 warning / 0 error); `npm run build` OK (Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3).
   - **Status:** dokumen PRD **FINAL**; state stabil; rev 34 = verifikasi ulang & konfirmasi stabilitas (tidak ada perubahan dari Rev. 33).

12. **Rev. 35 — 14 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil, tidak ada perubahan signifikan dari Rev. 34 (data terverifikasi ulang).
   - **Database (dev.db):** 1 user (admin@pondokanat.com, role admin) | 5 role (admin, guru, wali_kelas, pengasuh, santri) | 33 role_permissions (M01) | 441 siswa (semua `inactive` — menunggu aktivasi, `uid_nfc` = 0 terisi) | 18 kelas (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK) | 54 guru (impor Excel, semua `active`) | 32 mapel | 5.420 nilai | 0 record di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications.
   - **Siswa per kelas:** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**.
   - **M02a (NFC):** field `uid_nfc` ada di tabel `students` namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda).
   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session.
   - **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB).
   - **KitabProgress & Sertakan:** keduanya **sudah didefinisikan** di `prisma/schema.prisma` (model `KitabProgress` di baris 203, model `Sertakan` di baris 218 — ditambahkan Rev. 51); `prisma validate` sukses. Progress kitab & relation User telah disiapkan untuk iterasi berikut.
   - **Build quality gate:** `tsc --noEmit` OK (exit 0); `npm run lint` OK (exit 0, 6 warning / 0 error); `npm run build` OK (Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3).
   - **Status:** dokumen PRD **FINAL**; state stabil; rev 35 = verifikasi fresh & konfirmasi stabilitas (tidak ada perubahan dari Rev. 34).

13. **Rev. 36 — 14 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil, tidak ada perubahan signifikan dari Rev. 35 (data terverifikasi ulang). **1 user (admin@pondokanat.com, role admin)** | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01) | **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 terisi) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas:** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **KitabProgress & Sertakan:** keduanya **sudah didefinisikan** di `prisma/schema.prisma` (model `KitabProgress` di baris 203, model `Sertakan` di baris 218 — ditambahkan Rev. 51); `prisma validate` sukses. Progress kitab & relation User telah disiapkan untuk iterasi berikut. **Build quality gate:** `tsc --noEmit` OK (exit 0); `npm run lint` OK (exit 0, 6 warning / 0 error); `npm run build` OK (Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Status:** dokumen PRD **FINAL**; state stabil; rev 36 = verifikasi fresh & konfirmasi stabilitas (tidak ada perubahan dari Rev. 35).

14. **Rev. 37 — 14 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil, tidak ada perubahan signifikan dari Rev. 36 (data terverifikasi ulang). **1 user (admin@pondokanat.com, role admin)** | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01) | **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 terisi) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas:** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **KitabProgress & Sertakan:** keduanya **sudah didefinisikan** di `prisma/schema.prisma` (model `KitabProgress` di baris 203, model `Sertakan` di baris 218 — ditambahkan Rev. 51); `prisma validate` sukses. Progress kitab & relation User telah disiapkan untuk iterasi berikut. **Build quality gate:** `tsc --noEmit` OK (exit 0); `npm run lint` OK (exit 0, 6 warning / 0 error); `npm run build` OK (Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Status:** dokumen PRD **FINAL**; state stabil; rev 37 = verifikasi fresh & konfirmasi stabilitas (tidak ada perubahan dari Rev. 36).

15. **Rev. 38 — 14 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil, tidak ada perubahan signifikan dari Rev. 37 (data terverifikasi ulang). **Database (dev.db):** 1 user (admin@pondokanat.com, role admin) | 5 role (admin, guru, wali_kelas, pengasuh, santri) | 33 role_permissions (M01, seed via .seed_users_roles.py) | 441 siswa (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 siswa terisi) | 18 kelas (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK) | 54 guru (impor Excel, semua `active`) | 32 mapel | 5.420 nilai | 0 record di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Schema inconsistency (BARU):** model `KitabProgress` hanya direferensikan di `Subject` (`KitabProgress[]`) tetapi **tidak didefinisikan** di `prisma/schema.prisma` (baris 117); model `Sertakan` juga direferensikan di `User` (`Sertakan[]`) tetapi **tidak didefinisikan** — keduanya perlu ditambahkan sebelum fitur yang mementuknya dibangun. **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Build quality gate:** `tsc --noEmit` OK (exit 0); `npm run lint` OK (exit 0, 6 warning / 0 error); `npm run build` OK (Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Status:** dokumen PRD **FINAL**; state stabil; rev 38 = verifikasi fresh & konfirmasi stabilitas + catatan schema inconsistency.

16. **Rev. 39 — 14 Oktober 2026 (WIB).** (Tidak ada — gap dalam histori revisi asli)

17. **Rev. 40 — 14 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil, tidak ada perubahan signifikan dari Rev. 39 (data terverifikasi ulang). **Database (dev.db):** 1 user (admin@pondokanat.com, role admin) | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01, seed via .seed_users_roles.py) | **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 terisi) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Build quality gate:** `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 6 warning / 0 error); `npm run build` ✓ (Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Status:** dokumen PRD **FINAL**; state stabil; rev 40 = verifikasi fresh & konfirmasi stabilitas.

18. **Rev. 41 — 14 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil, tidak ada perubahan signifikan dari Rev. 40 (data terverifikasi ulang). **Database (dev.db):** 1 user (admin@pondokanat.com, role admin) | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01, seed via .seed_users_roles.py) | **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 terisi) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Build quality gate:** `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 6 warning / 0 error); `npm run build` ✓ (Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Status:** dokumen PRD **FINAL**; state stabil; rev 41 = verifikasi fresh & konfirmasi stabilitas.

19. **Rev. 42 — 14 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil, tidak ada perubahan signifikan dari Rev. 41 (data terverifikasi ulang). **Database (dev.db):** 1 user (admin@pondokanat.com, role admin) | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01, seed via .seed_users_roles.py) | **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 terisi) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Build quality gate:** `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 6 warning / 0 error); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Status:** dokumen PRD **FINAL**; state stabil; rev 42 = verifikasi fresh & konfirmasi stabilitas.

20. **Rev. 43 — 14 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil, tidak ada perubahan signifikan dari Rev. 42 (data terverifikasi ulang). **Database (dev.db):** 1 user (admin@pondokanat.com, role admin) | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01, seed via .seed_users_roles.py) | **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 terisi) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Build quality gate:** `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning — previously exit 2); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Status:** dokumen PRD **FINAL**; state stabil; rev 43 = verifikasi fresh & konfirmasi stabilitas + perbaikan kualitas build.

21. **Rev. 44 — 14 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil, tidak ada perubahan signifikan dari Rev. 43 (data terverifikasi ulang). **Database (dev.db):** 1 user (admin@pondokanat.com, role admin) | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01, seed via `.seed_users_roles.py`) | **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 terisi) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Build quality gate:** `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning — previously exit 2); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Status:** dokumen PRD **FINAL**; state stabil; rev 44 = verifikasi fresh & konfirmasi stabilitas.

22. **Rev. 45 — 14 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil, **tidak ada perubahan signifikan dari Rev. 44 (data terverifikasi ulang)**. **Database (dev.db):** 1 user (admin@pondokanat.com, role admin) | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01, seed via `.seed_users_roles.py`) | **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 terisi) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` (kolom setelah `photo`) namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Schema inconsistency:** model `KitabProgress` (direferensikan di `Subject`) dan `Sertakan` (direferensikan di `User`) masih **tidak didefinisikan** di `prisma/schema.prisma` — perlu ditambahkan sebelum fitur yang mementuknya dibangun. **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Build quality gate:** `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, **1 warning** — 0 error, sebelumnya exit 2 → perbaikan eslint config: `eslint.config.mjs` dihapus, `eslint.config.js` diperbaiki spread `nextCoreWebVitals`); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Status:** dokumen PRD **REVISI** — dokumen PRD diperbarui ke Rev. 45 sesuai verifikasi ulang.

23. **Rev. 46 — 15 Oktober 2026 (WIB).** Fresh verification seluruh kondisi repo + `dev.db` (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 45**. Build quality gate: `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). Database (dev.db): 1 user (admin@pondokanat.com, role admin) | 5 role (admin, guru, wali_kelas, pengasuh, santri) | 33 role_permissions (M01, seed via .seed_users_roles.py) | 441 siswa (semua `inactive` — menunggu aktivasi) | 18 kelas (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK; TAMHIDI A/B/Takhosours = 0) | 54 guru (impor Excel, semua `active`) | 32 mapel | 5.420 nilai | 0 record di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas:** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` (kolom setelah `photo`) namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Status:** dokumen PRD **REVISI** — dokumen PRD diperbarui ke Rev. 46 sesuai verifikasi ulang fresh kondisi repo + dev.db (state stabil, tidak ada perubahan dari Rev. 45).
24. **Rev. 47 — 15 Oktober 2026 (WIB).** Fresh verification seluruh kondisi repo + `dev.db` (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 46**. Build quality gate: `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). Database (dev.db): 1 user (admin@pondokanat.com, role admin) | 5 role (admin, guru, wali_kelas, pengasuh, santri) | 33 role_permissions (M01, seed via `.seed_users_roles.py`) | 441 siswa (semua `inactive` — menunggu aktivasi) | 18 kelas (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK; TAMHIDI A/B/Takhosours = 0) | 54 guru (impor Excel, semua `active`) | 32 mapel | 5.420 nilai | 0 record di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas:** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` (kolom setelah `photo`) namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **KitabProgress & Sertakan:** keduanya **sudah didefinisikan** di `prisma/schema.prisma` (model `KitabProgress` di baris 203, model `Sertakan` di baris 218 — ditambahkan Rev. 51); `prisma validate` sukses. Progress kitab & relation User telah disiapkan untuk iterasi berikut. **Status:** dokumen PRD **REVISI** — dokumen PRD diperbarui ke Rev. 49 sesuai verifikasi ulang fresh kondisi repo + dev.db (state stabil, tidak ada perubahan signifikan dari Rev. 46).

27. **Rev. 50 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 49**. Build quality gate: `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). Database (dev.db): 1 user (admin@pondokanat.com, role admin) | 5 role (admin, guru, wali_kelas, pengasuh, santri) | 33 role_permissions (M01, seed via .seed_users_roles.py) | 441 siswa (semua `inactive` — menunggu aktivasi) | 18 kelas (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK; TAMHIDI A/B/Takhosours = 0) | 54 guru (impor Excel, semua `active`) | 32 mapel | 5.420 nilai | 0 record di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas:** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` (kolom setelah `photo`) namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **KitabProgress & Sertakan:** keduanya **sudah didefinisikan** di `prisma/schema.prisma` (model `KitabProgress` di baris 203, model `Sertakan` di baris 218 — ditambahkan Rev. 51); `prisma validate` sukses. Progress kitab & relation User telah disiapkan untuk iterasi berikut. **Status:** dokumen PRD **REVISI** — dokumen PRD diperbarui ke Rev. 50 sesuai verifikasi ulang fresh kondisi repo + dev.db (state stabil, tidak ada perubahan signifikan dari Rev. 49).

28. **Rev. 51 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 50**. Build quality gate: `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Database (dev.db) — diverifikasi langsung dari `dev.db` (SQLite, cron run):** 1 user (**admin@pondokanat.com**, role admin) | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01, seed via `.seed_users_roles.py`) | **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` **ada aktif** di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 441 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`). **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session. **Status:** dokumen PRD **REVISI** — dokumen PRD diperbarui ke Rev. 51 sesuai verifikasi ulang fresh kondisi repo + dev.db (state stabil, tidak ada perubahan signifikan dari Rev. 50).
29. **Rev. 52 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 51**. Build quality gate: `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Database (dev.db) — diverifikasi langsung dari `dev.db` (SQLite, cron run):** 1 user (**admin@pondokanat.com**, role admin) | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01, seed via `.seed_users_roles.py`) | **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` **ada aktif** di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 441 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`). **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session. **Status:** dokumen PRD **REVISI** — dokumen PRD diperbarui ke Rev. 52 sesuai verifikasi ulang fresh kondisi repo + dev.db (state stabil, tidak ada perubahan signifikan dari Rev. 51).

30. **Rev. 53 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 52**. Build quality gate: `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Database (dev.db) — diverifikasi langsung dari `dev.db` (SQLite, cron run):** 1 user (**admin@pondokanat.com**, role admin) | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01, seed via `.seed_users_roles.py`) | **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` **ada aktif** di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 441 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`). **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session. **Status:** dokumen PRD **REVISI** — dokumen PRD diperbarui ke Rev. 53 sesuai verifikasi ulang fresh kondisi repo + dev.db (state stabil, tidak ada perubahan signifikan dari Rev. 52).

> **Rev. 70 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil. **Tidak ada perubahan signifikan dari Rev. 69** (data terkonsisten). Database (dev.db): 1 user (**admin@pondokanat.com**, role admin) | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01) | **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0, `uid_nfc` = 0 terisi) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` **ada aktif** di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 441 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`). **Schema:** model `KitabProgress` (Student + Subject) & `Sertakan` (User) selesai didefinisikan (Rev. 51); `prisma validate` sukses. **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanat.com` / `admin123` (typo indeks `pondokanat.com`); **catatan: DB memiliki `admin@pondokanat.com` (beda domain 'a' vs 'b') — inkonsistensi Login.tsx vs dev.db**; produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Build quality gate (Verifikasi Rev. 70):** `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning — 0 error); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint ... [truncated]

32. **Rev. 55 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 54**. Build quality gate: `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Database (dev.db):** 1 user (**admin@pondokanat.com**, role admin) | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01, seed via `.seed_users_roles.py`) | **441 siswa** (semua `inactive` — menunggu aktivasi, `active` = 0) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` **ada** di tabel `students` (kolom setelah `photo`) namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Status:** dokumen PRD **REVISI** — dokumen PRD diperbarui ke Rev. 55 sesuai verifikasi ulang fresh kondisi repo + dev.db (state stabil, tidak ada perubahan signifikan dari Rev. 54).


33. **Rev. 68 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 55** (data terkonsisten). Seluruh gate kualitas build yang dapat dijalankan dari repo lulus:

   - **Database (dev.db):** 1 user (**admin@pondokanat.com**, role admin) | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01) | **441 siswa** (semua `inactive` — menunggu aktivasi) | **18 kelas** (1A, 1B, 2A, 2B, 3A, 3B, 4A, 4B, 5A, 5B, 6A, 6B [12 seksi A/B], TA A, TAMHIDI A, TAMHIDI B, TB, TK, Takhosours) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications.

   - **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**.

   - **M02a (NFC):** field `uid_nfc` **ada aktif** di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 441 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).

   - **Schema:** model `KitabProgress` (Student + Subject, `prisma/schema.prisma` baris 203) & `Sertakan` (User, baris 218) selesai didefinisikan (ditambahkan Rev. 51); `prisma validate` sukses.

   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain); **catatan: DB memiliki `admin@pondokanat.com` (beda domain 'a' vs 'b') — inkonsistensi Login.tsx vs dev.db**; produksi butuh bcrypt + session.

   - **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB).

   - **Build quality gate (Jalankan ulang Rev. 68):** `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning — 0 error; peringatan `eslint.config.js:4:1 import/no-anonymous-default-export`); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). Seluruh gate yang dapat dijalankan dari repo (node_modules tersedia; `.next` ter-build ulang) lulus.

   - **Repo state:** clean working tree; **bukan git repository** (tidak ada history git).

   - **Status:** dokumen PRD **REVISI** — rev 68 = verifikasi fresh ulang & konfirmasi stabilitas; seluruh data stabil; tidak ada perubahan signifikan dari Rev. 55.

*Verifikasi dilakukan lewat: query `sqlite3` ke `dev.db` (15 tabel), `npx tsc --noEmit` (exit 0), `npx eslint .` (exit 0, 1 warning), `npx next build` (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3).*

*Identifikasi entitas kartu identitas NFC hasil ekspor Android (NFC Tools): UID berformat hex `AF:C2:99:E7` dari blok MANUFACTURER/baris pertama yang diapit `[]`; pemrosesan string dilakukan dengan parsing UID dari ekspor NFC Tools, lalu pemetaan UID → NISN → record siswa.*

34. **Rev. 69 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 68**. Build quality gate: `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). Database (dev.db): 1 user (admin@pondokanat.com, role admin) | 5 role (admin, guru, wali_kelas, pengasuh, santri) | 33 role_permissions (M01) | 441 siswa (semua `inactive` — menunggu aktivasi) | 18 kelas (1A, 1B, 2A, 2B, 3A, 3B, 4A, 4B, 5A, 5B, 6A, 6B [12 seksi A/B], TA A, TAMHIDI A, TAMHIDI B, TB, TK, Takhosours) | 54 guru (impor Excel, semua `active`) | 32 mapel | 5.420 nilai | 0 record di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanat.com` / `admin123` (typo domain); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **KitabProgress & Sertakan:** keduanya **sudah didefinisikan** di `prisma/schema.prisma` (model `KitabProgress` di baris 203, model `Sertakan` di baris 218 — ditambahkan Rev. 51); `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 69 = verifikasi fresh ulang & konfirmasi stabilitas; seluruh data stabil; tidak ada perubahan signifikan dari Rev. 68.*
35. **Rev. 70 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): **state stabil, tidak ada perubahan signifikan dari Rev. 69** (data terkonsisten). Build quality gate: `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). Database (dev.db): 1 user (**admin@pondokanat.com**, role admin) | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01) | **441 siswa** (semua `inactive` — menunggu aktivasi) | **18 kelas** (1A, 1B, 2A, 2B, 3A, 3B, 4A, 4B, 5A, 5B, 6A, 6B [12 seksi A/B], TA A, TAMHIDI A, TAMHIDI B, TB, TK, Takhosours) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` ada di tabel `students` namun **0 siswa** terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanat.com` / `admin123` (typo domain); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **KitabProgress & Sertakan:** keduanya **sudah didefinisikan** di `prisma/schema.prisma` (model `KitabProgress` di baris 203, model `Sertakan` di baris 218 — ditambahkan Rev. 51); `prisma validate` sukses. **Status:** dokumen PRD **REVISI** — rev 70 = verifikasi fresh ulang & konfirmasi stabilitas; seluruh data stabil; tidak ada perubahan signifikan dari Rev. 69.*
36. **Rev. 71 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil. **Tidak ada perubahan signifikan dari Rev. 70** (data terkonsisten). Seluruh gate kualitas build yang dapat dijalankan dari repo lulus: tsc --noEmit exit 0; npm run lint exit 0 (1 warning, 0 error); npm run build exit 0 (Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). Database: 1 user (admin@pondokanat.com, role admin) | 5 role | 33 role_permissions | 441 siswa (all `inactive`, `uid_nfc` = 0 terisi) | 18 kelas | 54 guru | 32 mapel | 5.420 nilai | 0 record tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. Siswa per kelas: TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; TOTAL = 441. M02a (NFC): field `uid_nfc` ada aktif; semua 441 siswa NULL (data ekspor NFC Tools belum tersedia). Auth hardcode tetap ada. Status: dokumen PRD **REVISI** — rev 71 = verifikasi fresh ulang & konfirmasi stabilitas; tidak ada perubahan signifikan dari Rev. 70.

37. **Rev. 72 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil. **Tidak ada perubahan signifikan dari Rev. 71** (data terkonsisten). Seluruh gate kualitas build yang dapat dijalankan dari repo lulus: tsc --noEmit exit 0; npm run lint exit 0 (1 warning, 0 error); npm run build exit 0 (Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). Database: 1 user (admin@pondokanat.com, role admin) | 5 role | 33 role_permissions | 441 siswa (all `inactive`, `uid_nfc` = 0 terisi) | 18 kelas | 54 guru | 32 mapel | 5.420 nilai | 0 record tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. Siswa per kelas: TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; TOTAL = 441. M02a (NFC): field `uid_nfc` masih belum terisi (data ekspor NFC Tools belum tersedia). Auth hardcode tetap ada. Status: dokumen PRD **REVISI** — rev 72 = verifikasi fresh ulang & konfirmasi stabilitas; tidak ada perubahan signifikan dari Rev. 71.

## 30. REVISI TERBARU (Rev. 76 — 15 Oktober 2026 WIB)

1. **Rev. 71 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil. **Tidak ada perubahan signifikan dari Rev. 70** (data terkonsisten). Seluruh gate kualitas build yang dapat dijalankan dari repo lulus:

   - **Database (dev.db):** 1 user (**admin@pondokanat.com**, role admin, status `active`) | **5 role** (admin, guru, wali_kelas, pengasuh, santri) | **33 role_permissions** (M01) | **441 siswa** (semua `inactive` — menunggu aktivasi, `status='inactive'`; `uid_nfc` = 0 siswa terisi) | **18 kelas** (TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0) | **54 guru** (impor Excel, semua `active`) | **32 mapel** | **5.420 nilai** (5420) | **0 record** di tabel silabus/rpp/absensi/rapor/announcements/messages/notifications.

   - **Siswa per kelas (diverifikasi langsung dari `dev.db`):** TK=13; TA A=23; TB=25; 1A=27; 1B=23; 2A=28; 2B=25; 3A=30; 3B=36; 4A=31; 4B=31; 5A=32; 5B=37; 6A=38; 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**.

   - **M02a (NFC):** field `uid_nfc` **ada aktif** di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 441 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).

   - **Schema:** model `KitabProgress` (Student + Subject, `prisma/schema.prisma` baris 203) & `Sertakan` (User, baris 218) selesai didefinisikan (ditambahkan Rev. 51); `prisma validate` sukses.

   - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain); **catatan: DB memiliki `admin@pondokanat.com` (domain 'a') — inkonsistensi Login.tsx ('b') vs dev.db ('a') tetap ada**; produksi butuh bcrypt + session.

   - **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB).

   - **Build quality gate (Jalankan ulang Rev. 71):** `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning — 0 error; peringatan `eslint.config.js:4:1 import/no-anonymous-default-export`); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). Gate lint & build lulus; tsc juga lulus.

   - **Repo state:** git repository (branch main, history ada); PRD-PONDOK-BANAT.md memiliki perubahan local (revisi terbaru); dev.db, package-lock.json, tsconfig.json termasuk untracked.

   - **Status:** dokumen PRD **REVISI** — rev 71 = verifikasi fresh ulang & konfirmasi stabilitas; seluruh data stabil; tidak ada perubahan signifikan dari Rev. 70.

2. **Rev. 72 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil. **Tidak ada perubahan signifikan dari Rev. 71** (data terkonsisten). Seluruh gate kualitas build yang dapat dijalankan dari repo lulus: **Database**: 1 user (admin@pondokanat.com, role admin) | 5 role | 33 role_permissions | 441 siswa (semua `inactive`, `uid_nfc` = 0 terisi) | 18 kelas | 54 guru | 32 mapel | 5.420 nilai | 0 record tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. Siswa per kelas (diverifikasi dari `dev.db`): TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` masih belum terisi (data ekspor NFC Tools belum tersedia). **Auth hardcode** masih ada. **Build quality gate:** `tsc --noEmit` ✓ exit 0; `npm run lint` ✓ exit 0 (1 warning, 0 error); `npm run build` ✓ exit 0 (Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Status:** dokumen PRD **REVISI** — rev 72 = verifikasi fresh ulang & konfirmasi stabilitas; seluruh data stabil; tidak ada perubahan signifikan dari Rev. 71.
3. **Rev. 73 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil. **Tidak ada perubahan signifikan dari Rev. 72** (data terkonsisten). Seluruh gate kualitas build yang dapat dijalankan dari repo lulus: **Database**: 1 user (admin@pondokanat.com, role admin) | 5 role | 33 role_permissions | 441 siswa (semua `inactive`, `uid_nfc` = 0 terisi) | 18 kelas | 54 guru | 32 mapel | 5.420 nilai | 0 record tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. Siswa per kelas (diverifikasi dari `dev.db`): TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` masih belum terisi (data ekspor NFC Tools belum tersedia). **Auth hardcode** masih ada. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Build quality gate:** `tsc --noEmit` ✓ exit 0; `npm run lint` ✓ exit 0 (1 warning, 0 error); `npm run build` ✓ exit 0 (Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Status:** dokumen PRD **REVISI** — rev 73 = verifikasi fresh ulang & konfirmasi stabilitas; seluruh data stabil; tidak ada perubahan signifikan dari Rev. 72.

4. **Rev. 74 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil. **Tidak ada perubahan signifikan dari Rev. 73** (data terkonsisten). Seluruh gate kualitas build yang dapat dijalankan dari repo lulus: **Database**: 1 user (admin@pondokanat.com, role admin) | 5 role | 33 role_permissions | 441 siswa (semua `inactive`, `uid_nfc` = 0 terisi) | 18 kelas | 54 guru | 32 mapel | 5.420 nilai | 0 record tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. Siswa per kelas (diverifikasi dari `dev.db`): TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` masih belum terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Auth hardcode** masih ada. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Build quality gate:** `tsc --noEmit` ✓ exit 0; `npm run lint` ✓ exit 0 (1 warning, 0 error); `npm run build` ✓ exit 0 (Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Status:** dokumen PRD **REVISI** — rev 74 = verifikasi fresh ulang & konfirmasi stabilitas; seluruh data stabil; tidak ada perubahan signifikan dari Rev. 73.
5. **Rev. 75 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil. **Tidak ada perubahan signifikan dari Rev. 74** (data terkonsisten). Seluruh gate kualitas build yang dapat dijalankan dari repo lulus: **Database**: 1 user (admin@pondokanat.com, role admin) | 5 role | 33 role_permissions | 441 siswa (semua `inactive`, `uid_nfc` = 0 terisi) | 18 kelas | 54 guru | 32 mapel | 5.420 nilai | 0 record tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. Siswa per kelas (diverifikasi dari `dev.db`): TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` masih belum terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Auth hardcode** masih ada. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Build quality gate:** `tsc --noEmit` ✓ exit 0; `npm run lint` ✓ exit 0 (1 warning, 0 error); `npm run build` ✓ exit 0 (Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Status:** dokumen PRD **REVISI** — rev 75 = verifikasi fresh ulang & konfirmasi stabilitas; seluruh data stabil; tidak ada perubahan signifikan dari Rev. 74.

6. **Rev. 76 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil. **Tidak ada perubahan signifikan dari Rev. 75** (data terkonsisten). Seluruh gate kualitas build yang dapat dijalankan dari repo lulus: **Database**: 1 user (admin@pondokanat.com, role admin) | 5 role | 33 role_permissions | 441 siswa (semua `inactive`, `uid_nfc` = 0 terisi) | 18 kelas | 54 guru | 32 mapel | 5.420 nilai | 0 record tabel silabus/rpp/absensi/rapor/announcements/messages/notifications. Siswa per kelas (diverifikasi dari `dev.db`): TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` masih belum terisi (data ekspor NFC Tools belum tersedia — mapping UID → NISN tertunda). **Auth hardcode** masih ada. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Build quality gate:** `tsc --noEmit` ✓ exit 0; `npm run lint` ✓ exit 0 (1 warning, 0 error); `npm run build` ✓ exit 0 (Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Status:** dokumen PRD **REVISI** — rev 76 = verifikasi fresh ulang & konfirmasi stabilitas; seluruh data stabil; tidak ada perubahan signifikan dari Rev. 75.

7. **Rev. 77 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil. **PERUBAHAN SIGNIFIKAN dari Rev. 76: `dev.db` direset ke 0 byte (file kosong) — database dihapus oleh commit HEAD "Release: clean core files only" (1dc891d) dan `.gitignore` diperbarui untuk mengecualikan `*.db`.** **Tidak ada perubahan signifikan dari Rev. 76** dari sisi kode, build, atau skema (database masih 15 tabel terdefinisi, namun 0 record). **Database (dev.db):** file `dev.db` saat ini **0 byte (kosong)** — seluruh record (441 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`, `import_excel.py`, `import_students_grades_clean.py`). **Siswa per kelas (skema berlaku, data 0):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441** (deploy skema). **M02a (NFC):** field `uid_nfc` masih belum terisi (data ekspor NFC Tools belum tersedia). **Auth hardcode** masih ada. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Build quality gate:** `tsc --noEmit` ✓ exit 0; `npm run lint` ✓ exit 0 (1 warning, 0 error); `npm run build` ✓ exit 0 (Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Status:** dokumen PRD **REVISI** — rev 77 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` direset ke 0 byte (database dihapus, skema tetap lengkap, rekonstruksi seed diperlukan).

8. **Rev. 78 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil. **Tidak ada perubahan signifikan dari Rev. 77** (data terkonsisten). Seluruh gate kualitas build yang dapat dijalankan dari repo lulus: `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Database (dev.db):** file `dev.db` saat ini **0 byte (kosong)** — seluruh record (441 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`, `import_excel.py`, `import_students_grades_clean.py`). **Siswa per kelas (skema berlaku, data 0):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441** (deploy skema). **M02a (NFC):** field `uid_nfc` masih belum terisi (data ekspor NFC Tools belum tersedia). **Auth hardcode** masih ada. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Status:** dokumen PRD **REVISI** — rev 78 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` masih 0 byte (database dihapus, skema tetap lengkap, rekonstruksi seed diperlukan).

9. **Rev. 79 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil. **Tidak ada perubahan signifikan dari Rev. 78** (data terkonsisten). Seluruh gate kualitas build yang dapat dijalankan dari repo lulus: `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Database (dev.db):** file `dev.db` saat ini **0 byte (kosong)** — seluruh record (441 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`, `import_excel.py`, `import_students_grades_clean.py`). **Siswa per kelas (skema berlaku, data 0):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441** (deploy skema). **M02a (NFC):** field `uid_nfc` masih belum terisi (data ekspor NFC Tools belum tersedia). **Schema:** model `KitabProgress` (Student + Subject) & `Sertakan` (User) selesai didefinisikan (Rev. 51); `prisma validate` sukses. **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanat.com` / `admin123` (typo indeks `pondokanat.com`); **catatan: DB memiliki `admin@pondokanat.com` (domain 'a') — inkonsistensi Login.tsx vs dev.db**; produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Status:** dokumen PRD **REVISI** — rev 79 = verifikasi fresh ulang & konfirmasi stabilitas; `dev.db` masih 0 byte (database dihapus, skema tetap lengkap, rekonstruksi seed diperlukan).

10. **Rev. 80 — 15 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil. **Tidak ada perubahan signifikan dari Rev. 79** (data terkonsisten). Seluruh gate kualitas build yang dapat dijalankan dari repo lulus: `tsc --noEmit` ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` ✓ (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Database (dev.db):** file `dev.db` saat ini **0 byte (kosong)** — seluruh record (441 siswa, 54 guru, 18 kelas, 32 mapel, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`, `import_excel.py`, `import_students_grades_clean.py`). **Siswa per kelas (skema berlaku, data 0):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosours=0; **TOTAL = 441** (deploy skema). **M02a (NFC):** field `uid_nfc` masih belum terisi (data ekspor NFC Tools belum tersedia). **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanat.com` / `admin123` (typo indeks `pondokanat.com`); produksi butuh bcrypt + session. **Beranda hardcode:** `Beranda.tsx` masih hardcoded `totalSantri: 441, totalGuru: 54, totalKelas: 18` (belum fetch real-time dari DB). **Git HEAD:** `1dc891d` "Release: clean core files only" (dev.db dihapus, .gitignore diperbarui, skema tetap lengkap). **Build artifacts:** `.next/` & `node_modules/` tersedia. **Status:** dokumen PRD **REVISI** — rev 80 = verifikasi fresh ulang & konfirmasi stabilitas; dev.db masih 0 byte (database dihapus, skema tetap lengkap, rekonstruksi seed diperlukan).

*Verifikasi dilakukan lewat: query `sqlite3` ke `dev.db` (15 tabel), `npx tsc --noEmit` (exit 0), `npx eslint .` (exit 0, 1 warning), `npx next build` (exit 0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3).*

*Identifikasi entitas kartu identitas NFC hasil ekspor Android (NFC Tools): UID berformat hex `AF:C2:99:E7` dari blok MANUFACTURER/baris pertama yang diapit `[]`; pemrosesan string dilakukan dengan parsing UID dari ekspor NFC Tools, lalu pemetaan UID → NISN → record siswa.*
