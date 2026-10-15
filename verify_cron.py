import sqlite3, os, subprocess, json

ws = "/opt/data/home/workspace/dev/pondok-banat"
db = os.path.join(ws, "dev.db")

print("=== DB CHECK ===")
conn = sqlite3.connect(db)
cur = conn.cursor()
cur.execute('SELECT name FROM sqlite_master WHERE type="table"')
tables = [r[0] for r in cur.fetchall()]
print("tables:", tables)
for t in ['users','roles','role_permissions','students','classes','teachers','subjects','silabus','rpp','grades','absensi','rapor','announcements','messages','notifications']:
    cur.execute('SELECT COUNT(*) FROM ' + t)
    print(t + ":", cur.fetchone()[0])
cur.execute('SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ""')
print("students with uid_nfc:", cur.fetchone()[0])
# License check on classes
cur.execute('SELECT COUNT(*) FROM classes')
print("classes total:", cur.fetchone()[0])
# teacher check
cur.execute('SELECT COUNT(*) FROM teachers')
print("teachers:", cur.fetchone()[0])
conn.close()

print("\n=== BUILD GATES ===")
for cmd in [["npx","tsc","--noEmit"], ["npx","eslint",".","--format","json"]]:
    r = subprocess.run(cmd, cwd=ws, capture_output=True, text=True, timeout=300)
    print(" ".join(cmd), "-> exit", r.returncode)
    if r.stdout.strip():
        print(r.stdout[:800])
    if r.stderr.strip():
        print(r.stderr[:800])

print("\n=== NEXT BUILD ===")
r = subprocess.run(["npx","next","build"], cwd=ws, capture_output=True, text=True, timeout=600)
print("next build -> exit", r.returncode)
if r.stdout.strip():
    print(r.stdout[-1500:])
if r.stderr.strip():
    print(r.stderr[-1500:])
