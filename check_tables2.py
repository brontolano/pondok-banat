import sqlite3
conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [r[0] for r in cur.fetchall()]
print('TOTAL TABLES:', len(tables))
print(tables)
for t in tables:
    cur.execute('SELECT COUNT(*) FROM "' + t + '"')
    print('  ' + t + ': ' + str(cur.fetchone()[0]) + ' rows')
conn.close()
