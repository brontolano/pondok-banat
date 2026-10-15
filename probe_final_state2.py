import sqlite3

conn = sqlite3.connect('dev.db')
cur = conn.cursor()

print('--- students schema ---')
cur.execute('PRAGMA table_info(students)')
for r in cur.fetchall():
    print(r)

print('--- uid_nfc check ---')
cur.execute('SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ""')
print('non-null uid_nfc:', cur.fetchone()[0])

print('--- uid_nfc empty check ---')
cur.execute('SELECT COUNT(*) FROM students WHERE uid_nfc = ""')
print('empty uid_nfc:', cur.fetchone()[0])

print('--- admin user ---')
cur.execute('SELECT * FROM users WHERE email = "admin@pondokanat.com"')
print(cur.fetchall())

print('--- roles ---')
cur.execute('SELECT id, name FROM roles ORDER BY id')
for r in cur.fetchall():
    print(r)

print('--- role_permissions ---')
cur.execute('SELECT role_id, COUNT(*) FROM role_permissions GROUP BY role_id ORDER BY role_id')
for r in cur.fetchall():
    print(r)

print('--- classes count ---')
cur.execute('SELECT COUNT(*) FROM classes')
print(cur.fetchone()[0])

print('--- classes sample ---')
cur.execute('SELECT id, kode, nama, seksi, jenjang, program FROM classes LIMIT 5')
for r in cur.fetchall():
    print(r)

conn.close()
