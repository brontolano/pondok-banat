import sqlite3
con = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = con.cursor()
print("students columns:", [r[1] for r in cur.execute("PRAGMA table_info(students)")])
print("classes columns:", [r[1] for r in cur.execute("PRAGMA table_info(classes)")])
print()
print("--- classes distribution ---")
rows = cur.execute("SELECT kode, nama, seksi, jenjang, program, COUNT(*) FROM students GROUP BY kode, nama, seksi, jenjang, program ORDER BY kode").fetchall()
for r in rows:
    print("  ", r)
print("TOTAL:", cur.execute("SELECT COUNT(*) FROM students").fetchone()[0])
print()
# teacher columns check
print("teacher columns:", [r[1] for r in cur.execute("PRAGMA table_info(teachers)")])
print("teacher sample:", cur.execute("SELECT COUNT(*), MIN(id) FROM teachers").fetchone())
