import sqlite3, os

path = "dev.db"
con = sqlite3.connect(path)
cur = con.cursor()
tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
print("DB:", path, "size:", os.path.getsize(path))
print("TABLE_COUNT:", len(tables))
for t in tables:
    try:
        n = cur.execute("SELECT COUNT(*) FROM \"" + t + "\"").fetchone()[0]
    except Exception as e:
        n = "ERR:" + str(e)
    print("  " + t + ":", n)
con.close()
