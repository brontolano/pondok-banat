import sqlite3
conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()
print("=== Students ===")
cur.execute('SELECT nisn,name,status,kelas_id FROM students ORDER BY nisn')
for r in cur.fetchall():
    print(' ', r)
print("=== Classes ===")
cur.execute('SELECT kode,nama,seksi,jenjang,program FROM classes ORDER BY kode')
for r in cur.fetchall():
    print(' ', r)
print("=== Teachers count ===")
cur.execute('SELECT COUNT(*) FROM teachers')
print('teacher count:', cur.fetchone()[0])
print("=== Teachers jabatan ===")
cur.execute('SELECT jabatan, COUNT(*) FROM teachers GROUP BY jabatan')
for r in cur.fetchall():
    print(' ', r)
conn.close()
