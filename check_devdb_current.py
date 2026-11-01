import sqlite3
c = sqlite3.connect('dev.db')
cur = c.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [r[0] for r in cur.fetchall()]
print("tables:", tables)
for t in tables:
    cur.execute('SELECT COUNT(*) FROM "{}"'.format(t))
    print("  {}: {}".format(t, cur.fetchone()[0]))
c.close()
