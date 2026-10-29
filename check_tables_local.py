import sqlite3, os
path = "dev.db"
print("db exists:", os.path.exists(path))
if os.path.exists(path):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [r[0] for r in cur.fetchall()]
    print("tables:", len(tables))
    for t in tables:
        cur.execute("SELECT COUNT(*) FROM \"" + t + "\"")
        print("  %s: %d" % (t, cur.fetchone()[0]))
    conn.close()
