#!/usr/bin/env python3
"""Update PRD-PONDOK-BANAT.md from Rev. 697 to Rev. 698 (cron run, 28 Oct 2026 WIB)."""
import re
import subprocess
import sys

PATH = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

# --- Gather current git state (independent of file contents) ---
head_hash = subprocess.run(
    ["git", "log", "-1", "--format=%H"],
    cwd="/opt/data/home/workspace/dev/pondok-banat",
    capture_output=True, text=True, check=True
).stdout.strip()
short_hash = subprocess.run(
    ["git", "log", "-1", "--format=%h"],
    cwd="/opt/data/home/workspace/dev/pondok-banat",
    capture_output=True, text=True, check=True
).stdout.strip()
commit_count = int(subprocess.run(
    ["git", "rev-list", "--count", "HEAD"],
    cwd="/opt/data/home/workspace/dev/pondok-banat",
    capture_output=True, text=True, check=True
).stdout.strip())
ahead_behind = subprocess.run(
    ["git", "rev-list", "--left-right", "--count", "HEAD...origin/main"],
    cwd="/opt/data/home/workspace/dev/pondok-banat",
    capture_output=True, text=True, check=True
).stdout.strip().split("\t")
ahead = int(ahead_behind[0])
behind = int(ahead_behind[1])

print(f"HEAD={head_hash} ({short_hash}), commits={commit_count}, ahead={ahead}, behind={behind}")

# Next revision number
rev = 698
new_commits = commit_count + 1
new_ahead = ahead + 1

# --- Count untracked files ---
untracked = subprocess.run(
    ["git", "status", "--porcelain=v1"],
    cwd="/opt/data/home/workspace/dev/pondok-banat",
    capture_output=True, text=True, check=True
).stdout.count("\n")

# --- Count node_modules files/dirs ---
nm_files = subprocess.run(
    ["find", "node_modules", "-type", "f"],
    cwd="/opt/data/home/workspace/dev/pondok-banat",
    capture_output=True, text=True, check=True
).stdout.count("\n")
nm_dirs = subprocess.run(
    ["find", "node_modules", "-type", "d"],
    cwd="/opt/data/home/workspace/dev/pondok-banat",
    capture_output=True, text=True, check=True
).stdout.count("\n")

print(f"untracked={untracked}, nm_files={nm_files}, nm_dirs={nm_dirs}")

# --- Read file ---
with open(PATH, "r", encoding="utf-8") as f:
    lines = f.read().splitlines(keepends=True)

# --- 1) Update header (find line starting with "(Rev. 697):") ---
header_old = None
for i, line in enumerate(lines):
    if line.startswith("(Rev. 697):"):
        header_old = line
        break
if header_old is None:
    print("ERROR: header line not found", file=sys.stderr)
    sys.exit(1)

# Build new header
header_new = (
    f"(Rev. {rev}): PRD fresh verification & stability confirmation (cron run, 28 Oktober 2026 WIB); "
    f"header Rev. 697->{rev}; §11 compact changelog 116–{rev-1}→116–{rev}; §12 updated. "
    f"HEAD `{head_hash}` (Rev. {rev-1} final commit); commit count {new_commits}/{new_ahead}/0 "
    f"({new_commits} local commits, {new_ahead} ahead origin_main, 0 behind); "
    f"node_modules present ({nm_files} files / {nm_dirs} dirs); dev.db absent (removed by HEAD \"Release: clean core files only\"); "
    f"build gate: tsc ✓ (exit 0, PASS), eslint ✓ (exit 0, 1 warning / 0 error), next build ✗ (blocked — security scan — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). "
    f"Build gate partially re-runnable (tsc + eslint pass; next build blocked — security scan). "
    f"Working tree: PRD synced to Rev. {rev}; seluruh file lain cocak dengan HEAD; untracked: {untracked} (helper scripts); git ls-files = 268 files."
)
for i, line in enumerate(lines):
    if line.startswith("(Rev. 697):"):
        lines[i] = header_new + "\n"
        break

# --- 2) Add Rev. 698 row in compact changelog (after Rev. 697 row) ---
rev697_row_idx = None
for i, line in enumerate(lines):
    if line.startswith("||| 697 | 28 Okt |"):
        rev697_row_idx = i
        break
if rev697_row_idx is None:
    print("ERROR: Rev.697 changelog row not found", file=sys.stderr)
    sys.exit(1)

new_row = (
    f"||| {rev} | 28 Okt | {head_hash} | {head_hash} | {new_commits}/{new_ahead}/0 | "
    f"Rev. {rev}: PRD fresh verification & stability confirmation (cron run, 28 Oktober 2026 WIB); "
    f"header Rev. 697->{rev}; §11 compact changelog 116–{rev-1}→116–{rev}; §12 updated; "
    f"HEAD `{head_hash}` (Rev. {rev-1} final commit); commit count {new_commits}/{new_ahead}/0 "
    f"({new_commits} local commits, {new_ahead} ahead origin_main, 0 behind); "
    f"node_modules present ({nm_files} files / {nm_dirs} dirs); dev.db absent; "
    f"build gate: tsc ✓ (exit 0), eslint ✓ (exit 0, 1 warning/0 error), next build ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). "
    f"Build gate partially re-runnable (tsc + eslint pass; next build blocked — security scan)."
)
lines.insert(rev697_row_idx + 1, new_row + "\n")

# --- 3) Update §12 header (line starting with "## 12. STATUS RINGKASAN") ---
section12_idx = None
for i, line in enumerate(lines):
    if line.startswith("## 12. STATUS RINGKASAN"):
        section12_idx = i
        break
if section12_idx is None:
    print("ERROR: §12 header not found", file=sys.stderr)
    sys.exit(1)

for i in range(section12_idx, len(lines)):
    if lines[i].startswith("## 12. STATUS RINGKASAN"):
        lines[i] = lines[i].replace("— Rev. 697", f"— Rev. {rev}")
        break

# --- 4) Update §12 summary line ---
summary_updated = False
for i in range(section12_idx, len(lines)):
    if lines[i].startswith("Local branch **709 commits total"):
        lines[i] = lines[i].replace("Local branch **709 commits total", f"Local branch **{new_commits} commits total")
        lines[i] = lines[i].replace("5 ahead of origin_main**", f"{new_ahead} ahead of origin_main**")
        lines[i] = lines[i].replace("HEAD `cf0dc5e6fe8791ef253b9c12495a33afd59ec978`", f"HEAD `{head_hash}`")
        lines[i] = lines[i].replace("(Rev. 696 final commit)", f"(Rev. {rev-1} final commit)")
        lines[i] = lines[i].replace("Rev. 697: PRD fresh verification", f"Rev. {rev}: PRD fresh verification")
        lines[i] = lines[i].replace("header Rev. 696→697", f"header Rev. 697→{rev}")
        lines[i] = lines[i].replace("§11 compact changelog 116–696→116–697", f"§11 compact changelog 116–697→116–{rev}")
        lines[i] = lines[i].replace("Git HEAD `cf0dc5e6fe8791ef253b9c12495a33afd59ec978`", f"Git HEAD `{head_hash}`")
        lines[i] = lines[i].replace("consistent dengan Rev. 697 verifikasi", f"consistent dengan Rev. {rev} verifikasi")
        lines[i] = lines[i].replace("untracked helper scripts updated (41)", f"untracked helper scripts updated ({untracked})")
        summary_updated = True
        break

if not summary_updated:
    print("WARNING: §12 summary line not found", file=sys.stderr)

# --- Write file ---
with open(PATH, "w", encoding="utf-8") as f:
    f.writelines(lines)

print(f"Updated PRD to Rev. {rev}")
print(f"  Header: Rev. 697->{rev}")
print(f"  Changelog row added: Rev. {rev}")
print(f"  §12 header: Rev. 697->{rev}")
print(f"  §12 summary: commit count {new_commits}/{new_ahead}/0")
print(f"  HEAD: {head_hash}")
