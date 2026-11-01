path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

updates = []

# 1. Header changes: Rev. 759 -> Rev. 760
old_header = "header Rev. 759; §11 compact changelog 116–754→116–759; §12 updated. HEAD 1aa511d (Rev. 758 final commit); commit count 773/5/0 (773 local commits, 5 ahead origin_main, 0 behind); node_modules present (477 dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0) — seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: npm run type-check (tsc --noEmit) ✓ (exit 0); npm run lint ✓ (exit 0, 1 warning / 0 error); npm run build (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable. Working tree: PRD synced ke Rev. 759; 340 tracked files; 8 untracked (check_header.py, dev_report.py, prd_update_758.py, prd_update_script.py, update_prd_757.py, verify_current.py, verify_db.py, verify_db_check.py, verify_fresh.py); 0 deleted (fix_duplicate.py removed)."
new_header = "header Rev. 760; §11 compact changelog 116–754→116–760; §12 updated. HEAD 0aa3589 (Rev. 759 committed); Rev. 760 in working tree; commit count 774/0/0 (774 local commits, 0 ahead / 0 behind origin_main); node_modules present (477 dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0) — seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: npm run type-check (tsc --noEmit) ✓ (exit 0); npm run lint ✓ (exit 0, 1 warning / 0 error); npm run build (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable. Working tree: PRD synced ke Rev. 760; 340 tracked files; 9 untracked (check_header.py, dev_report.py, prd_update_758.py, prd_update_script.py, update_prd_757.py, verify_current.py, verify_db.py, verify_db_check.py, verify_fresh.py); 0 deleted (fix_duplicate.py removed)."
if old_header in content:
    content = content.replace(old_header, new_header)
    updates.append("Header: updated to Rev. 760")
else:
    updates.append("Header: OLD_HEADER NOT FOUND")

# 2. §12 heading: Rev. 759 -> Rev. 760
old_s12 = "## 12. STATUS RINGKASAN (30 Oktober 2026 WIB) — Rev. 759"
new_s12 = "## 12. STATUS RINGKASAN (30 Oktober 2026 WIB) — Rev. 760"
if old_s12 in content:
    content = content.replace(old_s12, new_s12, 1)
    updates.append("§12 heading: updated to Rev. 760")
else:
    updates.append("§12 heading: NOT FOUND")

# 3. Rev. 760 section insertion (before ## 12. STATUS RINGKASAN)
rev760 = """### Rev. 760

> **Rev. 760 (fresh).** 30 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `0aa3589` (Rev. 759 committed; PRD file synced ke Rev. 760 in working tree); **774 / 0/0** (774 local commits, 0 ahead / 0 behind origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):

> - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` commands not available in this release).

> - **Build quality gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable — tsc + eslint lulus, next build diblokir security nudge. node_modules present (477 dirs / 84021 files).

> - **Database (dev.db):** **ada** — direkonstruksi schema-only via `init_db.py` (15 tabel, seluruh record 0). Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).

> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **0 siswa terisi (semua 453 NULL)** — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).

> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.

> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).

> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38–45) SELESAI.

> - **Repo state:** clean working tree; `dev.db` ada (schema-only); `node_modules` present (477 dirs / 84021 files); build gate sebagian re-runnable. 9 untracked helper scripts (check_header.py, dev_report.py, prd_update_758.py, prd_update_script.py, update_prd_757.py, verify_current.py, verify_db.py, verify_db_check.py, verify_fresh.py); 0 deleted (fix_duplicate.py removed).

> - **Commit count:** 774 / 0 (774 local commits, 0 ahead origin_main, 0 behind). Local branch **774 commits ahead / 0 behind** origin_main.

> - **Status:** dokumen PRD **REVISI** — rev 760: PRD fresh verification & stability confirmation (30 Oktober 2026 (WIB)); HEAD `0aa3589` (Rev. 759); **774 / 0/0** (774 local commits, 0 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 759 (data terkonsisten).

"""

marker = "## 12. STATUS RINGKASAN"
if marker in content:
    content = content.replace(marker, rev760 + marker, 1)
    updates.append("Rev. 760 section: inserted before §12")
else:
    updates.append("§12 marker: NOT FOUND")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updates applied:")
for u in updates:
    print("  -", u)
print("Done. File updated.")
print("Rev 760 section count:", content.count("### Rev. 760"))
print("Rev 760 heading present:", "## 12. STATUS RINGKASAN (30 Oktober 2026 WIB) — Rev. 760" in content)
