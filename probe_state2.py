import sqlite3

proj = '/opt/data/home/workspace/dev/pondok-banat'
con = sqlite3.connect(proj + '/dev.db')
cur = con.cursor()

print('== CLASSES ==')
rows = list(cur.execute('''
  SELECT c.kode, c.seksi, c.jenjang, c.program,
         (SELECT COUNT(*) FROM students s WHERE s.kelas_id = c.id) as nj
  FROM classes c
  ORDER BY c.jenjang, c.seksi, c.id
'''))
for r in rows:
    print('  ', r)
tot = sum(r[4] for r in rows)
print('  TOTAL students via join:', tot)

print('== TEACHERS status ==')
print('  ', cur.execute('SELECT status, COUNT(*) FROM teachers GROUP BY status').fetchall())

print('== USERS ==')
for row in cur.execute('SELECT id, email, role FROM users'):
    print('  ', row)

print('== ROLES ==')
for row in cur.execute('SELECT id, name FROM roles'):
    print('  ', row)

print('== role_permissions total ==', cur.execute('SELECT COUNT(*) FROM role_permissions').fetchone()[0])

print('== SUBJECTS status ==')
print('  ', cur.execute('SELECT status, COUNT(*) FROM subjects GROUP BY status').fetchall())

print('== STUDENT status ==')
print('  ', cur.execute('SELECT status, COUNT(*) FROM students GROUP BY status').fetchall())

con.close()
