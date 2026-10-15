import sqlite3
con = sqlite3.connect('dev.db')
for t in ['subjects', 'classes', 'teachers']:
    print('===', t, '===')
    cols = [r[1] for r in con.execute('PRAGMA table_info('+t+')')]
    print('cols:', cols)
    rows = con.execute('SELECT * FROM '+t+' LIMIT 3')
    for r in rows:
        print(r)
