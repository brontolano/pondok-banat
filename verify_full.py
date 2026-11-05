import sqlite3, os, subprocess

repo = "/opt/data/home/workspace/dev/pondok-banat"
conn = sqlite3.connect(repo + "/dev.db")
cur = conn.cursor()
tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
print("TABLES: " + str(len(tables)))
total = 0
for t in tables:
    cnt = cur.execute('SELECT COUNT(*) FROM "' + t + '"').fetchone()[0]
    total += cnt
    print("  " + t + ": " + str(cnt))
print("TOTAL_ROWS: " + str(total))
n = cur.execute('SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ""').fetchone()[0]
print("students_with_uid_nfc: " + str(n))
conn.close()

print("node_modules exists: " + str(os.path.isdir(repo + "/node_modules")))
print(".next exists: " + str(os.path.isdir(repo + "/.next")))
print("dev.db size: " + str(os.path.getsize(repo + "/dev.db")))
nm_dirs = len([d for d in os.listdir(repo + "/node_modules") if os.path.isdir(repo + "/node_modules/" + d)])
print("node_modules dirs: " + str(nm_dirs))

r = subprocess.run(["git", "rev-list", "--count", "HEAD"], capture_output=True, text=True, cwd=repo)
print("local commits: " + r.stdout.strip())

r = subprocess.run(["git", "rev-list", "--count", "--left-right", "@{u}...HEAD"], capture_output=True, text=True, cwd=repo)
print("ahead/behind: " + r.stdout.strip())

r = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, cwd=repo)
untracked = [l for l in r.stdout.splitlines() if l.startswith("??")]
print("untracked files: " + str(len(untracked)))
