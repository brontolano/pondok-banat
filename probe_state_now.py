import sqlite3, os, glob, subprocess, datetime

proj = '/opt/data/home/workspace/dev/pondok-banat'

# --- DB summary ---
db = os.path.join(proj, 'dev.db')
con = sqlite3.connect(db)
cur = con.cursor()
tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
print('== TABLES ==')
for t in tables:
    cnt = cur.execute('SELECT COUNT(*) FROM "%s"' % t).fetchone()[0]
    print('  %s: %d' % (t, cnt))
print('== students sample ==')
for row in cur.execute('SELECT id, name, status, uid_nfc, kelas_id FROM students LIMIT 5'):
    print('  ', row)
print('== distinct uid_nfc ==')
print('  ', cur.execute('SELECT COUNT(DISTINCT uid_nfc) FROM students').fetchone()[0])
con.close()

# --- Files by mtime (recent) ---
print('== FILES (recent 24h) ==')
for root, dirs, files in os.walk(proj):
    # skip node_modules and .venv
    dirs[:] = [d for d in dirs if d not in ('node_modules', '.venv', '.git')]
    for f in files:
        p = os.path.join(root, f)
        st = os.stat(p)
        if st.st_mtime >= time.time() - 86400:
            print('  %s  %s' % (datetime.datetime.fromtimestamp(st.st_mtime).strftime('%m-%d %H:%M'), p))
