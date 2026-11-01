import sqlite3, os, subprocess, sys

base = "/opt/data/home/workspace/dev/pondok-banat"
db = os.path.join(base, "dev.db")

print("=== DEV.DB ===")
if not os.path.exists(db):
    print("dev.db ABSENT")
else:
    con = sqlite3.connect(db)
    cur = con.cursor()
    tables = [r[0] for r in cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]
    print("TABLE COUNT:", len(tables))
    total_students = 0
    for t in tables:
        cnt = cur.execute('SELECT COUNT(*) FROM "%s"' % t).fetchone()[0]
        if t == "students":
            total_students = cnt
        print("  %s: %d" % (t, cnt))
    # student active count and uid_nfc count
    with con:
        qc = con.execute('SELECT COUNT(*) FROM students')
        print("  students row count:", qc.fetchone()[0])
    try:
        cur.execute('SELECT COUNT(*) FROM students WHERE active=1')
        print("  students.active=1:", cur.fetchone()[0])
    except Exception as e:
        print("  students.active=1: n/a (schema-only, no rows)")
    try:
        cur.execute('SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ""')
        print("  students.uid_nfc NOT NULL:", cur.fetchone()[0])
    except Exception as e:
        print("  students.uid_nfc NOT NULL: n/a (schema-only, no rows)")
    con.close()
    print("TOTAL students:", total_students)

print("=== NODE_MODULES ===")
nm = os.path.join(base, "node_modules")
if os.path.isdir(nm):
    nd = 0
    nf = 0
    for r, ds, fs in os.walk(nm):
        nd += len(ds)
        nf += len(fs)
    print("node_modules EXISTS; total files:", nf, "total dirs:", nd)
else:
    print("node_modules ABSENT")

print("=== BUILD GATES ===")
for cmd in [["npx", "tsc", "--noEmit"], ["npx", "eslint", "."]]:
    r = subprocess.run(cmd, cwd=base, capture_output=True, text=True, timeout=120)
    print("CMD:", " ".join(cmd), "EXIT:", r.returncode)
    out = (r.stdout or "") + (r.stderr or "")
    print(out[:1500])
