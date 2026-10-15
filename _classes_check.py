import sqlite3
con = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
con.row_factory = sqlite3.Row
cur = con.cursor()
print('--- classes ---')
for row in cur.execute('SELECT id, kode, jenjang, program, seksi, kapasitas, wali_kelas_id FROM classes ORDER BY id'):
    print(row['id'], '|', row['kode'], '|', row['jenjang'], '|', row['program'], '|', row['seksi'], '| kap', row['kapasitas'], '| wali', row['wali_kelas_id'])
