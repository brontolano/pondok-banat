import sqlite3

conn = sqlite3.connect("/opt/data/home/workspace/dev/pondok-banat/dev.db")
cur = conn.cursor()

print("=== FINAL STATE (Rev. 8 update) ===")
print("users:", cur.execute("SELECT COUNT(*) FROM users").fetchone()[0])
print("roles:", cur.execute("SELECT COUNT(*) FROM roles").fetchone()[0])
print("role_permissions:", cur.execute("SELECT COUNT(*) FROM role_permissions").fetchone()[0])
print("students:", cur.execute("SELECT COUNT(*) FROM students").fetchone()[0])
print("classes:", cur.execute("SELECT COUNT(*) FROM classes").fetchone()[0])
print("teachers:", cur.execute("SELECT COUNT(*) FROM teachers").fetchone()[0])
print("subjects:", cur.execute("SELECT COUNT(*) FROM subjects").fetchone()[0])
print("silabus:", cur.execute("SELECT COUNT(*) FROM silabus").fetchone()[0])
print("rpp:", cur.execute("SELECT COUNT(*) FROM rpp").fetchone()[0])
print("grades:", cur.execute("SELECT COUNT(*) FROM grades").fetchone()[0])
print("rapor:", cur.execute("SELECT COUNT(*) FROM rapor").fetchone()[0])
print("announcements:", cur.execute("SELECT COUNT(*) FROM announcements").fetchone()[0])
print("messages:", cur.execute("SELECT COUNT(*) FROM messages").fetchone()[0])
print("notifications:", cur.execute("SELECT COUNT(*) FROM notifications").fetchone()[0])

print("\n=== TEACHER SAMPLE (imported 54) ===")
for r in cur.execute("SELECT nip, name, jabatan, kelas_id FROM teachers LIMIT 5"):
    print(" ", r[0], "|", r[1], "|", r[2])

print("\n=== CLASSES (15) ===")
for r in cur.execute("SELECT kode, nama, jenjang FROM classes ORDER BY kode"):
    print(" ", r[0], "|", r[1], "|", r[2])

conn.close()
print("\nDone.")
