import sqlite3

conn = sqlite3.connect('dev.db')
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [r[0] for r in cur.fetchall()]
print('TABLES:', tables)
print('COUNT:', len(tables))
for t in tables:
    try:
        cur.execute('SELECT COUNT(*) FROM "' + t + '"')
        cnt = cur.fetchone()[0]
        print('  ' + t + ': ' + str(cnt) + ' records')
    except Exception as e:
        print('  ' + t + ': ERROR ' + str(e))
conn.close()
