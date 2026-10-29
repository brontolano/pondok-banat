import subprocess, os, sqlite3, json

repo = "/opt/data/home/workspace/dev/pondok-banat"

def run(cmd, cwd=repo):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr

results = {}

# 1. Git state
cmd = ["git", "rev-parse", "--short", "HEAD"]
rc, out, err = run(cmd)
results["HEAD"] = out.strip()

cmd = ["git", "rev-list", "--count", "HEAD"]
rc, out, err = run(cmd)
results["commit_count"] = out.strip()

cmd = ["git", "rev-list", "--count", "origin/main..HEAD"]
rc, out, err = run(cmd)
results["ahead"] = out.strip()

cmd = ["git", "rev-list", "--count", "HEAD..origin/main"]
rc, out, err = run(cmd)
results["behind"] = out.strip()

# 2. dev.db state
db = os.path.join(repo, "dev.db")
results["dev_db_exists"] = os.path.exists(db)
if os.path.exists(db):
    con = sqlite3.connect(db)
    cur = con.cursor()
    tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
    results["tables"] = tables
    counts = {}
    for t in tables:
        counts[t] = cur.execute(f"SELECT COUNT(*) FROM \"{t}\"").fetchone()[0]
    results["counts"] = counts
    con.close()

# 3. node_modules
nm = os.path.join(repo, "node_modules")
results["node_modules_exists"] = os.path.isdir(nm)
if os.path.isdir(nm):
    results["node_modules_count"] = len(os.listdir(nm))

# 4. Build gates
results["type_check"] = run(["npx", "tsc", "--noEmit"])[0]
results["lint"] = run(["npx", "eslint", "."])[0]
results["build"] = run(["npx", "next", "build"])[0]

print(json.dumps(results, indent=2))
