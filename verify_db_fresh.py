import sqlite3

conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()

tables = ['users','roles','role_permissions','students','classes','teachers','subjects','silabus','rpp','absensi','grades','rapor','announcements','messages','notifications']
for t in tables:
    try:
        cur.execute('SELECT COUNT(*) FROM ' + t)
        print(t + ': ' + str(cur.fetchone()[0]))
    except Exception as e:
        print(t + ': ERROR ' + str(e))

print('--- students per kelas ---')
cur.execute('SELECT kelas, COUNT(*) FROM students GROUP BY kelas ORDER BY kelas')
for r in cur.fetchall():
    print(r)
print('--- students total: ' + str(cur.execute('SELECT COUNT(*) FROM students').fetchone()[0]))
print('--- uid_nfc filled: ' + str(cur.execute("SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ''").fetchone()[0]))

cur.execute('SELECT COUNT(*) FROM classes')
print('--- classes total: ' + str(cur.execute('SELECT COUNT(*) FROM classes').fetchone()[0]))

cur.execute('SELECT COUNT(*) FROM subjects')
print('--- subjects total: ' + str(cur.execute('SELECT COUNT(*) FROM subjects').fetchone()[0]))

cur.execute('SELECT COUNT(*) FROM rpp')
print('--- rpp total: ' + str(cur.execute('SELECT COUNT(*) FROM rpp').fetchone()[0]))

cur.execute('SELECT COUNT(*) FROM silabus')
print('--- silabus total: ' + str(cur.execute('SELECT COUNT(*) FROM silabus').fetchone()[0]))

cur.execute('SELECT COUNT(*) FROM grades')
print('--- grades total: ' + str(cur.execute('SELECT COUNT(*) FROM grades').fetchone()[0]))

cur.execute('SELECT COUNT(*) FROM users')
print('--- users total: ' + str(cur.execute('SELECT COUNT(*) FROM users').fetchone()[0]))
cur.execute('SELECT COUNT(*) FROM roles')
print('--- roles total: ' + str(cur.execute('SELECT COUNT(*) FROM roles').fetchone()[0]))
cur.execute('SELECT COUNT(*) FROM role_permissions')
print('--- role_permissions total: ' + str(cur.execute('SELECT COUNT(*) FROM role_permissions').fetchone()[0]))

conn.close()
