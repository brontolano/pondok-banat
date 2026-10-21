import os, subprocess

print("=== GIT STATE ===")
r = subprocess.run(["git","rev-parse","HEAD"],capture_output=True,text=True); print("HEAD:", r.stdout.strip())
r = subprocess.run(["git","branch","--show-current"],capture_output=True,text=True); print("BRANCH:", r.stdout.strip())
r = subprocess.run(["git","rev-list","--count","--left-right","HEAD...@{u}"],capture_output=True,text=True); print("AHEAD/BEHIND:", r.stdout.strip().replace("\t"," / "))
r = subprocess.run(["git","rev-parse","origin/main"],capture_output=True,text=True); print("REMOTE_HEAD:", r.stdout.strip())
print("UNTRACKED:", subprocess.run(["git","ls-files","--others","--exclude-standard"],capture_output=True,text=True).stdout.strip())

print("\n=== FILES ===")
print("dev.db exists:", os.path.exists("dev.db"))
print(".data-pondokanat exists:", os.path.isdir(".data-pondokanat"))
print("PRD size:", os.path.getsize("PRD-PONDOK-BANAT.md"))
print("node_modules:", os.path.isdir("node_modules"))
print(".next:", os.path.isdir(".next"))
print("prisma/schema.prisma:", os.path.exists("prisma/schema.prisma"))

print("\n=== BUILD GATE ===")
for cmd in [["npx","tsc","--noEmit"],["npx","eslint","."]]:
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(f"{' '.join(cmd)} -> exit {r.returncode}", "stderr:", r.stderr[:200] if r.stderr else "")

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

print("\n=== SRC FILE CHECKS ===")
for f in ["src/components/Login.tsx","src/components/Beranda.tsx","src/app/beranda/page.tsx"]:
    if os.path.exists(f):
        c = open(f).read()
        print(f, "-> admin123 hardcoded:", "admin123" in c, "| totalSantri count:", c.count("totalSantri"))
    else:
        print(f, "NOT FOUND")

print("\n=== SRC APP STRUCTURE ===")
if os.path.isdir("src/app"):
    print("src/app subdirs:", sorted([d for d in os.listdir("src/app") if os.path.isdir(os.path.join("src/app",d))]))
print("src/components:", sorted(os.listdir("src/components")) if os.path.isdir("src/components") else "no dir")

print("\n=== SRC LIB ===")
print("src/lib files:", os.listdir("src/lib") if os.path.isdir("src/lib") else "empty/missing")
