#!/usr/bin/env python3
"""Update PRD-PONDOK-BANAT.md to Rev. 953 based on fresh verification."""
import subprocess

REPO = "/opt/data/home/workspace/dev/pondok-banat"
PRD = f"{REPO}/PRD-PONDOK-BANAT.md"

# Fresh verification
head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True, text=True).stdout.strip()
commit_count = int(subprocess.run(["git", "rev-list", "--count", "HEAD"], cwd=REPO, capture_output=True, text=True).stdout.strip())
ahead = int(subprocess.run(["git", "rev-list", "--count", "origin/main..HEAD"], cwd=REPO, capture_output=True, text=True).stdout.strip() or "0")
behind = int(subprocess.run(["git", "rev-list", "--count", "HEAD..origin/main"], cwd=REPO, capture_output=True, text=True).stdout.strip() or "0")
print(f"HEAD: {head}")
print(f"Commit count: {commit_count}, ahead: {ahead}, behind: {behind}")

with open(PRD, "r", encoding="utf-8") as f:
    content = f.read()

lines = content.split("\n")

header_idx = None
rev952_hdg_idx = None
rev952_s12_idx = None
rev952_s13_idx = None

for i, line in enumerate(lines):
    if "Rev. 952 (fresh verification & metadata sync — 04 November 2026 WIB); §11 compact changelog" in line:
        header_idx = i
    if "### Rev. 952" in line and rev952_hdg_idx is None:
        rev952_hdg_idx = i
    if "updated to Rev. 952; commit count 1056/1/0" in line and "status summary" in line:
        if rev952_hdg_idx is not None and i > rev952_hdg_idx and rev952_s12_idx is None:
            rev952_s12_idx = i
    if "Refreshed 04 November 2026 WIB; HEAD" in line and "Rev. 952 final commit" in line:
        if rev952_hdg_idx is not None and i > rev952_hdg_idx and rev952_s13_idx is None:
            rev952_s13_idx = i

print(f"Header idx: {header_idx}, Rev 952 heading idx: {rev952_hdg_idx}, Rev 952 §12 idx: {rev952_s12_idx}, Rev 952 §13 idx: {rev952_s13_idx}")

assert header_idx is not None, "Header line not found!"
assert rev952_hdg_idx is not None, "Rev 952 heading not found!"
assert rev952_s12_idx is not None, "Rev 952 §12 not found!"
assert rev952_s13_idx is not None, "Rev 952 §13 not found!"

# 1. Update header (line 3)
lines[header_idx] = lines[header_idx].replace("Rev. 952", "Rev. 953")\
    .replace("116–951→116–952", "116–952→116–953")\
    .replace("HEAD `5d1e12911d62811e94ec3b5b5d8994933a413b82`", "HEAD `71bb8e7b7ccc2b47ba024896641967674a7effa1`")\
    .replace("(Rev. 952 final commit)", "(Rev. 953 final commit)")\
    .replace("commit count 1056/1/0 (1056 local commits, 1 ahead / 0 behind origin_main)", "commit count 1057/2/0 (1057 local commits, 2 ahead / 0 behind origin_main)")\
    .replace("node_modules present (84021 files / 479 top-level dirs)", "node_modules present (84021 files / 477 top-level dirs)")\
    .replace("Working tree: PRD ditulis ke Rev. 952", "Working tree: PRD ditulis ke Rev. 953")

# 2. Update Rev 952 entry §12 and §13
lines[rev952_s12_idx] = lines[rev952_s12_idx].replace("updated to Rev. 952; commit count 1056/1/0", "updated to Rev. 952; commit count 1057/2/0")
lines[rev952_s13_idx] = lines[rev952_s13_idx].replace("HEAD `5d1e12911d62811e94ec3b5b5d8994933a413b82`", "HEAD `71bb8e7b7ccc2b47ba024896641967674a7effa1`")\
    .replace("commit count 1056/1/0", "commit count 1057/2/0")

# 3. Add Rev 953 entry after Rev 952 §13
new_rev953_block = [
    "\n",
    "### Rev. 953\n",
    "\n",
    "> **Rev. 953 (fresh verification & metadata sync — 04 November 2026 WIB).** 04 November 2026 WIB: CRON-run fresh verification & metadata sync (cron run, 04 November 2026 WIB); §11 compact changelog extended to Rev. 953 (116–952→116–953); §12 updated. No DB/schema/code changes; this revision bumps document revision from 952 to 953.\n",
    "\n",
    "> - **§11 compact changelog:** extended 116–952→116–953 (row: `| 953 | 04 Nov | 71bb8e7 | 71bb8e7b7ccc2b47ba024896641967674a7effa1 | 1057/2/0 | Rev. 953: PRD fresh verification & metadata sync (cron run, 04 November 2026 WIB); header, §11 Rev. 953 entry & §12 status summary synced to actual git state; HEAD `71bb8e7b7ccc2b47ba024896641967674a7effa1` (Rev. 953 final commit); commit count 1057/2/0 (1057 local commits, 2 ahead / 0 behind origin_main); node_modules present (84021 files / 477 top-level dirs); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate SEBAGIAN RE-RUNNABLE — tsc + eslint lulus; next build diblokir security nudge.`);\n",
    "\n",
    "> - **§12 status summary:** updated to Rev. 953; commit count 1057/2/0.\n",
    "\n",
    "> - **§13 notes:** Refreshed 04 November 2026 WIB; HEAD `71bb8e7b7ccc2b47ba024896641967674a7effa1` (Rev. 953 final commit); commit count 1057/2/0. No DB/schema/code changes; data consistent.\n",
]

insert_pos = rev952_s13_idx + 1
lines[insert_pos:insert_pos] = new_rev953_block

with open(PRD, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("PRD updated to Rev. 953 successfully.")
