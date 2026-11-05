import sqlite3, os

path = "/opt/data/home/workspace/dev/pondok-banat/dev.db"
print("DB exists:", os.path.exists(path))
print("DB size:", os.path.getsize(path) if os.path.exists(path) else 0)

con = sqlite3.connect(path)
cur = con.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [r[0] for r in cur.fetchall()]
print("TABLE COUNT:", len(tables))
for t in tables:
    cur.execute('SELECT COUNT(*) FROM "%s"' % t)
    print("  %s: %d" % (t, cur.fetchone()[0]))
