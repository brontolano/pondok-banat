import sqlite3
conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()

print('=== teachers schema ===')
for row in cur.execute('PRAGMA table_info(teachers)'):
    print(row)

print()
print('=== teachers sample ===')
for row in cur.execute('SELECT * FROM teachers LIMIT 3'):
    print(row)

print()
print('=== classes: full detail ===')
for row in cur.execute('SELECT id, kode, nama, seksi, jenjang, program, wali_kelas_id FROM classes ORDER BY jenjang, seksi'):
    print(row)

print()
print('=== uid_nfc: total null / filled ===')
for row in cur.execute('SELECT COUNT(*), SUM(CASE WHEN uid_nfc IS NOT NULL AND uid_nfc!="" THEN 1 ELSE 0 END) FROM students'):
    print(row)

print()
print('=== students with status active ===')
for row in cur.execute('SELECT COUNT(*), SUM(CASE WHEN status="active" THEN 1 ELSE 0 END) FROM students'):
    print(row)

print()
print('=== role_permissions distribution ===')
for row in cur.execute('SELECT permission, COUNT(*) FROM role_permissions GROUP BY permission'):
    print(row)

print()
print('=== classes with wali_kelas_id set ===')
for row in cur.execute('SELECT id, kode, wali_kelas_id FROM classes WHERE wali_kelas_id IS NOT NULL'):
    print(row)

conn.close()
