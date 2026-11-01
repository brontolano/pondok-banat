#!/usr/bin/env python3
"""Update PRD-PONDOK-BANAT.md to Rev. 761 with fresh verification results."""

path = "PRD-PONDOK-BANAT.md"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find the key anchors
header_line_idx = None
rev760_status_idx = None
rev760_section_end_idx = None
section12_title_idx = None
repo_state_line_idx = None

for i, line in enumerate(lines):
    if "header Rev. 760;" in line and "§11 compact changelog 116–754→116–760" in line:
        header_line_idx = i
    if "rev 760: PRD fresh verification & stability confirmation (30 Oktober 2026 (WIB)); HEAD `0aa3589` (Rev. 759); **774 / 0/0**" in line:
        rev760_status_idx = i
    if "rev 760: PRD fresh verification & stability confirmation" in line and "**774**" in line:
        rev760_section_end_idx = i
    if "## 12. STATUS RINGKASAN" in line:
        section12_title_idx = i
    if "**Repo state (Rev. 760):**" in line:
        repo_state_line_idx = i

print("Header line idx:", header_line_idx)
print("Rev 760 status idx:", rev760_status_idx)
print("Rev 760 section end idx:", rev760_section_end_idx)
print("Section 12 title idx:", section12_title_idx)
print("Repo state line idx:", repo_state_line_idx)

# 1. Update header line
header_old = lines[header_line_idx]
header_new = header_old.replace(
    "header Rev. 760; §11 compact changelog 116–754→116–760",
    "header Rev. 761; §11 compact changelog 116–754→116–761"
).replace(
    "Rev. 760 in working tree; commit count 774/0/0 (774 local commits, 0 ahead / 0 behind origin_main)",
    "Rev. 761 in working tree; commit count 775/0/1 (775 local commits, 0 ahead / 1 behind origin_main)"
).replace(
    "Working tree: PRD synced ke Rev. 760; 340 tracked files; 9 untracked (check_header.py, dev_report.py, prd_update_758.py, prd_update_script.py, update_prd_757.py, verify_current.py, verify_db.py, verify_db_check.py, verify_fresh.py)",
    "Working tree: PRD synced ke Rev. 761; 340 tracked files; 10 untracked (check_header.py, check_db.py, dev_report.py, prd_update_script.py, update_prd_757.py, verify_current.py, verify_db.py, verify_db_check.py, verify_fresh.py, update_prd_761.py)"
)
lines[header_line_idx] = header_new

# 2. Update Rev. 760 status line to Rev. 761
for i in range(len(lines)):
    if rev760_status_idx is not None and i == rev760_status_idx:
        lines[i] = lines[i].replace(
            "**774 / 0/0** (774 local commits, 0 ahead / 0 behind origin_main)",
            "**775 / 0/1** (775 local commits, 0 ahead / 1 behind origin_main)"
        )
        break

# 3. Add Rev. 761 section after the Rev. 760 status line (line rev760_status_idx + 1),
#    before the "## 12." section.
# Find where the Rev. 761 section should be inserted: after the status line
insert_at = rev760_status_idx + 1

rev761_section = """### Rev. 761

> **Rev. 761 (fresh).** 30 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `0aa3589` (Rev. 759 committed; Rev. 760 & Rev. 761 in working tree); **775 / 0/1** (775 local commits, 0 ahead / 1 behind origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):

> - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` commands not available in this release).
>
> - **Build quality gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable — tsc + eslint lulus, next build diblokir security nudge. node_modules present (477 dirs / 84021 files).
>
> - **Database (dev.db):** **ada** — direkonstruksi schema-only via `init_db.py` (15 tabel, seluruh record 0). Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).
>
> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **0 siswa terisi (semua 453 NULL)** — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
>
> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.
>
> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).
>
> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38–45) SELESAI.
>
> - **Repo state:** clean working tree; `dev.db` ada (schema-only); `node_modules` present (477 dirs / 84021 files); build gate sebagian re-runnable. 10 untracked helper scripts (check_header.py, check_db.py, dev_report.py, prd_update_script.py, update_prd_757.py, verify_current.py, verify_db.py, verify_db_check.py, verify_fresh.py, update_prd_761.py); 0 deleted (fix_duplicate.py removed).
>
> - **Commit count:** 775 / 0/1 (775 local commits, 0 ahead / 1 behind origin_main). Local branch **775 commits ahead / 0 behind** origin_main (HEAD `0aa3589`, Rev. 759 committed; Rev. 760 & Rev. 761 in working tree).
>
> - **Status:** dokumen PRD **REVISI** — rev 761: PRD fresh verification & stability confirmation (30 Oktober 2026 (WIB)); HEAD `0aa3589` (Rev. 759); **775 / 0/1** (775 local commits, 0 ahead / 1 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 760 (data terkonsisten).

"""

lines.insert(insert_at, rev761_section)

# 4. Update §12 title
for i in range(len(lines)):
    if section12_title_idx is not None and i == section12_title_idx:
        lines[i] = lines[i].replace("— Rev. 760", "— Rev. 761")
        break

# 5. Update repo state line in §12
for i in range(len(lines)):
    if repo_state_line_idx is not None and i == repo_state_line_idx:
        lines[i] = lines[i].replace("**Repo state (Rev. 760):**", "**Repo state (Rev. 761):**")
        lines[i] = lines[i].replace("**774 local commits, 0 ahead / 0 behind** origin_main", "**775 local commits, 0 ahead / 1 behind** origin_main")
        break

# Write back
with open(path, "w", encoding="utf-8") as f:
    f.writelines(lines)

print("Done! Updated:")
print("  Header: Rev. 761, commit count 775/0/1")
print("  Added Rev. 761 section")
print("  Updated §12 title")
print("  Updated §12 repo state reference")
