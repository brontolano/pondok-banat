import sqlite3, sys

path = sys.argv[1] if len(sys.argv) > 1 else "dev.db"
conn = sqlite3.connect(path)
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [r[0] for r in cur.fetchall()]
print("TABLES:", tables)
for t in tables:
    try:
        cur.execute('SELECT COUNT(*) FROM "%s"' % t)
        print('  %s: %d records' % (t, cur.fetchone()[0]))
    except Exception as e:
        print('  %s: ERROR %s' % (t, e))
conn.close()
