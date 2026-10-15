#!/usr/bin/env python3
import sqlite3, os

root = '/opt/data/home/workspace/dev/pondok-banat'
db_path = os.path.join(root, 'dev.db')

con = sqlite3.connect(db_path)
cur = con.cursor()

# Schema
cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='students'")
row = cur.fetchone()
print("=== students table DDL ===")
print(row[0] if row else "NO students table")
print()

# Check columns
cur.execute("PRAGMA table_info(students)")
cols = cur.fetchall()
print("=== students columns ===")
for c in cols:
    print(c[1], c[2], "pk" if c[5] else "")
print()

# Counts
print("=== counts ===")
for t in ['users','roles','role_permissions','students','classes','teachers','subjects','grades','absensi','rapor','announcements','messages','notifications','kitab_progress','silabus','rpp']:
    try:
        cur.execute(f"SELECT COUNT(*) FROM {t}")
        print(f"{t}: {cur.fetchone()[0]}")
    except Exception as e:
        print(f"{t}: ERROR ({e})")
print()

# students sample
print("=== students sample (first 3) ===")
cur.execute("SELECT id, NIS, nama, jk, kelas, seksi, uid_nfc FROM students LIMIT 3")
for r in cur.fetchall():
    print(r)
print()

# classes
print("=== classes sample ===")
cur.execute("SELECT id, nama, jenjang, seksi FROM classes LIMIT 20")
for r in cur.fetchall():
    print(r)
print()

# teachers
print("=== teachers sample (first 3) ===")
cur.execute("SELECT id, nama, jabatan, status FROM teachers LIMIT 3")
for r in cur.fetchall():
    print(r)
