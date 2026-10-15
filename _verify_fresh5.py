import sqlite3
db = '/opt/data/home/workspace/dev/pondok-banat/dev.db'
con = sqlite3.connect(db)
cur = con.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [r[0] for r in cur.fetchall()]
print('tables:', tables)
for t in tables:
    cur.execute('SELECT COUNT(*) FROM ' + t)
    print(' ', t, cur.fetchone()[0])
cur.execute("SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ''")
print('students with uid_nfc filled:', cur.fetchone()[0])
con.close()
