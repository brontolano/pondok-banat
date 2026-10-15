#!/usr/bin/env python3
"""Fresh-state verification for Pondok Banat PRD (Rev. 71)."""
import sqlite3, json, os, sys
from datetime import datetime, timezone

ROOT = "/opt/data/home/workspace/dev/pondok-banat"
DB = os.path.join(ROOT, "dev.db")

conn = sqlite3.connect(DB)
cur = conn.cursor()

def q(label, sql, one=False):
    try:
        rows = cur.execute(sql).fetchall()
        print(f"[{label}] rows={len(rows)}")
        if one and rows:
            r = rows[0]
            print("  sample:", r if isinstance(r, tuple) else [r])
        return rows
    except Exception as e:
        print(f"[{label}] ERROR: {e}")
        return []

def dist(label, sql):
    rows = cur.execute(sql).fetchall()
    total = sum(r[1] for r in rows)
    print(f"[{label}] {len(rows)} classes, TOTAL={total}")
    for r in rows:
        print(f"   {r[0]} {r[1]} {r[2]} {r[3]} {r[4]} = {r[5]}")

print("=== DEV.DB FRESH VERIFICATION ===")
print("Date:", datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S WIB (%Z)"))

q("users", "SELECT id, email, role, active FROM users")
q("roles", "SELECT id, name, created_at FROM roles")
q("role_permissions_count", "SELECT COUNT(*) FROM role_permissions")
q("students_total", "SELECT COUNT(*) FROM students")
q("students_active", "SELECT COUNT(*) FROM students WHERE active=1")
q("students_inactive", "SELECT COUNT(*) FROM students WHERE active=0")
q("students_uid_nfc_filled", "SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ''")
q("students_uid_nfc_null", "SELECT COUNT(*) FROM students WHERE uid_nfc IS NULL OR uid_nfc=''")
q("classes_total", "SELECT COUNT(*) FROM classes")
q("classes_with_students", "SELECT COUNT(*) FROM classes WHERE (SELECT COUNT(*) FROM students WHERE students.class_id = classes.id) > 0")
q("classes_empty", "SELECT COUNT(*) FROM classes WHERE (SELECT COUNT(*) FROM students WHERE students.class_id = classes.id) = 0")
q("teachers_total", "SELECT COUNT(*) FROM teachers")
q("teachers_active", "SELECT COUNT(*) FROM teachers WHERE active=1")
q("subjects_total", "SELECT COUNT(*) FROM subjects")
q("silabus_total", "SELECT COUNT(*) FROM silabus")
q("rpp_total", "SELECT COUNT(*) FROM rpp")
q("grades_total", "SELECT COUNT(*) FROM grades")
q("absensi_total", "SELECT COUNT(*) FROM absensi")
q("rapor_total", "SELECT COUNT(*) FROM rapor")
q("announcements_total", "SELECT COUNT(*) FROM announcements")
q("messages_total", "SELECT COUNT(*) FROM messages")
q("notifications_total", "SELECT COUNT(*) FROM notifications")

print("\n-- Siswa per kelas (diverifikasi dari dev.db) --")
dist("", "SELECT c.kode, c.nama, c.program, c.seksi, c.jenjang, COUNT(s.id) as jml FROM classes c LEFT JOIN students s ON s.class_id=c.id GROUP BY c.id ORDER BY c.jenjang, c.seksi")

conn.close()
