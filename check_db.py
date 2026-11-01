import sqlite3, os

path = "dev.db"
print("DB exists:", os.path.exists(path))
if os.path.exists(path):
    print("DB size:", os.path.getsize(path))
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in cur.fetchall()]
    print("TABLE COUNT:", len(tables))
    for t in tables:
        cur.execute("SELECT COUNT(*) FROM " + t)
        n = cur.fetchone()[0]
        print("  " + t + ":", n)
    conn.close()
