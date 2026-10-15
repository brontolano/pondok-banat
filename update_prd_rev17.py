#!/usr/bin/env python3
"""Update PRD to Rev. 17 with current verified state (corrected)."""

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r') as f:
    content = f.read()

# ---- 1. Header: Rev. 16 -> Rev. 17 ----
old_header = """> **Rev. 16 — 14 Oktober 2026 (WIB).** Sinkronisasi ulang dengan kondisi DB aktual (`dev.db` lewat `db_summary.py`): 1 user (role admin), 5 role, 0 role_permissions, **441 siswa (semua `inactive` — menunggu aktivasi)**, **18 kelas** (Takhosous + TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK), 54 guru (impor Excel), **32 mapel (impor Excel)**, **5.420 nilai (impor Excel)**, 0 record tabel kurikulum/akademik/lainnya. Build quality gate (terverifikasi ulang): `tsc --noEmit` ✓ (exit 0) + `npm run lint` ✓ (exit 0, 6 warning — tanpa error) + `npm run build` ✓ (exit 0). **M02a (NFC):** field `uid_nfc` **sudah ditambahkan** ke schema `prisma/schema.prisma` (kolom `uidNfc` dengan `@map(\\"uid_nfc\\")`), `init_db.py` & `init_schema.sql` (kolom `uid_nfc TEXT`); namun `dev.db` **belum direkonstruksi** — kolom `uid_nfc` tidak terdaftar di tabel `students` aktual (dev.db dibuat 2026-10-14 02:51 WIB, sebelum perubahan schema). Rekonstruksi: `python3 init_db.py` → `init_schema.sql`. Mapping UID → NISN masih **belum diuji** (data ekspor NFC Tools belum ada). **M02 (Santri): impor batch siswa selesai (441 siswa dari 15 sheet Excel). M05 (Akademik): impor batch nilai selesai (5.420 record dari 15 sheet Excel).** **Perbaikan:** Komponen `Beranda` masih menampilkan placeholder statis (`totalSantri: 42`, `totalGuru: 27`, `totalKelas: 13`) yang tidak mencerminkan jumlah aktual `dev.db` (441 siswa, 54 guru, 18 kelas) — perlu sinkronisasi ke DB. Rev. 15 = dokumen PRD sebelumnya."""

new_header = """> **Rev. 17 — 14 Oktober 2026 (WIB).** Sinkronisasi ulang dengan kondisi DB aktual (`dev.db` lewat `db_summary.py`): 1 user (role admin), 5 role, 0 role_permissions, **441 siswa (semua `inactive` — menunggu aktivasi)**, **18 kelas** (Takhosous + TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK), 54 guru (impor Excel), **32 mapel (impor Excel)**, **5.420 nilai (impor Excel)**, 0 record tabel kurikulum/akademik/komunikasi lainnya. Build quality gate (terverifikasi ulang): `tsc --noEmit` ✓ (exit 0) + `npm run lint` ✓ (exit 0, 6 warning — tanpa error) + `npm run build` ✓ (exit 0). **M02a (NFC):** field `uid_nfc` **sudah ditambahkan** ke schema `prisma/schema.prisma` (kolom `uidNfc` dengan `@map(\\"uid_nfc\\")`), `init_db.py` & `init_schema.sql` (kolom `uid_nfc TEXT`); namun `dev.db` **belum direkonstruksi** — kolom `uid_nfc` tidak terdaftar di tabel `students` aktual (dev.db dibuat 2026-10-14 02:51 WIB, sebelum perubahan schema). Rekonstruksi: `python3 init_db.py` → `init_schema.sql`. Mapping UID → NISN masih **belum diuji** (data ekspor NFC Tools belum ada). **Verifikasi Rev. 17:** Kolom `uid_nfc` memang ada di schema Prisma (line 68: `uidNfc String? @map(\\"uid_nfc\\")`) dan script init (init_schema.sql:44, init_db.py:60); `dev.db` (created 02:51) masih mengandung schema lama. **Struktur halaman:** `src/app/*` berisi 13 halaman; `src/components`: Beranda.tsx + Login.tsx; `src/lib` kosong (logic masih inline). **Perbaikan:** Komponen `Beranda` masih menampilkan placeholder statis (`totalSantri: 42`, `totalGuru: 27`, `totalKelas: 13`) yang tidak mencerminkan jumlah aktual `dev.db` (441 siswa, 54 guru, 18 kelas) — perlu sinkronisasi ke DB. Rev. 16 = dokumen PRD sebelumnya."""

if old_header in content:
    content = content.replace(old_header, new_header)
    print("Header updated: Rev. 16 -> Rev. 17")
else:
    print("WARNING: header pattern not found! Checking...")
    # Find the Rev. line
    import re
    m = re.search(r'> \*\*Rev\. \d+ — 14 Oktober 2026', content)
    if m:
        print("Found:", m.group(0))

# ---- 2. M02a row (already updated, no-op) ----
# The row was already updated in the previous run; verify it

# ---- 3. Notes: update ---
old_notes = """> **Catatan:** Komponen `Beranda` masih menampilkan placeholder statis (`totalSantri: 42`, `totalGuru: 27`) yang **tidak mencerminkan jumlah aktual** di `dev.db` — `dev.db` berisi **441 siswa (semua `inactive`)**, **54 guru (semua `active`)**, **18 kelas**. Placeholder `totalSantri`/`totalGuru` tetap hardcode dan akan disinkronkan ke DB di iterasi berikutnya."""

new_notes = """> **Catatan:** Komponen `Beranda` masih menampilkan placeholder statis (`totalSantri: 42`, `totalGuru: 27`, `totalKelas: 13`) yang **tidak mencerminkan jumlah aktual** di `dev.db` — `dev.db` berisi **441 siswa (semua `inactive`)**, **54 guru (semua `active`)**, **18 kelas**. Placeholder `totalSantri`/`totalGuru`/`totalKelas` masih hardcode dan akan disinkronisasi ke DB di iterasi berikutnya. Verifikasi Rev. 17: kode sudah dibaca (Beranda.tsx lines 12-18) — placeholder tetap `setTimeout` hardcode, tidak ada API fetch ke DB.

> **Catatan Struktur:** `src/app/*` berisi 13 halaman (beranda, berita, kelas, guru, absensi, laporan, login, nilai, pengasuh, ruang-kegiatan, santri, sekolah + layout/page); `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (semua logic masih inline di komponen). `prisma/schema.prisma` (line 68) mendefinisikan field `uidNfc` @map(`\"uid_nfc\"`) pada model `Student`.

> **Catatan Prisma:** model `KitabProgress` hanya direferensikan di `Subject` (`KitabProgress[]`) tetapi **tidak didefinisikan** di schema; perlu ditambahkan jika fitur progress kitab akan dibangun.

> **Catatan keamanan:** Autentikasi saat ini hardcode — email `admin@pondokanat.com` / password `admin123` terekam di `src/components/Login.tsx`. Ini hanya untuk demo; sebelum production wajib diganti dengan bcrypt + session management yang aman (lihat backlog §9.3).

> **Kualitas build (quality gate) — 14 Oktober 2026 (WIB):** — diverifikasi langsung dari repo, seluruh gate lulus:
> - `tsc --noEmit` ✓ (lulus, exit 0; TypeScript 6.0.3)
> - `npm run lint` ✓ (`eslint .` lulus, exit 0; ESLint 10.12.0, flat config `eslint.config.mjs` + `eslint-config-next`; Next.js 16 menghapus `next lint`)
> - `npm run build` ✓ (`next build` selesai, exit 0; Next.js 16.4.0)"""

if old_notes in content:
    content = content.replace(old_notes, new_notes)
    print("Notes updated")
else:
    print("WARNING: notes pattern not found! Checking...")
    # Find the notes
    import re
    m = re.search(r'> \*\*Catatan\*\*: Komponen `Beranda`', content)
    if m:
        print("Found: ...")

# ---- 4. §10.2: add Rev. 17 entry ----
old_rev16 = """- Nama file folder asli adalah `Pdf had mata pelajaran` (tiap spasi). Tidak ada masalah."""

new_rev16 = """- Nama file folder asli adalah `Pdf had mata pelajaran` (tiap spasi). Tidak ada masalah.

### 10.3 Perubahan Rev. 17 (14 Oktober 2026 WIB)

Verifikasi langsung dari repo + dev.db:

1. **Verifikasi DB (via db_summary.py):** 1 user, 5 role, 0 role_permissions, **441 siswa (semua `inactive`)**, **18 kelas** (Takhosous + TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK), 54 guru (impor Excel, semuanya `active`), **32 mapel**, **5.420 nilai**, 0 record tabel kurikulum/akademik/komunikasi lain. — *Khusus siswa per kelas:* TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosous=0.
2. **M02a (NFC):** Verifikasi kolom `uid_nfc`:
   - `prisma/schema.prisma` line 68: `uidNfc String? @map(\\"uid_nfc\\")` ✓
   - `init_schema.sql` line 44: `uid_nfc TEXT, -- NFC card UID: 'AF:C2:99:E7'` ✓
   - `init_db.py` line 60: `uid_nfc TEXT, -- NFC card UID: 'AF:C2:99:E7'` ✓
   - `dev.db` (created 2026-10-14 02:51 WIB): **kolom `uid_nfc` TIDAK terkunci** — schema dev.db adalah versi lama (dibuat sebelum perubahan schema). Perlu `python3 init_db.py` → `init_schema.sql` untuk rekonstruksi.
3. **Beranda placeholder:** Beranda.tsx (lines 12-18) masih hardcode `totalSantri: 42`, `totalGuru: 27`, `totalKelas: 13` — tidak me-reflect ke DB. Perlu sinkronisasi ke DB (fetch real counts).
4. **Struktur kode:** `src/app/*` = 13 halaman; `src/components` = Beranda.tsx + Login.tsx; `src/lib` = kosong (logic inline). Prisma schema (line 68) mendefinisikan `uidNfc` @map(`\"uid_nfc\"`) pada model `Student`.
5. **Build quality gate:** `tsc --noEmit` ✓ + `npm run lint` ✓ + `npm run build` ✓ (semua lulus, exit 0).

*Catatan:* revisi sebelumnya merujuk tanggal 15 Oktober, diperbaiki ke 14 Oktober 2026 (WIB) mengikuti jam sistem."""

if old_rev16 in content:
    content = content.replace(old_rev16, new_rev16)
    print("§10.2 entry added")
else:
    print("WARNING: §10.2 pattern not found! Checking...")
    m = re.search(r'Nama file folder asli adalah `Pdf had mata pelajaran`', content)
    if m:
        print("Found: ...")

with open(path, 'w') as f:
    f.write(content)

print("PRD updated to Rev. 17")
