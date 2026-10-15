import sqlite3
conn = sqlite3.connect('dev.db')
cur = conn.cursor()
tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
print('TABLES:', tables)
for t in tables:
    cnt = cur.execute('SELECT COUNT(*) FROM "' + t + '"').fetchone()[0]
    print('  ' + t + ': ' + str(cnt))
print('--- students sample ---')
for row in cur.execute('SELECT id, nama, status, uid_nfc FROM students LIMIT 5').fetchall():
    print(row)
print('--- kelas count ---')
print(cur.execute('SELECT COUNT(*) FROM classes').fetchone()[0])
print('--- teacher count ---')
print(cur.execute('SELECT COUNT(*) FROM teachers').fetchone()[0])
print('--- users ---')
for row in cur.execute('SELECT id, email, role FROM users LIMIT 5').fetchall():
    print(row)
print('--- roles ---')
for row in cur.execute('SELECT id, name FROM roles LIMIT 10').fetchall():
    print(row)
print('--- role_permissions ---')
print('count:', cur.execute('SELECT COUNT(*) FROM role_permissions').fetchone()[0])
conn.close()
