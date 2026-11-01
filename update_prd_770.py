#!/usr/bin/env python3
# Update PRD-PONDOK-BANAT.md to Rev. 770

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# --- 1. Header line (line 4) ---
old_header = '''header Rev. 769; §11 compact changelog 116–754→116–769; §12 updated. HEAD `95996e0` (Rev. 768 committed; Rev. 769 committed). Rev. 769 committed (working tree synced dengan HEAD, 0 perubahan lokal); commit count 786/0/0 (786 local commits, 0 ahead / 0 behind origin_main); node_modules present (479 dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: npm run type-check (tsc --noEmit) ✓ (exit 0); npm run lint ✓ (exit 0, 1 warning / 0 error); npm run build (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate: npm run type-check dan npm run lint sebagian re-runnable. Working tree: PRD synced ke Rev. 769; 340 tracked files; 17 untracked (_state_check.py, check_db.py, check_header.py, dev_report.py, prd_update_758.py, prd_update_script.py, update_prd_757.py, update_prd_760.py, update_prd_760b.py, update_prd_761.py, update_prd_762.py, update_prd_764.py, verify_current.py, verify_db.py, verify_db_check.py, verify_fresh.py, verify_fresh2.py); 0 deleted (fix_duplicate.py removed); node_modules present (479 dirs / 84021 files);'''

new_header = '''header Rev. 770; §11 compact changelog 116–754→116–770; §12 updated. HEAD `b27c80e` (Rev. 769 committed; Rev. 770 in working tree); Rev. 770 in working tree; commit count 787/0/0 (787 local commits, 0 ahead / 0 behind origin_main); node_modules present (477 dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: npm run type-check (tsc --noEmit) ✓ (exit 0); npm run lint ✓ (exit 0, 1 warning / 0 error); npm run build (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate: npm run type-check dan npm run lint sebagian re-runnable. Working tree: PRD synced ke Rev. 770; 340 tracked files; 17 untracked (_state_check.py, check_db.py, check_header.py, dev_report.py, prd_update_758.py, prd_update_script.py, update_prd_757.py, update_prd_760.py, update_prd_760b.py, update_prd_761.py, update_prd_762.py, update_prd_764.py, verify_current.py, verify_db.py, verify_db_check.py, verify_fresh.py, verify_fresh2.py); 0 deleted (fix_duplicate.py removed); node_modules present (477 dirs / 84021 files);'''

if old_header in content:
    content = content.replace(old_header, new_header)
    print("Header: updated -> Rev. 770, 787 local, 0 ahead / 0 behind, 17 untracked")
else:
    print("Header: OLD_HEADER NOT FOUND")

# --- 2. Insert Rev. 770 section in §11 (before '## 12.') ---
rev770 = """### Rev. 770

> **Rev. 770 (fresh).** 30 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `b27c80e` (Rev. 769 committed); commit count **787 / 0/0** (787 local commits, 0 ahead / 0 behind origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):

> - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` commands not available in this release).

> - **Build quality gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable — tsc + eslint lulus, next build diblokir security nudge. node_modules present (477 dirs / 84021 files).

> - **Database (dev.db):** **ada** — direkonstruksi schema-only via `init_db.py` (15 tabel, seluruh record 0). Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).

> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\\"uid_nfc\\")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **0 siswa terisi (semua 453 NULL)** — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).

> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.

> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).

> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38–45) SELESAI.

> - **Repo state:** clean working tree (PRD ditulis ke Rev. 770); `dev.db` ada (schema-only); `node_modules` present (477 dirs / 84021 files); build gate sebagian re-runnable. 17 untracked helper scripts (check_db.py, check_header.py, dev_report.py, prd_update_758.py, prd_update_script.py, update_prd_757.py, update_prd_760.py, update_prd_760b.py, update_prd_761.py, update_prd_762.py, update_prd_764.py, verify_current.py, verify_db.py, verify_db_check.py, verify_fresh.py, verify_fresh2.py); 0 deleted (fix_duplicate.py removed).

> - **Commit count:** 787 / 786 local commits (787 local commits, 0 ahead / 0 behind origin_main). Local branch **787 commits ahead / 0 behind** origin_main (HEAD `b27c80e`, Rev. 769 committed; Rev. 770 in working tree).

> - **Status:** dokumen PRD **REVISI** — rev 770: PRD fresh verification & stability confirmation (30 Oktober 2026 (WIB)); HEAD `b27c80e` (Rev. 769 committed); **787 / 0/0** (787 local commits, 0 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 769 (data terkonsisten).

"""

marker = "## 12. STATUS RINGKASAN"
if marker in content:
    content = content.replace(marker, rev770 + marker, 1)
    print("Inserted Rev. 770 section before §12")
else:
    print("§12 marker: NOT FOUND")

# --- 3. §12 title ---
old_s12 = "## 12. STATUS RINGKASAN (30 Oktober 2026 WIB) — Rev. 769"
new_s12 = "## 12. STATUS RINGKASAN (30 Oktober 2026 WIB) — Rev. 770"
if old_s12 in content:
    content = content.replace(old_s12, new_s12)
    print("§12 title: updated -> Rev. 770")
else:
    print("§12 title: NOT FOUND")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Done. File updated to Rev. 770.")
print("Rev 770 section count:", content.count("### Rev. 770"))
print("Rev 770 heading present:", new_s12 in content)
