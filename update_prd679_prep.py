#!/usr/bin/env python3
"""Update PRD-PONDOK-BANAT.md to Rev. 679 with fresh verification."""

import subprocess
import os

REPO = "/opt/data/home/workspace/dev/pondok-banat"
FILE = os.path.join(REPO, "PRD-PONDOK-BANAT.md")

# --- Gather fresh git state ---
def run(cmd):
    r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
    return r.stdout.strip()

head = run(["git", "log", "-1", "--format=%H %s"])
total = run(["git", "rev-list", "--count", "HEAD"])
ahead_behind = run(["git", "rev-list", "--left-right", "--count", "HEAD...origin/main"])
ahead, behind = ahead_behind.split("\t")
origin_head = run(["git", "log", "-1", "--format=%H %s", "origin/main"])
dev_db = "absent" if not os.path.exists(os.path.join(REPO, "dev.db")) else "present"
nm_dirs = run(["ls", "node_modules"] + ["|"] + ["wc", "-l"]).split()[0] if False else None
nm_count = len(os.listdir(os.path.join(REPO, "node_modules"))) if os.path.isdir(os.path.join(REPO, "node_modules")) else 0
untracked = run(["git", "status", "--porcelain=v1"]).count("\n")  # includes all status lines
untracked_only = run(["git", "status", "--porcelain=v1"]).count("\n")  # uncomment later

print("HEAD:", head)
print("TOTAL:", total)
print("AHEAD/BEHIND:", ahead, behind)
print("ORIGIN:", origin_head)
print("DEV.DB:", dev_db)
print("NODE_MODULES_DIRS:", nm_count)
print("UNTRACKED_LINES:", untracked)
