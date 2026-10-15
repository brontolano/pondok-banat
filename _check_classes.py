import sqlite3

DB = "/opt/data/home/workspace/dev/pondok-banat/dev.db"
conn = sqlite3.connect(DB)
cur = conn.cursor()

print("=== CLASSES TABLE COLUMNS ===")
cols = cur.execute("PRAGMA table_info(classes)").fetchall()
for c in cols:
    print(f"  {c[1]}: {c[2]}")

print("\n=== CLASSES DATA (sample) ===")
for row in cur.execute(
    "SELECT id, kode, nama, seksi, jenjang, program, wali_kelas_id FROM classes ORDER BY jenjang, seksi, kode"
).fetchall():
    print(row)

conn.close()
