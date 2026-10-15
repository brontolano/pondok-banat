#!/usr/bin/env python3
import sqlite3

BASE = "/opt/data/home/workspace/dev/pondok-banat"
con = sqlite3.connect(BASE + "/dev.db")
cur = con.cursor()

cols = cur.execute('PRAGMA table_info(students)').fetchall()
print('STUDENTS columns:', [c[1] for c in cols])

cols = cur.execute('PRAGMA table_info(classes)').fetchall()
print('CLASSES columns:', [c[1] for c in cols])

print('\nSTUDENT COUNTS PER CLASS:')
for row in cur.execute('''SELECT c.kode, c.jenjang, c.program, COUNT(s.id) FROM classes c LEFT JOIN students s ON s.kelas_id = c.id GROUP BY c.id ORDER BY c.kode'''):
    print('  ', row)

print('\nSTUDENTS summary:')
for row in cur.execute('SELECT COUNT(*), SUM(uid_nfc IS NOT NULL) FROM students'):
    print('  ', row)

print('STUDENTS schema sample (first 3):')
for row in cur.execute('SELECT id, name, status, uid_nfc FROM students LIMIT 3'):
    print('  ', row)

print('\nTEACHERS:')
for row in cur.execute('SELECT COUNT(*), SUM(active) FROM teachers'):
    print('  ', row)

print('\nGRADES per class:')
for row in cur.execute('''SELECT c.kode, COUNT(g.id) FROM classes c LEFT JOIN grades g ON g.kelas = c.id GROUP BY c.id ORDER BY c.kode'''):
    print('  ', row)

print('\nSUBJECTS:')
for row in cur.execute('SELECT COUNT(*), SUM(active) FROM subjects'):
    print('  ', row)

con.close()
