import sqlite3
conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
c = conn.cursor()
tables = ['users','roles','role_permissions','students','classes','teachers','subjects','silabus','rpp','absensi','grades','rapor','announcements','messages','notifications']
for t in tables:
    c.execute('SELECT COUNT(*) FROM ' + t)
    print(t + ': ' + str(c.fetchone()[0]))
print('--- students per kelas ---')
c.execute('SELECT jenjang, seksi, COUNT(*) FROM students GROUP BY jenjang, seksi ORDER BY jenjang')
for row in c.fetchall():
    print(row)
conn.close()
