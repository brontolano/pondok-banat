import subprocess
r = subprocess.run(['npx', 'eslint', '.'], cwd='/opt/data/home/workspace/dev/pondok-banat', capture_output=True, text=True, timeout=300)
print('=== ESLINT ===')
print('exit:', r.returncode)
print(r.stdout[-3000:])
print(r.stderr[-3000:])
