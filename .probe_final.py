import subprocess
import os

repo = '/opt/data/home/workspace/dev/pondok-banat'
os.chdir(repo)

def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return r.stdout.strip(), r.stderr.strip(), r.returncode

print('=== GIT ===')
out, err, rc = run('git rev-parse HEAD')
print('HEAD:', out)
out, err, rc = run('git rev-list --count HEAD')
print('commit count HEAD:', out)
out, err, rc = run('git rev-list --count origin/main..HEAD')
print('ahead origin/main:', out)
out, err, rc = run('git rev-list --count HEAD..origin/main')
print('behind origin/main:', out)
out, err, rc = run('git ls-files | wc -l')
print('tracked files:', out)
out, err, rc = run('git ls-files --others --exclude-standard | wc -l')
print('untracked files:', out)
print()
print('=== NODE_MODULES ===')
out, err, rc = run('find node_modules -type f 2>/dev/null | wc -l')
print('node_modules files:', out)
out, err, rc = run('find node_modules -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l')
print('node_modules top-level dirs (excl self):', out)
out, err, rc = run('find node_modules -type f -o -type d 2>/dev/null | wc -l')
print('node_modules total entries:', out)
print()
print('=== DEV.DB ===')
db = 'dev.db'
print('exists:', os.path.exists(db))
print('size:', os.path.getsize(db))
