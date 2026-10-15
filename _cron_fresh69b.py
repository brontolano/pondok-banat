import sqlite3
conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()

cur.execute('PRAGMA table_info(classes)')
print('classes columns:', cur.fetchall())
cur.execute('PRAGMA table_info(students)')
print('students columns:', cur.fetchall())

cur.execute('SELECT id, kode, nama, seksi, jenjang, program FROM classes ORDER BY kode')
rows = cur.fetchall()
print(f'Total kelas: {len(rows)}')
for r in rows:
    print(r)

# Student per class
cur.execute("""
    SELECT c.kode, c.nama, c.seksi, c.jenjang, c.program, COUNT(s.id) as total
    FROM classes c
    LEFT JOIN students s ON s.kelas_id = c.id
    GROUP BY c.id
    ORDER BY c.kode
""")
total = 0
for r in cur.fetchall():
    print(f'  {r}')
    total += r[5]
print('TOTAL siswa:', total)

# Students sample
cur.execute('SELECT id, nisn, name, jk, ttl, kelas_id, uid_nfc FROM students LIMIT 3')
print('Sample students:')
for r in cur.fetchall():
    print(r)

conn.close()
