import sqlite3
con = sqlite3.connect('dev.db')
print("=== ALL classes ===")
rows = con.execute("SELECT id, kode, nama, seksi, jenjang, program FROM classes ORDER BY id")
for r in rows:
    print(r)
print("count:", con.execute('SELECT COUNT(*) FROM classes').fetchone()[0])
print("=== programs ===")
rows = con.execute("SELECT DISTINCT program FROM classes ORDER BY program")
for r in rows:
    print(r)
print("=== jenjang values ===")
rows = con.execute("SELECT DISTINCT jenjang FROM classes ORDER BY jenjang")
for r in rows:
    print(r)
