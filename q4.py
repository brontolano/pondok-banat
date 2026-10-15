import sqlite3
conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
c = conn.cursor()
c.execute('SELECT s.status, COUNT(*) FROM students s GROUP BY s.status')
print('STATUS:', c.fetchall())
c.execute('SELECT c.jenjang, c.seksi, COUNT(*) FROM students s JOIN classes c ON s.kelas_id = c.id GROUP BY c.jenjang, c.seksi ORDER BY c.jenjang')
print('--- students per kelas ---')
for row in c.fetchall():
    print(row)
conn.close()
