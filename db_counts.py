import sqlite3
conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()
tables = ['users','roles','role_permissions','students','classes','teachers','subjects','silabus','rpp','absensi','grades','rapor','announcements','messages','notifications']
for t in tables:
    cur.execute('SELECT COUNT(*) FROM ' + t)
    print('  %s: %d' % (t, cur.fetchone()[0]))
conn.close()
