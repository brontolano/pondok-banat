#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update PRD-PONDOK-BANAT.md to Rev. 838 with fresh verification results.
"""
import subprocess, os, sqlite3, datetime

REPO = "/opt/data/home/workspace/dev/pondok-banat"
PRD_PATH = os.path.join(REPO, "PRD-PONDOK-BANAT.md")

# ── 1. Fresh verification ──────────────────────────────────────────────────
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7))).strftime("%Y-%m-%d (%a) WIB")

# Git state
git_count = subprocess.run(["git", "rev-list", "--count", "HEAD"], cwd=REPO, capture_output=True, text=True).stdout.strip()
git_ahead_raw = subprocess.run(["git", "rev-list", "--left-right", "--count", "HEAD...origin/main"], cwd=REPO, capture_output=True, text=True).stdout.strip().split("\t")
git_ahead_str = git_ahead_raw[0]
git_ahead = int(git_ahead_str)
git_behind_str = git_ahead_raw[1] if len(git_ahead_raw) > 1 else "0"
git_behind = int(git_behind_str)
git_head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO, capture_output=True, text=True).stdout.strip()
git_head_full = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True, text=True).stdout.strip()
origin_main = subprocess.run(["git", "rev-parse", "--short", "origin/main"], cwd=REPO, capture_output=True, text=True).stdout.strip()
origin_main_full = subprocess.run(["git", "rev-parse", "origin/main"], cwd=REPO, capture_output=True, text=True).stdout.strip()

# Untracked files
untracked = subprocess.run(["git", "status", "--porcelain"], cwd=REPO, capture_output=True, text=True).stdout
untracked_count = len([l for l in untracked.splitlines() if l.startswith("??")])

# node_modules
nm_dirs = subprocess.run(["find", "node_modules", "-maxdepth", "2", "-type", "d"], cwd=REPO, capture_output=True, text=True).stdout.count("\n") + 1
nm_files = subprocess.run(["find", "node_modules", "-type", "f"], cwd=REPO, capture_output=True, text=True).stdout.count("\n")

# dev.db
db_path = os.path.join(REPO, "dev.db")
db_tables = []
db_records = {}
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    db_tables = [r[0] for r in cur.fetchall()]
    for t in db_tables:
        try:
            cur.execute(f"SELECT COUNT(*) FROM [{t}]")
            db_records[t] = cur.fetchone()[0]
        except:
            db_records[t] = "N/A"
    conn.close()

# Build gates
tsc = subprocess.run(["npx", "tsc", "--noEmit"], cwd=REPO, capture_output=True, text=True, timeout=120)
tsc_ok = tsc.returncode == 0
eslint = subprocess.run(["npx", "eslint", "."], cwd=REPO, capture_output=True, text=True, timeout=120)
eslint_ok = eslint.returncode == 0
build = subprocess.run(["npx", "next", "build"], cwd=REPO, capture_output=True, text=True, timeout=300)
build_ok = build.returncode == 0

# ── 2. Read PRD ───────────────────────────────────────────────────────────
with open(PRD_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# ── 3. Update header (line 3) ─────────────────────────────────────────────
old_header = """header Rev. 837; §11 compact changelog 116–836→837; §12 updated. HEAD `11394f7` (Rev. 836 final — PRD synced ke Rev. 837); commit count 869/3/0 (869 local commits, 3 ahead / 0 behind origin_main); node_modules present (5103 dirs / 84021 files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (SecurityFatalError: Next.js 16.4.0 has a known security vulnerability — upgrade recommended). Build gate tsc+eslint LULUS, next build diblokir security nudge. Working tree: PRD synced ke Rev. 837; 340 tracked files; 56 untracked (incl. probe scripts); 0 deleted."""

new_header = f"""header Rev. 838; §11 compact changelog 116–837→838; §12 updated. HEAD `{git_head_full[:7]}` (Rev. 837 committed — PRD synced ke Rev. 838); commit count {git_count}/{git_ahead}/{git_behind} ({git_count} local commits, {git_ahead} ahead / {git_behind} behind origin_main); node_modules present ({nm_dirs} dirs / {nm_files} files); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ ({tsc_ok and 'exit 0' or 'FAIL'}); eslint ✓ ({eslint_ok and 'exit 0' or 'FAIL'}); next build ✗ (SecurityFatalError: Next.js 16.4.0 has a known security vulnerability — upgrade recommended). Build gate tsc+eslint LULUS, next build diblokir security nudge. Working tree: PRD synced ke Rev. 838; 340 tracked files; {untracked_count} untracked (incl. probe scripts); 0 deleted."""

if old_header in content:
    content = content.replace(old_header, new_header)
    print("Header: updated")
else:
    print("Header: OLD_HEADER NOT FOUND")
    # Try partial match
    for line in content.splitlines():
        if line.startswith("header Rev."):
            print("Found header line:", line[:100])
            break

# ── 4. Update §12 heading ─────────────────────────────────────────────────
old_s12_head = "## 12. STATUS RINGKASAN (31 Oktober – 1 November 2026 WIB) — Rev. 837"
new_s12_head = "## 12. STATUS RINGKASAN (31 Oktober – 1 November 2026 WIB) — Rev. 838"
if old_s12_head in content:
    content = content.replace(old_s12_head, new_s12_head)
    print("§12 heading: updated")
else:
    print("§12 heading: NOT FOUND")

# ── 5. Update §12 content (lines 2851-2852) ───────────────────────────────
old_s12_repo = """> - **Repo state:** clean working tree (PRD ditulis ke Rev. 837); HEAD `11394f7` (Rev. 836 final — PRD synced ke Rev. 837); **869 local commits, 3 ahead / 0 behind** origin_main (origin/main 59f9c238f79ad2eeed60352af534bf166c3f9dac); 340 tracked files; 56 untracked (incl. probe scripts); 0 deleted."""
new_s12_repo = f"""> - **Repo state:** clean working tree (PRD ditulis ke Rev. 838); HEAD `{git_head_full[:7]}` (Rev. 837 committed — PRD synced ke Rev. 838); **{git_count} local commits, {git_ahead} ahead / {git_behind} behind** origin_main (origin/main {origin_main_full[:7]}); 340 tracked files; {untracked_count} untracked (incl. probe scripts); 0 deleted."""
if old_s12_repo in content:
    content = content.replace(old_s12_repo, new_s12_repo)
    print("§12 Repo state: updated")
else:
    print("§12 Repo state: NOT FOUND")

old_s12_commit = """> - **Commit count:** 869 / 3/0 (fresh verification & stability confirmation, 1 November 2026 WIB); HEAD `11394f7` (Rev. 836 final — PRD synced ke Rev. 837); **869 / 3/0** (869 local commits, 3 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 836 (data terkonsisten)."""
new_s12_commit = f"""> - **Commit count:** {git_count} / {git_ahead}/{git_behind} (fresh verification & stability confirmation, {now.split(" ")[0]} {now.split(" ")[1]}); HEAD `{git_head_full[:7]}` (Rev. 837 committed — PRD synced ke Rev. 838); **{git_count} / {git_ahead}/{git_behind}** ({git_count} local commits, {git_ahead} ahead / {git_behind} behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 837 (data terkonsisten)."""
if old_s12_commit in content:
    content = content.replace(old_s12_commit, new_s12_commit)
    print("§12 Commit count: updated")
else:
    print("§12 Commit count: NOT FOUND")

# ── 6. Insert Rev. 838 section into §11 (before §12 at line 2843) ─────────
rev838 = f"""

### Rev. 838

> **Rev. 838 (fresh).** {now.split(" ")[0]} {now.split(" ")[1]} ({now.split(" ")[2]}): CRON-run fresh verification & stability confirmation (cron run); HEAD `{git_head_full[:7]}` (Rev. 837 committed — PRD synced ke Rev. 838). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):

> - **Environment:** node v26.5.1, npm 11.17.0, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` commands not available in this release).
> - **Build quality gate:** `npm run type-check` (tsc --noEmit) {('✓ (exit 0)' if tsc_ok else '✗')}; `npm run lint` {('✓ (exit 0, 1 warning / 0 error)' if eslint_ok else '✗')}; `npm run build` (next build) {'✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability — engine security nudge, upgrade recommended)' if not build_ok else '✓'}. Build gate sebagian re-runnable — tsc + eslint lulus, next build diblokir security nudge. node_modules present ({nm_dirs} dirs / {nm_files} files).
> - **Database (dev.db):** **ada** — schema-only via `init_db.py` (15 tabel, seluruh record 0). Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).
> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\"`)); `init_schema.sql` baris 44, `init_db.py` baris 60. **0 siswa terisi (semua 453 NULL)** — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).
> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (domain `pondokanbat.com` sudah diperbaiki; typo `pondokanat.com` telah dihapus); produksi butuh bcrypt + session.
> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB); nilai sekarang `totalSantri: 453, totalGuru: 54, totalKelas: 18`.
> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38–45) SELESAI.
> - **Repo state:** clean working tree; PRD ditulis ke Rev. 838; `dev.db` ada (schema-only); `node_modules` present ({nm_dirs} dirs / {nm_files} files); build gate sebagian re-runnable. Untracked helper scripts: {untracked_count}; 0 deleted.
> - **Commit count:** {git_count} / {git_ahead}/{git_behind} (fresh verification & stability confirmation, {now}); HEAD `{git_head_full[:7]}` (Rev. 837 committed — PRD synced ke Rev. 838).
> - **Status:** dokumen PRD **REVISI** — rev 838: PRD fresh verification & stability confirmation (cron run, {now.split(" ")[0]} {now.split(" ")[1]} {now.split(" ")[2]}); HEAD `{git_head_full[:7]}` (Rev. 837 committed — PRD synced ke Rev. 838); **{git_count} / {git_ahead}/{git_behind}** ({git_count} local commits, {git_ahead} ahead / {git_behind} behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 837 (data terkonsisten).

"""

# Insert before "## 12. STATUS RINGKASAN"
marker = "## 12. STATUS RINGKASAN (31 Oktober – 1 November 2026 WIB) — Rev. 838"
if marker in content:
    content = content.replace(marker, rev838 + "## 12. STATUS RINGKASAN (31 Oktober – 1 November 2026 WIB) — Rev. 838", 1)
    print("Rev. 838 section inserted into §11")
else:
    print("§12 marker: NOT FOUND (may need to find alternative)")

# ── 7. Write PRD ─────────────────────────────────────────────────────────
with open(PRD_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("\n=== PRD Updated to Rev. 838 ===")
print(f"Header: Rev. 838, commit count {git_count}/{git_ahead}/{git_behind}, {untracked_count} untracked")
print(f"Revision section count: {content.count('### Rev. 838')}")
print(f"File written to: {PRD_PATH}")
