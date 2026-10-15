import sqlite3, subprocess, os, datetime

base = "/opt/data/home/workspace/dev/pondok-banat"

print("=== SYSTEM DATE ===")
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z"))

con = sqlite3.connect(os.path.join(base, "dev.db"))
cur = con.cursor()

print("\n=== DB SUMMARY ===")
for row in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
    cnt = cur.execute(f"SELECT COUNT(*) FROM {row[0]}").fetchone()[0]
    print(f"{row[0]}: {cnt}")

print("\n=== UID NFC ===")
cols = [r[1] for r in cur.execute("PRAGMA table_info(students)")]
print("uid_nfc in columns:", "uid_nfc" in cols)
cnt = cur.execute("SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL").fetchone()[0]
print("students with uid_nfc filled:", cnt)

print("\n=== STUDENTS PER CLASS (DISTRIBUTION) ===")
rows = cur.execute("""SELECT c.kode, c.program, c.seksi, COUNT(s.id) FROM students s
JOIN classes c ON s.kelas_id = c.id GROUP BY c.kode, c.program ORDER BY c.kode""").fetchall()
tot = 0
for r in rows:
    print(r, "count:", r[3])
    tot += r[3]
print("TOTAL:", tot)

print("\n=== GRADES TOTAL ===")
print(cur.execute("SELECT COUNT(*) FROM grades").fetchone()[0])

print("\n=== TEACHERS STATUS ===")
for r in cur.execute("SELECT status, COUNT(*) FROM teachers GROUP BY status"):
    print(r)

print("\n=== ROLES ===")
for r in cur.execute("SELECT name, COUNT(*) FROM roles GROUP BY name"):
    print(r)

print("\n=== ROLE PERMISSIONS ===")
rp = cur.execute("SELECT COUNT(*) FROM role_permissions").fetchone()[0]
print("role_permissions count:", rp)

print("\n=== USERS ===")
for r in cur.execute("SELECT id, email, role FROM users"):
    print(r)

con.close()

# Build quality gates
print("\n=== BUILD QUALITY GATES ===")
for cmd in [["npm", "run", "type-check"], ["npm", "run", "lint"], ["npm", "run", "build"]]:
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=base)
    print(f"{' '.join(cmd)}: exit={r.returncode}")
    if r.returncode != 0:
        out = (r.stdout or '') + (r.stderr or '')
        for line in out.splitlines()[-5:]:
            print("   ", line)
