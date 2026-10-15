import sqlite3
con = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
con.row_factory = sqlite3.Row
cur = con.cursor()
cols = [r[1] for r in cur.execute('PRAGMA table_info(classes)')]
print('classes cols:', cols)
print('--- classes ---')
for row in cur.execute('SELECT id, kode, nama, seksi, jenjang, program, wali_kelas_id FROM classes ORDER BY id'):
    print(row['id'], '|', row['kode'], '|', row['nama'], '|', row['seksi'], '|', row['jenjang'], '|', row['program'], '| wali', row['wali_kelas_id'])
