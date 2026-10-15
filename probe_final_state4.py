import sqlite3

conn = sqlite3.connect('dev.db')
cur = conn.cursor()

print('--- students per kelas_id ---')
cur.execute('SELECT kelas_id, COUNT(*) FROM students GROUP BY kelas_id ORDER BY kelas_id')
for r in cur.fetchall():
    print(r)

print('--- classes full list ---')
cur.execute('SELECT id, kode, nama, seksi, jenjang, program, wali_kelas_id FROM classes ORDER BY jenjang, kode')
for r in cur.fetchall():
    print(r)

print('--- teachers full list ---')
cur.execute('SELECT id, name, jabatan, kelas_id, status FROM teachers ORDER BY id')
for r in cur.fetchall():
    print(r)

print('--- subjects full ---')
cur.execute('SELECT id, name, code FROM subjects ORDER BY id')
for r in cur.fetchall():
    print(r)

print('--- status breakdown students ---')
cur.execute('SELECT status, COUNT(*) FROM students GROUP BY status')
for r in cur.fetchall():
    print(r)

print('--- grades per semester ---')
cur.execute('SELECT semester, COUNT(*) FROM grades GROUP BY semester')
for r in cur.fetchall():
    print(r)

print('--- any non-admin user ---')
cur.execute('SELECT id, email, role FROM users WHERE role != "admin"')
for r in cur.fetchall():
    print(r)

print('--- total uid_nfc checked ---')
cur.execute('SELECT COUNT(*), SUM(CASE WHEN uid_nfc IS NOT NULL AND uid_nfc != "" THEN 1 ELSE 0 END) FROM students')
print(cur.fetchone())

conn.close()
