import sqlite3
con = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = con.cursor()
rows = cur.execute("""
SELECT c.kode, c.nama, c.seksi, c.jenjang, c.program, COUNT(*) AS jum
FROM students s
JOIN classes c ON s.kelas_id = c.id
GROUP BY c.kode, c.nama, c.seksi, c.jenjang, c.program
ORDER BY c.jenjang, c.seksi
""").fetchall()
print("--- students per kelas (kelas_id -> classes) ---")
for r in rows:
    print("  ", r)
print("TOTAL:", cur.execute("SELECT COUNT(*) FROM students").fetchone()[0])
print("classes count:", cur.execute("SELECT COUNT(*) FROM classes").fetchone()[0])
print()
print("--- classes table all 18 ---")
for r in cur.execute("SELECT id, kode, nama, seksi, jenjang, program FROM classes ORDER BY jenjang, seksi").fetchall():
    print("  ", r)
