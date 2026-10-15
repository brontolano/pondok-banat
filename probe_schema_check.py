import sqlite3
conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()
cur.execute('SELECT sql FROM sqlite_master WHERE type="table" AND name="students"')
row = cur.fetchone()
print(row[0] if row else 'no schema found')
conn.close()
