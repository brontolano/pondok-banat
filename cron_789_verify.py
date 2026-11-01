import sqlite3, os, subprocess
base = '/opt/data/home/workspace/dev/pondok-banat'
print('=== GIT ===')
r = subprocess.run(['git', '-C', base, 'status', '--porcelain'], capture_output=True, text=True)
print('status bytes:', len(r.stdout))
for l in r.stdout.splitlines():
    print('  track:', l)
r = subprocess.run(['git', '-C', base, 'log', '--oneline', '-3'], capture_output=True, text=True)
print('log (3):')
print(r.stdout)
r = subprocess.run(['git', '-C', base, 'branch', '-v'], capture_output=True, text=True)
print('branch:', r.stdout.replace('\n', ' | '))
print('=== NODE_MODULES ===')
r = subprocess.run(['find', base + '/node_modules', '-type', 'd'], capture_output=True, text=True)
print('dirs:', len(r.stdout.splitlines()))
r = subprocess.run(['find', base + '/node_modules', '-type', 'f'], capture_output=True, text=True)
print('files:', len(r.stdout.splitlines()))
print('=== DEV.DB ===')
con = sqlite3.connect(base + '/dev.db')
tables = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
print('tables (%d):' % len(tables), tables)
for t in tables:
    try:
        n = con.execute('SELECT COUNT(*) FROM "%s"' % t).fetchone()[0]
        print('  %s: %d' % (t, n))
    except Exception as e:
        print('  %s: ERR %s' % (t, e))
print('dev.db size:', os.path.getsize(base + '/dev.db'))
con.close()
