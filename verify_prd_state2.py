import sqlite3
conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()

print('=== role_permissions schema ===')
for row in cur.execute('PRAGMA table_info(role_permissions)'):
    print(row)

print()
print('=== role_permissions sample + count ===')
for row in cur.execute('SELECT * FROM role_permissions LIMIT 5'):
    print(row)
print('Count:', cur.execute('SELECT COUNT(*) FROM role_permissions').fetchone()[0])

print()
print('=== STUDENTS sample + count ===')
for row in cur.execute('SELECT * FROM students LIMIT 3'):
    print(row)
print('Count:', cur.execute('SELECT COUNT(*) FROM students').fetchone()[0])

print()
print('=== TEACHERS count + active ===')
for row in cur.execute('SELECT COUNT(*), SUM(CASE WHEN status="active" THEN 1 ELSE 0 END) FROM teachers'):
    print(row)

print()
print('=== SUBJECTS count ===')
for row in cur.execute('SELECT COUNT(*) FROM subjects'):
    print(row)

print()
print('=== GRADES count ===')
for row in cur.execute('SELECT COUNT(*) FROM grades'):
    print(row)

print()
print('=== ABSENSI count ===')
for row in cur.execute('SELECT COUNT(*) FROM absensi'):
    print(row)

print()
print('=== RAPOR count ===')
for row in cur.execute('SELECT COUNT(*) FROM rapor'):
    print(row)

print()
print('=== ANNOUNCEMENTS count ===')
for row in cur.execute('SELECT COUNT(*) FROM announcements'):
    print(row)

print()
print('=== MESSAGES count ===')
for row in cur.execute('SELECT COUNT(*) FROM messages'):
    print(row)

print()
print('=== NOTIFICATIONS count ===')
for row in cur.execute('SELECT COUNT(*) FROM notifications'):
    print(row)

print()
print('=== CLASSES ===')
for row in cur.execute('SELECT id, kode, nama, seksi, jenjang, program FROM classes ORDER BY jenjang, seksi'):
    print(row)

conn.close()
