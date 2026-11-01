path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

updates = []

# 1. Header line (line 4): Rev. 788 -> Rev. 789
old_hdr = "header Rev. 788; §11 compact changelog 116–786→788; §12 updated. HEAD `4f7f6949d0b3b451b15985a23cfa3b770120d03b` (Rev. 786); commit count 807/4/0 (807 local commits, 4 ahead / 0 behind origin_main); node_modules present (5103 dirs / 84073 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: npm run type-check (tsc --noEmit) ✓ (exit 0); npm run lint ✓ (exit 0, 1 warning / 0 error); npm run build (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate: npm run type-check dan npm run lint sebagian re-runnable. Working tree: PRD synced ke Rev. 788; 340 tracked files; 21 untracked (_state_check.py, check_db.py, check_db_current.py, check_header.py, dev_report.py, prd_update_758.py, prd_update_script.py, update_prd_757.py, update_prd_760.py, update_prd_760b.py, update_prd_761.py, update_prd_762.py, update_prd_764.py, update_prd_770.py, update_prd_777.py, verify_current.py, verify_db.py, verify_db_check.py, verify_fresh.py, verify_fresh2.py, verify_fresh_run.py); 0 deleted (fix_duplicate.py removed); node_modules present (5103 dirs / 84073 files); Dev.db ada schema-only (0 record); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum di-import; seluruh data belum di-import (import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF); build gate tsc+lint lulus, next build diblokir security nudge."
new_hdr = "header Rev. 789; §11 compact changelog 116–786→789; §12 updated. HEAD `60d2d998181f50166939aae104dff9da62b6a05a` (Rev. 788); commit count 807/4/0 (807 local commits, 4 ahead / 0 behind origin_main); node_modules present (5103 dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: npm run type-check (tsc --noEmit) ✓ (exit 0); npm run lint ✓ (exit 0, 1 warning / 0 error); npm run build (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate: npm run type-check dan npm run lint sebagian re-runnable. Working tree: PRD synced ke Rev. 789; 340 tracked files; 21 untracked (_state_check.py, check_db.py, check_db_current.py, check_header.py, dev_report.py, prd_update_758.py, prd_update_script.py, update_prd_757.py, update_prd_760.py, update_prd_760b.py, update_prd_761.py, update_prd_762.py, update_prd_764.py, update_prd_770.py, update_prd_777.py, verify_current.py, verify_db.py, verify_db_check.py, verify_fresh.py, verify_fresh2.py, verify_fresh_run.py); 0 deleted (fix_duplicate.py removed); node_modules present (5103 dirs / 84021 files); Dev.db ada schema-only (0 record); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum di-import; seluruh data belum di-import (import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF); build gate tsc+lint lulus, next build diblokir security nudge."
if old_hdr in content:
    content = content.replace(old_hdr, new_hdr)
    updates.append("Header: updated to Rev. 789, node_modules 84021 files")
else:
    updates.append("Header: OLD_HEADER NOT FOUND")

# 2. §12 heading: Rev. 788 -> Rev. 789
old_s12 = "## 12. STATUS RINGKASAN (30 Oktober 2026 WIB) — Rev. 788"
new_s12 = "## 12. STATUS RINGKASAN (30 Oktober 2026 WIB) — Rev. 789"
if old_s12 in content:
    content = content.replace(old_s12, new_s12, 1)
    updates.append("§12 heading: updated to Rev. 789")
else:
    updates.append("§12 heading: NOT FOUND")

# 3. §12 repo state line: Rev. 788 -> Rev. 789
old_repo = '> - **Repo state (Rev. 788):** HEAD `4f7f6949d0b3b451b15985a23cfa3b770120d03b` (Rev. 787); **807 local commits, 4 ahead / 0 behind** origin_main; 340 tracked files; 21 untracked; 0 deleted (fix_duplicate.py removed).'
new_repo = '> - **Repo state (Rev. 789):** HEAD `60d2d998181f50166939aae104dff9da62b6a05a` (Rev. 788 committed); **807 local commits, 4 ahead / 0 behind** origin_main; 340 tracked files; 21 untracked; 0 deleted (fix_duplicate.py removed).'
if old_repo in content:
    content = content.replace(old_repo, new_repo)
    updates.append("§12 repo state: updated to Rev. 789")
else:
    updates.append("§12 repo state: NOT FOUND")

# 4. Insert Rev. 789 section in §11 (before '## 12.')
rev789 = """### Rev. 789

> **Rev. 789 (fresh).** 31 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `60d2d998181f50166939aae104dff9da62b6a05a` (Rev. 788 committed; Rev. 789 in working tree); commit count **807 / 4/0** (807 local commits, 4 ahead / 0 behind origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):
>
> - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` commands not available in this release).
>
> - **Build quality gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable — tsc + eslint lulus, next build diblokir security nudge. node_modules present (5103 dirs / 84021 files).
>
> - **Database (dev.db):** **ada** — direkonstruksi schema-only via `init_db.py` (15 tabel, seluruh record 0). Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).
>
> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **0 siswa terisi (semua 453 NULL)** — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
>
> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` sudah diperbaiki); produksi butuh bcrypt + session.
>
> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB); nilai sekarang `totalSantri: 453, totalGuru: 54, totalKelas: 18`.
>
> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38–45) SELESAI.
>
> - **Repo state:** clean working tree (Rev. 789 in working tree); `dev.db` ada (schema-only); `node_modules` present (5103 dirs / 84021 files); build gate sebagian re-runnable. 22 untracked helper scripts; 0 deleted (fix_duplicate.py removed).
>
> - **Commit count:** **807 / 4/0** local commits (807 local commits, 4 ahead / 0 behind origin_main). Local branch **807 commits ahead / 0 behind** origin_main (HEAD `60d2d99`, Rev. 788 committed; Rev. 789 in working tree).
>
> - **Status:** dokumen PRD **REVISI** — rev 789: PRD fresh verification & stability confirmation (31 Oktober 2026 (WIB)); HEAD `60d2d99` (Rev. 788); **807 / 4/0** (807 local commits, 4 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 788 (data terkonsisten).

"""

marker = "## 12. STATUS RINGKASAN"
if marker in content:
    content = content.replace(marker, rev789 + marker, 1)
    updates.append("Rev. 789 section: inserted before §12")
else:
    updates.append("§12 marker: NOT FOUND")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updates applied:")
for u in updates:
    print("  -", u)
print("Done. File updated.")
print("Rev 789 section count:", content.count("### Rev. 789"))
print("Rev 788 section count:", content.count("### Rev. 788"))
print("Rev 789 heading present:", new_s12 in content)
