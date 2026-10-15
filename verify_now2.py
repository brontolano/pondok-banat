import sqlite3
c = sqlite3.connect("/opt/data/home/workspace/dev/pondok-banat/dev.db")
cur = c.cursor()
c.row_factory = sqlite3.Row
# Students per class name
cur.execute("""
    SELECT s.kelas_id, k.nama, k.kode, k.jenjang, k.program, COUNT(s.id) as cnt
    FROM students s
    JOIN classes k ON s.kelas_id = k.id
    GROUP BY s.kelas_id, k.nama, k.kode, k.jenjang, k.program
    ORDER BY k.jenjang, k.kode
""")
rows = cur.fetchall()
print("STUDENT DISTRIBUTION:")
total = 0
for r in rows:
    print(f"  {r['jenjang']} {r['kode']} {r['program'] or ''}: {r['cnt']}")
    total += r['cnt']
print("  TOTAL:", total)
# uid_nfc
cur.execute("SELECT COUNT(*) FROM students WHERE uidNfc IS NOT NULL AND uidNfc != ''")
print("Students with uid_nfc filled:", cur.fetchone()[0])
# status
cur.execute("SELECT status, COUNT(*) FROM students GROUP BY status")
for r in cur.fetchall():
    print(f"Status {r['status']}: {r['COUNT(*)']}")
# role counts
cur.execute("SELECT COUNT(*) FROM users")
print("users:", cur.fetchone()[0])
cur.execute("SELECT COUNT(*) FROM roles")
print("roles:", cur.fetchone()[0])
cur.execute("SELECT COUNT(*) FROM role_permissions")
print("role_permissions:", cur.fetchone()[0])
cur.execute("SELECT COUNT(*) FROM teachers")
print("teachers:", cur.fetchone()[0])
cur.execute("SELECT COUNT(*) FROM subjects")
print("subjects:", cur.fetchone()[0])
cur.execute("SELECT COUNT(*) FROM grades")
print("grades:", cur.fetchone()[0])
for t in ["silabus","rpp","absensi","rapor","announcements","messages","notifications"]:
    cur.execute("SELECT COUNT(*) FROM " + t)
    print(t + ":", cur.fetchone()[0])
c.close()
