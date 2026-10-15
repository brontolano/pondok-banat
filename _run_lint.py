import subprocess, sys
r = subprocess.run(['./node_modules/.bin/eslint', '.'], cwd='/opt/data/home/workspace/dev/pondok-banat', capture_output=True, text=True)
print('STDOUT:', r.stdout[:4000])
print('STDERR:', r.stderr[:2000])
print('EXIT:', r.returncode)
