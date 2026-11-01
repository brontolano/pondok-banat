import sqlite3, os, subprocess, sys

base = "/opt/data/home/workspace/dev/pondok-banat"
print("DEV.DB EXISTS:", os.path.exists(os.path.join(base, "dev.db")))

if os.path.exists(os.path.join(base, "dev.db")):
    conn = sqlite3.connect(os.path.join(base, "dev.db"))
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [r[0] for r in cur.fetchall()]
    print("TABLE COUNT:", len(tables))
    for t in tables:
        try:
            cur.execute('SELECT COUNT(*) FROM "%s"' % t)
            print("  %s: %d" % (t, cur.fetchone()[0]))
        except Exception as e:
            print("  %s: ERROR %s" % (t, e))
    conn.close()
else:
    print("dev.db ABSENT")

print("===GIT HEAD===")
r = subprocess.run(["git", "log", "-1", "--format=%H %s"], cwd=base, capture_output=True, text=True)
print(r.stdout.strip(), r.stderr.strip())

print("===GIT COUNT===")
r = subprocess.run(["git", "rev-list", "--count", "HEAD"], cwd=base, capture_output=True, text=True)
print("local commits:", r.stdout.strip(), r.stderr.strip())

print("===GIT STATUS===")
r = subprocess.run(["git", "status", "--short"], cwd=base, capture_output=True, text=True)
print(r.stdout[:500])

print("===NODE VERSION===")
r = subprocess.run(["node", "--version"], capture_output=True, text=True)
print(r.stdout.strip(), r.stderr.strip())

print("===NPM VERSION===")
r = subprocess.run(["npm", "--version"], capture_output=True, text=True)
print(r.stdout.strip(), r.stderr.strip())

print("===NODE_MODULES===")
r = subprocess.run(["find", "node_modules", "-maxdepth", "2", "-type", "d"], cwd=base, capture_output=True, text=True)
dirs = [l for l in r.stdout.strip().split("\n") if l]
print("node_modules dirs (sample):", dirs[:5], "total:", len(dirs))
