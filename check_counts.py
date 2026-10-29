import sqlite3

db_path = "/opt/data/home/workspace/dev/pondok-banat/dev.db"
con = sqlite3.connect(db_path)
cur = con.cursor()
tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
print("TABLES:", len(tables))
for t in tables:
    try:
        cnt = cur.execute("SELECT COUNT(*) FROM [" + t + "]").fetchone()[0]
        print("  " + t + ": " + str(cnt))
    except Exception as e:
        print("  " + t + ": ERROR " + str(e))
con.close()
