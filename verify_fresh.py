import sqlite3, os

base = '/opt/data/home/workspace/dev/pondok-banat'
c = sqlite3.connect(base + '/dev.db')
cur = c.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [r[0] for r in cur.fetchall()]
print('TABLES:')
for t in tables:
    cur.execute('SELECT COUNT(*) FROM "' + t + '"')
    print('  ' + t + ':', cur.fetchone()[0])
c.close()
print('dev.db size:', os.path.getsize(base + '/dev.db'))
