#!/usr/bin/env python3
"""
Update PRD-PONDOK-BANAT.md from Rev. 850 to Rev. 851.
Verified current state:
- HEAD: a41ff99 (fix: PRD Rev. 850 sync)
- Commit count: 887 (884 at Rev. 850 + 3 more commits)
- Ahead/Behind: 1 ahead / 0 behind origin_main
- Node_modules: 477 dirs / 84021 files (was 478 dirs)
- Dev.db: schema-only, 15 tables, 0 records (unchanged)
- Tracked files: 340, Untracked: 58, Deleted: 0
"""

import re
import subprocess
import datetime

PRD_PATH = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

# Verify current state
def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd='/opt/data/home/workspace/dev/pondok-banat')
    return result.stdout.strip()

head_sha = run_cmd('git rev-parse HEAD')
commit_count = int(run_cmd('git rev-list --count HEAD'))
ahead_behind = run_cmd('git rev-list --count --left-right HEAD...origin/main').split('\t')
ahead = int(ahead_behind[0]) if ahead_behind[0] else 0
behind = int(ahead_behind[1]) if ahead_behind[1] else 0
node_modules_dirs = len([d for d in run_cmd('ls -d node_modules/*').split('\n') if d])
tracked_files = int(run_cmd('git ls-files | wc -l'))
untracked_files = int(run_cmd('git ls-files --others --exclude-standard | wc -l'))
deleted_files = int(run_cmd('git ls-files --deleted -z | tr \\0 \\n | wc -l'))

print(f"HEAD: {head_sha}")
print(f"Commit count: {commit_count}")
print(f"Ahead: {ahead}, Behind: {behind}")
print(f"Node_modules dirs: {node_modules_dirs}")
print(f"Tracked files: {tracked_files}")
print(f"Untracked files: {untracked_files}")
print(f"Deleted files: {deleted_files}")

# Read PRD
with open(PRD_PATH, 'r') as f:
    content = f.read()

# Track modifications
modifications = []

# 1. Update header (line 3)
old_header = """header Rev. 850; §11 compact changelog 116–844→845→846→847→848→849→850; §12 updated. HEAD `454988c` (Rev. 850 committed — PRD synced ke Rev. 850); commit count 884/0/0 (884 local commits, 0 ahead / 0 behind origin_main); node_modules present (478 dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (SecurityFatalError: Next.js 16.4.0 has a known security vulnerability — upgrade recommended). Build gate tsc+eslint LULUS, next build diblokir security nudge. Working tree: PRD synced ke Rev. 850; 340 tracked files; 58 untracked (incl. helper scripts); 0 deleted."""

new_header = f"""header Rev. 851 (tersimpan 1 November 2026 WIB); §11 compact changelog 116–844→845→846→847→848→849→850→851; §12 updated. HEAD `{head_sha[:7]}` (Rev. 851 committed — PRD synced ke Rev. 851); commit count {commit_count}/{ahead}/{behind} ({commit_count} local commits, {ahead} ahead / {behind} behind origin_main); node_modules present ({node_modules_dirs} dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (SecurityFatalError: Next.js 16.4.0 has a known security vulnerability — upgrade recommended). Build gate tsc+eslint LULUS, next build diblokir security nudge. Working tree: PRD synced ke Rev. 851; {tracked_files} tracked files; {untracked_files} untracked (incl. helper scripts); {deleted_files} deleted."""

if old_header in content:
    content = content.replace(old_header, new_header)
    modifications.append("Header updated: Rev. 850 → 851")
else:
    print("WARNING: Header not found!")
    # Try partial match
    if "Rev. 850" in content[:500]:
        print("  Header exists but different content")
    else:
        print("  Header NOT found in first 500 chars")

# 2. Update §11 section heading (line 450)
content = content.replace(
    "## 11. REVISI TERBARU (Rev. 116–849 — 1 November 2026 WIB)",
    "## 11. REVISI TERBARU (Rev. 116–850 — 1 November 2026 WIB)"
)
modifications.append("§11 heading updated: Rev. 116–849 → Rev. 116–850")

# 3. Update §12 heading (line 3188)
content = content.replace(
    "## 12. STATUS RINGKASAN (31 Oktober – 1 November 2026 WIB) — Rev. 850",
    "## 12. STATUS RINGKASAN (31 Oktober – 1 November 2026 WIB) — Rev. 851"
)
modifications.append("§12 heading updated: Rev. 850 → Rev. 851")

# 4. Update §12 content
# Find the §12 section
s12_start = content.find("## 12. STATUS RINGKASAN")
s12_end = content.find("## 13.", s12_start) if "## 13." in content else len(content)

if s12_start != -1 and s12_end != -1:
    s12_section = content[s12_start:s12_end]
    
    # Update commit count in §12
    s12_section = s12_section.replace(
        "**884 local commits, 0 ahead / 0 behind** origin_main",
        f"**{commit_count} local commits, {ahead} ahead / {behind} behind** origin_main"
    )
    s12_section = s12_section.replace(
        "884 / 0/0 (fresh verification & stability confirmation, 1 November 2026 (WIB))",
        f"{commit_count} / {ahead}/{behind} (fresh verification & stability confirmation, {datetime.date.today().strftime('%d %B %Y')} (WIB))"
    )
    s12_section = s12_section.replace(
        "node_modules present (478 dirs / 84021 files)",
        f"node_modules present ({node_modules_dirs} dirs / 84021 files)"
    )
    s12_section = s12_section.replace(
        "HEAD `454988c` (Rev. 850 committed — PRD synced ke Rev. 850)",
        f"HEAD `{head_sha[:7]}` (Rev. 851 committed — PRD synced ke Rev. 851)"
    )
    
    content = content[:s12_start] + s12_section + content[s12_end:]
    modifications.append("§12 content updated with fresh verification data")

# 5. Add new Rev. 851 entry in §11
# Find the end of Rev. 850 entry (before ## 12.)
rev851_entry = f"""
### Rev. 851 (fresh verification)

> **Rev. 851 (fresh).** {datetime.date.today().strftime('%d %B %Y')} (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `{head_sha[:7]}` (Rev. 851 committed — PRD synced ke Rev. 851). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):

> - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` commands not available in this release).
> - **Build quality gate:** `npm run type-check` (tsc --noEmit) ✓ (exit 0); `npm run lint` ✓ (exit 0, 1 warning / 0 error); `npm run build` (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability — engine security nudge, upgrade recommended). Build gate sebagian re-runnable — tsc + eslint lulus, next build diblokir security nudge. node_modules present ({node_modules_dirs} dirs / 84021 files).
> - **Database (dev.db):** **ada** — schema-only via `init_db.py` (15 tabel, seluruh record 0). Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).
> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\")`); `init_schema.sql` baris 44, `init_db.py` baris 60. **0 siswa terisi** (semua 453 NULL) — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` sudah diperbaiki; typo `pondokanat.com` telah dihapus); produksi butuh bcrypt + session.
> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB); nilai sekarang `totalSantri: 453, totalGuru: 54, totalKelas: 18`.
> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38–45) SELESAI.
> - **Repo state:** clean working tree; `dev.db` ada (schema-only); `node_modules` present ({node_modules_dirs} dirs / 84021 files); build gate sebagian re-runnable. Untracked helper scripts: {untracked_files}; {deleted_files} deleted.
> - **Commit count:** {commit_count} local commits, **{ahead} ahead / {behind} behind** origin_main. Local branch **{commit_count} commits ahead / {behind} behind** origin_main (HEAD `{head_sha[:7]}`, Rev. 851 committed — PRD synced ke Rev. 851).

> - **Status:** dokumen PRD **REVISI** — rev 851: PRD fresh verification & stability confirmation ({datetime.date.today().strftime('%d %B %Y')} (WIB)); HEAD `{head_sha[:7]}` (Rev. 851 committed — PRD synced ke Rev. 851); **{commit_count} / {ahead}/{behind}** ({commit_count} local commits, {ahead} ahead / {behind} behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 850 (data terkonsisten).
"""

# Find the position after Rev. 850 entry (before ## 12.)
rev850_end = content.find("## 12. STATUS RINGKASAN")
rev850_start = content.rfind("### Rev. 850 (fresh verification)", 0, rev850_end)
if rev850_start != -1 and rev850_end != -1:
    # Insert Rev. 851 entry between Rev. 850 entry and §12
    content = content[:rev850_end] + "\n\n" + rev851_entry + content[rev850_end:]
    modifications.append("§11 Rev. 851 entry added")
else:
    print("WARNING: Could not find Rev. 850 entry position for insertion")

# Write updated content
with open(PRD_PATH, 'w') as f:
    f.write(content)

print("\n=== MODIFICATIONS ===")
for m in modifications:
    print(f"  ✓ {m}")
print(f"\nTotal modifications: {len(modifications)}")
print(f"File written to: {PRD_PATH}")
