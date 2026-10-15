import sqlite3

conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()

print('=== USERS ===')
cur.execute('SELECT id, email, password, role_id, active FROM users')
for r in cur.fetchall():
    print(r)

print()
print('=== ROLES ===')
cur.execute('SELECT id, name, description FROM roles')
for r in cur.fetchall():
    print(r)

print()
print('=== ROLE_PERMISSIONS ===')
cur.execute('SELECT COUNT(*) FROM role_permissions')
print('count:', cur.fetchone()[0])

print()
print('=== STUDENTS summary ===')
cur.execute('SELECT COUNT(*), SUM(active), SUM(uid_nfc IS NOT NULL) FROM students')
print('total, active_sum, uid_nfc_filled:', cur.fetchone())

print()
print('=== STUDENTS per kelas ===')
cur.execute('SELECT kode, seksi, COUNT(*) FROM students JOIN classes USING(class_id) GROUP BY kode, seksi ORDER BY kode')
for r in cur.fetchall():
    print(' ', r)

print()
print('=== GRADES count ===')
cur.execute('SELECT COUNT(*) FROM grades')
print(cur.fetchone()[0])

print()
print('=== TEACHERS ===')
cur.execute('SELECT COUNT(*), SUM(active) FROM teachers')
print(cur.fetchone())

print()
print('=== SUBJECTS ===')
cur.execute('SELECT COUNT(*) FROM subjects')
print(cur.fetchone()[0])

conn.close()
