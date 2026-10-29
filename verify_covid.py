import sqlite3, os, sys

BASE = "/opt/data/home/workspace/dev/pondok-banat"
DB = os.path.join(BASE, "dev.db")

print("=== DEV.DB ===")
if not os.path.exists(DB):
    print("MISSING dev.db")
else:
    print(f"dev.db size: {os.path.getsize(DB)} bytes")
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
    print(f"Tables ({len(tables)}): {tables}")
    print("Row counts:")
    for t in tables:
        try:
            n = cur.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0]
            print(f"  {t}: {n}")
        except Exception as e:
            print(f"  {t}: ERR {e}")
    n_students = cur.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    n_uid = cur.execute('SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ""').fetchone()[0]
    print(f"uid_nfc filled: {n_uid}/{n_students}")
    conn.close()

print()
print("=== GIT ===")
print(f"HEAD: {os.popen('cd %s && git rev-parse HEAD' % BASE).read().strip()}")
print(f"COUNT HEAD: {os.popen('cd %s && git rev-list --count HEAD' % BASE).read().strip()}")
print(f"ORIGIN/HEAD: {os.popen('cd %s && git rev-parse origin/main 2>/dev/null || echo MISSING' % BASE).read().strip()}")
print(f"AHEAD/BEHIND: {os.popen('cd %s && git rev-list --count --left-right HEAD...origin/main 2>/dev/null || echo n/a' % BASE).read().strip()}")
print(f"STATUS (short): {os.popen('cd %s && git status --short' % BASE).read().strip()}")
print(f"LS-FILES count: {os.popen('cd %s && git ls-files | wc -l' % BASE).read().strip()}")

print()
print("=== SOURCE DATA FILES (.data-pondokaneat) ===")
d = os.path.join(BASE, ".data-pondokanat")
if os.path.isdir(d):
    for f in sorted(os.listdir(d)):
        p = os.path.join(d, f)
        print(f"  {f} ({os.path.getsize(p)} bytes)")
else:
    print("MISSING .data-pondokanat")
