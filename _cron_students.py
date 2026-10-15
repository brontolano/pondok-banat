import sqlite3, json

BASE = '/opt/data/home/workspace/dev/pondok-banat'
con = sqlite3.connect(BASE + '/dev.db')
cur = con.cursor()

print('--- students: status values ---')
for r in cur.execute('SELECT status, COUNT(*) FROM students GROUP BY status ORDER BY status'):
    print('STATUS ' + str(r))

print('--- students: uid_nfc filled ---')
print('FILLED=' + str(cur.execute('SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL').fetchone()[0]))

print('--- students per kelas (via kelas_id) ---')
rows = cur.execute('''
SELECT c.jenjang, c.seksi, c.program, COUNT(s.id)
FROM students s
JOIN classes c ON s.kelas_id = c.id
GROUP BY c.jenjang, c.seksi, c.program
ORDER BY c.jenjang, c.seksi
''').fetchall()
tot = 0
for r in rows:
    print('  ' + str(r))
    tot += r[3]
print('  TOTAL=' + str(tot))

print('--- classes full list ---')
for r in cur.execute('SELECT id, kode, nama, seksi, jenjang, program, wali_kelas_id FROM classes ORDER BY jenjang, seksi'):
    print('  ' + str(r))
