import sqlite3
import datetime

base = '/opt/data/home/workspace/dev/pondok-banat'
db_path = base + '/dev.db'

print("=== Database Status ===")
conn = sqlite3.connect(db_path)
c = conn.cursor()

tables = ['users', 'roles', 'role_permissions', 'students', 'classes', 'teachers', 'subjects', 'silabus', 'rpp', 'absensi', 'grades', 'rapor', 'announcements', 'messages', 'notifications']
for t in tables:
    c.execute(f'SELECT COUNT(*) FROM {t}')
    print(f"  {t}: {c.fetchone()[0]}")

# Check student statuses
c.execute("SELECT COUNT(*), status FROM students GROUP BY status")
print("  Students by status:", c.fetchall())

# Check teacher statuses
c.execute("SELECT COUNT(*), status FROM teachers GROUP BY status")
print("  Teachers by status:", c.fetchall())

# Check what columns exist
c.execute("PRAGMA table_info(students)")
cols = [r[1] for r in c.fetchall()]
print("  Students columns:", cols)

if 'uid_nfc' in cols:
    c.execute("SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ''")
    print("  Students with uid_nfc:", c.fetchone()[0])
else:
    print("  uid_nfc column NOT in students table")

conn.close()

print()
print("=== File Timestamps ===")
import os
for f in ['init_db.py', 'init_schema.sql', 'prisma/schema.prisma', 'dev.db']:
    path = os.path.join(base, f)
    mtime = os.path.getmtime(path)
    dt = datetime.datetime.fromtimestamp(mtime)
    print(f"  {f}: {dt}")
