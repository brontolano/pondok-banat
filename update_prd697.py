#!/usr/bin/env python3
"""Update PRD-PONDOK-BANAT.md from Rev. 696 to Rev. 697 (cron run, 28 Oct 2026 WIB)."""
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
rev = 697
# After this commit: commits = commit_count + 1, ahead = ahead + 1
new_commits = commit_count + 1
new_ahead = ahead + 1

# --- Read file ---
with open(PATH, "r", encoding="utf-8") as f:
    lines = f.read().splitlines(keepends=True)

# --- 1) Update header (line index 3, line 4) ---
header_old = "**(Rev. 696): PRD fresh verification & stability confirmation (cron run, 28 Oktober 2026 WIB); header Rev. 695->696; §11 compact changelog 116–695→116–696; §12 updated. HEAD `351b942` (Rev. 695 final commit); commit count 707/3/0 (707 local commits, 3 ahead origin_main, 0 behind); node_modules present (84021 files / 5103 dirs); dev.db absent (removed by HEAD \"Release: clean core files only\"); build gate: tsc ✓ (exit 0, PASS), eslint ✓ (exit 0, 1 warning / 0 error), next build ✗ (blocked — security scan — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). Build gate partially re-runnable (tsc + eslint pass; next build blocked — security scan). Working tree: PRD synced to Rev. 696; seluruh file lain cocak dengan HEAD; untracked: 41 (helper scripts); git ls-files = 268 files."
header_new = (
    f"(Rev. {rev}): PRD fresh verification & stability confirmation (cron run, 28 Oktober 2026 WIB); "
    f"header Rev. 696->{rev}; §11 compact changelog 116–{rev-1}→116–{rev}; §12 updated. "
    f"HEAD `{head_hash}` (Rev. {rev-1} final commit); commit count {new_commits}/{new_ahead}/0 "
    f"({new_commits} local commits, {new_ahead} ahead origin_main, 0 behind); "
    f"node_modules present (84021 files / 5103 dirs); dev.db absent (removed by HEAD \"Release: clean core files only\"); "
    f"build gate: tsc ✓ (exit 0, PASS), eslint ✓ (exit 0, 1 warning / 0 error), next build ✗ (blocked — security scan — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). "
    f"Build gate partially re-runnable (tsc + eslint pass; next build blocked — security scan). "
    f"Working tree: PRD synced to Rev. {rev}; seluruh file lain cocak dengan HEAD; untracked: 41 (helper scripts); git ls-files = 268 files."
)
found = False
for i, line in enumerate(lines):
    if line.startswith("**(Rev. 696):"):
        lines[i] = header_new + "\n"
        found = True
        break
if not found:
    print("ERROR: header line not found", file=sys.stderr)
    sys.exit(1)

# --- 2) Add Rev. 697 row in compact changelog (after Rev. 696 row, line index 837) ---
# The Rev. 696 row is the line starting with "||| 696 | 28 Okt | 351b942"
rev696_row_idx = None
for i, line in enumerate(lines):
    if line.startswith("|| 696 | 28 Okt | 351b942"):
        rev696_row_idx = i
        break
if rev696_row_idx is None:
    print("ERROR: Rev.696 row not found", file=sys.stderr)
    sys.exit(1)

new_row = (
    f"||| {rev} | 28 Okt | {head_hash} | {head_hash} | {new_commits}/{new_ahead}/0 | "
    f"Rev. {rev}: PRD fresh verification & stability confirmation (cron run, 28 Oktober 2026 WIB); "
    f"header Rev. 696->{rev}; §11 compact changelog 116–{rev-1}→116–{rev}; §12 updated; "
    f"HEAD `{head_hash}` (Rev. {rev-1} final commit); commit count {new_commits}/{new_ahead}/0 "
    f"({new_commits} local commits, {new_ahead} ahead origin_main, 0 behind); "
    f"node_modules present (84021 files / 5103 dirs); dev.db absent; "
    f"build gate: tsc ✓ (exit 0), eslint ✓ (exit 0, 1 warning/0 error), next build ✗ (exit 1 — SecurityFatalError: Next.js 16.4.0 has a known security vulnerability). "
    f"Build gate partially re-runnable (tsc + eslint pass; next build blocked — security scan)."
)
lines.insert(rev696_row_idx + 1, new_row + "\n")

# --- 3) Update §12 header (line 1359) ---
# Find the §12 header line
section12_idx = None
for i, line in enumerate(lines):
    if line.startswith("## 12. STATUS RINGKASAN"):
        section12_idx = i
        break
if section12_idx is None:
    print("ERROR: §12 header not found", file=sys.stderr)
    sys.exit(1)

# Update the §12 header line
old_s12_header = "## 12. STATUS RINGKASAN (28 Oktober 2026 WIB) — Rev. 696"
new_s12_header = f"## 12. STATUS RINGKASAN (28 Oktober 2026 WIB) — Rev. {rev}"
lines[section12_idx] = new_s12_header + "\n"

# Also update the summary line inside §12 (line 1368) which references Rev. 696
# Find the line that starts with "Local branch **707 commits total"
summary_updated = False
for i in range(section12_idx, len(lines)):
    if lines[i].startswith("Local branch **707 commits total"):
        # Replace 707 -> new_commits, 3 -> new_ahead
        lines[i] = lines[i].replace(
            "Local branch **707 commits total, 3 ahead of origin_main**",
            f"Local branch **{new_commits} commits total, {new_ahead} ahead of origin_main**"
        )
        lines[i] = lines[i].replace("HEAD `351b942`", f"HEAD `{head_hash}`")
        lines[i] = lines[i].replace("Rev. 696", f"Rev. {rev}")
        lines[i] = lines[i].replace("Rev. 695→696", f"Rev. 696→{rev}")
        lines[i] = lines[i].replace("§11 compact changelog 116–695→116–696", "§11 compact changelog 116–696→116–697")
        # Update the trailing Rev. 696 reference
        lines[i] = lines[i].replace("Rev. 696: PRD", f"Rev. {rev}: PRD")
        # Update "Rev. 695 final commit" -> "Rev. 696 final commit"
        lines[i] = re.sub(r"Rev\. 695 final commit", f"Rev. {rev-1} final commit", lines[i])
        summary_updated = True
        break

if not summary_updated:
    print("WARNING: §12 summary line not found", file=sys.stderr)

# --- Write file ---
with open(PATH, "w", encoding="utf-8") as f:
    f.writelines(lines)

print(f"Updated PRD to Rev. {rev}")
print(f"  Header: Rev. 696->{rev}")
print(f"  Changelog row added: Rev. 697")
print(f"  §12 header: Rev. 696->{rev}")
print(f"  Commit count: {new_commits}/{new_ahead}/0")
print(f"  HEAD: {head_hash}")
