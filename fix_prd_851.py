#!/usr/bin/env python3
"""
Fix remaining inconsistencies in PRD-PONDOK-BANAT.md after Rev. 851 update.
"""

PRD_PATH = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

# Read PRD
with open(PRD_PATH, 'r') as f:
    content = f.read()

# Verify current state
import subprocess

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

# Fix 1: Update untracked count in §12
old_untracked = "340 tracked files; 58 untracked (incl. helper scripts); 0 deleted"
new_untracked = f"{tracked_files} tracked files; {untracked_files} untracked (incl. helper scripts); {deleted_files} deleted"
content = content.replace(old_untracked, new_untracked)
print(f"Fixed untracked count: {old_untracked} -> {new_untracked}")

# Fix 2: Update commit count in §12 line 3215
old_commit = "**884 / 0/0** (884 local commits, 0 ahead / 0 behind origin_main)"
new_commit = f"**{commit_count} / {ahead}/{behind}** ({commit_count} local commits, {ahead} ahead / {behind} behind origin_main)"
content = content.replace(old_commit, new_commit)
print(f"Fixed commit count: {old_commit} -> {new_commit}")

# Write updated content
with open(PRD_PATH, 'w') as f:
    f.write(content)

print("\nFixes applied successfully.")
