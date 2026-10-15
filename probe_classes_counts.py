import sqlite3
conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()
print('--- Siswa per kelas (via classes table) ---')
for row in cur.execute('SELECT c.kode, c.seksi, c.program, COUNT(s.id) FROM classes c LEFT JOIN students s ON s.kelas_id = c.id GROUP BY c.kode, c.seksi, c.program ORDER BY c.kode'):
    print(' ', row)
print()
print('--- UID NFC filled ---')
print(' ', cur.execute('SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ""').fetchone()[0])
conn.close()
