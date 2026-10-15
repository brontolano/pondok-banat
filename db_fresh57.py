import sqlite3, os

repo = "/opt/data/home/workspace/dev/pondok-banat"
db = os.path.join(repo, "dev.db")
con = sqlite3.connect(db)
cur = con.cursor()

tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
print("Total tables:", len(tables))

print("\nPer-table row counts:")
for t in tables:
    print("  %s: %s" % (t, cur.execute("SELECT COUNT(*) FROM [" + t + "]").fetchone()[0]))

dist = cur.execute("SELECT kelas, COUNT(*) FROM students GROUP BY kelas ORDER BY kelas").fetchall()
print("\nStudents per kelas:")
for k, v in dist:
    print("  %s: %s" % (k, v))
print("  TOTAL:", sum(v for _, v in dist))

print("\nuid_nfc non-null:", cur.execute("SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND TRIM(uid_nfc)!=''").fetchone()[0])
print("Admin user:", cur.execute("SELECT email, role FROM users LIMIT 1").fetchone())
print("Users:", cur.execute("SELECT COUNT(*) FROM users").fetchone()[0])
print("Roles:", cur.execute("SELECT COUNT(*) FROM roles").fetchone()[0])
print("Role_permissions:", cur.execute("SELECT COUNT(*) FROM role_permissions").fetchone()[0])
print("Teachers:", cur.execute("SELECT COUNT(*) FROM teachers").fetchone()[0])
print("Subjects:", cur.execute("SELECT COUNT(*) FROM subjects").fetchone()[0])
print("Grades:", cur.execute("SELECT COUNT(*) FROM grades").fetchone()[0])
print("Classes:", cur.execute("SELECT COUNT(*) FROM classes").fetchone()[0])
print("Students active=0:", cur.execute("SELECT COUNT(*) FROM students WHERE active=0").fetchone()[0])
print("Announcements:", cur.execute("SELECT COUNT(*) FROM announcements").fetchone()[0])
print("Messages:", cur.execute("SELECT COUNT(*) FROM messages").fetchone()[0])
print("Notifications:", cur.execute("SELECT COUNT(*) FROM notifications").fetchone()[0])

con.close()
