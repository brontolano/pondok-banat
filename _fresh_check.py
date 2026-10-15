import sqlite3
con = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
con.row_factory = sqlite3.Row
cur = con.cursor()
for t in ['users','roles','role_permissions','students','classes','teachers','subjects','grades','absensi','rapor','announcements','messages','notifications','silabus','rpp']:
    try:
        n = cur.execute('SELECT COUNT(*) c FROM ' + t).fetchone()['c']
        print(t + ': ' + str(n))
    except Exception as e:
        print(t + ': ERR ' + str(e))
print('--- students per class ---')
for row in cur.execute('SELECT kelas_id, COUNT(*) c FROM students GROUP BY kelas_id ORDER BY kelas_id'):
    print(row['kelas_id'], row['c'])
print('uid_nfc filled:', cur.execute('SELECT COUNT(*) c FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != \'\'').fetchone()['c'])
print('teachers:', cur.execute('SELECT COUNT(*) c FROM teachers').fetchone()['c'])
print('subjects:', cur.execute('SELECT COUNT(*) c FROM subjects').fetchone()['c'])
print('grades:', cur.execute('SELECT COUNT(*) c FROM grades').fetchone()['c'])
