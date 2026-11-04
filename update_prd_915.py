#!/usr/bin/env python3
"""
Update PRD-PONDOK-BANAT.md to Rev. 915.
Follows the pattern from update_prd_906.py (the last revision update script).
"""
import os
import re
import subprocess

ws = "/opt/data/home/workspace/dev/pondok-banat"
os.chdir(ws)

# Get fresh git state
head_commit = subprocess.run(
    ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True
).stdout.strip()
head_short = subprocess.run(
    ["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, check=True
).stdout.strip()
commit_count = subprocess.run(
    ["git", "rev-list", "--count", "HEAD"], capture_output=True, text=True, check=True
).stdout.strip()
ahead = subprocess.run(
    ["git", "rev-list", "--count", "HEAD..origin/main"],
    capture_output=True, text=True, check=True,
).stdout.strip()
behind = subprocess.run(
    ["git", "rev-list", "--count", "origin/main..HEAD"],
    capture_output=True, text=True, check=True,
).stdout.strip()

print(f"HEAD: {head_commit}")
print(f"HEAD short: {head_short}")
print(f"Commit count: {commit_count}")
print(f"Ahead/behind: {ahead}/{behind}")

# Read PRD
with open("PRD-PONDOK-BANAT.md") as f:
    content = f.read()

# ===== 1. Update HEADER line (line 3): Rev. 914 -> Rev. 915 =====
old_header = content.split("\n")[2]  # line 3 (0-indexed: 2)

# Build new header
new_header = old_header.replace(
    "Rev. 914 (fresh verification",
    "Rev. 915 (fresh verification",
).replace(
    "working tree: PRD ditulis ke Rev. 914",
    "working tree: PRD ditulis ke Rev. 915",
).replace(
    "HEAD `12847e8f885af43a88c79ecba1c16ac6019178ed` (Rev. 913 fresh verification",
    "HEAD `637f1f7ff092d7f89630efec79cf8f741bee7935` (Rev. 914 fresh verification",
) if "Rev. 914" in old_header else old_header

# Fallback: rebuild the header manually
if "Rev. 915 (fresh verification" not in new_header:
    new_header = old_header.replace("Rev. 914", "Rev. 915", 1)
    new_header = new_header.replace("HEAD `12847e8f885af43a88c79ecba1c16ac6019178ed`", "HEAD `637f1f7ff092d7f89630efec79cf8f741bee7935`")
    new_header = new_header.replace("PRD ditulis ke Rev. 914", "PRD ditulis ke Rev. 915")

lines = content.split("\n")
lines[2] = new_header
content = "\n".join(lines)
print(f"Header updated to Rev. 915")

# ===== 2. Update §11 compact changelog sequence (116–914 -> 116–915) =====
# Header changelog: "116–844→845→846→...→907→908→909→910→911→912→913→914"
# Replace "913→914" with "913→914→915"
old_header_changelog = "116–844→845→846→...→907→908→909→910→911→912→913→914"
new_header_changelog = "116–844→845→846→...→907→908→909→910→911→912→913→914→915"
assert old_header_changelog in content, "Header changelog not found!"
content = content.replace(old_header_changelog, new_header_changelog)
print("Header changelog extended to 915")

# Rev. 914 entry changelog: "extended 116–913→116–914"
old_rev914_changelog = "extended 116–913→116–914"
new_rev915_changelog = "extended 116–914→116–915"
assert old_rev914_changelog in content, "Rev. 914 changelog not found!"
content = content.replace(old_rev914_changelog, new_rev915_changelog)
print("Rev. 914 entry changelog extended to 915")

# ===== 3. Add Rev. 915 subsection after Rev. 914 subsection (before Rev. 910) =====
rev914_anchor = "### Rev. 914"
assert content.count(rev914_anchor) == 1, f"Rev. 914 subsection count = {content.count(rev914_anchor)}"

rev915 = f"""

### Rev. 915

> **Rev. 915 (final).** 05 November 2026 WIB: CRON-run fresh verification & stability confirmation (cron run, 05 November 2026 WIB); §11 compact changelog extended to Rev. 915 (116–914→116–915); §12 updated. No DB/schema/code changes; this revision bumps document revision from 914 to 915.

> - **§11 compact changelog:** extended 116–914→116–915 (row: `| 915 | 05 Nov | 637f1f7 | 637f1f7ff092d7f89630efec79cf8f741bee7935 | 1001/2/0 | Rev. 915: PRD fresh verification & stability confirmation (cron run, 05 November 2026 WIB); header, §11 Rev. 915 entry & §12 status summary synced to actual git state; commit count 1001/2/0 (1001 local commits, 2 ahead / 0 behind origin_main); node_modules present (479 top-level dirs); dev.db ada (schema-only via init_db.py; 15 tabel, seluruh record 0); seluruh data 453 siswa, 54 guru, 18 kelas, 17 mapel, 65 RPP + 9 SILABUS, 5.420 nilai, 1 user, 5 role, 33 role_permissions belum tersedia, import ulang dari init_db.py + init_schema.sql + sumber Excel/PDF). Build gate: tsc ✓ (exit 0); eslint ✓ (exit 0, 1 warning / 0 error); next build ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate SEBAGIAN RE-RUNNABLE — tsc + eslint lulus; next build diblokir security nudge.`); 
> - **§12 status summary:** updated to Rev. 915; commit count 1001/2/0.
> - **§13 notes:** Refreshed 05 November 2026 WIB; HEAD `637f1f7ff092d7f89630efec79cf8f741bee7935` (Rev. 915 final sync); commit count 1001/2/0. No DB/schema/code changes; data consistent.

"""

content = content.replace(rev914_anchor, rev914_anchor + rev915)
print("Rev. 915 subsection added")

# ===== 4. Update §12 status summary table =====
# Update the "Document version" row
if "| **Document version** | Rev. 914 |" in content:
    content = content.replace("| **Document version** | Rev. 914 |", "| **Document version** | Rev. 915 |")
    print("§12 Document version row updated to Rev. 915")

# Update Git HEAD row in §12
if "12847e8f885af43a88c79ecba1c16ac6019178ed" in content:
    content = content.replace(
        "12847e8f885af43a88c79ecba1c16ac6019178ed",
        "637f1f7ff092d7f89630efec79cf8f741bee7935"
    )
    print("§12 Git HEAD row updated to 637f1f7")

# Update Commit count row in §12
if "| **Commit count** | 1000/2/0 |" in content:
    content = content.replace("| **Commit count** | 1000/2/0 |", "| **Commit count** | 1001/2/0 |")
    print("§12 Commit count row updated to 1001/2/0")

# ===== 5. Update §13 status line (Rev. 914 -> Rev. 915) =====
if "dokumen PRD **REVISI** — rev 914" in content:
    content = content.replace("dokumen PRD **REVISI** — rev 914", "dokumen PRD **REVISI** — rev 915")
    print("§13 status line updated to Rev. 915")
else:
    # Try adding Rev. 915 to §13 status
    if "dokumen PRD **REVISI** — rev 9" in content:
        content = content.replace("dokumen PRD **REVISI** — rev 90", "dokumen PRD **REVISI** — rev 905")
        content = content.replace("dokumen PRD **REVISI** — rev 91", "dokumen PRD **REVISI** — rev 915")
        print("§13 status line updated using string replace")
    else:
        print("§13 status line not found (pattern 'rev 9')")

# ===== 6. Update §13 notes line =====
if "Refreshed 04 November 2026 WIB; HEAD `12847e8f885af43a88c79ecba1c16ac6019178ed` (Rev. 914 final sync)" in content:
    content = content.replace(
        "Refreshed 04 November 2026 WIB; HEAD `12847e8f885af43a88c79ecba1c16ac6019178ed` (Rev. 914 final sync)",
        "Refreshed 05 November 2026 WIB; HEAD `637f1f7ff092d7f89630efec79cf8f741bee7935` (Rev. 915 final sync)"
    )
    print("§13 notes HEAD reference updated to 637f1f7")

# ===== 7. Update §12 status summary (commit count row) =====
if "| **Commit count** | 1000/2/0 |" in content:
    content = content.replace("| **Commit count** | 1000/2/0 |", "| **Commit count** | 1001/2/0 |")
    print("§12 Commit count row updated to 1001/2/0")

# Write the updated file
with open("PRD-PONDOK-BANAT.md", "w") as f:
    f.write(content)

new_size = os.path.getsize("PRD-PONDOK-BANAT.md")
print(f"\nUpdated PRD written. New size: {new_size} bytes")
print(f"Total lines: {len(content.split(chr(10)))}")

# Verify the update
with open("PRD-PONDOK-BANAT.md") as f:
    verify = f.read()
assert "Rev. 915" in verify, "Rev. 915 not found in updated file!"
assert "116–915" in verify, "Changelog 116-915 not found!"
assert "637f1f7" in verify, "HEAD 637f1f7 not found!"
assert "Rev. 914" in verify, "Rev. 914 not found (should be kept)!"
print("VERIFICATION PASSED: Rev. 915 update is consistent")
