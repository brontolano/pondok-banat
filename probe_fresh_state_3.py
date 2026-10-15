import sqlite3

conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()

tables = ['users', 'roles', 'role_permissions', 'students', 'classes', 'teachers', 'subjects', 'silabus', 'rpp', 'grades', 'absensi', 'rapor', 'announcements', 'messages', 'notifications']
print('=== TABLE COUNTS ===')
for t in tables:
    cur.execute('SELECT COUNT(*) FROM "' + t + '"')
    print('  ' + t + ':', cur.fetchone()[0])

print()
print('=== STUDENTS per class ===')
cur.execute('SELECT c.kode, c.seksi, c.program, COUNT(s.id) FROM classes c LEFT JOIN students s ON s.kelas_id = c.id GROUP BY c.kode, c.seksi, c.program ORDER BY c.kode')
for r in cur.fetchall():
    print('  ', r)

print()
print('=== STUDENTS status ===')
cur.execute("SELECT status, COUNT(*) FROM students GROUP BY status")
for r in cur.fetchall():
    print('  ', r)

print()
print('=== STUDENTS uid_nfc ===')
cur.execute("SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ''")
print('  uid_nfc_filled:', cur.fetchone()[0])

print()
print('=== TEACHERS ===')
cur.execute('SELECT COUNT(*), SUM(active) FROM teachers')
print('  count, active:', cur.fetchone())

print()
print('=== SUBJECTS ===')
cur.execute('SELECT COUNT(*) FROM subjects')
print('  count:', cur.fetchone()[0])

print()
print('=== GRADES ===')
cur.execute('SELECT COUNT(*) FROM grades')
print('  count:', cur.fetchone()[0])

print()
print('=== USERS ===')
cur.execute('SELECT id, email, name, role, status FROM users')
for r in cur.fetchall():
    print('  ', r)

print()
print('=== ROLES ===')
cur.execute('SELECT id, name, description FROM roles')
for r in cur.fetchall():
    print('  ', r)

print()
print('=== ROLE_PERMISSIONS ===')
cur.execute('SELECT COUNT(*) FROM role_permissions')
print('  count:', cur.fetchone()[0])

print()
print('=== NOTIFICATIONS/MESSAGES/ANNOUNCEMENTS/RAPOR/SILABUS/RPP/ABSENSI ===')
for t in ['announcements', 'messages', 'notifications', 'rapor', 'silabus', 'rpp', 'absensi']:
    cur.execute('SELECT COUNT(*) FROM "' + t + '"')
    print('  ' + t + ':', cur.fetchone()[0])

conn.close()
