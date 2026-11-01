import sqlite3, os

db = '/opt/data/home/workspace/dev/pondok-banat/dev.db'
if not os.path.exists(db):
    print("dev.db absent")
    raise SystemExit

conn = sqlite3.connect(db)
cur = conn.cursor()
tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
print("TABLES:", tables)
for t in tables:
    cnt = cur.execute(f"SELECT COUNT(*) FROM [{t}]").fetchone()[0]
    print(f"  {t}: {cnt}")
conn.close()
