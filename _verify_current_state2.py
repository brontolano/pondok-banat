import sqlite3

conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()

# student columns
cols = [r[1] for r in cur.execute('PRAGMA table_info(students)')]
print("students columns:", cols)
print()

# Students summary
total = cur.execute('SELECT COUNT(*) FROM students').fetchone()[0]
print(f'total students: {total}')

# Uid filled count
uid_filled = cur.execute("SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ''").fetchone()[0]
print(f'uid_nfc filled: {uid_filled}')

# Active count - check what column indicates active status
for col in cols:
    if 'act' in col.lower() or 'status' in col.lower():
        cnt = cur.execute(f"SELECT COUNT(*) FROM students WHERE \"{col}\" = 1").fetchone()[0]
        cnt2 = cur.execute(f"SELECT COUNT(*) FROM students WHERE \"{col}\" = '1'").fetchone()[0]
        print(f"active count for column '{col}': {cnt} (also tried '1'): {cnt2}")

# class distribution
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

# teachers
teacher_count = cur.execute('SELECT COUNT(*) FROM teachers').fetchone()[0]
print(f'\nteachers: {teacher_count}')

# mapel
mapel_count = cur.execute('SELECT COUNT(*) FROM subjects').fetchone()[0]
print(f'mapel: {mapel_count}')

# grades
grade_count = cur.execute('SELECT COUNT(*) FROM grades').fetchone()[0]
print(f'grades: {grade_count}')

# users
user_count = cur.execute('SELECT COUNT(*) FROM users').fetchone()[0]
print(f'users: {user_count}')

# role_permissions
rp_count = cur.execute('SELECT COUNT(*) FROM role_permissions').fetchone()[0]
print(f'role_permissions: {rp_count}')

# roles
role_count = cur.execute('SELECT COUNT(*) FROM roles').fetchone()[0]
print(f'roles: {role_count}')

# absensi/rapor/rpp/silabus counts
for t in ['absensi', 'rapor', 'rpp', 'silabus', 'announcements', 'messages', 'notifications']:
    cnt = cur.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0]
    print(f'{t}: {cnt}')

conn.close()
