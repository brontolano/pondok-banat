import sqlite3, sys
path = sys.argv[1] if len(sys.argv) > 1 else 'dev.db'
con = sqlite3.connect(path)
cur = con.cursor()
tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
print('TABLES:', tables)
for t in tables:
    try:
        n = cur.execute('SELECT COUNT(*) FROM ' + t).fetchone()[0]
        print(t + ': ' + str(n))
    except Exception as e:
        print(t + ': ERROR ' + str(e))
