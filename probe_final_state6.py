import sqlite3

conn = sqlite3.connect('dev.db')
cur = conn.cursor()

print('--- students status breakdown ---')
cur.execute('SELECT status, COUNT(*) FROM students GROUP BY status')
for r in cur.fetchall():
    print(r)

print('--- total uid_nfc non-null ---')
cur.execute('SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ""')
print(cur.fetchone()[0])

print('--- teachers active ---')
cur.execute('SELECT COUNT(*), COALESCE(SUM(active),0) FROM teachers')
print(cur.fetchone())

print('--- users ---')
cur.execute('SELECT id, email, role FROM users')
for r in cur.fetchall():
    print(r)

print('--- role_permissions by role ---')
cur.execute('SELECT r.name, COUNT(rp.id) FROM roles r LEFT JOIN role_permissions rp ON rp.role_id = r.id GROUP BY r.id ORDER BY r.id')
for r in cur.fetchall():
    print(r, r[1])

# Verify total students
cur.execute('SELECT COUNT(*) FROM students')
total = cur.fetchone()[0]
print('--- total students:', total)

# Verify uid_nfc per student
cur.execute('SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ""')
print('students with uid_nfc:', cur.fetchone()[0])

# Check classes: TAMHIDI A, TAMHIDI B, Takhosous
cur.execute("SELECT kode, program, COUNT(*) FROM students s JOIN classes c ON s.kelas_id = c.id GROUP BY c.kode, c.program ORDER BY c.kode")
for r in cur.fetchall():
    print(r)

# Check grades per kelas
cur.execute('SELECT kelas_id, COUNT(*) FROM grades GROUP BY kelas_id')
grades = cur.fetchall()
print('--- grades per kelas_id ---')
for r in grades:
    print(r)

# Total grades
cur.execute('SELECT COUNT(*) FROM grades')
print('total grades:', cur.fetchone()[0])

# Check subjects
cur.execute('SELECT COUNT(*) FROM subjects')
print('subjects:', cur.fetchone()[0])

conn.close()
