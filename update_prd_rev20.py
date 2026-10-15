import re

path = 'PRD-PONDOK-BANAT.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Build the Rev. 20 verification summary
rev20 = """> **Rev. 20 — 14 Oktober 2026 (WIB).** Verifikasi akhir dari `dev.db` (lewat `db_summary.py`, `verify_counts.py`, `verify_detail.py`, `verify_classes.py`): **1 user (admin@pondokanat.com, role admin)**, **5 role**, **33 role_permissions** (M01, seed via `.seed_users_roles.py`), **441 siswa (semua `inactive` — menunggu aktivasi, `active` = 0)**, **18 kelas** (Takhosous + TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK), **54 guru (impor Excel, semua `active`)**, **32 mapel**, **5.420 nilai**, 0 record tabel kurikulum/akademik/komunikasi lainnya. **Siswa per kelas (diverifikasi):** TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosous=0; **TOTAL = 441**. **M02a (NFC):** field `uid_nfc` **sudah ada di `dev.db`** (kolom `uid_nfc` aktif di tabel `students` — `PRAGMA table_info(students)` memuat `uid_nfc`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map("uid_nfc")`), `init_schema.sql` baris 44, `init_db.py` baris 60 masing-masing didefinisikan. Mapping UID → NISN **belum diuji** (data ekspor NFC Tools belum ada — tersimpan manual, format `AF:C2:99:E7`). **Beranda:** `Beranda.tsx` (baris 26–28) & `page.tsx` (baris 14–16) **sudah diupdate ke nilai DB aktual (441/54/18)** — `grep` konfirmasi: `totalSantri: 441`, `totalGuru: 54`, `totalKelas: 18`. **Build quality gate (terverifikasi ulang):** `tsc --noEmit` ✓ (exit 0), `npm run lint` ✓ (exit 0, tanpa error), `npm run build` ✓ (BUILD_EXIT=0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). **Struktur:** `src/app/*` = 13 halaman; `src/components` = Beranda.tsx + Login.tsx; `src/lib` = kosong (logic masih inline). **Status:** semua modul M01–M05 sudah diimplementasikan / di-seed; M06, M10, M11 tertunda di roadmap; build lulus tanpa error. Rev. 19 = dokumen PRD sebelumnya."""

# Insert Rev. 20 after the Rev. 19 bullet (the block starts with "> **Rev. 19" and ends with "Rev. 18 = dokumen PRD sebelumnya.")
pattern = r'> \*\*Rev\. 19.*?\*\*Perbaikan:.*?Rev\. 18 = dokumen PRD sebelumnya\.'
replacement = rev20 + '\n\n'
content_new, count = re.subn(pattern, replacement, content, flags=re.DOTALL)

if count == 0:
    print("ERROR: Rev. 19 pattern not found!")
    print("--- SEARCHING ---")
    # Show the relevant section
    idx = content.find('Rev. 19')
    print(content[idx:idx+200] if idx != -1 else "Rev. 19 not found")
else:
    print(f"Replaced {count} occurrence(s)")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content_new)

print("File updated.")
print("Total lines:", content_new.count(chr(10)) + 1)
