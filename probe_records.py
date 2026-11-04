import sqlite3
conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()
tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
print('Tables:', tables)
for t in tables:
    cnt = cur.execute('SELECT COUNT(*) FROM ' + t).fetchone()[0]
    print('  ' + t + ':', cnt, 'records')
conn.close()
