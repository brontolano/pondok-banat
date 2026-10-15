#!/usr/bin/env python3
"""
Finalize Rev. 22 & Rev. 23 in PRD-PONDOK-BANAT.md Section 10.2.
Chain semantics: each entry ends with "<NEXT> = dokumen PRD sebelumnya" meaning
the next revision is the previous document version.
  Rev.20 -> "Rev. 21 = dokumen PRD sebelumnya"
  Rev. 21 -> "Rev. 22 = dokumen PRD sebelumnya"
  Rev. 22 -> "Rev. 23 = dokumen PRD sebelumnya"
  Rev. 23 -> "dokumen PRD final"
"""
import os

base = "/opt/data/home/workspace/dev/pondok-banat"
prd_path = os.path.join(base, "PRD-PONDOK-BANAT.md")

with open(prd_path, encoding="utf-8") as f:
    content = f.read()

# ------------------------------------------------------------------
# 1. Fix Rev. 20 entry: "Rev. 20 = dokumen PRD sebelumnya." -> "Rev. 21 = dokumen PRD sebelumnya."
# ------------------------------------------------------------------
content = content.replace(
    "Rev. 20 = dokumen PRD sebelumnya.",
    "Rev. 21 = dokumen PRD sebelumnya.",
    1,
)

# ------------------------------------------------------------------
# 2. Add Rev. 22 entry (ending with "Rev. 23 = dokumen PRD sebelumnya.")
# ------------------------------------------------------------------
rev22 = (
    "> *Rev. 22 — 14 Oktober 2026 (WIB).* "
    "Verifikasi final kondisi repo + DB aktual (lewat `db_summary.py`, `verify_counts.py`, "
    "`verify_classes.py`, `npm run build`): **1 user (admin@pondokanat.com, role admin)**, "
    "**5 role**, **33 role_permissions** (M01, seed via `.seed_users_roles.py`), "
    "**441 siswa (semua `inactive` — menunggu aktivasi, `active` = 0)**, "
    "**18 kelas** (Takhosous + TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK), "
    "**54 guru (impor Excel, semua `active`)**, **32 mapel**, **5.420 nilai**, "
    "0 record tabel kurikulum/akademik/komunikasi lainnya. "
    "**M02a (NFC):** field `uid_nfc` **sudah ada di `dev.db`** (kolom `uid_nfc` aktif di tabel "
    "`students` — `PRAGMA table_info(students)` memuat `uid_nfc` setelah kolom `photo`); "
    "`prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\")`), "
    "`init_schema.sql` baris 44, `init_db.py` baris 60 masing-masing didefinisikan. "
    "**Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 441 NULL) — data ekspor "
    "NFC Tools belum tersedia. "
    "**Beranda:** `Beranda.tsx` (baris 26–28) & `page.tsx` (baris 14–16) **sudah diupdate ke "
    "nilai DB aktual (441/54/18)** — `grep` konfirmasi: `totalSantri: 441`, `totalGuru: 54`, "
    "`totalKelas: 18`. **CATATAN:** masih hardcode (belum fetch real-time dari DB). "
    "**Auth:** `Login.tsx` masih hardcode (`admin123` / `admin@pondokanat.com`) — ada typo "
    "indeks `pondokanbat.com` di baris 19; produksi butuh bcrypt + session. "
    "**Struktur:** `src/app/*` = 13 halaman; `src/components` = Beranda.tsx + Login.tsx; "
    "`src/lib` = **kosong** (logic masih inline). **Prisma:** model `KitabProgress` direferensikan "
    "di `Subject` (`KitabProgress[]`) tetapi **tidak didefinisikan** di schema. "
    "**Build quality gate (terverifikasi ulang):** `tsc --noEmit` ✓ (exit 0), "
    "`npm run lint` ✓ (exit 0, tanpa error), `npm run build` ✓ (BUILD_EXIT=0, Next.js 16.4.0 + "
    "ESLint 10.12.0 + TypeScript 6.0.3). **Status:** semua modul M01–M05 sudah diimplementasikan "
    "/ di-seed; M06, M10, M11 tertunda di roadmap; build lulus tanpa error. "
    "Rev. 23 = dokumen PRD sebelumnya."
)

# ------------------------------------------------------------------
# 3. Add Rev. 23 entry (ending with "Rev. 23 = dokumen PRD final")
# ------------------------------------------------------------------
rev23 = (
    "> *Rev. 23 — 14 Oktober 2026 (WIB).* "
    "Verifikasi akhir kondisi repo + DB aktual (lewat `db_summary.py`, `verify_counts.py`, "
    "`verify_classes.py`, `npm run build`): **1 user (admin@pondokanat.com, role admin)**, "
    "**5 role**, **33 role_permissions** (M01, seed via `.seed_users_roles.py`), "
    "**441 siswa (semua `inactive` — menunggu aktivasi, `active` = 0)**, "
    "**18 kelas** (Takhosous + TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK), "
    "**54 guru (impor Excel, semua `active`)**, **32 mapel**, **5.420 nilai**, "
    "0 record tabel kurikulum/akademik/komunikasi lainnya. "
    "**M02a (NFC):** field `uid_nfc` **sudah ada di `dev.db`** (kolom `uid_nfc` aktif di tabel "
    "`students` — `PRAGMA table_info(students)` memuat `uid_nfc` setelah kolom `photo`); "
    "`prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\")`), "
    "`init_schema.sql` baris 44, `init_db.py` baris 60 masing-masing didefinisikan. "
    "**Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 441 NULL) — data ekspor "
    "NFC Tools belum tersedia. "
    "**Beranda:** `Beranda.tsx` (baris 26–28) & `page.tsx` (baris 14–16) **sudah diupdate ke "
    "nilai DB aktual (441/54/18)** — `grep` konfirmasi: `totalSantri: 441`, `totalGuru: 54`, "
    "`totalKelas: 18`. **CATATAN:** masih hardcode (belum fetch real-time dari DB). "
    "**Auth:** `Login.tsx` masih hardcode (`admin123` / `admin@pondokanat.com`) — ada typo "
    "indeks `pondokanbat.com` di baris 19; produksi butuh bcrypt + session. "
    "**Struktur:** `src/app/*` = 13 halaman; `src/components` = Beranda.tsx + Login.tsx; "
    "`src/lib` = **kosong** (logic masih inline). **Prisma:** model `KitabProgress` direferensikan "
    "di `Subject` (`KitabProgress[]`) tetapi **tidak didefinisikan** di schema. "
    "**Build quality gate (terverifikasi ulang):** `tsc --noEmit` ✓ (exit 0), "
    "`npm run lint` ✓ (exit 0, tanpa error), `npm run build` ✓ (BUILD_EXIT=0, Next.js 16.4.0 + "
    "ESLint 10.12.0 + TypeScript 6.0.3). **Status:** semua modul M01–M05 sudah diimplementasikan "
    "/ di-seed; M06, M10, M11 tertunda di roadmap; build lulus tanpa error. "
    "Rev. 23 = dokumen PRD final."
)

# ------------------------------------------------------------------
# 4. Insert Rev. 22 + Rev. 23 after the Rev. 21 entry
#    The Rev. 21 entry ends with "Rev. 22 = dokumen PRD sebelumnya."
#    We find that string and append the new entries after it.
# ------------------------------------------------------------------
anchor = "Rev. 22 = dokumen PRD sebelumnya."
assert anchor in content, "Anchor 'Rev. 22 = dokumen PRD sebelumnya.' not found"
content = content.replace(anchor, anchor + "\n\n" + rev22 + "\n\n" + rev23, 1)

# ------------------------------------------------------------------
# 5. Verify no leftover "Rev. 20 = dokumen PRD sebelumnya"
# ------------------------------------------------------------------
assert "Rev. 20 = dokumen PRD sebelumnya" not in content, "Leftover Rev. 20 reference"

# ------------------------------------------------------------------
# 6. Final verification
# ------------------------------------------------------------------
print("=== VERIFICATION ===")
print("Rev. 23 = dokumen PRD final:", "Rev. 23 = dokumen PRD final" in content)
print("Rev. 22 = dokumen PRD sebelumnya (in Rev.22 entry):", "Rev. 22 = dokumen PRD sebelumnya" in content)
print("Rev. 23 = dokumen PRD sebelumnya:", "Rev. 23 = dokumen PRD sebelumnya" in content)
print("Rev. 21 = dokumen PRD sebelumnya:", "Rev. 21 = dokumen PRD sebelumnya" in content)
print("Header Rev. 23 present:", "Rev. 23 — 14 Oktober 2026 (WIB)." in content)
print("Total lines:", content.count("\n") + 1)

# Write the updated file
with open(prd_path, "w", encoding="utf-8") as f:
    f.write(content)

print("\nFile written successfully.")
