import sqlite3
base = "/opt/data/home/workspace/dev/pondok-banat"
conn = sqlite3.connect(base + "/dev.db")
cur = conn.cursor()
tables = ['users','roles','role_permissions','students','classes','teachers','subjects','silabus','rpp','absensi','grades','rapor','announcements','messages','notifications','kitab_progress']
for t in tables:
    try:
        cur.execute('SELECT COUNT(*) FROM ' + t)
        n = cur.fetchone()[0]
        print(t + ': ' + str(n))
    except Exception as e:
        print(t + ': ERROR ' + str(e))
print()
print('=== uid_nfc sample ===')
cur.execute('SELECT id, nisn, name, kelas_id, uid_nfc FROM students LIMIT 5')
for r in cur.fetchall():
    print(r)
print('uid_nfc non-null count:', cur.execute('SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL').fetchone()[0])
print('active students:', cur.execute('SELECT COUNT(*) FROM students WHERE status="active"').fetchone()[0])
print('inactive students:', cur.execute('SELECT COUNT(*) FROM students WHERE status="inactive"').fetchone()[0])
conn.close()
