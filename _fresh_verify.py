import sqlite3
conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()
tables = ['users','roles','role_permissions','students','classes','teachers','subjects','silabus','rpp','absensi','grades','rapor','announcements','messages','notifications']
for t in tables:
    cur.execute('SELECT COUNT(*) FROM ' + t)
    print(t + ': ' + str(cur.fetchone()[0]))
print('--- students per class ---')
cur.execute('SELECT kelas_id, COUNT(*) FROM students GROUP BY kelas_id ORDER BY kelas_id')
for row in cur.fetchall():
    print(row)
print('--- students with uid_nfc ---')
cur.execute("SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ''")
print(cur.fetchone()[0])
print('--- teachers ---')
cur.execute('SELECT COUNT(*) FROM teachers')
print(cur.fetchone()[0])
print('--- subjects ---')
cur.execute('SELECT COUNT(*) FROM subjects')
print(cur.fetchone()[0])
print('--- grades ---')
cur.execute('SELECT COUNT(*) FROM grades')
print(cur.fetchone()[0])
conn.close()
