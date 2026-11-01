import sqlite3, os

repo = "/opt/data/home/workspace/dev/pondok-banat"

# dev.db check
db = os.path.join(repo, "dev.db")
print("=== dev.db ===")
if os.path.exists(db):
    print("exists, size:", os.path.getsize(db))
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [r[0] for r in cur.fetchall()]
    print("tables:", len(tables))
    for t in tables:
        try:
            cur.execute("SELECT COUNT(*) FROM " + t)
            print("  " + t + ":", cur.fetchone()[0])
        except Exception as e:
            print("  " + t + ":", "ERR " + str(e))
    conn.close()
else:
    print("ABSENT")

# node_modules check
nm = os.path.join(repo, "node_modules")
print("=== node_modules ===")
if os.path.isdir(nm):
    print("dirs:", sum(os.path.isdir(os.path.join(nm, d)) for d in os.listdir(nm)))
    print("files:", sum(os.path.isfile(os.path.join(nm, f)) for f in os.listdir(nm)))
else:
    print("ABSENT")

# PRD header info
prd = os.path.join(repo, "PRD-PONDOK-BANAT.md")
print("=== PRD file ===")
if os.path.exists(prd):
    with open(prd, encoding="utf-8") as f:
        lines = f.readlines()
    print("total lines:", len(lines))
    print("first 15 lines:")
    for l in lines[:15]:
        print(l.rstrip())
