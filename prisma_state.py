#!/usr/bin/env python3
import sqlite3, os

root = '/opt/data/home/workspace/dev/pondok-banat'
db_path = os.path.join(root, 'dev.db')
con = sqlite3.connect(db_path)
cur = con.cursor()

# students count by class
cur.execute("""
    SELECT c.nama, COUNT(s.id) 
    FROM classes c 
    LEFT JOIN students s ON s.kelas_id = c.id 
    GROUP BY c.id 
    ORDER BY c.id
""")
print("=== students per class ===")
for r in cur.fetchall():
    print(r)

# pages in src/app
print("\n=== src/app tree ===")
for dirpath, dirnames, filenames in os.walk(os.path.join(root, 'src', 'app')):
    dirnames[:] = [d for d in dirnames if d not in ('node_modules',)]
    rel = os.path.relpath(dirpath, os.path.join(root, 'src', 'app'))
    depth = 0 if rel == '.' else rel.count(os.sep) + 1
    print("  " * depth + os.path.basename(dirpath) + "/")
    for f in sorted(filenames):
        print("  " * (depth + 1) + f)

print("\n=== src/components ===")
comp_dir = os.path.join(root, 'src', 'components')
for f in sorted(os.listdir(comp_dir)):
    print(f)

print("\n=== src/lib ===")
lib_dir = os.path.join(root, 'src', 'lib')
for f in sorted(os.listdir(lib_dir)):
    print(f)

print("\n=== prisma/schema.prisma ===")
with open(os.path.join(root, 'prisma', 'schema.prisma'), 'r') as fh:
    content = fh.read()
# Print the Student model section
idx = content.find('model Student')
if idx >= 0:
    print(content[idx:idx+1500])
