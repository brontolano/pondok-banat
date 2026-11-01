import sqlite3
conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()
print('=== TABLES ===')
for row in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
    print('TABLE:', row[0])
print('=== ROW COUNTS ===')
for (t,) in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
    try:
        n = cur.execute('SELECT COUNT(*) FROM "%s"' % t).fetchone()[0]
        print(t, n)
    except Exception as e:
        print(t, 'ERR', e)
conn.close()
