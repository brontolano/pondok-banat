import sqlite3
con = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = con.cursor()
print('=== students table schema ===')
for row in cur.execute('PRAGMA table_info(students)'):
    print(row)
print()
print('=== Classes joined students counts ===')
for row in cur.execute('''
    SELECT c.id, c.kode, c.nama, c.seksi, c.jenjang, c.program, COUNT(s.id) as cnt
    FROM classes c
    LEFT JOIN students s ON s.kelas_id = c.id
    GROUP BY c.id
    ORDER BY c.program, c.seksi
'''):
    print(row)
print()
print('=== TOTAL students:', cur.execute('SELECT COUNT(*) FROM students').fetchone()[0])
print('=== uid_nfc filled:', cur.execute("SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ''").fetchone()[0])
print('=== Teachers ===')
print(cur.execute('SELECT COUNT(*), SUM(active), SUM(status) FROM teachers').fetchone())
print('=== Subjects ===')
print(cur.execute('SELECT COUNT(*), SUM(active) FROM subjects').fetchone())
print('=== Grades distinct mapel:', cur.execute('SELECT COUNT(DISTINCT mapel_id) FROM grades').fetchone()[0])
con.close()
