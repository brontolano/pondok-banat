import sqlite3
con = sqlite3.connect("/opt/data/home/workspace/dev/pondok-banat/dev.db")
cur = con.cursor()
tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
print("TABLE_COUNT:", len(tables))
for t in tables:
    try:
        cnt = cur.execute("SELECT COUNT(*) FROM [" + t + "]").fetchone()[0]
    except Exception as e:
        cnt = "ERR:" + str(e)
    print("  " + t + ":", cnt)
uid = cur.execute("SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ''").fetchone()[0]
print("UID_FILLED:", uid)
con.close()
