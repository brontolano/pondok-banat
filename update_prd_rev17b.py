#!/usr/bin/env python3
"""Update PRD to Rev. 17 - fix header (simple approach)."""

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r') as f:
    content = f.read()

# Find the Rev. line and replace the whole line
import re
# Match the entire Rev. line (line 4)
pattern = r'^> \*\*Rev\. 16 — 14 Oktober 2026 \(WIB\)\..*$'
replacement = '''> **Rev. 17 — 14 Oktober 2026 (WIB).** Sinkronisasi ulang dengan kondisi DB aktual (`dev.db` lewat `db_summary.py`): 1 user (role admin), 5 role, 0 role_permissions, **441 siswa (semua `inactive` — menunggu aktivasi)**, **18 kelas** (Takhosous + TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK), 54 guru (impor Excel), **32 mapel (impor Excel)**, **5.420 nilai (impor Excel)**, 0 record tabel kurikulum/akademik/komunikasi lainnya. Build quality gate (terverifikasi ulang): `tsc --noEmit` ✓ (exit 0) + `npm run lint` ✓ (exit 0, 6 warning — tanpa error) + `npm run build` ✓ (exit 0). **M02a (NFC):** field `uid_nfc` **sudah ditambahkan** ke schema `prisma/schema.prisma` (kolom `uidNfc` dengan `@map(\\"uid_nfc\\")`), `init_db.py` & `init_schema.sql` (kolom `uid_nfc TEXT`); namun `dev.db` **belum direkonstruksi** — kolom `uid_nfc` tidak terdaftar di tabel `students` aktual (dev.db dibuat 2026-10-14 02:51 WIB, sebelum perubahan schema). Rekonstruksi: `python3 init_db.py` → `init_schema.sql`. Mapping UID → NISN masih **belum diuji** (data ekspor NFC Tools belum ada). **Verifikasi Rev. 17:** Kolom `uid_nfc` memang ada di schema Prisma (line 68: `uidNfc String? @map(\\"uid_nfc\\")`) dan script init (init_schema.sql:44, init_db.py:60); `dev.db` (created 02:51) masih mengandung schema lama. **Struktur halaman:** `src/app/*` berisi 13 halaman; `src/components`: Beranda.tsx + Login.tsx; `src/lib` kosong (logic masih inline). **Perbaikan:** Komponen `Beranda` masih menampilkan placeholder statis (`totalSantri: 42`, `totalGuru: 27`, `totalKelas: 13`) yang tidak mencerminkan jumlah aktual `dev.db` (441 siswa, 54 guru, 18 kelas) — perlu sinkronisasi ke DB. Rev. 16 = dokumen PRD sebelumnya.'''

new_content = re.sub(pattern, replacement, content, count=1, flags=re.MULTILINE)

if new_content != content:
    with open(path, 'w') as f:
        f.write(new_content)
    print("Header updated: Rev. 16 -> Rev. 17")
else:
    print("WARNING: header pattern not found!")
    # Check if the pattern had issues
    m = re.search(r'^> \*\*Rev\. \d+ — 14 Oktober 2026.*$', content, flags=re.MULTILINE)
    if m:
        print("Found line:", m.group(0)[:100] + "...")
