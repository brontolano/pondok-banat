import sqlite3, os, json

BASE = os.environ.get('PONDOK_DIR', '/opt/data/home/workspace/dev/pondok-banat')
DB = os.path.join(BASE, 'dev.db')

con = sqlite3.connect(DB)
cur = con.cursor()

print('PONDOK_DIR=' + BASE)
print('db_file=' + DB + ' exists=' + str(os.path.exists(DB)))

tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
print('TOTAL_TABLES=' + str(len(tables)))

summary = {}
for t in tables:
    try:
        cnt = cur.execute('SELECT COUNT(*) FROM ' + t).fetchone()[0]
    except Exception as e:
        cnt = 'ERR:' + str(e)
    summary[t] = cnt

print('DB=' + json.dumps(summary, indent=2))

print('--- students per kelas ---')
rows = cur.execute('SELECT jenjang, seksi, COUNT(*) FROM students GROUP BY jenjang, seksi ORDER BY jenjang, seksi').fetchall()
print('STUDENTS_PER_KELAS=' + json.dumps([{'jenjang': r[0], 'seksi': r[1], 'cnt': r[2]} for r in rows]))
print('STUDENT_TOTAL=' + str(cur.execute('SELECT COUNT(*) FROM students').fetchone()[0]))
print('STUDENT_ACTIVE=' + str(cur.execute('SELECT COUNT(*) FROM students WHERE active=1').fetchone()[0]))
print('STUDENT_UID_NFC_FILLED=' + str(cur.execute('SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL').fetchone()[0]))

print('--- counts ---')
for name in ['users', 'roles', 'role_permissions', 'students', 'classes', 'teachers', 'subjects', 'silabus', 'rpp', 'grades', 'rapor', 'absensi', 'announcements', 'messages', 'notifications']:
    try:
        print(name + '=' + str(cur.execute('SELECT COUNT(*) FROM ' + name).fetchone()[0]))
    except Exception as e:
        print(name + '=ERR')

print('--- classes ---')
for r in cur.execute('SELECT id, kode, nama, seksi, jenjang, program, wali_kelas_id FROM classes ORDER BY jenjang, seksi'):
    print('CLASS ' + str(r))

print('--- users ---')
for r in cur.execute('SELECT id, email, role FROM users ORDER BY id'):
    print('USER ' + str(r))

print('--- role_permissions ---')
for r in cur.execute('SELECT COUNT(*) FROM role_permissions').fetchone():
    print('ROLE_PERMISSIONS=' + str(r[0]))

print('--- teachers ---')
for r in cur.execute('SELECT COUNT(*) FROM teachers').fetchone():
    print('TEACHERS=' + str(r[0]))

print('--- grades ---')
for r in cur.execute('SELECT COUNT(*) FROM grades').fetchone():
    print('GRADES=' + str(r[0]))
