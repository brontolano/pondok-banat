#!/usr/bin/env python3
"""Count node_modules files/dirs and run build gates for fresh verification."""
import os
import subprocess
import sys

REPO = "/opt/data/home/workspace/dev/pondok-banat"

print("=== node_modules counts ===")
nm = os.path.join(REPO, "node_modules")
n_dirs = 0
n_files = 0
for root, dirs, files in os.walk(nm):
    n_dirs += 1
    for _ in files:
        n_files += 1
print(f"dirs: {n_dirs}, files: {n_files}")

print("\n=== Build gates ===")
# tsc
r = subprocess.run(["npx", "tsc", "--noEmit"], cwd=REPO, capture_output=True, text=True)
print(f"tsc --noEmit: rc={r.returncode}")
if r.stdout.strip():
    print("  stdout:", r.stdout.strip()[:500])
if r.stderr.strip():
    print("  stderr:", r.stderr.strip()[:500])

# eslint
r = subprocess.run(["npx", "eslint", "."], cwd=REPO, capture_output=True, text=True)
print(f"eslint .: rc={r.returncode}")
if r.stdout.strip():
    print("  stdout:", r.stdout.strip()[:500])
if r.stderr.strip():
    print("  stderr:", r.stderr.strip()[:500])

# next build (short timeout to avoid hanging)
r = subprocess.run(["npx", "next", "build"], cwd=REPO, capture_output=True, text=True, timeout=300)
print(f"next build: rc={r.returncode}")
if r.stdout.strip():
    out = r.stdout.strip()
    print("  stdout (tail):", out[-500:])
if r.stderr.strip():
    err = r.stderr.strip()
    print("  stderr (tail):", err[-500:])

print("\nDone.")
