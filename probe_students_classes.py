import sqlite3

base = "/opt/data/home/workspace/dev/pondok-banat"
con = sqlite3.connect(base + "/dev.db")
cur = con.cursor()

# Check students count by status
print("=== Students by status ===")
for row in cur.execute("SELECT status, COUNT(*) as cnt FROM students GROUP BY status"):
    print(row)

# Check students count by class
print("\n=== Students count by class ===")
for row in cur.execute("SELECT c.kode, c.nama, c.seksi, COUNT(s.id) as cnt FROM classes c LEFT JOIN students s ON c.id = s.kelas_id GROUP BY c.id ORDER BY c.id"):
    print(row)

# Check classes
print("\n=== All classes ===")
for row in cur.execute("SELECT kode, nama, seksi, jenjang, program FROM classes ORDER BY jenjang, seksi"):
    print(row)

# Check teachers count by jabatan
print("\n=== Teachers by jabatan (top 15) ===")
for row in cur.execute("SELECT jabatan, COUNT(*) as cnt FROM teachers GROUP BY jabatan ORDER BY cnt DESC LIMIT 15"):
    print(row)

con.close()
