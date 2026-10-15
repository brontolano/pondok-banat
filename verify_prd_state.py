import sqlite3
conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()

print('=== TABLES ===')
for row in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
    print(row[0])

print()
print('=== USERS ===')
for row in cur.execute('SELECT id, email, role FROM users'):
    print(row)

print()
print('=== ROLES ===')
for row in cur.execute('SELECT id, name FROM roles'):
    print(row)

print()
print('=== ROLE_PERMISSIONS ===')
for row in cur.execute('SELECT id, role_id, module, permission, action FROM role_permissions'):
    print(row)

print()
print('=== STUDENTS count, active, uid_nfc_filled ===')
for row in cur.execute('SELECT COUNT(*), SUM(CASE WHEN status="active" THEN 1 ELSE 0 END), SUM(CASE WHEN uid_nfc IS NOT NULL AND uid_nfc!="" THEN 1 ELSE 0 END) FROM students'):
    print(row)

print()
print('=== STUDENTS per class (id, kelas_id) ===')
for row in cur.execute('SELECT kelas_id, COUNT(*) FROM students GROUP BY kelas_id'):
    print(row)

print()
print('=== TEACHERS count, active ===')
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
