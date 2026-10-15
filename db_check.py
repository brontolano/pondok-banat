import sqlite3

conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
c = conn.cursor()
c.execute('SELECT COUNT(*) FROM students')
print('Students count:', c.fetchone()[0])
c.execute('SELECT name FROM sqlite_master WHERE type="table"')
print('Tables:', [r[0] for r in c.fetchall()])
c.execute('PRAGMA table_info(students)')
print('Columns:', [r[1] for r in c.fetchall()])
conn.close()
