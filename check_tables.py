import sqlite3
conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cur.fetchall()]
print('TABLES:', len(tables))
for t in sorted(tables):
    cur.execute('SELECT COUNT(*) FROM "%s"' % t)
    cnt = cur.fetchone()[0]
    print('  %s: %d' % (t, cnt))
conn.close()
