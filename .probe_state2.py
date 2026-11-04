import sqlite3
conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [r[0] for r in cur.fetchall()]
print('Tables:', tables)
print('Count:', len(tables))
for t in tables:
    cur.execute('SELECT COUNT(*) FROM "' + t + '"')
    print('  ' + t + ':', cur.fetchone()[0], 'records')
conn.close()
