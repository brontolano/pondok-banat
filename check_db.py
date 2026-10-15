import sqlite3, os

conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()
tables = ['users','roles','role_permissions','students','classes','teachers','subjects','silabus','rpp','absensi','grades','rapor','announcements','messages','notifications']
print('=== Table row counts ===')
for t in tables:
    cur.execute('SELECT COUNT(*) FROM ' + t)
    print('  %s: %d' % (t, cur.fetchone()[0]))

print()
print('=== Students ===')
cur.execute('SELECT id, nisn, name, status, kelas_id FROM students ORDER BY nisn')
for r in cur.fetchall():
    print('  ', r)

print()
print('=== Classes ===')
cur.execute('SELECT id, kode, nama, seksi, jenjang, program FROM classes ORDER BY kode')
for r in cur.fetchall():
    print('  ', r)

print()
print('=== Teachers ===')
cur.execute('SELECT id, name, jabatan, status FROM teachers ORDER BY name')
for r in cur.fetchall():
    print('  ', r)

print()
print('=== Users ===')
cur.execute('SELECT id, email, name, role, status FROM users ORDER BY id')
for r in cur.fetchall():
    print('  ', r)

print()
print('=== Roles ===')
cur.execute('SELECT id, name, display_name FROM roles ORDER BY name')
for r in cur.fetchall():
    print('  ', r)

print()
print('=== Role permissions ===')
cur.execute('SELECT rp.permission, r.name FROM role_permissions rp JOIN roles r ON rp.role_id=r.id ORDER BY r.name')
for r in cur.fetchall():
    print('  ', r)

conn.close()
