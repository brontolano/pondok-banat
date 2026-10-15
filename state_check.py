import sqlite3
conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()
tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
print('TABLE:', tables)
for t in tables:
    cnt = cur.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0]
    print(f'  {t}: {cnt}')
# student status
rows = cur.execute('SELECT status, COUNT(*) FROM students GROUP BY status').fetchall()
print('STUDENT STATUS:', rows)
# uid_nfc filled
rows = cur.execute('SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ""').fetchone()[0]
print('UID_NFC_FILLED:', rows)
# teachers status
rows = cur.execute('SELECT status, COUNT(*) FROM teachers GROUP BY status').fetchall()
print('TEACHER STATUS:', rows)
conn.close()
