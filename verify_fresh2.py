import sqlite3

conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()

cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
print('total_tables:', cur.fetchone()[0])

for table in ['students', 'teachers', 'subjects', 'grades', 'users', 'roles', 'role_permissions']:
    try:
        cur.execute('SELECT COUNT(*) FROM ' + table)
        print(table + '_total:', cur.fetchone()[0])
    except Exception as e:
        print(table, 'ERROR:', e)

cur.execute('SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ""')
print('students_uid_filled:', cur.fetchone()[0])

cur.execute('SELECT kelas, COUNT(*) FROM students GROUP BY kelas ORDER BY kelas')
rows = cur.fetchall()
total = 0
for r in rows:
    print('class', r[0], r[1])
    total += r[1]
print('per_class_total:', total)

conn.close()
