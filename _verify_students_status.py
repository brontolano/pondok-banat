import sqlite3

conn = sqlite3.connect('/opt/data/home/workspace/dev/pondok-banat/dev.db')
cur = conn.cursor()

# Check distinct status values in students
statuses = cur.execute("SELECT status, COUNT(*) FROM students GROUP BY status").fetchall()
print("Students status distribution:")
for s in statuses:
    print(f"  '{s[0]}': {s[1]}")

print()

# Check uid_nfc values (first few)
uid_vals = cur.execute("SELECT uid_nfc FROM students WHERE uid_nfc IS NOT NULL LIMIT 5").fetchall()
print("Sample uid_nfc values:")
for u in uid_vals:
    print(f"  '{u[0]}'")

# Check classes
print("\nClasses:")
for r in cur.execute("SELECT id, kode, seksi, nama, jenjang, program FROM classes"):
    print(f"  {r}")

# Check User records
print("\nUsers:")
for r in cur.execute("SELECT id, email, role FROM users"):
    print(f"  {r}")

# Check role_permissions
print("\nRole permissions count:", cur.execute("SELECT COUNT(*) FROM role_permissions").fetchone()[0])

# Check seed_users_roles.py for reference
# Check the prisma schema for Student model
print("\n--- Student model in prisma/schema.prisma ---")
with open('/opt/data/home/workspace/dev/pondok-banat/prisma/schema.prisma') as f:
    content = f.read()
    # Find Student model
    idx = content.find('model Student')
    if idx >= 0:
        # print through end of model
        end = content.find('{', idx)
        # find next '}' at same level
        depth = 0
        for i in range(end, len(content)):
            if content[i] == '{':
                depth += 1
            elif content[i] == '}':
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        print(content[idx:end])

conn.close()
