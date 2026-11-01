import sqlite3
conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()
tables = ['users','roles','role_permissions','students','classes','teachers','subjects','silabus','rpp','absensi','grades','rapor','announcements','messages','notifications']
for t in tables:
    cur.execute('SELECT COUNT(*) FROM ' + t)
    print(t + ': ' + str(cur.fetchone()[0]))
print('--- uid_nfc filled students ---')
cur.execute('SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != \'\'')
print('students with uid_nfc filled: ' + str(cur.fetchone()[0]))
conn.close()
