import sqlite3

conn = sqlite3.connect('dev.db')
cur = conn.cursor()

print('--- subjects full ---')
cur.execute('SELECT id, name FROM subjects ORDER BY id')
for r in cur.fetchall():
    print(r)

print('--- grades per semester ---')
cur.execute('SELECT semester, COUNT(*) FROM grades GROUP BY semester')
for r in cur.fetchall():
    print(r)

print('--- grades per kelas_id ---')
cur.execute('SELECT kelas_id, COUNT(*) FROM grades GROUP BY kelas_id ORDER BY kelas_id')
for r in cur.fetchall():
    print(r)

print('--- classes per jenjang ---')
cur.execute('SELECT jenjang, COUNT(*) FROM classes GROUP BY jenjang ORDER BY jenjang')
for r in cur.fetchall():
    print(r)

# Verify total students per kelas
print('--- total students ---')
cur.execute('SELECT COUNT(*) FROM students')
print(cur.fetchone()[0])

# Verify grades per kelas
print('--- total grades per kelas_id ---')
cur.execute('SELECT kelas_id, COUNT(*) FROM grades GROUP BY kelas_id ORDER BY kelas_id')
for r in cur.fetchall():
    print(r)

# The classes have jenjang + kode
# Let me map
print('--- classes with jenjang, kode ---')
cur.execute('SELECT id, kode, jenjang, program FROM classes ORDER BY jenjang, kode')
for r in cur.fetchall():
    print(r)

conn.close()
