import sqlite3
con = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = con.cursor()
tables = ['users','roles','role_permissions','students','classes','teachers','subjects','grades','silabus','rpp','absensi','rapor','announcements','messages','notifications']
for t in tables:
    n = cur.execute('SELECT COUNT(*) FROM ' + t).fetchone()[0]
    print(t + ': ' + str(n))
print('--- students per class ---')
for row in cur.execute('SELECT kelas_id, COUNT(*) FROM students GROUP BY kelas_id ORDER BY kelas_id'):
    print(row)
print('--- uid_nfc filled ---')
print(cur.execute("SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ''").fetchone()[0])
print('--- active students ---')
print(cur.execute('SELECT COUNT(*) FROM students WHERE status = ?', ('active',)).fetchone()[0])
print('--- inactive students ---')
print(cur.execute('SELECT COUNT(*) FROM students WHERE status = ?', ('inactive',)).fetchone()[0])
print('--- teachers ---')
print(cur.execute('SELECT COUNT(*) FROM teachers').fetchone()[0])
print('--- subjects ---')
print(cur.execute('SELECT COUNT(*) FROM subjects').fetchone()[0])
print('--- grades ---')
print(cur.execute('SELECT COUNT(*) FROM grades').fetchone()[0])
con.close()
