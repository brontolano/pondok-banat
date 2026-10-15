import sqlite3

con = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = con.cursor()

print('=== Students columns ===')
for row in cur.execute('PRAGMA table_info(students)'):
    print(row)

print()
print('=== Teachers columns ===')
for row in cur.execute('PRAGMA table_info(teachers)'):
    print(row)

print()
print('=== Subjects columns ===')
for row in cur.execute('PRAGMA table_info(subjects)'):
    print(row)

print()
print('=== Subjects ===')
print(cur.execute('SELECT COUNT(*) FROM subjects').fetchone())
print(cur.execute('SELECT COUNT(*) FROM subjects WHERE jml_jp IS NOT NULL').fetchone())

print()
print('=== role_permissions count ===')
print(cur.execute('SELECT COUNT(*) FROM role_permissions').fetchone())

print()
print('=== Teachers status ===')
for row in cur.execute('SELECT status, COUNT(*) FROM teachers GROUP BY status'):
    print(row)

print()
print('=== Classes columns ===')
for row in cur.execute('PRAGMA table_info(classes)'):
    print(row)

print()
print('=== Classes ===')
for row in cur.execute('SELECT id, kode, nama, seksi, jenjang, program FROM classes ORDER BY jenjang, seksi'):
    print(row)

print()
print('=== role_permissions columns ===')
for row in cur.execute('PRAGMA table_info(role_permissions)'):
    print(row)

con.close()
