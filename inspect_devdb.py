import sqlite3, os
path = '/opt/data/home/workspace/dev/pondok-banat/dev.db'
c = sqlite3.connect(path)
tabs = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
print('TABLES:', len(tabs))
total = 0
for t in tabs:
    n = c.execute('SELECT COUNT(*) FROM "%s"' % t).fetchone()[0]
    total += n
    print('  %s: %d' % (t, n))
print('TOTAL RECORDS:', total)
print('DB SIZE:', os.path.getsize(path))
