import sqlite3, os

repo = "/opt/data/home/workspace/dev/pondok-banat"
conn = sqlite3.connect(os.path.join(repo, "dev.db"))
cur = conn.cursor()
tables = ["students","teachers","classes","subjects","silabus","rpp","grades","absensi","rapor","announcements","messages","notifications","users","roles","role_permissions"]
total = 0
for t in tables:
    n = cur.execute("SELECT COUNT(*) FROM " + t).fetchone()[0]
    total += n
    print(t, n)
print("TOTAL", total)
r = cur.execute('SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ""').fetchone()[0]
print("UID_NFC filled:", r)
conn.close()
