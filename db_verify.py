import sqlite3
conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()
tables = ['students', 'teachers', 'grades', 'classes', 'subjects', 'users', 'roles', 'role_permissions', 'announcements', 'messages', 'notifications', 'silabus', 'rpp', 'absensi', 'rapor']
for t in tables:
    try:
        cur.execute(f'SELECT COUNT(*) FROM {t}')
        print(f'{t}:', cur.fetchone()[0])
    except Exception as e:
        print(f'{t}: ERROR {e}')
cur.execute('SELECT status, COUNT(*) FROM students GROUP BY status')
print('student statuses:', cur.fetchall())
cur.execute('SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ""')
print('students with uid_nfc filled:', cur.fetchone()[0])
cur.execute('SELECT program, COUNT(*) FROM students GROUP BY program')
for row in cur.fetchall():
    print('class dist:', row)
cur.execute('SELECT COUNT(*) FROM students')
print('total students:', cur.fetchone()[0])
conn.close()
