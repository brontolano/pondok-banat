import sqlite3, os
db = '/opt/data/home/workspace/dev/pondok-banat/dev.db'
print('dev.db exists:', os.path.exists(db), 'size:', os.path.getsize(db))
conn = sqlite3.connect(db)
cur = conn.cursor()
tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
print('Tables (%d): %s' % (len(tables), tables))
for t in tables:
    c = cur.execute('SELECT COUNT(*) FROM ' + t).fetchone()[0]
    print('  ' + t + ': ' + str(c))
conn.close()
