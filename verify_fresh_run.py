#!/usr/bin/env python3
import sqlite3, subprocess, os, sys

BASE = "/opt/data/home/workspace/dev/pondok-banat"
DB = os.path.join(BASE, "dev.db")

def run(cmd, **kw):
    return subprocess.run(cmd, cwd=BASE, capture_output=True, text=True, **kw)

print("=" * 20, "DATABASE", "=" * 20)
conn = sqlite3.connect(DB)
cur = conn.cursor()
tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
print("TABLES:")
for t in tables:
    print("  ", t)
print()
counts = cur.execute("""
SELECT 'students', COUNT(*) FROM students
UNION ALL SELECT 'classes', COUNT(*) FROM classes
UNION ALL SELECT 'teachers', COUNT(*) FROM teachers
UNION ALL SELECT 'users', COUNT(*) FROM users
UNION ALL SELECT 'roles', COUNT(*) FROM roles
UNION ALL SELECT 'role_permissions', COUNT(*) FROM role_permissions
UNION ALL SELECT 'subjects', COUNT(*) FROM subjects
UNION ALL SELECT 'silabus', COUNT(*) FROM silabus
UNION ALL SELECT 'rpp', COUNT(*) FROM rpp
UNION ALL SELECT 'absensi', COUNT(*) FROM absensi
UNION ALL SELECT 'grades', COUNT(*) FROM grades
UNION ALL SELECT 'rapor', COUNT(*) FROM rapor
UNION ALL SELECT 'announcements', COUNT(*) FROM announcements
UNION ALL SELECT 'messages', COUNT(*) FROM messages
UNION ALL SELECT 'notifications', COUNT(*) FROM notifications
""")
print("COUNTS:")
for r in counts:
    print("  ", r)
print()
print("UID_FILLED:", cur.execute("SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ''").fetchone()[0])
print("UID_SAMPLE:", cur.execute("SELECT uid_nfc FROM students LIMIT 5").fetchall())
conn.close()

print()
print("=" * 20, "BUILD GATES", "=" * 20)
for gate in ["npm run type-check", "npm run lint", "npm run build"]:
    print(">>>", gate)
    res = run(["bash", "-lc", gate])
    print("    exit:", res.returncode)
    out = (res.stdout or "").strip().splitlines()
    err = (res.stderr or "").strip().splitlines()
    for line in out[-3:]:
        print("    OUT|", line)
    for line in err[-3:]:
        print("    ERR|", line)
