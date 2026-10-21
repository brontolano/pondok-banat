#!/usr/bin/env python3
# Fresh verification for PRD-PONDOK-BANAT (Rev 393 cron run)
import os, sqlite3, subprocess, json

REPO = "/opt/data/home/workspace/dev/pondok-banat"
results = {}

def run(cmd, shell=True):
    try:
        r = subprocess.run(cmd, shell=shell, cwd=REPO, capture_output=True, text=True, timeout=120)
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except Exception as e:
        return -1, "", str(e)

# 1. git HEAD / branch
rc, out, err = run("git rev-parse HEAD")
results["git_head"] = out
rc, out, err = run("git rev-parse --abbrev-ref HEAD")
results["git_branch"] = out
rc, out, err = run("git status -sb")
results["git_status"] = out.replace("\n", " | ")
rc, out, err = run("git rev-list --count origin/main..HEAD")
results["ahead"] = out
rc, out, err = run("git rev-list --count HEAD..origin/main")
results["behind"] = out

# 2. dev.db
results["dev_db_exists"] = os.path.exists(f"{REPO}/dev.db")

# 3. node_modules
results["node_modules_exists"] = os.path.exists(f"{REPO}/node_modules")

# 4. .next
results["next_exists"] = os.path.exists(f"{REPO}/.next")

# 5. tracked files
rc, out, err = run("git ls-files | wc -l")
results["tracked_files"] = out

# 6. dev.db summary (if present) - table count and sample row counts
if results["dev_db_exists"]:
    try:
        con = sqlite3.connect(f"{REPO}/dev.db")
        cur = con.cursor()
        tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
        results["tables"] = tables
        summary = {}
        for t in tables:
            try:
                n = cur.execute(f"SELECT COUNT(*) FROM [{t}]").fetchone()[0]
                summary[t] = n
            except Exception:
                summary[t] = "error"
        results["row_counts"] = summary
        con.close()
    except Exception as e:
        results["db_error"] = str(e)

# 7. build gates (npx) - skip if node_modules absent
if results["node_modules_exists"]:
    rc, out, err = run("npx tsc --noEmit")
    results["tsc_rc"] = rc
    rc, out, err = run("npx eslint .")
    results["eslint_rc"] = rc
    rc, out, err = run("npx next build")
    results["nextbuild_rc"] = rc
else:
    results["tsc_rc"] = None
    results["eslint_rc"] = None
    results["nextbuild_rc"] = None

print(json.dumps(results, indent=2, default=str))
