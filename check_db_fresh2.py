import sqlite3, os, json

db = "/opt/data/home/workspace/dev/pondok-banat/dev.db"
con = sqlite3.connect(db)
cur = con.cursor()

print("=== DB TABLES ===")
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [r[0] for r in cur.fetchall()]
for t in tables:
    cur.execute("SELECT COUNT(*) FROM [%s]" % t)
    print("  %s: %d" % (t, cur.fetchone()[0]))

print("=== STUDENTS per kelas ===")
cur.execute("SELECT kelas, COUNT(*) FROM students GROUP BY kelas ORDER BY kelas")
for row in cur.fetchall():
    print("  %s: %d" % (row[0], row[1]))

cur.execute("SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ''")
print("students with uid_nfc filled:", cur.fetchone()[0])

print("=== ROLES ===")
cur.execute("SELECT COUNT(*) FROM roles")
print("  roles:", cur.fetchone()[0])
cur.execute("SELECT COUNT(*) FROM role_permissions")
print("  role_permissions:", cur.fetchone()[0])
cur.execute("SELECT COUNT(*) FROM users")
print("  users:", cur.fetchone()[0])

con.close()
print("=== FILE STATE ===")
print("dev.db size:", os.path.getsize(db))
print("prisma/schema.prisma exists:", os.path.exists("/opt/data/home/workspace/dev/pondok-banat/prisma/schema.prisma"))
