import sqlite3
import os

conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()

tables = [
    'users', 'roles', 'role_permissions', 'students', 'classes',
    'teachers', 'subjects', 'silabus', 'rpp', 'absensi', 'grades',
    'rapor', 'announcements', 'messages', 'notifications'
]

total = 0
for t in tables:
    try:
        cur.execute(f'SELECT COUNT(*) FROM {t}')
        n = cur.fetchone()[0]
        total += n
        print(f'{t}: {n}')
    except Exception as e:
        print(f'{t}: ERROR {e}')

print(f'TOTAL: {total}')
conn.close()
