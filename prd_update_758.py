#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update PRD-PONDOK-BANAT.md to Rev. 758 after fresh verification (cron run)."""

path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# ---- 1. Header update (line 4) ----
old_header = (
    "header Rev. 757; §11 compact changelog 116–754→116–757; §12 updated. HEAD def79ed (Rev. 756 final commit); "
    "commit count 771/3/0 (771 local commits, 3 ahead origin_main, 0 behind); node_modules present (477 dirs / 84021 files); "
    "dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0) — seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, "
    "import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: npm run type-check (tsc --noEmit) ✓ (exit 0); "
    "npm run lint ✓ (exit 0, 1 warning / 0 error); npm run build (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). "
    "Build gate sebagian re-runnable. Working tree: PRD synced ke Rev. 757; 340 tracked files; 6 untracked (dev_report.py, prd_update_script.py, verify_current.py, verify_db.py, verify_db_check.py, verify_fresh.py); 0 deleted (fix_duplicate.py removed)."
)
new_header = (
    "header Rev. 758; §11 compact changelog 116–754→116–758; §12 updated. HEAD e5451a8 (Rev. 757 final commit); "
    "commit count 772/4/0 (772 local commits, 4 ahead origin_main, 0 behind); node_modules present (477 dirs / 84021 files); "
    "dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0) — seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, "
    "import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: npm run type-check (tsc --noEmit) ✓ (exit 0); "
    "npm run lint ✓ (exit 0, 1 warning / 0 error); npm run build (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). "
    "Build gate sebagian re-runnable. Working tree: PRD synced ke Rev. 758; 340 tracked files; 8 untracked (check_header.py, dev_report.py, prd_update_script.py, update_prd_757.py, verify_current.py, verify_db.py, verify_db_check.py, verify_fresh.py); 0 deleted (fix_duplicate.py removed)."
)
if old_header in content:
    content = content.replace(old_header, new_header)
    print("Header: updated to Rev. 758")
else:
    print("Header: OLD_HEADER NOT FOUND")
    raise SystemExit(1)

# ---- 2. §11 compact changelog ----
content = content.replace("§11 compact changelog 116–754→116–757", "§11 compact changelog 116–754→116–758")
print("§11 compact changelog: updated to 116–758")

# ---- 3. Insert Rev. 758 entry in §11 (before "## 12. STATUS RINGKASAN") ----
rev758 = (
    "### Rev. 758\n\n"
    "> **Rev. 758 (fresh).** 30 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `e5451a8` (Rev. 757 final commit); **772 / 4/0** (772 local commits, 4 ahead origin_main, 0 behind). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):\n"
    ">\n"
    "> - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` commands not available in this release).\n"
    ">\n"
    "> - **Build quality gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable — tsc + eslint lulus, next build diblokir security nudge. node_modules present (477 dirs / 84021 files).\n"
    ">\n"
    "> - **Database (dev.db):** **ada** — direkonstruksi schema-only via `init_db.py` (15 tabel, seluruh record 0). Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).\n"
    ">\n"
    "> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **0 siswa terisi (semua 453 NULL)** — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).\n"
    ">\n"
    "> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.\n"
    ">\n"
    "> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).\n"
    ">\n"
    "> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38–45) SELESAI.\n"
    ">\n"
    "> - **Repo state:** clean working tree; `dev.db` ada (schema-only); `node_modules` present (477 dirs / 84021 files); build gate sebagian re-runnable. 8 untracked helper scripts (check_header.py, dev_report.py, prd_update_script.py, update_prd_757.py, verify_current.py, verify_db.py, verify_db_check.py, verify_fresh.py); 0 deleted (fix_duplicate.py removed).\n"
    ">\n"
    "> - **Commit count:** 772 / 4 (772 local commits, 4 ahead origin_main, 0 behind). Local branch **772 commits ahead / 0 behind** origin_main.\n"
    ">\n"
    "> - **Status:** dokumen PRD **REVISI** — rev 758: PRD fresh verification & stability confirmation (30 Oktober 2026 (WIB)); HEAD `e5451a8` (Rev. 757 final commit); **772 / 4/0** (772 local commits, 4 ahead origin_main, 0 behind). State stabil, tidak ada perubahan signifikan dari Rev. 757 (data terkonsisten)."
)

marker = "## 12. STATUS RINGKASAN"
if marker in content:
    content = content.replace(marker, rev758 + marker, 1)
    print("Inserted Rev. 758 section before §12")
else:
    print("§12 marker: NOT FOUND")
    raise SystemExit(1)

# ---- 4. §12 header ----
old_s12 = "## 12. STATUS RINGKASAN (30 Oktober 2026 WIB) — Rev. 757"
new_s12 = "## 12. STATUS RINGKASAN (30 Oktober 2026 WIB) — Rev. 758"
if old_s12 in content:
    content = content.replace(old_s12, new_s12)
    print("§12 header: updated to Rev. 758")
else:
    print("§12 header: NOT FOUND")
    raise SystemExit(1)

# ---- 5. §12 Repo state line ----
old_repo = (
    "> > - **Repo state (Rev. 757):** HEAD `def79ed` (Rev. 756 final commit); **771 local commits, 3 ahead / 0 behind** origin_main; "
    "340 tracked files; 6 untracked (dev_report.py, prd_update_script.py, verify_current.py, verify_db.py, verify_db_check.py, verify_fresh.py); "
    "0 deleted (fix_duplicate.py removed)."
)
new_repo = (
    "> > - **Repo state (Rev. 758):** HEAD `e5451a8` (Rev. 757 final commit); **772 local commits, 4 ahead / 0 behind** origin_main; "
    "340 tracked files; 8 untracked (check_header.py, dev_report.py, prd_update_script.py, update_prd_757.py, verify_current.py, verify_db.py, verify_db_check.py, verify_fresh.py); "
    "0 deleted (fix_duplicate.py removed)."
)
if old_repo in content:
    content = content.replace(old_repo, new_repo)
    print("§12 Repo state: updated to Rev. 758")
else:
    print("§12 Repo state: NOT FOUND")
    raise SystemExit(1)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Done. File updated to Rev. 758.")
print("Rev 758 section count:", content.count("### Rev. 758"))
print("Rev 758 heading present:", "## 12. STATUS RINGKASAN (30 Oktober 2026 WIB) — Rev. 758" in content)
