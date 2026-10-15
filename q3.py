import sqlite3
conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
c = conn.cursor()
c.execute('PRAGMA table_info(students)')
print('STUDENTS:', [r[1] for r in c.fetchall()])
c.execute('PRAGMA table_info(classes)')
print('CLASSES:', [r[1] for r in c.fetchall()])
c.execute('SELECT jenjang, seksi, COUNT(*) FROM students GROUP BY jenjang, seksi ORDER BY jenjang')
print('--- students per kelas ---')
for row in c.fetchall():
    print(row)
conn.close()
