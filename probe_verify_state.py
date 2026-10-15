import sqlite3
conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()
tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
print('TABLES:', tables)
for t in tables:
    cnt = cur.execute('SELECT COUNT(*) FROM "%s"' % t).fetchone()[0]
    print('  %s: %d record' % (t, cnt))
print()
print('--- Siswa per kelas ---')
cur.execute('SELECT * FROM students LIMIT 1')
print('students columns:', [d[1] for d in cur.description])
for row in cur.execute('SELECT kode, seksi, program, COUNT(*) FROM students GROUP BY kode, seksi, program ORDER BY kode'):
    print(' ', row)
print()
print('--- UID NFC filled count ---')
print(' ', cur.execute('SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ""').fetchone()[0])
conn.close()
