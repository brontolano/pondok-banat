import sqlite3
conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()
tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
print('TABLES:', len(tables))
for t in tables:
    try:
        cnt = cur.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0]
        print(f'{t}: {cnt}')
    except Exception as e:
        print(f'{t}: ERROR {e}')
cols = [r[1] for r in cur.execute('PRAGMA table_info(students)')]
print('students cols:', cols)
try:
    res = cur.execute('SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ""').fetchone()[0]
    print('uid_nfc filled:', res)
except Exception as e:
    print('uid_nfc check error:', e)
# verify teachers
try:
    res = cur.execute('SELECT COUNT(*) FROM teachers').fetchone()[0]
    print('teachers:', res)
except Exception as e:
    print('teachers error:', e)
# verify students status
try:
    res = cur.execute('SELECT COUNT(*), SUM(active=1), SUM(active=0) FROM students').fetchone()
    print('students status active/inactive:', res)
except Exception as e:
    print('students status error:', e)
conn.close()
