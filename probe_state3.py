import sqlite3

proj = '/opt/data/home/workspace/dev/pondok-banat'
con = sqlite3.connect(proj + '/dev.db')
cur = con.cursor()
print('== PRAGMA classes ==')
for row in cur.execute('PRAGMA table_info(classes)'):
    print('  ', row)
print('== classes all rows ==')
for row in cur.execute('SELECT * FROM classes ORDER BY jenjang, seksi, id'):
    print('  ', row)
con.close()
