import sqlite3, os, sys
db = "dev.db"
if not os.path.exists(db):
    print("dev.db ABSENT")
    sys.exit(0)
con = sqlite3.connect(db)
cur = con.cursor()
tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
print("tables (%d): %s" % (len(tables), tables))
for t in tables:
    cnt = cur.execute("SELECT COUNT(*) FROM " + t).fetchone()[0]
    print("  %-15s %d" % (t, cnt))
con.close()
