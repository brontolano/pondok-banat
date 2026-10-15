import sqlite3

conn = sqlite3.connect('dev.db')
cur = conn.cursor()

tables = ['users', 'roles', 'role_permissions', 'students', 'classes', 'teachers', 'subjects', 'silabus', 'rpp', 'grades', 'absensi', 'rapor', 'announcements', 'messages', 'notifications']
for t in tables:
    try:
        cur.execute('SELECT COUNT(*) FROM ' + t)
        print(t + ': ' + str(cur.fetchone()[0]))
    except Exception as e:
        print(t + ': ERROR ' + str(e))

print('--- students uid_nfc non-null: ---')
cur.execute('SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ""')
print(cur.fetchone()[0])

print('--- students active: ---')
cur.execute('SELECT COUNT(*) FROM students WHERE active = 1')
print(cur.fetchone()[0])

print('--- students inactive: ---')
cur.execute('SELECT COUNT(*) FROM students WHERE active = 0')
print(cur.fetchone()[0])

print('--- students per class ---')
cur.execute('SELECT kelas, COUNT(*) FROM students GROUP BY kelas ORDER BY kelas')
for r in cur.fetchall():
    print(r)

print('--- teachers ---')
cur.execute('SELECT COUNT(*), COALESCE(SUM(active),0) FROM teachers')
print(cur.fetchone())

print('--- role_permissions ---')
cur.execute('SELECT COUNT(*) FROM role_permissions')
print(cur.fetchone()[0])

print('--- roles + perms ---')
cur.execute('SELECT r.name, COUNT(rp.id) FROM roles r LEFT JOIN role_permissions rp ON rp.role_id = r.id GROUP BY r.id ORDER BY r.id')
for r in cur.fetchall():
    print(' ', r)

print('--- classes by jenjang ---')
cur.execute('SELECT jenjang, COUNT(*) FROM classes GROUP BY jenjang ORDER BY jenjang')
for r in cur.fetchall():
    print(' ', r)

print('--- total students ---')
cur.execute('SELECT COUNT(*) FROM students')
print(cur.fetchone()[0])

print('--- subjects ---')
cur.execute('SELECT COUNT(*) FROM subjects')
print(cur.fetchone()[0])

print('--- grades ---')
cur.execute('SELECT COUNT(*) FROM grades')
print(cur.fetchone()[0])

print('--- teachers ---')
cur.execute('SELECT COUNT(*) FROM teachers')
print(cur.fetchone()[0])

print('--- classes ---')
cur.execute('SELECT COUNT(*) FROM classes')
print(cur.fetchone()[0])

print('--- users ---')
cur.execute('SELECT COUNT(*) FROM users')
print(cur.fetchone()[0])

conn.close()
