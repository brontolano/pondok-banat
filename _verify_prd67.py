import sqlite3
conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()
print('=== STUDENTS per class (join classes) ===')
cur.execute('''
    SELECT c.kode, c.nama, c.seksi, c.program, COUNT(s.id) 
    FROM students s 
    JOIN classes c ON s.kelas_id = c.id 
    GROUP BY c.kode, c.nama, c.seksi, c.program 
    ORDER BY c.kode
''')
for row in cur.fetchall():
    print(row)
print('TOTAL:', cur.execute('SELECT COUNT(*) FROM students').fetchone()[0])
print()
print('=== uid_nfc filled ===')
cur.execute("SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ''")
print('filled:', cur.fetchone()[0])
print()
print('=== Teachers ===')
cur.execute('SELECT COUNT(*) FROM teachers')
print('teachers:', cur.fetchone()[0])
print('=== Classes ===')
cur.execute('SELECT COUNT(*) FROM classes')
print('classes:', cur.fetchone()[0])
print('=== Subjects ===')
cur.execute('SELECT COUNT(*) FROM subjects')
print('subjects:', cur.fetchone()[0])
print('=== Grades ===')
cur.execute('SELECT COUNT(*) FROM grades')
print('grades:', cur.fetchone()[0])
conn.close()
