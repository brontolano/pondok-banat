import sqlite3
conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()
tables = ['users','roles','role_permissions','students','classes','teachers','subjects','silabus','rpp','absensi','grades','rapor','announcements','messages','notifications']
for t in tables:
    try:
        cur.execute('SELECT COUNT(*) FROM ' + t)
        print(f'{t:20s}', cur.fetchone()[0])
    except Exception as e:
        print(f'{t:20s} ERROR {e}')
print('--- roles detail ---')
cur.execute('SELECT name, display_name, description FROM roles')
for r in cur.fetchall():
    print(r)
print('--- users detail ---')
cur.execute('SELECT id, email, name, role FROM users')
for r in cur.fetchall():
    print(r)
