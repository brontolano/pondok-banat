import os
import re

prd_path = "/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md"

with open(prd_path, "r") as f:
    content = f.read()
lines = content.split("\n")

print(f"=== FINAL FILE STATS ===")
print(f"Lines: {len(lines)}")
print(f"Size: {len(content)} chars")

rev_nums = re.findall(r"Rev\.\s*(\d+)[—\-]", content)
print(f"Revision numbers: {sorted(set(int(r) for r in rev_nums))}")

# Check all key sections present
sections = [
    "## 1. RINGKASAN PRODUK",
    "## 2. ARSITEKTUR MODULER",
    "## 3. KATALOG MODUL",
    "## 4. SISTEM PERAN & PERIZINAN",
    "## 5. DEPENDENCY & ACTIVATION",
    "## 6. ROADMAP",
    "## 7. OPEN QUESTIONS",
    "## 8. SOURCES & APPENDIX",
    "## 9. STATUS IMPLEMENTASI SAAT INI",
    "## 10. CATATAN PENGEMBANG",
]
print("\n=== SECTION CHECK ===")
for s in sections:
    print(f"  [{'✓' if s in content else '✗'}] {s}")

# Check build quality gate
print("\n=== BUILD GATE ===")
print(f"  tsc --noEmit: {'tsc --noEmit' in content}")
print(f"  npm run lint: {'npm run lint' in content}")
print(f"  npm run build: {'npm run build' in content}")

# Check key data points
print("\n=== KEY DATA POINTS ===")
data_points = [
    ("1 user (admin@pondokanat.com)", "1 user (admin@pondokanat.com, role admin)" in content),
    ("5 role", "5 role" in content),
    ("33 role_permissions", "33 role_permissions" in content),
    ("441 siswa", "441 siswa" in content),
    ("18 kelas", "18 kelas" in content),
    ("54 guru", "54 guru" in content),
    ("32 mapel", "32 mapel" in content),
    ("5.420 nilai", "5.420 nilai" in content),
    ("uid_nfc 0 filled", "uid_nfc" in content and "441 NULL" in content),
    ("Beranda 441/54/18", "totalSantri: 441" in content),
    ("KitabProgress undefined", "KitabProgress" in content),
]
for name, result in data_points:
    print(f"  [{'✓' if result else '✗'}] {name}")

print("\n=== NEW REVISION SECTION ===")
in_section = False
for i, line in enumerate(lines):
    if "### 10.2" in line:
        in_section = True
    elif in_section:
        if "Dibuat dari data" in line:
            break
        if line.strip():
            print(f"  {i+1}|{line[:130]}")

# Cleanup temp files
for f in ["rev27_section.md", "update_prd_rev27.py"]:
    fp = os.path.join("/opt/data/home/workspace/dev/pondok-banat", f)
    if os.path.exists(fp):
        os.remove(fp)
        print(f"\nCleaned up: {f}")
