import sqlite3
conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()
print('=== STUDENTS PER CLASS ===')
for row in cur.execute('''
    SELECT c.kode, c.nama, c.jenjang, c.program, c.seksi,
           COUNT(s.id) as student_count
    FROM classes c
    LEFT JOIN students s ON s.kelas_id = c.id
    GROUP BY c.id
    ORDER BY c.jenjang, c.seksi, c.kode
'''):
    print(row)
print('--- total students ---')
print(cur.execute('SELECT COUNT(*) FROM students').fetchone()[0])
print('--- grades per student ---')
res = cur.execute('SELECT student_id, COUNT(*) FROM grades GROUP BY student_id ORDER BY student_id LIMIT 5').fetchall()
print(res)
print('--- total grades ---')
print(cur.execute('SELECT COUNT(*) FROM grades').fetchone()[0])
print('--- grades semesters ---')
for row in cur.execute('SELECT semester, COUNT(*) FROM grades GROUP BY semester'):
    print(row)
conn.close()
