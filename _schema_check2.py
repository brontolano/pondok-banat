import sqlite3
conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()
cur.execute('PRAGMA table_info(students)')
for row in cur.fetchall():
    print(row)
