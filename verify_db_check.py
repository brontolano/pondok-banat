import sqlite3, os, sys

path = "/opt/data/home/workspace/dev/pondok-banat/dev.db"
print("dev.db exists:", os.path.exists(path))
if os.path.exists(path):
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in cur.fetchall()]
    print("Tables:", tables)
    for t in tables:
        try:
            cur.execute("SELECT COUNT(*) FROM " + t)
            print(f"  {t}: {cur.fetchone()[0]}")
        except Exception as e:
            print(f"  {t}: ERROR {e}")
    con.close()
