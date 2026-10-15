import sqlite3, json

BASE = '/opt/data/home/workspace/dev/pondok-banat'
con = sqlite3.connect(BASE + '/dev.db')
cur = con.cursor()

print('--- per class (count students) ---')
rows = cur.execute('''
SELECT c.id, c.kode, c.nama, c.seksi, c.jenjang, c.program, COUNT(s.id) AS n
FROM classes c
LEFT JOIN students s ON s.kelas_id = c.id
GROUP BY c.id
ORDER BY
  CASE c.jenjang
    WHEN 'TK' THEN 0
    WHEN 'TA A' THEN 1
    WHEN 'TB' THEN 2
    WHEN 'Takhosours' THEN 3
    WHEN 'TAMHIDI A' THEN 4
    WHEN 'TAMHIDI B' THEN 5
    ELSE 6
  END,
  c.jenjang, c.seksi
''').fetchall()
tot = 0
for r in rows:
    print('  ' + str(r))
    tot += r[6]
print('  TOTAL_STUDENTS=' + str(tot))

# Also: students per jenjang/seksi again using kelas_id -> classes kode
print('--- students grouped by class.kode (no join to classes columns) ---')
rows2 = cur.execute('''
SELECT c.kode, c.jenjang, c.seksi, COUNT(s.id)
FROM students s JOIN classes c ON s.kelas_id = c.id
GROUP BY c.kode, c.jenjang, c.seksi
ORDER BY c.kode
''').fetchall()
for r in rows2:
    print('  ' + str(r))
