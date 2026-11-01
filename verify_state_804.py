#!/usr/bin/env python3
"""Verification script for pondok-banat repo state (fresh verification)."""
import sqlite3
import subprocess
import os
import sys

REPO = "/opt/data/home/workspace/dev/pondok-banat"
PRD = os.path.join(REPO, "PRD-PONDOK-BANAT.md")

print("=== Working dir ===")
print(os.getcwd())

print("\n=== Git state ===")
for cmd in [
    ["git", "rev-parse", "HEAD"],
    ["git", "rev-list", "--count", "HEAD"],
    ["git", "rev-parse", "--abbrev-ref", "HEAD"],
    ["git", "log", "--oneline", "-3"],
    ["git", "status", "-sb"],
    ["git", "rev-parse", "origin/main"],
]:
    r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
    print(f"$ {' '.join(cmd)}")
    print("rc:", r.returncode, "stdout:", r.stdout.strip(), "stderr:", r.stderr.strip())

print("\n=== dev.db ===")
db_path = os.path.join(REPO, "dev.db")
if os.path.exists(db_path):
    print("dev.db exists:", os.path.getsize(db_path), "bytes")
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [r[0] for r in cur.fetchall()]
    print("tables:", len(tables))
    for t in tables:
        try:
            cur.execute(f"SELECT COUNT(*) FROM [{t}]")
            n = cur.fetchone()[0]
            print(f"  {t}: {n}")
        except Exception as e:
            print(f"  {t}: ERROR {e}")
    con.close()
else:
    print("dev.db ABSENT")

print("\n=== node_modules ===")
nm = os.path.join(REPO, "node_modules")
if os.path.isdir(nm):
    n = sum(len(d) for _, _, d in os.walk(nm))
    print("node_modules present:", n, "dirs")
else:
    print("node_modules ABSENT")

print("\n=== Prisma schema checks ===")
schema = os.path.join(REPO, "prisma", "schema.prisma")
if os.path.exists(schema):
    with open(schema, encoding="utf-8") as f:
        sc = f.read()
    print("uidNfc present:", "uidNfc" in sc)
    print("KitabProgress defined:", "model KitabProgress" in sc)
    print("Sertakan defined:", "model Sertakan" in sc)
else:
    print("schema.prisma absent")

print("\n=== PRD file ===")
if os.path.exists(PRD):
    with open(PRD, encoding="utf-8") as f:
        prd = f.read()
    print("PRD size:", len(prd), "bytes, lines:", prd.count("\n") + 1)
    print("Header has 'Rev. 803':", "Rev. 803" in prd.split("\n")[0] or "803" in prd.split("\n")[0])
    print("Last line has 'Rev. 803':", "Rev. 803" in prd.split("\n")[-1] if prd else False)
else:
    print("PRD ABSENT")

print("\nDone.")
