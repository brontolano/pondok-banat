import sqlite3
con = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = con.cursor()
print('=== Students per class ===')
for row in cur.execute('SELECT kelas_id, COUNT(*) FROM students GROUP BY kelas_id ORDER BY kelas_id'):
    print(row)
print('Total:', cur.execute('SELECT COUNT(*) FROM students').fetchone()[0])
print('Active students:', cur.execute("SELECT COUNT(*) FROM students WHERE active=1").fetchone()[0])
print('uid_nfc filled:', cur.execute("SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ''").fetchone()[0])
print('=== Classes ===')
for row in cur.execute('SELECT id, kode, nama, seksi, jenjang, program FROM classes ORDER BY jenjang, seksi'):
    print(row)
print('=== Teachers active ===')
print(cur.execute('SELECT COUNT(*), SUM(active) FROM teachers').fetchone())
print('=== Subjects ===')
print(cur.execute('SELECT COUNT(*), SUM(active) FROM subjects').fetchone())
print('=== Grades mapel count ===')
print(cur.execute('SELECT COUNT(DISTINCT mapel_id) FROM grades').fetchone())
con.close()
