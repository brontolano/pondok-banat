import sqlite3
conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()
cols = [r[1] for r in cur.execute('PRAGMA table_info(students)')]
print('students columns:', cols)
print('uid_nfc present:', 'uid_nfc' in cols)
rows = cur.execute('SELECT nisn, name, uid_nfc FROM students WHERE uid_nfc IS NOT NULL LIMIT 5').fetchall()
print('samples with uid_nfc:', rows)
cur2 = conn.cursor()
print('status counts:', cur2.execute('SELECT status, COUNT(*) FROM students GROUP BY status').fetchall())
print('kelas counts:', cur2.execute('SELECT kelas_id, COUNT(*) FROM students GROUP BY kelas_id ORDER BY kelas_id').fetchall())
conn.close()
