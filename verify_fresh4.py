import sqlite3

db = "dev.db"
con = sqlite3.connect(db)
cur = con.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [r[0] for r in cur.fetchall()]
print("TABLES:", len(tables))
for t in tables:
    cur.execute("SELECT COUNT(*) FROM " + t)
    print(" ", t, cur.fetchone()[0])
if "students" in tables:
    cur.execute(
        "SELECT COUNT(*), SUM(CASE WHEN uid_nfc IS NOT NULL AND uid_nfc != '' THEN 1 ELSE 0 END) FROM students"
    )
    print("students uid_nfc:", cur.fetchone())
con.close()
