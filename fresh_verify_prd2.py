#!/usr/bin/env python3
"""Actual data counts & class distribution from dev.db."""
import sqlite3, os
from collections import defaultdict

DB = "/opt/data/home/workspace/dev/pondok-banat/dev.db"
conn = sqlite3.connect(DB)
cur = conn.cursor()

checks = {
    "user count": "SELECT COUNT(*) FROM users",
    "role count": "SELECT COUNT(*) FROM roles",
    "role_permission count": "SELECT COUNT(*) FROM role_permissions",
    "student count": "SELECT COUNT(*) FROM students",
    "student status=active": "SELECT COUNT(*) FROM students WHERE status='active'",
    "student status=inactive": "SELECT COUNT(*) FROM students WHERE status='inactive'",
    "student uid_nfc filled": "SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ''",
    "student uid_nfc null/empty": "SELECT COUNT(*) FROM students WHERE uid_nfc IS NULL OR uid_nfc=''",
    "teacher count": "SELECT COUNT(*) FROM teachers",
    "teacher status=active": "SELECT COUNT(*) FROM teachers WHERE status='active'",
    "subject count": "SELECT COUNT(*) FROM subjects",
    "silabus count": "SELECT COUNT(*) FROM silabus",
    "rpp count": "SELECT COUNT(*) FROM rpp",
    "grade count": "SELECT COUNT(*) FROM grades",
    "absensi count": "SELECT COUNT(*) FROM absensi",
    "rapor count": "SELECT COUNT(*) FROM rapor",
    "announcements count": "SELECT COUNT(*) FROM announcements",
    "messages count": "SELECT COUNT(*) FROM messages",
    "notifications count": "SELECT COUNT(*) FROM notifications",
}

for label, sql in checks.items():
    r = cur.execute(sql).fetchone()
    print(f"{label}: {r[0]}")

print("\n-- Class distribution --")
rows = cur.execute("""
    SELECT c.kode, c.nama, c.program, c.seksi, c.jenjang, COUNT(s.id) as jml
    FROM classes c
    LEFT JOIN students s ON s.kelas_id = c.id
    GROUP BY c.id
    ORDER BY c.jenjang, c.seksi
""").fetchall()
total = 0
for r in rows:
    print(f"  {r[0]} {r[1]} {r[2]} {r[3]} {r[4]} = {r[5]}")
    total += r[5]
print(f"  TOTAL: {total}")

print("\n-- Sample students --")
for r in cur.execute("SELECT id, nisn, name, jk, ttl, kelas_id, status, uid_nfc FROM students LIMIT 5").fetchall():
    print(" ", r)

print("\n-- Sample classes --")
for r in cur.execute("SELECT id, kode, nama, seksi, jenjang, program, wali_kelas_id FROM classes LIMIT 5").fetchall():
    print(" ", r)

print("\n-- Sample teachers --")
for r in cur.execute("SELECT id, nip, name, jk, jabatan, status, kelas_id FROM teachers LIMIT 5").fetchall():
    print(" ", r)

conn.close()
