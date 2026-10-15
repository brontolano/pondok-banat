import sqlite3
conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()
tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
print('TABLES:', tables)
for t in ['users','roles','role_permissions','students','classes','teachers','subjects','silabus','rpp','absensi','grades','rapor','announcements','messages','notifications']:
    try:
        cnt = cur.execute('SELECT COUNT(*) FROM ' + t).fetchone()[0]
        print(t + ':', cnt)
    except Exception as e:
        print(t + ':', 'ERR ' + str(e))
print('students_with_uid_nfc:', cur.execute('SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ""').fetchone()[0])
print('--- classes per program ---')
for row in cur.execute('SELECT program, COUNT(*) FROM classes GROUP BY program ORDER BY program'):
    print(row)
print('--- users ---')
for row in cur.execute('SELECT id, email, role FROM users'):
    print(row)
print('--- roles ---')
for row in cur.execute('SELECT id, name FROM roles'):
    print(row)
conn.close()
