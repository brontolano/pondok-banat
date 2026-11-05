import sqlite3, os, sys
p = 'dev.db'
print('dev.db exists:', os.path.exists(p))
if os.path.exists(p):
    con = sqlite3.connect(p)
    cur = con.cursor()
    tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]
    print('table_count:', len(tables))
    total = 0
    for t in tables:
        try:
            n = cur.execute('SELECT COUNT(*) FROM ' + t).fetchone()[0]
        except Exception as e:
            n = 'ERR:' + str(e)
        print(t + ':', n)
        if isinstance(n, int):
            total += n
    print('total_records:', total)
    con.close()
