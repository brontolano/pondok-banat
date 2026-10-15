import sqlite3

con = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = con.cursor()

total_students = cur.execute('SELECT COUNT(*) FROM students').fetchone()[0]
total_classes = cur.execute('SELECT COUNT(*) FROM classes').fetchone()[0]
total_teachers = cur.execute('SELECT COUNT(*) FROM teachers').fetchone()[0]
total_subjects = cur.execute('SELECT COUNT(*) FROM subjects').fetchone()[0]
total_grades = cur.execute('SELECT COUNT(*) FROM grades').fetchone()[0]
total_users = cur.execute('SELECT COUNT(*) FROM users').fetchone()[0]
total_roles = cur.execute('SELECT COUNT(*) FROM roles').fetchone()[0]
total_role_permissions = cur.execute('SELECT COUNT(*) FROM role_permissions').fetchone()[0]
uid_nfc_filled = cur.execute("SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ''").fetchone()[0]
students_inactive = cur.execute("SELECT COUNT(*) FROM students WHERE status='inactive'").fetchone()[0]
teachers_active = cur.execute("SELECT COUNT(*) FROM teachers WHERE status='active'").fetchone()[0]

class_dist = {}
for row in cur.execute('''
    SELECT c.program, c.seksi, COUNT(s.id) FROM classes c
    LEFT JOIN students s ON s.kelas_id = c.id
    GROUP BY c.id ORDER BY c.program, c.seksi
'''):
    program, seksi, cnt = row
    class_dist[program] = class_dist.get(program, 0) + cnt

dist_items = sorted(class_dist.items(), key=lambda x: (x[0] is None, x[0] or ''))
dist_str = '; '.join(f'{k}={v}' for k, v in dist_items)
print(f'total_students={total_students}')
print(f'total_classes={total_classes}')
print(f'total_teachers={total_teachers}')
print(f'total_subjects={total_subjects}')
print(f'total_grades={total_grades}')
print(f'total_users={total_users}')
print(f'total_roles={total_roles}')
print(f'total_role_permissions={total_role_permissions}')
print(f'uid_nfc_filled={uid_nfc_filled}')
print(f'students_inactive={students_inactive}')
print(f'teachers_active={teachers_active}')
print(f'DIST={dist_str}')
con.close()
