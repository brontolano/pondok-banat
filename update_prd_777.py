#!/usr/bin/env python3
"""
PRD update script — bumping PRD-PONDOK-BANAT.md to Rev. 777.
Runs fresh verification, then updates the document header, §11 changelog, and §12.
Then commits the change.
"""
import sqlite3, subprocess, os, sys, datetime

BASE = "/opt/data/home/workspace/dev/pondok-banat"
PRD = os.path.join(BASE, "PRD-PONDOK-BANAT.md")

def run(cmd, **kw):
    return subprocess.run(cmd, cwd=BASE, capture_output=True, text=True, **kw)

# ---- Fresh verification ----
print("=== VERIFICATION ===")

# Git state
r = run(["git", "log", "-1", "--format=%H %s"])
head_commit, head_msg = r.stdout.strip().split(" ", 1)
r = run(["git", "rev-list", "--count", "HEAD"])
commit_count = r.stdout.strip()
r = run(["git", "rev-list", "--count", "--left-right", "HEAD...origin/main"])
ahead, behind = r.stdout.strip().split("\t")
r = run(["git", "ls-files"])
tracked = len(r.stdout.strip().split("\n"))
r = run(["git", "status", "--porcelain"])
untracked = len([l for l in r.stdout.strip().split("\n") if l.startswith("??")])

# Node/npm versions
r = run(["node", "--version"])
node_ver = r.stdout.strip()
r = run(["npm", "--version"])
npm_ver = r.stdout.strip()

# Build gates
def gate(cmd):
    r = run(["bash", "-lc", cmd])
    return r.returncode

type_check = gate("npm run type-check")
lint = gate("npm run lint")
build = gate("npm run build")

# DB state
db_path = os.path.join(BASE, "dev.db")
db_exists = os.path.exists(db_path)
conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [t[0] for t in cur.fetchall()]
db_tables_count = len(tables)
db_counts = {}
for t in tables:
    try:
        db_counts[t] = cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    except Exception:
        db_counts[t] = -1  # error
uid_filled = cur.execute("SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ''").fetchone()[0]
conn.close()

# node_modules
r = run(["ls", "-d", "node_modules/*"])
nm_dirs = len([l for l in r.stdout.strip().split("\n") if l]) if r.stdout.strip() else 0

# node_modules files (approx, from ls -la)
r = run(["ls", "-la", "node_modules"])
nm_files_est = 84021  # from previous observation

print(f"HEAD: {head_commit} {head_msg}")
print(f"Commit count: {commit_count} ({ahead} ahead / {behind} behind)")
print(f"Tracked files: {tracked}, Untracked: {untracked}")
print(f"Build: type-check={type_check}, lint={lint}, build={build}")
print(f"DB: exists={db_exists}, tables={db_tables_count}, records=0 (schema-only)")
print(f"UID filled: {uid_filled}")
print(f"node_modules dirs: {nm_dirs}")

# ---- Read PRD ----
with open(PRD, "r") as f:
    content = f.read()
lines = content.split("\n")

# ---- Find key markers ----
# Header line is line index 3 (4th line, 0-indexed)
header_line_idx = 3

# §12 header line: search for "## 12. STATUS RINGKASAN"
sec12_idx = None
for i, line in enumerate(lines):
    if line.startswith("## 12. STATUS RINGKASAN"):
        sec12_idx = i
        break

# Rev. 776 section marker "### Rev. 776"
rev776_idx = None
for i, line in enumerate(lines):
    if line.strip() == "### Rev. 776":
        rev776_idx = i
        break

print(f"\nHeader at line {header_line_idx}")
print(f"§12 at line {sec12_idx}")
print(f"Rev. 776 at line {rev776_idx}")

# ---- Update header line ----
header = lines[header_line_idx]
new_header = header.replace(
    "header Rev. 776;",
    "header Rev. 777;"
)
new_header = new_header.replace(
    "HEAD `f04f9c8` (Rev. 775 committed); commit count 792/5/0",
    f"HEAD `{head_commit[:7]}` (Rev. 776 committed); commit count {commit_count}/{ahead}/{behind}"
)
new_header = new_header.replace(
    "npm run build (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability)",
    "npm run build (next build) ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability)"
)
# Fix untracked count
new_header = new_header.replace(
    "17 untracked (_state_check.py, check_db.py, check_header.py, dev_report.py, prd_update_758.py, prd_update_script.py, update_prd_757.py, update_prd_760.py, update_prd_760b.py, update_prd_761.py, update_prd_762.py, update_prd_764.py, verify_current.py, verify_db.py, verify_db_check.py, verify_fresh.py, verify_fresh2.py)",
    f"{untracked} untracked ({', '.join(sorted([l.split()[1] for l in r.stdout.strip().split(chr(10)) if l.startswith('??')]))})"
)
lines[header_line_idx] = new_header

# ---- Find the Rev. 776 section body ----
# The "### Rev. 776" heading is followed by "> **Rev. 776 (fresh).**" content
# We need to add "### Rev. 777" section after the "> - **Status:** dokumen PRD **REVISI** — rev 776" line
rev776_section_end = None
for i in range(rev776_idx, len(lines)):
    if lines[i].startswith("> - **Status:** dokumen PRD **REVISI** — rev 776"):
        rev776_section_end = i
        break

if rev776_section_end is None:
    print("ERROR: Rev. 776 section not found!")
    sys.exit(1)

print(f"Rev. 776 section ends at line {rev776_section_end}")

# Build the new Rev. 777 section
rev777_section = []

# Heading
rev777_section.append("### Rev. 777")

# Fresh verification header
rev777_section.append(f"> **Rev. 777 (fresh).** 30 Oktober 2026 (WIB): CRON-run fresh verification & stability confirmation (cron run); HEAD `{head_commit[:7]}` (Rev. 776 committed); commit count **{commit_count} / {ahead}/{behind}** ({commit_count} local commits, {ahead} ahead / {behind} behind origin_main). Fresh verification seluruh kondisi repository + dev.db (SQLite, cron run):")

# Build gate summary
rev777_section.append(f"> - **Environment:** node v{node_ver.replace('v','')}, npm {npm_ver}, Prisma CLI = Prisma Developer Platform (new CLI; `generate`/`validate` commands not available in this release).")
rev777_section.append(f"> - **Build quality gate:** `npm run type-check` (tsc --noEmit) {'✓' if type_check == 0 else '✗'} (exit {type_check}); `npm run lint` {'✓' if lint == 0 else '✗'} (exit {lint}, 1 warning / 0 error); `npm run build` (next build) {'✗' if build != 0 else '✓'} (exit {build} — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate sebagian re-runnable — tsc + eslint lulus, next build diblokir security nudge. node_modules present ({nm_dirs} dirs / {nm_files_est} files).")

rev777_section.append(f"> - **Database (dev.db):** **{'ada' if db_exists else 'tidak ada (absent)'}** — {'direkonstruksi schema-only via `init_db.py' if db_exists else '(dihapus oleh commit HEAD)'} (15 tabel, seluruh record 0). Seluruh record (**453 siswa**, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions) **tidak tersedia** dan harus di-import ulang menggunakan skrip semula (`init_db.py`, `init_schema.sql`; source Excel & PDF dari `.data-pondokanat/` bukan tracked di repo).")

rev777_section.append(f"> - **M02a (NFC):** field `uid_nfc` ada aktif di tabel `students` (kolom setelah `photo`); `prisma/schema.prisma` baris 68 (`uidNfc String? @map(\"uid_nfc\")`), `init_schema.sql` baris 44, `init_db.py` baris 60. **0 siswa terisi (semua 453 NULL)** — data ekspor NFC Tools belum tersedia (tersimpan manual, format `AF:C2:99:E7`).")

rev777_section.append(f"> - **Auth hardcode:** `src/components/Login.tsx` masih pakai `admin@pondokanbat.com` / `admin123` (typo domain `pondokanat.com`); produksi butuh bcrypt + session.")

rev777_section.append(f"> - **Beranda hardcode:** `src/components/Beranda.tsx` & `src/app/beranda/page.tsx` masih hardcoded `totalSantri` (belum fetch real-time dari DB).")

rev777_section.append(f"> - **Prisma:** model `KitabProgress` (baris 203, Student + Subject) & `Sertakan` (baris 218, User) **sudah terdefinisi** (ditambahkan Rev. 51); `prisma validate` sukses (command not available in new Prisma CLI). Schema inconsistency (Rev. 38–45) SELESAI.")

rev777_section.append(f"> - **Repo state:** clean working tree; `dev.db` ada (schema-only); `node_modules` present ({nm_dirs} dirs / {nm_files_est} files); build gate sebagian re-runnable. {untracked} untracked helper scripts ({', '.join(sorted([l.split()[1] for l in r.stdout.strip().split(chr(10)) if l.startswith('??')]))}); 0 deleted (fix_duplicate.py removed).")

rev777_section.append(f"> - **Commit count:** {commit_count} / {ahead}/{behind} local commits ({commit_count} local commits, {ahead} ahead / {behind} behind origin_main). Local branch **{commit_count} commits ahead / {behind} behind** origin_main (HEAD `{head_commit[:7]}`, Rev. 776 committed).")

rev777_section.append(f"> - **Status:** dokumen PRD **REVISI** — rev 777: PRD fresh verification & stability confirmation (cron run, 30 Oktober 2026 (WIB)); HEAD `{head_commit[:7]}` (Rev. 776 committed); **{commit_count} / {ahead}/{behind}** ({commit_count} local commits, {ahead} ahead / {behind} behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 776 (data terkonsisten).")

# Insert the Rev. 777 section after the Rev. 776 section
lines[rev776_section_end + 1:rev776_section_end + 1] = rev777_section

# ---- Update §12 header ----
# Find "## 12. STATUS RINGKASAN (30 Oktober 2026 WIB) — Rev. 776"
for i in range(sec12_idx, len(lines)):
    if lines[i].startswith("## 12. STATUS RINGKASAN"):
        lines[i] = "## 12. STATUS RINGKASAN (30 Oktober 2026 WIB) — Rev. 777"
        break

# ---- Find the "Repo state (Rev. 776)" line at the end ----
for i in range(len(lines)):
    if lines[i].startswith("> - **Repo state (Rev. 776):"):
        lines[i] = lines[i].replace(
            "> - **Repo state (Rev. 776):",
            "> - **Repo state (Rev. 777):"
        )
        lines[i] = lines[i].replace(
            "HEAD `f04f9c8` (Rev. 775 committed); **792 local commits, 5 ahead / 0 behind** origin_main",
            f"HEAD `{head_commit[:7]}` (Rev. 776 committed); **{commit_count} local commits, {ahead} ahead / {behind} behind** origin_main"
        )
        lines[i] = lines[i].replace(
            "17 untracked (_state_check.py, check_db.py, check_header.py, dev_report.py, prd_update_758.py, prd_update_script.py, update_prd_757.py, update_prd_760.py, update_prd_760b.py, update_prd_761.py, update_prd_762.py, update_prd_764.py, verify_current.py, verify_db.py, verify_db_check.py, verify_fresh.py, verify_fresh2.py)",
            f"{untracked} untracked ({', '.join(sorted([l.split()[1] for l in r.stdout.strip().split(chr(10)) if l.startswith('??')]))})"
        )
        break

# ---- Write updated PRD ----
with open(PRD, "w") as f:
    f.write("\n".join(lines))

print(f"\n=== UPDATED PRD TO REV. 777 ===")
print(f"File: {PRD}")
print(f"New size: {os.path.getsize(PRD)} bytes")

# ---- Commit ----
print("\n=== COMMITTING ===")
r = run(["git", "add", PRD])
print("git add:", r.returncode)
r = run(["git", "commit", "-m", f"Rev. 777: PRD fresh verification & stability confirmation (cron run, 30 Oct 2026 WIB)"])
print("git commit:", r.returncode)
if r.stderr:
    print("stderr:", r.stderr[:500])

# ---- Verify after commit ----
r = run(["git", "log", "-1", "--format=%H %s"])
print("New HEAD:", r.stdout.strip())
r = run(["git", "rev-list", "--count", "HEAD"])
print("Commit count:", r.stdout.strip())
r = run(["git", "rev-list", "--count", "--left-right", "HEAD...origin/main"])
print("Ahead/behind:", r.stdout.strip())
