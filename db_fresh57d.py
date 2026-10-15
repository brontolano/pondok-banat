import sqlite3

con = sqlite3.connect("dev.db")
cur = con.cursor()

print("classes schema:")
for r in cur.execute("PRAGMA table_info(classes)"):
    print("  ", r[1], r[2])

print("\nclasses sample (12):")
for r in cur.execute("SELECT id, kode, nama, seksi, jenjang, program, wali_kelas_id FROM classes ORDER BY id LIMIT 12").fetchall():
    print("  ", r)

print("\nStudents per kelas_id -> class kode/jenjang:")
rows = cur.execute("""
  SELECT c.kode, c.jenjang, c.seksi, COUNT(s.id) 
  FROM students s JOIN classes c ON s.kelas_id = c.id 
  GROUP BY c.id ORDER BY c.id
""").fetchall()
tot = 0
for k, j, s, cnt in rows:
    print("  class id=%s kode=%r jenjang=%r seksi=%r -> %s" % (k, k, j, s, cnt))
    tot += cnt
print("  TOTAL:", tot)

con.close()
