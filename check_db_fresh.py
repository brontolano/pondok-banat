import sqlite3, os

REPO = "/opt/data/home/workspace/dev/pondok-banat"
db = os.path.join(REPO, "dev.db")
con = sqlite3.connect(db)
cur = con.cursor()

# Table list
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [r[0] for r in cur.fetchall()]
print("TABLE_COUNT:", len(tables))
for t in tables:
    cur.execute("SELECT COUNT(*) FROM [%s]" % t)
    print("RECORD_COUNT %s: %d" % (t, cur.fetchone()[0]))

# schema info for students table
cur.execute("SELECT sql FROM sqlite_master WHERE name='students'")
row = cur.fetchone()
print("STUDENTS_SCHEMA:")
print(row[0] if row else "NOT FOUND")
con.close()
