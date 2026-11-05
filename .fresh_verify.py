import sqlite3, os, json

base = "/opt/data/home/workspace/dev/pondok-banat"
db_path = os.path.join(base, "dev.db")

print("DB exists:", os.path.exists(db_path))
if not os.path.exists(db_path):
    print("DB absent")
    exit(0)

conn = sqlite3.connect(db_path)
cur = conn.cursor()
tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
print("TABLES:", len(tables))
for t in tables:
    try:
        cnt = cur.execute('SELECT COUNT(*) FROM "' + t + '"').fetchone()[0]
    except Exception as e:
        cnt = "ERR:" + str(e)
    print(" ", t, ":", cnt)
conn.close()
