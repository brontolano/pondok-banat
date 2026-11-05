import sqlite3, os
path = "/opt/data/home/workspace/dev/pondok-banat/dev.db"
print("dev.db exists:", os.path.exists(path))
if os.path.exists(path):
    print("dev.db size:", os.path.getsize(path))
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [r[0] for r in cur.fetchall()]
    print("Tables (%d):" % len(tables))
    total = 0
    for t in tables:
        cur.execute("SELECT COUNT(*) FROM \"%s\"" % t)
        cnt = cur.fetchone()[0]
        total += cnt
        print("  %s: %d rows" % (t, cnt))
    print("TOTAL rows:", total)
    conn.close()
