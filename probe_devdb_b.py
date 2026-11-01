import sqlite3
conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()
tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
print('TOTAL TABLES:', len(tables))
for t in tables:
    try:
        n = cur.execute('SELECT COUNT(*) FROM "%s"' % t).fetchone()[0]
        print(t, n)
    except Exception as e:
        print(t, 'ERR:', e)
# detail on students
print('--- STUDENTS SAMPLE ---')
for row in cur.execute('SELECT id, nama, kelas, seksi, uid_nfc, aktif FROM students LIMIT 3'):
    print(row)
conn.close()
