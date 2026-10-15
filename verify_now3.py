import sqlite3
c = sqlite3.connect("/opt/data/home/workspace/dev/pondok-banat/dev.db")
c.row_factory = sqlite3.Row
cur = c.cursor()
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
    print("  " + str(r["jenjang"]) + " " + str(r["kode"]) + " " + str(r["program"] or "") + ": " + str(r["cnt"]))
    total += r["cnt"]
print("  TOTAL:", total)
cur.execute("SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ''")
print("Students with uid_nfc filled:", cur.fetchone()[0])
cur.execute("SELECT status, COUNT(*) FROM students GROUP BY status")
for r in cur.fetchall():
    print("Status " + str(r["status"]) + ": " + str(r["COUNT(*)"]))
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
