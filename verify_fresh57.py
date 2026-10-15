import sqlite3, os, subprocess

repo = "/opt/data/home/workspace/dev/pondok-banat"
db = os.path.join(repo, "dev.db")

print("=== DEV.DB STATE ===")
con = sqlite3.connect(db)
cur = con.cursor()

tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
print("Total tables:", len(tables))
for t in tables:
    try:
        cnt = cur.execute("SELECT COUNT(*) FROM [" + t + "]").fetchone()[0]
    except Exception as e:
        cnt = "ERR:" + str(e)
    print("  %s: %s" % (t, cnt))

print("\nStudents per kelas:")
dist = cur.execute("SELECT kelas, COUNT(*) FROM students GROUP BY kelas ORDER BY kelas").fetchall()
for k, v in dist:
    print("  %s: %s" % (k, v))
print("  TOTAL:", sum(v for _, v in dist))

uid_nfc = cur.execute("SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND TRIM(uid_nfc) != ''").fetchone()[0]
print("\nuid_nfc non-null:", uid_nfc)

print("\nAdmin user:", cur.execute("SELECT id, email, role FROM users LIMIT 1").fetchone())
print("Total users:", cur.execute("SELECT COUNT(*) FROM users").fetchone()[0])
print(" Roles:", cur.execute("SELECT COUNT(*) FROM roles").fetchone()[0])
print(" Role_permissions:", cur.execute("SELECT COUNT(*) FROM role_permissions").fetchone()[0])
print(" Teachers:", cur.execute("SELECT COUNT(*) FROM teachers").fetchone()[0])
print(" Subjects:", cur.execute("SELECT COUNT(*) FROM subjects").fetchone()[0])
print(" Grades:", cur.execute("SELECT COUNT(*) FROM grades").fetchone()[0])
print(" Classes:", cur.execute("SELECT COUNT(*) FROM classes").fetchone()[0])
print(" Students active=0:", cur.execute("SELECT COUNT(*) FROM students WHERE active = 0").fetchone()[0])
print(" Students active>0:", cur.execute("SELECT COUNT(*) FROM students WHERE active > 0").fetchone()[0])
print(" Announcements:", cur.execute("SELECT COUNT(*) FROM announcements").fetchone()[0])
print(" Messages:", cur.execute("SELECT COUNT(*) FROM messages").fetchone()[0])
print(" Notifications:", cur.execute("SELECT COUNT(*) FROM notifications").fetchone()[0])

print("\n=== BUILD QUALITY GATE ===")
for cmd in [["npx", "tsc", "--noEmit"], ["npm", "run", "lint"], ["npm", "run", "build"]]:
    try:
        p = subprocess.run(cmd, cwd=repo, capture_output=True, text=True, timeout=900)
        print("%s: exit=%s" % (" ".join(cmd), p.returncode))
        if p.stdout.strip():
            print("  STDOUT tail:", p.stdout.strip()[-400:])
        if p.stderr.strip():
            print("  STDERR tail:", p.stderr.strip()[-400:])
    except subprocess.TimeoutExpired:
        print("%s: TIMEOUT" % " ".join(cmd))

con.close()
