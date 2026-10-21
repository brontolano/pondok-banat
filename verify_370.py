import re, os, subprocess

# --- Fresh verification (re-run for the record) ---
print("=== GIT ===")
r = subprocess.run(["git","rev-parse","HEAD"],capture_output=True,text=True); print("HEAD:", r.stdout.strip())
r = subprocess.run(["git","rev-list","--count","--left-right","HEAD...@{u}"],capture_output=True,text=True); print("AHEAD/BEHIND:", r.stdout.strip().replace("\t"," / "))
r = subprocess.run(["git","rev-parse","origin/main"],capture_output=True,text=True); print("REMOTE:", r.stdout.strip())
print("dev.db exists:", os.path.exists("dev.db"))
print(".data-pondokanat exists:", os.path.isdir(".data-pondokanat"))
pr = os.path.getsize("PRD-PONDOK-BANAT.md"); print("PRD size:", pr)
print("node_modules:", os.path.isdir("node_modules"))
print(".next:", os.path.isdir(".next"))

p = "prisma/schema.prisma"
prisma = open(p).read() if os.path.exists(p) else ""
print("KitabProgress:", "model KitabProgress" in prisma)
print("Sertakan:", "model Sertakan" in prisma)
print("uidNfc:", "uidNfc" in prisma)

for f in ["src/components/Login.tsx","src/components/Beranda.tsx","src/app/beranda/page.tsx"]:
    fp = os.path.join("src", f)
    if os.path.exists(fp):
        c = open(fp).read()
        print(f, "| admin123:", "admin123" in c, "| totalSantri count:", c.count("totalSantri"))

print("=== DONE ===")
