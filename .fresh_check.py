import os, sqlite3, subprocess

print("=== GIT STATE ===")
r = subprocess.run(["git","rev-parse","HEAD"],capture_output=True,text=True)
print("HEAD:", r.stdout.strip())
r = subprocess.run(["git","branch","--show-current"],capture_output=True,text=True)
print("BRANCH:", r.stdout.strip())
r = subprocess.run(["git","rev-list","--count","--left-right","HEAD...@{u}"],capture_output=True,text=True)
print("AHEAD/BEHIND:", r.stdout.strip().replace("\t"," / "))
r = subprocess.run(["git","rev-parse","origin/main"],capture_output=True,text=True)
print("REMOTE_HEAD:", r.stdout.strip())

print("\n=== FILES ===")
print("dev.db exists:", os.path.exists("dev.db"), os.path.getsize("dev.db") if os.path.exists("dev.db") else "-")
print(".data-pondokanat exists:", os.path.isdir(".data-pondokanat"), os.listdir(".data-pondokanat") if os.path.isdir(".data-pondokanat") else "-")
print("PRD size:", os.path.getsize("PRD-PONDOK-BANAT.md"))
print("node_modules:", os.path.isdir("node_modules"))
print(".next:", os.path.isdir(".next"))

print("\n=== BUILD GATE ===")
for cmd in [["npx","tsc","--noEmit"],["npx","eslint","."],["npx","next","build"]]:
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(f"{' '.join(cmd[1:])} -> exit {r.returncode}")

print("\n=== SCHEMA CHECK ===")
if os.path.exists("prisma/schema.prisma"):
    content = open("prisma/schema.prisma").read()
    print("KitabProgress defined:", "model KitabProgress" in content)
    print("Sertakan defined:", "model Sertakan" in content)
    print("uidNfc defined:", "uidNfc" in content)

print("\n=== AUTH / BERANDA HARCODED ===")
for f in ["src/components/Login.tsx","src/components/Beranda.tsx","src/app/beranda/page.tsx"]:
    if os.path.exists(f):
        c = open(f).read()
        print(f, "-> admin123:", "admin123" in c, "| totalSantri count:", c.count("totalSantri"))
