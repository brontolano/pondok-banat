import sqlite3
conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
c = conn.cursor()
print('--- all classes ---')
c.execute('SELECT id, kode, nama, seksi, jenjang, program FROM classes ORDER BY jenjang, seksi')
for row in c.fetchall():
    print(row)
print('--- students per class (join) ---')
c.execute('''SELECT c.kode, c.nama, c.jenjang, c.seksi, c.program, COUNT(s.id) as cnt
    FROM classes c LEFT JOIN students s ON s.kelas_id = c.id
    GROUP BY c.id ORDER BY c.jenjang, c.seksi''')
for row in c.fetchall():
    print(row)
conn.close()
