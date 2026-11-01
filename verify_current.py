import sqlite3, os

repo = "/opt/data/home/workspace/dev/pondok-banat"
conn = sqlite3.connect(repo + "/dev.db")
cur = conn.cursor()
tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
print("TABLES:", len(tables))
total = 0
for t in tables:
    cnt = cur.execute('SELECT COUNT(*) FROM "' + t + '"').fetchone()[0]
    total += cnt
    print("  " + t + ":", cnt)
print("TOTAL_ROWS:", total)
n = cur.execute('SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ""').fetchone()[0]
print("students_with_uid_nfc:", n)
conn.close()

print("node_modules exists:", os.path.isdir(repo + "/node_modules"))
print(".next exists:", os.path.isdir(repo + "/.next"))
print("dev.db size:", os.path.getsize(repo + "/dev.db"))
print("node_modules dirs:", len([d for d in os.listdir(repo + "/node_modules") if os.path.isdir(repo + "/node_modules/" + d)]))
