#!/usr/bin/env python3
import sqlite3, subprocess, json, os

base = "/opt/data/home/workspace/dev/pondok-banat"
db = os.path.join(base, "dev.db")
out = {}

con = sqlite3.connect(db)
cur = con.cursor()

def q(sql):
    cur.execute(sql)
    return cur.fetchall()

out["tables"] = [r[0] for r in q("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
out["user_count"] = q("SELECT COUNT(*) FROM users")[0][0]
out["role_count"] = q("SELECT COUNT(*) FROM roles")[0][0]
out["role_perm_count"] = q("SELECT COUNT(*) FROM role_permissions")[0][0]
out["student_count"] = q("SELECT COUNT(*) FROM students")[0][0]
out["student_active"] = q("SELECT COUNT(*) FROM students WHERE status='active'")[0][0]
out["student_uid_nfc_filled"] = q("SELECT COUNT(*) FROM students WHERE uid_nfc IS NOT NULL AND uid_nfc != ''")[0][0]
out["teacher_count"] = q("SELECT COUNT(*) FROM teachers")[0][0]
out["subject_count"] = q("SELECT COUNT(*) FROM subjects")[0][0]
out["grade_count"] = q("SELECT COUNT(*) FROM grades")[0][0]
out["class_count"] = q("SELECT COUNT(*) FROM classes")[0][0]
out["silabus_count"] = q("SELECT COUNT(*) FROM silabuS")[0][0] if q("SELECT COUNT(*) FROM silabus")[0][0] else 0
out["rpp_count"] = q("SELECT COUNT(*) FROM rpp")[0][0]
out["announcement_count"] = q("SELECT COUNT(*) FROM announcements")[0][0]
out["message_count"] = q("SELECT COUNT(*) FROM messages")[0][0]
out["notification_count"] = q("SELECT COUNT(*) FROM notifications")[0][0]

# Students per class
per_class = q("SELECT c.kode, c.seksi, c.jenjang, c.program, COUNT(*) FROM students s JOIN classes c ON s.kelas_id = c.id GROUP BY c.kode, c.seksi, c.jenjang, c.program ORDER BY c.jenjang, c.seksi")
out["students_per_class"] = [{"kode": r[0], "seksi": r[1], "jenjang": r[2], "program": r[3], "n": r[4]} for r in per_class]

con.close()

# Save to a JSON file for later use
with open(os.path.join(base, "db_fresh_check.json"), "w") as f:
    json.dump(out, f, indent=2)

# Print summary
print("=== FRESH DB VERIFICATION ===")
for k, v in out.items():
    if k != "students_per_class":
        print(f"{k}: {v}")

total = sum(r["n"] for r in out["students_per_class"])
print(f"students_per_class_total: {total}")
print("students_per_class:")
for r in out["students_per_class"]:
    print(f"  {r['jenjang']}{r['seksi']} {r['program']}: {r['n']}")
