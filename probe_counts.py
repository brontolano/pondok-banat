import sqlite3
base = "/opt/data/home/workspace/dev/pondok-banat"
db_path = base + "/dev.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()
tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
print("TABLES (" + str(len(tables)) + "):")
for t in tables: print("  -", t)
print()
check = ['users','roles','role_permissions','students','classes','teachers','subjects','silabus','rpp','absensi','grades','rapor','announcements','messages','notifications']
for t in check:
    try:
        n = cur.execute('SELECT COUNT(*) FROM ' + t).fetchone()[0]
        print(t + ": " + str(n))
    except Exception as e:
        print(t + ": ERROR " + str(e))
conn.close()
