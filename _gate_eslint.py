import subprocess
r = subprocess.run(['npx','eslint','.'], cwd='/opt/data/home/workspace/dev/pondok-banat', capture_output=True, text=True, timeout=180)
print('eslint exit:', r.returncode)
print('eslint stdout:', r.stdout[-3000:])
print('eslint stderr:', r.stderr[-1000:])
