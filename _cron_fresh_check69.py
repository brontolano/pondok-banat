import sqlite3
conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()

# uid_nfc count
cur.execute('SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ""')
print('Siswa uid_nfc terisi:', cur.fetchone()[0], '/ 441')

# Student distribution per class
cur.execute("""
    SELECT c.kode, c.program, c.seksi, COUNT(s.id) as total
    FROM classes c
    LEFT JOIN students s ON s.kelas_id = c.id
    GROUP BY c.id
    ORDER BY c.kode
""")
total = 0
for kode, program, seksi, count in cur.fetchall():
    print(f'  {kode} ({program}, {seksi}) = {count}')
    total += count
print('  TOTAL =', total)

# Admin user
cur.execute("SELECT id, email, role FROM users WHERE role='admin'")
print('Admin:', cur.fetchall())

# KitabProgress/Sertakan tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('kitab_progress','sertakan')")
print('KitabProgress/Sertakan tables:', cur.fetchall())

# Sample classes
cur.execute("SELECT id, kode, nama, program, seksi FROM classes LIMIT 5")
print('Sample classes:')
for r in cur.fetchall():
    print('  ', r)

# Sample students
cur.execute("SELECT id, nama, kelas_id, uid_nfc FROM students LIMIT 3")
print('Sample students:')
for r in cur.fetchall():
    print('  ', r)

conn.close()
