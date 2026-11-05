import sqlite3
conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cur.fetchall()]
print('TABLES:', tables)
print()
for t in tables:
    cur.execute('SELECT COUNT(*) FROM "' + t + '"')
    cnt = cur.fetchone()[0]
    print(t + ': ' + str(cnt) + ' records')
print('total_records:', sum(cur.execute('SELECT COUNT(*) FROM "' + t + '"').fetchone()[0] for t in tables))
conn.close()
