import sqlite3, os
con = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
con.row_factory = sqlite3.Row
cur = con.cursor()
print('users:', cur.execute('SELECT COUNT(*) c FROM users').fetchone()['c'])
print('roles:', cur.execute('SELECT COUNT(*) c FROM roles').fetchone()['c'])
print('role_permissions:', cur.execute('SELECT COUNT(*) c FROM role_permissions').fetchone()['c'])
print('students:', cur.execute('SELECT COUNT(*) c FROM students').fetchone()['c'])
print('students uid_nfc filled:', cur.execute('SELECT COUNT(*) c FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != \'\'').fetchone()['c'])
print('classes:', cur.execute('SELECT COUNT(*) c FROM classes').fetchone()['c'])
print('teachers:', cur.execute('SELECT COUNT(*) c FROM teachers').fetchone()['c'])
print('subjects:', cur.execute('SELECT COUNT(*) c FROM subjects').fetchone()['c'])
print('grades:', cur.execute('SELECT COUNT(*) c FROM grades').fetchone()['c'])
for t in ['absensi','rapor','announcements','messages','notifications','silabus','rpp']:
    print(t + ':', cur.execute('SELECT COUNT(*) c FROM ' + t).fetchone()['c'])
# per-class distribution
dist = {}
for row in cur.execute('SELECT kode, program FROM classes'):
    dist[row['kode']] = dist.get(row['kode'], 0) + 1
print('classes list:', sorted(dist.items()))
# verify total students
total = 0
for row in cur.execute('SELECT kelas_id, COUNT(*) c FROM students GROUP BY kelas_id'):
    total += row['c']
print('students total:', total)
# build state
print('src/app pages:', sorted([os.path.basename(p) for p in __import__('glob').glob('/opt/data/home/workspace/dev/pondok-banat/src/app/*/page.tsx')]))
print('src/components:', sorted([os.path.basename(p) for p in __import__('glob').glob('/opt/data/home/workspace/dev/pondok-banat/src/components/*.tsx')]))
print('src/lib files:', os.listdir('/opt/data/home/workspace/dev/pondok-banat/src/lib'))
print('.data-pondokbanat files:', sum(len(files) for _,_,files in os.walk('/opt/data/home/workspace/dev/pondok-banat/.data-pondokbanat')))
print('excel:', sum(1 for r,_,f in os.walk('/opt/data/home/workspace/dev/pondok-banat/.data-pondokbanat') for fs in f if fs.endswith('.xlsx')))
print('pdf:', sum(1 for r,_,f in os.walk('/opt/data/home/workspace/dev/pondok-banat/.data-pondokbanat') for fs in f if fs.endswith('.pdf')))
