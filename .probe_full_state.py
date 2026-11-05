import subprocess, os, sqlite3, json

repo = "/opt/data/home/workspace/dev/pondok-banat"

def run(cmd):
    r = subprocess.run(cmd, cwd=repo, capture_output=True, text=True)
    return r.stdout.strip(), r.stderr.strip(), r.returncode

print("=== GIT HEAD ===")
out, err, rc = run(["git", "log", "-1", "--pretty=format:%H | %s"])
print(out)
print("=== COMMIT COUNT (local) ===")
out, err, rc = run(["git", "rev-list", "--count", "HEAD"])
print("local:", out)
print("=== AHEAD/BEHIND origin_main ===")
out, err, rc = run(["git", "rev-list", "--left-right", "--count", "HEAD...origin_main"])
print("ahead/behind:", out)
print("=== NODE_MODULES ===")
nm = os.path.join(repo, "node_modules")
if os.path.isdir(nm):
    dirs = sum([len(d) for d in os.walk(nm)])
    # count top-level dirs
    top = [d for d in os.listdir(nm) if os.path.isdir(os.path.join(nm, d))]
    print("top dirs:", len(top))
    # count files
    files = sum([len(files) for _, _, files in os.walk(nm)])
    print("files:", files)
else:
    print("node_modules ABSENT")
print("=== GIT STATUS ===")
out, err, rc = run(["git", "status", "--porcelain"])
lines = [l for l in out.splitlines() if l.strip()]
untracked = [l for l in lines if l.startswith("??")]
deleted = [l for l in lines if l.startswith(" D")]
print("total lines:", len(lines))
print("untracked:", len(untracked))
print("deleted:", len(deleted))
print("=== DB STATE ===")
db = os.path.join(repo, "dev.db")
if os.path.exists(db):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [r[0] for r in cur.fetchall()]
    print("tables:", len(tables))
    for t in tables:
        cur.execute('SELECT COUNT(*) FROM "%s"' % t)
        print("  %s: %d" % (t, cur.fetchone()[0]))
else:
    print("dev.db ABSENT")
print("=== BUILD GATES ===")
for cmd in [["npm", "run", "type-check"], ["npm", "run", "lint"]]:
    out, err, rc = run(cmd)
    print("CMD:", " ".join(cmd), "exit:", rc)
    if out: print("  stdout:", out[:200])
    if err: print("  stderr:", err[:200])
