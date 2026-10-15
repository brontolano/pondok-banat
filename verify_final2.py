import sqlite3

con = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = con.cursor()

print('=== Students per class (ID, kode, name, seksi, jenjang, program, count) ===')
rows = cur.execute('''
    SELECT c.id, c.kode, c.nama, c.seksi, c.jenjang, c.program, COUNT(s.id)
    FROM classes c
    LEFT JOIN students s ON s.kelas_id = c.id
    GROUP BY c.id
    ORDER BY c.program, c.seksi
''').fetchall()
total = 0
for r in rows:
    print(r)
    total += r[6]
print('TOTAL students:', total)

print()
print('=== Student status distribution ===')
for row in cur.execute('SELECT status, COUNT(*) FROM students GROUP BY status'):
    print(row)

print('uid_nfc filled:', cur.execute("SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ''").fetchone()[0])

print()
print('=== Teachers ===')
print(cur.execute('SELECT COUNT(*), SUM(status) FROM teachers').fetchone())

print()
print('=== Subjects active ===')
print(cur.execute('SELECT COUNT(*), SUM(active) FROM subjects').fetchone())

print()
print('=== Grades ===')
print(cur.execute('SELECT COUNT(*), COUNT(DISTINCT mapel_id) FROM grades').fetchone())

print()
print('=== Roles / RolePermissions ===')
print(cur.execute('SELECT COUNT(*) FROM role_permissions').fetchone())
print('Roles:')
for row in cur.execute('SELECT id, name FROM roles'):
    print(row)

print()
print('=== Teachers columns ===')
for row in cur.execute('PRAGMA table_info(teachers)'):
    print(row)

print()
print('=== All classes ===')
for row in cur.execute('SELECT id, kode, nama, seksi, jenjang, program FROM classes ORDER BY jenjang, seksi'):
    print(row)

con.close()
