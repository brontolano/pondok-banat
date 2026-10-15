import sqlite3
import json

conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()

# Get all tables and counts
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [r[0] for r in cur.fetchall()]
print("TABLES:", tables)
print()

counts = {}
for t in tables:
    cur.execute("SELECT COUNT(*) FROM [%s]" % t)
    counts[t] = cur.fetchone()[0]
    print("  %s: %d" % (t, counts[t]))

print()
# Students per class
cur.execute("SELECT kelas_id, COUNT(*) FROM students GROUP BY kelas_id ORDER BY kelas_id")
print("STUDENTS BY CLASS:")
for row in cur.fetchall():
    print("  ", row)
print("TOTAL students:", counts['students'])

# uid_nfc filled
cur.execute("SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ''")
print("Students with uid_nfc filled:", cur.fetchone()[0])

# Roles
cur.execute("SELECT COUNT(*) FROM roles")
print("Roles:", cur.fetchone()[0])
cur.execute("SELECT COUNT(*) FROM role_permissions")
print("Role permissions:", cur.fetchone()[0])
cur.execute("SELECT COUNT(*) FROM users")
print("Users:", cur.fetchone()[0])

# Grades
cur.execute("SELECT COUNT(*) FROM grades")
print("Grades:", cur.fetchone()[0])

# Subjects
cur.execute("SELECT COUNT(*) FROM subjects")
print("Subjects:", cur.fetchone()[0])
cur.execute("SELECT COUNT(*) FROM silabus")
print("Silabus:", cur.fetchone()[0])
cur.execute("SELECT COUNT(*) FROM rpp")
print("RPP:", cur.fetchone()[0])

# Teachers
cur.execute("SELECT COUNT(*) FROM teachers")
print("Teachers:", cur.fetchone()[0])

# Classes
cur.execute("SELECT COUNT(*) FROM classes")
print("Classes:", cur.fetchone()[0])

# Announcements, messages, notifications
for t in ['announcements', 'messages', 'notifications']:
    cur.execute("SELECT COUNT(*) FROM [%s]" % t)
    print("%s: %d" % (t, cur.fetchone()[0]))

# Check PRISMA schema for KitabProgress & Sertakan
cur.execute("SELECT sql FROM sqlite_master WHERE name='Students'")
print()
print("Students table schema:")
print(cur.fetchone()[0])

conn.close()
