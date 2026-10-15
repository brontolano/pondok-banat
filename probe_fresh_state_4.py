import sqlite3

conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()

print('=== TEACHERS ===')
cur.execute('PRAGMA table_info(teachers)')
for r in cur.fetchall():
    print('  col:', r[1], r[2])
cur.execute('SELECT COUNT(*), SUM(status) FROM teachers')
print('  count, active:', cur.fetchone())
cur.execute('SELECT name, COUNT(*) FROM teachers GROUP BY name')
print('  unique names:', cur.fetchone())

print()
print('=== STUDENTS per class (full) ===')
cur.execute('SELECT c.kode, c.seksi, c.program, c.jenjang, COUNT(s.id) FROM classes c LEFT JOIN students s ON s.kelas_id = c.id GROUP BY c.kode, c.seksi, c.program, c.jenjang ORDER BY c.kode')
total = 0
for r in cur.fetchall():
    print('  ', r)
    total += r[4]
print('  TOTAL:', total)

print()
print('=== GRADES by mapel count ===')
cur.execute('SELECT COUNT(DISTINCT mapel_id) FROM grades')
print('  mapel_count:', cur.fetchone()[0])

print()
print('=== GRADE distribution ===')
cur.execute('SELECT student_status, COUNT(*) FROM grades GROUP BY student_status')
for r in cur.fetchall():
    print('  ', r)

conn.close()
