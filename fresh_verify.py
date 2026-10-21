import os, subprocess, sqlite3

def run(cmd, shell=False):
    r = subprocess.run(cmd, capture_output=True, text=True, shell=shell)
    return r.returncode, r.stdout.strip(), r.stderr.strip()

print("=== GIT STATE ===")
rc, out, err = run(["git","rev-parse","HEAD"]); print("HEAD:", out)
rc, out, err = run(["git","branch","--show-current"]); print("BRANCH:", out)
rc, out, err = run(["git","rev-list","--count","--left-right","HEAD...@{u}"]); print("AHEAD/BEHIND:", out.replace("\t"," / "))
rc, out, err = run(["git","rev-parse","origin/main"]); print("REMOTE_HEAD:", out)
rc, out, err = run(["git","log","--oneline","-1","HEAD"]); print("HEAD commit:", out)

print("\n=== FILES ===")
print("dev.db exists:", os.path.exists("dev.db"), os.path.getsize("dev.db") if os.path.exists("dev.db") else "-")
print(".data-pondokanat exists:", os.path.isdir(".data-pondokanat"))
print("PRD size:", os.path.getsize("PRD-PONDOK-BANAT.md"))
print("node_modules:", os.path.isdir("node_modules"))
print(".next:", os.path.isdir(".next"))
print("prisma/schema.prisma:", os.path.exists("prisma/schema.prisma"))

print("\n=== BUILD GATE ===")
for cmd in [["npx","tsc","--noEmit"],["npx","eslint","."]]:
    rc, out, err = run(cmd)
    print(f"{' '.join(cmd)} -> exit {rc}", "err:", err[:150] if err else "")

print("\n=== SCHEMA CHECK ===")
schema_path = "prisma/schema.prisma"
if os.path.exists(schema_path):
    c = open(schema_path).read()
    print("KitabProgress defined:", "model KitabProgress" in c)
    print("Sertakan defined:", "model Sertakan" in c)
    print("uidNfc defined:", "uidNfc" in c)
    for i,line in enumerate(c.splitlines(),1):
        if "model KitabProgress" in line or "model Sertakan" in line or "uidNfc" in line:
            print(f"  line {i}: {line.strip()[:100]}")

print("\n=== AUTH / BERANDA HARCODED ===")
for f in ["src/components/Login.tsx","src/components/Beranda.tsx","src/app/beranda/page.tsx"]:
    if os.path.exists(f):
        c = open(f).read()
        print(f, "-> admin123:", "admin123" in c, "| totalSantri count:", c.count("totalSantri"))
    else:
        print(f, "NOT FOUND")

print("\n=== SRC APP STRUCTURE ===")
if os.path.isdir("src/app"):
    print("src/app subdirs:", sorted([d for d in os.listdir("src/app") if os.path.isdir(os.path.join("src/app",d))]))
print("src/components:", sorted(os.listdir("src/components")) if os.path.isdir("src/components") else "no dir")
print("src/lib:", os.listdir("src/lib") if os.path.isdir("src/lib") else "empty/missing")

print("\n=== DB SCHEMA (if dev.db exists) ===")
if os.path.exists("dev.db"):
    con = sqlite3.connect("dev.db")
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [r[0] for r in cur.fetchall()]
    print("Tables:", tables)
    cur.execute("SELECT COUNT(*) FROM students")
    print("students count:", cur.fetchone()[0])
    cur.execute("SELECT COUNT(*) FROM classes")
    print("classes count:", cur.fetchone()[0])
    cur.execute("SELECT COUNT(*) FROM teachers")
    print("teachers count:", cur.fetchone()[0])
    con.close()
