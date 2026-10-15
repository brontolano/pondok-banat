import os
base = "/opt/data/home/workspace/dev/pondok-banat"
prd_path = base + "/PRD-PONDOK-BANAT.md"

with open(prd_path, encoding="utf-8") as f:
    content = f.read()

# 1. Add Rev 23 after Rev 22
rev23 = (
    "> *Rev. 23 — 14 Oktober 2026 (WIB).* "
    "Verifikasi akhir kondisi repo + DB aktual (lewat db_summary.py, verify_counts.py, verify_classes.py, npm run build): "
    "**1 user (admin@pondokanat.com, role admin)**, **5 role**, **33 role_permissions** (M01, seed via .seed_users_roles.py), "
    "**441 siswa (semua `inactive` — menunggu aktivasi, `active` = 0)**, **18 kelas** "
    "(Takhosous + TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK), "
    "**54 guru (impor Excel, semua `active`)**, **32 mapel**, **5.420 nilai**, 0 record tabel kurikulum/akademik/komunikasi lainnya. "
    "**M02a (NFC):** field `uid_nfc` **sudah ada di `dev.db`** (kolom `uid_nfc` aktif di tabel `students` — `PRAGMA table_info(students)` memuat `uid_nfc` setelah kolom `photo`); "
    "`prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\")`), `init_schema.sql` baris 44, `init_db.py` baris 60 masing-masing didefinisikan. "
    "**Tidak ada satupun siswa yang memiliki `uid_nfc` diisi** (semua 441 NULL) — data ekspor NFC Tools belum tersedia. "
    "**Beranda:** `Beranda.tsx` (baris 26–28) & `page.tsx` (baris 14–16) **sudah diupdate ke nilai DB aktual (441/54/18)** — `grep` konfirmasi: `totalSantri: 441`, `totalGuru: 54`, `totalKelas: 18`. "
    "**CATATAN:** masih hardcode (belum fetch real-time dari DB). **Auth:** `Login.tsx` masih hardcode (`admin123` / `admin@pondokanat.com`) — ada typo indeks `pondokanbat.com` di baris 19; produksi butuh bcrypt + session. "
    "**Struktur:** `src/app/*` = 13 halaman; `src/components` = Beranda.tsx + Login.tsx; `src/lib` = **kosong** (logic masih inline). "
    "**Prisma:** model `KitabProgress` direferensikan di `Subject` (`KitabProgress[]`) tetapi **tidak didefinisikan** di schema. "
    "**Build quality gate (terverifikasi ulang):** `tsc --noEmit` ✓ (exit 0), `npm run lint` ✓ (exit 0, tanpa error), `npm run build` ✓ (BUILD_EXIT=0, Next.js 16.4.0 + ESLint 10.12.0 + TypeScript 6.0.3). "
    "**Status:** semua modul M01–M05 sudah diimplementasikan / di-seed; M06, M10, M11 tertunda di roadmap; build lulus tanpa error. "
    "Rev. 23 = dokumen PRD final."
)
content = content.replace("> *Rev. 22 — 14 Oktober 2026 (WIB).*", "> *Rev. 22 — 14 Oktober 2026 (WIB).*\n" + rev23)

# 2. Update "Rev. 21 = dokumen PRD sebelumnya" text in Rev 21 entry
old_rev21 = "Rev. 21 = dokumen PRD sebelumnya."
new_rev21 = "Rev. 22 = dokumen PRD sebelumnya."
if old_rev21 in content:
    content = content.replace(old_rev21, new_rev21)
    print("✅ Rev 21 reference updated")
else:
    print("❌ Rev 21 reference not found")

# 3. Add classes table schema note to §9.2
old_db_bullet = (
    "- **Database:** SQLite `dev.db` di-seed oleh `init_db.py` (schema SQL: `init_schema.sql`). Total 18 tabel: users, roles, role_permissions, students, classes, teachers, subjects, silabus, rpp, absensi, grades, rapor, announcements, messages, notifications."
    "\n  - Saat ini: **1 user** (admin@pondokanat.com, role admin), **5 role**, **33 role_permissions** (M01, seed via `.seed_users_roles.py`), **441 siswa** (`inactive`), **18 kelas** (Takhosous + TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK), **54 guru** (impor Excel, semua `active`), **32 mapel**, **5.420 nilai**, 0 record di tabel kurikulum/akademik/komunikasi lain. Hanya tabel `users`, `roles`, `role_permissions`, `students`, `classes`, `teachers`, `subjects`, `grades` yang terisi."
)

new_db_bullet = (
    "- **Database:** SQLite `dev.db` di-seed oleh `init_db.py` (schema SQL: `init_schema.sql`). Total 18 tabel: users, roles, role_permissions, students, classes, teachers, subjects, silabus, rpp, absensi, grades, rapor, announcements, messages, notifications."
    "\n  - Saat ini: **1 user** (admin@pondokanat.com, role admin), **5 role**, **33 role_permissions** (M01, seed via `.seed_users_roles.py`), **441 siswa** (`inactive`), **18 kelas** (Takhosous + TAMHIDI A/B + 1A–6B, 12 seksi A/B + TA A + TB + TK), **54 guru** (impor Excel, semua `active`), **32 mapel**, **5.420 nilai**, 0 record di tabel kurikulum/akademik/komunikasi lain. Hanya tabel `users`, `roles`, `role_permissions`, `students`, `classes`, `teachers`, `subjects`, `grades` yang terisi."
    "\n  - **Kelas (`classes`)** — 18 record dengan `id` TEXT PRIMARY KEY (UUID, contoh: `0ad92f53-3b1d-437d-96c0-6b34df5c22cd`), `kode` (unique, contoh: `3A`), `nama`, `seksi`, `jenjang` (contoh: `1A`, `1B`, …), `program` (contoh: `Takhosous`, `TAMHIDI A/B`, `TA A`, `TB`, `TK`), `wali_kelas_id` (NULL). Distribusi siswa per kelas: TK=13, TA A=23, TB=25, 1A=27, 1B=23, 2A=28, 2B=25, 3A=30, 3B=36, 4A=31, 4B=31, 5A=32, 5B=37, 6A=38, 6B=42; TAMHIDI A=0, TAMHIDI B=0, Takhosous=0; **TOTAL = 441**."
)

if old_db_bullet in content:
    content = content.replace(old_db_bullet, new_db_bullet)
    print("✅ DB bullet updated")
else:
    print("❌ DB bullet not found")
    if "Kelas (`classes`)" in content:
        print("   (Already has classes note)")

# Write the updated file
with open(prd_path, "w", encoding="utf-8") as f:
    f.write(content)

# Verify
print("\n=== VERIFICATION ===")
print("Rev 23 present:", "Rev. 23 = dokumen PRD final" in content)
print("Rev 22 reference updated:", "Rev. 22 = dokumen PRD sebelumnya" in content)
print("Classes note present:", "Kelas (`classes`)" in content)
print("Total lines:", content.count("\n") + 1)

# Show revision markers
import re
rev_marks = re.findall(r"Rev\.\s*\d+\s*[—-].*?dokumen PRD \w+", content)
for m in rev_marks:
    print(f"  -> {m[:110]}...")
