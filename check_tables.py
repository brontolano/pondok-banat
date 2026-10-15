import sqlite3

base = "/opt/data/home/workspace/dev/pondok-banat"
con = sqlite3.connect(base + "/dev.db")
cur = con.cursor()

for t in ['silabus', 'rpp', 'absensi', 'rapor', 'announcements', 'messages', 'notifications', 'kegiatan', 'health_records', 'subjects', 'teachers', 'classes', 'students', 'grades']:
    try:
        cnt = cur.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]
        cols = [r[1] for r in cur.execute(f'PRAGMA table_info({t})')]
        print(f'{t}: {cnt} records | columns: {cols}')
    except Exception as e:
        print(f'{t}: ERROR - {e}')

# Students per class with program
print("\n=== STUDENTS PER CLASS (with program) ===")
for r in cur.execute("""
    SELECT c.kode, c.program, c.seksi, COUNT(s.id)
    FROM students s JOIN classes c ON s.kelas_id = c.id
    GROUP BY c.kode, c.program ORDER BY c.kode
"""):
    print(r)

# Teachers sample
print("\n=== TEACHERS SAMPLE ===")
for r in cur.execute('SELECT id, nama, jabatan, status FROM teachers LIMIT 5'):
    print(r)

con.close()
