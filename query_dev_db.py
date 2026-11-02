import sqlite3, sys

conn = sqlite3.connect('dev.db')
cur = conn.cursor()
tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
print('TABLES:', tables)
print()
for t in tables:
    try:
        count = cur.execute('SELECT COUNT(*) FROM "%s"' % t).fetchone()[0]
    except Exception as e:
        count = 'ERR: %s' % e
    print('%s: %s records' % (t, count))
conn.close()
