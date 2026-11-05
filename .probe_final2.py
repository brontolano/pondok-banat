import subprocess, sqlite3, os

def run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd or '/opt/data/home/workspace/dev/pondok-banat', capture_output=True, text=True).stdout.strip()

print("=== GIT ===")
print("HEAD:", run(['git','rev-parse','HEAD']))
print("HEAD_SHORT:", run(['git','rev-parse','--short','HEAD']))
print("TOTAL_LOCAL:", run(['git','rev-list','--count','HEAD']))
print("AHEAD:", run(['git','rev-list','--count','origin/main..HEAD']))
print("BEHIND:", run(['git','rev-list','--count','HEAD..origin/main']))
print("UNTRACKED_COUNT:", len(run(['git','ls-files','--others','--exclude-standard']).splitlines()))
print("BRANCH:", run(['git','branch','--show-current']))

print("\n=== DEV.DB ===")
db = '/opt/data/home/workspace/dev/pondok-banat/dev.db'
con = sqlite3.connect(db)
cur = con.cursor()
tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
print("TABLES:", len(tables), tables)
for t in tables:
    cnt = cur.execute(f"SELECT COUNT(*) FROM '{t}'").fetchone()[0]
    print(f"  {t}: {cnt}")
con.close()

print("\n=== NODE_MODULES ===")
nm = '/opt/data/home/workspace/dev/pondok-banat/node_modules'
files = dirs = 0
for root, ds, fs in os.walk(nm):
    dirs += len(ds)
    files += len(fs)
print("node_modules files:", files, "dirs:", dirs)

print("\n=== GIT LOG (last 12) ===")
print(run(['git','log','--oneline','-12']))
