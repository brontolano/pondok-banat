#!/usr/bin/env python3
"""Complete the PRD update: add Rev 19 & Rev 20 to section 10.2, remove duplicate 10.3."""
import re

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# ============================================================
# 1. Update Section 10.2 header: Rev 15 -> Rev 15-20
# ============================================================
content = content.replace(
    '### 10.2 Perubahan Rev. 15 (14 Oktober 2026 WIB) + Penamaan',
    '### 10.2 Perubahan Rev. 15–20 (14 Oktober 2026 WIB)'
)

# ============================================================
# 2. Add Rev. 19 entry after Rev. 18 (before the "Nama file folder" line)
# ============================================================
rev19 = """4. **Rev. 19 — 14 Oktober 2026 (WIB):** Sinkronisasi Beranda ke nilai DB aktual: `Beranda.tsx` (baris 26–28) & `page.tsx` (baris 14–16) diupdate ke nilai DB aktual (`totalSantri: 441`, `totalGuru: 54`, `totalKelas: 18`). `grep` konfirmasi: `totalSantri: 441`, `totalGuru: 54`, `totalKelas: 18`. — *Catatan:* revisi sebelumnya merujuk `Beranda.tsx` lines 12-18, diperbaiki ke lines 26-28 (atau `page.tsx` lines 14-16) mengikuti lokasi aktual di codebase.

""" + "".join([
    "1. **Verifikasi DB:** 1 user (admin@pondokanat.com, role admin), **5 role**, **33 role_permissions** (M01, seed via `.seed_users_roles.py`), **441 siswa (semua `inactive`)**, **18 kelas** (Takhosous + TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK), 54 guru (impor Excel, semua `active`), **32 mapel**, **5.420 nilai**, 0 record tabel kurikulum/akademik/komunikasi lain. — *Khusus siswa per kelas:* TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosous=0.\n",
]) + """

5. **Beranda placeholder:** `Beranda.tsx` (baris 26–28) & `page.tsx` (baris 14–16) **sudah diupdate** ke nilai DB aktual (441/54/18) — `grep` konfirmasi: `totalSantri: 441`, `totalGuru: 54`, `totalKelas: 18`. Perlu sinkronisasi ke DB (fetch real counts) untuk iterasi berikutnya.\n
6. **Struktur kode:** `src/app/*` = 13 halaman; `src/components` = Beranda.tsx + Login.tsx; `src/lib` = kosong (logic inline). Prisma schema (line 68) mendefinisikan `uidNfc` @map(`\"uid_nfc\"`) pada model `Student`.\n
7. **Build quality gate:** `tsc --noEmit` ✓ + `npm run lint` ✓ + `npm run build` ✓ (semua lulus, exit 0).\n
"""

# Insert Rev. 19 after Rev. 18 (before "Nama file folder asli")
if 'Nama file folder asli' in content:
    # Replace the "Nama file folder asli" line with Rev. 19 + that line
    content = content.replace(
        '- Nama file folder asli adalah `Pdf had mata pelajaran` (tiap spasi). Tidak ada masalah.',
        rev19 + '- Nama file folder asli adalah `Pdf had mata pelajaran` (tiap spasi). Tidak ada masalah.'
    )
    print("Inserted Rev. 19 OK")
else:
    print("ERROR: 'Nama file folder asli' not found!")

# ============================================================
# 3. Add Rev. 20 entry after Rev. 19 (before "### 10.3")
# ============================================================
rev20 = """5. **Rev. 20 — 14 Oktober 2026 (WIB).** Verifikasi akhir dari `dev.db` (lewat `db_summary.py`, `verify_counts.py`, `verify_detail.py`, `verify_classes.py`): **1 user (admin@pondokanat.com, role admin)**, **5 role**, **33 role_permissions** (M01, seed via `.seed_users_roles.py`), **441 siswa (semua `inactive` — menunggu aktivasi, `active` = 0)**, **18 kelas** (Takhosous + TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK), **54 guru (impor Excel, semua `active`)**, **32 mapel**, **5.420 nilai**, 0 record tabel kurikulum/akademik/komunikasi lainnya. **Siswa per kelas (diverifikasi):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosous=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` **sudah ada di `dev.db`** (kolom `uid_nfc` aktif di tabel `students` — `PRAGMA table_info(students)` memuat `uid_nfc`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\")`), `init_schema.sql` baris 44, `init_db.py` baris 60 masing-masing didefinisikan. Mapping UID → NISN **belum diuji** (data ekspor NFC Tools belum ada — tersimpan manual, format `AF:C2:99:E7`). **Beranda:** `Beranda.tsx` (baris 26–28) & `page.tsx` (baris 14–16) **sudah diupdate ke nilai DB aktual (441/54/18)** — `grep` konfirmasi: `totalSantri: 441`, `totalGuru: 54`, `totalKelas: 18`. **Build quality gate (terverifikasi ulang):** `tsc --noEmit` ✓ (exit 0), `npm run lint` ✓ (exit 0, tanpa error), `npm run build` ✓ (BUILD_EXIT=0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Struktur:** `src/app/*` = 13 halaman; `src/components` = Beranda.tsx + Login.tsx; `src/lib` = kosong (logic masih inline). **Status:** semua modul M01–M05 sudah diimplementasikan / di-seed; M06, M10, M11 tertunda di roadmap; build lulus tanpa error. Rev. 19 = dokumen PRD sebelumnya.

"""

# Insert Rev. 20 after Rev. 19 (before "### 10.3")
if '### 10.3 Perubahan Rev. 17' in content:
    # First remove the duplicate section 10.3 (which is just Rev. 17 content)
    # Find the section 10.3 start
    idx_103 = content.find('### 10.3 Perubahan Rev. 17')
    # Find the end of section 10.3 (the line before "---")
    idx_dash = content.find('---\n> *Rev. 14', idx_103)
    if idx_dash != -1:
        # Remove from 10.3 start to the dash before footer
        content = content[:idx_103] + content[idx_dash:]
        print("Removed duplicate section 10.3 OK")
    
    # Now insert Rev. 20 after Rev. 19
    # Find the last "7. **Build quality gate**" in section 10.2 (end of Rev. 18)
    # and add Rev. 20 after Rev. 19 (which we just added)
    # Actually, let's insert Rev. 20 after the Rev. 19 block we added
    # The Rev. 19 block ends with "7. **Build quality gate:** ... (semua lulus, exit 0).\n"
    rev20_insert = rev20 + '\n'
    content = content.replace(
        '7. **Build quality gate:** `tsc --noEmit` ✓ + `npm run lint` ✓ + `npm run build` ✓ (semua lulus, exit 0).\n\n- Nama file folder asli',
        '7. **Build quality gate:** `tsc --noEmit` ✓ + `npm run lint` ✓ + `npm run build` ✓ (semua lulus, exit 0).\n' + rev20_insert + '- Nama file folder asli'
    )
    print("Inserted Rev. 20 OK")
else:
    print("ERROR: '### 10.3 Perubahan Rev. 17' not found!")

# ============================================================
# 4. Update header: Rev. 20 = dokumen PRD sebelumnya
# ============================================================
content = content.replace(
    'Rev. 19 = dokumen PRD sebelumnya.',
    'Rev. 20 = dokumen PRD sebelumnya.'
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("File updated.")
print("Total lines:", content.count(chr(10)) + 1)
