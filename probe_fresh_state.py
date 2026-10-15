import sqlite3, subprocess, os, glob

repo = '/opt/data/home/workspace/dev/pondok-banat'
conn = sqlite3.connect(repo + '/dev.db')
cur = conn.cursor()

print('=== FRESH STATE VERIFICATION ===')
print()
print('--- Database (dev.db) ---')
tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
print('Total tables:', len(tables))
for t in tables:
    cnt = cur.execute('SELECT COUNT(*) FROM "%s"' % t).fetchone()[0]
    print('  %s: %d record' % (t, cnt))
print()
print('--- Siswa per kelas ---')
for row in cur.execute('SELECT c.kode, c.seksi, c.program, COUNT(s.id) FROM classes c LEFT JOIN students s ON s.kelas_id = c.id GROUP BY c.kode, c.seksi, c.program ORDER BY c.kode'):
    print(' ', row)
print()
print('--- UID NFC filled ---')
print(' ', cur.execute('SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ""').fetchone()[0])
print()
print('--- Auth hardcode check ---')
with open(repo + '/src/components/Login.tsx') as f:
    login = f.read()
if 'admin123' in login:
    print('  Auth: hardcoded password admin123 FOUND')
else:
    print('  Auth: no hardcoded password')
if 'admin@pondokanbat.com' in login:
    print('  Auth: hardcoded email admin@pondokanbat.com FOUND')
else:
    print('  Auth: no hardcoded email')
print()
print('--- Beranda hardcode check ---')
with open(repo + '/src/components/Beranda.tsx') as f:
    beranda = f.read()
for val in ['441', '54', '18']:
    if val in beranda:
        print('  Beranda: hardcoded %s found' % val)
    else:
        print('  Beranda: %s not found (dynamic?)' % val)
print()
print('--- prisma/schema.prisma ---')
with open(repo + '/prisma/schema.prisma') as f:
    prisma = f.read()
if 'model KitabProgress' in prisma:
    print('  KitabProgress: model DEFINED (line %d)' % (prisma.find('model KitabProgress') + 1))
else:
    print('  KitabProgress: NOT DEFINED')
if 'model Sertakan' in prisma:
    print('  Sertakan: model DEFINED (line %d)' % (prisma.find('model Sertakan') + 1))
else:
    print('  Sertakan: NOT DEFINED')
print()
print('--- .next dir timestamp ---')
next_dirs = glob.glob(repo + '/.next/*', recursive=True)
if next_dirs:
    latest = max(os.path.getmtime(d) for d in next_dirs)
    import datetime
    print('  .next latest: ' + str(datetime.datetime.fromtimestamp(latest)))
print()
print('--- Repo file count ---')
n = 0
for root, dirs, files in os.walk(repo):
    dirs[:] = [d for d in dirs if d not in ('.next', 'node_modules', '.git')]
    n += len(files)
print('  Total files (excluding .next, node_modules, .git):', n)
print()
print('=== DONE ===')
conn.close()
