import sqlite3, os
path = '/opt/data/home/workspace/dev/pondok-banat/dev.db'
print('dev.db exists:', os.path.exists(path), 'size:', os.path.getsize(path) if os.path.exists(path) else 'N/A')
conn = sqlite3.connect(path)
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cur.fetchall()]
print('TABLE COUNT:', len(tables))
for t in sorted(tables):
    cur.execute('SELECT COUNT(*) FROM "' + t + '"')
    cnt = cur.fetchone()[0]
    print('  ' + t + ':', cnt)
conn.close()
