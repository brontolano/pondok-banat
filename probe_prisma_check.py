import subprocess, os

repo = '/opt/data/home/workspace/dev/pondok-banat'

# prisma validate
print('=== PRISMA VALIDATE ===')
r = subprocess.run(['npx', 'prisma', 'validate'], cwd=repo, capture_output=True, text=True)
print('STDOUT:', r.stdout)
print('STDERR:', r.stderr)
print('EXIT:', r.returncode)
print()

# Check .next timestamp after our fresh build
print('=== .next DIR ===')
import glob, datetime
next_dirs = glob.glob(repo + '/.next/*', recursive=True)
if next_dirs:
    latest = max(os.path.getmtime(d) for d in next_dirs)
    print('Latest .next: ' + str(datetime.datetime.fromtimestamp(latest)))
    # Check if .next exists and is fresh (today 2026-10-15)
    now = datetime.datetime.now()
    print('Now:', now)
    print('.next fresh (today):', datetime.datetime.fromtimestamp(latest).date() == now.date())
print()

# Check ids of users, roles
import sqlite3
conn = sqlite3.connect(repo + '/dev.db')
cur = conn.cursor()
print('=== USERS ===')
for row in cur.execute('SELECT id, email, role FROM users'):
    print(' ', row)
print()
print('=== ROLES ===')
for row in cur.execute('SELECT id, name, description FROM roles'):
    print(' ', row)
print()
print('=== ROLE_PERMISSIONS ===')
for row in cur.execute('SELECT module, action, entity, can FROM role_permissions LIMIT 5'):
    print(' ', row)
print('  total:', cur.execute('SELECT COUNT(*) FROM role_permissions').fetchone()[0])
print()
conn.close()
