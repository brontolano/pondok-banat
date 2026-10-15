import sqlite3
conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()

print('=== STUDENT per kelas distribution ===')
for row in cur.execute('SELECT kelas_id, COUNT(*) as cnt, SUM(CASE WHEN uid_nfc IS NOT NULL AND uid_nfc!="" THEN 1 ELSE 0 END) as nfc_filled FROM students GROUP BY kelas_id ORDER BY kelas_id'):
    print(row)

print()
print('=== uid_nfc field info for a few students ===')
for row in cur.execute('SELECT nisn, name, kelas_id, uid_nfc FROM students LIMIT 5'):
    print(row)

print()
print('=== uid_nfc null count ===')
for row in cur.execute('SELECT COUNT(*), SUM(CASE WHEN uid_nfc IS NULL OR uid_nfc="" THEN 1 ELSE 0 END) FROM students'):
    print(row)

print()
print('=== classes with wali_kelas_id ===')
for row in cur.execute('SELECT id, kode, wali_kelas_id FROM classes WHERE wali_kelas_id IS NOT NULL'):
    print(row)

print()
print('=== classes count ===')
for row in cur.execute('SELECT COUNT(*) FROM classes'):
    print(row)

print()
print('=== Teacher sample ===')
for row in cur.execute('SELECT id, name, role, status FROM teachers LIMIT 3'):
    print(row)

print('=== Teacher count ===')
for row in cur.execute('SELECT COUNT(*), SUM(CASE WHEN status="active" THEN 1 ELSE 0 END) FROM teachers'):
    print(row)

print()
print('=== Silabus/RPP count ===')
for row in cur.execute('SELECT (SELECT COUNT(*) FROM silabus), (SELECT COUNT(*) FROM rpp)'):
    print(row)

conn.close()
