#!/usr/bin/env python3
"""Fresh verification of repo + dev.db, compare against PRD stated state."""
import sqlite3, os, subprocess, re

REPO = "/opt/data/home/workspace/dev/pondok-banat"
db = os.path.join(REPO, "dev.db")

print("=" * 60)
print("FRESH VERIFICATION — 14 Oktober 2026")
print("=" * 60)

# 1. dev.db state
con = sqlite3.connect(db)
cur = con.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [r[0] for r in cur.fetchall()]
print("\n[1] dev.db tables (%d):" % len(tables))
for t in tables:
    cur.execute("SELECT COUNT(*) FROM \"%s\"" % t)
    cnt = cur.fetchone()[0]
    print("    %s: %d" % (t, cnt))

# role_permissions detail
cur.execute("SELECT COUNT(*) FROM role_permissions")
rp = cur.fetchone()[0]
print("    role_permissions: %d" % rp)

# users
cur.execute("SELECT id, email, role FROM users")
users = cur.fetchall()
print("    users:")
for u in users:
    print("      ", u)

# students uid_nfc counts
cur.execute("SELECT COUNT(*), SUM(CASE WHEN uid_nfc > '' THEN 1 ELSE 0 END) FROM students")
print("    students with uid_nfc filled:", cur.fetchone()[1])

# 2. prisma/schema.prisma
print("\n[2] prisma/schema.prisma")
schema_path = os.path.join(REPO, "prisma", "schema.prisma")
schema_txt = open(schema_path).read()
print("    KitabProgress defined:", "model KitabProgress" in schema_txt)
print("    Sertakan defined:", "model Sertakan" in schema_txt)
print("    uidNfc defined:", "uidNfc" in schema_txt)

# 3. Login.tsx
print("\n[3] src/components/Login.tsx")
login_txt = open(os.path.join(REPO, "src", "components", "Login.tsx")).read()
print("    admin@pondokanat.com:", "admin@pondokanat.com" in login_txt)
print("    admin@pondokanbat.com (typo):", "admin@pondokanbat.com" in login_txt)
print("    admin123:", "admin123" in login_txt)

# 4. Beranda.tsx
print("\n[4] src/components/Beranda.tsx")
beranda_txt = open(os.path.join(REPO, "src", "components", "Beranda.tsx")).read()
print("    totalSantri: 441:", "totalSantri: 441" in beranda_txt)
print("    totalGuru: 54:", "totalGuru: 54" in beranda_txt)
print("    totalKelas: 18:", "totalKelas: 18" in beranda_txt)

# 5. Build quality gate
print("\n[5] Build quality gate")
for cmd in [["npm", "run", "type-check"], ["npm", "run", "lint"], ["npm", "run", "build"]]:
    r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, timeout=300)
    print("    %s: exit=%d" % (" ".join(cmd), r.returncode))
    if r.returncode != 0:
        out = (r.stdout or "") + (r.stderr or "")
        print("      STDOUT:", out[:500])
        print("      STDERR:", out[-500:])

# 6. Compare with PRD stated state
print("\n[6] Comparison vs PRD Rev.43 stated state")
prd = open(os.path.join(REPO, "PRD-PONDOK-BANAT.md")).read()
checks = {
    "1 user (admin)": "1 user (admin@pondokanat.com" in prd,
    "5 role": "5 role" in prd,
    "33 role_permissions": "33 role_permissions" in prd,
    "441 siswa": "441 siswa" in prd,
    "18 kelas": "18 kelas" in prd,
    "54 guru": "54 guru" in prd,
    "32 mapel": "32 mapel" in prd,
    "5.420 nilai": "5.420 nilai" in prd,
    "0 silabus/rpp": "0 record" in prd,
    "Login hardcode": "auth hardcode" in prd.lower(),
    "Beranda hardcode": "Beranda hardcode" in prd,
    "KitabProgress ref": "KitabProgress" in prd,
    "Sertakan ref": "Sertakan" in prd,
}
for k, v in checks.items():
    print("    %-25s: %s" % (k, "✓" if v else "✗ MISSING from PRD!"))

print("\nDONE")
