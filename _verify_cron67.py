#!/usr/bin/env python3
import sqlite3, os, subprocess, datetime

BASE = "/opt/data/home/workspace/dev/pondok-banat"
print("=== REPO STATE ===")
print("Path:", BASE)
print("dev.db exists:", os.path.exists(BASE + "/dev.db"))
print("dev.db size:", os.path.getsize(BASE + "/dev.db") if os.path.exists(BASE + "/dev.db") else "N/A")
print("PRD size:", os.path.getsize(BASE + "/PRD-PONDOK-BANAT.md"))

con = sqlite3.connect(BASE + "/dev.db")
cur = con.cursor()

print("\n=== DB TABLES ===")
tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
print(tables)

counts = {}
for t in ['users','roles','role_permissions','students','classes','teachers','subjects','silabus','rpp','absensi','grades','rapor','announcements','messages','notifications']:
    try:
        counts[t] = cur.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]
    except Exception as e:
        counts[t] = f"ERR:{e}"

print("\n=== TABLE COUNTS ===")
for t in counts:
    print(f"{t}: {counts[t]}")

# students summary
ns, sum_active, sum_uid = cur.execute("SELECT COUNT(*), SUM(active), SUM(uid_nfc IS NOT NULL) FROM students").fetchone()
print(f"\nStudents: total={ns}, active={sum_active}, uid_nfc_filled={sum_uid}")

# classes summary
cls_rows = cur.execute("SELECT kode, jenjang, program, (SELECT COUNT(*) FROM students s2 WHERE s2.kelas = classes.id) FROM classes ORDER BY kode").fetchall()
print(f"\nClasses: {len(cls_rows)}")
for r in cls_rows:
    print("  ", r)

# teachers
ng = cur.execute("SELECT COUNT(*) FROM teachers").fetchone()[0]
print(f"\nTeachers: {ng}")

# grades
ng2 = cur.execute("SELECT COUNT(*) FROM grades").fetchone()[0]
print(f"Grades: {ng2}")

# subjects, silabus, rpp
nsub = cur.execute("SELECT COUNT(*) FROM subjects").fetchone()[0]
nsil = cur.execute("SELECT COUNT(*) FROM silabus").fetchone()[0]
nrpp = cur.execute("SELECT COUNT(*) FROM rpp").fetchone()[0]
print(f"Subjects: {nsub}, Silabus: {nsil}, RPP: {nrpp}")

# role_permissions
nrp = cur.execute("SELECT COUNT(*) FROM role_permissions").fetchone()[0]
print(f"Role permissions: {nrp}")

con.close()
