import sqlite3, json

BASE = '/opt/data/home/workspace/dev/pondok-banat'
con = sqlite3.connect(BASE + '/dev.db')
cur = con.cursor()

def show(t):
    print('SCHEMA ' + t + ':')
    for r in cur.execute('PRAGMA table_info(' + t + ')'):
        print('  ', r)
    print('  count=' + str(cur.execute('SELECT COUNT(*) FROM ' + t).fetchone()[0]))

show('students')
show('classes')
