import sqlite3, os, sys

p = "dev.db"
print("=== dev.db ===")
print("exists:", os.path.exists(p))
if os.path.exists(p):
    con = sqlite3.connect(p)
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [r[0] for r in cur.fetchall()]
    print("tables:", tables)
    for t in tables:
        try:
            cur.execute("SELECT COUNT(*) FROM " + t)
            print("  " + t + ":", cur.fetchone()[0])
        except Exception as e:
            print("  " + t + ":", "ERR " + str(e))
    con.close()
