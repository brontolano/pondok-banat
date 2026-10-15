import sqlite3, os

base = "/opt/data/home/workspace/dev/pondok-banat"

con = sqlite3.connect(os.path.join(base, "dev.db"))
cur = con.cursor()

print("=== GRADES TABLE SCHEMA ===")
for row in cur.execute("PRAGMA table_info(grades)"):
    print(row)

print("\n=== GRADES SAMPLE (5) ===")
for row in cur.execute("SELECT * FROM grades LIMIT 5"):
    print(row)

print("\n=== GRADES TOTAL ===")
print(cur.execute("SELECT COUNT(*) FROM grades").fetchone())

print("\n=== GRADES WHERE KELAS_ID NOT NULL ===")
print(cur.execute("SELECT COUNT(*) FROM grades WHERE kelas_id IS NOT NULL").fetchone())

print("\n=== GRADE KELAS_ID DISTINCT (first 10) ===")
for r in cur.execute("SELECT DISTINCT kelas_id FROM grades LIMIT 10"):
    print(r)

print("\n=== MAPEL COUNT ===")
print(cur.execute("SELECT COUNT(*) FROM subjects").fetchone())

print("\n=== CLASSES (all) ===")
for r in cur.execute("SELECT id, kode, nama, seksi, jenjang, program, wali_kelas_id FROM classes"):
    print(r)

con.close()
