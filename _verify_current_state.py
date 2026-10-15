import sqlite3

conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()

# List all tables
tables = [r[0] for r in cur.execute(
    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
print("TABLES:", tables)
print()

# Count records per table
for t in tables:
    try:
        count = cur.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0]
        print(f'{t}: {count} records')
    except Exception as e:
        print(f'{t}: ERROR {e}')

print()
# Student summary
total = cur.execute('SELECT COUNT(*) FROM students').fetchone()[0]
active = cur.execute("SELECT COUNT(*) FROM students WHERE active=1").fetchone()[0]
uid_filled = cur.execute("SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ''").fetchone()[0]
print(f'total students: {total}, active: {active}, uid_nfc filled: {uid_filled}')

# Class distribution
print('\n--- CLASSES (kode, seksi, program, student_count) ---')
rows = cur.execute('''
    SELECT c.kode, c.seksi, c.program, COUNT(s.id)
    FROM classes c
    LEFT JOIN students s ON s.kelas_id = c.id
    GROUP BY c.id
    ORDER BY c.id
''').fetchall()
for r in rows:
    print(r)
print('class count:', len(rows))

# Teachers
teacher_count = cur.execute('SELECT COUNT(*) FROM teachers').fetchone()[0]
print(f'\nteachers: {teacher_count}')

# Mapel
mapel_count = cur.execute('SELECT COUNT(*) FROM subjects').fetchone()[0]
print(f'mapel: {mapel_count}')

# Grades
grade_count = cur.execute('SELECT COUNT(*) FROM grades').fetchone()[0]
print(f'grades: {grade_count}')

conn.close()
