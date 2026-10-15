#!/usr/bin/env python3
"""Update PRD-PONDOK-BANAT.md with Rev. 16 and fixes (corrected patterns)."""

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r') as f:
    content = f.read()

# 1. Update Rev. 15 header note to Rev. 16
old_rev15 = """> **Rev. 15 — 14 Oktober 2026 (WIB).** Sinkronisasi ulang dengan kondisi DB aktual (`dev.db` lewat `db_summary.py`): 1 user (role admin), 5 role, 0 role_permissions, **441 siswa (semua `inactive` — menunggu aktivasi)**, **18 kelas** (Takhosous + TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK), 54 guru (impor Excel), **32 mapel (impor Excel)**, **5.420 nilai (impor Excel)**, 0 record tabel kurikulum/akademik/lainnya. Build quality gate (terverifikasi ulang): `tsc --noEmit` ✓ (exit 0) + `npm run lint` ✓ (exit 0, 6 warning — tanpa error) + `npm run build` ✓ (exit 0). M02a (NFC): field `uid_nfc` **sudah ditambahkan** ke schema `prisma/schema.prisma` (kolom `uidNfc` dengan `@map(\"uid_nfc\")`); field juga ditambahkan ke `init_db.py` & `init_schema.sql` (kolom `uid_nfc TEXT`); reconstruct `dev.db` via `python3 init_db.py` → `init_schema.sql` untuk mempersiapkan. Mapping UID → NISN masih **belum diuji** (data ekspor NFC Tools belum ada). **M02 (Santri): impor batch siswa selesai (441 siswa dari 15 sheet Excel). M05 (Akademik): impor batch nilai selesai (5.420 record dari 15 sheet Excel).** Rev. 14 = dokumen PRD sebelumnya."""

new_rev16 = """> **Rev. 16 — 14 Oktober 2026 (WIB).** Sinkronisasi ulang dengan kondisi DB aktual (`dev.db` lewat `db_summary.py`): 1 user (role admin), 5 role, 0 role_permissions, **441 siswa (semua `inactive` — menunggu aktivasi)**, **18 kelas** (Takhosous + TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK), 54 guru (impor Excel), **32 mapel (impor Excel)**, **5.420 nilai (impor Excel)**, 0 record tabel kurikulum/akademik/lainnya. Build quality gate (terverifikasi ulang): `tsc --noEmit` ✓ (exit 0) + `npm run lint` ✓ (exit 0, 6 warning — tanpa error) + `npm run build` ✓ (exit 0). **M02a (NFC):** field `uid_nfc` **sudah ditambahkan** ke schema `prisma/schema.prisma` (kolom `uidNfc` dengan `@map("uid_nfc")`), `init_db.py` & `init_schema.sql` (kolom `uid_nfc TEXT`); namun `dev.db` **belum direkonstruksi** — kolom `uid_nfc` tidak terdaftar di tabel `students` aktual (dev.db dibuat 2026-10-14 02:51 WIB, sebelum perubahan schema). Rekonstruksi: `python3 init_db.py` → `init_schema.sql`. Mapping UID → NISN masih **belum diuji** (data ekspor NFC Tools belum ada). **M02 (Santri): impor batch siswa selesai (441 siswa dari 15 sheet Excel). M05 (Akademik): impor batch nilai selesai (5.420 record dari 15 sheet Excel).** **Perbaikan:** Komponen `Beranda` masih menampilkan placeholder statis (`totalSantri: 42`, `totalGuru: 27`, `totalKelas: 13`) yang tidak mencerminkan jumlah aktual `dev.db` (441 siswa, 54 guru, 18 kelas) — perlu sinkronisasi ke DB. Rev. 15 = dokumen PRD sebelumnya."""

if old_rev15 in content:
    content = content.replace(old_rev15, new_rev16)
    print("✓ Updated Rev. 15 → Rev. 16 (header)")
else:
    print("✗ Rev. 15 header not found")

# 2. Fix §8.1 folder name
old_folder = """`.data-pondokanat/` (folder asli bernama `data-pondokanat` - huruf 'k' tidak sengaja; PRD merujuk `.data-pondokanat/`). Pada tanggal revisi ini, folder berisi:"""

new_folder = """`.data-pondokanat/` (folder asli bernama `data-pondokanat` - huruf 'k' tidak sengaja; PRD merujuk `.data-pondokanat/`). Catatan: folder di sistem berisi `.data-pondokanat` (huruf 'k' memang ada di file sistem). Pada tanggal revisi ini, folder berisi:"""

if old_folder in content:
    content = content.replace(old_folder, new_folder)
    print("✓ Fixed folder name reference in §8.1")
else:
    print("✗ Folder name pattern not found in §8.1")

# 3. Update §9.1 M02a row (correct pattern: 2 pipes not 3)
old_m02a = """|| **M02a** | 🔧 In progress | Spec lengkap (§2.2); field `uid_nfc` tambahan di `prisma/schema.prisma` + `dev.db` (jika restart DB, jalankan `init_db.py` ulang) — mapping UID → NISN belum diuji | rumus parse: baris MANUFACTURER diapit `[]` → `AF:C2:99:E7` → update field `uid_nfc` di record siswa. Data UID kartu siswa masih tersimpan manual (tidak ada file ekspor terpisah). |"""

new_m02a = """||| **M02a** | 🔧 In progress | Spec lengkap (§2.2); field `uid_nfc` tambahan di `prisma/schema.prisma` (kolom `uidNfc`), `init_db.py` & `init_schema.sql`; **kolom belum terdaftar di dev.db aktual** — rekonstruksi DB: `python3 init_db.py` → `init_schema.sql`; mapping UID → NISN belum diuji | rumus parse: baris MANUFACTURER diapit `[]` → `AF:C2:99:E7` → update field `uid_nfc` di record siswa. Data UID kartu siswa masih tersimpan manual (tidak ada file ekspor terpisah). |"""

if old_m02a in content:
    content = content.replace(old_m02a, new_m02a)
    print("✓ Updated M02a row in §9.1")
else:
    print("✗ M02a row not found in §9.1")

# 4. Add Rev. 16 to §10.2 after the Rev. 15 entry
old_rev15_10 = """1. **Rev. 15 — 14 Oktober 2026 (WIB):** Sinkronisasi ulang ke `dev.db` aktual (status tidak berubah: 1 user, 5 role, 0 role_permissions, 441 siswa `inactive`, 18 kelas, 54 guru `active`, 32 mapel, 5.420 nilai, 0 record lainnya); build quality gate: `tsc --noEmit` ✓ + `npm run lint` ✓ + `npm run build` ✓. **M02a (NFC):** field `uid_nfc` **sudah ditambahkan** ke schema `prisma/schema.prisma` (kolom `uidNfc` dengan `@map(\"uid_nfc\")`); field juga ditambahkan ke script `init_db.py` & `init_schema.sql` (kolom `uid_nfc TEXT`); `dev.db` perlu direkonstruksi via `python3 init_db.py` (menggunakan `init_schema.sql`) sebelum kolom tersebut aktif. Mapping UID → NISN masih **belum diuji** (data ekspor NFC Tools belum ada). — *Catatan:* revisi sebelumnya merujuk tanggal 15 Oktober, diperbaiki ke 14 Oktober 2026 (WIB) mengikuti jam sistem."""

new_rev15_10 = """1. **Rev. 15 — 14 Oktober 2026 (WIB):** Sinkronisasi ulang ke `dev.db` aktual (status tidak berubah: 1 user, 5 role, 0 role_permissions, 441 siswa `inactive`, 18 kelas, 54 guru `active`, 32 mapel, 5.420 nilai, 0 record lainnya); build quality gate: `tsc --noEmit` ✓ + `npm run lint` ✓ + `npm run build` ✓. **M02a (NFC):** field `uid_nfc` **sudah ditambahkan** ke schema `prisma/schema.prisma` (kolom `uidNfc` dengan `@map("uid_nfc")`); field juga ditambahkan ke script `init_db.py` & `init_schema.sql` (kolom `uid_nfc TEXT`); `dev.db` perlu direkonstruksi via `python3 init_db.py` (menggunakan `init_schema.sql`) sebelum kolom tersebut aktif. Mapping UID → NISN masih **belum diuji** (data ekspor NFC Tools belum ada). — *Catatan:* revisi sebelumnya merujuk tanggal 15 Oktober, diperbaiki ke 14 Oktober 2026 (WIB) mengikuti jam sistem.

2. **Rev. 16 — 14 Oktober 2026 (WIB):** Sinkronisasi ulang dengan `db_summary.py`: 1 user, 5 role, 0 role_permissions, **441 siswa (semua `inactive`)**, **18 kelas**, 54 guru `active`, **32 mapel**, **5.420 nilai**, 0 record lainnya. Verifikasi ulang build quality gate: `tsc --noEmit` ✓ + `npm run lint` ✓ + `npm run build` ✓. **M02a (NFC) — koreksi:** field `uid_nfc` ditambahkan ke schema Prisma (`prisma/schema.prisma`), `init_db.py`, `init_schema.sql` (kolom `uid_nfc TEXT`), **TETAPI dev.db tidak direkonstruksi** — kolom `uid_nfc` tidak muncul di tabel `students` aktual (dev.db dibuat 02:51 WIB sebelum perubahan schema). Perlu `python3 init_db.py` untuk rekonstruksi. Mapping UID → NISN masih **belum diuji**. **Perbaikan Beranda:** placeholder `totalSantri: 42`, `totalGuru: 27`, `totalKelas: 13` masih hardcode — tidak mencerminkan jumlah aktual `dev.db` (441 siswa, 54 guru, 18 kelas). --->

2. **Rev. 16 — 14 Oktober 2026 (WIB):** Sinkronisasi ulang dengan `db_summary.py`: 1 user, 5 role, 0 role_permissions, **441 siswa (semua `inactive`)**, **18 kelas**, 54 guru `active`, **32 mapel**, **5.420 nilai**, 0 record lainnya. Verifikasi ulang build quality gate: `tsc --noEmit` ✓ + `npm run lint` ✓ + `npm run build` ✓. **M02a (NFC):** field `uid_nfc` ditambahkan ke schema Prisma (`prisma/schema.prisma`), `init_db.py`, `init_schema.sql` (kolom `uid_nfc TEXT`), **TETAPI dev.db tidak direkonstruksi** — kolom `uid_nfc` tidak muncul di tabel `students` aktual (dev.db dibuat 02:51 WIB sebelum perubahan schema). Perlu `python3 init_db.py` untuk rekonstruksi. Mapping UID → NISN masih **belum diuji**. **Perbaikan Beranda:** placeholder `totalSantri: 42`, `totalGuru: 27`, `totalKelas: 13` masih hardcoded — tidak mencerminkan jumlah aktual `dev.db` (441 siswa, 54 guru, 18 kelas)."""

if old_rev15_10 in content:
    content = content.replace(old_rev15_10, new_rev15_10)
    print("✓ Added Rev. 16 entry in §10.2")
else:
    print("✗ Rev. 15 entry in §10.2 not found")
    if "Rev. 15 — 14 Oktober 2026" in content:
        print("  (Rev. 15 found in §10.2)")

# Write the updated content
with open(path, 'w') as f:
    f.write(content)

print("\nDone.")
