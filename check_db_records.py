import sqlite3, os
base = "/opt/data/home/workspace/dev/pondok-banat"
conn = sqlite3.connect(os.path.join(base, "dev.db"))
cur = conn.cursor()
tables = ["users","roles","role_permissions","students","classes","teachers","subjects","silabus","rpp","absensi","grades","rapor","announcements","messages","notifications"]
for t in tables:
    try:
        cur.execute("SELECT COUNT(*) FROM " + t)
        print(t + ": " + str(cur.fetchone()[0]))
    except Exception as e:
        print(t + ": ERROR " + str(e))
conn.close()
