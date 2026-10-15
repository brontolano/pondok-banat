import sqlite3
c = sqlite3.connect("/opt/data/home/workspace/dev/pondok-banat/dev.db")
c.row_factory = sqlite3.Row
cur = c.cursor()
cur.execute("SELECT kelas_id, COUNT(*) as cnt FROM students GROUP BY kelas_id ORDER BY kelas_id")
rows = cur.fetchall()
print("TOTAL:", sum(r["cnt"] for r in rows))
for r in rows:
    print(r["kelas_id"], r["cnt"])
cur.execute("SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != \"\"")
print("uid_nfc filled:", cur.fetchone()[0])
cur.execute("SELECT COUNT(*) FROM students WHERE active=1")
print("active:", cur.fetchone()[0])
c.close()
